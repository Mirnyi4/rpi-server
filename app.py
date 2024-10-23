import cv2
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO
from gpiozero import Motor, PWMOutputDevice
import base64

# Настраиваем Flask и веб-сокеты
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Настраиваем моторы
motor1 = Motor(17, 27)
motor2 = Motor(22, 23)
ena = PWMOutputDevice(12)
enb = PWMOutputDevice(13)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Отправка видео через веб-сокеты
def send_video():
    cap = cv2.VideoCapture(0)  # Используйте '0' для первой камеры

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Кодируем кадр в JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')
        
        # Отправляем кадр через веб-сокет
        socketio.emit('video_frame', {'data': frame_data})
        socketio.sleep(0.03)  # Уменьшаем частоту передачи (примерно 30 fps)

    cap.release()

# Запуск потока видео в фоновом режиме
@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(send_video)

# Обработка команд управления через веб-сокеты
@socketio.on('command')
def handle_command(data):
    command = data['action']
    if command == 'forward':
        motor1.forward()
        motor2.forward()
    elif command == 'backward':
        motor1.backward()
        motor2.backward()
    elif command == 'left':
        motor1.forward()
        motor2.stop()
    elif command == 'right':
        motor1.stop()
        motor2.forward()
    elif command == 'stop':
        motor1.stop()
        motor2.stop()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
