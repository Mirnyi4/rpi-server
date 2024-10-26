import asyncio
from aiohttp import web
import cv2
import aiortc
from aiortc import VideoStreamTrack
import logging
import os

logging.basicConfig(level=logging.INFO)

class CameraStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()  # Initialize the base class
        # Запуск libcamera
        self.video = cv2.VideoCapture("libcamera-vid --inline --format=h264 --width 640 --height 480 --timeout 10000 -o -", cv2.CAP_GSTREAMER)

    async def recv(self):
        frame = self.video.read()[1]
        if frame is None:
            raise Exception("Failed to capture frame")
        
        # Конвертация кадра в формат JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        return aiortc.VideoFrame.from_ndarray(buffer, format="jpeg")

async def webrtc_handler(request):
    pc = aiortc.RTCPeerConnection()

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            track.attach(CameraStreamTrack())

    # Обработка предложения
    offer = await request.json()
    await pc.setRemoteDescription(aiortc.RTCSessionDescription(offer['sdp'], offer['type']))
    answer = pc.createAnswer()
    await pc.setLocalDescription(answer)
    
    return web.json_response({
        'sdp': pc.localDescription.sdp,
        'type': pc.localDescription.type
    })

async def control_handler(request):
    data = await request.json()
    direction = data.get('direction')
    state = data.get('state')
    # Здесь можно добавить управление машинкой
    return web.Response(text="OK")

async def index_handler(request):
    return web.FileResponse('./templates/index.html')

async def main():
    app = web.Application()
    app.router.add_get('/', index_handler)  # Добавляем обработчик для главной страницы
    app.router.add_post('/webrtc', webrtc_handler)
    app.router.add_post('/control', control_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()
    
    logging.info("Server started at http://0.0.0.0:5000")
    await asyncio.Event().wait()  # Keep running

if __name__ == '__main__':
    asyncio.run(main())
