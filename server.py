import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer

# Трек для передачи видео с помощью GStreamer
class CameraStream(MediaStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()
        # Используем GStreamer для захвата видео
        self.player = MediaPlayer(
            "libcamerasrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink",
            format="raw"
        )

    async def recv(self):
        frame = await self.player.video.recv()
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

    # Добавляем поток камеры
    video_track = CameraStream()
    pc.addTrack(video_track)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    print("Local Description set:", pc.localDescription)

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
