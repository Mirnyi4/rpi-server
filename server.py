import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, VideoStreamTrack
import av

# Инициализация
pcs = set()

async def webrtc_handler(request):
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("icecandidate")
    async def on_icecandidate(candidate):
        # Отправляем кандидата обратно клиенту
        await request.app["websocket"].send_json({"candidate": candidate})

    # Получение SDP от клиента
    data = await request.json()
    if data.get("type") == "offer":
        await pc.setRemoteDescription(RTCPeerConnection.SDP(data["sdp"]))
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        return web.json_response({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})
    
    return web.Response(status=400)

async def control_handler(request):
    data = await request.json()
    direction = data.get('direction')
    state = data.get('state')
    # Здесь вы можете обработать команды для управления машинкой
    print(f'Command received: {direction}, State: {state}')
    return web.Response(status=200)

async def init_app():
    app = web.Application()
    app.router.add_get("/", lambda request: web.FileResponse("templates/index.html"))
    app.router.add_post("/webrtc", webrtc_handler)
    app.router.add_post("/control", control_handler)
    
    return app

if __name__ == "__main__":
    web.run_app(init_app(), port=5000)
