import socket

def send_command_to_tcp_server(server_ip, server_port, command):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect the socket to the server's port
        server_address = (server_ip, server_port)
        print(f"Connecting to {server_ip} port {server_port}")
        sock.connect(server_address)

        try:
            # Send the command
            print(f"Sending: {command}")
            sock.sendall(command.encode())

            # Look for the response (optional)
            response = sock.recv(1024)
            print(f"Received: {response.decode()}")

            while True:
                ...

        finally:
            # Close the socket
            print("Closing socket")
            sock.close()


    except Exception as e:
        print(f"Failed to connect or send command: {e}")
        raise e

    # Define the server IP, port, and the command to send
server_ip = '192.168.100.1'
stream_path = "rtsp://" + server_ip + "/stream0"
server_port = 8888
command = 'CMD_RTSP_TRANS_START'

# Send the command to the TCP server
send_command_to_tcp_server(server_ip, server_port, command)