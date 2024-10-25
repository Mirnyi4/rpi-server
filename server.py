import asyncio
import websockets
from aiortc import RTCPeerConnection, VideoStreamTrack
from aiortc.contrib.media import MediaPlayer
import RPi.GPIO as GPIO

# Настраиваем GPIO
pins = [12, 14, 16, 17]
GPIO.setmode(GPIO.BCM)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# Функции управления двигателями
def control_motor(pin, state):
    GPIO.output(pin, state)

# Поток с камеры
class CameraStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.player = MediaPlayer('/dev/video0')

    async def recv(self):
        frame = await self.player.video.recv()
        return frame

# WebRTC соединение
async def webrtc_handler(peer: RTCPeerConnection):
    track = CameraStreamTrack()
    peer.addTrack(track)

# WebSocket для управления двигателями
async def motor_handler(websocket, path):
    async for message in websocket:
        if message == "w":
            control_motor(12, True)
        elif message == "s":
            control_motor(12, False)
        elif message == "a":
            control_motor(16, True)
        elif message == "d":
            control_motor(16, False)

# Запуск серверов
async def main():
    # WebRTC
    rtc = RTCPeerConnection()
    rtc_handler = webrtc_handler(rtc)

    # WebSocket
    websocket_server = websockets.serve(motor_handler, '0.0.0.0', 8000)

    await asyncio.gather(rtc_handler, websocket_server)

asyncio.run(main())
