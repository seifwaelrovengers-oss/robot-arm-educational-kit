from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulation.plot import update_robot_plot

BG_COLOR = "#04153B"

def open_ik_page(window):
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text="IK PAGE", bg=BG_COLOR, fg="white").pack()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    update_robot_plot(ax, canvas, [0]*6)