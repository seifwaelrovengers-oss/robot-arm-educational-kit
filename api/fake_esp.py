import serial

# نفس البورت
ser = serial.Serial('COM3', 115200)

print("Fake ESP Started...")

while True:
    if ser.in_waiting:
        data = ser.readline().decode().strip()
        print("Received from Python:", data)

        angles = list(map(int, data.split(",")))

        print("Parsed Angles:", angles)
        print("Simulating motors...\n")