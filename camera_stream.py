import cv2
from aiortc import VideoStreamTrack, MediaStreamTrack
from av import VideoFrame

class CameraStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # Подключение к камере

    async def recv(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Преобразование кадра для WebRTC
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        return video_frame
