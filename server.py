import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer
import RPi.GPIO as GPIO
from aiohttp import web

# Настройки пинов для двигателей
motor_pins = {"left": 12, "right": 14, "forward": 16, "backward": 17}
GPIO.setmode(GPIO.BCM)
for pin in motor_pins.values():
    GPIO.setup(pin, GPIO.OUT)

# Функции управления двигателями
def control_motor(direction, state):
    GPIO.output(motor_pins[direction], GPIO.HIGH if state else GPIO.LOW)

# Видео-поток с камеры
class CameraVideoStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.player = MediaPlayer("/dev/video0", format="v4l2")

    async def recv(self):
        frame = await self.player.video.recv()
        return frame

# Инициализация WebRTC
pc = RTCPeerConnection()

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    await pc.setRemoteDescription(offer)

    pc.addTrack(CameraVideoStream())
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })

async def handle_control(request):
    data = await request.json()
    direction = data.get("direction")
    state = data.get("state", False)
    control_motor(direction, state)
    return web.Response(text="OK")

# Настройка сервера
app = web.Application()
app.add_routes([web.post("/offer", offer), web.post("/control", handle_control)])

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
