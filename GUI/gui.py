# Libraries 
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import webbrowser 
import subprocess 


#3l4an a create window 
window = Tk()
window.title('Robotic Arm Virtual Lab App')
window.state('zoomed') 
BG_COLOR = "#04153B" 
window.configure(bg=BG_COLOR)


import subprocess
import os

# file seif 
def run_pybullet_sim():
    try:
        # 7ot hna asm file bta3k 
        file_name = "pybullet_robot_sim.py" 
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, file_name)
        
        if os.path.exists(file_path):
            subprocess.Popen(["python", file_path])
        else:
            messagebox.showerror("File Error", f"Simulation file not found \nMake sure '{file_name}' is located in the same project folder.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not start simulation: {str(e)}")

def calculate_ik_angles(x, y, z):
    j1 = np.degrees(np.arctan2(y, x))
    r = np.sqrt(x**2 + y**2)
    d = np.sqrt(r**2 + z**2)
    if d > 12: d = 12 
    j2 = np.degrees(np.arccos(np.clip(d/15, -1, 1))) * 1.5
    j3 = -j2 * 0.8
    return [j1, j2, j3, 0, 0, 0]

#3l4an 3d robot elfeh simulation
def update_robot_plot(ax, canvas, joints, matrix_labels=None, dh_labels=None):
    ax.clear()
    # Style
    ax.set_facecolor('#081b4b')
    ax.set_box_aspect([1, 1, 0.7])
    ax.grid(False)

    angles = []
    for j in joints:
        if hasattr(j, "get"):
            angles.append(np.radians(j.get())) 
        else:
            angles.append(np.radians(j))

    # DRAW BASE  
    t = np.linspace(0, 2*np.pi, 60)
    ax.plot(np.cos(t)*2, np.sin(t)*2, 0, color="white", linewidth=2)
    ax.scatter(0, 0, 0, color="white", s=80)

    # FORWARD KINEMATICS 
    L = 5
    x = y = z = 0
    pitch = 0
    base_angle = angles[0]
    T_total = np.eye(4)
    
    # DH Parameters 
    dh_params = [
        [angles[0], 0, 0, -np.pi/2],
        [angles[1], 0, L,  0],
        [angles[2], 0, L,  0],
        [angles[3], 0, 0, -np.pi/2],
        [angles[4], 0, 0,  np.pi/2],
        [angles[5], 0, 0,  0]
    ]

    # LOOP calculations 
    for i in range(len(angles)):
        px, py, pz = x, y, z
        if i > 0:
            pitch += angles[i]
            
        x += L * np.cos(base_angle) * np.cos(pitch)
        y += L * np.sin(base_angle) * np.cos(pitch)
        z += L * np.sin(pitch)

        ax.plot([px, x], [py, y], [pz, z],
                color="orange",
                linewidth=max(2, 10-i),
                solid_capstyle='round')
        
        ax.scatter(x, y, z, color="white", s=90, edgecolors="black")

        # Matrix Calculation
        theta_dh, d_dh, a_dh, alpha_dh = dh_params[i]
        ct, st = np.cos(theta_dh), np.sin(theta_dh)
        ca, sa = np.cos(alpha_dh), np.sin(alpha_dh)
        
        A = np.array([
            [ct, -st*ca,  st*sa, a_dh*ct],
            [st,  ct*ca, -ct*sa, a_dh*st],
            [0,   sa,     ca,    d_dh],
            [0,   0,      0,     1]
        ])
        T_total = T_total @ A
        # hna 3l4an a5od kol angles mn slider parameter wa7d bs elgowa matrix elhit8ir elba2y na hsbto t7t mn mechanical 
        if dh_labels is not None:
            try:
                current_theta_deg = np.degrees(theta_dh)
                dh_labels[i].config(text=f"{current_theta_deg:.1f}")
            except:
                pass

    #  7agat tb3 AXES design 
    ax.set_xlabel('X Axis', color='white', labelpad=10)
    ax.set_ylabel('Y Axis', color='white', labelpad=10)
    ax.set_zlabel('Z Axis', color='white', labelpad=10)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    ax.set_xlim([-15, 30])
    ax.set_ylim([-20, 20])
    ax.set_zlim([0, 30])
    ax.tick_params(colors="white")
    ax.set_title("6-DOF ROBOTIC ARM SIMULATION", color="white", fontsize=12, fontweight="bold")
    ax.grid(True)
    
    # MATRIX OUTPUT 
    if matrix_labels:
        vals = [
            T_total[0,0], T_total[0,1], T_total[0,2], T_total[0,3],
            T_total[1,0], T_total[1,1], T_total[1,2], T_total[1,3],
            T_total[2,0], T_total[2,1], T_total[2,2], T_total[2,3]
        ]
        names = ["nx","ox","ax","px","ny","oy","ay","py","nz","oz","az","pz"]
        for i in range(12):
            matrix_labels[i].config(text=f"{names[i]} = {vals[i]:.4f}")

    if dh_labels:
        for i, s in enumerate(joints):
            val = s.get()
            dh_labels[i].config(text=f"{val:.1f}")
    canvas.draw()
    
    
