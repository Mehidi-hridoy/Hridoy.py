from typing import Dict, Any
import yt_dlp
import os

# Path to save all downloads
download_folder =  r"D:\Quran Tilawat"
os.makedirs(download_folder, exist_ok=True)  # Create folder if it doesn't exist

# Path to FFmpeg
ffmpeg_path = r"C:\Users\hrido\Downloads\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin"

def download_from_youtube(url: str, audio_only: bool = False):
    ydl_opts: Dict[str, Any] = {
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save in your folder
        'ffmpeg_location': ffmpeg_path,
        'noplaylist': True,  # <-- Add this line to ignore playlists
    }

    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    choice = input("Download (a)udio or (v)ideo? [a/v]: ").lower()

    if choice == 'a':
        print(f"Downloading audio as MP3 into '{download_folder}'...")
        download_from_youtube(url, audio_only=True)
    elif choice == 'v':
        print(f"Downloading best quality video into '{download_folder}'...")
        download_from_youtube(url, audio_only=False)
    else:
        print("Invalid choice. Please enter 'a' or 'v'.")
