import os
from argparse import ArgumentParser
from numpy import average as avg

import rmsnormalize.settings as st

import pydub as pyd
from pydub.utils import mediainfo

pyd.AudioSegment.converter = st.FFMPEG_EXECUTABLE_PATH


def rms_normalize(file_path_list, silence_thresh=st.DEFAULT_SILENCE_DBFS, is_silence_removed=True):
    """
    The main process which takes in file absolute file paths, normalizes the audio files and saves them to working
    directory.

    :param file_path_list: A list of file paths
    :param silence_thresh: A value in dBFS which specifies the silence threshold of the audio files.
    :param is_silence_removed: A True or False value of whether to exclude silent parts of audios from dBFS calculation.
    :return: Returns 0 if process is completed.
    """
    audios = get_audios(file_path_list)

    file_names, file_extensions, bit_rates = parse_file_info(file_path_list)

    if is_silence_removed:
        dbfs_list, max_dbfs_list = get_audio_dbfs_without_silence(audios, silence_thresh)
    else:
        dbfs_list, max_dbfs_list = get_audio_dbfs(audios)

    target_dbfs = get_target_dbfs(dbfs_list, max_dbfs_list)

    audios = normalize_audios(audios, dbfs_list, target_dbfs)

    export_audios(audios, file_names, file_extensions, bit_rates)

    print('Process completed!\nNormalized ' + str(len(audios)) + ' files.')

    return 0


def export_audios(audios, file_names, file_extensions, bit_rates):
    """
    Writes Pydub audio segments to working directory.

    :param bit_rates: A list of audio file bitrates.
    :param audios: A list of Pydub audio segment Object.
    :param file_names: A list of file names as string.
    :param file_extensions: A list of file extensions as string.
    :return: Returns 0 if successful.
    """
    for counter, audio in enumerate(audios):
        file_name = file_names[counter]
        file_extension = file_extensions[counter]
        bit_rate = bit_rates[counter]

        file_output_path = get_file_output_path(file_name, file_extension)

        audio.export(file_output_path, format=file_extension, bitrate=bit_rate)

    return


def normalize_audios(audios, dbfs_list, target_dbfs):
    """
    Normalizes given Pydub audio segment Objects.

    :param audios: A list of Pydub audio segment Objects.
    :param dbfs_list: A list of dBFS values as float.
    :param target_dbfs: A float dBFS value.
    :return: Returns a list of normalized Pydub audio segment Objects.
    """
    normalized = []
    for counter, audio in enumerate(audios):
        init_dbfs = dbfs_list[counter]
        db_gain = target_dbfs - init_dbfs

        normalized.append(audio.apply_gain(db_gain))

    return normalized


def get_file_output_path(file_name, file_extension):
    """
    Gives the path to file destination in current working directory.

    :param file_name: File name as string.
    :param file_extension: File extension as string.
    :return: Returns an absolute path of a file in current working directory.
    """
    return os.path.join(st.CURR_WORKING_DIR, file_name + st.FILE_OUTPUT_SUFFIX + "." + file_extension)


def parse_file_info(file_list):
    """
    Gets file names, extensions (formats) and bit rates from absolute file paths as lists.

    :param file_list: A list of file paths as string.
    :return: Returns file names, extensions and bit rates as string list.
    """
    file_names = []
    file_extensions = []
    bit_rates = []

    for file in file_list:
        head, tail = os.path.basename(file).split(".")
        file_names.append(head)
        file_extensions.append(tail)
        bit_rates.append(mediainfo(file)[st.BIT_RATE_MEDIA_INFO_KEY])

    return file_names, file_extensions, bit_rates


def get_target_dbfs(dbfs_list, max_dbfs_list):
    """
    Calculates the target dBFS value which to normalize audio levels to.

    :param dbfs_list: A list of dBFS values as float.
    :param max_dbfs_list: A list of dBFS values as float - these are the peak volumes of the audio files.
    :return: Returns the target dBFS value as float.
    """
    avg_dbfs = avg(dbfs_list)
    dbfs_changes = avg_dbfs - dbfs_list
    headrooms = -(max_dbfs_list + dbfs_changes)
    min_headroom = min(headrooms)
    target_dbfs = avg_dbfs + min_headroom

    return target_dbfs


