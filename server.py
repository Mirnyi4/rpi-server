import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, VideoStreamTrack
import cv2
import numpy as np
from aiortc.contrib.media import MediaPlayer
import json

class CameraStreamTrack(VideoStreamTrack):
    """
    A video stream track that gets frames from the camera.
    """
    def __init__(self):
        super().__init__()
        self.player = MediaPlayer('/dev/video0')

    async def recv(self):
        frame = await self.player.recv()
        return frame

async def webrtc_handler(request):
    pc = RTCPeerConnection()

    @pc.on("icecandidate")
    async def on_icecandidate(candidate):
        await request.app['websocket'].send(json.dumps({
            "event": "icecandidate",
            "candidate": candidate
        }))

    @pc.on("track")
    async def on_track(track):
        if track.kind == "video":
            pc.addTrack(CameraStreamTrack())

    offer = await request.json()
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })

async def control_handler(request):
    data = await request.json()
    direction = data.get("direction")
    state = data.get("state")
    
    # Здесь добавьте код для управления вашей машинкой на основе полученных команд

    return web.Response(text="Command received")

async def main():
    app = web.Application()
    app.router.add_post('/offer', webrtc_handler)
    app.router.add_post('/control', control_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()

    print("Server started at http://0.0.0.0:5000")
    while True:
        await asyncio.sleep(3600)  # Keep the server running

if __name__ == '__main__':
    asyncio.run(main())
