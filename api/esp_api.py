import socket


# =========================
# ESP32
# =========================
ESP_IP = "192.168.4.1"
ESP_PORT = 80


# =========================
# Twin mapped
# =========================
TWIN_IP = "127.0.0.1"
TWIN_PORT = 5005


# =========================
# Twin raw
# =========================
RAW_TWIN_IP = "127.0.0.1"
RAW_TWIN_PORT = 5006


# =========================
# Clamp
# =========================
def clamp(v, mn, mx):

    return max(
        mn,
        min(mx, v)
    )


# =========================
# Servo mapping
# =========================
def map_angles(angles):

    if len(angles) < 7:

        angles = list(angles)

        while len(angles) < 7:

            angles.append(90)

    base = clamp(
        angles[0],
        -135,
        135
    )

    shoulder = clamp(
        angles[1],
        0,
        180
    )

    elbow = clamp(
        angles[2],
        -80,
        90
    )

    wrist = clamp(
        angles[3],
        -90,
        90
    )

    roll = clamp(
        angles[4],
        -180,
        180
    )

    yaw = clamp(
        angles[5],
        0,
        180
    )

    gripper = clamp(
        angles[6],
        0,
        180
    )

    # convert to positive
    stepper_base = int(
        base + 135
    )

    stepper_roll = int(
        roll + 180
    )

    servo_shoulder = int(
        shoulder
    )

    servo_elbow = int(
        elbow + 80
    )

    servo_wrist = int(
        wrist + 90
    )

    servo_yaw = int(
        yaw
    )

    servo_gripper = int(
        gripper
    )

    return [

        stepper_base,

        stepper_roll,

        servo_shoulder,

        servo_elbow,

        servo_wrist,

        servo_yaw,

        servo_gripper
    ]


# =========================
# Send
# =========================
def send_angles(angles):

    mapped_vals = map_angles(
        angles
    )

    mapped_data = ",".join(

        str(int(v))

        for v in mapped_vals

    ) + "\n"

    raw_data = ",".join(

        str(float(v))

        for v in angles

    ) + "\n"

    # =====================
    # ESP32
    # =====================
    try:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(
            0.3
        )

        sock.connect(
            (
                ESP_IP,
                ESP_PORT
            )
        )

        sock.sendall(
            mapped_data.encode()
        )

        sock.close()

    except Exception as e:

        print(
            "ESP Connection Error:",
            e
        )

    # =====================
    # mapped twin
    # =====================
    try:

        twin_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        twin_sock.sendto(

            mapped_data.encode(),

            (
                TWIN_IP,
                TWIN_PORT
            )
        )

        twin_sock.close()

    except:
        pass

    # =====================
    # raw twin
    # =====================
    try:

        raw_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        raw_sock.sendto(

            raw_data.encode(),

            (
                RAW_TWIN_IP,
                RAW_TWIN_PORT
            )
        )

        raw_sock.close()

    except:
        pass