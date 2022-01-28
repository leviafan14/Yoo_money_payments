# -*- coding: utf-8 -*-
from yoo_money_payment import get_email
from auth_data import username, password
import fdb

if __name__ == '__main__':
    
    try:
        # Подключение к серверу Atirra
        atirra_connection_test= fdb.connect(dsn='127.0.0.1:ATIRRA', user='SYSDBA', password='masterkey')
        print('OK')
        get_email(username,password,'internet','tv')
    except:
        print('Ошибка', 'Не удалось подключиться к серверу ATIRRA')
    
