# coding:utf-8
'''
Raspberry Pi Car Demo Series
'''

import sys
import cv2
import os
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from sklearn.cross_validation import train_test_split

from squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import to_categorical



class ControlModel:
    def __init__(self, image_path):
        self.IMAGE_WIDTH = 120
        self.IMAGE_HEIGHT = 60
        self.data = []
        self.labels = []
        self.model = None

        self.model_path = "."
        self.model_name = "control_model"

        if image_path is not None:
            self.image_path = image_path
        else:
            self.image_path = "/home/madi/deeplearning/raspberry-pi/datasets"
        pass

    def gen_training_image_set(self):
        imagePaths = os.listdir(self.image_path)
        # loop over the input images
        count = 0
        total_count = len(imagePaths)
        for imagePath in imagePaths:
            # load the image, pre-process it, and store it in the data list
            imagePath = self.image_path + "/" + imagePath
            #print " -> processing image %s" % imagePath
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
            image = img_to_array(image)

            self.data.append(image)

            # extract the class label from the image path and update the
            # labels list]
            ss = imagePath.split('_')
            if len(ss) < 2:
                continue
            path_label = ss[1]

            if "left" in path_label:
                label = 1
            elif "right" in path_label:
                label = 2
            elif "forward" in path_label:
                label = 3
            elif "backward" in path_label:
                label = 4
            else:
                label = 0

            self.labels.append(label)
            count += 1
            print "=> (%03d/%03d) Label=%d in path: %s" % (count, total_count, label, imagePath)

        # scale the raw pixel intensities to the range [0, 1]
        self.data = np.array(self.data, dtype="float") / 255.0
        self.data = np.transpose(self.data, (0,2,1,3)) # transpose shape
        self.labels = np.array(self.labels)
        print "Data processing done"


    def scale_and_norm_training_samples(self):
        # scale the raw pixel intensities to the range [0, 1]
        self.data = np.array(self.data, dtype="float") / 255.0
        self.labels = np.array(self.labels)

    def build_model(self):
        self.model = SqueezeNet(include_top=True, weights=None, classes=5, input_shape=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT, 3))
        self.model.summary()
        opt = Adam()
        self.model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
        return self.model

    def train(self):
        # split train and test set
        (trainX, testX, trainY, testY) = train_test_split(self.data, self.labels, test_size=0.25, random_state=42)

        # convert the labels from integers to vectors
        trainY = to_categorical(trainY, num_classes=5)
        testY = to_categorical(testY, num_classes=5)

        self.model.fit(trainX, trainY, batch_size=1, epochs=3, verbose=1, validation_data=(testX, testY))
        pass

    def predict(self, img_frame):
        img_frame = cv2.resize(img_frame, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        img_frame = img_to_array(img_frame)
        data = np.array([img_frame])
        # scale the raw pixel intensities to the range [0, 1]
        data = np.array(data, dtype="float") / 255.0
        data = np.transpose(data, (0,2,1,3)) # transpose shape

        ret = self.model.predict(data)

        if len(ret) > 0:
            return np.argmax(ret)
        else:
            return -1
        pass

    def save_model(self):
        path = "%s/%s.squeeze.h5" % (self.model_path, self.model_name)
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
        for i in xrange(len(self.data)):
            data = np.expand_dims(self.data[i], 0)
            ret = self.model.predict(data)
            pred = np.argmax(ret)
            if pred == self.labels[i]:
                cnt += 1
        print "total correct number is %d" % cnt

if __name__ == '__main__':

    if len(sys.argv) > 1:
        cmodel = ControlModel(sys.argv[1])
        if len(sys.argv) > 2:
            cmodel.model_path = sys.argv[2]
        cmodel.gen_training_image_set()
        cmodel.build_model()
        cmodel.train()
        cmodel.save_model()
        #cmodel.load_model(sys.argv[2])
        #cmodel.test()
