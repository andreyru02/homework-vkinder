import json
import vk_api
from vk_api.longpoll import VkLongPoll
import requests
from random import randrange
import os
import config
from database import sql

vk = vk_api.VkApi(token=config.TOKEN_BOT)
longpoll = VkLongPoll(vk)
info = {'errors': {'user_id': []}}
error_stop_limit = 1

params = {
    'access_token': config.TOKEN_USER,
    'v': '5.131'
}
resp = requests.get(config.URL + 'account.getProfileInfo', params).json().get('response')
id_user = resp.get('id')


def write_bd():
    """
    Функция запускается при запуске бота
    Проверяет, пустой ли json, если не пустой, то записывает данные в БД
    """
    bd = sql.SQL('database/bd.db')
    try:
        print('Проверка файла с ошибками.')
        with open('errors_bd/errors.json', encoding='utf-8') as f:
            data = json.load(f)
            print('Произведена запись в базу данных следующих пользователей:')
            for user in data['errors']['user_id']:
                bd.add_user(user)
                print(user)
        bd.close()
        os.remove('errors_bd/errors.json')
    except FileNotFoundError:
        print('Ошибок не найдено.')


def write_json(err, user_id):
    """Если произошла ошибка записи в БД, то пишем в json и сообщаем пользователю в чат"""
    info["errors"]['user_id'].append(user_id)
    with open('errors_bd/errors.json', 'w') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    global error_stop_limit
    if error_stop_limit == 1:
        print(f'Произошла ошибка: {err}')

        send_err_msg()
        error_stop_limit += 1


def check_json(user_id, err):
    try:
        with open('errors_bd/errors.json', encoding='utf-8') as f:
            data = json.load(f)
            if user_id not in data['errors']['user_id']:
                write_json(err, user_id)
                return True
            return False
    except FileNotFoundError:
        write_json(err, user_id)
        return True


def send_err_msg():
    """Отправляет сообщение об ошибке пользователю в чат"""
    write_msg(id_user, 'Произошла ошибка при взаимодействии с базой данных\n'
                       'Отсутствует возможность добавления пользователей в избранное.')


def write_msg(user_id, message):
    """Отправляет сообщение"""
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})
