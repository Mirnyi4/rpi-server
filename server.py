import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time

# Настройка GPIO
GPIO.setmode(GPIO.BOARD)
pins = {
    'w': 12,  # GPIO 18 - Вперед
    's': 16,  # GPIO 23 - Назад
    'a': 18,  # GPIO 24 - Влево
    'd': 22   # GPIO 25 - Вправо
}

# Настраиваем пины как выходы и выключаем их
for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

app = Flask(__name__)

# Функция активации пина
def activate_pin(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для получения команд управления
@app.route('/control', methods=['POST'])
def control():
    direction = request.form['direction']
    if direction in pins:
        activate_pin(pins[direction])
    return '', 204  # Пустой ответ с кодом 204 (успех, без контента)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()  # Очищаем пины при завершении работы
Надо добавить управление ЕНА через какой то гпио, и добавить ползунок управления на хтмл 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Управление машинкой</title>
    <script>
        // Отправляем команду на сервер
        function sendCommand(direction) {
            fetch('/control', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: direction=${direction}
            });
        }

        // Обработчик нажатий клавиш
        document.addEventListener('keydown', (event) => {
            const key = event.key.toLowerCase();
            if (['w', 'a', 's', 'd'].includes(key)) {
                sendCommand(key);
            }
        });
    </script>
</head>
<body>
    <h1>Управление машинкой с помощью WASD</h1>
    <p>Нажимайте клавиши <strong>W</strong>, <strong>A</strong>, <strong>S</strong>, <strong>D</strong> для управления.</p>
</body>
</html>
