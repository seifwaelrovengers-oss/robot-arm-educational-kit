def run_fk():

    import sys
    import os

    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..'
            )
        )
    )

    import pybullet as p
    import pybullet_data as pd
    import time
    import numpy as np

    from api.esp_api import send_angles

    # Prevent multiple runs
    if getattr(run_fk, "running", False):

        print("FK already running")

        return

    run_fk.running = True

    try:

        # Init PyBullet
        if p.isConnected():

            p.disconnect()

        p.connect(p.GUI)

        p.setAdditionalSearchPath(
            pd.getDataPath()
        )

        p.setGravity(0, 0, -9.8)

        p.setPhysicsEngineParameter(
            fixedTimeStep=1/240,
            numSolverIterations=150
        )

        # Plane
        plane = p.loadURDF("plane.urdf")

        p.changeDynamics(
            plane,
            -1,
            lateralFriction=1.5,
            spinningFriction=0.1,
            rollingFriction=0.1
        )

        # Robot
        robot = p.loadURDF(
            "kuka_iiwa/model.urdf",
            useFixedBase=True
        )

        for i in range(p.getNumJoints(robot)):

            p.changeDynamics(
                robot,
                i,
                linearDamping=0,
                angularDamping=0
            )

        end_effector_index = (
            p.getNumJoints(robot) - 1
        )

        # Joint sliders
        joint_sliders = []

        for i in range(
            p.getNumJoints(robot)
        ):

            slider = p.addUserDebugParameter(
                f"joint{i}",
                -3.14,
                3.14,
                0
            )

            joint_sliders.append(slider)

        # DH parameter sliders
        a1_slider = p.addUserDebugParameter(
            "a1",
            100,
            300,
            200
        )

        a2_slider = p.addUserDebugParameter(
            "a2",
            100,
            300,
            160
        )

        a3_slider = p.addUserDebugParameter(
            "a3",
            50,
            150,
            90
        )

        # State
        current_angles = (
            [0.0] *
            p.getNumJoints(robot)
        )

        velocities = (
            [0.0] *
            p.getNumJoints(robot)
        )

        last_sent = None

        # Motion parameters
        max_speed = 0.07
        accel = 0.015
        damping = 0.92

        # Main loop
        while True:

            # Stop if window closed
            if not p.isConnected():
                break

            # Read DH parameters
            a1 = p.readUserDebugParameter(
                a1_slider
            )

            a2 = p.readUserDebugParameter(
                a2_slider
            )

            a3 = p.readUserDebugParameter(
                a3_slider
            )

            # Read target angles
            target_angles = [

                p.readUserDebugParameter(
                    slider
                )

                for slider in joint_sliders
            ]

            # Smooth motion
            for i in range(
                p.getNumJoints(robot)
            ):

                error = (
                    target_angles[i]
                    - current_angles[i]
                )

                velocities[i] += (
                    accel *
                    np.sign(error)
                )

                velocities[i] = np.clip(
                    velocities[i],
                    -max_speed,
                    max_speed
                )

                if abs(error) < 0.05:

                    velocities[i] *= damping

                current_angles[i] += (
                    velocities[i]
                )

                if abs(error) < 0.001:

                    current_angles[i] = (
                        target_angles[i]
                    )

                    velocities[i] = 0

                p.setJointMotorControl2(
                    robot,
                    i,
                    p.POSITION_CONTROL,
                    targetPosition=current_angles[i],
                    force=2000
                )

            # Convert to degrees
            angles_deg = [

                int(np.degrees(a))

                for a in current_angles[:6]
            ]

            # Send to ESP32
            if angles_deg != last_sent:

                send_angles(angles_deg)

                last_sent = angles_deg

            # FK math
            

            t1 = current_angles[0]
            t2 = current_angles[1]
            t3 = current_angles[2]

            # Base height
            d1 = a1

            # Radius in XY plane
            r = (
                a2 * np.cos(t2) +
                a3 * np.cos(t2 + t3)
            )

            # Cartesian coordinates
            x = r * np.cos(t1)

            y = r * np.sin(t1)

            z = (
                d1 +
                a2 * np.sin(t2) +
                a3 * np.sin(t2 + t3)
            )

            # End effector orientation
            orn = p.getLinkState(
                robot,
                end_effector_index
            )[1]

            roll, pitch, yaw = (
                p.getEulerFromQuaternion(orn)
            )

            # Print FK
            print(
                f"X: {x:.2f} | "
                f"Y: {y:.2f} | "
                f"Z: {z:.2f} | "
                f"Roll: {np.degrees(roll):.2f} | "
                f"Pitch: {np.degrees(pitch):.2f} | "
                f"Yaw: {np.degrees(yaw):.2f}"
            )

            # Display FK
            p.addUserDebugText(
                (
                    f"X={x:.2f}\n"
                    f"Y={y:.2f}\n"
                    f"Z={z:.2f}"
                ),
                [0, 0, 1.5],
                textColorRGB=[1, 0, 0],
                textSize=1.5,
                lifeTime=0.1
            )

            p.stepSimulation()

            time.sleep(1/240)

    finally:

        run_fk.running = False


if __name__ == "__main__":

    run_fk()