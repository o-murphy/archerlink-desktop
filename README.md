```bash
# Demo installation
# Linux

python3 -m venv venv
venv/bin/activate
pip install -r ./requirements.txt
python main.py
```

```bash
# Demo installation
# Windows

python -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt
python main.py
```

```
1. Connect to device AP
2. Run the app
3. Wait until the connection has been established
```


```powershell
# Build for windows
python -m venv venv
.\venv\Scripts\activate
python -m pip install -U pip setuptools wheel
pip install -r .\requirements.txt
pyinstaller .\archerlink.spec --clean --log-level WARN
```

```cmd
# run fake stream
"C:\Program Files\VideoLAN\VLC\vlc.exe" -vvv "screen://" --screen-fps=30 --sout "#transcode{vcodec=mp4v,acodec=none}:rtp{sdp=rtsp://:8554/test}" --no-sout-all --sout-keep
"C:\Program Files\VideoLAN\VLC\vlc.exe" -vvv "screen://" --screen-fps=50 --sout "#transcode{vcodec=mp4v,vfilter=croppadd{croptop=0,cropbottom=0,cropleft=0,cropright=0,paddtop=0,paddbottom=0,paddleft=0,paddright=0},width=720,height=405,acodec=none}:rtp{sdp=rtsp://:8554/test}" --no-sout-all --sout-keep
```

TODO:
* status messages

pyAV Requires
```
avutil-58-aad225323a2c50e2b64811f8c9af9793.dll - Utility functions used by most ffmpeg components.
avcodec-60-6573ce00ca9847d2b689b4f42ec0d60e.dll - Core library for encoding/decoding audio and video.
avformat-60-f54f9d942eaf6551e0c2ddd5e28eaa9e.dll - Library for handling various multimedia container formats.
avfilter-9-5ef5eee8d4d9fdc58e1a21c774320655.dll - Filtering operations (e.g., scaling, cropping) for video frames.
swresample-4-68411c4695bd16acb756c0976edb3438.dll - Library for audio resampling, rematrixing, and conversion.
swscale-7-baa6473a961c89473bfff44702253cd5.dll - Library for image scaling and format conversion.
libx264-164-9273570c3f8af033faf6f9299e0f8e93.dll - H.264/MPEG-4 AVC encoder.
libx265-fd9ddf38ef624d29c298d6e3ec6c7069.dll - H.265/HEVC encoder.

# Maybe
libvpx-1-7ae7e6b102bc4c9fe00f9c37ce406938.dll - VP8/VP9 codec.
libmp3lame-0-27102ea40aba42ddf338d39f663d2b68.dll - MP3 codec.
libopus-0-9832974b3694c52fb65d9f62d23fdcee.dll - Opus codec.
libvorbis-0-edabcb67b3131465bf267e49a38af57b.dll and libvorbisenc-2-2c299b0222cd6fad2bcdeaa199394b3c.dll - Vorbis codec.
```