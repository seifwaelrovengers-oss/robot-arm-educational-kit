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
import serial
import time
import math
from tkinter import ttk
import PIL.Image  
from PIL import ImageTk
import tkinter as tk  
from tkinter import Frame, Label, Entry, Button, LabelFrame, ttk, messagebox
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame, Label, Entry, Button, ttk, messagebox, SUNKEN, FLAT, LEFT, X, BOTH, Y, RIGHT, BOTTOM, SOLID, RIDGE, TOP



#3l4an a create window 
window = Tk()
window.title('Robotic Arm Virtual Lab App')
window.state('zoomed') 
BG_COLOR = "#04153B" 
window.configure(bg=BG_COLOR)

# file seif 

def run_pybullet_sim():
    try:
        # 1. 7ot asma2 el files kolaha hna f List wa7da
        all_files = ["twin.py", "fk.py"] 
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Lef mara wa7da (Loop) 3la kol el files
        for file_name in all_files:
            file_path = os.path.join(base_path, file_name)
            
            if os.path.exists(file_path):
                # Sha8al el file
                subprocess.Popen(["python", file_path])
            else:
                # Law file na2es, talle3 error w kammel elly ba3do (aw emel break)
                messagebox.showerror("File Error", f"El file '{file_name}' mesh mawgood!\nEt2aked eno fe nfs el folder.")
                
    except Exception as e:
        messagebox.showerror("Error", f"Ma3reftsh afta7 el simulation: {str(e)}")

  
