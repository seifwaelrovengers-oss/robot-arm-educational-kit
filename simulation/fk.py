def run_fk():
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    import pybullet as p
    import pybullet_data as pd
    import time
    import numpy as np
    from api.esp_api import send_angles

    # ===== PREVENT MULTIPLE RUN =====
    if getattr(run_fk, "running", False):
        print("FK already running")
        return
    run_fk.running = True

    try:
        # ===== INIT =====
        if p.isConnected():
            print("Restarting PyBullet...")
            p.disconnect()

        p.connect(p.GUI)
        p.setRealTimeSimulation(1)

        p.setAdditionalSearchPath(pd.getDataPath())
        p.setGravity(0, 0, -9.8)

        # 🔥 تحسين الفيزياء
        p.setPhysicsEngineParameter(fixedTimeStep=1/240, numSolverIterations=150)

        # ===== PLANE =====
        plane = p.loadURDF("plane.urdf")

        p.changeDynamics(plane, -1,
            lateralFriction=1.5,
            spinningFriction=0.1,
            rollingFriction=0.1
        )

        # ===== ROBOT =====
        robot = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

        for i in range(p.getNumJoints(robot)):
            p.changeDynamics(robot, i,
                linearDamping=0,
                angularDamping=0
            )

        end_effector_index = p.getNumJoints(robot) - 1

        # ===== SLIDERS =====
        joint_sliders = [
            p.addUserDebugParameter(f"joint{i}", -3.14, 3.14, 0)
            for i in range(p.getNumJoints(robot))
        ]

        # ===== STATE =====
        current_angles = [0.0] * p.getNumJoints(robot)
        velocities = [0.0] * p.getNumJoints(robot)
        last_sent = None

        # ===== PARAMETERS =====
        max_speed = 0.07
        accel = 0.015
        damping = 0.92

        # ===== LOOP =====
        while True:
            target_angles = [
                p.readUserDebugParameter(slider)
                for slider in joint_sliders
            ]

            for i in range(p.getNumJoints(robot)):

                error = target_angles[i] - current_angles[i]

                # تسارع
                velocities[i] += accel * np.sign(error)

                # limit speed
                velocities[i] = np.clip(velocities[i], -max_speed, max_speed)

                # تبطيء عند الوصول
                if abs(error) < 0.05:
                    velocities[i] *= damping

                current_angles[i] += velocities[i]

                # تثبيت نهائي
                if abs(error) < 0.001:
                    current_angles[i] = target_angles[i]
                    velocities[i] = 0

                # 🔥 موتور قوي
                p.setJointMotorControl2(
                    robot,
                    i,
                    p.POSITION_CONTROL,
                    targetPosition=current_angles[i],
                    force=2000
                )

            # ===== DIGITAL TWIN =====
            angles_deg = [int(np.degrees(a)) for a in current_angles[:6]]

            if angles_deg != last_sent:
                send_angles(angles_deg)
                last_sent = angles_deg

            # ===== FK =====
            pos = p.getLinkState(robot, end_effector_index)[0]

            print(f"X: {pos[0]:.2f}, Y: {pos[1]:.2f}, Z: {pos[2]:.2f}")

            p.addUserDebugText(
                f"X={pos[0]:.2f}, Y={pos[1]:.2f}, Z={pos[2]:.2f}",
                [0, 0, 1.5],
                textColorRGB=[1, 0, 0],
                textSize=1.5,
                lifeTime=0.1,
            )

            p.stepSimulation()
            time.sleep(1/240)

    finally:
        run_fk.running = False
def nice(__name__, run_fk):
    if __name__ == "__main__":
        run_fk()

nice(__name__, run_fk)