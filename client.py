import rtsp


def preview():
    # client = rtsp.Client(rtsp_server_uri='rtsp://192.168.100.1:8888/stream0', verbose=True)
    client = rtsp.Client(rtsp_server_uri='rtsp://192.168.100.1/stream0', verbose=True)
    # client.read().show()
    client.preview()
    client.close()


def retrieve():
    with rtsp.Client(rtsp_server_uri='rtsp://...') as client:
        _image = client.read()

        while True:
            # process_image(_image)
            _image = client.read(raw=True)