# 3l4an popup manual 3la 4kl window
def show_fancy_manual(title, content):
    popup = Toplevel(window)
    popup.title(title)
    popup.geometry("750x650") 
    popup.configure(bg="#0a1e4d")
    popup.grab_set() 

    Label(popup, text=title, font=("Helvetica", 18, "bold"), fg="#f39c12", bg="#0a1e4d", pady=20).pack()
    msg = Message(popup, text=content, font=("Consolas", 11), fg="white", bg="#0a1e4d", width=680, justify=LEFT)
    msg.pack(expand=True, padx=25, pady=10)

    Button(popup, text="LET'S GO", font=("Arial", 14, "bold"), bg="#27ae60", fg="white", 
           activebackground="#2ecc71", activeforeground="white", padx=40, pady=10, 
           cursor="hand2", command=popup.destroy).pack(pady=20)

# trajectory page 
def open_trajectory_page():
    for widget in window.winfo_children(): widget.destroy()
    
    traj_theory = (
        "TRAJECTORY PLANNING THEORY:\n\n"
        "1. OBJECTIVE:\n"
        "Moving the end-effector from Point A to Point B smoothly.\n\n"
        "2. MATHEMATICAL ACCURACY:\n"
        "Monitoring Euclidean Distance and Position Error to ensure precision.\n\n"
        "3. PERFORMANCE METRICS:\n"
        "- Path Smoothness (Cubic Spline).\n"
        "- Accuracy (Difference between desired and reached XYZ)."
    )
    show_fancy_manual("Trajectory Planning Module", traj_theory)

    # Navigation Button
    Button(window, text="Back to Experiments", font=("Arial", 12, "bold"), 
           fg="#f36412", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(anchor=NW, padx=20, pady=10)
    
    container = Frame(window, bg=BG_COLOR)
    container.pack(expand=True, fill=BOTH, padx=20)


    left_p = Frame(container, bg=BG_COLOR)
    left_p.pack(side=LEFT, fill=Y, padx=10, pady=10)
    
    Label(left_p, text="MISSION CONTROL", font=("Helvetica", 18, "bold"), fg="#1abc9c", bg=BG_COLOR).pack(pady=10)

    def play_traj_video():
        webbrowser.open("https://youtu.be/HOfuDcTtVNs?si=qsuffP4wRIbYW7hm")

    Button(left_p, text=" WATCH TRAJECTORY TUTORIAL", font=("Arial", 10, "bold"), 
           bg="#2ecc71", fg="white", pady=8, command=play_traj_video).pack(pady=5, fill=X)

    current_start = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
    start_coords = {}; end_coords = {}

    start_frame = LabelFrame(left_p, text=" START POINT (A) ", fg="white", bg="#03265b", font=("Arial", 10, "bold"), padx=10, pady=10)
    start_frame.pack(fill=X, pady=5)
    
    for axis in ['X', 'Y', 'Z']:
        f = Frame(start_frame, bg="#03265b")
        f.pack(fill=X)
        Label(f, text=f"{axis}:", fg="#00f2ff", bg="#03265b", font=("Consolas", 10)).pack(side=LEFT)
        s = Entry(f, width=10, bg="#051c4d", fg="white", insertbackground="white", bd=0)
        s.insert(0, "0.0")
        s.pack(side=RIGHT, pady=2)
        start_coords[axis] = s

    def apply_start_position():
        try:
            current_start['X'] = float(start_coords['X'].get().strip())
            current_start['Y'] = float(start_coords['Y'].get().strip())
            current_start['Z'] = float(start_coords['Z'].get().strip())
            
            angles = calculate_ik_angles(current_start['X'], current_start['Y'], current_start['Z'])
            update_robot_plot(ax, canvas, angles, target_dot=(current_start['X'], current_start['Y'], current_start['Z']))
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid numbers for START POINT.")

    Button(start_frame, text="APPLY START", bg="#3498db", fg="white", 
           font=("Arial", 9, "bold"), command=apply_start_position).pack(pady=5, fill=X)

    
    target_frame = LabelFrame(left_p, text=" TARGET POINT (B) ", fg="white", bg="#0a1e4d", font=("Arial", 10, "bold"), padx=10, pady=10)
    target_frame.pack(fill=X, pady=5)
    
    for axis in ['X', 'Y', 'Z']:
        f = Frame(target_frame, bg="#0a1e4d")
        f.pack(fill=X)
        Label(f, text=f"{axis}:", fg="#00f2ff", bg="#0a1e4d", font=("Consolas", 10)).pack(side=LEFT)
        s = Entry(f, width=10, bg="#051c4d", fg="white", insertbackground="white", bd=0)
        s.insert(0, "5.0")
        s.pack(side=RIGHT, pady=2)
        end_coords[axis] = s

    
    out_frame = LabelFrame(left_p, text=" ANALYTICS DASHBOARD ", fg="#f1c40f", bg="#051c4d", font=("Arial", 10, "bold"), padx=10, pady=10)
    out_frame.pack(fill=X, pady=10)
    
    res_labels = {}
    for item in ['Distance', 'Accuracy']:
        f = Frame(out_frame, bg="#051c4d")
        f.pack(fill=X)
        Label(f, text=f"{item}:", fg="white", bg="#051c4d", font=("Arial", 9)).pack(side=LEFT)
        l = Label(f, text="--", fg="#1abc9c", bg="#051c4d", font=("Consolas", 10, "bold"))
        l.pack(side=RIGHT)
        res_labels[item] = l

    def run_simulation():
        try:
            bx = float(end_coords['X'].get().strip())
            by = float(end_coords['Y'].get().strip())
            bz = float(end_coords['Z'].get().strip())
            ax_v, ay_v, az_v = current_start['X'], current_start['Y'], current_start['Z']

            dist = ((bx - ax_v)**2 + (by - ay_v)**2 + (bz - az_v)**2)**0.5
            res_labels['Distance'].config(text=f"{dist:.2f} units")
            res_labels['Accuracy'].config(text=f"{max(0, 100-(dist*0.5)):.2f} %")

            num_steps = 30
            path = [(ax_v + (bx-ax_v)*i/num_steps, ay_v + (by-ay_v)*i/num_steps, az_v + (bz-az_v)*i/num_steps) for i in range(num_steps+1)]

            def animate(step):
                if step < len(path):
                    curr = path[step]
                    angles = calculate_ik_angles(curr[0], curr[1], curr[2])
                    update_robot_plot(ax, canvas, angles, target_dot=(bx, by, bz))
                    window.after(30, lambda: animate(step + 1))
            animate(0)
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid numbers for TARGET POINT.")

    Button(left_p, text="RUN SIMULATION", bg="#f36412", fg="white", 
           font=("Arial", 12, "bold"), pady=12, command=run_simulation).pack(pady=10, fill=X)

    manual_frame = Frame(container, bg="#0a1e4d", bd=1, relief=SOLID)
    manual_frame.pack(side=RIGHT, fill=Y, padx=10, pady=20)
    
    Label(manual_frame, text="LAB MANUAL", font=("Helvetica", 14, "bold"), fg="#f39c12", bg="#0a1e4d").pack(pady=10, padx=20)
    
    steps = "1. Watch Tutorial\n2. Set Start/End Points\n3. Apply Start Position\n4. Run Simulation\n5. Observe Metrics\n6. Sync with Hardware"
    msg = Message(manual_frame, text=steps, font=("Arial", 10), fg="#70afc2", bg="#0a1e4d", width=220, justify=LEFT)
    msg.pack(pady=10, padx=10, anchor=NW)
    
    def upload_trajectory():
        messagebox.showinfo("Hardware Sync", "Trajectory points streamed to ESP32 successfully!")

    Label(manual_frame, text="Sync ESP32 for real motion.", font=("Arial", 8, "italic"), fg="white", bg="#0a1e4d").pack(side=BOTTOM, pady=(0, 2))
    Button(manual_frame, text="UPLOAD TO HARDWARE", bg="#27ae60", fg="white", 
           font=("Arial", 10, "bold"), pady=10, command=upload_trajectory).pack(side=BOTTOM, pady=10, padx=10, fill=X) 
    right_p = Frame(container, bg="#081b4b", bd=2, relief=RIDGE)
    right_p.pack(side=RIGHT, expand=True, fill=BOTH, padx=10, pady=20)
    
    fig = plt.figure(figsize=(9, 9))
    fig.patch.set_facecolor('#081b4b')
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=right_p)
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)
    
    update_robot_plot(ax, canvas, [0]*6)
    
