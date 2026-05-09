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

    # El-Zetona: Damegna attempt_login gowa final_step
    def final_step():
        global CURRENT_USER, CURRENT_ID
        name = name_entry.get()
        uid = id_entry.get()
        
        if name and uid:
            CURRENT_USER = name
            CURRENT_ID = uid
            
            # 1. Save data awel ma yedous verify
            save_lab_result("Login System", "Student Verified & Entered Lab")
            
            # 2. El-Rabt bel-page elly ba3d keda
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
    for widget in window.winfo_children(): widget.destroy()
    
    main_frame = Frame(window, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH)

   
    Label(main_frame, text="6-DOF ROBOTIC ARM EDUCATIONAL KIT", 
          font=("Helvetica", 24, "bold"), fg="#099da5", bg=BG_COLOR).place(relx=0.5, rely=0.05, anchor=CENTER)
    Label(main_frame, text="VIRTUAL LAB INTERFACE v1.0", font=("Consolas", 10, "bold"), 
          fg="#efefef", bg=BG_COLOR).place(relx=0.5, rely=0.08, anchor=CENTER)

    # Logo
    try:
        logo_path = r"C:\Users\Bassant\robot-arm-educational-kit\GUI\uni_logo.png"
        logo_img = Image.open(logo_path).resize((110, 110), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        l_lbl = Label(main_frame, image=logo_photo, bg=BG_COLOR)
        l_lbl.image = logo_photo
        l_lbl.place(relx=0.92, rely=0.07, anchor=CENTER)
    except: pass


    text_container = Frame(main_frame, bg=BG_COLOR)
    text_container.place(relx=0.07, rely=0.15, width=500)

    title_txt = "WELCOME TO\nOUR\nVIRTUAL LAB"
    Label(text_container, text=title_txt, font=("Helvetica", 48, "bold"), 
          fg="#050c1f", bg=BG_COLOR, justify=LEFT).place(x=3, y=3)
    Label(text_container, text=title_txt, font=("Helvetica", 48, "bold"), 
          fg="#099da5", bg=BG_COLOR, justify=LEFT).pack(anchor=W)

    desc_text = (
    "Explore robotics through real-time simulation, motion analysis,\n"
    "and live synchronization with a physical 6-DOF robotic arm."
)
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
    glow_frame.place(relx=0.55, rely=0.20, width=520, height=580) # Much larger frame

    try:
        robot_path = os.path.join(os.path.dirname(__file__), "robot_arm.png")
        # Image resize kabbarnah le 480
        r_img = Image.open(robot_path).resize((480, 480), Image.Resampling.LANCZOS)
        r_photo = ImageTk.PhotoImage(r_img)
        robot_lbl = Label(glow_frame, image=r_photo, bg="#14264d")
        robot_lbl.image = r_photo
        robot_lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Animation (Enhanced)
        def animate_robot(angle=0):
            import math
            off_y = math.sin(angle) 
            robot_lbl.place(relx=0.5, rely=0.5, y=off_y, anchor=CENTER)
            window.after(50, lambda: animate_robot(angle + 0.04))
        animate_robot()
    except: pass
        
show_welcome_page()      
window.mainloop()
