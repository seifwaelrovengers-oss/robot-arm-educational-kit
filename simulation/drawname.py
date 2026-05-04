def run_draw():
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    import pybullet as p
    import pybullet_data
    import time
    import numpy as np

    # ===== DIGITAL TWIN SAFE =====
    try:
        from api.esp_api import send_angles
    except:
        def send_angles(x):
            print("SIM:", x)

    # ===== INIT =====
    if p.isConnected():
        p.disconnect()

    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-9.8)

    robot = p.loadURDF("kuka_iiwa/model.urdf",[0,0,0],useFixedBase=True)

    end_effector = 6

    DRAW_Z = 0.22
    MOVE_Z = 0.35

    last_sent = None
    path_points = []

    # ===== LINE =====
    def line(a,b):
        pts=[]
        for i in range(40):
            t=i/40
            x=a[0]+(b[0]-a[0])*t
            y=a[1]+(b[1]-a[1])*t
            pts.append([x,y,DRAW_Z])
        return pts

    # ===== BEZIER =====
    def bezier(p0,p1,p2,p3,steps=50):
        pts=[]
        for i in range(steps+1):
            t=i/steps
            x=(1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0]
            y=(1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]
            pts.append([x,y,DRAW_Z])
        return pts

    # ===== FOLLOW =====
    def follow_path(path):
        nonlocal last_sent, path_points

        if not path:
            return

        for target in path:
            joint_target = p.calculateInverseKinematics(robot, end_effector, target)

            for _ in range(4):
                for j in range(7):
                    p.setJointMotorControl2(
                        robot,
                        j,
                        p.POSITION_CONTROL,
                        targetPosition=joint_target[j],
                        force=1500
                    )

                angles=[int(np.degrees(a)) for a in joint_target[:6]]
                if angles!=last_sent:
                    send_angles(angles)
                    last_sent=angles

                pos=p.getLinkState(robot,end_effector)[0]

                if len(path_points)>0:
                    p.addUserDebugLine(path_points[-1],pos,[0,1,0],3,lifeTime=0)

                path_points.append(pos)

                p.stepSimulation()
                time.sleep(1/240)

    # ===== PEN =====
    def pen_move(p):
        follow_path([[p[0],p[1],MOVE_Z],[p[0],p[1],DRAW_Z]])

    # ===== LETTERS =====
    def draw_letter(ch,offset):

        h=0.3
        w=0.2

        def P(x,y): return [offset+x,y]

        path=[]

        # ===== ALL LETTERS =====

        if ch=="A":
            path+=line(P(0,-h),P(w/2,h))
            path+=line(P(w,-h),P(w/2,h))
            path+=line(P(w*0.25,0),P(w*0.75,0))

        elif ch=="B":
            path+=line(P(0,-h),P(0,h))
            path+=bezier(P(0,h),P(w,h/2),P(w,0),P(0,0))
            path+=bezier(P(0,0),P(w,0),P(w,-h/2),P(0,-h))

        elif ch=="C":
            path+=bezier(P(w,h),P(0,h),P(0,-h),P(w,-h))

        elif ch=="D":
            path+=line(P(0,-h),P(0,h))
            path+=bezier(P(0,h),P(w,h/2),P(w,-h/2),P(0,-h))

        elif ch=="E":
            path+=line(P(0,h),P(0,-h))
            path+=line(P(0,h),P(w,h))
            path+=line(P(0,0),P(w*0.7,0))
            path+=line(P(0,-h),P(w,-h))

        elif ch=="F":
            path+=line(P(0,h),P(0,-h))
            path+=line(P(0,h),P(w,h))
            path+=line(P(0,0),P(w*0.7,0))

        elif ch=="G":
            path+=bezier(P(w,h),P(0,h),P(0,-h),P(w,-h))
            path+=line(P(w,-h),P(w*0.5,0))

        elif ch=="H":
            path+=line(P(0,h),P(0,-h))
            path+=line(P(w,h),P(w,-h))
            path+=line(P(0,0),P(w,0))

        elif ch=="I":
            path+=line(P(w/2,h),P(w/2,-h))

        elif ch=="J":
            path+=bezier(P(w,h),P(w,-h),P(0,-h),P(0,-h/2))

        elif ch=="K":
            path+=line(P(0,h),P(0,-h))
            path+=line(P(0,0),P(w,h))
            path+=line(P(0,0),P(w,-h))

        elif ch=="L":
            path+=line(P(0,h),P(0,-h))
            path+=line(P(0,-h),P(w,-h))

        elif ch=="M":
            path+=line(P(0,-h),P(0,h))
            path+=line(P(0,h),P(w/2,0))
            path+=line(P(w/2,0),P(w,h))
            path+=line(P(w,h),P(w,-h))

        elif ch=="N":
            path+=line(P(0,-h),P(0,h))
            path+=line(P(0,h),P(w,-h))
            path+=line(P(w,-h),P(w,h))

        elif ch=="O":
            path+=bezier(P(0,h),P(w,h),P(w,-h),P(0,-h))
            path+=bezier(P(0,-h),P(-w,-h),P(-w,h),P(0,h))

        elif ch=="P":
            path+=line(P(0,-h),P(0,h))
            path+=bezier(P(0,h),P(w,h/2),P(w,0),P(0,0))

        elif ch=="Q":
            path+=bezier(P(0,h),P(w,h),P(w,-h),P(0,-h))
            path+=line(P(w*0.5,-h),P(w,h))

        elif ch=="R":
            path+=line(P(0,-h),P(0,h))
            path+=bezier(P(0,h),P(w,h/2),P(w,0),P(0,0))
            path+=line(P(0,0),P(w,-h))

        elif ch=="S":
            path+=bezier(P(w,h),P(0,h),P(0,0),P(w,0))
            path+=bezier(P(w,0),P(w,0),P(w,-h),P(0,-h))

        elif ch=="T":
            path+=line(P(0,h),P(w,h))
            path+=line(P(w/2,h),P(w/2,-h))

        elif ch=="U":
            path+=bezier(P(0,h),P(0,-h),P(w,-h),P(w,h))

        elif ch=="V":
            path+=line(P(0,h),P(w/2,-h))
            path+=line(P(w,h),P(w/2,-h))

        elif ch=="W":
            path+=line(P(0,h),P(w*0.25,-h))
            path+=line(P(w*0.25,-h),P(w*0.5,0))
            path+=line(P(w*0.5,0),P(w*0.75,-h))
            path+=line(P(w*0.75,-h),P(w,h))

        elif ch=="X":
            path+=line(P(0,h),P(w,-h))
            path+=line(P(w,h),P(0,-h))

        elif ch=="Y":
            path+=line(P(0,h),P(w/2,0))
            path+=line(P(w,h),P(w/2,0))
            path+=line(P(w/2,0),P(w/2,-h))

        elif ch=="Z":
            path+=line(P(0,h),P(w,h))
            path+=line(P(w,h),P(0,-h))
            path+=line(P(0,-h),P(w,-h))

        else:
            print(f"Letter {ch} not supported ❌")
            return

        follow_path(path)

    # ===== DRAW NAME =====
    def draw_name(name):
        nonlocal path_points
        path_points=[]

        offset=0

        for ch in name:
            pen_move([offset,0])
            draw_letter(ch,offset)
            offset+=0.35

    # ===== START =====
    name=input("Enter Name: ").upper()
    draw_name(name)

    # ===== LOOP =====
    while True:
        p.stepSimulation()
        time.sleep(1/240)


if __name__ == "__main__":
    run_draw()