from tkinter import *
from gui.fk_page import open_fk_page
from gui.ik_page import open_ik_page

BG_COLOR = "#04153B"

def start_gui():
    window = Tk()
    window.title("Robot Lab")
    window.state("zoomed")
    window.configure(bg=BG_COLOR)

    def open_menu():
        for w in window.winfo_children():
            w.destroy()

        Button(window, text="Forward Kinematics",
               command=lambda: open_fk_page(window)).pack(pady=20)

        Button(window, text="Inverse Kinematics",
               command=lambda: open_ik_page(window)).pack(pady=20)

    Button(window, text="ENTER LAB", command=open_menu).pack(pady=100)

    window.mainloop()