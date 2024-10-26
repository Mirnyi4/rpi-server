import asyncio
import json
import websockets
from aiortc import RTCConfiguration, RTCPeerConnection, VideoStreamTrack
import subprocess
import numpy as np
import cv2

class CameraStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        # Запускаем libcamera и получаем вывод через пайп
        self.process = subprocess.Popen(
            ['libcamera-vid', '-t', '0', '--inline', '--output', '-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    async def recv(self):
        # Читаем из stdout и обрабатываем кадры
        raw_frame = self.process.stdout.read(640 * 480 * 3)  # Предполагаем 640x480
        if len(raw_frame) == 640 * 480 * 3:  # Проверка, что размер кадра корректный
            frame = np.frombuffer(raw_frame, np.uint8).reshape((480, 640, 3))
            return frame
        return None

async def webrtc_handler(websocket, path):
    pc = RTCPeerConnection(RTCConfiguration())
    track = CameraStreamTrack()
    pc.addTrack(track)

    # Обработка обмена SDP
    async for message in websocket:
        offer = json.loads(message)
        await pc.setRemoteDescription(offer)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        await websocket.send(pc.localDescription)

async def control_car(direction, state):
    # Логика управления машинкой
    if state:  # Если кнопка нажата
        if direction == 'forward':
            print("Moving forward")
            # Здесь добавьте код для управления движением вперед
        elif direction == 'backward':
            print("Moving backward")
            # Здесь добавьте код для управления движением назад
        elif direction == 'left':
            print("Turning left")
            # Здесь добавьте код для управления поворотом влево
        elif direction == 'right':
            print("Turning right")
            # Здесь добавьте код для управления поворотом вправоj

async def control_handler(websocket, path):
    async for message in websocket:
        command = json.loads(message)
        await control_car(command['direction'], command['state'])

async def main():
    # Запускаем WebSocket сервер для WebRTC
    webrtc_server = websockets.serve(webrtc_handler, "0.0.0.0", 8765)
    control_server = websockets.serve(control_handler, "0.0.0.0", 8766)

    async with webrtc_server, control_server:
        await asyncio.Future()  # Keep running

if __name__ == "__main__":
    asyncio.run(main())
