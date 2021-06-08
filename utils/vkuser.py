import requests
from datetime import date
import config


class VKUser:
    def __init__(self, token):
        self.token = token
        self.params = {
            'access_token': self.token,
            'v': '5.131'
        }

    def get_user_info(self):
        """
        Получает информацию о юзере
        Возвращает словарь с возрастом, полом, городом и семейным положением
        """
        resp = requests.get(config.URL + 'account.getProfileInfo', self.params).json().get('response')
        user_id = resp.get('id')
        bdate = resp.get('bdate').split('.')
        bdate_dict = {
            'year': int(bdate[2]),
            'month': int(bdate[1]),
            'day': int(bdate[0])
        }
        age = self.get_year(bdate_dict)
        sex = resp.get('sex')
        city = resp.get('city').get('id')
        status = resp.get('relation')

        user_info = {
            "id": user_id,
            "age": age,
            "sex": sex,
            "city": city,
            "status": status
        }

        return user_info

    def get_year(self, bdate):
        """Получаем возраст юзера"""
        today = date.today()

        return today.year - bdate.get('year') - ((today.month, today.day) < (bdate.get('month'), bdate.get('day')))
