from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from gpiozero import Motor, PWMOutputDevice
import cv2

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

# Генератор видео-потока
def gen():
    # Загружаем статическое изображение
    frame = cv2.imread('test_image.jpg')  # Убедитесь, что изображение находится в той же директории
    while True:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
