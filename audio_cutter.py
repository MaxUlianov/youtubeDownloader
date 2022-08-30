from pydub import AudioSegment
import os
import logging


def convert_timestamp(timestamp):
    """
    Convert start-end timestamps into start and end time in milliseconds
    :param timestamp: string tuple ('mm:ss', 'mm:ss')
    :return: start: millisecond value integer, end: millisecond value integer
    """
    start_time = [int(i) for i in timestamp[0].split(':')]
    end_time = [int(i) for i in timestamp[1].split(':')]

    start_ms = start_time[0] * 60 * 1000 + start_time[1] * 1000
    end_ms = end_time[0] * 60 * 1000 + end_time[1] * 1000

    return start_ms, end_ms


def cut_audio(filename, cut_points, base_path='static/files/'):
    """
    Cut a part of audio file, save to specified location with a name 'original name -start-end'
    :param filename: original file name
    :param base_path: path to audio file being cut
    :param cut_points: string tuple (start 'mm:ss', end 'mm:ss')
    """
    save_path = os.path.join(base_path, filename)
    logging.info(f'save path: {save_path}')

    track = AudioSegment.from_file(f'{save_path}')

    start_time, end_time = convert_timestamp(cut_points)
    logging.info(f'Start: {type(start_time)}: {start_time}; end: {type(end_time)}: {end_time};')

    audio = track[start_time:end_time]

    file_format = 'mp3'
    name = filename.replace('.m4a', f' {cut_points[0]}-{cut_points[1]}.{file_format}')
    save_path = os.path.join(base_path, name)
    logging.info(f'save path: {save_path}')

    audio.export(f'{save_path}', format=file_format)


def cut_audio_segments(file, timestamps, base_path='static/files/'):
    """
    Cuts multiple parts of audio file, saves to specified location
    :param file: original file name
    :param timestamps: list of string tuples, defining parts to cut, in format (start 'mm:ss', end 'mm:ss')
    :param base_path: path to original file location
    """
    ex_list = {}

    for timestamp in timestamps:
        try:
            cut_audio(file, timestamp, base_path)
        except Exception as e:
            ex_list[timestamp] = (repr(e))


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

    file = '01 Back To Earth.m4a'
    path = '/Users/MaxUlianov/Downloads/'

    time = input('Insert timestamps \n')
    times = get_timestamps(time)

    cut_audio_segments(file, times, path)
