from flask import Flask, request, render_template_string
import socket

app = Flask(__name__)

ESP_IP = "192.168.4.1"
ESP_PORT = 80


def send_to_esp(vals):

    data = ",".join(
        str(int(v))
        for v in vals
    ) + "\n"

    try:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(0.5)

        sock.connect(
            (ESP_IP, ESP_PORT)
        )

        sock.sendall(
            data.encode()
        )

        sock.close()

        print("Sent:", data.strip())

    except Exception as e:
        print("ESP Connection Error:", e)


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Robot Arm</title>

    <style>
        body{
            font-family:Arial;
            text-align:center;
            margin-top:20px;
        }

        input{
            width:80px;
            margin:6px;
            font-size:18px;
        }

        button{
            font-size:20px;
            padding:10px 20px;
            margin-top:15px;
        }
    </style>
</head>

<body>

<h2>Robot Arm Control</h2>

<form method="POST">

Base:
<input name="base" value="135"><br>

Shoulder:
<input name="shoulder" value="90"><br>

Elbow:
<input name="elbow" value="90"><br>

Wrist:
<input name="wrist" value="90"><br>


Roll:
<input name="roll" value="180"><br>

Yaw:
<input name="yaw" value="90"><br>

Gripper:
<input name="gripper" value="90"><br>

<button type="submit">APPLY</button>

</form>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        vals = [

            int(request.form["base"]),
            int(request.form["roll"]),
            int(request.form["shoulder"]),
            int(request.form["elbow"]),
            int(request.form["wrist"]),
            int(request.form["yaw"]),
            int(request.form["gripper"]),
        ]

        send_to_esp(vals)

    return render_template_string(HTML)


@app.route("/test")
def test():
    return "OK"


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )