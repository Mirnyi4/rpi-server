import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import cv2

class CameraStream(VideoStreamTrack):
    """Класс для передачи кадров с камеры через WebRTC."""
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # Используем камеру /dev/video0

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.cap.read()
        if not ret:
            return

        # Преобразуем кадр в формат RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Возвращаем кадр в формате VideoFrame
        from av import VideoFrame
        video_frame = VideoFrame.from_ndarray(frame, format="rgb24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

pcs = set()  # Список подключений

async def index(request):
    """Отправляем HTML-страницу."""
    return web.FileResponse('./templates/index.html')

async def offer(request):
    """Обрабатываем SDP-офер от клиента."""
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # Добавляем поток с камеры в соединение
    pc.addTrack(CameraStream())

    # Отправляем SDP-ответ клиенту
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response(
        {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    )

async def cleanup(app):
    """Закрываем все соединения при завершении работы."""
    for pc in pcs:  # Исправление: добавлено двоеточие
        await pc.close()

app = web.Application()
app.on_shutdown.append(cleanup)
app.router.add_get("/", index)
app.router.add_post("/offer", offer)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=5000)
