import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import rmsnormalize.settings as st
import pydub as pyd
pyd.AudioSegment.converter = st.FFMPEG_EXE_PATH  # os.path.join(PREREQUISITES_FOLDER_PATH, "libav", "bin")


def rms_normalize(file_list):
    audios = get_audios(file_list)

    dbfs_list = []
    rms_list = []
    max_dbfs_list = []
    cut_audio_list = []

    audio_without_silence_list = []

    for audio in audios:
        audio_without_silence = pyd.audio_segment.effects.strip_silence(audio, 500, -64, 100)
        audio_without_silence_list.append(audio_without_silence)
        dbfs_list.append(audio_without_silence.dBFS)
        max_dbfs_list.append(audio.max_dBFS)
        cut_audio_list.append(audio.duration_seconds - audio_without_silence.duration_seconds)
        rms_list.append(audio.rms)

    max_max_dbfs = max(max_dbfs_list)
    avg_dbfs = np.average(dbfs_list)
    dbfs_change = avg_dbfs - dbfs_list
    headrooms = -(max_dbfs_list + dbfs_change)
    min_headroom = min(headrooms)
    target_dbfs = avg_dbfs + min_headroom

    print("Max max dBFS - {0:.5}".format(max_max_dbfs))
    print("AVG dBFS - {0:.5}".format(avg_dbfs))

    counter = 0
    new_dbfs_list = []
    new_max_dbfs_list = []

    for audio in audios:
        init_dbfs = dbfs_list[counter]
        init_max_dbfs = max_dbfs_list[counter]
        cut_dur = cut_audio_list[counter]

        multiplier = 1 - init_dbfs / avg_dbfs
        db_gain = target_dbfs - init_dbfs

        audio = audio.apply_gain(db_gain)
        audio_without_silence_list[counter] = audio_without_silence_list[counter].apply_gain(db_gain)

        print("File - {0:d} : init_dbfs={1:.5} init_max_dbfs={2:.5} silence_dur={7:.2} gain={4:.2} new_max_dbfs={5:.5} new_rms={6:d} new_dBFS={3:.5}".format(
            counter, init_dbfs, init_max_dbfs, audio.dBFS, db_gain, audio.max_dBFS, audio.rms, cut_dur))

        print("File - {0:d} (without silence) : dBFS={1:.5} rms={2:d}".format(
            counter, audio_without_silence_list[counter].dBFS, audio_without_silence_list[counter].rms
        ))

        filename = "trial_" + str(counter + 1) + "_normalized.wav"
        file_path = os.path.join(st.STATIC_FILE_FOLDER_PATH, filename)

        file_handle = audio.export(file_path, format="wav")

        new_dbfs_list.append(audio.dBFS)
        new_max_dbfs_list.append(audio.max_dBFS)

        counter += 1

    return


def get_audios(file_list):
    audios = []

    for file in file_list:
        file_full_path = os.path.join(st.STATIC_FILE_FOLDER_PATH, file)
        file_format = file.split('.')[-1]
        data = pyd.AudioSegment.from_file(file_full_path, file_format)
        audios.append(data)

    return audios


if __name__ == '__main__':
    files = []
    for file_name in sys.argv[1:len(sys.argv)]:
        files.append(file_name)
    rms_normalize(files)


