import datetime
import isodate
import os

from googleapiclient.discovery import build


class PlayList:
    """
    Класс для плейлиста YouTube.
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.response = PlayList.youtube.playlists().list(id=self.playlist_id,
                                                          part='contentDetails,snippet',
                                                          maxResults=50,
                                                          ).execute()

        self.title: str = self.response["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'  # ссылка на канал

    @property
    def total_duration(self):
        """
        Метод с геттером подсчитывает общую продолжительность всех видеороликов плейлиста.
        """
        timelist = []
        playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                part='contentDetails,snippet',
                                                                maxResults=50,
                                                                ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        videos_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(video_ids)
                                                         ).execute()
        for video in videos_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            timelist.append(duration)
        return sum(timelist, datetime.timedelta())


    def show_best_video(self):
        """
        Метод возвращает url-адрес видеоролика с максимальным количеством лайков.
        """
        playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                part='contentDetails,snippet',
                                                                maxResults=50,
                                                                ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        videos_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(video_ids)
                                                         ).execute()
        max_video_likes = 0
        max_video_id = None
        for video in videos_response['items']:
            video_likes_count = int(video['statistics']['likeCount'])
            if video_likes_count > max_video_likes:
                max_video_likes = video_likes_count
                max_video_id = video['id']
        return f'https://youtu.be/{max_video_id}'

