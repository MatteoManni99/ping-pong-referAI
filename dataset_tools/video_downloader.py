import yt_dlp
import ffmpeg
import shutil
VIDEOS_PATH = '../videos'

url = 'https://www.youtube.com/watch?v=c-T30NAhJE0'

ydl_opts = {
    'outtmpl': VIDEOS_PATH + '/' +'%(title)s.%(ext)s',  # nome file
    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(url, download=False)  # solo info, non scarica
    filename = ydl.prepare_filename(info_dict)
    ydl.download([url])

output_file = VIDEOS_PATH + '/' +"output.mp4"
input_file = filename

ffmpeg.input(input_file, ss=90, to=180).output(output_file, c='copy').run()