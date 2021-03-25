import email
import imaplib
import os
import urllib3
from auto_add_ticket import auto_add_tickets

# Обработка платежей за интернет
def internet_pay(abonent:int, pay_sum:str, trans_num:str):
    try:
        pay_string = '/netup/utm5/bin/utm5_payment_tool -a %d -b %s -e %s -C /netup/utm5/utm5_payment_tool_yandex.cfg' % (abonent, pay_sum, trans_num)
        os.popen(pay_string)
        print('internet_pay-ok','ls: ',abonent, 'sum: ',pay_sum)
    except Exception as inet_pay_except:
        print(f"Ошибка проведения платежа за интернет {inet_pay_except}")

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
def tv_pay_python3(abonent:str, pay_sum:str, trans_num:str, notification_sum:int):
    pay_string = 'http://127.0.0.1/tv-yandex.php?command=pay&account=%s&sum=%s&txn_id=%s' % (abonent, pay_sum, trans_num)
    try:
        response = urllib.request.urlopen(pay_string)
        content = response.read().decode('UTF-8')
        n_cont = content.replace('\ufeff',' ').split()
        amount = int(float(pay_sum))
        # Отправка уведомления если сумма платежа >= сумме вероятной оплате задолжености за ТВ
            if  amount >= notification_sum:
                auto_add_tickets('1','31','л/c: ',body_abonent,'Отправлено через yoo money')
                else:
            pass
        return int(n_cont[0])
    except Exception as tv_pay_except:
        print(f"Ошибка проведения платежа за телевидение {tv_pay_except}")
        
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
                body = part.get_payload(decode=True)
                body_txt=body.decode('utf-8').split('\n')
                body_sum=body_txt[5].split()[1]
                body_trans=body_txt[6].split()[2]
                body_abonent=body_txt[7].split()[2]
                pay_type = body_txt[-2].split()[0]
                print (body_sum,' ',body_trans,' ',body_abonent,' ',pay_type)
                if pay_type == internet_service_alias:
                    pass
                elif pay_type == tv_service_alias:
                    pass
            else:
                continue