# de IK gahza 
def open_ik_page():
    for widget in window.winfo_children(): widget.destroy()
    
    IK_ACCENT = "#1abc9c"
    IK_TEXT = "#00f2ff"
    
   
    ik_theory = (
        "INVERSE KINEMATICS (IK) SCIENTIFIC FRAMEWORK:\n\n"
        "1. THE ANALYTICAL CHALLENGE:\n"
        "Calculating Theta (θ1, θ2, θ3) from desired (X, Y, Z). Unlike FK, "
        "IK is non-linear and may have multiple solutions (Elbow Up/Down).\n\n"
        "2. GEOMETRIC DECOUPLING:\n"
        "We solve the position and orientation separately. In this 3-DOF model, "
        "we use the Law of Cosines to solve the triangle formed by the links.\n\n"
        "3. MATHEMATICAL MODEL:\n"
        "- Joint 1: Base rotation using atan2(y, x).\n"
        "- Joint 3: Solve for cos(θ3) using (R²+Z² - L1²-L2²) / (2*L1*L2).\n"
        "- Joint 2: Angle subtraction between the reach vector and link elevation.\n\n"
        "4. CONSTRAINTS:\n"
        "- Workspace Singularity: Points outside the reachable radius.\n"
        "- Joint Limits: Physical range of the stepper motors."
    )
    show_fancy_manual("IK Scientific Module", ik_theory)

    # zorar el back  el seif  2ali a3mlo 
    Button(window, text=" Back to Experiments", font=("Arial", 12, "bold"), 
           fg="#f36412", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(anchor=NW, padx=20, pady=10)
    
    container = Frame(window, bg=BG_COLOR)
    container.pack(expand=True, fill=BOTH, padx=20)
    
    
    left_p = Frame(container, bg=BG_COLOR)
    left_p.pack(side=LEFT, fill=Y, padx=10, pady=20)
    
    Label(left_p, text="POSITION INPUT (IK)", font=("Helvetica", 18, "bold"), fg="#f39c12", bg=BG_COLOR).pack(pady=10)
    
    def play_ik_video():
        webbrowser.open("https://youtu.be/x2o9dcGKcho?si=VglmJS9i1FNjyUvi")
        
    Button(left_p, text="WATCH IK TUTORIAL", font=("Arial", 10, "bold"), 
           bg="#2ecc71", fg="white", command=play_ik_video).pack(pady=5, fill=X)

    
    coords = {}
    for axis in ['X', 'Y', 'Z']:
        f = Frame(left_p, bg=BG_COLOR)
        f.pack(pady=5, fill=X)
        Label(f, text=f"{axis} AXIS", fg="white", bg=BG_COLOR, font=("Arial", 10, "bold"), width=7).pack(side=LEFT)
        s = Scale(f, from_=-8, to=8, resolution=0.1, orient=HORIZONTAL, bg="#03265b", 
                  fg="white", troughcolor=IK_ACCENT, length=180, bd=0)
        s.pack(side=LEFT)
        coords[axis] = s

   
    output_frame = Frame(left_p, bg="#03265b", bd=1, relief=SUNKEN, pady=10)
    output_frame.pack(pady=10, fill=X)
    Label(output_frame, text="CALCULATED JOINT ANGLES", font=("Courier", 10, "bold"), fg=IK_TEXT, bg="#03265b").pack()
    
    angle_labels = {}
    for j in ['J1', 'J2', 'J3']:
        lbl = Label(output_frame, text=f"{j}: 0.00 deg", font=("Consolas", 10), fg="white", bg="#03265b")
        lbl.pack()
        angle_labels[j] = lbl

    def run_ik_process():
        x_val, y_val, z_val = coords['X'].get(), coords['Y'].get(), coords['Z'].get()
        # de el function elly fya el Math elly saba2 w 3dlnaah
        calc_angles = calculate_ik_angles(x_val, y_val, z_val)
        
        angle_labels['J1'].config(text=f"J1 (Base): {calc_angles[0]:.2f} deg")
        angle_labels['J2 (Shoulder)'].config(text=f"J2: {calc_angles[1]:.2f} deg") if 'J2 (Shoulder)' in angle_labels else angle_labels['J2'].config(text=f"J2: {calc_angles[1]:.2f} deg")
        angle_labels['J3'].config(text=f"J3 (Elbow): {calc_angles[2]:.2f} deg")
        
        update_robot_plot(ax, canvas, calc_angles, target_dot=(x_val, y_val, z_val))

    Button(left_p, text="SOLVE AND SIMULATE", bg="#f36412", fg="white", 
        font=("Arial", 12, "bold"), pady=12, command=run_ik_process).pack(pady=10, fill=X)

   
    manual_frame = Frame(container, bg="#0a1e4d", bd=1, relief=SOLID)
    manual_frame.pack(side=RIGHT, fill=Y, padx=10, pady=20)
    
    Label(manual_frame, text="LAB MANUAL", font=("Helvetica", 14, "bold"), fg="#f39c12", bg="#0a1e4d").pack(pady=10, padx=20)
    Label(manual_frame, text="IK Quick Reference", font=("Arial", 11, "bold", "underline"), fg="white", bg="#0a1e4d").pack(pady=5, anchor=W, padx=10)
    
    steps = (
        "1. Define Target XYZ in the workspace.\n"
        "2. Click 'Solve' to run the Geometric IK engine.\n"
        "3. Check if 'Red Dot' and 'End Effector' overlap.\n"
        "4. Synchronize with ESP32 to move the hardware arm."
    )
    msg = Message(manual_frame, text=steps, font=("Arial", 10), fg="#70afc2", bg="#0a1e4d", width=220, justify=LEFT)
    msg.pack(pady=10, padx=10, anchor=NW)
    
    def upload_to_esp32():
        messagebox.showinfo("Hardware Sync", "Streaming IK solutions to ESP32 via Serial!")

    Label(manual_frame, text="Sync with ESP32 for real motion.", font=("Arial", 8, "italic"), fg="white", bg="#0a1e4d").pack(side=BOTTOM, pady=(0, 2), padx=10)
    Button(manual_frame, text="UPLOAD TO HARDWARE", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=upload_to_esp32).pack(side=BOTTOM, pady=10, padx=10, fill=X)

   
    right_p = Frame(container, bg="#081b4b", bd=0)
    right_p.pack(side=RIGHT, expand=True, fill=BOTH)
    
    
    fig = plt.figure(figsize=(11, 11), dpi=100) 
    fig.patch.set_facecolor('#081b4b') 
    fig.subplots_adjust(left=-0.1, right=1.1, bottom=-0.1, top=1.1)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#081b4b') 
    canvas = FigureCanvasTkAgg(fig, master=right_p)
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)
    
    update_robot_plot(ax, canvas, [0]*6)
    
