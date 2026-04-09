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

#3l4an a create window 
window = Tk()
window.title('Robotic Arm Virtual Lab App')
window.state('zoomed') 
BG_COLOR = "#04153B" 
window.configure(bg=BG_COLOR)


def calculate_ik_angles(x, y, z):
    
    j1 = np.degrees(np.arctan2(y, x))
    r = np.sqrt(x**2 + y**2)
    d = np.sqrt(r**2 + z**2)
    if d > 12: d = 12 
    j2 = np.degrees(np.arccos(np.clip(d/15, -1, 1))) * 1.5
    j3 = -j2 * 0.8
    return [j1, j2, j3, 0, 0, 0]

#3l4an 3d robot elfeh simulation
def update_robot_plot(ax, canvas, joints, target_dot=None):
    ax.clear()
    ax.set_facecolor('#081b4b')
    t = np.linspace(0, 2*np.pi, 50)
    r_base = 1.2
    X_b = r_base * np.cos(t)
    Y_b = r_base * np.sin(t)
    Z_b = np.zeros_like(X_b)
    ax.plot(X_b, Y_b, Z_b, color="#4c7f8f", linewidth=2)
    
    if target_dot:
        ax.scatter([target_dot[0]], [target_dot[1]], [target_dot[2]], color='red', s=100, label='Target')

    
    angles = [np.radians(j.get() if hasattr(j, 'get') else j) for j in joints]
    curr_x, curr_y, curr_z = 0, 0, 0
    L = 2 
    for i in range(len(angles)):
        prev_pos = [curr_x, curr_y, curr_z]
        curr_x += L * np.cos(sum(angles[:i+1]))
        curr_y += L * np.sin(sum(angles[:i+1]))
        curr_z += L * np.sin(angles[i]) 
        new_pos = [curr_x, curr_y, curr_z]
        ax.plot([prev_pos[0], new_pos[0]], [prev_pos[1], new_pos[1]], [prev_pos[2], new_pos[2]], 
                color='#f36412', linewidth=10, solid_capstyle='round')
        ax.scatter([curr_x], [curr_y], [curr_z], color='white', s=60, edgecolors='black')

    ax.set_xlim([-10, 10]); ax.set_ylim([-10, 10]); ax.set_zlim([0, 10])
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_title("3D ROBOTIC ARM SIMULATION", color='white', fontname="Arial", fontsize=14, fontweight='bold')
    ax.view_init(elev=30, azim=45)
    canvas.draw()

# 3l4an popup manual 3la 4kl window
def show_fancy_manual(title, content):
    manual_window = Toplevel(window)
    manual_window.title(title)
    manual_window.geometry("550x550")
    manual_window.configure(bg="#0a1e4d")
    manual_window.transient(window)
    manual_window.grab_set()
    Label(manual_window, text=" " + title, font=("Helvetica", 18, "bold"), fg="#f39c12", bg="#0a1e4d").pack(pady=20)
    text_area = Message(manual_window, text=content, font=("Arial", 12), fg="white", bg="#0a1e4d", width=400, justify=LEFT)
    text_area.pack(pady=10, padx=20)
    Label(manual_window, text="__________________________", fg="#f36412", bg="#0a1e4d").pack()
    Button(manual_window, text="LET'S GO!", font=("Arial", 12, "bold"), bg="#f36412", fg="white", 
           padx=20, pady=10, command=manual_window.destroy).pack(pady=20)

#da message box 3la gnb keda
def create_manual_box(parent, title, steps):
    manual_frame = Frame(parent, bg="#0a1e4d", bd=1, relief=SOLID)
    manual_frame.pack(side=RIGHT, fill=Y, padx=10, pady=20)
    Label(manual_frame, text="LAB MANUAL", font=("Helvetica", 14, "bold"), fg="#f39c12", bg="#0a1e4d").pack(pady=10, padx=20)
    Label(manual_frame, text=title, font=("Arial", 11, "bold", "underline"), fg="white", bg="#0a1e4d").pack(pady=5, anchor=W, padx=10)
    msg = Message(manual_frame, text=steps, font=("Arial", 10), fg="#70afc2", bg="#0a1e4d", width=220, justify=LEFT)
    msg.pack(pady=10, padx=10, anchor=NW)
    Label(manual_frame, text="Sync with ESP32 for real motion.", font=("Arial", 8, "italic"), fg="white", bg="#0a1e4d").pack(side=BOTTOM, pady=(0, 10), padx=10)

