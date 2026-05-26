
import sys
import os


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


sys.path.append(resource_path('GUI'))
sys.path.append(resource_path('kinematics'))
sys.path.append(resource_path('simulation'))

try:
    from GUI.main_gui import start_gui
except ImportError:
    from main_gui import start_gui

if __name__ == "__main__":
    start_gui()