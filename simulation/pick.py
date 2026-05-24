import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import pybullet as p
import pybullet_data
import time
import numpy as np
from api.esp_api import send_angles


# =========================
# PyBullet
# =========================
p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

p.setGravity(0, 0, -9.8)


# =========================
# Objects
# =========================
plane = p.loadURDF(
    "plane.urdf"
)

robot = p.loadURDF(
    "kuka_iiwa/model.urdf",
    [0, 0, 0],
    useFixedBase=True
)

ball = p.loadURDF(
    "sphere_small.urdf",
    [0.6, 0, 0.05]
)

end_effector = 6

last_sent = None
path_points = []


# =========================
# Smooth easing
# =========================
def smooth_step(t):

    return t * t * (3 - 2 * t)


# =========================
# Send 7 angles
# =========================
def build_angles(interpolated):

    base = int(np.degrees(interpolated[0]))
    shoulder = int(np.degrees(interpolated[1]))
    elbow = int(np.degrees(interpolated[2]))

    wrist = 0
    roll = 0
    yaw = 90
    gripper = 90

    return [
        base,
        shoulder,
        elbow,
        wrist,
        roll,
        yaw,
        gripper
    ]


# =========================
# Move robot
# =========================
def move_robot(target, steps=180):

    global last_sent
    global path_points

    target_pos = p.calculateInverseKinematics(
        robot,
        end_effector,
        target
    )

    current_pos = []

    for i in range(7):

        joint_state = p.getJointState(
            robot,
            i
        )

        current_pos.append(
            joint_state[0]
        )

    for step in range(steps):

        t = step / steps
        t = smooth_step(t)

        interpolated = []

        for i in range(7):

            val = (
                current_pos[i]
                + (
                    target_pos[i]
                    - current_pos[i]
                ) * t
            )

            interpolated.append(val)

            p.setJointMotorControl2(
                robot,
                i,
                p.POSITION_CONTROL,
                targetPosition=val,
                force=500
            )

        # send to twin
        angles_deg = build_angles(
            interpolated
        )

        if angles_deg != last_sent:

            send_angles(
                angles_deg
            )

            last_sent = angles_deg

        # draw path
        state = p.getLinkState(
            robot,
            end_effector
        )

        pos = state[0]

        if len(path_points) > 0:

            prev = path_points[-1]

            p.addUserDebugLine(
                prev,
                pos,
                [0, 1, 0],
                2,
                lifeTime=0
            )

        path_points.append(pos)

        p.stepSimulation()

        time.sleep(
            1 / 240
        )


# =========================
# Pick and place
# =========================
def pick_and_place():

    move_robot([0.6, 0, 0.3])

    move_robot([0.6, 0, 0.1])

    cid = p.createConstraint(
        robot,
        end_effector,
        ball,
        -1,
        p.JOINT_FIXED,
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    )

    move_robot([0.6, 0, 0.3])

    move_robot([0.2, 0.6, 0.3])

    move_robot([0.2, 0.6, 0.12])

    p.removeConstraint(
        cid
    )

    move_robot([0.2, 0.6, 0.3])

    move_robot([0.4, 0, 0.4])


# =========================
# Reset
# =========================
def reset_scene():

    global path_points

    path_points = []

    p.resetBasePositionAndOrientation(
        ball,
        [0.6, 0, 0.05],
        [0, 0, 0, 1]
    )

    p.removeAllUserDebugItems()


# =========================
# Main loop
# =========================
while True:

    keys = p.getKeyboardEvents()

    if (
        ord("s") in keys
        and
        keys[ord("s")]
        & p.KEY_WAS_TRIGGERED
    ):

        pick_and_place()

    if (
        ord("r") in keys
        and
        keys[ord("r")]
        & p.KEY_WAS_TRIGGERED
    ):

        reset_scene()

    p.stepSimulation()

    time.sleep(
        1 / 240
    )