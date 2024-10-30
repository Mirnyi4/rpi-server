import gpiozero
import keyboard
from time import sleep

# Инициализация GPIO-пинов для управления двигателями
forward = gpiozero.OutputDevice(12)
backward = gpiozero.OutputDevice(14)
left = gpiozero.OutputDevice(16)
right = gpiozero.OutputDevice(17)

# Функции движения
def move_forward():
    forward.on()
    backward.off()
    print("Вперед")

def move_backward():
    backward.on()
    forward.off()
    print("Назад")

def turn_left():
    left.on()
    right.off()
    print("Влево")

def turn_right():
    right.on()
    left.off()
    print("Вправо")

def stop():
    forward.off()
    backward.off()
    left.off()
    right.off()
    print("Стоп")

# Основной цикл для отслеживания нажатий WASD
try:
    while True:
        if keyboard.is_pressed('w'):
            move_forward()
        elif keyboard.is_pressed('s'):
            move_backward()
        elif keyboard.is_pressed('a'):
            turn_left()
        elif keyboard.is_pressed('d'):
            turn_right()
        else:
            stop()
        sleep(0.1)  # Задержка для снижения нагрузки на процессор

except KeyboardInterrupt:
    print("Завершение программы")
    stop()
