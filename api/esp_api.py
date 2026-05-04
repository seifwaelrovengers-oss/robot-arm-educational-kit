import serial
import time

ser = serial.Serial('COM4', 115200)
time.sleep(2)

def send_angles(angles):
    data = ",".join([str(int(a)) for a in angles[:6]]) + "\n"
    ser.write(data.encode())
    print("Sent:", data)