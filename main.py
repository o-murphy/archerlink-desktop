from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
# from tcp_client import TCPClient
from kivy import platform
from kivy.config import Config
from kivy.core.window import Window


# from rtsp_stream import RTSPStream
from kvgui.left_column import LeftColumn
from kvgui.right_column import RightColumn
from kvgui.center_column import CenterColumn

# kvShotButton = """
# MDButton:
#     style: "elevated"
#     pos_hint: {"center_x": .5, "center_y": .5}
#
#     MDButtonIcon:
#         icon: "camera"
#
#     MDButtonText:
#         text: "Photo"
# """
#
# kvRecordButton = """
# MDButton:
#     style: "elevated"
#     pos_hint: {"center_x": .5, "center_y": .5}
#
#     MDButtonIcon:
#         icon: "video"
#
#     MDButtonText:
#         text: "Record"
# """


# class StreamApp(MDApp):
#     def build(self):
#         # Main horizontal layout
#         self.layout = MDBoxLayout(orientation='horizontal')
#
#         # Left column
#         self.left_column = MDBoxLayout(orientation='vertical', size_hint_x=0.2)
#         # self.left_button = MDButton(text="Left Button")
#         self.left_button = Builder.load_string(kvShotButton)
#         self.left_column.add_widget(self.left_button)
#
#         # Center column
#         self.center_column = MDBoxLayout(orientation='vertical', size_hint_x=0.6)
#         self.placeholder = MDLabel(text='Waiting for connection...', halign='center')
#         self.center_column.add_widget(self.placeholder)
#
#         # Right column
#         self.right_column = MDBoxLayout(orientation='vertical', size_hint_x=0.2)
#         self.right_button = Builder.load_string(kvRecordButton)
#         self.right_column.add_widget(self.right_button)
#
#         # Add columns to main layout
#         self.layout.add_widget(self.left_column)
#         self.layout.add_widget(self.center_column)
#         self.layout.add_widget(self.right_column)
#
#         # Schedule the RTSP stream initialization
#         Clock.schedule_once(self.init_rtsp_stream, 2)  # Adjust the delay as needed
#         return self.layout
#
#     def on_sock_issue(self):
#         raise ConnectionError("Socket closed")
#
#     def on_rtsp_issue(self):
#         raise ConnectionError("RTSP stream closed")
#
#     def init_rtsp_stream(self, dt):
#         self.tcp_client = TCPClient(
#             server_ip='192.168.100.1',
#             server_port=8888,
#             command='CMD_RTSP_TRANS_START',
#             on_issue=self.on_sock_issue
#         )
#
#         self.rtsp_stream_widget = RTSPStream(
#             rtsp_url='rtsp://192.168.100.1/stream0',
#             tcp_client=self.tcp_client,
#             on_issue=self.on_rtsp_issue
#         )
#
#         self.center_column.remove_widget(self.placeholder)
#         self.center_column.add_widget(self.rtsp_stream_widget)
#
#     def on_stop(self):
#         if self.layout.children:
#             self.layout.children[0].on_close()

if platform == 'win' or platform == 'linux':
    # Window.size = (600, 700)
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class StreamApp(MDApp):

    def init_ui(self):
        self.layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None))
        self.layout.orientation = 'horizontal'

        # self.left_column = LeftColumn()
        # self.center_column = CenterColumn()
        # self.right_column = RightColumn()
        #
        # self.layout.add_widget(self.left_column)
        # self.layout.add_widget(self.center_column)
        # self.layout.add_widget(self.right_column)

        self.screen.add_widget(self.layout)

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = "800"

        self.screen = Screen()
        return self.screen


    def bind_ui(self):
        ...

    def on_start(self):
        self.init_ui()
        self.bind_ui()

    def on_stop(self):
        # print('creating translation template')
        # create_translation_template()
        pass










if __name__ == '__main__':
    StreamApp().run()
