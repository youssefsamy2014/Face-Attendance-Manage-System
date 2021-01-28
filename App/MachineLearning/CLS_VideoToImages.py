from App.MainAbstract.CLS_MainAbstractModule import CLS
import cv2
import imutils
import os


class CLS_VideoToImages(CLS):
    def __init__(self, Id, name):
        self.Id = Id
        self.name = name
        self.detector = cv2.CascadeClassifier("Assets\\haarcascade\\haarcascade_frontalface_default.xml")
        self.RES_W = 640  # 1280 # 640 # 256 # 320 # 480 # pixels
        self.RES_H = 480  # 720 # 480 # 144 # 240 # 360 # pixels
        # Take image function

    def assure_path_exists(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def SpliterVideo(self):
        vidcap = cv2.VideoCapture("Assets\\videos\\" +self.name+'_'+self.Id+ ".avi")
        face_id =self.Id
        path =self.name+'_'+self.Id+'\\'
        finalpath = 'Assets\\TrainingImage\\' + path
        self.assure_path_exists(finalpath)
        count = 0
        self.assure_path_exists("Assets\\TrainingImage\\")
        if (vidcap.isOpened() == False):
            print("Error opening video stream or file")

        # Read until video is completed
        # Capture frame-by-frame

        while (vidcap.isOpened()):

            ret, frame = vidcap.read()
            if ret == True:
                image = imutils.resize(frame, width=self.RES_W, height=self.RES_H)
                #image = frame

            # Convert frame to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detect frames of different sizes, list of faces rectangles
            faces = self.detector.detectMultiScale(gray, 1.3, 5)

            # Loops for each faces
            for (x, y, w, h) in faces:
                # Crop the image frame into rectangle
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Increment sample face image
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite(finalpath + '\\' + self.name + "." + str(face_id) + '.' + str(count) + ".jpg",
                            gray[y:y + h, x:x + w])

            if count > 100:
                break



