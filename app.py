import asyncio
import cv2
import numpy as np
from aiohttp import web
from aiortc import RTCPeerConnection, VideoStreamTrack

# Создание класса для видео потока
class CameraStreamTrack(VideoStreamTrack):
    kind = "video"

    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    async def recv(self):
        # Захват кадра
        frame = self.camera.read()
        if not frame[0]:
            raise Exception("Камера не доступна")

        # Преобразование кадра в формат, подходящий для WebRTC
        frame_bgr = frame[1]
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (640, 480))
        return frame_rgb

# Создание экземпляра RTCPeerConnection
async def create_peer_connection():
    pc = RTCPeerConnection()
    camera = cv2.VideoCapture(0)  # Замените 0 на соответствующий номер камеры

    # Добавление видео потока
    pc.addTrack(CameraStreamTrack(camera))

    return pc

# Обработка запросов от клиента
async def websocket_handler(request):
    pc = await create_peer_connection()

    # Создание WebSocket соединения
    websocket = web.WebSocketResponse()
    await websocket.prepare(request)

    async for msg in websocket:
        if msg.type == web.WSMsgType.TEXT:
            # Логика обработки сообщений WebSocket
            pass

    return websocket

# Отправка HTML страницы
async def index(request):
    return web.FileResponse('templates/index.html')

# Создание приложения
app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/ws', websocket_handler)

# Запуск веб-сервера
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
