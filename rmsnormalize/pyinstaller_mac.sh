pyinstaller \
	-F \
	--hidden-import os \
	--hidden-import sys \
	--hidden-import argparse \
	--hidden-import platform \
	--hidden-import numpy \
	--hidden-import pydub \
	--hidden-import rmsnormalize \
	--add-binary ./prerequisites/Darwin;prerequisites/Darwin \
	rms_normalize.py