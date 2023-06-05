import os
from googleapiclient.discovery import build


class Video:
    """Класс для видео из ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id  # id видео
        self.video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=video_id).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']  # название видео
        self.url: str = f'https://www.youtube.com/watch?v={video_id}'  # url-адрес видео
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']  # количество просмотров
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']  # количество лайков

    def __str__(self):
        """ Функция для отображения информации об  объекте для пользователей"""
        return self.video_title


class PLVideo(Video):
    """Класс для видео с плейлистом"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id  # id плейлиста
