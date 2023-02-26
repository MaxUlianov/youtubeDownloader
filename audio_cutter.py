from pydub import AudioSegment
import os
import logging


def convert_timestamp(timestamp):
    """
    Convert start-end timestamps into start and end time in milliseconds
    :param timestamp: string tuple ('mm:ss', 'mm:ss')
    :type timestamp: tuple[str, str]
    :return: start: millisecond value integer, end: millisecond value integer
    :return type: tuple[int, int]
    """
    start_time = [int(i) for i in timestamp[0].split(':')]
    end_time = [int(i) for i in timestamp[1].split(':')]

    start_ms = start_time[0] * 60 * 1000 + start_time[1] * 1000
    end_ms = end_time[0] * 60 * 1000 + end_time[1] * 1000

    return start_ms, end_ms


def cut_audio(filename, cut_points, base_path='static/files/'):
    """
    Cut a part of audio file, save to specified location with a
    name '<original name>_start-end'
    :param filename: original file name
    :type filename: str
    :param base_path: path to audio file being cut
    :param cut_points: string tuple (start 'mm:ss', end 'mm:ss')
    :type cut_points: tuple[str, str]
    :return str: name of audio file cut
    """
    save_path = os.path.join(base_path, filename)
    logging.info(f'save path: {save_path}')

    AudioSegment.ffprobe = '/usr/local/bin/ffprobe'

    track = AudioSegment.from_file(f'{save_path}')

    start_time, end_time = convert_timestamp(cut_points)
    logging.info(f'Start: {type(start_time)}: {start_time}; end: {type(end_time)}: {end_time};')

    audio = track[start_time:end_time]

    file_format = 'm4a'

    # if len(filename) > 20:
    #     filename = filename[:20]
    #     print(filename)

    name = filename.replace('.m4a', f'_{cut_points[0]}-{cut_points[1]}.{file_format}')
    save_path = os.path.join(base_path, name)
    logging.info(f'save path: {save_path}')

    audio.export(f'{save_path}', format='mp4')
    return name


def cut_audio_segments(file, timestamps, base_path='static/files/'):
    """
    Cuts multiple parts of audio file, saves to specified location
    :param file: original file name
    :type file: str
    :param timestamps: list of string tuples, defining parts to cut, in format (start 'mm:ss', end 'mm:ss')
    :type timestamps: List
    :param base_path: path to original file location
    :type base_path: str
    :return list: list of names for audio segment files
    """
    # ex_list = {}
    files = []
    for timestamp in timestamps:
        try:
            file_cut = cut_audio(file, timestamp, base_path)
            files.append(file_cut)
        except Exception as e:
            # ex_list[timestamp] = (repr(e))
            logging.info(f'Error when cutting audio: {repr(e)}')

    return files


def get_timestamps(time_input):
    """
    Converting input to timestamps
    :param time_input: string of timestamp pairs in format 'mm:ss mm:ss'
    :return: list of string tuples of timestamps: ('mm:ss', 'mm:ss')
    """
    time_input = time_input.split(' ')
    times = list(zip(time_input[::2], time_input[1::2]))
    logging.info(f'Timestamps: {times}')
    return times


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)

    file = input('Insert filename:\n')
    path = 'static/files'

    time = input('Insert timestamps\n')
    times = get_timestamps(time)

    print(f'File: {file}, timestamps: {times}')

    files = cut_audio_segments(file, times, path)
    print(f'files: {files}')
    os.remove(os.path.join(path, file))
