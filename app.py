import os
import yt_dlp
import requests
from PIL import Image
from io import BytesIO

output_dir = input("Enter the directory where you want to save the files (press Enter for default './downloads'): ").strip()
if not output_dir:
    output_dir = "downloads"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{output_dir}/%(title)s.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'writethumbnail': True,
        'embedthumbnail': True,
        'postprocessor_args': [
            '-metadata', 'title=%(title)s',
            '-metadata', 'artist=%(uploader)s',
            '-metadata', 'album=%(uploader)s',
        ],
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        song_title = info_dict.get('title', 'unknown')
        thumbnail_url = info_dict.get('thumbnail', '')

    mp3_filename = f"{output_dir}/{song_title}.mp3"
    
    if thumbnail_url:
        download_thumbnail(thumbnail_url, song_title)

    print(f"\nDownloaded: {mp3_filename}")

def download_thumbnail(thumbnail_url, song_title):
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image_path = f"{output_dir}/{song_title}.jpg"
        image.save(image_path, "JPEG")
        print(f"Thumbnail saved: {image_path}")
    else:
        print("Failed to download thumbnail.")

if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ")
    download_youtube_audio(video_url)