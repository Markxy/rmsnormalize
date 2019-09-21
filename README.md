# rms_normalize

This utility application normalizes audio between multiple files as a standalone application - no external software is needed.
The end goal is to normalize the RMS and dBFS levels for all of the audio files.

The algorithm normalizes the audio files based on the non-silent parts of the audio files.

> The software is compatible with **Windows** and **MacOS**.

> The software works with most common audio file types, such as: `mp3`, `wav`, `flac`, `m4a`, `aac` - the list is not exhaustive.

The original developer of this utility is <a href="https://github.com/Markxy/">Mark-Felix Mumma</a>.

### External packages, which this software uses and has packaged
  - PyDub
  - FFmpeg

## FFmpeg
This software uses libraries from the <a href=http://ffmpeg.org>FFmpeg</a> project under the LGPLv2.1.
  - We distribute the packages for FFmpeg's Windows & MacOS build's "ffmpeg" and "ffprobe".
  - The "ffmpeg" and "ffprobe" packages are never modified and only to be used as an utility in the program.
  - The original packages from <a href=http://ffmpeg.org>FFmpeg</a> can be found in the "prerequisites" folder.
  - The ffmpeg packages are also found in the "dist" folder's executable files, packaged with CArchive.

# Getting the prebuilt software
The prepackaged software can be found in the "rmsnormalize/dist" folder.
  - rms_normalize corresponds to the MacOS executable.
  - rms_normalize.exe corresponds to the Windows executable.
  
# Using the software
The software is used through commandline.

```
usage: rms_normalize.exe [-h] [-silence_dbfs SILENCE_DBFS] files [files ...]

The rms_normalize.exe utility will take audio files and normalize them to each
other based on their dBFS values. Outputs normalized files to current working
directory.

positional arguments:
  files                 One or more file paths which point to audio files. If
                        they are in current working directory, absolute path
                        is not needed, just the filenames.

optional arguments:
  -h, --help            show this help message and exit
  -silence_dbfs SILENCE_DBFS
                        The dBFS level which qualifies as silence level in
                        selected audio files. The audio files are normalized
                        based on the non-silent sections of the audio files.
                        If no silence floor is required, the dBFS level should
                        be specified as 0 - this will include the entirety of
                        the audio files. The default is -64. Accepts 0 or
                        negative values.
```
                        
## Example usages (on Windows)
> The usage is the same on MacOS, just switch `\` with `/` and `rms_normalize.exe` without the `.exe`.

The simplest example. Assumes that all of the files are in current working directory.

  - `.\rms_normalize.exe .\trial_1.wav .\trial_2.wav .\trial_3.wav`

You can also use absolute paths. The output will be to current working directory.

  - `.\rms_normalize.exe C:\path\to\trial_1.wav C:\path\to\trial_2.wav C:\path\to\trial_3.wav`

To normalize the audio files without cutting out silence.

  - `.\rms_normalize.exe -silence_dbfs 0 .\trial_1.wav .\trial_2.wav .\trial_3.wav`

To specify your own silence level in dbFS. The default is -64.

  - `.\rms_normalize.exe -silence_dbfs -50 .\trial_1.wav .\trial_2.wav .\trial_3.wav`

# Building the executables
You will need to have all of the libraries (argparse, numpy, pydub) which the program uses installed and in your python libs.

To build the executables, run the corresponding shell executable in the `rmsnormalize` folder.

This will run pyinstaller with options defined in the shell scripts and output an executable in the `dist` folder.
## On Windows
```
.\pyinstaller_win.bat
```
## On MacOS
Since MacOS has Python 2.7 installed by default and this program was coded in 3.7, the shell script modifies the pyinstaller build .spec file to use the correct python version with the line: `sed -i '' 's/mode: python ;/mode: python 3.7 ;/' rms_normalize.spec`.

You may want to modify this if you are not using Python 3.7.
```
bash ./pyinstaller_mac.sh
```
