import pybullet as p
import pybullet_data
import serial
import time
import numpy as np

# ===== SERIAL =====
try:
    ser = serial.Serial('COM3', 115200)
    print("Serial Connected ✅")
except:
    ser = None
    print("Simulation Mode (No Serial) ❌")

print("Digital Twin Started...")

# ===== PYBULLET =====
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

plane = p.loadURDF("plane.urdf")
robot = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

# ===== LOOP =====
while True:

    if ser and ser.in_waiting:
        data = ser.readline().decode().strip()
        print("Received:", data)

        try:
            angles = list(map(float, data.split(",")))

            # degrees → radians
            angles_rad = [np.radians(a) for a in angles]

            for i in range(min(len(angles_rad), p.getNumJoints(robot))):
                p.setJointMotorControl2(
                    robot,
                    i,
                    p.POSITION_CONTROL,
                    targetPosition=angles_rad[i],
                    force=1500  # 🔥 أقوى
                )

        except:
            print("Invalid data")

    p.stepSimulation()
    time.sleep(1/240)