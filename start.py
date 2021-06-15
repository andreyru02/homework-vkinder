from utils.vkuser import VKUser
from utils.search_users import SearchUsers
from utils.message import Message
from errors_bd import errors
import config


if __name__ == '__main__':
    token_user = config.TOKEN_USER
    token_bot = config.TOKEN_BOT
    errors.write_bd()  # Проверяет наличие файла с ошибками, если файл не пустой - пишет в базу
    user = VKUser(token_user)  # Инициализируем пользователя
    search = SearchUsers(user.token, token_bot, user.get_user_info())  # Ищем пользователей
    send_message = Message(token_bot, user.token, search.get_user_id())
    send_message.get_msg()  # Ждем сообщения начать и отправляем фото
