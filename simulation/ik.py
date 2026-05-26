def run_ik():
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
    import tkinter as tk

    try:
        from api.esp_api import send_angles
    except:
        def send_angles(x):
            print("SIM:", x)

    # =========================
    # INIT
    # =========================
    if p.isConnected():
        p.disconnect()

    p.connect(p.GUI)

    p.setAdditionalSearchPath(
        pybullet_data.getDataPath()
    )

    p.setGravity(0, 0, -9.8)

    # =========================
    # LOAD
    # =========================
    plane = p.loadURDF("plane.urdf")

    robot = p.loadURDF(
        "kuka_iiwa/model.urdf",
        useFixedBase=True
    )
    p.resetDebugVisualizerCamera(
    cameraDistance=1.5,
    cameraYaw=45,
    cameraPitch=-30,
    cameraTargetPosition=[0, 0, 0.3]
)

    # 6 theta
    end_effector = 5

    # =========================
    # TK WINDOW
    # =========================
    root = tk.Tk()

    root.title("IK Input")

    tk.Label(
        root,
        text="X"
    ).grid(row=0, column=0)

    tk.Label(
        root,
        text="Y"
    ).grid(row=1, column=0)

    tk.Label(
        root,
        text="Z"
    ).grid(row=2, column=0)

    x_var = tk.StringVar(value="0.4")
    y_var = tk.StringVar(value="0")
    z_var = tk.StringVar(value="0.4")

    tk.Entry(
        root,
        textvariable=x_var
    ).grid(row=0, column=1)

    tk.Entry(
        root,
        textvariable=y_var
    ).grid(row=1, column=1)

    tk.Entry(
        root,
        textvariable=z_var
    ).grid(row=2, column=1)

    target = None

    # =========================
    # APPLY
    # =========================
    def apply_values():

        nonlocal target

        try:

            x = float(
                x_var.get()
            )

            y = float(
                y_var.get()
            )

            z = float(
                z_var.get()
            )

            target = [
                x,
                y,
                z
            ]

            print(
                "\nTarget:",
                target
            )

        except:

            print(
                "Invalid Input"
            )

    tk.Button(
        root,
        text="Apply",
        command=apply_values
    ).grid(
        row=3,
        column=0,
        columnspan=2,
        pady=10
    )

    # =========================
    # LOOP
    # =========================
    while True:

        root.update()

        if target is not None:

            # IK
            joint_angles = p.calculateInverseKinematics(
                robot,
                end_effector,
                target
            )

            # ---------------------
            # FLOAT for terminal
            # ---------------------
            angles_deg_float = [

                round(
                    np.degrees(a),
                    2
                )

                for a in joint_angles[:6]
            ]

            # gripper
            gripper = 40

            angles_deg_float.append(
                gripper
            )

            # ---------------------
            # INT for pybullet/esp
            # ---------------------
            angles_deg_int = [

                int(a)

                for a in angles_deg_float
            ]

            # terminal
            print(
                "Theta:",
                angles_deg_float
            )

            # send esp
            send_angles(
                angles_deg_float
            )

            # move robot
            for i in range(6):

                p.setJointMotorControl2(
                    robot,
                    i,
                    p.POSITION_CONTROL,
                    targetPosition=joint_angles[i],
                    force=2000
                )

            # show theta
            p.addUserDebugText(
                f"Theta = {angles_deg_int}",
                [0, 0, 1.2],
                textColorRGB=[
                    1,
                    1,
                    0
                ],
                textSize=1.5,
                lifeTime=5
            )

            # wait next apply
            target = None

        p.stepSimulation()

        time.sleep(
            1 / 240
        )


if __name__ == "__main__":
    run_ik()