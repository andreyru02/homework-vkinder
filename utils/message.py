from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from utils.search_photo import Photo
import config
from utils.favorites import update_favorites, get_favorites


class Message(Photo):
    def __init__(self, token_bot, token_user, users):
        super().__init__(token_user, users)
        self.token_bot = token_bot
        self.vk = vk_api.VkApi(token=self.token_bot)
        self.longpoll = VkLongPoll(self.vk)

    def top_photo(self):
        photo = Photo(self.token, self.users)
        search_top_photo = photo.get_top_photo()
        return search_top_photo

    def instructions(self):
        txt = 'Привет!\n' \
              'Vkinder - чат-бот ищущий людей на основании введенных поисковых данных.\n' \
              'Сейчас я отправлю первого человека подходящего под критерии поиска.\n' \
              'Для того, что бы отправить следующего человека напиши в чат "далее".\n' \
              'Что бы добавить пользователя в избранное отправь ссылку в чат.\n' \
              'Что бы посмотреть список избранных - напиши в чат "избранные".'
        return txt

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def write_attachment(self, user_id, attachment):
        self.vk.method('messages.send', {'user_id': user_id, 'attachment': attachment, 'random_id': randrange(10 ** 7)})

    def get_msg(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text.lower()

                    if request == 'начать':
                        self.write_msg(event.user_id, self.instructions())
                        for link, photos in self.top_photo().items():
                            for photo in photos:
                                self.write_attachment(event.user_id, photo)
                            self.write_attachment(event.user_id, link)
                    if request == 'далее':
                        for link, photos in self.top_photo().items():
                            for photo in photos:
                                self.write_attachment(event.user_id, photo)
                            self.write_attachment(event.user_id, link)

                    if request[:17] == config.URL_VK:  # добавляем/удаляем в избранное
                        self.write_msg(event.user_id, update_favorites(request[17:]))

                    if request == 'избранные':  # отправляем в чат список из избранных
                        favorites = get_favorites()
                        for favorit in favorites:
                            self.write_msg(event.user_id, config.URL_VK + str(favorit[0]))
