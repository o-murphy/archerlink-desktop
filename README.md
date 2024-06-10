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