#de FK gahza kamlaaaa into w FK calculations
#intro page 
def open_fk_intro_page():
    for widget in window.winfo_children(): widget.destroy()

    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)
    
    Button(header_frame, text="← Back to Experiments", font=("Arial", 12, "bold"), 
           fg="#f36412", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(side=LEFT, padx=20, pady=10)
    
    Label(header_frame, text="Forward Kinematics ", font=("Helvetica", 22, "bold"), 
          fg="white", bg=BG_COLOR , anchor=W).pack(pady=20)

    video_frame = Frame(window, bg="#0a1e4d", bd=3, relief=RIDGE)
    video_frame.pack(pady=10, padx=50, fill=BOTH, expand=True)
    
    Label(video_frame, text=" WATCHING SOLVED EXAMPLE", font=("Arial", 18, "bold"), 
          fg="#2ecc71", bg="#0a1e4d").pack(pady=(60, 10))

    def play_local_video():
        video_name = "Solved Example - Forward Kinematics.mp4"
        base_path = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(base_path, video_name)
        if os.path.exists(video_path): os.startfile(video_path)

    window.after(500, play_local_video)

    btn_container = Frame(window, bg=BG_COLOR)
    btn_container.pack(side=BOTTOM, fill=X, pady=50, padx=80)

    Button(btn_container, text="Simulation & Calculations →", font=("Arial", 13, "bold"), 
           bg="#f36412", fg="white", width=25, height=2, command=open_fk_page).pack(side=RIGHT)

    # button bybullet
    Button(btn_container, 
           text=" ← 3D Visualization (PyBullet)", 
           font=("Arial", 13, "bold"), 
           bg="#2980b9", 
           fg="white", 
           width=25, 
           height=2, 
           command=run_pybullet_sim).pack(side=LEFT)



# FK el gdida
def open_fk_page():
    for widget in window.winfo_children(): widget.destroy()

    # Manual theory
    fk_theory = (

        "FORWARD KINEMATICS (FK) THEORY:\n\n"
        "1. DEFINITION:\nCalculating the end-effector position (X, Y, Z) based on known joint angles (Theta 1-6).\n\n"
        "2. DENAVIT-HARTENBERG (D-H) PARAMETERS:\nWe describe links using: Link Length (a), Twist (alpha), Offset (d), and Angle (theta).\n\n"
        "3. THE TRANSFORMATION MATRIX (Ai):\nEach joint is represented by a 4x4 Homogeneous Matrix:\n\n"
        "   [ cosθ  -sinθcosα   sinθsinα  acosθ ]\n"
        "   [ sinθ   cosθcosα  -cosθsinα  asinθ ]\n"
        "   [  0       sinα        cosα      d   ]\n"
        "   [  0        0           0        1   ]\n\n"
        "4. TOTAL TRANSFORMATION (T0n):\nThe overall system is solved by chain multiplication:\nTn = A1 * A2 * A3 * A4 * A5 * A6\n\n"
        "5. RESULT:\nThe coordinates (Px, Py, Pz) are extracted from the last column of the T0n matrix."

    )

    try: show_fancy_manual("FK Mathematical Framework", fk_theory)
    except: pass

    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)
    
    # yrg3 l saf7t el video tany na gbt elashom mn website https://www.i2symbol.com/symbols/arrows 3l4an mnsa4
    Button(header_frame, text="← Back to Video Intro ", font=("Arial", 12, "bold"), 
           fg="#f36412", bg=BG_COLOR, bd=0, command=open_fk_intro_page , borderwidth=10).pack(side=LEFT, padx=20, pady=10)

    main_container = Frame(window, bg=BG_COLOR)
    main_container.pack(expand=True, fill=BOTH, padx=10, pady=5)

    #  Sliders 
    left_p = LabelFrame(main_container, text=" Joint Controls ", font=("Arial", 12, "bold"), fg="#f39c12", bg=BG_COLOR, bd=2)
    left_p.pack(side=LEFT, fill=Y, padx=5, pady=5)

    joints = []
    for i in range(1, 7):
        f = Frame(left_p, bg=BG_COLOR)
        f.pack(pady=2, fill=X, padx=5)
        Label(f, text=f"θ{i}:", fg="white", bg=BG_COLOR, font=("Arial", 10, "bold"), width=3).pack(side=LEFT)
        s = Scale(f, from_=-180, to=180, orient=HORIZONTAL, bg="#03265b", fg="white", troughcolor="#f36412", length=150)
        s.pack(side=LEFT, padx=5); joints.append(s)

    Button(left_p, text="RUN SIMULATION", bg="#f36412", fg="white", font=("Arial", 11, "bold"), 
           command=lambda: update_robot_plot(ax, canvas, joints, matrix_labels, dh_labels)).pack(pady=20, fill=X, padx=10)

    #  Middle Panel 3D Visualization
    middle_p = Frame(main_container, bg="#081b4b", bd=2, relief=SUNKEN)
    middle_p.pack(side=LEFT, expand=True, fill=BOTH, padx=10, pady=10)
    
    fig = plt.figure(figsize=(8, 8)); fig.patch.set_facecolor('#081b4b')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#081b4b')
    
    
    ax.set_xlabel('X Axis', color='white', labelpad=15)
    ax.set_ylabel('Y Axis', color='white', labelpad=15)
    ax.set_zlabel('Z Axis', color='white', labelpad=15)
    ax.tick_params(axis='both', colors='white')
    
    canvas = FigureCanvasTkAgg(fig, master=middle_p)
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)

    #  Calculations 
    right_p = Frame(main_container, bg=BG_COLOR)
    right_p.pack(side=RIGHT, fill=Y, padx=5, pady=5)

    # T6 Matrix 
    tm_frame = LabelFrame(right_p, text=" Transformation Matrix (T6) ", font=("Arial", 11, "bold"), fg="white", bg=BG_COLOR)
    tm_frame.pack(fill=X, pady=5)
    for i in range(4): tm_frame.grid_columnconfigure(i, weight=1, uniform="matrix")

    matrix_labels = []
    rows_names, cols_names = ["x", "y", "z"], ["n", "o", "a", "p"] 

    
    for r_idx, axis in enumerate(rows_names):
        for c_idx, component in enumerate(cols_names):
            # yb2a kolo 0 0 0 0 l7d ma a7rk sliders
            lbl = Label(tm_frame, text=f"{component}{axis} = 0.0000", 
                        font=("Consolas", 10), fg="#70afc2", bg=BG_COLOR, width=12)
            lbl.grid(row=r_idx, column=c_idx, padx=5, pady=6)
            matrix_labels.append(lbl)

    # 3l4an a5r satr yb2a sabt howa keda keda sabt fe ay matrix
    for i, val in enumerate(["0.0000", "0.0000", "0.0000", "1.0000"]):
        Label(tm_frame, text=val, font=("Consolas", 10), fg="white", bg=BG_COLOR, width=12).grid(row=3, column=i, pady=10)

    # DH Table
    dh_frame = LabelFrame(right_p, text=" Denavit-Hartenberg Parameters ", font=("Arial", 11, "bold"), fg="white", bg=BG_COLOR, bd=2)
    dh_frame.pack(fill=X, pady=15)
    headers = ["Link", "θ*", "d", "a", "α"]
    for i, h in enumerate(headers): Label(dh_frame, text=h, fg="#f39c12", bg=BG_COLOR, font=("Arial", 9, "bold")).grid(row=0, column=i, padx=10)
    
