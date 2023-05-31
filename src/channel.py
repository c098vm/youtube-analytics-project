import json
import os

from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id # id канала
        self.channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"] # название канала
        self.description = self.channel["items"][0]["snippet"]["description"] # описание канала
        self.url = f'https://www.youtube.com/channel/{channel_id}' # ссылка на канал
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"] # количество подписчиков
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"] # количество видео
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"] # общее количество просмотров


    def __str__(self) -> str:
        """
        Возвращает информацю об объекте класса для пользователей
        в формате <название_канала> (<ссылка_на_канал>)
        """
        return f'{self.title} ({self.url})'


    def __add__(self, other):
        """
        Возвращает результат сложения экземпляров класса.
        """
        return int(self.subscriber_count) + int(other.subscriber_count)


    def __sub__(self, other):
        """
        Возвращает результат вычитания экземпляров класса.
        """
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        """
        Возвращает результат сравнения "меньше" экземпляров класса.
        """
        return self.subscriber_count < other.subscriber_count


    def __le__(self, other):
        """
        Возвращает результат сравнения "меньше либо равно" экземпляров класса.
        """
        return self.subscriber_count <= other.subscriber_count


    def __gt__(self, other):
        """
        Возвращает результат сравнения "больше" экземпляров класса.
        """
        return self.subscriber_count > other.subscriber_count


    def __ge__(self, other):
        """
        Возвращает результат сравнения "больше либо равно" экземпляров класса.
        """
        return self.subscriber_count >= other.subscriber_count


    def __eq__(self, other):
        """
        Возвращает результат равенства экземпляров класса.
        """
        return self.subscriber_count == other.subscriber_count



    # @property
    # def channel_id(self):
    #     """
    #     Возвращает атрибут channel_id определяемую при инициализации экземпляра
    #     """
    #     return self.channel_id

    @classmethod
    def get_service(cls) -> object:
        """
        Возвращает экземпляр класса
        """
        return cls.youtube

    def to_json(self, filename):
        """
        Собирает свойства объекта в словарь и сохраняет в json формате в файл
        """
        attr_dict = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(filename, 'w') as file:
            json.dump(attr_dict, file)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
