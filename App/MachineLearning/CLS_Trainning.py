#import csv
from App.MainAbstract.CLS_MainAbstractModule import CLS
import cv2
import imutils
import os
import numpy as np
from PIL import Image
import pickle
### STill under develop we can input video instead of open camera
# counting the numbers

class CLS_Trainning(CLS):

    def __init__(self):
     
        self.detector = cv2.CascadeClassifier("Assets\\haarcascade\\haarcascade_frontalface_default.xml")
        self.RES_W = 640  # 1280 # 640 # 256 # 320 # 480 # pixels
        self.RES_H = 480  # 720 # 480 # 144 # 240 # 360 # pixels
        # Take image function

    def assure_path_exists(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
    def getImagesAndLabels(self, path):

        faceSamples = []
        ids = []
        IMAGE_dir = "Assets\\TrainingImage"
        print(IMAGE_dir)
        for root,dirs ,files in os.walk(IMAGE_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    #label = os.path.basename(root).replace(" ", "-").lower()
                # Get the image and convert it to grayscale
                PIL_img = Image.open(path).convert('L')

                # PIL image to numpy array
                img_numpy = np.array(PIL_img, 'uint8')

                # Get the image id
                id = int(os.path.split(path)[-1].split(".")[1])

                # Get the face from the training images
                faces = self.detector.detectMultiScale(img_numpy)

                # Loop for each face, append to their respective ID
                for (x, y, w, h) in faces:
                    # Add the image to face samples
                    faceSamples.append(img_numpy[y:y + h, x:x + w])

                    # Add the ID to IDs
                    ids.append(id)

            # Pass the face array and IDs array
        return faceSamples, ids

    def TrainImages(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        # Get the faces and IDs
        p = 'Assets\\TrainingImage\\'
        #+ self.name + ' , ' + self.Id + '\\'
        faces, ids = self.getImagesAndLabels(p)

        # Train the model using the faces and IDs
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer.yml
        self.assure_path_exists('Assets\\TrainingImageLabel\\')
        recognizer.save('Assets\\TrainingImageLabel\\trainer.yml')
