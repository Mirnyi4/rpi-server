import RPi.GPIO as GPIO
import time

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
motor_pins = {
    'forward': 17,
    'backward': 18,
    'left': 27,
    'right': 22,
}

# Настройка пинов для моторов
for pin in motor_pins.values():
    GPIO.setup(pin, GPIO.OUT)

def check_motors():
    for direction, pin in motor_pins.items():
        print(f"Проверка мотора {direction}...")
        GPIO.output(pin, GPIO.HIGH)  # Включаем мотор
        time.sleep(1)  # Ждем 1 секунду
        GPIO.output(pin, GPIO.LOW)   # Выключаем мотор
        print(f"Мотор {direction} проверен.")

try:
    while True:
        check_motors()
        time.sleep(2)  # Задержка перед следующей проверкой
except KeyboardInterrupt:
    print("Остановка проверки двигателей.")
finally:
    GPIO.cleanup()  # Очистка настроек GPIO
