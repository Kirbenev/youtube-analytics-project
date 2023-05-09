import os, datetime
from src.video import Video
from googleapiclient.discovery import build

class PlayList():
    """Класс для ютуб-плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""

        self.__playlist_id = playlist_id
        playlist = self.youtube.playlists().list(part="snippet", id=self.__playlist_id).execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    def get_videos_in_pl(self):
        """Функция возвращает список объектов класса Video находящихся в данном плейлисте"""
        videos_in_pl = []
        playlist_response = self.youtube.playlistItems().list(part="contentDetails, snippet",
                                                         playlistId=self.__playlist_id).execute()
        for item in playlist_response["items"]:
            videos_in_pl.append(Video(item["contentDetails"]["videoId"]))

        return videos_in_pl

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def total_duration(self):
        """ Функция возвращает общее время всех видео в плей-листе """
        total_duration = datetime.timedelta(hours=0, minutes=0, seconds=0)

        for video in self.get_videos_in_pl():
            total_duration += video.duration

        return total_duration

    def show_best_video(self):
        """Функция возвращает ссылку на видео из плейлиста, которое имеет наибольшее количество просмотров"""
        best_video_url = None
        best_video_likes = 0

        for video in self.get_videos_in_pl():
            if video.like_count > best_video_likes:
                best_video_likes = video.like_count
                best_video_url = video.url

        return best_video_url