import os
from typing import Any

from googleapiclient.discovery import build  # type: ignore


class Video:
    """
    Класс по видео из YouTube.
    """

    def __init__(self, video_id: Any) -> None:
        self.video_id = video_id
        self.request = self.get_service().videos().list(part="snippet,contentDetails,statistics", id=self.video_id)
        self.response = self.request.execute()
        self.name = self.response["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/channel/{self.video_id}"
        self.view_count = self.response["items"][0]["statistics"]["viewCount"]
        self.like_count = self.response["items"][0]["statistics"]["likeCount"]

    @classmethod
    def get_service(cls) -> build:
        """
        Класс-метод, возвращающий объект для работы с YouTube API.
        """
        channel_id = os.getenv("YOUTUBE_API_KEY")
        cls.youtube = build("youtube", "v3", developerKey=channel_id)  # type: ignore
        return build("youtube", "v3", developerKey=channel_id)

    def __str__(self) -> str:
        """
        Возвращает названия видео.
        """
        return f"{self.name}"


class PLVideo(Video):
    """
    Класс для видео по плейлисту из YouTube-канала.
    """

    def __init__(self, video_id: str, playlist_id: Any) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = (
            self.get_service()
            .playlistItems()
            .list(
                playlistId=self.playlist_id,
                part="contentDetails",
                maxResults=50,
            )
            .execute()
        )
