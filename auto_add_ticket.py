import requests
from datetime import datetime
from bs4 import BeautifulSoup

#auto_add_tickets(тип заявки:str,класс_заявки:str,строка идущая перед лиц.счетом:str,лицевой счет:str,Описание заявки:str):
# Функция автоматического добавления заявки если сумма соответсвтует условию
def auto_add_tickets(type_ticket:str,class_ticket:str,ls_prefix:str,ls:str,descr_ticket:str):
    # Текущая дата
    current_date = str(datetime.now()).split()[0]
    ls = str(ls_prefix+ls)
    # Адрес скрипта добавления заявки
    url_add_ticket = 'http://g90890zj.beget.tech/new_ticket_back.php'
    # Адрес скрипта авторизации
    url_enter = 'http://g90890zj.beget.tech/check.php'

    # Данные авторизации на сайте
    data_enter = {'t_login':'010', 'password':'801623ab'}
    # Данные новой заявки
    data_add_ticket = {'s_type':type_ticket,'t_tarif':'','s_class':class_ticket,'t_time':'','d_date':current_date,
        't_adress':ls, 'n_phone':'','t_descr':descr_ticket,
        's_status':'','s_state':''}
    
    # Загаловки запросов
    headers_requests = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

    # Авторизация на сайте
    try:
        # Запрос на авторизацию пользователя
        response_enter = requests.post(url=url_enter, headers=headers_requests, data=data_enter)
        # Куки пользователя после авторизации - необходимо для добавления заявки
        response_enter_cookies = response_enter.cookies

        # Если запрос не удался
        if str(response_enter) != '<Response [200]>':
            print('Не удалось авторизироваться на сайте')
            exit()
        else:
            pass
    except Exception as e:
        print('Ошибка при выполнении запроса авторизации')
        exit()
        
    # Добавление заявки
    try:
        # Запрос на добавление заявки
        response_add_ticket = requests.post(url=url_add_ticket, headers=headers_requests, cookies=response_enter_cookies, data=data_add_ticket)

        # Проверка, удалось ли добавить заявку 
        result = response_add_ticket.text
        soup = BeautifulSoup(result,'html.parser')
        item = soup.find('td', text=ls)
        if len(item) == 0:
            print('Не удалось добавить заявку')
            exit()
        else:
            pass
        
       # Если запрос не удался 
        if str(response_add_ticket) != '<Response [200]>':
            print('Не удалось добавить заявку')
            exit()
        else:
            pass
    except Exception as e:
        print('Не удалось добавить заявку')
        exit()
        
#auto_add_tickets('1','31','л/с: ','1060','Добавлено скриптом Сберабанк.Реестры')
