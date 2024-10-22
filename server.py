from flask import Flask, request, render_template
from gpiozero import Motor, PWMOutputDevice

# Настройка моторов
motor1 = Motor(17, 27)  # Первый мотор: IN1 и IN2
motor2 = Motor(22, 23)  # Второй мотор: IN3 и IN4

ena = PWMOutputDevice(12)  # ENA для первого мотора (скорость)
enb = PWMOutputDevice(13)  # ENB для второго мотора (скорость)

app = Flask(__name__)

# Главная страница сайта
@app.route('/')
def index():
    return render_template('index.html')

# Обработка команд управления
@app.route('/control', methods=['POST'])
def control():
    command = request.form.get('command')

    if command == 'forward':
        ena.value = 1
        enb.value = 1
        motor1.forward()
        motor2.forward()
    elif command == 'backward':
        ena.value = 1
        enb.value = 1
        motor1.backward()
        motor2.backward()
    elif command == 'left':
        motor1.stop()
        motor2.forward()
    elif command == 'right':
        motor1.forward()
        motor2.stop()
    elif command == 'stop':
        motor1.stop()
        motor2.stop()

    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
