from tensorflow.keras.models import load_model
import cv2
import os
import pickle
import numpy as np
import pickle
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from keras_vggface import utils

model = load_model('Cbl\model\_face_cnn_model2.h5')

image_width = 224
image_height = 224

face_label_filename = 'Cbl\model\cface-labels1.pickle'
with open(face_label_filename, "rb") as \
    f: class_dictionary = pickle.load(f)

class_list = [value for _, value in class_dictionary.items()]
print(class_list)

facecascade = cv2.CascadeClassifier(
    'Cbl\haarcascade_frontalface_default.xml')

for i in range(1,4): 
    test_image_filename = f'Cbl\datatest/face{i}.jpg'

    imgtest = cv2.imread(test_image_filename, cv2.IMREAD_COLOR)
    image_array = np.array(imgtest, "uint8")

    faces = facecascade.detectMultiScale(imgtest, 
        scaleFactor=1.1, minNeighbors=5)

    if len(faces) != 1: 
        print(f'---We need exactly 1 face; photo skipped---')
        print()
        continue

    for (x_, y_, w, h) in faces:
        
        size = (image_width, image_height)
        roi = image_array[y_: y_ + h, x_: x_ + w]
        resized_image = cv2.resize(roi, size)

        x = image.img_to_array(resized_image)
        x = np.expand_dims(x, axis=0)
        x = utils.preprocess_input(x, version=1)

        predicted_prob = model.predict(x)
        font = cv2.FONT_HERSHEY_SIMPLEX
        face_detect = cv2.rectangle(
        imgtest, (x_, y_), (x_+w, y_+h), (255, 0, 255), 2)
        cv2.putText(face_detect, f'({class_list[predicted_prob[0].argmax()]})', (x_,y_-8),font, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(face_detect, f'({predicted_prob[0].max()*100})', (x_,y_+h-8),font, 1, (255, 0, 255), 1, cv2.LINE_AA)
        plt.imshow(face_detect)
        plt.show()
