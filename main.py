from glob import glob
from pydub import AudioSegment

# Достать все файлы в формате .wav
playlist_songs = [AudioSegment.from_wav(mp3_file) for mp3_file in glob("*.wav")]

# Добавить и удалить первый файл в overlay
overlay = playlist_songs.pop(0)

# Комбинировать все файлы
for song in playlist_songs:
    overlay = overlay.overlay(song, position=0)

# Умножить все файлы
do_it_over = overlay * 2
# simple export
file_handle = do_it_over.export("output.wav", format="wav")