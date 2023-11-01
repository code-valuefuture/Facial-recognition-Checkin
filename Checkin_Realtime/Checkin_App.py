######
#imort thư viện, model, label
######

from PIL import Image as pilimg
import numpy as np
import cv2
import pickle
from date import CurrentDate
from PIL import ImageTk
from excel import Export, append_to_excel
from tensorflow.keras.models import load_model
import tkinter as tk
from tkinter import *
from Lib import threading 
from Lib.threading import Lock
import time as time_out
from tkinter import filedialog
from keras_vggface import utils
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image as proimg


# tải model detect
face_cascade = cv2.CascadeClassifier(
    'Cbl\haarcascade_eye.xml')

# tải model nhạn diện khuôn mặt
model = load_model('Cbl\model\_face_cnn_model2.h5')

# tải 
with open("Cbl\model\cface-labels1.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {key:value for key,value in og_labels.items()}
    print(labels)

#########
# Chương trình check
########

root = Tk()
root.title('Attendance app')
root.iconbitmap('Cbl\pic_app\icon.jpg')
root.geometry('890x500')
root.resizable(False,False)
imgBackgroundLogin = ImageTk.PhotoImage(pilimg.open('Cbl\pic_app\main.jpg'))
panel = Label(root, image = imgBackgroundLogin)
panel.image = imgBackgroundLogin
panel.place(x = 0, y = 0)

fontTypeApp = 'Times New Roman'

image_width = 224
image_height = 224

def checkvar():
    root.destroy()
    cameraOptionScreen = Tk()
    cameraOptionScreen.geometry('730x300')## set kthc man hinh
    cameraOptionScreen.configure(bg = 'CornflowerBlue')
    
    global optionCamera, cap, latestFrame, lo, lastRet
    optionCamera = ''
    cap = cv2.VideoCapture(0)
    cap.set(3, 640) 
    cap.set(4, 480) 
    latestFrame = None
    lastRet = None
    lo = Lock()
    def rtspProtocolbuffer(cap):
        global latestFrame, lo, lastRet
        while True:
            with lo:
                try:
                    lastRet, latestFrame = cap.read()
                except:
                    print('error exception')
    t1 = threading.Thread(target = rtspProtocolbuffer, args = (cap,), name = 'rtsp_read_thread')
    t1.daemon = True
    t1.start()

    cameraOptionScreen.destroy()
    mainAppScreen = Tk()
    mainAppScreen.geometry('1200x600') #Kthc cửa sổ 
    mainAppScreen.resizable(False,False)
    background_main=ImageTk.PhotoImage(pilimg.open('Cbl\pic_app\cackground.jpg'))
    panel = Label(mainAppScreen, image = background_main)
    panel.image = background_main
    panel.place(x = 0, y = 0)

    lableShowFace = Label(mainAppScreen)
    lableShowFace.place(x = 0, y = 0)
    def showFaceStream():
        try:
            global faceStream
            if((optionCamera.isnumeric and len(optionCamera)==1) or len(optionCamera)==0):
                _,faceStream = cap.read()
            else:
                faceStream = latestFrame.copy()
            # faceStream = cv2.flip(faceStream,1)
            imageStream = cv2.cvtColor(faceStream, cv2.COLOR_BGR2RGBA)
            imgFace = pilimg.fromarray(imageStream)
            imgShowFace = ImageTk.PhotoImage(image = imgFace)
            lableShowFace.imgShowFace = imgShowFace
            lableShowFace.configure(image = imgShowFace)
            lableShowFace.after(10, showFaceStream)
        except:
            print('error exception')
    showFaceStream()
    
    def attendanceRealtimeFunc():
        global imgRealtime
        take= False
        while True:
            if((lastRet is not None) and (latestFrame is not None)):
                faceStream = latestFrame.copy()
            else:
                print('Not take of video')
                time_out.sleep(0.2)
                continue

            gray = cv2.cvtColor(faceStream,cv2.IMREAD_COLOR)
            image_array = np.array(gray, "uint8")
            today, currentTime, startMorning, endMorning, startAfternoon, endAfternoon = CurrentDate.dateHourTimeAttendance()

            checkid=[]
            checkname=[]
            checkdate=[]
            checktime=[]
            faces = face_cascade.detectMultiScale( 
                gray,
                scaleFactor = 1.1,
                minNeighbors = 5,
            )

            for(x,y,w,h) in faces:
                size = (image_width, image_height)
                roi = image_array[y: y + h, x: x + w]
                resized_image = cv2.resize(roi, size)

                x1 = proimg.img_to_array(resized_image)
                x1 = np.expand_dims(x1, axis=0)
                x1 = utils.preprocess_input(x1, version=1)
                
                predicted_prob = model.predict(x1)
                confidence= predicted_prob[0].max()*100
                id= predicted_prob[0].argmax()
                print(confidence,'   ')
                
                if (confidence >30):
                    name = labels[id]
                else:
                    name = "unknown"
                # print(confidence,name)
                # lưu dữ liệu
                if(name!= "unknown"): # kiểm tra khuôn mặt đã được nhận dạng
                    checkid.append(str(id))
                    checkname.append(str(name))
                    checkdate.append(str(today))
                    checktime.append(str(currentTime))
                
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.rectangle(faceStream, (x,y), (x+w,y+h), (255, 0, 255), 2)
                cv2.putText(faceStream, f'({name})', (x,y-8),font, 1, (255, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(faceStream, f'({confidence})', (x,y+h-8),font, 1, (255, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('cam',faceStream) 
            
            if len(checkid)>0 and take== False:
                fileName = 'Cbl\checkinlist\checkin.xls'
                # print(checkid,checkname,checktime)
                append_to_excel(checkid, checkname,checkdate,checktime,fileName)
                take= True

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        print("\n [INFO] Exiting Program and cleanup stuff")
        # cap.release()
        cv2.destroyAllWindows()
    # Cài giao diện checkcamera
    buttonAttendanceRealtime = Button(mainAppScreen, text = 'Checkin', font = (fontTypeApp, 14), fg = 'white', bg = 'red',
        width = 18, height = 1, command = attendanceRealtimeFunc)
    buttonAttendanceRealtime.place(x = 10, y = 500)


def checkimg():
    root.destroy()
    cameraOptionScreen = Tk()
    cameraOptionScreen.geometry('430x450')## set kthc man hinh
    cameraOptionScreen.configure(bg = 'brown')
    
    def loadimg():
        file_path = filedialog.askopenfilename()
        
        img = pilimg.open(file_path)
        image= img
        max_width = 400
        if image.width > max_width:
            ratio = max_width / image.width
            new_height = int(image.height * ratio)
            image = image.resize((max_width, new_height))
        
        # Display the image on a canvas
        canvas.delete("all")  # Clear previous image
        img_tk = ImageTk.PhotoImage(image)
        canvas.create_image(10, 100, anchor='nw', image=img_tk)
        canvas.image = img_tk

        # load the image
        imgtest = cv2.imread(file_path, cv2.IMREAD_COLOR)
        image_array = np.array(imgtest, "uint8")

        # get the faces detected in the image
        faces = face_cascade.detectMultiScale(imgtest, 
            scaleFactor=1.1, minNeighbors=5)
        
        today, currentTime, startMorning, endMorning, startAfternoon, endAfternoon = CurrentDate.dateHourTimeAttendance()
        checkid=[]
        checkname=[]
        checkdate=[]
        checktime=[]
        take= False
        for (x_, y_, w, h) in faces:

            size = (image_width, image_height)
            roi = image_array[y_: y_ + h, x_: x_ + w]
            resized_image = cv2.resize(roi, size)

            x = proimg.img_to_array(resized_image)
            x = np.expand_dims(x, axis=0)
            x = utils.preprocess_input(x, version=1)

            predicted_prob = model.predict(x)
            
            confidence= predicted_prob[0].max()*100
            id= predicted_prob[0].argmax()
            print(confidence,'   ')
            
            if (confidence >30):
                name = labels[id]
            else:
                name = "unknown"
            # lưu dữ liệu
            if(name!= "unknown"): # kiểm tra khuôn mặt đã được nhận dạng
                checkid.append(str(id))
                checkname.append(str(name))
                checkdate.append(str(today))
                checktime.append(str(currentTime))
            
            # print(predicted_prob) # trả về mảng chứa xác suất từng nhãn
            print( predicted_prob[0].max()*100) # TRả về vị trí có xác suất lớn nhất
            print("Predicted face: " + labels[predicted_prob[0].argmax()])
            
            oke= Tk()
            oke.geometry('230x40')## set kthc man hinh
            oke.configure(bg = 'CornflowerBlue')
            label_title = Label(oke, text="Checkin thành công", font=(fontTypeApp, 20), fg="red", width=15, justify="center")
            label_title.place(relx=0.5, rely=0.5, anchor="center")
            # Đặt thời gian chờ 3000ms (3 giây) trước khi đóng cửa sổ
            def close_window():
                oke.destroy()
            oke.after(2000, close_window)

            face_detect = cv2.rectangle(imgtest, (x_, y_), (x_+w, y_+h), (255, 0, 255), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(face_detect, f'({name})', (x_,y_-8),font, 1, (255, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(face_detect, f'({confidence})', (x_,y_+h-8),font, 1, (255, 0, 255), 1, cv2.LINE_AA)
            plt.imshow(face_detect)
            plt.show()
        
        if len(checkid)>0 and take== False:
            fileName = 'Cbl\checkinlist\checkin.xls'
            # print(checkid,checkname,checktime)
            append_to_excel(checkid, checkname,checkdate,checktime,fileName)
            take= True

    # Cài giao diện checkimg
    canvas = Canvas(cameraOptionScreen, width=400, height=300, bg='white') # width= max_width, height= max_height
    canvas.place(x=10, y=100)
    
    lableOptionCamera = Label(cameraOptionScreen, text = 'Tải ảnh để check', font = (fontTypeApp, 18), fg = 'orange', bg = 'white')
    lableOptionCamera.place(x = 10, y = 10)
    buttonOptionCamera = Button(cameraOptionScreen, text = 'Tải lên', font = (fontTypeApp,14),fg = 'white', bg = 'red',
                width = 15, height = 1, bd = 2, command = loadimg)  
    buttonOptionCamera.place(x = 10, y = 60)
#cài giao diện trang chủ
label_title = Label(root, text="Checkin App", font=(fontTypeApp, 40), fg="orange", width=10, justify="center", bg = 'white')
label_title.place(relx=0.5, rely=0.3, anchor="center")
buttonLogin = Button(root, text='Checkin bằng camera', font = (fontTypeApp, 14), fg = 'purple', bg = 'red',
    width = 20, height = 1, bd = 4,command = checkvar)
buttonLogin.place(x = 540, y = 320)

buttonpic = Button(root, text='Checkin bằng hình ảnh', font = (fontTypeApp, 14), fg = 'purple', bg = 'red',
    width = 20, height = 1, bd = 4,command = checkimg)
buttonpic.place(x = 140, y = 320)
root.mainloop()
