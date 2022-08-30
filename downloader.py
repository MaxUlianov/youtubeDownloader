from pytube import YouTube
from pytube.cli import on_progress
import os
import logging
from audio_cutter import cut_audio_segments, get_timestamps


def get_video_options(link):
    """
    Get download options for Yt video
    :param link: Yt link
    :return: list of options
    """
    yt = YouTube(link, on_progress_callback=on_progress)
    options = yt.streams.filter(progressive=True, file_extension='mp4')

    return options


def get_audio_options(link):
    """
    Get audio-only download options for Yt video
    :param link: Yt link
    :return: list of options
    """
    yt = YouTube(link, on_progress_callback=on_progress)
    options = yt.streams.filter(only_audio=True, file_extension='mp4')

    return options


def download_video(link, save_path='static/files/', itag=None):
    """
    Download Youtube video
    :param link: Yt link
    :param save_path: file save location
    :param itag: download option tag
    :return: name of video file saved
    """
    yt = YouTube(link, on_progress_callback=on_progress)

    logging.info(yt.streams.filter(progressive=True, file_extension='mp4'))

    if itag is None:
        vid = yt.streams.filter(progressive=True, file_extension='mp4').first()
    else:
        vid = yt.streams.filter(progressive=True, file_extension='mp4').get_by_itag(itag)

    video = vid.download(save_path)
    file_name = os.path.basename(video)

    return file_name


def download_audio_only(link, save_path='static/files/', itag=None):
    """
    Download Youtube video as audio-only file
    :param link: Yt link
    :param save_path: file save location
    :param itag: download option tag
    :return: name of audio file saved
    """

    yt = YouTube(link, on_progress_callback=on_progress)

    logging.info(yt.streams.filter(only_audio=True, file_extension='mp4'))

    if itag is None:
        vid = yt.streams.filter(only_audio=True, file_extension='mp4').last()
    else:
        vid = yt.streams.filter(only_audio=True, file_extension='mp4').get_by_itag(itag)

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
