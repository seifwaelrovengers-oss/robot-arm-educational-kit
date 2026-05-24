def run_fk():

    import tkinter as tk
    from threading import Thread
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
    import pybullet_data as pd
    import time
    import numpy as np

    from api.esp_api import send_angles

    if getattr(run_fk, "running", False):

        print("FK already running")

        return

    run_fk.running = True

    try:

        if p.isConnected():

            p.disconnect()

        p.connect(p.GUI)

        p.setAdditionalSearchPath(
            pd.getDataPath()
        )

        p.setGravity(
            0,
            0,
            -9.8
        )

        p.setPhysicsEngineParameter(
            fixedTimeStep=1 / 240,
            numSolverIterations=150
        )

        plane = p.loadURDF(
            "plane.urdf"
        )

        robot = p.loadURDF(
            "kuka_iiwa/model.urdf",
            useFixedBase=True
        )

        p.resetDebugVisualizerCamera(
            cameraDistance=1.5,
            cameraYaw=45,
            cameraPitch=-35,
            cameraTargetPosition=[0, 0, 0.3]
        )

        end_effector_index = (
            p.getNumJoints(robot) - 1
        )

        for i in range(
            p.getNumJoints(robot)
        ):

            p.changeDynamics(
                robot,
                i,
                linearDamping=0,
                angularDamping=0
            )

        current_angles = [0.0] * 6
        velocities = [0.0] * 6

        target_angles_deg = [
            0,      # base
            0,      # shoulder
            0,     # elbow
            0,      # wrist 
            0,      # roll 
            0,     # yaw
            0      # gripper   
        ]
        link1 = 160  #mm   
        link2 = 150  #mm
        link3 = 100  #mm

        last_sent = None

        max_speed = 0.07
        accel = 0.015
        damping = 0.92

        last_print = time.time()

        def angle_gui():

            nonlocal target_angles_deg
            nonlocal link1
            nonlocal link2  
            nonlocal link3

            root = tk.Tk()

            root.title(
                "FK Angle Control"
            )
            name= [
                "Base",
                "Shoulder",
                "Elbow",
                "Wrist",
                "Roll",
                "Yaw",
                "Gripper"
            ]
            entries = []

            for i in range(7):

                tk.Label(
                    root,
                    text=name[i]
                ).grid(
                    row=i,
                    column=0,
                    padx=5,
                    pady=5
                )

                entry = tk.Entry(
                    root,
                    width=10
                )

                entry.insert(
                    0,
                    str(target_angles_deg[i])
                )

                entry.grid(
                    row=i,
                    column=1
                )

                entries.append(entry)
            
            #link1
            tk.Label(
                root,
                text="Link 1 (mm)"
            ).grid(
                row=7,
                column=0,
                padx=5,
                pady=5
            )
            link1_entry = tk.Entry(
                root,
                width=10
            )
            link1_entry.insert(
                0,
                str(link1)
            )
            link1_entry.grid(
                row=7,
                column=1
            )
            #link2
            tk.Label(
                root,
                text="Link 2 (mm)"
            ).grid(
                row=8,
                column=0,
                padx=5,
                pady=5
            )
            link2_entry = tk.Entry(
                root,
                width=10
            )
            link2_entry.insert(
                0,
                str(link2)
            )
            link2_entry.grid(
                row=8,
                column=1
            )
            #link3
            tk.Label(
                root,
                text="Link 3 (mm)"
            ).grid(
                row=9,
                column=0,
                padx=5,
                pady=5
            )
            link3_entry = tk.Entry(
                root,
                width=10
            )
            link3_entry.insert(
                0,
                str(link3)
            )
            link3_entry.grid(
                row=9,
                column=1
            )

            def apply_angles():

                nonlocal target_angles_deg
                nonlocal link1
                nonlocal link2
                nonlocal link3

                try:


                    vals = [
                        float(e.get())
                        for e in entries
                    ]
                    vals[0]= max(-135, min(135, vals[0]))  # Base
                    vals[1]= max(0, min(180, vals[1]))    # Shoulder
                    vals[2]= max(-80, min(90, vals[2]))    # Elbow
                    vals[3]= max(-90, min(90, vals[3]))    # Wrist
                    vals[4]= max(-180, min(180, vals[4]))    # Roll
                    vals[5]= max(0, min(180, vals[5]))    # Yaw
                    vals[6]= max(0, min(180, vals[6]))      # Gripper
                    link1 = max(100, min(220, float(link1_entry.get())))  # Link 1
                    link2 = max(100, min(200, float(link2_entry.get())))  # Link 2
                    link3 = max(50, min(150, float(link3_entry.get())))  # Link 3
                    target_angles_deg = vals
                
                except:

                    print(
                    "Invalid Input"
                    )

            tk.Button(
                root,
                text="APPLY",
                command=apply_angles
            ).grid(
                row=10,
                column=0,
                columnspan=2,
                pady=10
            )

            root.mainloop()

        Thread(
            target=angle_gui,
            daemon=True
        ).start()
        x_text_id = -1
        y_text_id = -1
        z_text_id = -1

        while True:

            if not p.isConnected():

                run_fk.running = False

                break
            # degrees -> radians

            target_angles = [

                np.radians(a)

                for a in target_angles_deg[:6]
            ]

            # smooth motion
            for i in range(6):

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

            angles_deg = [

                int(
                    np.degrees(a)
                )

                for a in current_angles[:6]
            ]
            angles_deg.append(
                int(
                    target_angles_deg[6]
                )
            )

            # ESP later
            if angles_deg != last_sent:

                send_angles(angles_deg)

                last_sent = angles_deg

            # REAL position from pybullet
            link_state = p.getLinkState(
                robot,
                end_effector_index
            )

            pos = link_state[4]

            x = pos[0] * 1000

            y = pos[1] * 1000

            z = pos[2] * 1000

            orn = link_state[5]

            roll, pitch, yaw = (
                p.getEulerFromQuaternion(
                    orn
                )
            )

            if time.time() - last_print > 0.2:

                print(
                    f"X: {x:.2f} | "
                    f"Y: {y:.2f} | "
                    f"Z: {z:.2f}"
                )

                if x_text_id != -1:
                    p.removeUserDebugItem(x_text_id)
                x_text_id = p.addUserDebugText(
                    f"X = {x:.2f}",
                    [0.3, 0, 0.4],
                    textColorRGB=[1, 0, 0],
                    textSize=1.5,
                    lifeTime=0.2
                )

                if y_text_id != -1:
                    p.removeUserDebugItem(y_text_id)
                y_text_id = p.addUserDebugText(
                    f"Y = {y:.2f}",
                    [0.3, 0, 0.3],
                    textColorRGB=[0, 1, 0],
                    textSize=1.5,
                    lifeTime=0.2
                )

                if z_text_id != -1:
                    p.removeUserDebugItem(z_text_id)
                z_text_id = p.addUserDebugText(
                    f"Z = {z:.2f}",
                    [0.3, 0, 0.2],
                    textColorRGB=[0, 0.7, 1],
                    textSize=1.5,
                    lifeTime=0.2
                )

                last_print = time.time()

            p.stepSimulation()

            time.sleep(
                1 / 240
            )

    finally:

        run_fk.running = False

        if p.isConnected():

            p.disconnect()


if __name__ == "__main__":

    run_fk()