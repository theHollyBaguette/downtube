from pytube import YouTube
from pytube.helpers import RegexMatchError
from sys import argv
from pytube.cli import on_progress
from moviepy.editor import VideoFileClip, AudioFileClip
import os


def main():
    path = "/Users/buro/Downloads"
    temp_path = path + "/.temp"

    try:
        link = argv[1]
    except IndexError:
        print("You need to provide a link")
        quit()

    try:
        yt = YouTube(link, on_progress_callback=on_progress)
    except RegexMatchError as e:
        print("Check your link.", e)
        quit()

    print(link)
    print("Title: ", yt.title)
    print("Views: ", yt.views)
    print("searching...")

    audio_stream = yt.streams.get_audio_only()
    video_stream = yt.streams.filter(adaptive=True, only_video=True).first()

    if audio_stream is None:
        quit("Error: No audio stream found")

    if video_stream is None:
        quit("Error: No video stream found")

    print(audio_stream)
    print(video_stream)

    audio_name = "audio.mp4"
    video_name = "video.mp4"
    file_name = video_stream.default_filename

    open_temp(temp_path)

    audio_stream.download(temp_path, filename=audio_name)
    video_stream.download(temp_path, filename=video_name)

    concatenate_video(
        temp_path + "/" + audio_name, temp_path + "/" + video_name, path, file_name
    )

    cleanup_temp(temp_path, audio_name, video_name)


def cleanup_temp(temp_path, audio_name, video_name):
    print("\nCleanup...")
    try:
        os.remove(temp_path + "/" + audio_name)
        os.remove(temp_path + "/" + video_name)
        os.rmdir(temp_path)
    except OSError as e:
        print(e)


def open_temp(temp_path):
    print("Opening temp...")
    try:
        os.mkdir(temp_path)
    except OSError as e:
        print(e)


def concatenate_video(audio_path, video_path, path, file_name):
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)

    final_clip = video_clip.set_audio(audio_clip)

    final_clip.write_videofile(path + "/" + file_name)


if __name__ == "__main__":
    main()
