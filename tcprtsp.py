import socket

# Function to send a command and receive the response
def send_command_receive_response(command, socket):
    socket.sendall(command.encode())
    response = socket.recv(1024)  # Adjust buffer size as needed
    return response.decode()

# Replace with your actual RTSP URL, IP, and ports
target_ip = "192.168.100.1"
init_port = 8888  # Port for initializing the RTSP server
rtsp_port = 554  # Port for RTSP streaming
stream_path = "/stream0"  # Path for the RTSP stream

# Define RTSP request messages
DESCRIBE_REQUEST = "DESCRIBE {url} RTSP/1.0\r\nCSeq: 1\r\n\r\n"
SETUP_REQUEST = "SETUP {url} RTSP/1.0\r\nCSeq: 2\r\nTransport: RTP/UDP;unicast;client_port=1234-1235\r\n\r\n"
PLAY_REQUEST = "PLAY {url} RTSP/1.0\r\nCSeq: 3\r\nSession: {session}\r\n\r\n"

# Create a TCP socket for initializing the RTSP server
init_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
init_socket.connect((target_ip, init_port))

# Send the command to start streaming
init_command = "CMD_RTSP_TRANS_START"
init_response = send_command_receive_response(init_command, init_socket)
print("Response:", init_response)

# Check if the response indicates success
if "CMD_ACK_START_RTSP_LIVE" in init_response:
    # Close the initialization socket as we don't need it anymore
    init_socket.close()

    # Establish the RTSP connection
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.connect((target_ip, rtsp_port))

    # Send RTSP requests (DESCRIBE, SETUP, PLAY)
    rtsp_socket.send(DESCRIBE_REQUEST.format(url=stream_path).encode())
    response = rtsp_socket.recv(4096)
    print(response.decode())

    # Extract session ID from the response
    session_id = None
    for line in response.decode().split('\n'):
        if line.startswith('Session'):
            session_id = line.split(':')[1].strip()

    rtsp_socket.send(SETUP_REQUEST.format(url=stream_path).encode())
    response = rtsp_socket.recv(4096)
    print(response.decode())

    rtsp_socket.send(PLAY_REQUEST.format(url=stream_path, session=session_id).encode())
    response = rtsp_socket.recv(4096)
    print(response.decode())

    # Receive and process frames
    while True:
        data = rtsp_socket.recv(4096)
        if not data:
            break
        # Process received data (e.g., decode and display frames)
        print("Received data:", data)

    # Clean up
    rtsp_socket.close()
else:
    print("Failed to start RTSP stream")
