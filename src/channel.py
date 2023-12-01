import json
import os
from pprint import pprint
from typing import Any

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv("YOUTUBE_API_KEY")

    # создан специальный объект для работы с API
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут
        подтягиваться по API."""
        self.channel__id = channel_id
        self.channel = (
            self.youtube.channels()
            .list(id=channel_id, part="snippet,statistics")
            .execute()
        )

        self.title = self.channel["items"][0]["snippet"]["title"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.url = f"https://www.youtube.com/channel/channel_id"
        self.id = self.channel["items"][0]["id"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.subscriber_count = self.channel["items"][0]["statistics"][
            "subscriberCount"
        ]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self) -> str:
        """
        Вовращает id канала
        """
        return self.__channel_id

    @classmethod
    def get_service(cls) -> Any:
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        """
        channel_id = os.getenv("YOUTUBE_API_KEY")
        cls.youtube = build("youtube", "v3", developerKey=channel_id)
        return cls.youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        pprint(self.channel)

    def to_json(self, filename: Any) -> Any:
        """
        Функция, сохраняющая в файл значения атрибутов экземпляра Channel
        """
        channel_info = {
            "title": self.title,
            "channel_id": self.__channel_id,
            "description": self.description,
            "url": self.url,
            "count_subscriberCount": self.subscriber_count,
            "video_count": self.video_count,
            "count_views": self.view_count,
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(channel_info, file, indent=4, ensure_ascii=False)

    @channel_id.setter
    def channel_id(self, value):
        self.__channel_id = value
