import socket

ESP_IP = "192.168.4.1"
ESP_PORT = 80

def send_angles(angles):

    data = ",".join(
        [str(int(a)) for a in angles[:6]]
    ) + "\n"

    try:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(0.01)

        sock.connect(
            (ESP_IP, ESP_PORT)
        )

        sock.send(
            data.encode()
        )

        sock.close()

    except Exception as e:

        print(
            "Connection Error:",
            e
        )