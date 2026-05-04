def run_ik():
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    import pybullet as p
    import pybullet_data as pd
    import time
    import numpy as np

    # 🔥 لو عندك esp API
    try:
        from api.esp_api import send_angles
    except:
        def send_angles(x):
            print("SIM SEND:", x)

    # ===== INIT =====
    if p.isConnected():
        p.disconnect()

    p.connect(p.GUI)
    p.setAdditionalSearchPath(pd.getDataPath())
    p.setGravity(0, 0, -9.8)

    # ===== LOAD =====
    plane = p.loadURDF("plane.urdf")
    robot = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

    end_effector = p.getNumJoints(robot) - 1

    # ===== SLIDERS =====
    x_slider = p.addUserDebugParameter("X", -1, 1, 0.4)
    y_slider = p.addUserDebugParameter("Y", -1, 1, 0)
    z_slider = p.addUserDebugParameter("Z", 0, 1, 0.4)

    # ===== LOOP =====
    while True:
        # 🎯 target position
        x = p.readUserDebugParameter(x_slider)
        y = p.readUserDebugParameter(y_slider)
        z = p.readUserDebugParameter(z_slider)

        target = [x, y, z]

        # 🔥 IK
        joint_angles = p.calculateInverseKinematics(
            robot,
            end_effector,
            target
        )

        # ===== APPLY =====
        for i in range(p.getNumJoints(robot)):
            p.setJointMotorControl2(
                robot,
                i,
                p.POSITION_CONTROL,
                targetPosition=joint_angles[i],
                force=2000
            )

        # ===== CONVERT TO DEG =====
        angles_deg = [int(np.degrees(a)) for a in joint_angles[:6]]

        # ===== PRINT =====
        print("Angles:", angles_deg)

        # ===== SEND TO DIGITAL TWIN =====
        send_angles(angles_deg)

        # ===== DISPLAY =====
        p.addUserDebugText(
            f"Angles: {angles_deg}",
            [0, 0, 1.2],
            textColorRGB=[1, 1, 0],
            textSize=1.5,
            lifeTime=0.1,
        )

        p.stepSimulation()
        time.sleep(1/60)


# تشغيل مباشر
if __name__ == "__main__":
    run_ik()