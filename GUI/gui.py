#libraries
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
import matplotlib.ticker as ticker
from PIL import Image, ImageTk
import csv
from datetime import datetime



#3l4an a create window 
window = Tk()
window.title('Robotic Arm Virtual Lab App')
window.state('zoomed') 
BG_COLOR = "#04153B" 
window.configure(bg=BG_COLOR)

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
def update_robot_plot(ax, canvas, joints, matrix_labels=None, dh_labels=None, ee_coords=None):
    ax.clear()
    # Style
    ax.set_facecolor('#081b4b')
    ax.set_box_aspect([1, 1, 0.7])
    ax.grid(False)

    angles = []
    for j in joints:
        try:
            # Ben7awel el text le float el awel, ba3den radians
            val = float(j.get()) if hasattr(j, "get") else float(j)
            angles.append(np.radians(val))
        except ValueError:
            # Lw el user katab 7arf aw sabha fadya,n5leha 0.0
            angles.append(0.0)
            
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
            [0,   sa,     ca,     d_dh],
            [0,   0,      0,      1]
        ])
        T_total = T_total @ A


    ax.plot([x, x], [y, y], [0, z], color="white", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.plot([0, x], [y, y], [0, 0], color="#e74c3c", linestyle=":", linewidth=1)
    ax.plot([x, x], [0, y], [0, 0], color="#2ecc71", linestyle=":", linewidth=1)
    
    
    ax.text(x, y, z + 1.5, f"P({x:.1f}, {y:.1f}, {z:.1f})", color="#f1c40f", 
            fontsize=10, fontweight='bold', ha='center',
            bbox=dict(facecolor='#081b4b', alpha=0.6, edgecolor='none'))
   

   
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(5))


    ax.grid(True, which='major', linestyle='--', linewidth=0.5, color='white', alpha=0.2)
    
    ax.set_xlabel('X Axis (cm)', color='#00eeee', fontweight='bold')
    ax.set_ylabel('Y Axis (cm)', color='#00eeee', fontweight='bold')
    ax.set_zlabel('Z Axis (cm)', color='#00eeee', fontweight='bold')


    ax.set_xlim([-15, 30])
    ax.set_ylim([-20, 20])
    ax.set_zlim([0, 30])
    
    
    ax.tick_params(colors="white", labelsize=8)
    ax.set_title("6-DOF ROBOTIC ARM SIMULATION", color="white", fontsize=12, fontweight="bold")
    
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

    
    if ee_coords:
        ee_coords["X"].config(text=f"{x:.2f}")
        ee_coords["Y"].config(text=f"{y:.2f}")
        ee_coords["Z"].config(text=f"{z:.2f}")

    if dh_labels:
        for i, s in enumerate(joints):
            try:
                # Lazem float 3ashan el formatting (:.1f) yashtaghal
                val = float(s.get())
                dh_labels[i].config(text=f"{val:.1f}")
            except ValueError:
                dh_labels[i].config(text="0.0")
                
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
    for widget in window.winfo_children(): 
        widget.destroy()
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "video_preview.PNG")
    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)
    Button(header_frame, text="← Back to Experiments", font=("Arial", 12, "bold"), 
           fg="#f36412", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(side=LEFT, padx=20, pady=10)
    
    Label(header_frame, text="Forward Kinematics ", font=("Helvetica", 22, "bold"), 
          fg="white", bg=BG_COLOR , anchor=W).pack(pady=20)

    def play_local_video():
        video_name = "Solved Example - Forward Kinematics.mp4"
        video_full_path = os.path.join(base_path, video_name)
        if os.path.exists(video_full_path): 
            os.startfile(video_full_path)
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Video not found at: {video_full_path}")

    video_frame = Frame(window, bg="#0a1e4d", bd=3, relief=RIDGE)
    video_frame.pack(pady=10, padx=50, fill=BOTH, expand=True)
    
    Label(video_frame, text="WATCHING TUTORIAL", font=("Arial", 18, "bold"), 
          fg="#2ecc71", bg="#0a1e4d").pack(pady=(20, 10))

    preview_container = Frame(video_frame, bg="#0a1e4d")
    preview_container.pack(expand=True)

    image_path = r"C:\Users\Bassant\robot-arm-educational-kit\GUI\video_preview.png"
    try:
        img = Image.open(image_path) 
        img = img.resize((750, 420), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        img_label = Label(preview_container, image=photo, bg="#0a1e4d", cursor="hand2")
        img_label.image = photo
        img_label.pack(pady=10)
        
        img_label.bind("<Button-1>", lambda e: play_local_video())
        Label(preview_container, text="Click image to play tutorial", 
              font=("Arial", 10, "italic"), fg="white", bg="#0a1e4d").pack()

    except Exception as e:
    
        print(f"DEBUG: Image not found at {image_path}. Error: {e}")
        Button(preview_container, text="▶ Watch Tutorial", font=("Arial", 16, "bold"),
               bg="#2ecc71", fg="white", padx=30, pady=15,
               command=play_local_video, cursor="hand2").pack(pady=50)

    btn_container = Frame(window, bg=BG_COLOR)
    btn_container.pack(side=BOTTOM, fill=X, pady=40, padx=80)
    Button(btn_container, text="Simulation & Calculations →", font=("Arial", 13, "bold"), 
           bg="#f36412", fg="white", width=25, height=2, command=open_fk_page).pack(side=RIGHT)
    Button(btn_container, text=" ← 3D Visualization (PyBullet)", font=("Arial", 13, "bold"), 
           bg="#2980b9", fg="white", width=25, height=2, command=run_pybullet_sim).pack(side=LEFT)



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
    
    #  Inputs (Entry Boxes instead of Sliders)
    left_p = LabelFrame(main_container, text=" Joint Controls (Degrees) ", font=("Arial", 12, "bold"), fg="#f39c12", bg=BG_COLOR, bd=2)
    left_p.pack(side=LEFT, fill=Y, padx=5, pady=5)
    
    #  Joint Controls Container
    left_p = LabelFrame(main_container, text=" Joint Controls ", font=("Arial", 12, "bold"), 
                        fg="#f39c12", bg=BG_COLOR, bd=2, padx=10, pady=10)
    left_p.pack(side=LEFT, fill=Y, padx=10, pady=5)
    
    joints = []
    # Esmaa el joints 3ashan nsa3ed el user
    joint_names = ["Base", "Shoulder", "Elbow", "Wrist Pitch", "Wrist Roll", "Gripper"]

    for i in range(6):
        # Frame le kol joint (Card)
        joint_card = Frame(left_p, bg=BG_COLOR, pady=8)
        joint_card.pack(fill=X)
        
        # 1. El Label (esm el joint) mn fo2
        Label(joint_card, text=f"θ{i+1}: {joint_names[i]}", 
              fg="#70afc2", bg=BG_COLOR, font=("Arial", 9, "bold")).pack(anchor=W)
        
        # 2. El Entry Box (t7toh)
        e = Entry(joint_card, font=("Consolas", 12, "bold"), width=15, 
                  justify="center", bg="#0a1e4d", fg="#2ecc71", 
                  insertbackground="white", relief=FLAT, bd=2)
        
        # Trick: Ne3mel line ta7t el box 3ashan yban "Modern"
        e.insert(0, "0.0")
        e.pack(pady=2)
        
        # Line decorative ta7t el box
        Frame(joint_card, height=2, bg="#f36412").pack(fill=X, padx=2)
        
        joints.append(e)

    # Simulation Button
    Button(left_p, text="RUN SIMULATION", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), 
           activebackground="#27ae60", cursor="hand2", 
           command=lambda: update_robot_plot(ax, canvas, joints, matrix_labels, dh_labels, ee_coords)).pack(pady=25, fill=X)
    
    
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
        
    #  End-Effector Position (Coordinates) 
    ee_frame = LabelFrame(right_p, text=" End-Effector Position (X, Y, Z) ", 
                          font=("Arial", 11, "bold"), fg="#27ae60", bg=BG_COLOR, bd=2)
    ee_frame.pack(fill=X, pady=10)

    for i in range(3): ee_frame.grid_columnconfigure(i, weight=1)

    ee_coords = {}
    axes_cfg = [("X", "#e74c3c"), ("Y", "#2ecc71"), ("Z", "#3498db")]

    for i, (axis, color) in enumerate(axes_cfg):
        container = Frame(ee_frame, bg=BG_COLOR)
        container.grid(row=0, column=i, pady=10, padx=2)
        
        Label(container, text=f"{axis}:", font=("Arial", 10, "bold"), fg=color, bg=BG_COLOR).pack(side=LEFT)
        
        
        val_lbl = Label(container, text="0.00", font=("Consolas", 11, "bold"), 
                        fg="white", bg="#0a1e4d", width=7, relief=RIDGE)
        val_lbl.pack(side=LEFT, padx=3)
        ee_coords[axis] = val_lbl

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
    
    # Zorrar el-Back
    Button(window, text="Back to Main Menu", font=("Arial", 12, "bold"), 
           fg="#f36412", bg=BG_COLOR, bd=0, command=show_welcome_page, borderwidth=10).pack(anchor=NW, padx=20, pady=10)
    
    Label(window, text="SELECT EXPERIMENT", font=("Helvetica", 30, "bold"), 
          fg="#f39c12", bg=BG_COLOR).pack(pady=30) 

    Experiments = [
        ("1. Forward Kinematics (FK)", open_fk_intro_page), 
        ("2. Inverse Kinematics (IK)", open_ik_page), 
        ("3. Trajectory Planning", open_trajectory_page), 
        ("4. Pick and Place Control", None)
    ]

    for text, cmd in Experiments:
        def log_and_open(t=text, c=cmd):
            if c:
                save_lab_result(t, "Experiment Started Successfully")
                c()
            else:
                messagebox.showinfo("lsa m3mlto4", f"{t}, isa yt3ml 3latol")

        
        Button(window, text=text, font=("Arial", 16, "bold"), fg="white", 
               bg="#03265b", width=35, pady=18, 
               command=log_and_open, 
               borderwidth=5).pack(pady=15) 

file_path = "lab_records.csv"

if not os.path.exists(file_path):
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Student Name", "Student ID", "Experiment Type", "Result Data"])

CURRENT_USER = ""
CURRENT_ID = ""

def save_lab_result(exp_name, data_values):
    # Lazm CURRENT_USER yeb2a global hena kaman
    global CURRENT_USER, CURRENT_ID
    with open("lab_records.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            CURRENT_USER, 
            CURRENT_ID, 
            exp_name, 
            data_values
        ])

