import os
import datetime

import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist = youtube.playlists().list(part='snippet', id=playlist_id).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()

    @property
    def total_duration(self):
        duration = datetime.timedelta(seconds=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        for video in self.video_response['items']:
            video['statistics']['likeCount'] = int(video['statistics']['likeCount'])
        best_video_id = sorted(self.video_response['items'],
                               key=lambda x: x['statistics']['likeCount'],
                               reverse=True)[0]['id']
        return f'https://youtu.be/{best_video_id}'
