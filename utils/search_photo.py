import requests
import config
from database import sql


class Photo:
    def __init__(self, token, users):
        self.token = token
        self.bd = sql.SQL('database/bd.db')
        self.users = users
        self.params = {
            'access_token': self.token,
            'v': 5.131
        }

    def get_top_photo(self, album_id='profile'):
        """
        Получаем ссылку и топ-3 фотографии
        dict = {user_link: [photo_link, photo_link, photo_link]}
        """
        for user in self.users:
            if not self.write_user_bd(user):  # если пользователя в базе нет - добавляем,
                continue  # если есть - пропускаем.
            photos_params = {
                'owner_id': user,
                'album_id': album_id,
                'extended': 1,
                'rev': 1
            }
            res = requests.get(config.URL + 'photos.get', params={**self.params, **photos_params}).json()
            if 'error' in res:
                if res['error']['error_code'] == 200:
                    print(f'Access denied for user {user}!')
                    continue
            elif len(res['response']['items']) == 0:
                print(f'User album {user} is null!')
                continue

            #  получение url фотографий в макс. размере
            photo_url_dick = {}
            for photo in res['response']['items']:
                photo_url = photo['sizes'][-1]['url']
                likes = photo['likes']['count']
                if likes not in photo_url_dick:
                    photo_url_dick[likes] = photo_url
                else:
                    photo_url_dick[likes + 1] = photo_url

            #  получаем топ-3 фотографии
            link = config.URL_VK + str(user)
            top_photo_key = sorted(photo_url_dick, reverse=True)[:3]
            top_photo = {}
            top_photo_list = []
            for t_photo in top_photo_key:
                top_photo_list.append(photo_url_dick.get(t_photo))
                top_photo[link] = top_photo_list
            return top_photo

    def write_user_bd(self, user_id):
        """Если пользователя в базе нет, то добавляем его"""
        if not self.bd.user_exists(user_id):
            self.bd.add_user(user_id)
            return True
        return False