def show_login_page():
    for widget in window.winfo_children(): widget.destroy()
    
    login_frame = Frame(window, bg=BG_COLOR)
    login_frame.pack(expand=True, fill=BOTH)

    card = Frame(login_frame, bg="#0d2142", highlightbackground="#099da5", highlightthickness=2, padx=50, pady=50)
    card.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(card, text="STUDENT IDENTIFICATION", font=("Helvetica", 18, "bold"), fg="#099da5", bg="#0d2142").pack(pady=(0, 20))

    Label(card, text="Full Name:", font=("Arial", 10), fg="#efefef", bg="#0d2142").pack(anchor=W)
    name_entry = Entry(card, font=("Arial", 14), bg="#050c1f", fg="white", insertbackground="white", bd=0)
    name_entry.pack(fill=X, pady=(5, 15))
    Frame(card, height=1, bg="#099da5").pack(fill=X)

    Label(card, text="Student ID:", font=("Arial", 10), fg="#efefef", bg="#0d2142").pack(anchor=W)
    id_entry = Entry(card, font=("Arial", 14), bg="#050c1f", fg="white", insertbackground="white", bd=0)
    id_entry.pack(fill=X, pady=(5, 15))
    Frame(card, height=1, bg="#099da5").pack(fill=X)

    def final_step():
        global CURRENT_USER, CURRENT_ID
        name = name_entry.get()
        uid = id_entry.get()
        
        if name and uid:
            CURRENT_USER = name
            CURRENT_ID = uid
            
            # Save data awel ma ydous verify
            save_lab_result("Login System", "Student Verified & Entered Lab")

            try:
                open_experiments_page() 
            except NameError:
               
                print("Error: Function 'open_experiments_page' not found!")
        else:
            err = Label(card, text="Please fill all fields", fg="#f36412", bg="#0d2142")
            err.pack(pady=5)
            window.after(2000, err.destroy)
    Button(card, text="VERIFY & ENTER LAB →", bg="#099da5", fg="white", 
           font=("Arial", 12, "bold"), padx=30, pady=10, bd=0, command=final_step).pack(pady=25)



