import os


def cut_video(filename, cut_points, base_path='static/files/'):
    """
    Cut a part of audio file, save to specified location with a
    name '<original name>_start-end'
    :param filename: original file name
    :type filename: str
    :param cut_points: string tuple (start 'mm:ss', end 'mm:ss')
    :type cut_points: tuple[str, str]
    :param base_path: path to video file being cut
    :return: name of video file after cutting
    """
    start_time, end_time = cut_points

    file_format = 'mp4'
    new_file = f'{filename[:-4]}_{cut_points[0]}-{cut_points[1]}.{file_format}'

    os.system(f"ffmpeg -i {base_path}{filename} -ss {start_time} -t {end_time} {base_path}{new_file}")
    return new_file


def cut_video_segments(file, timestamps, base_path='static/files/'):
    """
    Cuts multiple parts of video file, saves to specified location
    :param file: original file name
    :type file: str
    :param timestamps: list of string tuples, defining parts to cut, in format (start 'mm:ss', end 'mm:ss')
    :type timestamps: List
    :param base_path: path to original file location
    :type base_path: str
    :return list: list of names for video segment files
    """
    ex_list = {}
    files = []
    for timestamp in timestamps:
        try:
            file_cut = cut_video(file, timestamp, base_path)
            files.append(file_cut)
        except Exception as e:
            ex_list[timestamp] = (repr(e))

    return files


if __name__ == '__main__':
    print(cut_video('rotated-shark.mov', ('00:01', '00:05')))
