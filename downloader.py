from pytube import YouTube
from pytube.cli import on_progress
import os
import logging
from audio_cutter import cut_audio_segments, get_timestamps


def get_video_options(link):
    yt = YouTube(link, on_progress_callback=on_progress)

    options = yt.streams.filter(progressive=True, file_extension='mp4')

    return options


def get_audio_options(link):
    yt = YouTube(link, on_progress_callback=on_progress)

    options = yt.streams.filter(only_audio=True, file_extension='mp4')

    return options


def download_video(link, save_path='static/files/'):
    yt = YouTube(link, on_progress_callback=on_progress)

    logging.info(yt.streams.filter(progressive=True, file_extension='mp4'))
    vid = yt.streams.filter(progressive=True, file_extension='mp4').first()
    # choose which stream to download with itag=ID in stream attributes
    # vid = yt.streams.get_by_itag(22)

    vid.download(save_path)


def download_audio_only(link, save_path='static/files/'):

    yt = YouTube(link, on_progress_callback=on_progress)

    logging.info(yt.streams.filter(only_audio=True, file_extension='mp4'))
    vid = yt.streams.filter(only_audio=True, file_extension='mp4').last()

    file = vid.download(save_path)

    base, ext = os.path.splitext(file)
    new_file = base + '.m4a'
    os.rename(file, new_file)

    return new_file


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)

    lnk = input('Insert link: \n')
    path = '/Users/MaxUlianov/Downloads/'

    opt = get_audio_options(lnk)

    logging.info(f'{opt}')
    c = input('Confirm?')
    file = download_audio_only(lnk, path)

    time = input('Insert timestamps \n')
    times = get_timestamps(time)

    c = input('Confirm?')
    cut_audio_segments(file, times, path)
