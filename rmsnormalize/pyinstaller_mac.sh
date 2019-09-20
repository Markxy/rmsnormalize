pyi-makespec \
	-F \
	--hidden-import=os \
	--hidden-import=sys \
	--hidden-import=argparse \
	--hidden-import=platform \
	--hidden-import=numpy \
	--hidden-import=pydub \
	--hidden-import=rmsnormalize \
	--add-binary="prerequisites/Darwin/ffmpeg/ffmpeg:prerequisites/Darwin/ffmpeg" \
	--add-binary="prerequisites/Darwin/ffmpeg/ffprobe:prerequisites/Darwin/ffmpeg" \
	rms_normalize.py
sed -i '' 's/mode: python ;/mode: python 3.7 ;/' rms_normalize.spec
pyinstaller rms_normalize.spec