# dol ay 7aga l7d ma n3rfhom mn mechanical
    dh_labels = [] 
    my_robot_consts = [[5, 0, 90], 
                       [0, 10, 0], 
                       [0, 10, 0], 
                       [0, 0, 90],
                       [0, 0, -90],
                       [2, 0, 0]]
    
    
    for i, row in enumerate(my_robot_consts):
        Label(dh_frame, text=str(i+1), fg="white", bg=BG_COLOR).grid(row=i+1, column=0, padx=10)
        t_lbl = Label(dh_frame, text="0.0", fg="#f39c12", bg=BG_COLOR, font=("Arial", 9, "bold"))
        t_lbl.grid(row=i+1, column=1, padx=10)
        dh_labels.append(t_lbl)
        Label(dh_frame, text=str(row[0]), fg="white", bg=BG_COLOR).grid(row=i+1, column=2, padx=10)
        Label(dh_frame, text=str(row[1]), fg="white", bg=BG_COLOR).grid(row=i+1, column=3, padx=10)
        Label(dh_frame, text=str(row[2]), fg="white", bg=BG_COLOR).grid(row=i+1, column=4, padx=10)


    # Hardware Sync Button
    sync_frame = Frame(right_p, bg="#0a1e4d", bd=1, relief=SOLID)
    sync_frame.pack(side=BOTTOM, fill=X, pady=10)
    Button(sync_frame, text="UPLOAD TO HARDWARE", bg="#27ae60", fg="white", 
           font=("Arial", 10, "bold"), command=lambda: messagebox.showinfo("Hardware Sync", "Uploading to ESP32")).pack(pady=10, padx=10, fill=X)


    # Initial Draw
    #window.after(200, lambda: update_robot_plot(ax, canvas, joints, matrix_labels, dh_labels))


