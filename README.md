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
"C:\Program Files\VideoLAN\VLC\vlc.exe" -vvv "screen://" --screen-fps=60 --sout "#transcode{vcodec=mp4v,vfilter=croppadd{croptop=0,cropbottom=0,cropleft=0,cropright=0,paddtop=0,paddbottom=0,paddleft=0,paddright=0},width=640,height=480,acodec=none}:rtp{sdp=rtsp://:8554/test}" --no-sout-all --sout-keep

```

TODO:
* logging
* status messages