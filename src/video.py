import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            if 'items' in video_response and len(video_response['items']) > 0:
                self.title: str = video_response['items'][0]['snippet']['title']
                self.view_count: int = video_response['items'][0]['statistics']['viewCount']
                self.like_count: int = video_response['items'][0]['statistics']['likeCount']
                self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
            else:
                self.title = None
                self.view_count = None
                self.like_count = None
                self.comment_count = None
        except HttpError:
            self.title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_videos):
        super().__init__(video_id)
        self.playlist_videos = playlist_videos
