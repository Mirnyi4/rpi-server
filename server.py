from flask import Flask, render_template, Response, request
import cv2
import json
from threading import Thread
import socket

app = Flask(__name__)

# Настройки камеры
camera = cv2.VideoCapture(0)

# Параметры управления машинкой
direction = 'stop'
state = False

def send_command(direction, state):
    """Отправляет команду управления машинкой."""
    # Здесь должна быть логика управления мотором
    print(f"Direction: {direction}, State: {state}")

@app.route('/')
def index():
    """Отправляет HTML-страницу."""
    return render_template('index.html')

def generate_frames():
    """Генерирует кадры с камеры для передачи в видеопотоке."""
    while True:
        success, frame = camera.read()  # Читаем кадр
        if not success:
            break
        else:
            # Кодируем кадр в JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Отправляем кадр
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Обрабатывает видеопоток."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    """Обрабатывает команды управления."""
    global direction, state
    data = request.get_json()
    direction = data['direction']
    state = data['state']
    send_command(direction, state)
    return json.dumps({'status': 'success'}), 200

if __name__ == '__main__':
    # Запуск Flask-сервера
    app.run(host='0.0.0.0', port=5000, debug=True)

# Не забудьте остановить поток камеры при завершении
camera.release()
