import RPi.GPIO as GPIO
import time

# Устанавливаем физическую нумерацию пинов
GPIO.setmode(GPIO.BOARD)

# Используем новые безопасные пины
pins = {
    'w': 12,  # GPIO 18 - Вперед
    's': 16,  # GPIO 23 - Назад
    'a': 18,  # GPIO 24 - Влево
    'd': 22   # GPIO 25 - Вправо
}

# Настраиваем пины как выходы
try:
    for pin in pins.values():
        print(f"Настраиваю пин {pin}")
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
except ValueError as e:
    print(f"Ошибка при настройке пина: {e}")
    GPIO.cleanup()
    exit(1)

print("Пины успешно настроены. Используйте WASD для управления.")

# Функция для включения и выключения пина
def activate_pin(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)

try:
    while True:
        command = input("Введите команду (w/a/s/d): ").strip().lower()
        if command in pins:
            activate_pin(pins[command])
        elif command == "q":
            print("Выход.")
            break
        else:
            print("Неизвестная команда. Используйте w/a/s/d или q для выхода.")
finally:
    GPIO.cleanup()
    print("GPIO очищены.")
