import json
import os

from googleapiclient.discovery import build

import isodate

class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel_data = self.youtube.channels().list(id=self.__channel_id, part='snippet, statistics').execute()
        self.title = channel_data["items"][0]['snippet']['title']
        self.description = channel_data["items"][0]['snippet']['description']
        self.url = f'https://youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = channel_data["items"][0]['statistics']['subscriberCount']
        self.video_count = channel_data["items"][0]['statistics']['videoCount']
        self.view_count = channel_data["items"][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(info, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def to_json(self, filename):
        with open(filename, 'w', encoding='utf8') as f:
            channel_info = {'Channel_id': self.__channel_id,
                            'Title': self.title,
                            'Description': self.description,
                            'URL': self.url,
                            'Subscribers': self.subscriber_count,
                            'Videos': self.video_count,
                            'Views': self.view_count
                            }
            json.dump(channel_info, f, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        return self.__channel_id
