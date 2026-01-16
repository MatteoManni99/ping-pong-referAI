import yt_dlp
import ffmpeg
import json

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

video_to_download = "youtube_video_2"
url = config_data[video_to_download]

ydl_opts = {
    'outtmpl': config_data["PATH_VIDEOS"] + '/' +'%(title)s.%(ext)s',  # nome file
    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(url, download=False)  # solo info, non scarica
    filename = ydl.prepare_filename(info_dict)
    ydl.download([url])

output_file = config_data["PATH_VIDEOS"] + '/' + video_to_download + ".mp4"
input_file = filename

ffmpeg.input(input_file, ss=0, to=20).output(output_file, c='copy').run()