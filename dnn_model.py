# coding:utf-8
'''
Raspberry Pi Car Demo Series
'''

import cv2
import os
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from sklearn.cross_validation import train_test_split

from squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import to_categorical



class DNNModel:
    def __init__(self, image_path):
        self.IMAGE_SIZE = 64
        self.data = []
        self.labels = []
        self.model = self.build_model()

        if image_path is not None:
            self.image_path = image_path
        else:
            self.image_path = "/home/madi/deeplearning/raspberry-pi/datasets"
        pass

    def gen_training_image_set(self):
        imagePaths = os.listdir(self.image_path)
        # loop over the input images
        for imagePath in imagePaths:
            # load the image, pre-process it, and store it in the data list
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (self.IMAGE_SIZE, self.IMAGE_SIZE))
            image = img_to_array(image)
            self.data.append(image)

            # extract the class label from the image path and update the
            # labels list]
            if "left" in imagePath.split(os.path.sep)[-2]:
                label = 1
            elif "right" in imagePath.split(os.path.sep)[-2]:
                label = 2
            else:
                label = 0

            self.labels.append(label)

        # scale the raw pixel intensities to the range [0, 1]
        self.data = np.array(self.data, dtype="float") / 255.0
        self.labels = np.array(self.labels)

    def build_model(self):
        self.model = SqueezeNet(include_top=False, weights=None, classes=3)
        opt = Adam()
        self.model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
        pass

    def train(self):
        # split train and test set
        (trainX, testX, trainY, testY) = train_test_split(self.data, self.labels, test_size=0.25, random_state=42)

        # convert the labels from integers to vectors
        trainY = to_categorical(trainY, num_classes=3)
        testY = to_categorical(testY, num_classes=3)

        self.model.fit(trainX, trainY, batch_size=32, epochs=10, verbose=1)

        pass

    def predict(self, img_frame):
        img_frame = cv2.resize(img_frame, (self.IMAGE_SIZE, self.IMAGE_SIZE))
        img_frame = img_to_array(img_frame)
        data = np.array([img_frame])

        ret = self.model.predict(data)

        if len(ret) > 0:
            return ret[0]
        pass

    def save_model(self):
        self.model.save("greenball_squeezenet.h5")
        pass

    def load_model(self):
        self.model = load_model("greenball_squeezenet.h5")
        pass


if __name__ == '__main__':
    dnn = DNNModel()
    dnn.gen_training_image_set()
    dnn.train()
    dnn.save_model()