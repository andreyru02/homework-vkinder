from utils.vkuser import VKUser
from utils.search_users import SearchUsers
from utils.message import Message
import config


if __name__ == '__main__':
    token_user = config.TOKEN_USER
    token_bot = config.TOKEN_BOT
    user = VKUser(token_user)  # Инициализируем пользователя
    search = SearchUsers(user.token, user.get_user_info())  # Ищем пользователей
    send_message = Message(token_bot, user.token, search.get_user_id())
    send_message.get_msg()  # Ждем сообщения начать и отправляем фото
