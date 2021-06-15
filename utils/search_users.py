import requests
import config
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import time
from utils.txt import *


class SearchUsers:
    def __init__(self, token, token_bot, user_info):
        self.token = token
        self.token_bot = token_bot
        self.vk = vk_api.VkApi(token=self.token_bot)
        self.longpoll = VkLongPoll(self.vk)
        self.users = None
        self.users_list = None
        self.search_params = self.get_search_parameters()
        self.params = {
            'count': 1000,
            'age_from': self.search_params.get('age_from'),
            'age_to': self.search_params.get('age_to'),
            'sex': self.search_params.get('sex'),
            'city': user_info.get('city'),
            'status': self.search_params.get('status'),
            'access_token': self.token,
            'v': 5.131
        }

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def get_search_parameters(self):
        """Получаем критерии поиска"""
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text.lower()

                    if request == 'начать':
                        self.write_msg(event.user_id, step_1())
                        time.sleep(3)
                        self.write_msg(event.user_id, instructions())
                        time.sleep(3)
                        self.write_msg(event.user_id, step_2())
                        self.write_msg(event.user_id, '1) Возраст от:\n'
                                                      '2) Возраст до:\n'
                                                      '3) Пол (Где 1 - женский, 2 - мужской): \n'
                                                      '4) Семейное положение:\n'
                                                      '1 — не женат (не замужем);\n'
                                                      '2 — встречается;\n'
                                                      '3 — помолвлен(-а);\n'
                                                      '4 — женат (замужем);\n'
                                                      '5 — всё сложно;\n'
                                                      '6 — в активном поиске;\n'
                                                      '7 — влюблен(-а);\n'
                                                      '8 — в гражданском браке: ')

                if event.to_me:
                    request = event.text.lower()
                    if request != 'начать':
                        resp_params = request.split(', ')

                        search_parameters = {
                            'age_from': int(resp_params[0]),
                            'age_to': int(resp_params[1]),
                            'sex': int(resp_params[2]),
                            'status': int(resp_params[3])
                        }
                        self.write_msg(event.user_id, 'Ответы приняты. Для поиска пары напиши "Поиск".')
                        return search_parameters

    def get_user_id(self):
        """Возвращает список с ИД найденных пользователей"""
        # Получаем 1000 найденных пользователей на основании критерия поиска
        self.users = requests.get(config.URL + 'users.search', self.params).json().get('response').get('items')
        users_list = []
        for user in self.users:
            if user.get('is_closed') is False:
                users_list.append(user.get('id'))
        return users_list
