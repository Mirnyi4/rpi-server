import RPi.GPIO as GPIO
import time

# Настройки GPIO
GPIO.setmode(GPIO.BCM)
motor_pins = {'left': 17, 'right': 27, 'forward': 22, 'backward': 23}

# Инициализация пинов
for pin in motor_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def move(direction):
    GPIO.output(motor_pins[direction], GPIO.HIGH)
    time.sleep(0.5)  # Двигаться 0.5 секунды
    GPIO.output(motor_pins[direction], GPIO.LOW)

def stop():
    for pin in motor_pins.values():
        GPIO.output(pin, GPIO.LOW)
