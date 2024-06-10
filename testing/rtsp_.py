import cv2
import numpy as np
import time
import threading
import queue


def create_frame(w, h, color):
    f = np.zeros((h, w, 3), dtype=np.uint8)
    f[:] = color
    return f


def sim(w, h, fps, frame_queue):
    st = time.time()
    frame_count = 0
    while True:
        et = time.time() - st
        color = (0, 255, 0)
        f = create_frame(w, h, color)

        tl = (int((et * 50) % w), int((et * 30) % h))
        br = (tl[0] + 50, tl[1] + 50)
        cv2.rectangle(f, tl, br, (0, 0, 255), -1)

        try:
            frame_queue.put(f, timeout=1)  # Add timeout to detect blocking
            frame_count += 1
            print(f"Sim: Frame {frame_count} generated")
        except queue.Full:
            print("Frame queue is full, clearing queue")
            with frame_queue.mutex:
                frame_queue.queue.clear()
        time.sleep(1 / fps)


def start_rtsp_stream(w, h, fps, port):
    pipeline = (
        f'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtspclientsink '
        f'location=rtsp://127.0.0.1:{port}/live.sdp'
    )
    return cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, fps, (w, h), True)


def stream_frames_to_rtsp(writer, frame_queue):
    frame_count = 0
    while True:
        frame = frame_queue.get()
        if frame is None:
            break
        if writer.isOpened():
            start_time = time.time()
            writer.write(frame)
            frame_count += 1
            end_time = time.time()
            print(f"RTSP: Frame {frame_count} written in {end_time - start_time:.2f} seconds")
        else:
            print("RTSP stream is not open")
            break
        frame_queue.task_done()


def create_rtsp_stream(w, h, fps, port):
    frame_queue = queue.Queue(maxsize=30)  # Adjust queue size
    writer = start_rtsp_stream(w, h, fps, port)

    # Start thread to stream frames
    threading.Thread(target=stream_frames_to_rtsp, args=(writer, frame_queue), daemon=True).start()

    try:
        sim(w, h, fps, frame_queue)
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        frame_queue.put(None)
        frame_queue.join()
        writer.release()


if __name__ == "__main__":
    width, height, fps, port = 640, 480, 30, 8554
    create_rtsp_stream(width, height, fps, port)
    print(f"RTSP stream started on rtsp://127.0.0.1:{port}/live.sdp")
