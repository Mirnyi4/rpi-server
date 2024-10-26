from flask import Flask, render_template
from flask_socketio import SocketIO
from motor_control import move, stop
from aiortc import RTCPeerConnection, MediaStreamTrack
from camera_stream import CameraStream

app = Flask(__name__)
socketio = SocketIO(app)
camera = CameraStream()

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Управление движением через WebSocket
@socketio.on('move')
def handle_move(data):
    direction = data['direction']
    if direction in ['left', 'right', 'forward', 'backward']:
        move(direction)
    elif direction == 'stop':
        stop()

# WebRTC: Установление соединения
@socketio.on('offer')
async def handle_offer(data):
    pc = RTCPeerConnection()
    pc.addTrack(camera)
    await pc.setRemoteDescription(data['offer'])
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    socketio.emit('answer', {'sdp': answer.sdp, 'type': answer.type})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
