import email
import imaplib
import os
import urllib3
import urllib
from auto_add_ticket import auto_add_tickets
from connect_to_atirra import db_connect, get_customer_data, update_service_customer

# Внесение платежей за интернет в биллинг UTM5
def internet_pay(abonent:int, pay_sum:str, trans_num:str):
    try:
        pay_string = "C:\\Program Files\\NetUp\\UTM5\\utm5_payment_tool.exe -a %d -b %s -e %s -C C:\\Program Files\\NetUp\\UTM5\\utm5_payment_tool.cfg" % (abonent, pay_sum, trans_num)
        payment_result = os.popen(pay_string)
        print('internet_pay-ok','ls: ',abonent, 'sum: ',pay_sum, payment_result)
    except Exception as inet_pay_except:
        print(f"Ошибка проведения платежа за интернет {payment_result} {inet_pay_except}")

# Внесение платежей за ТВ в биллинг Atirra Для python2.7    
def tv_pay_python2(abonent:int, db_username:str, db_password:str):
    pay_string = 'http://127.0.0.1/tv-yandex.php?command=pay&account=%d&sum=%s&txn_id=%s' % (abonent, pay_sum, trans_num)
    urllib2.urlopen(pay_string).read()
    con = kinterbasdb.connect(dsn='192.168.0.13:ATIRRA', user=db_username, password=db_password, charset='win1251')
    cur = con.cursor()
    cur.execute(sql)
    sql_data = cur.fetchall()
    cur.close()
    con.close()
    print('tv_pay-ok', 'ls: ', abonent, 'sum: ', pay_sum)
    
# Внесение платежей за ТВ в биллинг Atirra Для python3
def tv_pay_python3(abonent:int, pay_sum:str, trans_num:str, payment_date:str, body_notice:str, notification_sum:int) -> int:
    result_payment = int()
    global customer_adress
    try:
        amount = int(float(pay_sum))
        pay_string = 'http://localhost/tv-yandex.php?command=pay&account=%d&sum=%s&txn_id=%s&txn_date=%s' % (abonent, pay_sum, trans_num, payment_date)
        response = urllib.request.urlopen(pay_string)
        content = response.read().decode('UTF-8')
        n_cont = content.replace('\ufeff',' ').split()
        # Проверка результата внесения платежа
        result_payment = int(n_cont[0])
        
        # Если платеж не удалось провести, то добавляется заявка с номером извещения
        if int(result_payment) != 0:
            auto_add_tickets('1','43','Изв. № ',str(body_notice),'Отправлено через yoo money')
            return result_payment
        else:
            print(f"Платеж проведен успешно {result_payment}")
            
        # Отправка уведомления если сумма платежа >= сумме вероятной оплате задолжености за ТВ
        if  amount >= notification_sum:
            # Получение адреса пользователя
            try:
                adress_customer = get_customer_data(int(abonent),'Disable')
                auto_add_tickets('1','43','',str(adress_customer),'Отправлено через yoo money')
                print('return',adress_customer)
            # Если не удалось получить адрес пользователя
            except Exception as e:               
                auto_add_tickets('1','43','л/c: ',str(abonent),'Отправлено через yoo money')
                
        else:
            pass
        
        return int(result_payment)
    
    except Exception as tv_pay_except:
        print(f"Ошибка проведения платежа за телевидение {tv_pay_except}\n{pay_sum}  {abonent} {trans_num}")
        
# Чтение входящей почты
def get_email(username:str, password:str, internet_service_alias:str, tv_service_alias:str):
    server = imaplib.IMAP4_SSL('imap.yandex.ru')
    # Авторизация в почтовом ящике
    server.login(username, password)
    # Выбор папки для обработки писем
    server.select('Test')
    # Список сообщений
    rv, data = server.search(None, 'ALL')
    # Строка номеров писем
    ids = data[0]
    # Разделение ID писем
    id_list = ids.split()
    # ID последнего письма
    latest_email_id = id_list[0]
    # Получаем все непрочитанные письма (ALL/UNSEEN)
    result, data = server.uid('search', None, "UNSEEN")
    # Получаем количество платежей
    i = len(data[0].split())
    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = server.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                # Получение тела письма
                body = part.get_payload(decode=True)
                # Получение содержимого тела письма
                body_txt = body.decode('utf-8').split('\n')
                # Получение даты платежа
                payment_date = body_txt[4].split()[2]
                # Получение номера транзакции
                body_trans = body_txt[6].split()[2]
                # Получение номера извещения платежа
                body_notice = str(body_txt[0].split()[2])
                # Получение типа платежа tv/internet
                pay_type = body_txt[-2].split()[0]
                # Получение суммы платежа
                body_sum = body_txt[5].split()[1]
                body_sum = body_sum.split()[0]
                
                # Получение и проверка корректности лицевого счета
                try:
                    body_abonent = body_txt[7].split()[2]
                    body_abonent = int(body_abonent)
                # Если лицевой счет некорректен, то в заявку передается номер извещения
                except Exception as e:
                    print(f'Лицевой счет не является числом: {body_abonent}\n{e}')
                    auto_add_tickets('1','44','Изв. № ',str(body_notice),'Отправлено через yoo money')
                    continue
                
                # Если платеж за интернет
                if pay_type == internet_service_alias:
                    inet_result = internet_pay(int(body_abonent), str(body_sum), str(body_trans))
                    print(inet_result)
                # Если платеж за телевидение
                elif pay_type == tv_service_alias:
                    tv_pay_python3(int(body_abonent), str(body_sum), str(body_trans), str(payment_date), str(body_notice), 1000)
            else:
                continue
