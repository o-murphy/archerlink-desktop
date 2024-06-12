import subprocess
import atexit
import threading
import time

from sys import platform
import socket


def open_vlc(rtsp_uri):
    if platform.startswith('win'):
        vlc_process = subprocess.Popen(r'"C:\Program Files\VideoLAN\VLC\vlc.exe" '
                                       r'-vvv "screen://" --screen-fps=50 --sout '
                                       r'"#transcode{vcodec=mp4v,vfilter=croppadd'
                                       r'{croptop=0,cropbottom=0,cropleft=0,cropright=0,'
                                       r'paddtop=0,paddbottom=0,paddleft=0,paddright=0},'
                                       r'width=1280,height=720,acodec=none}:'
                                       r'rtp{sdp='
                                       fr'{rtsp_uri}'
                                       r'}" --no-sout-all --sout-keep')

        def cleanup():
            vlc_process.terminate()
            vlc_process.wait()  # Wait for the process to terminate

        atexit.register(cleanup)


def run_tcp_server(host, port, stop_event):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server is listening on {host}:{port}")

        while not stop_event.is_set():
            s.settimeout(1.0)  # Set timeout for non-blocking accept
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while not stop_event.is_set():
                        conn.settimeout(1.0)  # Set timeout for non-blocking recv
                        try:
                            # Receive data from the client
                            data = conn.recv(1024)
                            if not data:
                                break
                            # Simulate some processing delay
                            time.sleep(2)
                            # Process received data (here, we'll just print it)
                            print(f"Received: {data.decode()}")
                            if data.decode() == 'CMD_RTSP_TRANS_START':
                                conn.sendall('CMD_ACK_START_RTSP_LIVE'.encode())
                            else:
                                # Echo back the received data
                                conn.sendall(data)
                            time.sleep(5)
                        except socket.timeout:
                            continue
            except socket.timeout:
                continue
            except ConnectionError:
                pass
    print("Server is shutting down.")


def open_tcp(host, port):
    stop_event = threading.Event()
    tcp_thread = threading.Thread(target=run_tcp_server, args=(host, port, stop_event), daemon=True)
    tcp_thread.start()

    def cleanup():
        stop_event.set()
        tcp_thread.join()

    atexit.register(cleanup)
