import requests
import config


class SearchUsers:
    def __init__(self, token, user_info):
        self.token = token
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

    def get_search_parameters(self):
        """Получаем критерии поиска"""
        print('Введите параметры поиска: ')
        age_from = int(input('Возраст от: '))
        age_to = int(input('Возраст до: '))
        sex = int(input('Пол (Где 1 - женский, 2 - мужской): '))
        status = int(input('Семейное положение:\n'
                           '1 — не женат (не замужем);\n'
                           '2 — встречается;\n'
                           '3 — помолвлен(-а);\n'
                           '4 — женат (замужем);\n'
                           '5 — всё сложно;\n'
                           '6 — в активном поиске;\n'
                           '7 — влюблен(-а);\n'
                           '8 — в гражданском браке: '))

        search_parameters = {
            'age_from': age_from,
            'age_to': age_to,
            'sex': sex,
            'status': status
        }
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
