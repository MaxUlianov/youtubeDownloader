from pytube import YouTube
from pytube.cli import on_progress
import os
import logging
from zipfile import ZipFile
from audio_cutter import cut_audio_segments, get_timestamps
from video_cutter import cut_video_segments


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


def get_options(link, a_only=False):
    if a_only:
        return get_audio_options(link)
    elif not a_only:
        return get_video_options(link)


def download_video(link, itag=None, save_path='static/files/'):
    """
    Download Youtube video
    :param link: Yt link
    :param save_path: file save location
    :param itag: download option tag
    :return str: name of video file saved
    """
    yt = YouTube(link, on_progress_callback=on_progress)

    # logging.info(yt.streams.filter(progressive=True, file_extension='mp4'))

    if itag is None:
        vid = yt.streams.filter(progressive=True, file_extension='mp4').first()
    else:
        vid = yt.streams.filter(progressive=True, file_extension='mp4').get_by_itag(itag)

    video = vid.download(save_path)
    file_name = rename_file(video, '.mp4')

    logging.info(f'Saved video file name: {file_name}')
    return file_name


def download_audio_only(link, itag=None, save_path='static/files/'):
    """
    Download Youtube video as audio-only file
    :param link: Yt link
    :param save_path: file save location
    :param itag: download option tag
    :return: name of audio file saved
    """

    yt = YouTube(link, on_progress_callback=on_progress)

    # logging.info(yt.streams.filter(only_audio=True, file_extension='mp4'))

    if itag is None:
        vid = yt.streams.filter(only_audio=True, file_extension='mp4').last()
    else:
        vid = yt.streams.filter(only_audio=True, file_extension='mp4').get_by_itag(itag)

    file = vid.download(save_path)

    file_new = rename_file(file, '.m4a')
    logging.info(f'Saved audio file name: {file_new}')
    return file_new


def rename_file(file: str, ext=''):
    dir = os.path.dirname(file)
    filename = os.path.basename(file)

    if len(filename) > 20:
        filename = filename[:20]

    file_new = os.path.join(dir, filename) + ext
    os.rename(file, file_new)
    return file_new


def make_archive(file_list):
    name = '/' + os.path.basename(file_list[0][:-16]) + '.zip'
    archive_name = os.path.abspath('static/files' + name)
    # print(archive_name)
    with ZipFile(archive_name, 'w') as archive:
        for file in file_list:
            archive.write(file, os.path.basename(file))
    return os.path.abspath(archive_name)


def download_controller(link, timestamps, itag=None, a_only=False, path=None):
    dl_file = ''

    if a_only:
        dl_file = download_audio_only(link, itag)

        if timestamps:
            ts = get_timestamps(timestamps)

            try:
                dl_files = cut_audio_segments(dl_file, ts)
                archive = make_archive(dl_files)

                os.remove(dl_file)
                for file in dl_files:
                    os.remove(file)
                return archive
            except Exception as e:
                logging.debug(f'Error in audio cutter: {repr(e)}; returning full audio')
                return dl_file

    elif not a_only:
        dl_file = download_video(link, itag)

        if timestamps:
            ts = get_timestamps(timestamps)
            dl_files = cut_video_segments(dl_file, ts)
            archive = make_archive(dl_files)

            os.remove(dl_file)
            for file in dl_files:
                os.remove(file)
            return archive
    return dl_file


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)
    # for testing purposes and for cli usage

    lnk = input('Insert link:\n')
    path = 'static/files'

    aud_only = input('Audio only? y/n\n')
    if aud_only == 'y':
        a_o = True
    else:
        a_o = False

    opt = get_options(lnk, a_o)

    print(opt)
    choice_tag = input('\nInsert itag for option from list above:\n')

    if a_o:
        time = input('Insert timestamps, format 00:00 00:00 \n')
    else:
        time = None

    files = download_controller(lnk, time, itag=choice_tag, a_only=a_o)
    print(files)
