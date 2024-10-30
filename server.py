import RPi.GPIO as GPIO
import time

# Устанавливаем режим нумерации: физические номера пинов
GPIO.setmode(GPIO.BOARD)

# Настраиваем пины 12, 14, 16, 17 как выходы
pins = {"forward": 12, "backward": 14, "left": 16, "right": 17}

for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

print("Пины настроены: 12, 14, 16, 17.")

# Функции управления движением
def move(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)

try:
    while True:
        command = input("Введите команду (w/a/s/d): ").strip().lower()
        if command == "w":
            move(pins["forward"])
        elif command == "s":
            move(pins["backward"])
        elif command == "a":
            move(pins["left"])
        elif command == "d":
            move(pins["right"])
        elif command == "q":
            print("Выход.")
            break
        else:
            print("Неизвестная команда. Используйте w/a/s/d или q для выхода.")
finally:
    GPIO.cleanup()
    print("GPIO очищены.")