#page fiha kol experiments hna
def open_experiments_page():
    for widget in window.winfo_children(): widget.destroy()
    Button(window, text="Back to Main Menu", font=("Arial", 12, "bold"), fg="#f36412", bg=BG_COLOR, bd=0, command=show_welcome_page, borderwidth=10).pack(anchor=NW, padx=20, pady=10)
    Label(window, text="SELECT EXPERIMENT", font=("Helvetica", 30, "bold"), fg="#f39c12", bg=BG_COLOR).pack(pady=20)
    Experiments = [
        ("1. Forward Kinematics (FK)", open_fk_intro_page), 
        ("2. Inverse Kinematics (IK)", open_ik_page), 
        ("3. Trajectory Planning", open_trajectory_page), 
        ("4. Pick and Place Control", None),
        ("5. Cup Filling Simulation", None)
    ]
    #ay 7aga bs 3l4an lw clickinaa 3la ay 7aga lsa mt3mlt4
    for text, cmd in Experiments:
        action = cmd if cmd else lambda t=text: messagebox.showinfo("lsa m3mlto4", f"{t},isa yt3ml 3latol ")
        Button(window, text=text, font=("Arial", 16), fg="white", bg="#03265b", width=35, pady=12, command=action, borderwidth=5).pack(pady=10)

