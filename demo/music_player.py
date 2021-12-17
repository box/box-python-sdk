# coding: utf-8

from random import shuffle
import subprocess
import tempfile
from boxsdk.client import Client
from demo.auth import authenticate


class MusicPlayer:
    def __init__(self, folder_path):
        self._folder_path = folder_path
        self._client = self._get_client()
        self._mp3_files = self._get_all_mp3_files(self._client)
        shuffle(self._mp3_files)

    def _get_client(self):
        oauth, _, _ = self._authenticate()
        return Client(oauth)

    def _authenticate(self):
        return authenticate()

    def _get_all_mp3_files(self, client):
        # music_folder = client.folder(folder_id='0').get_subfolder('music')
        return client.search().query(query='*.mp3', limit=100, offset=0, file_extensions=['mp3'])

    def play(self):
        for item in self._mp3_files:
            temp_file = tempfile.NamedTemporaryFile()
            temp_file.write(item.content())
            item_with_name = item.get()
            print(item_with_name.name)
            subprocess.check_call(['afplay', temp_file.name])


if __name__ == '__main__':
    music_player = MusicPlayer('music')
    music_player.play()
