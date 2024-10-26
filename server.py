import asyncio
import json
import logging
from aiohttp import web
from aiortc import RTCPeerConnection, VideoStreamTrack
import av
import subprocess

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class CameraStreamTrack(VideoStreamTrack):
    """Video stream track using libcamera."""
    
    def __init__(self):
        super().__init__()  # Initialize base class
        self.process = subprocess.Popen(
            ["libcamera-vid", "-t", "0", "--inline", "-o", "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
    async def recv(self):
        frame = await self._get_frame()
        return frame

    async def _get_frame(self):
        # Read frame from libcamera
        data = await asyncio.get_event_loop().run_in_executor(
            None, self.process.stdout.read, 1024 * 1024
        )
        if data:
            # Create a frame
            return av.VideoFrame.from_buffer(data, format="bgr", width=640, height=480)
        raise RuntimeError("Could not read frame from camera")

async def webrtc_handler(request):
    try:
        # Create a new RTCPeerConnection
        pc = RTCPeerConnection()
        camera_track = CameraStreamTrack()
        pc.addTrack(camera_track)

        # Handle incoming signaling messages
        data = await request.json()
        logging.info(f"Received data: {data}")  # Логируем полученные данные

        if data.get("type") == "offer":
            await pc.setRemoteDescription(data["sdp"])
            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)
            return web.Response(text=json.dumps({"sdp": pc.localDescription.sdp}), content_type="application/json")

    except Exception as e:
        logging.error(f"Error handling WebRTC request: {e}")  # Логируем ошибку
        return web.Response(status=500)

    return web.Response(status=400)

async def index(request):
    return web.FileResponse('./templates/index.html')

app = web.Application()
app.router.add_get('/', index)
app.router.add_post('/webrtc', webrtc_handler)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
