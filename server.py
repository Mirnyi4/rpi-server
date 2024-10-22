from flask import Flask, request
import RPi.GPIO as GPIO

app = Flask(__name__)

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
motor_pins = {
    'forward': 17,
    'backward': 18,
    'left': 27,
    'right': 22,
    'stop': 23
}

# Настройка пинов для моторов
for pin in motor_pins.values():
    GPIO.setup(pin, GPIO.OUT)

@app.route('/move', methods=['POST'])
def move():
    direction = request.form.get('direction')
    if direction in motor_pins:
        GPIO.output(motor_pins[direction], GPIO.HIGH)
        return 'Motor moving ' + direction, 200
    return 'Invalid direction', 400

@app.route('/stop', methods=['POST'])
def stop():
    for pin in motor_pins.values():
        GPIO.output(pin, GPIO.LOW)
    return 'All motors stopped', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Убедитесь, что хост и порт указаны правильно
