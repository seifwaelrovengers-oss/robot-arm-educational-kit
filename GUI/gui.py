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
import time
from collections import deque
import threading
from tkinter import Frame, Label, Button, Entry, X, Y, BOTH, LEFT, RIGHT
import serial
import json

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
        
        
        
def open_dynamics_intro_page():

    for widget in window.winfo_children():
        widget.destroy()

    base_path = os.path.dirname(os.path.abspath(__file__))
    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)

    Button(
        header_frame,
        text="← Back to Experiments",
        font=("Arial", 12, "bold"),
        fg="#099da5",
        bg=BG_COLOR,
        bd=0,
        borderwidth=10,
        command=open_experiments_page
    ).pack(side=LEFT, padx=20, pady=10)

    Label(
        header_frame,
        text="Torques & Dynamics Analysis",
        font=("Helvetica", 22, "bold"),
        fg="white",
        bg=BG_COLOR,
        anchor=W
    ).pack(pady=20)


    def play_dyn_video():

        video_name = "torque.mp4"
        video_full_path = os.path.join(base_path, video_name)

        if os.path.exists(video_full_path):
            os.startfile(video_full_path)
        else:
            messagebox.showerror(
                "Error",
                f"Video not found at: {video_full_path}"
            )

    video_frame = Frame(window, bg="#0a1e4d", bd=3, relief=RIDGE)
    video_frame.pack(pady=10, padx=50, fill=BOTH, expand=True)

    Label(
        video_frame,
        text="WATCH DYNAMICS & TORQUE TUTORIAL",
        font=("Arial", 18, "bold"),
        fg="#f1c40f",
        bg="#0a1e4d"
    ).pack(pady=(20, 10))

    preview_container = Frame(video_frame, bg="#0a1e4d")
    preview_container.pack(expand=True)


    dyn_image_path = os.path.join(base_path, "Torque_video_preview.png")

    try:
        img = Image.open(dyn_image_path)
        img = img.resize((750, 420), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        img_label = Label(
            preview_container,
            image=photo,
            bg="#0a1e4d",
            cursor="hand2"
        )
        img_label.image = photo
        img_label.pack(pady=10)

        img_label.bind("<Button-1>", lambda e: play_dyn_video())

        Label(
            preview_container,
            text="Click image to play Dynamics tutorial",
            font=("Arial", 10, "italic"),
            fg="white",
            bg="#0a1e4d"
        ).pack()

    except Exception as e:
        print(f"DEBUG: Dynamics Image not found. Error: {e}")

        Button(
            preview_container,
            text="▶ Watch Dynamics Tutorial",
            font=("Arial", 16, "bold"),
            bg="#f1c40f",
            fg="black",
            padx=30,
            pady=15,
            command=play_dyn_video,
            cursor="hand2"
        ).pack(pady=50)


    btn_container = Frame(window, bg=BG_COLOR)
    btn_container.pack(side=BOTTOM, fill=X, pady=40, padx=80)

    Button(
        btn_container,
        text="Simulation & Torque Analysis →",
        font=("Arial", 13, "bold"),
        bg="#e67e22",
        fg="white",
        width=25,
        height=2,
        command=open_dynamics_page
    ).pack(side=RIGHT)

    Button(
        btn_container,
        text=" ← 3D Robot Simulation",
        font=("Arial", 13, "bold"),
        bg="#2980b9",
        fg="white",
        width=25,
        height=2,
        command=run_pybullet_sim
    ).pack(side=LEFT)
    show_university_logo()



# lsa m7tagh a3dlha kolha 3la rules eldr
def open_dynamics_page():
    for widget in window.winfo_children():
        widget.destroy()

   
    BG = "#0b1a3a"
    PANEL = "#102a5c"
    ACCENT = "#00d2ff"
    GREEN = "#2ecc71"
    RED = "#e74c3c"

    sim = {"run": True}

  
    header = tk.Frame(window, bg=BG)
    header.pack(fill=tk.X)

    tk.Button(header,
              text="← Back to Experiments",
              fg="#099da5",
              bg=BG,
              bd=0,
              font=("Arial", 12, "bold"),
              command=open_experiments_page).pack(side=tk.LEFT, padx=15, pady=10)

    tk.Button(header,
              text="← Kinematics",
              fg=ACCENT,
              bg=BG,
              bd=0,
              font=("Arial", 12, "bold"),
              command=open_trajectory_page).pack(side=tk.LEFT)

    tk.Label(header,
             text="6DOF DYNAMICS | LAGRANGE + JACOBIAN",
             bg=BG,
             fg=ACCENT,
             font=("Arial", 18, "bold")).pack(side=tk.LEFT, padx=25)

  
    main = tk.Frame(window, bg=BG)
    main.pack(fill=tk.BOTH, expand=True)

    left = tk.Frame(main, bg=BG, width=300)
    left.pack(side=tk.LEFT, fill=tk.Y)

    center = tk.Frame(main, bg=PANEL)
    center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right = tk.Frame(main, bg=BG, width=350)
    right.pack(side=tk.RIGHT, fill=tk.Y)

    
    def make_input(label, default):
        tk.Label(left, text=label, fg="white", bg=BG).pack(anchor="w")
        e = tk.Entry(left, bg=PANEL, fg=ACCENT, insertbackground="white")
        e.insert(0, str(default))
        e.pack(fill=tk.X, pady=3)
        return e

    tk.Label(left, text="SYSTEM INPUTS",
             fg=ACCENT, bg=BG,
             font=("Arial", 12, "bold")).pack(pady=10)

    mass = make_input("Mass (kg)", 2)

    theta = [make_input(f"θ{i+1} (deg)", 20*(i+1)) for i in range(6)]
    links = [make_input(f"Link L{i+1} (cm)", 10+i*2) for i in range(6)]

   
    status = tk.Label(right, text="READY", fg=GREEN, bg=BG,
                      font=("Arial", 12, "bold"))
    status.pack(pady=10)

    torque_labels = []
    for i in range(6):
        lb = tk.Label(right, text=f"τ{i+1} = 0",
                      fg="white", bg=BG)
        lb.pack()
        torque_labels.append(lb)

    lagrange_lbl = tk.Label(right,
                            text="Lagrange: ---",
                            fg="white", bg=BG,
                            justify="left",
                            font=("Consolas", 9))
    lagrange_lbl.pack(pady=10)

    jacobian_lbl = tk.Label(right,
                            text="Jacobian: ---",
                            fg="white", bg=BG,
                            font=("Consolas", 8))
    jacobian_lbl.pack()


    fig, ax = plt.subplots()
    fig.patch.set_facecolor(PANEL)
    ax.set_facecolor(PANEL)

    canvas = FigureCanvasTkAgg(fig, master=center)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    t_data = []
    tau = [[] for _ in range(6)]

  
    def torque_model(m, th, L, t):

        g = 9.81
        out = []

        for i in range(6):
            θ = np.radians(float(th[i]) + t*(i+1)*0.3)
            Li = float(L[i]) / 100

            τ = m * g * Li * np.cos(θ)
            out.append(τ)

        return out

    
    def lagrange(m, th, L):

        g = 9.81
        T = 0
        V = 0

        for i in range(6):
            Li = float(L[i]) / 100
            wi = np.radians(float(th[i]))

            v = Li * wi
            T += 0.5 * m * v**2
            V += m * g * Li * np.sin(wi)

        return T, V, T - V

   
    def jacobian(th, L):

        J = np.zeros((6,6))

        for i in range(6):
            for j in range(6):

                Li = float(L[j]) / 100
                θ = np.radians(float(th[j]))

                if j <= i:
                    J[i][j] = Li * np.cos(θ)
                else:
                    J[i][j] = 0

        return J

   
    def run():

        m = float(mass.get())

        th = [float(x.get()) for x in theta]
        L = [float(x.get()) for x in links]

        for i in range(80):

            if not sim["run"]:
                break

            t = i * 0.1

            τ = torque_model(m, th, L, t)
            T, V, Lg = lagrange(m, th, L)
            J = jacobian(th, L)

            t_data.append(t)

            for j in range(6):
                tau[j].append(τ[j])

           
            ax.clear()

            for j in range(6):
                ax.plot(t_data, tau[j], label=f"τ{j+1}")

            ax.set_title("6DOF Torque vs Time", color="white")
            ax.legend()

            canvas.draw()

          
            for j in range(6):
                torque_labels[j].config(text=f"τ{j+1} = {τ[j]:.2f}")

            lagrange_lbl.config(
                text=f"T = {T:.2f}\nV = {V:.2f}\nL = {Lg:.2f}"
            )

            jacobian_lbl.config(text=str(np.round(J, 2)))

            if max(abs(x) for x in τ) > 80:
                status.config(text="OVERLOAD", fg=RED)
            else:
                status.config(text="SAFE", fg=GREEN)

            window.update()
            window.after(50)

  
    tk.Button(left, text="▶ START",
              bg=GREEN, fg="white",
              command=run).pack(fill=tk.X, pady=5)

    tk.Button(left, text="⛔ STOP",
              bg=RED, fg="white",
              command=lambda: sim.update({"run": False})
              ).pack(fill=tk.X, pady=5)

    tk.Button(left, text="🔄 RESET",
              bg="gray", fg="white",
              command=lambda: (
                  t_data.clear(),
                  [x.clear() for x in tau],
                  ax.clear(),
                  canvas.draw()
              )
              ).pack(fill=tk.X, pady=5)

    canvas.draw()
    show_university_logo()





def open_trajectory_intro_page():
    for widget in window.winfo_children(): 
        widget.destroy()

    base_path = os.path.dirname(os.path.abspath(__file__))
    
  
    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)
    
    Button(header_frame, text="← Back to Experiments", font=("Arial", 12, "bold"), 
           fg="#099da5", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(side=LEFT, padx=20, pady=10)
    
    Label(header_frame, text="Trajectory & Pick-and-Place", font=("Helvetica", 22, "bold"), 
          fg="white", bg=BG_COLOR, anchor=W).pack(pady=20)
    
    
    def play_traj_video():
        video_name = "trajectory_mp4_video.mp4" 
        video_full_path = os.path.join(base_path, video_name)
        if os.path.exists(video_full_path): 
            os.startfile(video_full_path)
        else:
            messagebox.showerror("Error", f"Video not found at: {video_full_path}")

    
    video_frame = Frame(window, bg="#0a1e4d", bd=3, relief=RIDGE)
    video_frame.pack(pady=10, padx=50, fill=BOTH, expand=True)
    
    Label(video_frame, text="WATCHING TUTORIAL", font=("Arial", 18, "bold"), 
          fg="#2ecc71", bg="#0a1e4d").pack(pady=(20, 10))

    preview_container = Frame(video_frame, bg="#0a1e4d")
    preview_container.pack(expand=True)

   
    traj_image_path = os.path.join(base_path, "Trajectory_video_preview.png") 
    
    try:
        img = Image.open(traj_image_path) 
        img = img.resize((750, 420), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        img_label = Label(preview_container, image=photo, bg="#0a1e4d", cursor="hand2")
        img_label.image = photo
        img_label.pack(pady=10)
        
        img_label.bind("<Button-1>", lambda e: play_traj_video())
        Label(preview_container, text="Click image to play Trajectory Planning tutorial", 
              font=("Arial", 10, "italic"), fg="white", bg="#0a1e4d").pack()

    except Exception as e:
        print(f"DEBUG: Trajectory Image not found. Error: {e}")
        Button(preview_container, text="▶ Watch Trajectory Tutorial", font=("Arial", 16, "bold"),
                bg="#2ecc71", fg="white", padx=30, pady=15,
                command=play_traj_video, cursor="hand2").pack(pady=50)

    
    btn_container = Frame(window, bg=BG_COLOR)
    btn_container.pack(side=BOTTOM, fill=X, pady=40, padx=80)
    
    Button(btn_container, text="Simulation & Calculations →", font=("Arial", 13, "bold"), 
           bg="#f36412", fg="white", width=25, height=2, command=open_trajectory_page).pack(side=RIGHT)

    Button(btn_container, text=" ← 3D Visualization (PyBullet)", font=("Arial", 13, "bold"), 
           bg="#2980b9", fg="white", width=25, height=2, command=run_pybullet_sim).pack(side=LEFT)
    show_university_logo()
    
    
  
  
    
    


def open_trajectory_intro_page():
    for widget in window.winfo_children(): 
        widget.destroy()

    base_path = os.path.dirname(os.path.abspath(__file__))
    
  
    header_frame = Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=X)
    
    Button(header_frame, text="← Back to Experiments", font=("Arial", 12, "bold"), 
           fg="#099da5", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(side=LEFT, padx=20, pady=10)
    
    Label(header_frame, text="Trajectory & Pick-and-Place", font=("Helvetica", 22, "bold"), 
          fg="white", bg=BG_COLOR, anchor=W).pack(pady=20)
    
    
    def play_traj_video():
        video_name = "trajectory_mp4_video.mp4" 
        video_full_path = os.path.join(base_path, video_name)
        if os.path.exists(video_full_path): 
            os.startfile(video_full_path)
        else:
            messagebox.showerror("Error", f"Video not found at: {video_full_path}")

    
    video_frame = Frame(window, bg="#0a1e4d", bd=3, relief=RIDGE)
    video_frame.pack(pady=10, padx=50, fill=BOTH, expand=True)
    
    Label(video_frame, text="WATCHING TUTORIAL", font=("Arial", 18, "bold"), 
          fg="#2ecc71", bg="#0a1e4d").pack(pady=(20, 10))

    preview_container = Frame(video_frame, bg="#0a1e4d")
    preview_container.pack(expand=True)

   
    traj_image_path = os.path.join(base_path, "Trajectory_video_preview.png") 
    
    try:
        img = Image.open(traj_image_path) 
        img = img.resize((750, 420), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        img_label = Label(preview_container, image=photo, bg="#0a1e4d", cursor="hand2")
        img_label.image = photo
        img_label.pack(pady=10)
        
        img_label.bind("<Button-1>", lambda e: play_traj_video())
        Label(preview_container, text="Click image to play Trajectory Planning tutorial", 
              font=("Arial", 10, "italic"), fg="white", bg="#0a1e4d").pack()

    except Exception as e:
        print(f"DEBUG: Trajectory Image not found. Error: {e}")
        Button(preview_container, text="▶ Watch Trajectory Tutorial", font=("Arial", 16, "bold"),
                bg="#2ecc71", fg="white", padx=30, pady=15,
                command=play_traj_video, cursor="hand2").pack(pady=50)

    
    btn_container = Frame(window, bg=BG_COLOR)
    btn_container.pack(side=BOTTOM, fill=X, pady=40, padx=80)
    
    Button(btn_container, text="Simulation & Calculations →", font=("Arial", 13, "bold"), 
           bg="#f36412", fg="white", width=25, height=2, command=open_trajectory_page).pack(side=RIGHT)

    Button(btn_container, text=" ← 3D Visualization (PyBullet)", font=("Arial", 13, "bold"), 
           bg="#2980b9", fg="white", width=25, height=2, command=run_pybullet_sim).pack(side=LEFT)
    show_university_logo()
    
    
  
    


def open_trajectory_page():

    for widget in window.winfo_children():
        widget.destroy()

    BG = "#04153B"
    PANEL = "#081b4b"
    EXPERIMENT_TYPE = StringVar(value="Pick and Place")

   

    header = Frame(window, bg=BG)
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
        command=open_trajectory_intro_page
    ).pack(side=LEFT, padx=20, pady=5)

    Label(
        header,
        text="ADVANCED ROBOTICS TRAJECTORY LAB",
        bg=BG,
        fg="#00d2ff",
        font=("Helvetica",18,"bold")
    ).pack(side=LEFT,padx=25)



    main = Frame(window,bg=BG)
    main.pack(fill=BOTH,expand=True)

    left = Frame(main,bg=BG,width=280)
    left.pack(side=LEFT,fill=Y,padx=10,pady=10)


    selection_frame = LabelFrame(
        left,
        text=" EXPERIMENT TYPE ",
        bg=BG,
        fg="#ffcc00",
        font=("Arial",10,"bold")
    )
    selection_frame.pack(fill=X,pady=5)

    experiments = [
        "Pick and Place",
        "Trajectory Planning",
        "Circular Path",
        "Point to Point"
    ]

    combo = ttk.Combobox(
        selection_frame,
        values=experiments,
        textvariable=EXPERIMENT_TYPE,
        state="readonly",
        font=("Arial",10)
    )

    combo.pack(fill=X,padx=5,pady=10)
    
    def sync_to_hardware():
        print("Sending angles to hardware...")
      
    sync_btn = Button(
        selection_frame,
        text="SYNC TO HARDWARE",
        bg="#00ff77",
        fg="black",
        font=("Arial", 10, "bold"),
        command=sync_to_hardware
    )

    sync_btn.pack(fill=X, padx=5, pady=5)

   
    dynamic_left_frame = Frame(left,bg=BG)
    dynamic_left_frame.pack(fill=BOTH,expand=True)

    center = Frame(main,bg=PANEL)
    center.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)

    fig = plt.figure(figsize=(7,7))
    fig.patch.set_facecolor(PANEL)

    ax = fig.add_subplot(111,projection='3d')

    canvas = FigureCanvasTkAgg(fig,master=center)
    canvas.get_tk_widget().pack(fill=BOTH,expand=True)


    right = Frame(main,bg=BG,width=340)
    right.pack(side=RIGHT,fill=Y,padx=10,pady=10)

    dynamic_right_frame = Frame(right,bg=BG)
    dynamic_right_frame.pack(fill=BOTH,expand=True)


    status_frame=LabelFrame(
        right,
        text=" STATUS ",
        bg=BG,
        fg="#ff4d4d",
        font=("Arial",10,"bold")
    )
    status_frame.pack(fill=X,pady=5)

    status_lbl=Label(
        status_frame,
        text="READY",
        bg="#081b4b",
        fg="#2ecc71",
        font=("Arial",11,"bold"),
        pady=10
    )
    status_lbl.pack(fill=X)


    matrix_frame=LabelFrame(
        right,
        text=" T06 MATRIX ",
        bg=BG,
        fg="#00d2ff",
        font=("Arial",10,"bold")
    )
    matrix_frame.pack(fill=BOTH,expand=True,pady=5)

    matrix_lbl=Label(
        matrix_frame,
        text="NO MATRIX",
        bg="#050c1f",
        fg="#2ecc71",
        justify=LEFT,
        font=("Consolas",8),
        padx=10,
        pady=10
    )
    matrix_lbl.pack(fill=BOTH,expand=True)

  

    jacobian_frame=LabelFrame(
        right,
        text=" JACOBIAN MATRIX ",
        bg=BG,
        fg="#f39c12",
        font=("Arial",10,"bold")
    )
    jacobian_frame.pack(fill=BOTH,expand=True,pady=5)

    jacobian_lbl=Label(
        jacobian_frame,
        text="NO JACOBIAN",
        bg="#050c1f",
        fg="#2ecc71",
        justify=LEFT,
        font=("Consolas",8),
        padx=10,
        pady=10
    )
    jacobian_lbl.pack(fill=BOTH,expand=True)


    euler_frame=LabelFrame(
        right,
        text=" EULER ANGLES ",
        bg=BG,
        fg="#9b59b6",
        font=("Arial",10,"bold")
    )
    euler_frame.pack(fill=X,pady=5)

    euler_lbl=Label(
        euler_frame,
        text="ROLL = 0\nPITCH = 0\nYAW = 0",
        bg="#081b4b",
        fg="white",
        justify=LEFT,
        font=("Consolas",9),
        padx=10,
        pady=10
    )
    euler_lbl.pack(fill=X)



    motion_frame=LabelFrame(
        right,
        text=" MOTION ANALYSIS ",
        bg=BG,
        fg="#2ecc71",
        font=("Arial",10,"bold")
    )
    motion_frame.pack(fill=X,pady=5)

    motion_lbl=Label(
        motion_frame,
        text="Velocity = 0\nAcceleration = 0",
        bg="#081b4b",
        fg="white",
        justify=LEFT,
        font=("Consolas",9),
        padx=10,
        pady=10
    )
    motion_lbl.pack(fill=X)


    analysis_frame=LabelFrame(
        right,
        text=" ANALYSIS ",
        bg=BG,
        fg="#1abc9c",
        font=("Arial",10,"bold")
    )
    analysis_frame.pack(fill=X,pady=5)

    analysis_lbl=Label(
        analysis_frame,
        text="WAITING...",
        bg="#061743",
        fg="white",
        justify=LEFT,
        font=("Consolas",9),
        padx=10,
        pady=10
    )
    analysis_lbl.pack(fill=X)
    

    def draw_workspace(d1,a2,a3):

        reach=a2+a3+190

        u=np.linspace(0,2*np.pi,30)
        v=np.linspace(0,np.pi/2,20)

        x=reach*np.outer(np.cos(u),np.sin(v))
        y=reach*np.outer(np.sin(u),np.sin(v))
        z=reach*np.outer(np.ones(np.size(u)),np.cos(v))

        z+=d1

        ax.plot_wireframe(
            x,y,z,
            color="#00ffff",
            alpha=0.05
        )

   

    def draw_cylinder(p1,p2,radius=7,color='#3498db'):

        v=p2-p1
        mag=np.linalg.norm(v)

        if mag<1e-5:
            return

        v=v/mag

        not_v=np.array([1,0,0])

        if abs(v[0])>0.9:
            not_v=np.array([0,1,0])

        n1=np.cross(v,not_v)
        n1/=np.linalg.norm(n1)

        n2=np.cross(v,n1)

        t=np.linspace(0,2*np.pi,20)

        X=[]
        Y=[]
        Z=[]

        for s in [0,1]:

            circle=p1+(p2-p1)*s

            x=circle[0]+radius*np.cos(t)*n1[0]+radius*np.sin(t)*n2[0]
            y=circle[1]+radius*np.cos(t)*n1[1]+radius*np.sin(t)*n2[1]
            z=circle[2]+radius*np.cos(t)*n1[2]+radius*np.sin(t)*n2[2]

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

   

    def draw_gripper(p3,theta1,theta2,theta3,open_amount=15):

        alpha=theta2+theta3

        forward=np.array([
            np.cos(alpha)*np.cos(theta1),
            np.cos(alpha)*np.sin(theta1),
            np.sin(alpha)
        ])

        side=np.array([
            -np.sin(theta1),
            np.cos(theta1),
            0
        ])

        length=30

        s1=p3+side*open_amount
        e1=s1+forward*length

        s2=p3-side*open_amount
        e2=s2+forward*length

        ax.plot3D(
            [s1[0],e1[0]],
            [s1[1],e1[1]],
            [s1[2],e1[2]],
            color='yellow',
            linewidth=4
        )

        ax.plot3D(
            [s2[0],e2[0]],
            [s2[1],e2[1]],
            [s2[2],e2[2]],
            color='yellow',
            linewidth=4
        )

    

    def IK(x, y, z,
       roll, pitch, yaw,
       d1,
       a2, a3,
       d4, d5, d6):

      
        cr, sr = np.cos(roll), np.sin(roll)
        cp, sp = np.cos(pitch), np.sin(pitch)
        cy, sy = np.cos(yaw), np.sin(yaw)

        R06 = np.array([
            [cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
            [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
            [-sp,   cp*sr,            cp*cr]
        ])


        tool_offset =  d6
        wc = np.array([x, y, z]) - tool_offset * R06[:, 2]

        wc_x, wc_y, wc_z = wc

      
        theta1 = np.arctan2(wc_y, wc_x)

       
        r = np.sqrt(wc_x**2 + wc_y**2)
        s = wc_z - d1

        D = (r**2 + s**2 - a2**2 - a3**2) / (2 * a2 * a3)

        if abs(D) > 1:
            return None

        theta3 = np.arctan2(np.sqrt(1 - D**2), D)

        theta2 = np.arctan2(s, r) - np.arctan2(
            a3 * np.sin(theta3),
            a2 + a3 * np.cos(theta3)
        )

       
        def DH(theta, d, a, alpha):
            return np.array([
                [np.cos(theta), -np.sin(theta)*np.cos(alpha),
                np.sin(theta)*np.sin(alpha), a*np.cos(theta)],

                [np.sin(theta), np.cos(theta)*np.cos(alpha),
                -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],

                [0, np.sin(alpha), np.cos(alpha), d],
                [0, 0, 0, 1]
            ])

        T01 = DH(theta1, d1, 0, np.pi/2)
        T12 = DH(theta2, 0, a2, 0)
        T23 = DH(theta3, 0, a3, 0)

        T03 = T01 @ T12 @ T23
        R03 = T03[:3, :3]

        
        R36 = R03.T @ R06

        theta5 = np.arctan2(
            np.sqrt(R36[0,2]**2 + R36[1,2]**2),
            R36[2,2]
        )

        if abs(np.sin(theta5)) < 1e-6:
            theta4 = 0
            theta6 = np.arctan2(-R36[1,0], R36[0,0])
        else:
            theta4 = np.arctan2(R36[1,2], R36[0,2])
            theta6 = np.arctan2(R36[2,1], -R36[2,0])

        return theta1, theta2, theta3, theta4, theta5, theta6
  

    def update_matrix(theta1, theta2, theta3,
                  theta4, theta5, theta6,
                  d1, a2, a3, d4, d5, d6):

        def DH(theta, d, a, alpha):
            return np.array([
                [np.cos(theta), -np.sin(theta)*np.cos(alpha),
                np.sin(theta)*np.sin(alpha), a*np.cos(theta)],

                [np.sin(theta), np.cos(theta)*np.cos(alpha),
                -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],

                [0, np.sin(alpha),
                np.cos(alpha), d],

                [0,0,0,1]
            ])

        
        T01 = DH(theta1, d1, 0, np.pi/2)
        T12 = DH(theta2, 0, a2, 0)
        T23 = DH(theta3, 0, a3, 0)

        
        T34 = DH(theta4, d4, 0, np.pi/2)   # yaw link
        T45 = DH(theta5, d5, 0, -np.pi/2)  # roll link
        T56 = DH(theta6, d6, 0, 0)         # gripper

       
        T06 = T01 @ T12 @ T23 @ T34 @ T45 @ T56

        txt = (
            f"[ {T06[0,0]:>8.3f} {T06[0,1]:>8.3f} {T06[0,2]:>8.3f} {T06[0,3]:>8.3f} ]\n"
            f"[ {T06[1,0]:>8.3f} {T06[1,1]:>8.3f} {T06[1,2]:>8.3f} {T06[1,3]:>8.3f} ]\n"
            f"[ {T06[2,0]:>8.3f} {T06[2,1]:>8.3f} {T06[2,2]:>8.3f} {T06[2,3]:>8.3f} ]\n"
            f"[ {T06[3,0]:>8.3f} {T06[3,1]:>8.3f} {T06[3,2]:>8.3f} {T06[3,3]:>8.3f} ]"
        )

        matrix_lbl.config(text=txt)

        return T06

    

    def update_euler(theta1, theta2, theta3,
                 theta4, theta5, theta6,
                 d1, a2, a3, d4, d5, d6):

        def DH(theta, d, a, alpha):
            return np.array([
                [np.cos(theta), -np.sin(theta)*np.cos(alpha),
                np.sin(theta)*np.sin(alpha), a*np.cos(theta)],

                [np.sin(theta), np.cos(theta)*np.cos(alpha),
                -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],

                [0, np.sin(alpha),
                np.cos(alpha), d],

                [0,0,0,1]
            ])

        # base + arm
        T01 = DH(theta1, d1, 0, np.pi/2)
        T12 = DH(theta2, 0, a2, 0)
        T23 = DH(theta3, 0, a3, 0)

        # wrist (FIXED LENGTHS HERE)
        T34 = DH(theta4, d4, 0, np.pi/2)
        T45 = DH(theta5, d5, 0, -np.pi/2)
        T56 = DH(theta6, d6, 0, 0)

        T06 = T01 @ T12 @ T23 @ T34 @ T45 @ T56
        R = T06[:3, :3]

        sy = np.sqrt(R[0,0]**2 + R[1,0]**2)
        singular = sy < 1e-6

        if not singular:
            roll  = np.arctan2(R[2,1], R[2,2])
            pitch = np.arctan2(-R[2,0], sy)
            yaw   = np.arctan2(R[1,0], R[0,0])
        else:
            roll  = np.arctan2(-R[1,2], R[1,1])
            pitch = np.arctan2(-R[2,0], sy)
            yaw   = 0

        euler_lbl.config(
            text=
            f"ROLL  = {np.degrees(roll):.2f}°\n"
            f"PITCH = {np.degrees(pitch):.2f}°\n"
            f"YAW   = {np.degrees(yaw):.2f}°"
        )
    

    def update_jacobian(theta1, theta2, theta3,
                    theta4, theta5, theta6,
                    d1, a2, a3,
                    d4=74.17, d5=71.09, d6=40):

        def DH(theta, d, a, alpha):
            return np.array([
                [np.cos(theta), -np.sin(theta)*np.cos(alpha),
                np.sin(theta)*np.sin(alpha), a*np.cos(theta)],

                [np.sin(theta), np.cos(theta)*np.cos(alpha),
                -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],

                [0, np.sin(alpha),
                np.cos(alpha), d],

                [0,0,0,1]
            ])

       
        T01 = DH(theta1, d1, 0, np.pi/2)
        T12 = DH(theta2, 0, a2, 0)
        T23 = DH(theta3, 0, a3, 0)

        T34 = DH(theta4, d4, 0, np.pi/2)
        T45 = DH(theta5, 0, 0, -np.pi/2)
        T56 = DH(theta6, d6, 0, 0)

        T02 = T01 @ T12
        T03 = T02 @ T23
        T04 = T03 @ T34
        T05 = T04 @ T45
        T06 = T05 @ T56

     
        p0 = np.array([0,0,0])
        p1 = T01[:3,3]
        p2 = T02[:3,3]
        p3 = T03[:3,3]
        p4 = T04[:3,3]
        p5 = T05[:3,3]
        p6 = T06[:3,3]

        z0 = np.array([0,0,1])
        z1 = T01[:3,2]
        z2 = T02[:3,2]
        z3 = T03[:3,2]
        z4 = T04[:3,2]
        z5 = T05[:3,2]

       
        J = np.zeros((6,6))

        # linear and angular 3l4an tb2a s7
        

        J[0:3,0] = np.cross(z0, p6 - p0)
        J[3:6,0] = z0

        J[0:3,1] = np.cross(z1, p6 - p1)
        J[3:6,1] = z1

        J[0:3,2] = np.cross(z2, p6 - p2)
        J[3:6,2] = z2

        J[0:3,3] = np.cross(z3, p6 - p3)
        J[3:6,3] = z3

        J[0:3,4] = np.cross(z4, p6 - p4)
        J[3:6,4] = z4

        J[0:3,5] = np.cross(z5, p6 - p5)
        J[3:6,5] = z5

        txt = ""
        for i in range(6):
            txt += "[ " + " ".join(f"{x:7.2f}" for x in J[i]) + " ]\n"

        jacobian_lbl.config(text=txt)
       
        
        return J
    
    def draw_robot(theta1, theta2, theta3,
               theta4, theta5, theta6,
               d1, a2, a3,
               trail=[],
               obj=None,
               color="#00ff99",
               grip_open=15):

        ax.clear()
        ax.set_facecolor(PANEL)

        draw_workspace(d1, a2, a3)

       
        
        # JOINT 0 (BASE) elhowa fe elard
        p0 = np.array([0, 0, 0])

    
        # JOINT 1 (BASE ROTATION - theta1) 
        p1 = np.array([0, 0, d1])

        
        # JOINT 2 (SHOULDER - theta2)
        p2 = p1 + np.array([
            a2*np.cos(theta2)*np.cos(theta1),
            a2*np.cos(theta2)*np.sin(theta1),
            a2*np.sin(theta2)
        ])

       
        # JOINT 3 (ELBOW - theta3)
    
        p3 = p2 + np.array([
            a3*np.cos(theta2 + theta3)*np.cos(theta1),
            a3*np.cos(theta2 + theta3)*np.sin(theta1),
            a3*np.sin(theta2 + theta3)
        ])

      
        # TOOL DIRECTION (end-effector axis)
    
        tool_dir = np.array([
            np.cos(theta1)*np.cos(theta2 + theta3),
            np.sin(theta1)*np.cos(theta2 + theta3),
            np.sin(theta2 + theta3)
        ])

      
        # SIDE AXIS (perpendicular to arm)

        side = np.array([
            -np.sin(theta1),
            np.cos(theta1),
            0
        ])

       
        # UP AXIS 
        up = np.cross(side, tool_dir)

        # tool link lengths (wrist + gripper) a5r t7disat mina 
        L4 = 74.17   # joint 4 (yaw link)
        L5 = 71.09   # joint 5 (pitch/roll link)
        L6 = 40      # gripper

        
        # JOINT 4 (WRIST YAW - theta4)
       
        p4 = p3 + L4 * (np.cos(theta4)*tool_dir + np.sin(theta4)*side)
      
        # JOINT 5 (WRIST PITCH - theta5)
        #gripper up/down
      
        p5 = p4 + L5 * (
            np.cos(theta5)*tool_dir +
            np.sin(theta5)*up
        )

    
        # JOINT 6 (GRIPPER - theta6) zi el TPT
        # final extension 
        p6 = p5 + L6 * tool_dir

      
    
        pts = [p0, p1, p2, p3, p4, p5, p6]

        colors = ['#34495e', '#3498db', '#9b59b6',
                '#f39c12', '#1abc9c', '#e67e22']

        
        for i in range(len(pts) - 1):
            draw_cylinder(pts[i], pts[i+1], radius=7, color=colors[i])

      
        draw_gripper(p6, theta1, theta2, theta3, grip_open)

        ax.scatter(p6[0], p6[1], p6[2], color='yellow', s=160)

       
       
     
        if len(trail) > 1:
            xs = [p[0] for p in trail]
            ys = [p[1] for p in trail]
            zs = [p[2] for p in trail]
            ax.plot3D(xs, ys, zs, color=color, linewidth=3)

       
       
     
        if obj is not None:
            ax.scatter(obj[0], obj[1], obj[2], color='black', s=250)


        # VIEW LIMITS
        
        max_range = d1 + a2 + a3 + 200

        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([0, max_range])

        ax.set_xlabel("X", color='white')
        ax.set_ylabel("Y", color='white')
        ax.set_zlabel("Z", color='white')

        ax.tick_params(colors='white')
        ax.view_init(elev=28, azim=40)

        canvas.draw()

        return p6

    
    # EXPERIMENTS
   
    def run_pick_and_place():

        sx = float(sx_entry.get())
        sy = float(sy_entry.get())
        sz = float(sz_entry.get())

        ex = float(ex_entry.get())
        ey = float(ey_entry.get())
        ez = float(ez_entry.get())

       
        # FIXED LINKS
       
        d1 = 100
        d4 = 74.17
        d5 = 71.09
        d6 = 40   # gripper offset 
        
      
        # VARIABLE LINKS sabt atwalhom yarbbbbbbbbbb
       
        a2 = float(link_entries[0].get()) # de keda shoulder
        a3 = float(link_entries[1].get()) # de keda elbowww

        
        # LIMIT CHECK
       
        if not (150 <= a2 <= 180):
            messagebox.showerror(
                "Invalid Shoulder",
                "a2 must be 150 → 180 mm (step 10)"
            )
            return

        if not (130 <= a3 <= 150):
            messagebox.showerror(
                "Invalid Elbow",
                "a3 must be 130 → 150 mm (step 10)"
            )
            return

        trail = []
        steps = 80

        for i in range(steps):

            tau = i / steps
            t = 3*(tau**2) - 2*(tau**3)   

            x = sx + (ex - sx) * t
            y = sy + (ey - sy) * t
            z = sz + (ez - sz) * t + 30*np.sin(np.pi*t)

            ik = IK(x, y, z,
                        0, 0, 0,
                        d1, a2, a3,
                        d4, d5, d6)

            if ik is None:
                continue

            theta1, theta2, theta3, theta4, theta5, theta6 = ik


            trail.append([x, y, z])

            draw_robot(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3, 
                trail,
                [x, y, z],
                "#00ff99",
                5
            )

            update_matrix(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )

            update_euler(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )

            jac = update_jacobian(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )
            
            jac_rank = np.linalg.matrix_rank(jac)

            velocity = np.sqrt(
                (ex - sx)**2 +
                (ey - sy)**2 +
                (ez - sz)**2
            ) / steps

            accel = velocity / steps

            motion_lbl.config(
                text=f"Velocity = {velocity:.2f}\nAcceleration = {accel:.4f}"
            )

            analysis_lbl.config(
                text=
                f"MODE: PICK & PLACE\n"
                f"X={x:.2f}\n"
                f"Y={y:.2f}\n"
                f"Z={z:.2f}\n\n"
                f"JACOBIAN:\n{np.array2string(jac, precision=2)}"
            )

            if jac_rank < 6:
                status_lbl.config(text="SINGULARITY", fg="orange")
            else:
                status_lbl.config(text="SAFE", fg="#2ecc71")

            window.update()
            time.sleep(0.02)
    

    def run_circular_motion():

       
        # FIXED LINKS
      
        d1 = 100
        d4 = 74.17
        d5 = 71.09
        d6 = 40   # gripper 

      
        # VARIABLE LINKS 
       
        a2 = float(link_entries[0].get())
        a3 = float(link_entries[1].get())

        
        # LIMITS
        
        if not (150 <= a2 <= 180):
            messagebox.showerror("Error", "Shoulder must be 150–180 mm")
            return

        if not (130 <= a3 <= 150):
            messagebox.showerror("Error", "Elbow must be 130–150 mm")
            return

        
        # ROBOT REACH MODEL 7asa fe 7aga m7tagh ttzwd m7tagen ns2l mina
     
        reach = a2 + a3

        radius = reach * 0.30
        center_x = reach * 0.40
        center_y = 0
        z = d1 + 80

       
        if center_x + radius > reach:
            radius = reach * 0.20

        trail = []

        
      
        
        for ang in np.linspace(0, 2*np.pi, 150):

            x = center_x + radius * np.cos(ang)
            y = center_y + radius * np.sin(ang)

            ik = IK(x, y, z,
                0, 0, 0,
                d1, a2, a3,
                d4, d5, d6)

            if ik is None:
                continue

            theta1, theta2, theta3, theta4, theta5, theta6 = ik

          
            trail.append([x, y, z])

            draw_robot(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                trail,
                [x, y, z],
                color="#00ff99",
                grip_open=5
            )

            update_matrix(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )

            update_euler(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )

            jac = update_jacobian(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )
            
            jac_rank = np.linalg.matrix_rank(jac)
            
            analysis_lbl.config(
                text=
                f"CIRCULAR TRAJECTORY\n\n"
                f"Reach  = {reach:.1f} mm\n"
                f"Radius = {radius:.1f} mm\n"
                f"Angle  = {np.degrees(ang):.1f}°\n"
                f"Jacobian:\n{np.array2string(jac, precision=2)}"
            )
            if jac_rank < 6:
                status_lbl.config(text="SINGULARITY", fg="orange")
            else:
                status_lbl.config(text="SAFE", fg="#2ecc71")
                
            status_lbl.config(
                text="CIRCULAR MOTION",
                fg="#f39c12"
            )

            window.update()
            time.sleep(0.02)

   

    def run_ptp_motion():

        sx = float(sx_entry.get())
        sy = float(sy_entry.get())
        sz = float(sz_entry.get())

        ex = float(ex_entry.get())
        ey = float(ey_entry.get())
        ez = float(ez_entry.get())

      
        # FIXED LINKS (6 DOF)
        
        d1 = 100
        d4 = 74.17
        d5 = 71.09
        d6 = 40   # gripper

       
        # VARIABLE LINKS
       
        a2 = float(link_entries[0].get())
        a3 = float(link_entries[1].get())

        
        # LIMITS 
      
        if not (150 <= a2 <= 180):
            messagebox.showerror("Error", "Shoulder must be 150–180 mm")
            return

        if not (130 <= a3 <= 150):
            messagebox.showerror("Error", "Elbow must be 130–150 mm")
            return

       
       
       
        reach = a2 + a3

        start_dist = np.sqrt(sx**2 + sy**2 + (sz - d1)**2)
        end_dist   = np.sqrt(ex**2 + ey**2 + (ez - d1)**2)

        if start_dist > reach or end_dist > reach:
            messagebox.showerror("Workspace Error", "Point outside workspace")
            return

      
      
      
        trail = []

        steps = 80

        for i in range(steps + 1):

            t = i / steps

            x = sx + (ex - sx) * t
            y = sy + (ey - sy) * t
            z = sz + (ez - sz) * t

            ik = IK(x, y, z,
                0,0,0,
                d1,a2,a3,
                d4,d5,d6)

            if ik is None:
                continue

            theta1, theta2, theta3, theta4, theta5, theta6 = ik

           

            trail.append([x, y, z])

          
            # DRAW
          
            draw_robot(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                trail,
                [x, y, z],
                color="#00ff99",
                grip_open=5
            )

           
            # MATRIX (FULL 6 DOF)
        
            update_matrix(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )

           
            # EULER
          
            update_euler(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )

           
            # JACOBIAN 
            
            jac = update_jacobian(
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3,
                d4, d5, d6
            )
            
            jac_rank = np.linalg.matrix_rank(jac)
            
            analysis_lbl.config(
                text=
                f"POINT TO POINT (6 DOF)\n\n"
                f"X = {x:.1f}\nY = {y:.1f}\nZ = {z:.1f}\n\n"
                 f"Jacobian:\n{np.array2string(jac, precision=2)}"
            )

            if jac_rank < 6:
                status_lbl.config(text="SINGULARITY", fg="orange")
            else:
                status_lbl.config(text="SAFE MOTION", fg="#9b59b6")

            window.update()
            time.sleep(0.02)
   

    def run_experiment():

        exp=EXPERIMENT_TYPE.get()

        if exp=="Pick and Place":
            run_pick_and_place()

        elif exp=="Circular Path":
            run_circular_motion()

        elif exp=="Point to Point":
            run_ptp_motion()

        else:
            run_pick_and_place()

  
   
    

    def update_experiment_ui(event=None):

        for widget in dynamic_left_frame.winfo_children():
            widget.destroy()

        global sx_entry, sy_entry, sz_entry
        global ex_entry, ey_entry, ez_entry
        global link_entries

        #INPUTS FOR THE SYSTEM M7TAGEN 3LA ASASHA NZABT REACH W TOL Z AXIS K MAXIMUM RANGE
        # START POSITION
        
        start_frame = LabelFrame(
            dynamic_left_frame,
            text=" START POSITION ",
            bg=BG,
            fg="#2ecc71",
            font=("Arial",10,"bold")
        )
        start_frame.pack(fill=X,pady=5)

        start_entries = []

        for txt, val in [("X",120), ("Y",40), ("Z",180)]:

            Label(start_frame, text=f"{txt} (mm)", bg=BG, fg="white").pack()

            e = Entry(start_frame, font=("Consolas",11))
            e.insert(0, str(val))
            e.pack(fill=X, pady=2)

            start_entries.append(e)

        sx_entry, sy_entry, sz_entry = start_entries


        # TARGET POSITION
        
        end_frame = LabelFrame(
            dynamic_left_frame,
            text=" TARGET POSITION ",
            bg=BG,
            fg="#f1c40f",
            font=("Arial",10,"bold")
        )
        end_frame.pack(fill=X,pady=5)

        end_entries = []

        for txt, val in [("X",220), ("Y",120), ("Z",140)]:

            Label(end_frame, text=f"{txt} (mm)", bg=BG, fg="white").pack()

            e = Entry(end_frame, font=("Consolas",11))
            e.insert(0, str(val))
            e.pack(fill=X, pady=2)

            end_entries.append(e)

        ex_entry, ey_entry, ez_entry = end_entries

       
        # LINK PARAMETERS (6 DOF)
    

        links_frame = LabelFrame(
            dynamic_left_frame,
            text=" 6 DOF ROBOT LINKS ",
            bg=BG,
            fg="#00d2ff",
            font=("Arial",10,"bold")
        )
        links_frame.pack(fill=X,pady=5)

        link_entries = []

        # fixed + variable links
        link_data = [

           
            ("Shoulder a2 (150–180 step10)", 150),
            ("Elbow a3 (130–150 step10)", 130),

        ]

        for txt, val in link_data:

            Label(
                links_frame,
                text=txt,
                bg=BG,
                fg="white"
            ).pack()

            e = Entry(
                links_frame,
                font=("Consolas",11)
            )

            e.insert(0, str(val))

            
            if "fixed" in txt:
                e.config(state="disabled")

            e.pack(fill=X,pady=2)

            link_entries.append(e)

      
        # RUN BUTTON
  

        Button(
            dynamic_left_frame,
            text="RUN EXPERIMENT",
            bg="#2ecc71",
            fg="white",
            font=("Arial",12,"bold"),
            height=2,
            command=run_experiment
        ).pack(fill=X,pady=15)

    
    combo.bind("<<ComboboxSelected>>", update_experiment_ui)
    update_experiment_ui()
    draw_robot(
        0, 0, 0, 0, 0, 0,
        100, 150, 130,
        [],
        None,
        "#00ff99",
        15
    )
    show_university_logo()



 
    
    
    
    
    
    
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
    
    Label(video_frame, text="Watch IK Tutorial", font=("Arial", 18, "bold"), 
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
 
 
 
    




# yarb IK t5ls b2aaaaaaaaaa ma4oft4 22rf mn keda 

def open_ik_page():

    for widget in window.winfo_children():
        widget.destroy()
    global SAVED_A_MATRICES, SAVED_T06,IK_STARTED
    SAVED_A_MATRICES = []
    SAVED_T06 = None
    IK_STARTED = False
    BG_COLOR = "#0c1a30"
    IK_METHOD = StringVar(value="Geometric")
# simulation bt3t robot
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

        if len(SAVED_A_MATRICES) < 6 or SAVED_T06 is None:
           return

        idx = matrix_selector.current()

        matrices = [
            SAVED_A_MATRICES[0],
            SAVED_A_MATRICES[1],
            SAVED_A_MATRICES[2],
            SAVED_A_MATRICES[3],
            SAVED_A_MATRICES[4],
            SAVED_A_MATRICES[5],
            SAVED_T06
        ]

        titles = [
            "A1 MATRIX",
            "A2 MATRIX",
            "A3 MATRIX",
            "A4 MATRIX",
            "A5 MATRIX",
            "A6 MATRIX",
            "T06 MATRIX"
        ]
        descriptions = [
            "Base Rotation Matrix\nFrame0 → Frame1",

            "Shoulder Transformation\nFrame1 → Frame2",

            "Elbow Transformation\nFrame2 → Frame3",

            "Wrist Pitch Matrix\nFrame3 → Frame4",

            "Wrist Roll Matrix\nFrame4 → Frame5",

            "Tool/Yaw Matrix\nFrame5 → Frame6",

            "Final End Effector Matrix\nT06 = A1×A2×A3×A4×A5×A6"
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

    def draw_workspace(ax, d1, a2, a3, d6=40):

        r_max = a2 + a3 + d6
        r_min = abs(a2 - a3)

        theta = np.linspace(0, 2*np.pi, 60)
        phi = np.linspace(-np.pi/2, np.pi/2, 35)

        TH, PH = np.meshgrid(theta, phi)

        Xo = r_max * np.cos(PH) * np.cos(TH)
        Yo = r_max * np.cos(PH) * np.sin(TH)
        Zo = d1 + r_max * np.sin(PH)

        Xi = r_min * np.cos(PH) * np.cos(TH)
        Yi = r_min * np.cos(PH) * np.sin(TH)
        Zi = d1 + r_min * np.sin(PH)

        ax.plot_wireframe(Xo, Yo, Zo, color='#00ffaa', alpha=0.12, linewidth=0.5)
        ax.plot_wireframe(Xi, Yi, Zi, color='#ff5555', alpha=0.08, linewidth=0.5)

        z_line = np.linspace(d1 - r_max, d1 + r_max, 30)
        ax.plot(np.zeros_like(z_line), np.zeros_like(z_line), z_line,
                '--', color='white', alpha=0.1)

  

    def draw_robot(
            theta1, theta2, theta3,
            theta4, theta5, theta6,
            d1=100, a2=160, a3=140,
            a4=190, d6=40,
            projection=True):

        global SAVED_A_MATRICES, SAVED_T06

       
        ax.clear()

        ax.set_facecolor("#081b4b")
        ax.grid(True, color="#1f2d4d")

       
        def DH(theta, d, a, alpha):
            return np.array([
                [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
                [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
                [0,              np.sin(alpha),              np.cos(alpha),              d],
                [0, 0, 0, 1]
            ])

     
        T01 = DH(theta1, d1, 0, np.pi/2)
        T12 = DH(theta2, 0, a2, 0)
        T23 = DH(theta3, 0, a3, 0)

        T34 = DH(theta4, 0, 0, np.pi/2)
        T45 = DH(theta5, 0, 0, -np.pi/2)
        T56 = DH(theta6, d6, 0, 0)

        T02 = T01 @ T12
        T03 = T02 @ T23
        T04 = T03 @ T34
        T05 = T04 @ T45
        T06 = T05 @ T56

        
        SAVED_A_MATRICES = [T01, T12, T23, T34, T45, T56]
        SAVED_T06 = T06

     
        p0 = np.array([0, 0, 0])
        p1 = T01[:3, 3]
        p2 = T02[:3, 3]
        p3 = T03[:3, 3]
        p4 = T04[:3, 3]
        p5 = T05[:3, 3]
        p6 = T06[:3, 3]

        pts = [p0, p1, p2, p3, p4, p5, p6]

        colors = [
            '#34495e', '#3498db', '#9b59b6',
            '#e67e22', '#1abc9c', '#f1c40f'
        ]

        for i in range(len(pts)-1):
            draw_3d_cylinder(ax, pts[i], pts[i+1], radius=7, color=colors[i])

            ax.scatter(
                pts[i][0], pts[i][1], pts[i][2],
                color='#e74c3c', s=80
            )

       
        ax.scatter(
            p6[0], p6[1], p6[2],
            color='yellow', s=150
        )

        draw_gripper(
            ax,
            p6,
            math.degrees(theta1),
            math.degrees(theta2),
            math.degrees(theta3)
        )

       
        if projection:
            ax.plot([p6[0], p6[0]], [p6[1], p6[1]], [0, p6[2]],
                    '--', color='#00ffff')

            ax.plot([0, p6[0]], [0, p6[1]], [0, 0],
                    '--', color='#ff00ff')

        draw_workspace(ax, d1, a2, a3)

    
        max_range = d1 + a2 + a3 + d4 + 200

        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([0, max_range])

        ax.set_xlabel("X Axis (mm)", color='white')
        ax.set_ylabel("Y Axis (mm)", color='white')
        ax.set_zlabel("Z Axis (mm)", color='white')

        ax.tick_params(colors='white')

        ax.view_init(elev=28, azim=40)

        ax.text(
            p6[0], p6[1], p6[2] + 20,
            f"EE\nX={p6[0]:.1f}\nY={p6[1]:.1f}\nZ={p6[2]:.1f}",
            color='yellow'
        )

        canvas.draw()
    

    def animate_robot(
        current_t1, current_t2, current_t3,
        current_t4, current_t5, current_t6,
        target_t1, target_t2, target_t3,
        target_t4, target_t5, target_t6,
        d1, a2, a3, a4):

        steps = 40

        for i in range(steps + 1):
            r = i / steps

            draw_robot(
                current_t1 + (target_t1 - current_t1) * r,
                current_t2 + (target_t2 - current_t2) * r,
                current_t3 + (target_t3 - current_t3) * r,
                current_t4 + (target_t4 - current_t4) * r,
                current_t5 + (target_t5 - current_t5) * r,
                current_t6 + (target_t6 - current_t6) * r,
                d1, a2, a3, a4
            )

            window.update()

    def solve_inverse_kinematics():
        global IK_STARTED, SAVED_A_MATRICES, SAVED_T06

        try:
            IK_STARTED = True

           
            x = float(x_entry.get())
            y = float(y_entry.get())
            z = float(z_entry.get())

            d1 = 100
            a2, a3 = [float(e.get()) for e in link_entries]
            a4 = 190
            # tool offset
            z = z - a4

            roll  = math.radians(float(roll_entry.get()))
            pitch = math.radians(float(pitch_entry.get()))
            yaw   = math.radians(float(yaw_entry.get()))

           

            cr, sr = math.cos(roll), math.sin(roll)
            cp, sp = math.cos(pitch), math.sin(pitch)
            cy, sy = math.cos(yaw), math.sin(yaw)

            R06 = np.array([
                [cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
                [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
                [-sp,   cp*sr,            cp*cr]
            ])

           
            wc_x = x - a4 * R06[0, 2]
            wc_y = y - a4 * R06[1, 2]
            wc_z = z - a4 * R06[2, 2]

            

            theta1 = math.atan2(wc_y, wc_x)

            r = math.sqrt(wc_x**2 + wc_y**2)
            s = wc_z - d1

            D = (r**2 + s**2 - a2**2 - a3**2) / (2 * a2 * a3)
            D = max(min(D, 1.0), -1.0)

            if abs(D) > 1.0:
                singularity_lbl.config(text="UNREACHABLE ❌", fg="red")
                return
            
            theta3 = math.atan2(math.sqrt(1 - D**2), D)

            theta2 = math.atan2(s, r) - math.atan2(
                a3 * math.sin(theta3),
                a2 + a3 * math.cos(theta3)
            )

            

            def DH(theta, d, a, alpha):
                return np.array([
                    [math.cos(theta), -math.sin(theta)*math.cos(alpha), math.sin(theta)*math.sin(alpha), a*math.cos(theta)],
                    [math.sin(theta),  math.cos(theta)*math.cos(alpha), -math.cos(theta)*math.sin(alpha), a*math.sin(theta)],
                    [0,               math.sin(alpha),                  math.cos(alpha),                 d],
                    [0, 0, 0, 1]
                ])

            A1 = DH(theta1, d1, 0, math.pi/2)
            A2 = DH(theta2, 0, a2, 0)
            A3 = DH(theta3, 0, a3, 0)

          
            T03 = A1 @ A2 @ A3
            R03 = T03[:3, :3]

            R36 = R03.T @ R06

            theta5 = math.atan2(
                math.sqrt(R36[0,2]**2 + R36[1,2]**2),
                R36[2,2]
            )

            if abs(math.sin(theta5)) < 1e-6:
                theta4 = 0
                theta6 = math.atan2(-R36[1,0], R36[0,0])
            else:
                theta4 = math.atan2(R36[1,2], R36[0,2])
                theta6 = math.atan2(R36[2,1], -R36[2,2])

           
            A4 = DH(theta4, 0, 0, math.pi/2)
            A5 = DH(theta5, 0, 0, -math.pi/2)
            A6 = DH(theta6, a4, 0, 0)

            SAVED_A_MATRICES = [A1, A2, A3, A4, A5, A6]
            SAVED_T06 = A1 @ A2 @ A3 @ A4 @ A5 @ A6

          
            angles = [theta1, theta2, theta3, theta4, theta5, theta6]

            for i in range(6):
                angle_labels[i].config(
                    text=f"{math.degrees(angles[i]):.2f}°"
                )

          
            ee_pos = SAVED_T06[:3, 3]
            target = np.array([x, y, z])

            error = np.linalg.norm(ee_pos - target)

            extra_info.config(
                text=f"Position Error: {error:.5f}"
            )

           
            if abs(math.sin(theta3)) < 0.05:
                singularity_lbl.config(text="SINGULARITY ⚠", fg="orange")
            else:
                singularity_lbl.config(text="SAFE ✔", fg="#2ecc71")

            update_matrix_view()

            
            prev = getattr(solve_inverse_kinematics, "last_angles",
                        [0,0,0,0,0,0])

            animate_robot(
                prev[0], prev[1], prev[2],
                prev[3], prev[4], prev[5],
                theta1, theta2, theta3,
                theta4, theta5, theta6,
                d1, a2, a3, a4
            )

            solve_inverse_kinematics.last_angles = angles

        except Exception as e:
            messagebox.showerror("IK ERROR", str(e))

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
    
    "Link2 Shoulder (160-200)",
    "Link3 Elbow (140-160)",
    
   ]

    defaults = [ 160, 140]


    link_entries = []

    for i in range(2):

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
    


    rpy_frame = LabelFrame(
    left,
    text=" END-EFFECTOR ORIENTATION (RPY) ",
    bg=BG_COLOR,
    fg="#9b59b6",
    font=("Arial",10,"bold")
    )

    rpy_frame.pack(fill=X, pady=5)

    rpy_entries = []

    for txt, val in [
        ("Roll (deg)", 0),
        ("Pitch (deg)", 0),
        ("Yaw (deg)", 0)
    ]:
        Label(
            rpy_frame,
            text=txt,
            bg=BG_COLOR,
            fg="white"
        ).pack()

        e = Entry(
            rpy_frame,
            font=("Consolas",11)
        )

        e.insert(0, str(val))
        e.pack(fill=X, pady=2)

        rpy_entries.append(e)

    roll_entry, pitch_entry, yaw_entry = rpy_entries
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
            "A4 Matrix",
            "A5 Matrix",
            "A6 Matrix",
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
    
    Label(video_frame, text="Watch FK Tutorial", font=("Arial", 18, "bold"), 
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
current_angles = [0, 0, 0, 0, 0, 0]
SAVED_A_MATRICES = [np.eye(4) for _ in range(6)]
SAVED_T06 = np.eye(4)

is_sim_started = False

def open_fk_page():
    for widget in window.winfo_children(): 
        widget.destroy()
    global SAVED_A_MATRICES, SAVED_T06
    if not isinstance(SAVED_A_MATRICES, list) or len(SAVED_A_MATRICES) < 6:
        SAVED_A_MATRICES = [np.eye(4) for _ in range(6)]
    if SAVED_T06 is None:
        SAVED_T06 = np.eye(4)
   
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
            # m7tagen n3dlhom 3la a5r 7aga 3nd mina
            joint_limits = [
                (-135.0, 135.0), # Base
                (0.0, 180.0),    # Shoulder
                (-80.0, 90.0),   # Elbow
                (-90.0, 90.0),   # Wrist Pitch / Rest
                (-180.0, 180.0), # Wrist Roll / Roll
                (0.0, 180.0),    # Yaw 
                (0.0, 90.0),     #Gripper
            ]
            
        # limits bt3t mina kolo mm a5r update 
            dim_limits = [
                (150.0, 180.0),  # a2
                (130.0, 150.0)  # a3    
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

            d1_val = 100.0          # fixed base link
            a2_val = link_vals[0]   # variable shoulder
            a3_val = link_vals[1]   # variable elbow

            d4_val = 74.17          # FIXED
            d5_val = 71.09          # FIXED (wrist roll segment)
            d6_val = 40.0           # gripper
            
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
            
            # Link 2 shoulder 
            c2, s2 = math.cos(thetas[1]), math.sin(thetas[1])
            ca2, sa2 = math.cos(alphas[1]), math.sin(alphas[1])
            SAVED_A_MATRICES[1] = np.array([
                [c2, -s2*ca2,  s2*sa2, a2_val * c2],
                [s2,  c2*ca2, -c2*sa2, a2_val * s2],
                [ 0,     sa2,     ca2, 0],
                [ 0,       0,       0, 1]
            ])
            
            # Link 3 elbow
            c3, s3 = math.cos(thetas[2]), math.sin(thetas[2])
            ca3, sa3 = math.cos(alphas[2]), math.sin(alphas[2])
            SAVED_A_MATRICES[2] = np.array([
                [c3, -s3*ca3,  s3*sa3, a3_val * c3],
                [s3,  c3*ca3, -c3*sa3, a3_val * s3],
                [ 0,     sa3,     ca3, 0],
                [ 0,       0,       0, 1]
            ])
            
            # a3takd keda tmm m3a 4o8l mina elgdid
            for i in range(3, 6):
                c, s = math.cos(thetas[i]), math.sin(thetas[i])
                ca, sa = math.cos(alphas[i]), math.sin(alphas[i])

                if i == 3:
                   d_val = d4_val

                elif i == 5:
                   d_val = d6_val

                else:
                   d_val = 0.0
                
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
            
            max_range = d1_val + a2_val + a3_val + d4_val + d6_val
            
           
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
                p4 = p3 + np.array([
                     d4_val * math.cos(phi23) * math.cos(phi1),
                     d4_val * math.cos(phi23) * math.sin(phi1),
                     d4_val * math.sin(phi23)
                ])

                pts.append(p4)
                ee_pos = SAVED_T06[0:3, 3]
                
                if all(abs(t) < 1e-6 for t in thetas):
                    
                    p5 = p4 + np.array([20.0 * math.cos(phi1),20.0 * math.sin(phi1),0.0])
                    p6 = p5 + np.array([d6_val * math.cos(phi1), d6_val * math.sin(phi1), 0.0])
                    pts.extend([ p5, p6])
                else:
                    p5 = p4 + (ee_pos - p4) * 0.5
                    p6 = ee_pos

                    pts.extend([p5, p6])
                    
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
                
        
                gripper_val = float(joints[6].get()) 
                gripper_span = 20.0 - (gripper_val * (15.0 / 90.0)) 
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

                if i == 3:
                    dh_labels[i]["d"].config(text=f"{d4_val:.1f}")
                elif i == 4:
                    dh_labels[i]["d"].config(text=f"{d5_val:.1f}")
                elif i == 5:
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
    
    joint_names = ["Base (NEMA 23)", "Shoulder (Servo 35)", "Elbow (Servo 35)", "Rest (Servo 11/20)", "Roll (NEMA 17)", "Yaw (Servo 11)","Gripper(Black Servo)"]
    joint_ranges_text = ["[-135° to 135°]", "[0° to 180°]", "[-80° to 90°]", "[-90° to 90°]", "[-180° to 180°]", "[0° to 180°]","[0° to 90°]"]
    
    for i in range(7):
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
    for i, d_entry in enumerate(link_dims):
        d_entry.bind("<KeyRelease>", lambda event: run_fk_calculations(from_button=False))
        d_entry.bind("<FocusOut>", lambda event: run_fk_calculations(from_button=False))
     # 7aagt mina b default   
    dim_configs = [
    ("Link 2 Length a2 (150-180 mm)", "150.0"),
    ("Link 3 Length a3 (130-150 mm)", "130.0")
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
    my_robot_alphas = [90, 0, 0, 90, -90, 0] # keda keda l7d ma nzabta
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
        
    # seif grb hna     
    try:          # 8yr com bs 3la 7sb htwasl fen 
        esp = serial.Serial('COM5', 115200, timeout=1)
        print("ESP connected ")
    except:
        esp = None
        print("ESP not connected ")
        
    def sync_to_hardware():
        try:
            angles = [float(j.get()) for j in joints]
            link_vals = [
                100.0,      # d1 fixed base
                float(link_dims[0].get()), # shoulder
                float(link_dims[1].get()), #elbow
                74.17, # yaw
                71.09, #roll
                40.0  # gripper ay 7aga l7d ma n3rf el tol
            ] 
            payload = {
                "angles": angles,
                "links": link_vals
            }
            
            msg = json.dumps(payload)
            print("SENDING TO HARDWARE:")
            print(msg)

            if esp is not None:
                esp.write((msg + "\n").encode())   
                esp.flush()
                print("Sent to ESP32 ")
                messagebox.showinfo("SUCCESS", "Data sent to ESP32")
            else:
                print("No ESP connection")
                messagebox.showwarning("WARNING", "ESP not connected")

          

        except Exception as e:
            messagebox.showerror("Error", str(e))
           

       
    
    
    
    sync_frame = Frame(right_p, bg="#0a1e4d", bd=1, relief=SOLID)
    sync_frame.pack(side=BOTTOM, fill=X, pady=4)
    Button(
        sync_frame,
        text="SYNC TO HARDWARE",
        bg="#27ae60",
        fg="white",
        font=("Arial", 10, "bold"),
        command=sync_to_hardware
    ).pack(pady=4, padx=10, fill=X)

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
        ("3. Pick and Place Control", open_trajectory_intro_page), 
        ("4. Torque & Forces", open_dynamics_intro_page)
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
        l_lbl.place(relx=0.99, rely=0.01, anchor="ne")
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