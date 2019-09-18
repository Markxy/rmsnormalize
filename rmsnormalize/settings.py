import os
import sys
import platform


def get_current_file_path():
    """
    Checks if application is run from Python or .exe file (from pyinstaller).

    :return: Returns script.py folder path for Python script, X:\\...\\temp\\MEI_x folder for .exe executable.
    """
    if getattr(sys, 'frozen', False):
        curr_path = sys.prefix
    elif __file__:
        curr_path = os.path.dirname(__file__)

    return curr_path


def get_current_os():
    return platform.system()


def get_ffmpeg_executable_path(ffmpeg_folder_path):
    return FFMPEG_EXECUTABLE_OS_DICT[get_current_os()]


FFMPEG_EXECUTABLE_OS_DICT = {
    "Windows": "ffmpeg.exe",
    "Darwin": "ffmpeg"
}


CURR_WORKING_DIR = os.getcwd()
CURR_FILE_PATH = get_current_file_path()
PREREQUISITES_FOLDER_NAME = "prerequisites"
PREREQUISITES_FOLDER_PATH = os.path.join(CURR_FILE_PATH, PREREQUISITES_FOLDER_NAME)
PLATFORM_NAME = get_current_os()


FFMPEG_EXE_NAME = "ffmpeg.exe"
# FFPROBE_EXE_NAME = "ffprobe.exe"
FFMPEG_FOLDER_NAME = "ffmpeg"
FFMPEG_FOLDER_PATH = os.path.join(PREREQUISITES_FOLDER_PATH, PLATFORM_NAME, FFMPEG_FOLDER_NAME)
FFMPEG_EXECUTABLE_PATH = get_ffmpeg_executable_path(FFMPEG_FOLDER_PATH)

os.environ["PATH"] += os.pathsep + FFMPEG_FOLDER_PATH

DEFAULT_SILENCE_DBFS = -64
SILENCE_MIN_LEN = 500
SILENCE_PADDING = 100

FILE_OUTPUT_SUFFIX = "_normalized"

BIT_RATE_MEDIA_INFO_KEY = 'bit_rate'
