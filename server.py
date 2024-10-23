import subprocess

def gen():
    process = subprocess.Popen(
        ['libcamera-vid', '--inline', '--width', '640', '--height', '480', '--framerate', '30', '--output', 'stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    while True:
        raw_frame = process.stdout.read(640 * 480 * 3)  # Чтение одного кадра
        if len(raw_frame) != 640 * 480 * 3:
            print("Недостаточно данных для кадра, пропускаем...")
            continue
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((480, 640, 3))
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
