import os
import subprocess
import sys
from datetime import datetime

from kivy.config import Config
from kivy.resources import resource_add_path
from kivy import platform

try:
    import tomllib
except ImportError:
    import tomli as tomllib

os.environ["KIVY_NO_CONSOLELOG"] = "1"

ICO_PATH = 'icon.png'
KVGUI_PATH = "gui.kv"
CONFIG_PATH = "config.toml"

if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))
    ICO_PATH = os.path.join(sys._MEIPASS, ICO_PATH)
    KVGUI_PATH = os.path.join(sys._MEIPASS, KVGUI_PATH)
    CONFIG_PATH = os.path.join(sys._MEIPASS, CONFIG_PATH)

if platform == 'win' or platform == 'linux':
    Config.set('graphics', 'maxfps', '120')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.set('kivy', 'window_icon', ICO_PATH)

if platform == 'win':
    OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Local", "ArcherLink")
else:
    OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Pictures", 'ArcherLink')
os.makedirs(OUTPUT_DIR, exist_ok=True)


# TCP_IP = '192.168.100.1'
# TCP_PORT = 8888
# WS_PORT = 8080
# WS_URI = f'ws://{TCP_IP}:{WS_PORT}/websocket'
# RTSP_URI = f'rtsp://{TCP_IP}/stream0'

# if not hasattr(sys, '_MEIPASS'):
with open(CONFIG_PATH, 'rb') as fp:
    cfg = tomllib.load(fp)

DEBUG = cfg.get('DEBUG', False)

SERVER = cfg['debug-server' if DEBUG else 'server']

TCP_IP = SERVER['TCP_IP']
TCP_PORT = SERVER['TCP_PORT']
WS_PORT = SERVER['WS_PORT']
WS_URI = SERVER['WS_URI'].format(TCP_IP=TCP_IP, WS_PORT=WS_PORT)
RTSP_URI = SERVER['RTSP_URI'].format(TCP_IP=TCP_IP)
AV_OPTIONS = cfg['av-options']

if DEBUG:
    from modules import debug
    debug.open_tcp(TCP_IP, TCP_PORT)
    debug.open_vlc(RTSP_URI)


async def get_output_filename():
    dt = datetime.now().strftime("%y%m%d-%H%M%S")
    return os.path.join(OUTPUT_DIR, f"{dt}")


async def open_output_dir():
    if sys.platform == "win32":
        os.startfile(OUTPUT_DIR)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", OUTPUT_DIR])
    else:
        subprocess.Popen(["xdg-open", OUTPUT_DIR])


async def open_file_path(filepath):
    if sys.platform == "win32":
        # Use 'explorer' with '/select,' to highlight the file
        subprocess.Popen(['explorer', '/select,', filepath])
    elif sys.platform == "darwin":
        # Use 'open' with '-R' to reveal the file in Finder
        subprocess.Popen(['open', '-R', filepath])
    else:
        # On Linux, there is no standard way to highlight a file, just open the directory
        subprocess.Popen(['xdg-open', filepath])


__all__ = (
    'ICO_PATH',
    'KVGUI_PATH',
    'OUTPUT_DIR',
    'DEBUG',
    'TCP_IP',
    'TCP_PORT',
    'WS_PORT',
    'WS_URI',
    'RTSP_URI',
    'AV_OPTIONS',
    'get_output_filename',
    'open_output_dir',
    'open_file_path',
)
