pyinstaller \
	-F \
	-d all \
	--hidden-import os \
	--hidden-import sys \
	--hidden-import argparse \
	--hidden-import platform \
	--hidden-import numpy \
	--hidden-import pydub \
	--hidden-import rmsnormalize \
	--add-binary "prerequisites/Darwin/ffmpeg/ffmpeg:prerequisites/Darwin/ffmpeg" \
	rms_normalize.py