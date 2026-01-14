import yt_dlp
import shutil
VIDEOS_PATH = '../videos'

url = 'https://www.youtube.com/watch?v=c-T30NAhJE0'

ydl_opts = {
    'outtmpl': VIDEOS_PATH + '/' +'%(title)s.%(ext)s',  # nome file
    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])