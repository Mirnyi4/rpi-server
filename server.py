import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaRelay
import subprocess

relay = MediaRelay()

class CameraStream(MediaStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()
        # Запускаем GStreamer как отдельный процесс
        self.process = subprocess.Popen(
            [
                "gst-launch-1.0", "libcamerasrc", "!", 
                "video/x-raw,width=640,height=480,framerate=30/1", "!",
                "videoconvert", "!", "queue", "!", 
                "vp8enc", "!", "rtpvp8pay", "!", 
                "udpsink", "host=127.0.0.1", "port=5004"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    async def recv(self):
        frame = await relay.subscribe(self).recv()
        return frame

pcs = set()

async def index(request):
    return web.FileResponse('./templates/index.html')

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    video_track = CameraStream()
    pc.addTrack(video_track)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response(
        {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    )

async def cleanup(app):
    for pc in pcs:
        await pc.close()

app = web.Application()
app.on_shutdown.append(cleanup)
app.router.add_get("/", index)
app.router.add_post("/offer", offer)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=5000)
