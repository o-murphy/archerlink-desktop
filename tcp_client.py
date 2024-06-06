# import socket
#
#
# class TCPClient:
#     def __init__(self, server_ip, server_port, command):
#         self.server_ip = server_ip
#         self.server_port = server_port
#         self.command = command
#         self.sock = None
#         self.sock_connected = False
#
#     def connect(self):
#         if self.sock_connected:
#             return
#
#         # Create a TCP/IP socket
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#         try:
#             # Connect the socket to the server's port
#             server_address = (self.server_ip, self.server_port)
#             print(f"Connecting to {self.server_ip} port {self.server_port}")
#             self.sock.connect(server_address)
#
#             # Send the command
#             print(f"Sending: {self.command}")
#             self.sock.sendall(self.command.encode())
#
#             # Set the socket to non-blocking mode
#             self.sock.setblocking(False)
#             self.sock_connected = True
#             print("Socket connected")
#
#         except Exception as e:
#             print(f"Failed to connect or send command: {e}")
#             self.sock_connected = False
#
#     def check_socket(self):
#         # Check for any data from the TCP socket
#         try:
#             response = self.sock.recv(1024)
#             if response:
#                 print(f"Received: {response.decode()}")
#         except BlockingIOError:
#             # No data received, continue
#             pass
#         except Exception as e:
#             print(f"Socket error: {e}")
#             self.sock_connected = False
#             self.sock.close()
#
#     def close(self):
#         print("Socket close")
#         if self.sock:
#             self.sock.close()
#             self.sock_connected = False


import socket
import asyncio

class TCPClient:
    def __init__(self, server_ip, server_port, command):
        self.server_ip = server_ip
        self.server_port = server_port
        self.command = command
        self.sock = None
        self.sock_connected = False

    async def connect(self):
        if self.sock_connected:
            return True

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect the socket to the server's port
            server_address = (self.server_ip, self.server_port)
            print(f"Connecting to {self.server_ip} port {self.server_port}")
            await asyncio.get_event_loop().sock_connect(self.sock, server_address)

            # Send the command
            print(f"Sending: {self.command}")
            await asyncio.get_event_loop().sock_sendall(self.sock, self.command.encode())

            self.sock_connected = True
            print("Socket connected")
            return True

        except Exception as e:
            print(f"Failed to connect or send command: {e}")
            self.sock_connected = False
            return False

    async def check_socket(self):
        # Check for any data from the TCP socket
        try:
            response = await asyncio.get_event_loop().sock_recv(self.sock, 1024)
            if response:
                print(f"Received: {response.decode()}")
                return True
        except BlockingIOError:
            # No data received, continue
            return False
        except Exception as e:
            print(f"Socket error: {e}")
            self.sock_connected = False
            self.sock.close()
            return False

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock_connected = False