#de main page kolha texts
def show_welcome_page():
    for widget in window.winfo_children(): 
        widget.destroy()
    
    main_frame = Frame(window, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH)

    # Headers
    Label(main_frame, text="6-DOF ROBOTIC ARM EDUCATIONAL KIT", 
          font=("Helvetica", 24, "bold"), fg="#099da5", bg=BG_COLOR).place(relx=0.5, rely=0.05, anchor=CENTER)
    Label(main_frame, text="VIRTUAL LAB INTERFACE v1.0", font=("Consolas", 10, "bold"), 
          fg="#efefef", bg=BG_COLOR).place(relx=0.5, rely=0.08, anchor=CENTER)

   
    try:
        logo_path = r"C:\Users\Bassant\robot-arm-educational-kit\GUI\uni_logo.png"
        logo_img = Image.open(logo_path).resize((110, 110), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        l_lbl = Label(main_frame, image=logo_photo, bg=BG_COLOR)
        l_lbl.image = logo_photo
        l_lbl.place(relx=0.92, rely=0.07, anchor=CENTER)
    except: 
        pass

    
    text_container = Frame(main_frame, bg=BG_COLOR)
    text_container.place(relx=0.07, rely=0.15, width=500)

    title_txt = "WELCOME TO\nOUR\nVIRTUAL LAB"
    Label(text_container, text=title_txt, font=("Helvetica", 48, "bold"), 
          fg="#050c1f", bg=BG_COLOR, justify=LEFT).place(x=3, y=3)
    Label(text_container, text=title_txt, font=("Helvetica", 48, "bold"), 
          fg="#099da5", bg=BG_COLOR, justify=LEFT).pack(anchor=W)

    desc_text = ("Explore robotics through real-time simulation, motion analysis,\n"
                 "and live synchronization with a physical 6-DOF robotic arm.")
    Label(text_container, text=desc_text, font=("Segoe UI", 12, "italic"), 
          fg="#efefef", bg=BG_COLOR, justify=LEFT).pack(pady=(15, 10), anchor=W)


    instr_card = Frame(text_container, bg="#0d2142", bd=0, highlightbackground="#099da5", highlightthickness=1, padx=20, pady=15)
    instr_card.pack(anchor=W, fill=X, pady=10)
    
    Label(instr_card, text="LABORATORY OBJECTIVES & SCOPE:", font=("Arial", 11, "bold"), fg="#efefef", bg="#0d2142").pack(anchor=W, pady=(0,5))
    
    points = [
        "• REAL-TIME SIMULATION: Visualize robotic arm motion inside a 3D virtual workspace.",
        "• HARDWARE SYNCHRONIZATION: Observe the physical robotic arm responding live to simulation commands.",
        "• KINEMATIC ANALYSIS: Perform Forward and Inverse Kinematics calculations using DH Parameters.",
        "• TRAJECTORY & CONTROL: Analyze motion paths, joint behavior, and actuator responses in real time."
    ]
    for p in points:
        Label(instr_card, text=p, font=("Arial", 9), fg="#9db2bf", bg="#0d2142", justify=LEFT, wraplength=450).pack(anchor=W, pady=2)

   
    btn_get_started = Button(text_container, text="GET STARTED / LOGIN →", bg="#099da5", fg="white", 
                            font=("Arial", 12, "bold"), padx=40, pady=12, bd=0, cursor="hand2",
                            command=show_login_page) 
    btn_get_started.pack(pady=20, anchor=W)

    
    glow_frame = Frame(main_frame, bg="#0d2142", bd=0, highlightbackground="#099da5", highlightthickness=1)
    glow_frame.place(relx=0.55, rely=0.20, width=520, height=580)

    try:
        robot_path = os.path.join(os.path.dirname(__file__), "robot_arm.png")
        r_img = Image.open(robot_path).resize((480, 480), Image.Resampling.LANCZOS)
        r_photo = ImageTk.PhotoImage(r_img)
        robot_lbl = Label(glow_frame, image=r_photo, bg="#14264d")
        robot_lbl.image = r_photo
        robot_lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

        #3ayzen nzabt animation zi ma shahd 2alttt
        def animate_robot(angle=0):
            import math
            # Sin wave movement (10 pixels up/down)
            off_y = math.sin(angle) * 10 
            robot_lbl.place(relx=0.5, rely=0.5, y=off_y, anchor=CENTER)
            # Repeat after 20ms (Fast & Smooth)
            window.after(20, lambda: animate_robot(angle + 0.1)) 
            
        animate_robot()
        
    except Exception as e: 
        print(f"Error in animation or image: {e}")

show_welcome_page()       
window.mainloop()