import cv2
import os
import time
import csv

attendance = []
def TheMainFunc():
    global attendance
    attendance = []
    lis=[]
# Function to load images and encode faces
    def load_images_and_encode():
        known_face_encodings = []
        known_roll_numbers = []

        # Path to the folder containing student photos
        dataset_path = r"C:\Users\vkpvk\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\attendance\dataset"

        for student_folder in os.listdir(dataset_path):
            student_path = os.path.join(dataset_path, student_folder)
            if os.path.isdir(student_path):
                for image_name in os.listdir(student_path):
                    image_path = os.path.join(student_path, image_name)
                    image = cv2.imread(image_path)
                    face_encoding = encode_face(image)
                    if face_encoding is not None:
                        known_face_encodings.append(face_encoding)
                        known_roll_numbers.append(student_folder)

        return known_face_encodings, known_roll_numbers

    # Function to encode a face using OpenCV Haar Cascade classifier
    def encode_face(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        # Load the Haar Cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            face_roi = gray[y:y + h, x:x + w]
            return cv2.resize(face_roi, (1000, 500))
        else:
            return None

    # Function to recognize faces and mark attendance
    def recognize_faces():
        global attendance
        known_face_encodings, known_roll_numbers = load_images_and_encode()

        cap = cv2.VideoCapture(0)  # Change to the appropriate camera index if not using the default camera

        while True:
            ret, frame = cap.read()

            face_encoding = encode_face(frame)

            if face_encoding is not None:
                # You can use a face recognition algorithm here if needed
            # For simplicity, we're comparing the detected face with known faces using OpenCV's matchTemplate
                match_results = [cv2.matchTemplate(face_encoding, known_face, cv2.TM_CCOEFF_NORMED) for known_face in known_face_encodings]
                best_match_index = int(max(enumerate(match_results), key=lambda x: x[1])[0])

                name = known_roll_numbers[best_match_index]

                cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                if name not in lis:
                    lis.append(name)
            cv2.namedWindow('Face Recognition', cv2.WINDOW_GUI_NORMAL)
            cv2.imshow('Face Recognition', frame)
            cv2.resizeWindow('Face Recognition', 500, 450)
            cv2.moveWindow('Face Recognition', 150, 70)

            if cv2.waitKey(1) & 0xFF == ord('w'):
                attendance=lis
                break

        cap.release()
        cv2.destroyAllWindows()
        print(attendance)

    if __name__ == "__main__":
        recognize_faces()

from tkinter import *
import time
main = Tk()
main.config(background='white')
main.iconbitmap(r"C:\Users\vkpvk\Downloads\blue logo vit.ico")
main.title('VIT')
main.geometry('1000x500+50+50')
main.resizable(False, False)
logo_lbl = Label(main, background='#3b5998', text="", font="Bold 20", fg='white', pady=10)
logo_lbl.place(x=0, y=0, height=70, width=1000)


def get_user():
    user_file = open(r"C:\Users\vkpvk\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\users.txt.txt")
    val = [i.split(":") for i in user_file.read().split(";")]
    return val
loggedin_user = ''
def home():
    global loggedin_user

    def view():
        start_att.place(x=100)
        welcome.place(x=70)
        rec.place(x=50)
        closebtn.place(x=100)
        open_btn.place(x=425)
        o = Listbox(main, font="cursive 20", bd=0, bg="#f1f1f1", fg="black")
        o.place(x=800, y=70, height=400, width=200)
        for i in attendance:
            o.insert(attendance.index(i), i)
        
        def savef():
            global attendance
            with open(r'C:\Users\vkpvk\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\attendance.csv', 'w') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(attendance)
            start_att.place(x=200)
            welcome.place(x=170)
            rec.place(x=150)
            closebtn.place(x=200)
            open_btn.place(x=525) 
            o.destroy()
            save_btn.destroy()   

        
        save_btn = Button(main, text="Save", font="cursive 15", bg="#3b5998", fg="white", bd=0, command=savef)
        save_btn.place(x=800, y=470, height=30, width=200)

    bg = Label(main, background="white")
    bg.place(x=0, y=70, height=430, width=1000)
    start_att = Button(main, text="Take Attendance", bg="green", fg="white", bd=0, font="cursive 30", command=TheMainFunc)
    start_att.place(x=200, y=320, height=70, width=600)
    welcome = Label(main, text="Welcome ", font="cursive 20", bg="white", justify="left")
    welcome.place(x=170, y=100, height=60, width=200)
    rec = Label(main, text='''- To start taking attendance press "q"
                
- To end the attendace press "w"
                
- Make sure to have proper lighting while taking attendance
                
- Students should not wear any face accesories while taking attendance
''', font="cursive 15", fg="#3b5998", bg="white", justify="left")
    rec.place(x=150, y=150, height=140, width=700)
    
    closebtn = Button(main, text="Close", fg="white", bg="red", font="cursive 30", bd=0, command=lambda:main.destroy())
    closebtn.place(x=200, y=400, height=70, width=275)
    open_btn = Button(main, text="Open", fg="white", bg='#3b5998', font="cursive 30", bd=0, command=lambda:view())
    open_btn.place(x=525, y=400, height=70, width=275)

    main.bind('q', TheMainFunc)

def login():
    global loggedin_user
    users = get_user()    
    re = 0
    def auth(r, p):
        global loggedin_user, re
        temp = True
        for i in users:
            if i[0]==r and i[1]==p:
                val.destroy()
                loggedin_user = r
                home()
                temp = False
                break
        if temp == True:
            val.destroy()
            login()
            inco()
            
    val = Frame(main, background='white')
    val.place(x=0, y=70, height=430, width=1000)
    reg_no_l = Label(val, text="Registration number", background='white', font='cursive 15').place(x=370, y=75, height=40, width=200)
    reg_no = Entry(val, background='#f3f3f3', bd=0)
    reg_no.place(x=375, y=110, height=30, width=300)
    pass_l = Label(val, text="Password", background='white', font='cursive 15').place(x=325, y=165, height=40, width=200)
    passn = Entry(val, background='#f3f3f3', bd=0)
    passn.place(x=375, y=200, height=30, width=300)
    log = Button(val, text='Login', background='#28a745', command=lambda:auth(reg_no.get(), passn.get()), bd=0, font='cursive 15', fg="white")
    log.place(x=405, y=270, height=50, width=240)
    sign = Button(val, text="signup->", fg="#3b5998", bg="white", bd=0, command=lambda:signup())
    sign.place(x=430, y=330, height=30, width=200)
    def inco():
        inc = Label(main, text="Incorrect Password", fg="red", bg="white")
        inc.place(x=405, y=80, height=30, width=200)

    def signup():
        t = Tk()
        t.config(bg="white")
        t.geometry("500x320")
        cvr = Label(t, bg="#3b5998")
        cvr.place(x=0, y=0, height=50, width=500)
        reg_no_l_ = Label(t, text="Registration number", background='white', font='cursive 15', justify="left", fg="black")
        reg_no_l_.place(x=95, y=80, height=40, width=200)
        reg_no_ = Entry(t, background='#f3f3f3', bd=0)
        reg_no_.place(x=100, y=115, height=30, width=300)
        pass_l_ = Label(t, text="Enter Password", background='white', font='cursive 15', justify="left", fg="black")
        pass_l_.place(x=75, y=160, height=40, width=200)
        passn_ = Entry(t, background='#f3f3f3', bd=0)
        passn_.place(x=100, y=195, height=30, width=300)
        def add():
            global users
            file = open(r"C:\Users\vkpvk\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\users.txt.txt", "a")
            file.write(reg_no_.get()+":"+passn_.get()+";")
            file.close()
            login()
            t.destroy()
        add_btn = Button(t, text="Signup", bd=0, fg="white", bg="#28a745", command=lambda:add())
        add_btn.place(x=100, y=245, height=30, width=300)



login()
main.mainloop()
