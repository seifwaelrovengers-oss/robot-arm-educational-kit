#Libraries 
from tkinter import *
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
print("libraries are loaded successfully")


window = Tk()
window.title('Robotic Arm Virtual Lab App')
window.state('zoomed') 
BG_COLOR = "#04153B" 
window.configure(bg=BG_COLOR)


def update_robot_plot(ax, canvas, joints):
    ax.clear()
    ax.set_facecolor('#081b4b')
    t = np.linspace(0, 2*np.pi, 50)
    r_base = 1.2
    X_b = r_base * np.cos(t)
    Y_b = r_base * np.sin(t)
    Z_b = np.zeros_like(X_b)
    ax.plot(X_b, Y_b, Z_b, color="#4c7f8f", linewidth=2)
    verts = [list(zip(X_b, Y_b, Z_b))]
    poly = Poly3DCollection(verts, alpha=0.3, facecolor='#1a3a5f')
    ax.add_collection3d(poly)
    angles = [np.radians(j.get()) for j in joints]
    curr_x, curr_y, curr_z = 0, 0, 0
    L = 2 
    for i in range(6):
        prev_pos = [curr_x, curr_y, curr_z]
        
       
        curr_x += L * np.cos(sum(angles[:i+1]))
        curr_y += L * np.sin(sum(angles[:i+1]))
        curr_z += L * np.sin(angles[i]) 
        
        new_pos = [curr_x, curr_y, curr_z]

        
        ax.plot([prev_pos[0], new_pos[0]], 
                [prev_pos[1], new_pos[1]], 
                [prev_pos[2], new_pos[2]], 
                color='#f36412', linewidth=10, solid_capstyle='round')
        
        ax.scatter([curr_x], [curr_y], [curr_z], color='white', s=60, edgecolors='black', zorder=5)

   
    ax.set_xlim([-10, 10]); ax.set_ylim([-10, 10]); ax.set_zlim([0, 10])
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_title("3D ROBOTIC ARM SIMULATION", color='white', fontname="Arial", fontsize=12)
    ax.view_init(elev=25, azim=45)
    canvas.draw()


def open_fk_page():
    for widget in window.winfo_children():
        widget.destroy()
        
   
    Button(window, text="← Back to Experiments", font=("Arial", 12, "bold"), fg="#f36412", 
           bg=BG_COLOR, bd=0, cursor="hand2", command=open_experiments_page, borderwidth=5).pack(anchor=NW, padx=20, pady=10)

    container = Frame(window, bg=BG_COLOR)
    container.pack(expand=True, fill=BOTH, padx=30)

    
    left_p = Frame(container, bg=BG_COLOR)
    left_p.pack(side=LEFT, fill=Y, padx=20)
    
    Label(left_p, text="JOINT CONTROL", font=("Helvetica", 20, "bold"), fg="#f39c12", bg=BG_COLOR).pack(pady=10)   
    joints_list = []
    for i in range(1, 7):
        f = Frame(left_p, bg=BG_COLOR)
        f.pack(pady=5, fill=X)
        Label(f, text=f"Joint {i}:", fg="white", bg=BG_COLOR, font=("Arial", 10, "bold"), width=8, anchor=W).pack(side=LEFT)
        s = Scale(f, from_=-180, to=180, orient=HORIZONTAL, bg="#03265b", fg="white", troughcolor="#f36412", length=200, bd=0)
        s.set(0)
        s.pack(side=LEFT)
        joints_list.append(s)

    
    right_p = Frame(container, bg="#081b4b", bd=2, relief=RIDGE)
    right_p.pack(side=RIGHT, expand=True, fill=BOTH, padx=20, pady=20)

    fig = plt.figure(figsize=(5,5))
    fig.patch.set_facecolor('#081b4b')
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=right_p)
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)

   
    Button(left_p, text="RUN SIMULATION", bg="#f36412", fg="white", font=("Arial", 14, "bold"),
           pady=15, cursor="hand2", command=lambda: update_robot_plot(ax, canvas, joints_list)).pack(pady=20, fill=X)