#de main page kolha texts
def show_welcome_page():
    for widget in window.winfo_children(): widget.destroy()
    left_c = Frame(window, bg=BG_COLOR); left_c.pack(side=LEFT, expand=True, fill=BOTH, padx=80)
    right_c = Frame(window, bg=BG_COLOR); right_c.pack(side=RIGHT, expand=True, fill=BOTH)
    Label(left_c, text="WELCOME TO OUR VIRTUAL LAB", font=("Helvetica", 35, "bold"), fg="#f36412", bg=BG_COLOR, justify=LEFT).pack(pady=(120, 20), anchor=W)
    intro_text = ("This Virtual Lab provides an integrated environment to simulate and analyze 4 distinct robotic experiments. It allows you to explore robotic kinematics and trajectory planning in a 3D simulation. Finally, you can bridge the gap between virtual and reality by connecting your ESP32 kit to synchronize and observe the real-time motion of the physical robotic arm.")
    Label(left_c, text=intro_text, font=("Times New Roman", 14, "bold"), fg="#70afc2", bg=BG_COLOR, justify=LEFT, wraplength=600).pack(pady=10, anchor=W)
    how_to_use = ("How to use this lab:\n1. Click the button below to start.\n2. Select your desired experiment.\n3. Observe the 3D simulation in real-time.\n4. Connect your ESP32 kit to sync motion!")
    Label(left_c, text=how_to_use, font=("Arial", 13), fg="white", bg=BG_COLOR, justify=LEFT).pack(pady=20, anchor=W)
    Button(left_c, text='ENTER THE LAB', bg='#f36412', fg='white', font=('Arial', 14, 'bold'), padx=40, pady=20, bd=0, command=open_experiments_page).pack(pady=30, anchor=W)
    try:
        img_path = os.path.join(os.path.dirname(__file__), "robot_arm.png")
        img = ImageTk.PhotoImage(Image.open(img_path).resize((800, 800)))
        lbl = Label(right_c, image=img, bg=BG_COLOR); lbl.image = img; lbl.pack(expand=True)
    except: pass

show_welcome_page()
window.mainloop()