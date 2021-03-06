# -*- coding: utf-8 -*-
"""Digit recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uK01c1VGK4MiE6hX5u5M48L30pokCP6L
"""

import cv2
from keras.datasets import mnist
import keras
from keras.models import Sequential
from keras.layers import Conv2D,Dropout,Dense,Flatten,MaxPooling2D
from google.colab.patches import cv2_imshow
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from skimage.segmentation import clear_border
import imutils

(x_train,y_train),(x_test,y_test)=mnist.load_data()
x_train=255-x_train
x_test=255-x_test
x_train,x_val,y_train,y_val=train_test_split(x_train,y_train)

def preprocess(img):
    img=cv2.equalizeHist(img)
    img=img/255.0
    return img

x_train=np.array(list(map(preprocess,x_train)))
x_test=np.array(list(map(preprocess,x_test)))
x_val=np.array(list(map(preprocess,x_val)))
x_train=x_train.reshape(x_train.shape[0],28,28,1)
x_val=x_val.reshape(x_val.shape[0],28,28,1)
x_test=x_test.reshape(x_test.shape[0],28,28,1)

gen=ImageDataGenerator(width_shift_range=0.1,height_shift_range=0.1,zoom_range=0.2,shear_range=0.1,rotation_range=25)
gen.fit(x_train)
y_train=to_categorical(y_train,10)
y_test=to_categorical(y_test,10)
y_val=to_categorical(y_val,10)

model= Sequential()
model.add(Conv2D(20,5,padding="same",input_shape=(28,28,1),activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2)))
model.add(Conv2D(50,5,padding="same",activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2)))
model.add(Flatten())
model.add(Dense(250, activation='relu',use_bias=True))
model.add(Dense(10, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adam(lr=0.001),metrics=['accuracy'])

batch_size = 100
epochs = 6
hist=model.fit_generator(gen.flow(x_train,y_train,batch_size),steps_per_epoch=450,epochs=epochs,verbose=1,validation_data=(x_val, y_val))

plt.figure(1)
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.legend(['train','validation'])
plt.title('Loss')
plt.figure(2)
plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.legend(['train','validation'])
plt.title('Accuracy')
plt.show()

score=model.evaluate(x_test,y_test,verbose=0)
print("score = ",score[0])
print("accuracy = ",score[1])
model.save('t1.h5')