def open_experiments_page():
    for widget in window.winfo_children():
        widget.destroy()
    
    Button(window, text="← Back to Main Menu", font=("Arial", 12, "bold"), fg="#f36412", 
           bg=BG_COLOR, bd=0, cursor="hand2", command=show_welcome_page, borderwidth=5).pack(anchor=NW, padx=20, pady=10)

    Label(window, text="SELECT YOUR EXPERIMENT", font=("Helvetica", 30, "bold"), fg="#f39c12", bg=BG_COLOR).pack(pady=20)

    btn1 = Button(window, text="1. Forward Kinematics (FK)", font=("Arial", 16), fg="white", bg="#03265b", width=35, pady=15, cursor="hand2", command=open_fk_page, borderwidth=5)
    btn1.pack(pady=30)
    btn2 = Button(window, text="2. Inverse Kinematics (IK)", font=("Arial", 16), fg="white", bg="#03265b", width=35, pady=15, cursor="hand2", borderwidth=5)
    btn2.pack(pady=30)
    btn3 = Button(window, text="3. Trajectory Planning", font=("Arial", 16), fg="white", bg="#03265b", width=35, pady=15, cursor="hand2",borderwidth=5)
    btn3.pack(pady=30)
    btn4 = Button(window, text="4. Pick and Place Control", font=("Arial", 16), fg="white", bg="#03265b", width=35, pady=15, cursor="hand2",borderwidth=5)
    btn4.pack(pady=30)


def show_welcome_page():
    for widget in window.winfo_children():
        widget.destroy()

    left_container = Frame(window, bg=BG_COLOR)
    left_container.pack(side=LEFT, expand=True, fill=BOTH, padx=80)
    right_container = Frame(window, bg=BG_COLOR)
    right_container.pack(side=RIGHT, expand=True, fill=BOTH)

    Label(left_container, text="WELCOME TO OUR VIRTUAL LAB", font=("Helvetica", 35, "bold"), 
          fg="#f36412", bg=BG_COLOR, justify=LEFT).pack(pady=(120, 20), anchor=W)

    intro_text = (
        "This Virtual Lab provides an integrated environment to simulate and analyze 4 distinct robotic experiments. "
        "It allows you to explore robotic kinematics and trajectory planning in a 3D simulation. "
        "Finally, you can bridge the gap between virtual and reality by connecting your ESP32 kit to synchronize and "
        "observe the real-time motion of the physical robotic arm."
    )
    Label(left_container, text=intro_text, font=("Times New Roman", 14, "bold"), 
          fg="#70afc2", bg=BG_COLOR, justify=LEFT, wraplength=600).pack(pady=10, anchor=W)

    how_to_use = (
        "How to use this lab:\n"
        "1. Click the button below to start.\n"
        "2. Select your desired experiment.\n"
        "3. Observe the 3D simulation in real-time.\n"
        "4. Connect your ESP32 kit to sync motion!"
    )
    Label(left_container, text=how_to_use, font=("Arial", 13), fg="white", bg=BG_COLOR, justify=LEFT).pack(pady=20, anchor=W)

    Button(left_container, text='ENTER THE LAB', bg='#f36412', fg='white', 
                    font=('Arial', 14, 'bold'), padx=40, pady=20, bd=0, cursor="hand2",
                    command=open_experiments_page).pack(pady=30, anchor=W)

    try:
        current_folder = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_folder, "robot_arm.png")
        if os.path.exists(img_path):
            img_open = Image.open(img_path).resize((600, 600))
            img_final = ImageTk.PhotoImage(img_open)
            image_label = Label(right_container, image=img_final, bg=BG_COLOR)
            image_label.image = img_final
            image_label.pack(expand=True)
    except: pass

show_welcome_page()
window.mainloop()