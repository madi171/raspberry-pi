# coding:utf-8
'''

'''

import sys
import os

import cv2
import numpy as np

from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.optimizers import Adam
from keras.utils import to_categorical



class SelfDrivingModel:
    def __init__(self, image_path):
        self.IMAGE_WIDTH = 120
        self.IMAGE_HEIGHT = 59
        self.data = []
        self.labels = []
        self.model = None

        self.model_path = "."
        self.model_name = "self_driving_model"

        self.train_data_dir = '/home/ubuntu/raspberry-pi/autocars/data/dataset_f_l_r_3c/train'
        self.validation_data_dir = '/home/ubuntu/raspberry-pi/autocars/data/dataset_f_l_r_3c/valid'

        self.nb_train_samples = 2000
        self.nb_validation_samples = 100
        self.epochs = 15
        self.batch_size = 10

        pass

    def apply_lane_detection(image):
        image = np.asarray(image)
        image = image.astype(float) * 255
        image = image.astype(np.uint8)
        image = cv2.GaussianBlur(image,(5,5),0)
        edges = cv2.Canny(image,50,150)
        height, width = image.shape[:2]
        valid_height = 20
        triangle = np.array([[(0, valid_height), (0, height), (width, height), (width, valid_height)]])
        mask = np.zeros_like(image)
        mask = cv2.fillPoly(mask, triangle, 255)
        mask = cv2.bitwise_and(image, mask)
        mask = mask.astype(float) / 255.0
        mask = mask.reshape(height, width, 1)
        return mask


    def scale_and_norm_training_samples(self):
        # scale the raw pixel intensities to the range [0, 1]
        self.data = np.array(self.data, dtype="float") / 255.0
        self.labels = np.array(self.labels)

    def build_model(self):
        input_shape = (self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 1)
        self.model = Sequential()
        self.model.add(Conv2D(8, (3, 3), input_shape=input_shape))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(16, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(32))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(3))
        self.model.add(Activation('sigmoid'))
        self.model.summary()
        self.model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['categorical_accuracy']
        )
        return self.model

    def train(self):
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=False
        )
        test_datagen = ImageDataGenerator(rescale=1. / 255,
            horizontal_flip=False
        )

        train_generator = train_datagen.flow_from_directory(
            self.train_data_dir,
            target_size=(self.IMAGE_HEIGHT, self.IMAGE_WIDTH),
            batch_size=self.batch_size,
            color_mode='grayscale',
            class_mode='categorical'
        )

        validation_generator = test_datagen.flow_from_directory(
            self.validation_data_dir,
            target_size=(self.IMAGE_HEIGHT, self.IMAGE_WIDTH),
            batch_size=self.batch_size,
            color_mode='grayscale',
            class_mode='categorical')
      
        self.model.fit_generator(
            train_generator,
            steps_per_epoch=self.nb_train_samples // self.batch_size,
            epochs=self.epochs,
            validation_data=validation_generator,
            validation_steps=self.nb_validation_samples // self.batch_size)

        pass

    def predict(self, img_frame):
        img_frame = cv2.resize(img_frame, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        img_frame = cv2.cvtColor(img_frame, cv2.COLOR_BGR2RGB)
        img_frame = cv2.cvtColor(img_frame, cv2.COLOR_RGB2GRAY)
        img_frame = img_to_array(img_frame)
        data = np.array([img_frame])
        # scale the raw pixel intensities to the range [0, 1]
        data = np.array(data, dtype="float") / 255.0

        ret = self.model.predict(data)

        if len(ret) > 0:
            return np.argmax(ret)
        else:
            return -1
        pass

    def save_model(self):
        path = "%s/%s.h5" % (self.model_path, self.model_name)
        print " -> Start saving model to %s" % path
        self.model.save(path)
        print " -> Saved model to '%s'" % path
        pass

    def load_model(self, path):
        print " -> Start loading from %s" % path
        self.model = load_model(path)
        print " -> Loaded model from '%s'" % path
        pass

    def test(self):
        cnt = 0
        for i in range(len(self.data)):
            data = np.expand_dims(self.data[i], 0)
            ret = self.model.predict(data)
            pred = np.argmax(ret)
            if pred == self.labels[i]:
                cnt += 1
        print "total correct number is %d" % cnt

if __name__ == '__main__':

    if len(sys.argv) > 1:
        cmodel = SelfDrivingModel(sys.argv[1])
        if len(sys.argv) > 2:
            cmodel.model_path = sys.argv[2]
        cmodel.gen_training_image_set()
        cmodel.build_model()
        cmodel.train()
        cmodel.save_model()
        #cmodel.load_model(sys.argv[2])
        #cmodel.test()
