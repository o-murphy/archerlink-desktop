# import cv2
# import threading
# import kivy
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.uix.image import Image
# from kivy.graphics.texture import Texture
#
# class RTSPClientApp(App):
#     def build(self):
#         self.img = Image()
#         self.url_input = TextInput(hint_text='Enter RTSP URL', multiline=False)
#         self.connect_btn = Button(text='Connect', on_press=self.connect_to_stream)
#
#         layout = BoxLayout(orientation='vertical')
#         layout.add_widget(self.url_input)
#         layout.add_widget(self.connect_btn)
#         layout.add_widget(self.img)
#
#         self.capture = None
#         self.thread = None
#         self.stop_thread = False
#
#         return layout
#
#     def connect_to_stream(self, instance):
#         rtsp_url = self.url_input.text
#         if rtsp_url:
#             if self.capture:
#                 self.stop_stream()
#             self.capture = cv2.VideoCapture(rtsp_url)
#             self.thread = threading.Thread(target=self.update_image)
#             self.stop_thread = False
#             self.thread.start()
#
#     def update_image(self):
#         while not self.stop_thread:
#             ret, frame = self.capture.read()
#             if ret:
#                 buf1 = cv2.flip(frame, 0)
#                 buf = buf1.tostring()
#                 image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
#                 image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#                 self.img.texture = image_texture
#
#     def stop_stream(self):
#         self.stop_thread = True
#         self.thread.join()
#         self.capture.release()
#
#     def on_stop(self):
#         if self.capture:
#             self.stop_stream()
#
# if __name__ == '__main__':
#     RTSPClientApp().run()


# import rtsp
#
# with rtsp.Client(rtsp_server_uri='rtsp://192.168.100.1:8888/stream0') as client:
#     _image = client.read()
#
#     while True:
#         # process_image(_image)
#         _image = client.read(raw=True)
#         print(_image)
#
#



import rtsp
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


# # client = rtsp.Client(rtsp_server_uri='rtsp://192.168.100.1:8888/stream0', verbose=True)
# client = rtsp.Client(rtsp_server_uri='rtsp://192.168.100.1/stream0', verbose=True)
# # client.read().show()
# client.preview()
# client.close()

# import asyncio
# import av
# import cv2
# from aiortsp.rtsp.reader import RTSPReader
# #
# # # async def main():
# # #     # Open a reader (which means RTSP connection, then media session)
# # #     async with RTSPReader(stream_path) as reader:
# # #         # Iterate on RTP packets
# # #         async for pkt in reader.iter_packets():
# # #             print('PKT', pkt.seq, pkt.pt, len(pkt))
# # #
# # # asyncio.run(main())
# #
# async def main():
#     # Open a reader (which means RTSP connection, then media session)
#     async with RTSPReader(stream_path) as reader:
#         # Initialize PyAV container and codec context
#         codec = av.CodecContext.create('h264', 'r')
#
#         # Iterate on RTP packets
#         async for pkt in reader.iter_packets():
#             try:
#                 # Create an AVPacket from the RTP packet data
#                 packet = av.packet.Packet(pkt.data)
#
#                 # Decode the packet to get the frame
#                 frames = codec.decode(packet)
#                 for frame in frames:
#                     # Convert the frame to a numpy array
#                     img = frame.to_ndarray(format='bgr24')
#
#                     # Display the frame using OpenCV
#                     cv2.imshow('Frame', img)
#
#                     if cv2.waitKey(1) & 0xFF == ord('q'):
#                         break
#
#             except av.AVError as e:
#                 print(f"Error decoding packet: {e}")
#                 continue
#
#         cv2.destroyAllWindows()
#
# asyncio.run(main())
#
# #
# # import cv2
# #
# # def main():
# #     # Open the RTSP stream
# #     cap = cv2.VideoCapture(stream_path)
# #     print(cap)
# #     if not cap.isOpened():
# #         print(f"Error: Unable to open video stream {stream_path}")
# #         return
# #
# #     while True:
# #         # Capture frame-by-frame
# #         ret, frame = cap.read()
# #
# #         if not ret:
# #             print("Error: Unable to retrieve frame from stream")
# #             break
# #
# #         # Display the frame
# #         cv2.imshow('Frame', frame)
# #
# #         # Press 'q' to quit the video stream
# #         if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break
# #
# #     # When everything done, release the capture and close windows
# #     cap.release()
# #     cv2.destroyAllWindows()
# #
# # if __name__ == "__main__":
# #     main()