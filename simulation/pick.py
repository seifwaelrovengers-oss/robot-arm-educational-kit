import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pybullet as p
import pybullet_data
import time
import numpy as np
from api.esp_api import send_angles

# تشغيل PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)

# تحميل العناصر
plane = p.loadURDF("plane.urdf")
robot = p.loadURDF("kuka_iiwa/model.urdf",[0,0,0],useFixedBase=True)
ball = p.loadURDF("sphere_small.urdf",[0.6,0,0.05])

end_effector = 6

# تقليل spam
last_sent = None

# تخزين path
path_points = []

# easing function
def smooth_step(t):
    return t * t * (3 - 2 * t)

# الحركة الناعمة + رسم path
def move_robot(target, steps=180):
    global last_sent, path_points

    targetPos = p.calculateInverseKinematics(robot, end_effector, target)

    currentPos = []
    for i in range(7):
        joint_state = p.getJointState(robot, i)
        currentPos.append(joint_state[0])

    for step in range(steps):
        t = step / steps
        t = smooth_step(t)

        interpolated = []

        for i in range(7):
            val = currentPos[i] + (targetPos[i] - currentPos[i]) * t
            interpolated.append(val)

            p.setJointMotorControl2(
                robot,
                i,
                p.POSITION_CONTROL,
                targetPosition=val,
                force=500
            )

        # إرسال للـ Digital Twin
        angles_deg = [int(np.degrees(a)) for a in interpolated[:6]]

        if angles_deg != last_sent:
            send_angles(angles_deg)
            last_sent = angles_deg

        # رسم المسار
        state = p.getLinkState(robot, end_effector)
        current_pos = state[0]

        if len(path_points) > 0:
            prev = path_points[-1]
            p.addUserDebugLine(prev, current_pos, [0, 1, 0], 2, lifeTime=0)

        path_points.append(current_pos)

        p.stepSimulation()
        time.sleep(1/240)

# السيناريو
def pick_and_place():

    move_robot([0.6,0,0.3])   # فوق الكرة
    move_robot([0.6,0,0.1])   # نزول

    # مسك الكرة
    cid = p.createConstraint(
        robot,
        end_effector,
        ball,
        -1,
        p.JOINT_FIXED,
        [0,0,0],
        [0,0,0],
        [0,0,0]
    )

    move_robot([0.6,0,0.3])   # رفع
    move_robot([0.2,0.6,0.3]) # نقل
    move_robot([0.2,0.6,0.12])# نزول

    p.removeConstraint(cid)   # إفلات

    move_robot([0.2,0.6,0.3]) # رفع
    move_robot([0.4,0,0.4])   # رجوع

# reset
def reset_scene():
    global path_points

    path_points = []

    p.resetBasePositionAndOrientation(
        ball,
        [0.6,0,0.05],
        [0,0,0,1]
    )

    p.removeAllUserDebugItems()

# التحكم
while True:

    keys = p.getKeyboardEvents()

    if ord("s") in keys and keys[ord("s")] & p.KEY_WAS_TRIGGERED:
        pick_and_place()

    if ord("r") in keys and keys[ord("r")] & p.KEY_WAS_TRIGGERED:
        reset_scene()

    p.stepSimulation()
    time.sleep(1/240)