# de IK gahza 
def open_ik_page():
    for widget in window.winfo_children(): widget.destroy()
    
    ik_info = (
        "WELCOME TO INVERSE KINEMATICS LAB!\n\n"
        "Objectives:\n"
        "1. Input coordinates (X, Y, Z).\n"
        "2. Let the algorithm find the required angles.\n\n"
        "Steps:\n"
        "1. Set the target position using sliders.\n"
        "2. Click 'SOLVE & MOVE'.\n"
        "3. Watch the arm reach the target."
    )
    show_fancy_manual("IK Study Guide", ik_info)

    Button(window, text=" Back to Experiments", font=("Arial", 12, "bold"), fg="#f36412", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(anchor=NW, padx=20, pady=10)
    
    container = Frame(window, bg=BG_COLOR); container.pack(expand=True, fill=BOTH, padx=20)
    
    left_p = Frame(container, bg=BG_COLOR); left_p.pack(side=LEFT, fill=Y, padx=10)
    Label(left_p, text="TARGET POSITION (IK)", font=("Helvetica", 18, "bold"), fg="#f39c12", bg=BG_COLOR).pack(pady=10)
    
    # Sliders l X, Y, Z coordinates
    coords = {}
    for axis in ['X', 'Y', 'Z']:
        f = Frame(left_p, bg=BG_COLOR); f.pack(pady=5, fill=X)
        Label(f, text=f"{axis}:", fg="white", bg=BG_COLOR, font=("Arial", 10, "bold"), width=4).pack(side=LEFT)
        s = Scale(f, from_=-8, to=8, resolution=0.1, orient=HORIZONTAL, bg="#03265b", fg="white", troughcolor="#2ecc71", length=180, bd=0)
        s.pack(side=LEFT)
        coords[axis] = s

    def run_ik_process():
        x_val = coords['X'].get()
        y_val = coords['Y'].get()
        z_val = coords['Z'].get()
        
        # hn7sb el Angles
        calc_angles = calculate_ik_angles(x_val, y_val, z_val)
        
        # hna bn3ml update ll parameters 
        update_robot_plot(ax, canvas, calc_angles, target_dot=(x_val, y_val, z_val))

    Button(left_p, text="SOLVE & MOVE ARM", bg="#f36412", fg="white", font=("Arial", 12, "bold"), pady=15, 
           command=run_ik_process).pack(pady=20, fill=X)

    create_manual_box(container, "IK Quick Reference", "1. Set Target XYZ\n2. Solve IK\n3. Verify Reachability")

    right_p = Frame(container, bg="#081b4b", bd=2, relief=RIDGE); right_p.pack(side=RIGHT, expand=True, fill=BOTH, padx=10, pady=20)
    fig = plt.figure(figsize=(10,10)); fig.patch.set_facecolor('#081b4b'); ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=right_p); canvas.get_tk_widget().pack(expand=True, fill=BOTH)
    update_robot_plot(ax, canvas, [0]*6)

#de FK gahza
def open_fk_page():
    for widget in window.winfo_children(): widget.destroy()
    
    fk_info = (
        "WELCOME TO FORWARD KINEMATICS LAB!\n\n"
        "Objectives:\n"
        "1. Understand joint angles to define position.\n"
        "2. Observe serial robotic chain behavior.\n\n"
        "Steps to follow:\n"
        "1. Watch the Tutorial video.\n"
        "2. Use J1 to J6 sliders to set angles.\n"
        "3. Click 'RUN SIMULATION' to see results."
    )
    show_fancy_manual("FK Study Guide", fk_info)

    Button(window, text="Back to Experiments", font=("Arial", 12, "bold"), fg="#f36412", bg=BG_COLOR, bd=0, command=open_experiments_page, borderwidth=10).pack(anchor=NW, padx=20, pady=10)
    container = Frame(window, bg=BG_COLOR); container.pack(expand=True, fill=BOTH, padx=20)
    
    left_p = Frame(container, bg=BG_COLOR); left_p.pack(side=LEFT, fill=Y, padx=10)
    Label(left_p, text="JOINTS (FK)", font=("Helvetica", 18, "bold"), fg="#f39c12", bg=BG_COLOR).pack(pady=10)

    def play_video():
        webbrowser.open("https://youtu.be/cKHsil0V6Qk?si=-akGHJx7F7lg2LbM") 
    Button(left_p, text="WATCH FK TUTORIAL", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", command=play_video).pack(pady=5)

    joints = []
    for i in range(1, 7):
        f = Frame(left_p, bg=BG_COLOR); f.pack(pady=3, fill=X)
        Label(f, text=f"J{i}:", fg="white", bg=BG_COLOR, font=("Arial", 10, "bold"), width=4).pack(side=LEFT)
        s = Scale(f, from_=-180, to=180, orient=HORIZONTAL, bg="#03265b", fg="white", troughcolor="#f36412", length=180, bd=0)
        s.pack(side=LEFT); joints.append(s)
    
    Button(left_p, text="RUN SIMULATION", bg="#f36412", fg="white", font=("Arial", 12, "bold"), pady=15, 
           command=lambda: update_robot_plot(ax, canvas, joints)).pack(pady=20, fill=X)

    create_manual_box(container, "FK Quick Reference", "1. Watch Video first\n2. Set Angles\n3. Run Simulation")

    right_p = Frame(container, bg="#081b4b", bd=2, relief=RIDGE); right_p.pack(side=RIGHT, expand=True, fill=BOTH, padx=10, pady=20)
    fig = plt.figure(figsize=(9,9)); fig.patch.set_facecolor('#081b4b'); ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=right_p); canvas.get_tk_widget().pack(expand=True, fill=BOTH)
    update_robot_plot(ax, canvas, [0]*6)

#page fiha kol experiments hna
def open_experiments_page():
    for widget in window.winfo_children(): widget.destroy()
    Button(window, text="Back to Main Menu", font=("Arial", 12, "bold"), fg="#f36412", bg=BG_COLOR, bd=0, command=show_welcome_page, borderwidth=10).pack(anchor=NW, padx=20, pady=10)
    Label(window, text="SELECT EXPERIMENT", font=("Helvetica", 30, "bold"), fg="#f39c12", bg=BG_COLOR).pack(pady=20)
    Experiments = [
        ("1. Forward Kinematics (FK)", open_fk_page), 
        ("2. Inverse Kinematics (IK)", open_ik_page), 
        ("3. Trajectory Planning", None), 
        ("4. Pick and Place Control", None),
        ("5. Cup Filling Simulation", None)
    ]
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