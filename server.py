import asyncio
from aiortc import RTCPeerConnection, VideoStreamTrack
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import cv2

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
pins = {'forward': 12, 'backward': 14, 'left': 16, 'right': 17}

for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Инициализация Flask и SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

class CameraStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    async def recv(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

# Настройка WebRTC
pcs = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/offer', methods=['POST'])
async def offer():
    params = await request.json
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("iceconnectionstatechange")
    def on_icestatechange():
        if pc.iceConnectionState == "closed":
            pcs.discard(pc)

    pc.addTrack(CameraStream())
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return jsonify({'sdp': pc.localDescription.sdp, 'type': pc.localDescription.type})

@socketio.on('command')
def handle_command(data):
    command = data['action']
    print(f"Received command: {command}")

    if command == 'forward':
        GPIO.output(pins['forward'], GPIO.HIGH)
    elif command == 'backward':
        GPIO.output(pins['backward'], GPIO.HIGH)
    elif command == 'left':
        GPIO.output(pins['left'], GPIO.HIGH)
    elif command == 'right':
        GPIO.output(pins['right'], GPIO.HIGH)
    elif command == 'stop':
        for pin in pins.values():
            GPIO.output(pin, GPIO.LOW)

if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Server stopped and GPIO cleaned up.")
