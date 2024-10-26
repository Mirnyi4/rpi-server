import asyncio
import json
import websockets
from aiortc import RTCPeerConnection, MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRecorder
import subprocess

class CameraStreamTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()
        # Запускаем libcamera-vid и выводим на stdout
        self.process = subprocess.Popen(
            ["libcamera-vid", "--inline", "--framerate", "30", "-t", "0", "--output", "/dev/stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    async def recv(self):
        # Получаем один кадр из stdout
        frame = await asyncio.get_event_loop().run_in_executor(None, self.process.stdout.read, 4096)
        return frame

async def webrtc_handler(websocket):
    pc = RTCPeerConnection()
    camera = CameraStreamTrack()

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            pc.addTrack(camera)

    try:
        async for message in websocket:
            message = json.loads(message)

            if message["type"] == "offer":
                await pc.setRemoteDescription(message["sdp"])
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)
                await websocket.send(json.dumps({"type": "answer", "sdp": pc.localDescription.sdp}))

    finally:
        await pc.close()

async def main():
    async with websockets.serve(webrtc_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Keep running

if __name__ == "__main__":
    asyncio.run(main())
