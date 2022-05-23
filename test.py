
######## Importing modules for Tkinter ###########
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

######## Importing modules for mediapipe ############
import cv2
import numpy as np
import time
import PoseModule as PM


########### Accessing Video ###########

def camselect(cam=1, file1=NONE):
    global cap

    if cam:
        cap = cv2.VideoCapture(0)

    else:
        cap = cv2.VideoCapture(file1)


camselect()

detector = PM.PoseDetector()


ptime = 0  # variable for fps


def test2():
    global ptime

    success, img = cap.read()

    # img = cv2.imread('assets/dab.jpg')
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (990, 640))  # width, height

    img = detector.findPose(img, False)
    lmlist = detector.findPosition(img, False)

    ###### main processing ######
    if len(lmlist) != 0:


        RightShoulder = detector.findAngle(img, 13, 11, 23, False)
        RightHip = detector.findAngle(img, 25, 23, 11, False)


        pArm=0
        pShoulder=0
        pHip=0
        pKnee=0


        if RightHip > 200 and RightShoulder > 250:

            ########## code for Left Side #############

            LeftArm = detector.findAngle(img, 16, 14, 12)
            LeftShoulder = detector.findAngle(img, 24, 12, 14)
            LeftHip = detector.findAngle(img, 12, 24, 26)
            LeftKnee = detector.findAngle(img, 24, 26, 28)

            ########## percentages ###########
            pArm = np.interp(LeftArm, (20, 185), (0, 200))
            pShoulder = np.interp(LeftShoulder, (15, 140), (100, 0))
            pHip = np.interp(LeftHip, (100, 180), (200, 50))
            pKnee = np.interp(LeftKnee, (20, 190), (0, 100))


            
            cv2.putText(img, 'Left Cobra Pose', (20, 500),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        else:

            ################ code for Right Side #######################

            RightArm = detector.findAngle(img, 11, 13, 15)
            RightShoulder = detector.findAngle(img, 13, 11, 23)
            RightHip = detector.findAngle(img, 25, 23, 11)
            RightKnee = detector.findAngle(img, 27, 25, 23)

            ########## percentages ###########

            pArm = np.interp(RightArm, (20, 185), (0, 200))
            pShoulder = np.interp(RightShoulder, (15, 140), (100, 0))
            pHip = np.interp(RightHip, (100, 180), (200, 50))
            pKnee = np.interp(RightKnee, (20, 190), (0, 100))


            cv2.putText(img, 'Right Cobra Pose', (20, 500),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        # print(pArm, pShoulder, pHip, pKnee)

        total = pArm+pShoulder+pHip+pKnee
        ptotal = np.interp(total, (0, 600), (0, 100))
        cv2.putText(img, f'{str(int(ptotal))}%', (850, 100),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

        # print(ptotal)

        if ptotal < 50:

            ackText = 'Very Poor'

        elif ptotal < 75:

            ackText = 'Almost There'

        else:

            ackText = 'YAY ! Youv\'e got it'

        cv2.putText(img, ackText, (20, 200),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    else:
        cv2.putText(img, 'Come on D33r! Do the Pose', (30, 400),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 0), 4)

    ########## fps calculation ########
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS = {str(int(fps))}', (20, 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)

    cv2.putText(img, ' COPYRIGHT CLAIMS BY ABDUREHMAN ASIF ', (300, 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 2)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return rgb


################################### Tkinter Code ##########################################


def openvid():
    file1 = filedialog.askopenfilename()
    cam = 0
    camselect(cam, file1)


def openV1():  # code for opening first video
    file1 = 'assets/video2.mp4'
    cam = 0
    camselect(cam, file1)


def camvideo():
    cam = 1
    camselect(cam)


def close():
    window.destroy()




# Window Creation
window = Tk()
window.configure(bg='black')
window.title("Cobra Pose")
width = window.winfo_screenwidth()+10
height = window.winfo_screenheight()+10
window.geometry("%dx%d" % (width, height))
window.minsize(width, height)
window.maxsize(width, height)


################ Design ################
mainlabel = Label(window, text="Cobra Pose Program", font=(
    "Raleway", 20, "bold", "italic"), bg="#e7e6d1", fg='blue')
mainlabel.pack()


f1 = Frame(window, bg='green')
f1.pack(side=LEFT, fill='y', anchor='nw')

explore = Button(f1, text="Browse Video", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=openvid).pack(padx=50)

livecam = Button(f1, text="Open Web Cam", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=camvideo).pack()

v1 = Button(f1, text="Test Video 1", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=openV1).pack(padx=50)


Exit_Application = Button(f1, text="Exit the Application", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=close).pack(pady=200)


############### Video Player #######################


label1 = Label(window, width=960, height=640)
label1.place(x=240, y=50)


def select_img():
    image = Image.fromarray(test2())
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    window.after(1, select_img)


select_img()


window.mainloop()
