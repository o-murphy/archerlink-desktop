import socket

# Define host and port
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)

while True:
    try:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind the socket to the address and port
            s.bind((HOST, PORT))
            # Listen for incoming connections
            s.listen()
            print(f"Server is listening on {HOST}:{PORT}")
            # Accept incoming connections
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    # Receive data from the client
                    data = conn.recv(1024)
                    if not data:
                        break
                    time.sleep(2)
                    # Process received data (here, we'll just print it)
                    print(f"Received: {data.decode()}")
                    if data.decode() == 'CMD_RTSP_TRANS_START':
                        conn.sendall('CMD_ACK_START_RTSP_LIVE'.encode())
                    else:
                        # Echo back the received data
                        conn.sendall(data)
    except ConnectionError:
        pass