def get_audio_dbfs_without_silence(audios, silence_thresh):
    """
    Removes silence from given Pydub audio segment Objects and returns a list of their dBFS and max_dBFS.

    :param audios: A list of Pydub audio segment Objects.
    :param silence_thresh: A dBFS value as float. This is the maximum volume which is classified as silence.
    :return: Retuns a list of dBFS values and a list of max_dBFS values.
    """
    dbfs_list = []
    max_dbfs_list = []

    for audio in audios:
        audio_without_silence = pyd.audio_segment.effects.strip_silence(
            audio, st.SILENCE_MIN_LEN, silence_thresh, st.SILENCE_PADDING
        )
        dbfs_list.append(audio_without_silence.dBFS)
        max_dbfs_list.append(audio.max_dBFS)

    return dbfs_list, max_dbfs_list


def get_audio_dbfs(audios):
    """
    Gets a list of dBFS and max_dBFS values from Pydub audio segment Objects.

    :param audios: A list of Pydub audio segment Objects.
    :return: Retuns a list of dBFS values and a list of max_dBFS values.
    """
    dbfs_list = []
    max_dbfs_list = []

    for audio in audios:
        dbfs_list.append(audio.dBFS)
        max_dbfs_list.append(audio.max_dBFS)

    return dbfs_list, max_dbfs_list


def get_audios(file_path_list):
    """
    Reads audio files from disk into a list of Pydub audio segment Objects.

    :param file_path_list: A list of absolute file paths as string.
    :return: Returns a list of Pydub audio segment Objects.
    """
    audios = []

    for file_path in file_path_list:
        file_format = file_path.split('.')[-1]

        audio = pyd.AudioSegment.from_file(file_path, file_format)

        audios.append(audio)

    return audios


def init_arg_parser():
    """
    Initializes Python's ArgumentParser object.
    :return: Returns the ArgumentParser object.
    """
    parser = ArgumentParser()
    parser.description = ('The %(prog)s utility will take audio files and normalize them to each other based on their '
                          'dBFS values. Outputs normalized files to current working directory.')

    parser.add_argument('files',
                        help='One or more file paths which point to audio files. '
                             'If they are in current working directory, absolute path is not needed, just the '
                             'filenames.',
                        nargs='+')

    parser.add_argument('-silence_dbfs',
                        help='The dBFS level which qualifies as silence level in selected audio files. '
                             'The audio files are normalized based on the non-silent sections of the audio files. '
                             'If no silence floor is required, the dBFS level should be specified as 0 - this will '
                             'include the entirety of the audio files. '
                             'The default is -64. '
                             'Accepts 0 or negative values.',
                        nargs=1,
                        type=float)

    return parser


def parse_file_paths(path_list):
    """
    Turns a mixed list of absolute paths and file names into absolute paths. Current working directory path is
    prefixed to just file names.
    
    :param path_list: A list of file names or absolute paths as string.
    :return: Returns a list of absolute paths as string.
    """
    paths = []
    for path in path_list:
        if os.path.isabs(path):
            paths.append(path)
        else:
            paths.append(os.path.join(st.CURR_WORKING_DIR, path))

    return paths


if __name__ == '__main__':
    arg_parser = init_arg_parser()
    args = arg_parser.parse_args()

    file_paths = parse_file_paths(args.files)
    silence_dbfs = args.silence_dbfs

    if silence_dbfs is None:
        rms_normalize(file_paths)
    elif silence_dbfs[0] > 0:
        print("silence_dbfs must be 0 or negative if specified.")
    elif silence_dbfs[0] == 0:
        rms_normalize(file_paths, is_silence_removed=False)
    else:
        rms_normalize(file_paths, silence_dbfs[0])
