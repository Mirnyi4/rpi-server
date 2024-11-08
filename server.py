import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time

# Настройка GPIO
GPIO.setmode(GPIO.BOARD)
pins = {
    'w': 12,  # GPIO 18 - Вперед
    's': 16,  # GPIO 23 - Назад
    'a': 18,  # GPIO 24 - Влево
    'd': 22,  # GPIO 25 - Вправо
    'ena': 8  # GPIO 8 - Управление ENA
}

# Настраиваем пины как выходы и выключаем их
for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

app = Flask(__name__)

# Функция активации пина
def activate_pin(pin):
    GPIO.output(pin, GPIO.HIGH)

# Функция деактивации пина
def deactivate_pin(pin):
    GPIO.output(pin, GPIO.LOW)

# Функция для регулирования ENA
def control_ena(value):
    pwm_value = int(value)
    duty_cycle = pwm_value / 100.0
    if duty_cycle > 0:
        GPIO.output(pins['ena'], GPIO.HIGH)
    else:
        GPIO.output(pins['ena'], GPIO.LOW)

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для получения команд управления
@app.route('/control', methods=['POST'])
def control():
    directions = request.form.getlist('direction')  # Получаем список направлений
    for direction in directions:
        if direction in pins:
            activate_pin(pins[direction])
    return '', 204  # Пустой ответ с кодом 204 (успех, без контента)

# Маршрут для управления ENA с выбором значения
@app.route('/control_ena', methods=['POST'])
def control_ena_route():
    value = request.form['value']
    control_ena(value)
    return '', 204  # Пустой ответ с кодом 204 (успех, без контента)

# Маршрут для отключения пинов при отпускании клавиш
@app.route('/stop_control', methods=['POST'])
def stop_control():
    directions = request.form.getlist('direction')
    for direction in directions:
        if direction in pins:
            deactivate_pin(pins[direction])
    return '', 204  # Пустой ответ с кодом 204 (успех, без контента)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()  # Очищаем пины при завершении работы
