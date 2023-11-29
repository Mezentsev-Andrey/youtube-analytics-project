import os
from pprint import pprint

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
        self.channel_id = channel_id
        self.channel = (
            self.youtube.channels()
            .list(id=channel_id, part="snippet,statistics")
            .execute()
        )

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        pprint(self.channel)
