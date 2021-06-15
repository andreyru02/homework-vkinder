from database.sql import SQL
import config
from errors_bd import errors

bd = SQL('database/bd.db')


def update_favorites(user_id):
    try:
        if bd.user_exists(user_id):
            if bd.get_user_favorites(user_id):  # Если юзер уже в избранном
                bd.update_user(user_id, False)  # То убираем ему статус
                return f'Пользователь {config.URL_VK}{user_id} удален из избранного.'
            else:
                bd.update_user(user_id, True)  # если юзера в избранном не было - добавляем
                return f'Пользователь {config.URL_VK}{user_id} добавлен в избранное.'

        return 'С таким пользователем мы не работали.'
    except Exception as err:
        print(err)
        errors.write_msg(errors.id_user, 'Действие невозможно.')


def get_favorites():
    try:
        return bd.get_users_favorites()
    except Exception as err:
        print(err)
        errors.write_msg(errors.id_user, 'Действие невозможно.')
