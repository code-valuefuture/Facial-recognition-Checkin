import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Dense, GlobalAveragePooling2D, Flatten

from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.layers import Input
from keras.preprocessing.image import ImageDataGenerator

from keras.models import Model

from keras.optimizers import Adam

# Tăng cường hình ảnh
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input)

train_generator = \
    train_datagen.flow_from_directory(
'Headshots',
target_size=(224,224),
color_mode='rgb',
batch_size=32,
class_mode='categorical',
shuffle=True)

train_generator.class_indices.values()
# dict_values([0, 1, 2])
NO_CLASSES = len(train_generator.class_indices.values())

print('aaa',NO_CLASSES)

# Xây dựng mô hình
from keras_vggface.vggface import VGGFace
# 26 layers in the original VGG-Face
# base_model = VGGFace(include_top=True,
#     model='vgg16',
#     input_shape=(224, 224, 3))
# base_model.summary()
# print(len(base_model.layers))

# 19 layers after excluding the last few layers
base_model1 = VGGFace(include_top=False,
model='vgg16',
input_shape=(224, 224, 3))
base_model1.summary()
print(len(base_model1.layers))

# thêm các lớp tùy chỉnh để mô hình có thể nhận dạng khuôn mặt trong hình ảnh
x = base_model1.output
# x = Flatten()(x)
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dense(1024, activation='relu')(x)
x = Dense(512, activation='relu')(x)

# final layer with softmax activation
preds = Dense(NO_CLASSES, activation='softmax')(x)

# đặt 19 lớp đầu tiên thành không thể huấn luyện và các lớp còn lại có thể tập huấn
# create a new model with the base model's original input and the 
# new model's output
model = Model(inputs = base_model1.input, outputs = preds)
model.summary()

# don't train the first 19 layers - 0..18
for layer in model.layers[:19]:
    layer.trainable = False

# train the rest of the layers - 19 onwards
for layer in model.layers[19:]:
    layer.trainable = True

# Vì 19 lớp đầu tiên đã được huấn luyện bởi mô hình VGGFace16 nên bạn chỉ cần huấn luyện các lớp mới mà bạn đã thêm vào mô hình. Về cơ bản, các lớp mới mà bạn đã thêm sẽ được đào tạo để nhận dạng hình ảnh mới

# Biên dịch mô hình
model.compile(optimizer='Adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'])

# Đào tạo mô hình
model.fit(train_generator,
  batch_size = 10,
  verbose = 1,
  epochs = 3)

# Lưu moo hình
# creates a HDF5 file
model.save('Cbl\model\_face_cnn_model3.h5')

import pickle

class_dictionary = train_generator.class_indices
class_dictionary = {
    value:key for key, value in class_dictionary.items()
}
print(class_dictionary)

# save the class dictionary to pickle
face_label_filename = 'Cbl\model\cface-labels3.pickle'
with open(face_label_filename, 'wb') as f: pickle.dump(class_dictionary, f)


