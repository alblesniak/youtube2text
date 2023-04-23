import os
import yt_dlp


def get_video_urls(playlist_url):
    ydl_options = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        video_urls = [entry['url'] for entry in playlist_info['entries']]

    return playlist_info['title'], video_urls


def download_audio_from_playlist(playlist_url):
    playlist_name, video_urls = get_video_urls(playlist_url)
    output_directory = playlist_name

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    ydl_options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_directory}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'merge_output_format': 'mp3',  # Ensure the output file is in mp3 format
        'retries': 10,  # Number of times to retry the download in case of errors
        'fragment_retries': 10,  # Number of times to retry a fragment in case of errors
        'ignoreerrors': True,  # Continue downloading the next video in case of errors
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download(video_urls)

    print(
        f"Audio files have been downloaded to the folder: {output_directory}")


if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    download_audio_from_playlist(playlist_url)
