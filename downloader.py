from pytube import YouTube
from pytube.cli import on_progress
import os


save_path = ''

# title = yt.title


def get_video_options(link):
    yt = YouTube(link, on_progress_callback=on_progress)

    options = yt.streams.filter(progressive=True, file_extension='mp4')

    return options


def download_video(link, SAVE_PATH):
    yt = YouTube(link, on_progress_callback=on_progress)

    print(yt.streams.filter(progressive=True, file_extension='mp4'))
    vid = yt.streams.filter(progressive=True, file_extension='mp4').first()
    # choose which stream to download with itag=ID in stream attributes
    # vid = yt.streams.get_by_itag(22)

    vid.download(SAVE_PATH)


def download_audio_only(link, SAVE_PATH):

    yt = YouTube(link, on_progress_callback=on_progress)

    print(yt.streams.filter(only_audio=True, file_extension='mp4'))
    vid = yt.streams.filter(only_audio=True, file_extension='mp4').last()

    file = vid.download(SAVE_PATH)

    base, ext = os.path.splitext(file)
    new_file = base + '.m4a'
    os.rename(file, new_file)


if __name__ == '__main__':
    lnk = ''

    # download_audio_only(lnk, save_path)
    # download_video(lnk, save_path)
    save_path = input('Enter save path:\n')

    opt = get_video_options(lnk)
    # print(opt)
    # print(opt[0].itag)