# bayza lsa 
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

    Button(start_frame, text="Run SImulation", bg="#3498db", fg="white", 
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
    
def open_ik_intro_page():
    
    for widget in window.winfo_children(): 
        widget.destroy()

    base_path = os.path.dirname(os.path.abspath(__file__))
    
   
    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)
    
    Button(header_frame, text="← Back to Experiments", font=("Arial", 12, "bold"), 
           fg="#099da5", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(side=LEFT, padx=20, pady=10)
    
    Label(header_frame, text="Inverse Kinematics", font=("Helvetica", 22, "bold"), 
          fg="white", bg=BG_COLOR, anchor=W).pack(pady=20)

    
    def play_ik_video():
        video_name = "inverse_kinematics_mp4_video.mp4" 
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

   
    ik_image_path = os.path.join(base_path, "IK_video_preview.png") 
    
    try:
        img = Image.open(ik_image_path) 
        img = img.resize((750, 420), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        img_label = Label(preview_container, image=photo, bg="#0a1e4d", cursor="hand2")
        img_label.image = photo
        img_label.pack(pady=10)
        
        img_label.bind("<Button-1>", lambda e: play_ik_video())
        Label(preview_container, text="Click image to play Inverse Kinematics tutorial", 
              font=("Arial", 10, "italic"), fg="white", bg="#0a1e4d").pack()

    except Exception as e:
        print(f"DEBUG: IK Image not found. Error: {e}")
        Button(preview_container, text="▶ Watch IK Tutorial", font=("Arial", 16, "bold"),
               bg="#2ecc71", fg="white", padx=30, pady=15,
               command=play_ik_video, cursor="hand2").pack(pady=50)

    
    btn_container = Frame(window, bg=BG_COLOR)
    btn_container.pack(side=BOTTOM, fill=X, pady=40, padx=80)
    
    
    Button(btn_container, text="Simulation & Calculations →", font=("Arial", 13, "bold"), 
           bg="#f36412", fg="white", width=25, height=2, command=open_ik_page).pack(side=RIGHT)

    Button(btn_container, text=" ← 3D Visualization (PyBullet)", font=("Arial", 13, "bold"), 
           bg="#2980b9", fg="white", width=25, height=2, command=run_pybullet_sim).pack(side=LEFT)
    show_university_logo()       
 
 
 
    



# yarb IK t5ls b2aaaaaaaaaa

def open_ik_page():



    for widget in window.winfo_children():
        widget.destroy()

    global SAVED_A_MATRICES, SAVED_T06

    SAVED_A_MATRICES = []
    SAVED_T06 = None

    BG_COLOR = "#0c1a30"

    IK_METHOD = StringVar(value="Geometric")

   

    def draw_3d_cylinder(ax, p1, p2, radius=7, color='#3498db'):

        try:

            v = p2 - p1
            mag = np.linalg.norm(v)

            if mag < 1e-5:
                return

            v = v / mag

            not_v = np.array([1,0,0])

            if abs(v[0]) > 0.9:
                not_v = np.array([0,1,0])

            n1 = np.cross(v, not_v)
            n1 /= np.linalg.norm(n1)

            n2 = np.cross(v, n1)

            t = np.linspace(0, 2*np.pi, 25)

            X = []
            Y = []
            Z = []

            for s in [0,1]:

                circle = p1 + (p2-p1)*s

                x = circle[0] + radius*np.cos(t)*n1[0] + radius*np.sin(t)*n2[0]
                y = circle[1] + radius*np.cos(t)*n1[1] + radius*np.sin(t)*n2[1]
                z = circle[2] + radius*np.cos(t)*n1[2] + radius*np.sin(t)*n2[2]

                X.append(x)
                Y.append(y)
                Z.append(z)

            ax.plot_surface(
                np.array(X),
                np.array(Y),
                np.array(Z),
                color=color,
                alpha=0.95
            )

        except:
            pass

    

    def draw_gripper(ax, p6, t1, t2, t3):

        try:

            alpha = math.radians(t2+t3)
            beta = math.radians(t1)

            forward = np.array([
                math.cos(alpha)*math.cos(beta),
                math.cos(alpha)*math.sin(beta),
                math.sin(alpha)
            ])

            side = np.array([
                -math.sin(beta),
                math.cos(beta),
                0
            ])

            claw_length = 30
            claw_gap = 12

            claw1_start = p6 + side*claw_gap
            claw1_end = claw1_start + forward*claw_length

            claw2_start = p6 - side*claw_gap
            claw2_end = claw2_start + forward*claw_length

            ax.plot3D(
                [claw1_start[0], claw1_end[0]],
                [claw1_start[1], claw1_end[1]],
                [claw1_start[2], claw1_end[2]],
                color='#f1c40f',
                linewidth=4
            )

            ax.plot3D(
                [claw2_start[0], claw2_end[0]],
                [claw2_start[1], claw2_end[1]],
                [claw2_start[2], claw2_end[2]],
                color='#f1c40f',
                linewidth=4
            )

            ax.plot3D(
                [claw1_start[0], claw2_start[0]],
                [claw1_start[1], claw2_start[1]],
                [claw1_start[2], claw2_start[2]],
                color='#e67e22',
                linewidth=5
            )

        except:
            pass

    

    def update_matrix_view(event=None):

        if len(SAVED_A_MATRICES) == 0:
            return

        idx = matrix_selector.current()

        matrices = [
            SAVED_A_MATRICES[0],
            SAVED_A_MATRICES[1],
            SAVED_A_MATRICES[2],
            SAVED_T06
        ]

        titles = [
            "A1 MATRIX",
            "A2 MATRIX",
            "A3 MATRIX",
            "T06 MATRIX"
        ]

        descriptions = [

            "Base Rotation Matrix\nFrame0 → Frame1",

            "Shoulder Transformation\nControls Link1",

            "Elbow Transformation\nControls Link2",

            "Final End Effector Matrix\nT06 = A1 × A2 × A3"
        ]

        mat = matrices[idx]

        matrix_title.config(text=titles[idx])
        matrix_desc.config(text=descriptions[idx])

        txt = (
            f"[ {mat[0,0]:>8.3f} {mat[0,1]:>8.3f} {mat[0,2]:>8.3f} {mat[0,3]:>8.3f} ]\n"
            f"[ {mat[1,0]:>8.3f} {mat[1,1]:>8.3f} {mat[1,2]:>8.3f} {mat[1,3]:>8.3f} ]\n"
            f"[ {mat[2,0]:>8.3f} {mat[2,1]:>8.3f} {mat[2,2]:>8.3f} {mat[2,3]:>8.3f} ]\n"
            f"[ {mat[3,0]:>8.3f} {mat[3,1]:>8.3f} {mat[3,2]:>8.3f} {mat[3,3]:>8.3f} ]"
        )

        matrix_lbl.config(text=txt)

  # workspace m4 kwisa 3andk 

    def draw_workspace(ax, d1, a2, a3):

        reach = a2 + a3

        u = np.linspace(0, 2*np.pi, 50)
        v = np.linspace(0, np.pi, 50)

        x = reach * np.outer(np.cos(u), np.sin(v))
        y = reach * np.outer(np.sin(u), np.sin(v))
        z = reach * np.outer(np.ones(np.size(u)), np.cos(v))

        z = z + d1

        ax.plot_wireframe(
            x, y, z,
            color='#1abc9c',
            alpha=0.15
        )

  

    def draw_robot(theta1, theta2, theta3,
                   d1, a2, a3,
                   projection=True):

        ax.clear()

        ax.set_facecolor("#081b4b")

        ax.grid(True, color="#1f2d4d")

  

        p0 = np.array([0,0,0])

        p1 = np.array([0,0,d1])

        p2 = p1 + np.array([
            a2*np.cos(theta2)*np.cos(theta1),
            a2*np.cos(theta2)*np.sin(theta1),
            a2*np.sin(theta2)
        ])

        p3 = p2 + np.array([
            a3*np.cos(theta2+theta3)*np.cos(theta1),
            a3*np.cos(theta2+theta3)*np.sin(theta1),
            a3*np.sin(theta2+theta3)
        ])

        p6 = p3

        pts = [p0,p1,p2,p3]

        colors = [
            '#34495e',
            '#3498db',
            '#9b59b6'
        ]

  

        for i in range(len(pts)-1):

            draw_3d_cylinder(
                ax,
                pts[i],
                pts[i+1],
                radius=7,
                color=colors[i]
            )

            ax.scatter(
                pts[i][0],
                pts[i][1],
                pts[i][2],
                color='#e74c3c',
                s=90
            )

    

        ax.scatter(
            p6[0],
            p6[1],
            p6[2],
            color='yellow',
            s=160
        )

        draw_gripper(
            ax,
            p6,
            math.degrees(theta1),
            math.degrees(theta2),
            math.degrees(theta3)
        )

       

        if projection:

            ax.plot(
                [p6[0], p6[0]],
                [p6[1], p6[1]],
                [0, p6[2]],
                '--',
                color='#00ffff'
            )

            ax.plot(
                [0, p6[0]],
                [0, p6[1]],
                [0, 0],
                '--',
                color='#ff00ff'
            )

# mo7awlaa m4 s7 
        draw_workspace(ax, d1, a2, a3)

        

        max_range = d1+a2+a3+100

        ax.set_xlim([-max_range,max_range])
        ax.set_ylim([-max_range,max_range])
        ax.set_zlim([0,max_range])

        ax.set_xlabel("X Axis (mm)", color='white', fontsize=10)
        ax.set_ylabel("Y Axis (mm)", color='white', fontsize=10)
        ax.set_zlabel("Z Axis (mm)", color='white', fontsize=10)

        ax.tick_params(colors='white')

        ax.view_init(elev=28, azim=40)



        ax.text(
            p6[0],
            p6[1],
            p6[2]+20,
            f"EE\nX={p6[0]:.1f}\nY={p6[1]:.1f}\nZ={p6[2]:.1f}",
            color='yellow'
        )

        canvas.draw()

    

    def animate_robot(target_t1, target_t2, target_t3,
                      d1, a2, a3):

        steps = 40

        for i in range(steps):

            r = i / steps

            t1 = target_t1 * r
            t2 = target_t2 * r
            t3 = target_t3 * r

            draw_robot(
                t1, t2, t3,
                d1, a2, a3
            )

            window.update()

    
    

    def solve_inverse_kinematics():

        try:

            x = float(x_entry.get())
            y = float(y_entry.get())
            z = float(z_entry.get())

            d1 = float(link_entries[0].get())
            a2 = float(link_entries[1].get())
            a3 = float(link_entries[2].get())


            r = math.sqrt(x**2 + y**2)

            s = z - d1

            theta1 = math.atan2(y, x)

            D = ((r**2 + s**2 - a2**2 - a3**2)/(2*a2*a3))

            if abs(D) > 1:

                singularity_lbl.config(
                    text="UNREACHABLE POINT",
                    fg="#ff4d4d"
                )

                return

            theta3 = math.atan2(
                math.sqrt(1-D**2),
                D
            )

            theta2 = math.atan2(s, r) - math.atan2(
                a3*math.sin(theta3),
                a2+a3*math.cos(theta3)
            )

            t1 = math.degrees(theta1)
            t2 = math.degrees(theta2)
            t3 = math.degrees(theta3)

            

            vals = [t1,t2,t3,0,0,0]

            for i in range(6):
                angle_labels[i].config(
                    text=f"{vals[i]:.2f}°"
                )


            c1,s1 = math.cos(theta1), math.sin(theta1)
            c2,s2 = math.cos(theta2), math.sin(theta2)
            c3,s3 = math.cos(theta3), math.sin(theta3)

            A1 = np.array([
                [c1,0,s1,0],
                [s1,0,-c1,0],
                [0,1,0,d1],
                [0,0,0,1]
            ])

            A2 = np.array([
                [c2,-s2,0,a2*c2],
                [s2,c2,0,a2*s2],
                [0,0,1,0],
                [0,0,0,1]
            ])

            A3 = np.array([
                [c3,-s3,0,a3*c3],
                [s3,c3,0,a3*s3],
                [0,0,1,0],
                [0,0,0,1]
            ])

            SAVED_A_MATRICES.clear()

            SAVED_A_MATRICES.extend([
                A1,A2,A3
            ])

            global SAVED_T06

            SAVED_T06 = np.dot(
                np.dot(A1,A2),
                A3
            )

            update_matrix_view()

    

            reach = math.sqrt(x**2+y**2+z**2)

            jacobian_det = abs(
                a2*a3*math.sin(theta3)
            )

            extra_info.config(
                text=
                f"Reach Distance = {reach:.2f} mm\n"
                f"Jacobian Determinant = {jacobian_det:.3f}\n"
                f"Workspace Radius = {(a2+a3):.1f} mm"
            )

            
           

            theory = (
                "GEOMETRIC IK METHOD\n\n"
                "θ1 = atan2(y,x)\n"
                "θ3 from cosine law\n"
                "θ2 from triangle decomposition\n\n"
                "T06 = A1 × A2 × A3\n"
                "Uses Homogeneous Matrices.\n"
                "Fast and stable."
            )

            theory_lbl.config(text=theory)

        
# animation bayzzz 
            animate_robot(
                theta1,
                theta2,
                theta3,
                d1,
                a2,
                a3
            )

           # singularity bayzaaaaaaa 3andyyy rakzyy fe rule tany 

            if abs(math.sin(theta3)) < 0.05:

                singularity_lbl.config(
                    text=
                    "SINGULARITY DETECTED\n"
                    "ELBOW FULLY EXTENDED",
                    fg="orange"
                )

            else:

                singularity_lbl.config(
                    text="SAFE CONFIGURATION",
                    fg="#2ecc71"
                )

        except Exception as e:

            messagebox.showerror(
                "IK ERROR",
                str(e)
            )



    header = Frame(window, bg=BG_COLOR)
    header.pack(fill=X)

    Button(
        header,
        text="← Back to Video Intro",
        font=("Arial", 11, "bold"),
        fg="#099da5",
        bg=BG_COLOR,
        bd=0,
        borderwidth=10,
        activebackground=BG_COLOR,
        activeforeground="#00d2ff",
        cursor="hand2",
        command=open_ik_intro_page
    ).pack(side=LEFT, padx=20, pady=5)

    Label(
        header,
        text="ADVANCED INVERSE KINEMATICS",
        font=("Helvetica",16,"bold"),
        fg="#00d2ff",
        bg=BG_COLOR
    ).pack(pady=10)

    


    main = Frame(window, bg=BG_COLOR)
    main.pack(fill=BOTH, expand=True)



    left = Frame(main, bg=BG_COLOR)
    left.pack(side=LEFT, fill=Y, padx=10)

    # TARGET

    target_frame = LabelFrame(
        left,
        text=" TARGET POSITION ",
        bg=BG_COLOR,
        fg="#2ecc71",
        font=("Arial",10,"bold")
    )

    target_frame.pack(fill=X,pady=5)

    entries = []

    for txt,val in [
        ("X (mm)",180),
        ("Y (mm)",50),
        ("Z (mm)",180)
    ]:

        Label(
            target_frame,
            text=txt,
            bg=BG_COLOR,
            fg="white"
        ).pack()

        e = Entry(
            target_frame,
            font=("Consolas",11)
        )

        e.insert(0,str(val))

        e.pack(fill=X,pady=2)

        entries.append(e)

    x_entry,y_entry,z_entry = entries

   

    links_frame = LabelFrame(
        left,
        text=" LINK LENGTHS ",
        bg=BG_COLOR,
        fg="#f1c40f",
        font=("Arial",10,"bold")
    )

    links_frame.pack(fill=X,pady=5)

    names = [
        "Link1 : 100-220",
        "Link2 : 100-200",
        "Link3 : 50-150"
    ]

    defaults = [160,150,100]

    link_entries = []

    for i in range(3):

        Label(
            links_frame,
            text=names[i],
            bg=BG_COLOR,
            fg="white"
        ).pack()

        e = Entry(
            links_frame,
            font=("Consolas",10)
        )

        e.insert(0,str(defaults[i]))

        e.pack(fill=X,pady=2)

        link_entries.append(e)

    # BUTTON

    Button(
        left,
        text="SOLVE and RUN IK",
        bg="#2ecc71",
        fg="white",
        font=("Arial",11,"bold"),
        command=solve_inverse_kinematics
    ).pack(fill=X,pady=15)

   

    center = Frame(main, bg="#081b4b")
    center.pack(side=LEFT, fill=BOTH, expand=True)

    fig = plt.figure(figsize=(6,6))

    fig.patch.set_facecolor("#081b4b")

    ax = fig.add_subplot(
        111,
        projection='3d'
    )

    canvas = FigureCanvasTkAgg(
        fig,
        master=center
    )

    canvas.get_tk_widget().pack(
        fill=BOTH,
        expand=True
    )



    right = Frame(main, bg=BG_COLOR)
    right.pack(side=RIGHT, fill=Y, padx=10)

    # ANGLES

    angles_frame = LabelFrame(
        right,
        text=" JOINT ANGLES ",
        bg=BG_COLOR,
        fg="#00d2ff",
        font=("Arial",10,"bold")
    )

    angles_frame.pack(fill=X,pady=5)

    joint_names = [
        "Base",
        "Shoulder",
        "Elbow",
        "Wrist",
        "Roll",
        "Yaw"
    ]

    ranges = [
        "-135 → 135",
        "0 → 180",
        "-80 → 90",
        "-90 → 90",
        "-180 → 180",
        "0 → 180"
    ]

    angle_labels = []

    for i in range(6):

        row = Frame(
            angles_frame,
            bg=BG_COLOR
        )

        row.pack(fill=X,pady=2)

        Label(
            row,
            text=joint_names[i],
            bg=BG_COLOR,
            fg="white",
            width=10,
            anchor='w'
        ).pack(side=LEFT)

        Label(
            row,
            text=ranges[i],
            bg=BG_COLOR,
            fg="#f1c40f",
            width=12
        ).pack(side=LEFT)

        lbl = Label(
            row,
            text="0.00°",
            bg="#081b4b",
            fg="#2ecc71",
            width=10,
            font=("Consolas",10,"bold")
        )

        lbl.pack(side=RIGHT)

        angle_labels.append(lbl)



    extra_frame = LabelFrame(
        right,
        text=" EXTRA CALCULATIONS ",
        bg=BG_COLOR,
        fg="#1abc9c",
        font=("Arial",10,"bold")
    )

    extra_frame.pack(fill=X,pady=5)

    extra_info = Label(
        extra_frame,
        text="",
        bg="#081b4b",
        fg="white",
        justify=LEFT,
        font=("Consolas",9)
    )

    extra_info.pack(fill=X,padx=5,pady=5)


    theory_frame = LabelFrame(
        right,
        text=" IK THEORY ",
        bg=BG_COLOR,
        fg="#f1c40f",
        font=("Arial",10,"bold")
    )

    theory_frame.pack(fill=X,pady=5)

    theory_lbl = Label(
        theory_frame,
        text="",
        bg="#081b4b",
        fg="white",
        justify=LEFT,
        wraplength=300,
        font=("Consolas",8)
    )

    theory_lbl.pack(fill=X,padx=5,pady=5)

    # MATRIX

    matrix_frame = LabelFrame(
        right,
        text=" MATRIX ANALYSIS ",
        bg=BG_COLOR,
        fg="#00d2ff",
        font=("Arial",10,"bold")
    )

    matrix_frame.pack(fill=BOTH,expand=True,pady=5)

    matrix_selector = ttk.Combobox(
        matrix_frame,
        values=[
            "A1 Matrix",
            "A2 Matrix",
            "A3 Matrix",
            "T06 Matrix"
        ],
        state="readonly"
    )

    matrix_selector.current(0)

    matrix_selector.pack(
        fill=X,
        pady=5
    )

    matrix_selector.bind(
        "<<ComboboxSelected>>",
        update_matrix_view
    )

    matrix_title = Label(
        matrix_frame,
        text="A1 MATRIX",
        bg=BG_COLOR,
        fg="#2ecc71",
        font=("Arial",10,"bold")
    )

    matrix_title.pack()

    matrix_desc = Label(
        matrix_frame,
        text="",
        bg=BG_COLOR,
        fg="#9db2bf",
        justify=LEFT,
        wraplength=320
    )

    matrix_desc.pack()

    matrix_lbl = Label(
        matrix_frame,
        text="",
        bg="#050c1f",
        fg="#2ecc71",
        justify=LEFT,
        font=("Consolas",8),
        padx=10,
        pady=10
    )

    matrix_lbl.pack(
        fill=X,
        padx=5,
        pady=5
    )

    # SINGULARITY

    singularity_frame = LabelFrame(
        right,
        text=" SINGULARITY ",
        bg=BG_COLOR,
        fg="#ff4d4d",
        font=("Arial",10,"bold")
    )

    singularity_frame.pack(fill=X,pady=5)

    singularity_lbl = Label(
        singularity_frame,
        text="WAITING...",
        bg="#081b4b",
        fg="white",
        font=("Arial",10,"bold"),
        pady=10
    )

    singularity_lbl.pack(fill=X)

  
    solve_inverse_kinematics()
    show_university_logo()
    
    
    
#de FK gahza kamlaaaa intro w FK calculations
#intro page 
def open_fk_intro_page():
    for widget in window.winfo_children(): 
        widget.destroy()
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "video_preview.PNG")
    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)
    Button(header_frame, text="← Back to Experiments", font=("Arial", 12, "bold"), 
           fg="#099da5", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(side=LEFT, padx=20, pady=10)
    
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
    show_university_logo()




# Fk PAGE 

SAVED_A_MATRICES = [np.eye(4) for _ in range(6)]
SAVED_T06 = np.eye(4)

is_sim_started = False

def open_fk_page():
    for widget in window.winfo_children(): 
        widget.destroy()

   
    def draw_3d_cylinder(ax, p1, p2, radius=8, color='#2ecc71'):
        try:
            v = p2 - p1
            mag = np.linalg.norm(v)
            if mag < 1e-3: return
            v_norm = v / mag
            n = 12
            theta = np.linspace(0, 2*np.pi, n)
            if abs(v_norm[0]) < 0.9:
                not_v = np.array([1, 0, 0])
            else:
                not_v = np.array([0, 1, 0])
            u1 = np.cross(v_norm, not_v)
            u1 /= np.linalg.norm(u1)
            u2 = np.cross(v_norm, u1)
            
            z_steps = np.linspace(0, 1, 2)
            X, Y, Z = [], [], []
            for z in z_steps:
                x_circle = p1[0] + z*v[0] + radius * (np.cos(theta)*u1[0] + np.sin(theta)*u2[0])
                y_circle = p1[1] + z*v[1] + radius * (np.cos(theta)*u1[1] + np.sin(theta)*u2[1])
                z_circle = p1[2] + z*v[2] + radius * (np.cos(theta)*u1[2] + np.sin(theta)*u2[2])
                X.append(x_circle)
                Y.append(y_circle)
                Z.append(z_circle)
            ax.plot_surface(np.array(X), np.array(Y), np.array(Z), color=color, alpha=0.85, shade=True)
        except:
            pass


    def run_fk_calculations(from_button=False):
        global SAVED_A_MATRICES, SAVED_T06, is_sim_started
        
        try:
       # gripper na2ss hna
            joint_limits = [
                (-135.0, 135.0), # Base
                (0.0, 180.0),    # Shoulder
                (-80.0, 90.0),   # Elbow
                (-90.0, 90.0),   # Wrist Pitch / Rest
                (-180.0, 180.0), # Wrist Roll / Roll
                (0.0, 180.0)     # Yaw / Gripper
            ]
            
        # limits bt3t mina kolo mm
            dim_limits = [
                (100.0, 220.0),  # Link 1
                (100.0, 200.0),  # Link 2
                (50.0, 150.0)    # Link 3
            ]

           
            thetas_deg = []
            for idx, j_entry in enumerate(joints):
                val = float(j_entry.get())
                min_lim, max_lim = joint_limits[idx]
                if from_button and (val < min_lim or val > max_lim):
                    messagebox.showwarning("Limit Violation", f"Joint θ{idx+1} ({joint_names[idx]}) out of range!\nAllowed: {min_lim} to {max_lim} deg.")
                    return
                thetas_deg.append(val)
            
            thetas = [math.radians(t) for t in thetas_deg]
            
           
            link_vals = []
            for idx, d_entry in enumerate(link_dims):
                val = float(d_entry.get())
                min_lim, max_lim = dim_limits[idx]
                if from_button and (val < min_lim or val > max_lim):
                    messagebox.showwarning("Limit Violation", f"Link {idx+1} Dimension out of range!\nAllowed: {min_lim} to {max_lim} mm.")
                    return
                link_vals.append(val)

            d1_val, a2_val, a3_val = link_vals[0], link_vals[1], link_vals[2]
            d6_val = 40.0  
            
            if from_button:
                is_sim_started = True

           # alphass ay 7aga l7d ma ttzbt 
            alphas = [math.radians(90), 0, 0, math.radians(90), math.radians(-90), 0]
           # 7sbat kol links 3la asas alphas 
            # Link 1
            c1, s1 = math.cos(thetas[0]), math.sin(thetas[0])
            ca1, sa1 = math.cos(alphas[0]), math.sin(alphas[0])
            SAVED_A_MATRICES[0] = np.array([
                [c1, -s1*ca1,  s1*sa1, 0],
                [s1,  c1*ca1, -c1*sa1, 0],
                [ 0,     sa1,     ca1, d1_val],
                [ 0,       0,       0, 1]
            ])
            
            # Link 2
            c2, s2 = math.cos(thetas[1]), math.sin(thetas[1])
            ca2, sa2 = math.cos(alphas[1]), math.sin(alphas[1])
            SAVED_A_MATRICES[1] = np.array([
                [c2, -s2*ca2,  s2*sa2, a2_val * c2],
                [s2,  c2*ca2, -c2*sa2, a2_val * s2],
                [ 0,     sa2,     ca2, 0],
                [ 0,       0,       0, 1]
            ])
            
            # Link 3
            c3, s3 = math.cos(thetas[2]), math.sin(thetas[2])
            ca3, sa3 = math.cos(alphas[2]), math.sin(alphas[2])
            SAVED_A_MATRICES[2] = np.array([
                [c3, -s3*ca3,  s3*sa3, a3_val * c3],
                [s3,  c3*ca3, -c3*sa3, a3_val * s3],
                [ 0,     sa3,     ca3, 0],
                [ 0,       0,       0, 1]
            ])
            
            # Links 4 to 6
            for i in range(3, 6):
                c, s = math.cos(thetas[i]), math.sin(thetas[i])
                ca, sa = math.cos(alphas[i]), math.sin(alphas[i])
                
                d_val = d6_val if i == 5 else 0.0
                
                SAVED_A_MATRICES[i] = np.array([
                    [c, -s*ca,  s*sa, 0.0],
                    [s,  c*ca, -c*sa, 0.0],
                    [0,    sa,    ca, d_val],
                    [0,     0,     0, 1]
                ])
            
            T = np.eye(4)
            for A in SAVED_A_MATRICES:
                T = np.dot(T, A)
            SAVED_T06 = T
            
         
            ax.clear()
            ax.set_facecolor('#081b4b')
            ax.grid(True, color='#1a2a5a', linestyle=':')
            
            max_range = d1_val + a2_val + a3_val + d6_val
            
           
            if is_sim_started:
              
                pts = []
                p0 = np.array([0.0, 0.0, 0.0])
                pts.append(p0)
                
                p1 = np.array([0.0, 0.0, d1_val])
                pts.append(p1)
                
                phi1 = thetas[0]
                phi2 = thetas[1]
                p2 = p1 + np.array([
                    a2_val * math.cos(phi2) * math.cos(phi1),
                    a2_val * math.cos(phi2) * math.sin(phi1),
                    a2_val * math.sin(phi2)
                ])
                pts.append(p2)
                
                phi23 = thetas[1] + thetas[2]
                p3 = p2 + np.array([
                    a3_val * math.cos(phi23) * math.cos(phi1),
                    a3_val * math.cos(phi23) * math.sin(phi1),
                    a3_val * math.sin(phi23)
                ])
                pts.append(p3)
                
                ee_pos = SAVED_T06[0:3, 3]
                
                if all(t == 0 for t in thetas):
                    p4 = p3 + np.array([20.0 * math.cos(phi1), 20.0 * math.sin(phi1), 0.0])
                    p5 = p4 + np.array([20.0 * math.cos(phi1), 20.0 * math.sin(phi1), 0.0])
                    p6 = p5 + np.array([d6_val * math.cos(phi1), d6_val * math.sin(phi1), 0.0])
                    pts.extend([p4, p5, p6])
                else:
                    p4 = p3 + (ee_pos - p3) * 0.33
                    p5 = p3 + (ee_pos - p3) * 0.66
                    p6 = ee_pos
                    pts.extend([p4, p5, p6])
                    
                colors_list = ['#34495e', '#3498db', '#9b59b6', '#e67e22', '#1abc9c', '#f1c40f']
                for i in range(len(pts) - 1):
                    draw_3d_cylinder(ax, pts[i], pts[i+1], radius=8, color=colors_list[i])
                    ax.scatter(pts[i][0], pts[i][1], pts[i][2], color='#e74c3c', s=50, zorder=5)
                
      
                ee_actual = pts[-1]
                wrist_actual = pts[-2]
                dir_v = ee_actual - wrist_actual
                if np.linalg.norm(dir_v) > 1e-3:
                    dir_v /= np.linalg.norm(dir_v)
                else:
                    dir_v = np.array([1, 0, 0])
                    
                ortho_v = np.array([-dir_v[1], dir_v[0], 0])
                if np.linalg.norm(ortho_v) < 1e-3: ortho_v = np.array([0, 1, 0])
                ortho_v /= np.linalg.norm(ortho_v)
                
                gripper_span = 18.0
                g_left_base = ee_actual + ortho_v * gripper_span
                g_right_base = ee_actual - ortho_v * gripper_span
                g_left_tip = g_left_base + dir_v * 15.0
                g_right_tip = g_right_base + dir_v * 15.0
                
                ax.plot([g_left_base[0], g_right_base[0]], [g_left_base[1], g_right_base[1]], [g_left_base[2], g_right_base[2]], color='#f1c40f', linewidth=3)
                ax.plot([g_left_base[0], g_left_tip[0]], [g_left_base[1], g_left_tip[1]], [g_left_base[2], g_left_tip[2]], color='#f1c40f', linewidth=3)
                ax.plot([g_right_base[0], g_right_tip[0]], [g_right_base[1], g_right_tip[1]], [g_right_base[2], g_right_tip[2]], color='#f1c40f', linewidth=3)
                ax.scatter(ee_actual[0], ee_actual[1], ee_actual[2], color='#f1c40f', s=70, zorder=10)
                
                ax.plot([ee_actual[0], ee_actual[0]], [ee_actual[1], ee_actual[1]], [0, ee_actual[2]], '--', color='#f1c40f', linewidth=1.2)
                ax.text(ee_actual[0], ee_actual[1], ee_actual[2] + 15, f"EE ({ee_actual[0]:.1f}, {ee_actual[1]:.1f}, {ee_actual[2]:.1f})", color='#f1c40f', fontweight='bold', fontsize=8)
                
              
                ee_coords["X"].config(text=f"{ee_actual[0]:.2f}")
                ee_coords["Y"].config(text=f"{ee_actual[1]:.2f}")
                ee_coords["Z"].config(text=f"{ee_actual[2]:.2f}")
            else:
                
                ee_coords["X"].config(text="0.00")
                ee_coords["Y"].config(text="0.00")
                ee_coords["Z"].config(text="0.00")

            
            ax.set_xlim([-max_range*0.4, max_range*1.2])
            ax.set_ylim([-max_range*0.7, max_range*0.7])
            ax.set_zlim([0, max_range*1.2])
            ax.set_xlabel('X (mm)', color='white', fontsize=8)
            ax.set_ylabel('Y (mm)', color='white', fontsize=8)
            ax.set_zlabel('Z (mm)', color='white', fontsize=8)
            ax.tick_params(axis='both', colors='white', labelsize=7)
            ax.view_init(elev=25, azim=35)
            canvas.draw()
            
            
            flat_labels = matrix_labels
            idx = 0
            for r in range(3):
                for c in range(4):
                    val = SAVED_T06[r, c]
                    comp = ["n", "o", "a", "p"][c]
                    axis = ["x", "y", "z"][r]
                    flat_labels[idx].config(text=f"{comp}{axis} = {val:.2f}", fg="#2ecc71")
                    idx += 1
                    
           
            dh_labels[0]["theta"].config(text=f"{float(joints[0].get()):.1f}")
            dh_labels[0]["d"].config(text=f"{d1_val:.1f}")
            dh_labels[0]["a"].config(text="0.0")
            
            dh_labels[1]["theta"].config(text=f"{float(joints[1].get()):.1f}")
            dh_labels[1]["d"].config(text="0.0")
            dh_labels[1]["a"].config(text=f"{a2_val:.1f}")
            
            dh_labels[2]["theta"].config(text=f"{float(joints[2].get()):.1f}")
            dh_labels[2]["d"].config(text="0.0")
            dh_labels[2]["a"].config(text=f"{a3_val:.1f}")
            
            for i in range(3, 6):
                dh_labels[i]["theta"].config(text=f"{float(joints[i].get()):.1f}")
                if i == 5:
                    dh_labels[i]["d"].config(text=f"{d6_val:.1f}")
                else:
                    dh_labels[i]["d"].config(text="0.0")
                dh_labels[i]["a"].config(text="0.0")
                
            on_link_select(None)
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def on_link_select(event):
        selected_idx = link_selector.current() + 1
        
        link_titles = {
            1: "Link 1: Base to Shoulder Joint",
            2: "Link 2: Shoulder to Elbow Joint",
            3: "Link 3: Elbow to Wrist Pitch Joint",
            4: "Link 4: Wrist Pitch to Wrist Roll",
            5: "Link 5: Wrist Roll to Gripper Base",
            6: "Link 6: Gripper / End-Effector"
        }
        
        link_descs = {
            1: "• Frame 0 (Base) is fixed at the center.\n• Frame 1 rotates around Z0 by θ1.\n• Translation along Z0 by d1.",
            2: "• Frame 2 is at the shoulder joint.\n• Rotates around Z1 (Pitch).\n• Translation along X1 by a2.",
            3: "• Frame 3 tracks the forearm.\n• Rotates around Z2.\n• Translation along X2 by a3.",
            4: "• Frame 4 controls wrist pitch.\n• Introduces a 90° twist angle (α4) around X4.",
            5: "• Frame 5 is the wrist roll.\n• Rotates orthogonally to spin the gripper.",
            6: "• Frame 6 (Tool Frame) at gripper tip.\n• Final transformation point for End-Effector."
        }
        
    
        step_title_lbl.config(text=link_titles[selected_idx])
        step_desc_lbl.config(text=link_descs[selected_idx])
        
    
        ax_edu.clear()
        ax_edu.set_facecolor('#0d2142')
        
     
        mat = SAVED_A_MATRICES[selected_idx - 1]
        origin = np.array([0, 0, 0])
        
        
        scale = 5.0
        x_axis = mat[0:3, 0] * scale
        y_axis = mat[0:3, 1] * scale
        z_axis = mat[0:3, 2] * scale
        
        
        ax_edu.scatter(0, 0, 0, color='#f1c40f', s=40, zorder=5)
        
        
        ax_edu.quiver(0, 0, 0, x_axis[0], x_axis[1], x_axis[2], color='#e74c3c', linewidth=2, arrow_length_ratio=0.3, label='X')
        ax_edu.quiver(0, 0, 0, y_axis[0], y_axis[1], y_axis[2], color='#2ecc71', linewidth=2, arrow_length_ratio=0.3, label='Y')
        ax_edu.quiver(0, 0, 0, z_axis[0], z_axis[1], z_axis[2], color='#3498db', linewidth=2, arrow_length_ratio=0.3, label='Z')
        
       
        ax_edu.text(x_axis[0]*1.2, x_axis[1]*1.2, x_axis[2]*1.2, f"X{selected_idx}", color='#e74c3c', fontweight='bold', fontsize=8)
        ax_edu.text(y_axis[0]*1.2, y_axis[1]*1.2, y_axis[2]*1.2, f"Y{selected_idx}", color='#2ecc71', fontweight='bold', fontsize=8)
        ax_edu.text(z_axis[0]*1.2, z_axis[1]*1.2, z_axis[2]*1.2, f"Z{selected_idx}", color='#3498db', fontweight='bold', fontsize=8)
        
        
        ax_edu.set_xlim([-7, 7])
        ax_edu.set_ylim([-7, 7])
        ax_edu.set_zlim([-7, 7])
        ax_edu.axis('off') 
        ax_edu.view_init(elev=20, azim=45)
        canvas_edu.draw()
        
        
        formatted_matrix = (
            f"[[ {mat[0,0]:>7.2f}  {mat[0,1]:>7.2f}  {mat[0,2]:>7.2f}  {mat[0,3]:>7.2f} ]\n"
            f" [ {mat[1,0]:>7.2f}  {mat[1,1]:>7.2f}  {mat[1,2]:>7.2f}  {mat[1,3]:>7.2f} ]\n"
            f" [ {mat[2,0]:>7.2f}  {mat[2,1]:>7.2f}  {mat[2,2]:>7.2f}  {mat[2,3]:>7.2f} ]\n"
            f" [ {mat[3,0]:>7.2f}  {mat[3,1]:>7.2f}  {mat[3,2]:>7.2f}  {mat[3,3]:>7.2f} ]]"
        )
        step_matrix_lbl.config(text=formatted_matrix)


    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)

    Button(header_frame, text="← Back to Video Intro", font=("Arial", 11, "bold"), 
           fg="#099da5", bg=BG_COLOR, bd=0, command=open_fk_intro_page, borderwidth=10).pack(side=LEFT, padx=20, pady=5)

    Label(header_frame, text="FORWARD KINEMATICS STEP BY STEP ANALYSIS", 
          font=("Helvetica", 15, "bold"), fg="#099da5", bg=BG_COLOR).pack(side=LEFT, expand=True)

    main_container = Frame(window, bg=BG_COLOR)
    main_container.pack(expand=True, fill=BOTH, padx=10, pady=2)
    
    # LEFT PANEL
    left_p = Frame(main_container, bg=BG_COLOR, bd=2)
    left_p.pack(side=LEFT, fill=Y, padx=10, pady=2)

    tabs = ttk.Notebook(left_p)
    tabs.pack(fill=X, pady=2)

    
    joints_tab = Frame(tabs, bg=BG_COLOR, padx=10, pady=2)
    tabs.add(joints_tab, text=" Joint Angles (θ) ")
    joints = []
    
    joint_names = ["Base (NEMA 23)", "Shoulder (Servo 35)", "Elbow (Servo 35)", "Rest (Servo 11/20)", "Roll (NEMA 17)", "Yaw (Servo 11)"]
    joint_ranges_text = ["[-135° to 135°]", "[0° to 180°]", "[-80° to 90°]", "[-90° to 90°]", "[-180° to 180°]", "[0° to 180°]"]
    
    for i in range(6):
        joint_card = Frame(joints_tab, bg=BG_COLOR, pady=1)
        joint_card.pack(fill=X)
        
        lbl_text = f"θ{i+1}: {joint_names[i]} {joint_ranges_text[i]}"
        Label(joint_card, text=lbl_text, fg="#70afc2", bg=BG_COLOR, font=("Arial", 8, "bold")).pack(anchor=W)
        
        e = Entry(joint_card, font=("Consolas", 10, "bold"), width=15, justify="center", bg="#0a1e4d", fg="#2ecc71", relief=FLAT)
        e.insert(0, "0.0")
        e.pack(pady=1)
        Frame(joint_card, height=1, bg="#099da5").pack(fill=X)
        joints.append(e)

   
    # Dims Tab (D w A)
    dims_tab = Frame(tabs, bg=BG_COLOR, padx=10, pady=4)
    tabs.add(dims_tab, text=" Dimensions (a/d) ")
    link_dims = []
    
    dim_configs = [
        ("Link 1 Length d1 (100-220 mm)", "160.0"),
        ("Link 2 Length a2 (100-200 mm)", "150.0"),
        ("Link 3 Length a3 (50-150 mm)", "100.0")
    ]
    
    for label_text, default_val in dim_configs:
        dim_card = Frame(dims_tab, bg=BG_COLOR, pady=2)
        dim_card.pack(fill=X)
        Label(dim_card, text=label_text, fg="#70afc2", bg=BG_COLOR, font=("Arial", 8, "bold")).pack(anchor=W)
        
        d_entry = Entry(dim_card, font=("Consolas", 10, "bold"), width=15, justify="center", bg="#1a2a5a", fg="#f1c40f", relief=FLAT)
        d_entry.insert(0, default_val)
        d_entry.pack(pady=1)
        Frame(dim_card, height=1, bg="#f1c40f").pack(fill=X)
        
        d_entry.bind("<KeyRelease>", lambda event: run_fk_calculations(from_button=False))
        
        link_dims.append(d_entry)


    edu_frame = LabelFrame(left_p, text="  Live Frame Description (DH Axes) ", font=("Arial", 9, "bold"), fg="#f1c40f", bg="#0d2142", bd=2)
    edu_frame.pack(fill=BOTH, expand=True, pady=4)

    step_title_lbl = Label(edu_frame, text="Link 1: Base to Shoulder Joint", font=("Arial", 9, "bold"), fg="#2ecc71", bg="#0d2142")
    step_title_lbl.pack(anchor=W, padx=5, pady=2)
    
    step_desc_lbl = Label(edu_frame, text="", font=("Arial", 8), fg="#9db2bf", bg="#0d2142", justify=LEFT, wraplength=180)
    step_desc_lbl.pack(anchor=W, padx=5, pady=2)


    fig_edu = plt.figure(figsize=(2, 2))
    fig_edu.patch.set_facecolor('#0d2142')
    ax_edu = fig_edu.add_subplot(111, projection='3d')
    
    canvas_edu = FigureCanvasTkAgg(fig_edu, master=edu_frame)
    canvas_edu.get_tk_widget().pack(fill=BOTH, expand=True, padx=5, pady=2)

    Button(left_p, text="RUN SIMULATION", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), command=lambda: run_fk_calculations(from_button=True)).pack(pady=8, fill=X)


    middle_p = Frame(main_container, bg="#081b4b", bd=2, relief=SUNKEN)
    middle_p.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)
    
    fig = plt.figure(figsize=(5, 5))
    fig.patch.set_facecolor('#081b4b')
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=middle_p)
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)


    right_p = Frame(main_container, bg=BG_COLOR)
    right_p.pack(side=RIGHT, fill=Y, padx=5, pady=2)

    matrix_select_frame = LabelFrame(right_p, text="Link Transformation Matrix (A_i) ", 
                                     font=("Arial", 9, "bold"), fg="#099da5", bg=BG_COLOR)
    matrix_select_frame.pack(fill=X, pady=(50, 2)) 
    
    link_selector = ttk.Combobox(matrix_select_frame, values=["Link 1 (Base Joint)", "Link 2 (Shoulder Joint)", "Link 3 (Elbow Joint)", "Link 4 (Wrist Pitch)", "Link 5 (Wrist Roll)", "Link 6 (End-Effector)"], state="readonly", width=28)
    link_selector.current(0)
    link_selector.pack(pady=2, padx=10)
    link_selector.bind("<<ComboboxSelected>>", on_link_select)

    
    step_matrix_lbl = Label(matrix_select_frame, text="", font=("Consolas", 9), fg="white", bg="#050c1f", padx=10, pady=4, justify=LEFT, width=38)
    step_matrix_lbl.pack(fill=X, padx=10, pady=2)

    chain_lbl = Label(matrix_select_frame, text="Total Chain: T06 = A1 × A2 × A3 × A4 × A5 × A6", font=("Arial", 8, "italic", "bold"), fg="#efefef", bg="#1a2a5a", pady=2)
    chain_lbl.pack(fill=X, padx=5, pady=1)

    tm_frame = LabelFrame(right_p, text=" Final Transformation Matrix (T06) ", font=("Arial", 9, "bold"), fg="white", bg=BG_COLOR)
    tm_frame.pack(fill=X, pady=2)
    for i in range(4): tm_frame.grid_columnconfigure(i, weight=1, uniform="matrix")

    matrix_labels = []
    rows_names, cols_names = ["x", "y", "z"], ["n", "o", "a", "p"] 
    for r_idx, axis in enumerate(rows_names):
        for c_idx, component in enumerate(cols_names):
         
            lbl = Label(tm_frame, text=f"{component}{axis} =  0.00", font=("Consolas", 8), fg="#70afc2", bg=BG_COLOR, width=12, anchor=W)
            lbl.grid(row=r_idx, column=c_idx, padx=1, pady=1)
            matrix_labels.append(lbl)
    for i, val in enumerate(["0.00", "0.00", "0.00", "1.00"]):
        Label(tm_frame, text=val, font=("Consolas", 8), fg="white", bg=BG_COLOR, width=12).grid(row=3, column=i, pady=2)


    dh_frame = LabelFrame(right_p, text=" Denavit-Hartenberg Parameters ", font=("Arial", 9, "bold"), fg="white", bg=BG_COLOR, bd=2)
    dh_frame.pack(fill=X, pady=2)
    headers = ["Link", "θ*", "d", "a", "α"]
    for i, h in enumerate(headers): 
        Label(dh_frame, text=h, fg="#099da5", bg=BG_COLOR, font=("Arial", 8, "bold")).grid(row=0, column=i, padx=6)
    
    dh_labels = [] 
    my_robot_alphas = [90, 0, 0, 90, -90, 0]
    for i in range(6):
        Label(dh_frame, text=str(i+1), fg="white", bg=BG_COLOR, font=("Arial", 8)).grid(row=i+1, column=0, padx=6)
        
        t_lbl = Label(dh_frame, text="0.0", fg="#099da5", bg=BG_COLOR, font=("Arial", 8, "bold"))
        t_lbl.grid(row=i+1, column=1, padx=6)
        
        d_lbl = Label(dh_frame, text="0.0", fg="white", bg=BG_COLOR, font=("Arial", 8))
        d_lbl.grid(row=i+1, column=2, padx=6)
        
        a_lbl = Label(dh_frame, text="0.0", fg="white", bg=BG_COLOR, font=("Arial", 8))
        a_lbl.grid(row=i+1, column=3, padx=6)
        
        Label(dh_frame, text=str(my_robot_alphas[i]), fg="white", bg=BG_COLOR, font=("Arial", 8)).grid(row=i+1, column=4, padx=6)
        
        dh_labels.append({"theta": t_lbl, "d": d_lbl, "a": a_lbl})

    ee_frame = LabelFrame(right_p, text=" End-Effector 3-Axes Projection ", font=("Arial", 9, "bold"), fg="#27ae60", bg=BG_COLOR, bd=2)
    ee_frame.pack(fill=X, pady=4)
    for i in range(3): ee_frame.grid_columnconfigure(i, weight=1)

    ee_coords = {}
    axes_cfg = [("X", "#e74c3c"), ("Y", "#2ecc71"), ("Z", "#3498db")]
    for i, (axis, color) in enumerate(axes_cfg):
        container = Frame(ee_frame, bg=BG_COLOR)
        container.grid(row=0, column=i, pady=6, padx=2)
        Label(container, text=f"{axis}:", font=("Arial", 10, "bold"), fg=color, bg=BG_COLOR).pack(side=LEFT)
        val_lbl = Label(container, text="0.00", font=("Consolas", 11, "bold"), fg="white", bg="#0a1e4d", width=8, relief=RIDGE)
        val_lbl.pack(side=LEFT, padx=2)
        ee_coords[axis] = val_lbl

    sync_frame = Frame(right_p, bg="#0a1e4d", bd=1, relief=SOLID)
    sync_frame.pack(side=BOTTOM, fill=X, pady=4)
    Button(sync_frame, text="UPLOAD TO HARDWARE", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=lambda: messagebox.showinfo("Hardware Sync", "Uploading to ESP32")).pack(pady=4, padx=10, fill=X)
    

    run_fk_calculations(from_button=False)
    show_university_logo()

  
    
