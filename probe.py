import cv2
import rtsp

def test_stream():
    try:
        with rtsp.Client(rtsp_server_uri='rtsp://192.168.100.1/stream0') as client:
            while True:
                frame = client.read(raw=True)
                if frame is not None:
                    cv2.imshow("RTSP Stream", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("Frame is None")
    except Exception as e:
        print(f"Error in streaming: {e}")

if __name__ == "__main__":
    test_stream()