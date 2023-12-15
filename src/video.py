import os
from typing import Any

from googleapiclient.discovery import build  # type: ignore


class Video:
    """
    Класс по видео из YouTube.
    """

    def __init__(self, video_id: Any) -> None:
        try:
            self.video_id = video_id
            youtube = self.get_service()
            self.video = (
                youtube.videos()
                .list(part="snippet,statistics,contentDetails,topicDetails", id=self.id_video)
                .execute()
            )
            self.title = self.video["items"][0]["snippet"]["title"]
            self.request = self.get_service().videos().list(part="snippet,contentDetails,statistics", id=self.video_id)
            self.response = self.request.execute()
            self.name = self.response["items"][0]["snippet"]["title"]
            self.url = "https://www.youtube.com/watch?v=" + self.video_id
            self.view_count = self.response["items"][0]["statistics"]["viewCount"]
            self.like_count = self.response["items"][0]["statistics"]["likeCount"]
        except Exception:
            self.video_id = video_id
            self.video = None
            self.title = None
            self.request = None
            self.response = None
            self.name = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"

    @classmethod
    def get_service(cls) -> build:
        """
        Класс-метод, возвращающий объект для работы с YouTube API.
        """
        channel_id = os.getenv("YOUTUBE_API_KEY")
        cls.youtube = build("youtube", "v3", developerKey=channel_id)  # type: ignore
        return build("youtube", "v3", developerKey=channel_id)


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
