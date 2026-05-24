import pybullet as p
import pybullet_data
import socket
import time
import numpy as np


# =========================
# UDP
# =========================
HOST = "0.0.0.0"
PORT = 5006

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.bind((HOST, PORT))
sock.setblocking(False)

print("Digital Twin Started ✅")


# =========================
# LIMITS
# =========================
LIMITS = [
    (-135, 135),   # Base
    (0, 180),      # Shoulder
    (-80, 90),     # Elbow
    (-90, 90),     # Wrist
    (-180, 180),   # Roll
    (0, 180),      # Yaw
    (0, 180),      # Gripper
]


# =========================
# PYBULLET
# =========================
p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

p.setGravity(0, 0, -9.8)

plane = p.loadURDF(
    "plane.urdf"
)


# =========================
# YOUR URDF
# =========================
robot = p.loadURDF(
    "cad file/my_robot.urdf",
    [0, 0, 0],
    useFixedBase=True
)


# =========================
# JOINT ORDER
# لازم يبقى نفس ترتيب الروبوت
# =========================
joint_ids = [
    0,  # base
    1,  # shoulder
    2,  # elbow
    3,  # wrist
    4,  # roll
    5,  # yaw
    6,  # gripper
]


# =========================
# clamp
# =========================
def clamp(v, mn, mx):
    return max(
        mn,
        min(mx, v)
    )


# =========================
# startup default pose
# =========================
defaults = [
    0,
    90,
    0,
    0,
    0,
    90,
    90
]

for i in range(7):

    deg = defaults[i]

    rad = np.radians(
        deg
    )

    p.resetJointState(
        robot,
        joint_ids[i],
        rad
    )

    p.setJointMotorControl2(
        robot,
        joint_ids[i],
        p.POSITION_CONTROL,
        targetPosition=rad,
        force=5000,
        maxVelocity=1000
    )


# =========================
# apply angles
# =========================
def apply_angles(angles):

    count = min(
        len(angles),
        7
    )

    for i in range(count):

        mn, mx = LIMITS[i]

        deg = clamp(
            angles[i],
            mn,
            mx
        )

        rad = np.radians(
            deg
        )

        p.resetJointState(
            robot,
            joint_ids[i],
            rad
        )

        p.setJointMotorControl2(
            robot,
            joint_ids[i],
            p.POSITION_CONTROL,
            targetPosition=rad,
            force=5000,
            maxVelocity=1000
        )


# =========================
# loop
# =========================
while True:

    try:

        data, _ = sock.recvfrom(
            1024
        )

        msg = data.decode().strip()

        angles = list(
            map(
                float,
                msg.split(",")
            )
        )

        apply_angles(
            angles
        )

    except BlockingIOError:
        pass

    except Exception as e:

        print(
            "Twin Error:",
            e
        )

    p.stepSimulation()

    time.sleep(
        1 / 240
    )