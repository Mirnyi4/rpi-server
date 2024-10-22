from gpiozero import Motor, PWMOutputDevice
from time import sleep

# Настраиваем моторы и PWM-выходы для управления скоростью
motor1 = Motor(17, 27)  # IN1 и IN2 для первого мотора
motor2 = Motor(22, 23)  # IN3 и IN4 для второго мотора

ena = PWMOutputDevice(12)  # ENA для регулировки скорости первого мотора
enb = PWMOutputDevice(13)  # ENB для второго мотора

# Устанавливаем скорость (0.0 - 1.0)
ena.value = 0.8
enb.value = 0.8

# Команды для управления моторами
print("Двигатели вперёд")
motor1.forward()
motor2.forward()
sleep(2)

print("Стоп")
motor1.stop()
motor2.stop()
sleep(1)

print("Двигатели назад")
motor1.backward()
motor2.backward()
sleep(2)

print("Стоп")
motor1.stop()
motor2.stop()
