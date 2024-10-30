from flask import Flask, render_template, request
import RPi.GPIO as GPIO

# Настраиваем GPIO
GPIO.setmode(GPIO.BOARD)
pins = {"forward": 12, "backward": 14, "left": 16, "right": 17}
for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Запуск Flask-сервера
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    direction = request.form.get('direction')
    if direction in pins:
        GPIO.output(pins[direction], GPIO.HIGH)
    return '', 204

@app.route('/stop', methods=['POST'])
def stop():
    for pin in pins.values():
        GPIO.output(pin, GPIO.LOW)
    return '', 204

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080)
    finally:
        GPIO.cleanup()