#page fiha kol experiments hna
def open_experiments_page():
    for widget in window.winfo_children(): widget.destroy()
    
    # Zorrar el-Back
    Button(window, text=" ← Back to Main Menu", font=("Arial", 12, "bold"), 
           fg="#099da5", bg=BG_COLOR, bd=0, command=show_welcome_page, borderwidth=10).pack(anchor=NW, padx=20, pady=10)
    
    Label(window, text="SELECT EXPERIMENT", font=("Helvetica", 30, "bold"), 
          fg="#099da5", bg=BG_COLOR).pack(pady=30) 

    Experiments = [
        ("1. Forward Kinematics (FK)", open_fk_intro_page), 
        ("2. Inverse Kinematics (IK)", open_ik_intro_page), 
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
    show_university_logo()    
    
# file excel     
file_path = "lab_records.csv"

if not os.path.exists(file_path):
    with open(file_path, mode='w', newline='') as f:
        csv.writer(f).writerow(["Timestamp", "Student Name", "Student ID", "Experiment Type", "Result Data"])

CURRENT_USER = ""
CURRENT_ID = ""

def save_lab_result(exp_name, data_values):
    global CURRENT_USER, CURRENT_ID
    with open("lab_records.csv", mode='a', newline='') as f:
        csv.writer(f).writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            CURRENT_USER, 
            CURRENT_ID, 
            exp_name, 
            data_values
        ])


