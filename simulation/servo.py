import sys
import os
import time

# علشان نقدر نعمل import من api
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from api.esp_api import send_angles


print("ESP Servo Test Started...")


# وضع البداية
send_angles([
    0,    # base
    90,   # shoulder
    0,    # elbow
    0,    # wrist
    0,    # roll
    90,   # yaw
    90    # gripper
])

time.sleep(2)


# حركة يمين
print("shoulder -> 120")

send_angles([
    0,
    120,
    0,
    0,
    0,
    90,
    90
])

time.sleep(2)


# حركة شمال
print("shoulder -> 60")

send_angles([
    0,
    60,
    0,
    0,
    0,
    90,
    90
])

time.sleep(2)


# رجوع
print("center")

send_angles([
    0,
    90,
    0,
    0,
    0,
    90,
    90
])

print("Done ✅")