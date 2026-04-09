from tkinter import *
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulation.plot import update_robot_plot

BG_COLOR = "#04153B"

def open_fk_page(window):
    for widget in window.winfo_children():
        widget.destroy()

    container = Frame(window, bg=BG_COLOR)
    container.pack(expand=True, fill=BOTH)

    left = Frame(container, bg=BG_COLOR)
    left.pack(side=LEFT, fill=Y, padx=10)

    Label(left, text="FK CONTROL", fg="white", bg=BG_COLOR).pack()

    joints = []
    for i in range(6):
        s = Scale(left, from_=-180, to=180, orient=HORIZONTAL)
        s.pack()
        joints.append(s)

    def play_video():
        webbrowser.open("https://youtu.be/cKHsil0V6Qk")

    Button(left, text="Tutorial", command=play_video).pack()

    Button(left, text="Run",
           command=lambda: update_robot_plot(ax, canvas, joints)).pack()

    right = Frame(container)
    right.pack(side=RIGHT, expand=True, fill=BOTH)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=right)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    update_robot_plot(ax, canvas, [0]*6)