#  Login Page 
def show_login_page():
    for widget in window.winfo_children(): 
        widget.destroy()
    
    login_frame = Frame(window, bg=BG_COLOR)
    login_frame.pack(expand=True, fill=BOTH)

    Label(login_frame, text="6-DOF ROBOTIC ARM EDUCATIONAL KIT", 
          font=("Helvetica", 24, "bold"), fg="#099da5", bg=BG_COLOR).place(relx=0.5, rely=0.05, anchor=CENTER)
    Label(login_frame, text="VIRTUAL LAB INTERFACE v1.0 - LOGIN", font=("Consolas", 10, "bold"), 
          fg="#efefef", bg=BG_COLOR).place(relx=0.5, rely=0.08, anchor=CENTER)

    card = Frame(login_frame, bg="#0d2142", highlightbackground="#099da5", highlightthickness=2, padx=50, pady=50)
    card.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(card, text="STUDENT IDENTIFICATION", font=("Helvetica", 18, "bold"), fg="#099da5", bg="#0d2142").pack(pady=(0, 20))


    #(Limitations)
  
    def validate_name(text_inserted):
       
        if len(text_inserted) > 40:
            return False
            
        
        for char in text_inserted:
            if not (char.isalpha() or char.isspace()):
                return False  
        return True

    
    vcmd = (window.register(validate_name), '%P')

    Label(card, text="Full Name :", font=("Arial", 10), fg="#efefef", bg="#0d2142").pack(anchor=W)
    
   
    name_entry = Entry(card, font=("Arial", 14), bg="#050c1f", fg="white", insertbackground="white", bd=0,
                       validate="key", validatecommand=vcmd)
    name_entry.pack(fill=X, pady=(5, 15))
    Frame(card, height=1, bg="#099da5").pack(fill=X)

    Label(card, text="Student ID:", font=("Arial", 10), fg="#efefef", bg="#0d2142").pack(anchor=W)
    id_entry = Entry(card, font=("Arial", 14), bg="#050c1f", fg="white", insertbackground="white", bd=0)
    id_entry.pack(fill=X, pady=(5, 15))
    Frame(card, height=1, bg="#099da5").pack(fill=X)

    def final_step():
        global CURRENT_USER, CURRENT_ID
        name = name_entry.get().strip() 
        uid = id_entry.get().strip()
        
      
        if name and uid:
            CURRENT_USER = name
            CURRENT_ID = uid
            
            save_lab_result("Login System", "Student Verified & Entered Lab")

            try:
                open_experiments_page() 
            except NameError:
                print("Error: Function 'open_experiments_page' not found!")
        else:
            err = Label(card, text="Please fill all fields correctly", fg="#f36412", bg="#0d2142")
            err.pack(pady=5)
            window.after(2000, err.destroy)

    Button(card, text="VERIFY & ENTER LAB →", bg="#099da5", fg="white", 
           font=("Arial", 12, "bold"), padx=30, pady=10, bd=0, command=final_step).pack(pady=25)
    
    show_university_logo()

# logo
def show_university_logo():
  
    try:
        logo_path = r"C:\Users\Bassant\robot-arm-educational-kit\GUI\uni_logo.png"
        logo_img = Image.open(logo_path).resize((80, 70), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        
     
        l_lbl = Label(window, image=logo_photo, bg=BG_COLOR)
        l_lbl.image = logo_photo  
        l_lbl.place(relx=0.92, rely=0.07, anchor=CENTER)
    except Exception as e:
        print(f"Logo error: {e}")
        pass

#main page
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

        def animate_robot(angle=0):
            try:
                if 'robot_lbl' in globals() and robot_lbl.winfo_exists():
                    off_y = math.sin(angle) * 10 
                    robot_lbl.place(relx=0.5, rely=0.5, y=off_y, anchor="center")
                    window.after(20, lambda: animate_robot(angle + 0.1))
            except:
                pass
# w2fa hna zbtiha fe venu bt3tk v14
        animate_robot()
        
    except Exception as e:
        print(f"Error in animation or image: {e}")

    
    show_university_logo()


show_welcome_page()       
window.mainloop()