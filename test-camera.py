import cv2

cap = cv2.VideoCapture(0)  # Попробуйте 0 или 1, если несколько камер

if not cap.isOpened():
    print("Не удалось открыть камеру")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Не удалось получить кадр")
        break
    cv2.imshow('Видео с камеры', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
