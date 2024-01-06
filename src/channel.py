import os

from dotenv import load_dotenv

load_dotenv()

YT_API_KEY = os.getenv("YOUTUBE_API_KEY")

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.YT_API_KEY = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.YT_API_KEY)
