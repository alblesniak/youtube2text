import os
import yt_dlp


def get_video_urls(channel_url, keyword):
    ydl_options = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        channel_info = ydl.extract_info(channel_url, download=False)
        video_urls = [entry['url'] for entry in channel_info['entries']
                      if keyword.lower() in entry['title'].lower()]

    return channel_info['title'], video_urls


def download_audio_from_videos(channel_url, keyword):
    channel_name, video_urls = get_video_urls(channel_url, keyword)
    output_directory = channel_name

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
        'merge_output_format': 'mp3',
        'retries': 10,
        'fragment_retries': 10,
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download(video_urls)

    print(
        f"Audio files have been downloaded to the folder: {output_directory}")


if __name__ == "__main__":
    channel_url = "https://www.youtube.com/@Langustanapalmie/videos"
    keyword = "Wstawaki"
    download_audio_from_videos(channel_url, keyword)
