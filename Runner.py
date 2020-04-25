"""
    Title: Guidance-System-for-Visually-Impaired-People
    Author: Ashish Kore and Syeda Atiya Husain and Nupur Kshatri
    Language: Python
    Requirements:
    Python version-> 3 or later
    Python Packages or Modules->    1. flask
                                    2. imageai
                                    3. requests
                                    4. cv2
                                    5. numpy
                                    6. random
                                    7. gtts
                                    8. playsound
    Additional Files->      1. Yolov3.h5
"""

#importing necessary packages and modules
from flask import Flask, render_template
from imageai.Detection import ObjectDetection
import requests as r
import cv2
import numpy as np
import random
from gtts import gTTS 
import playsound

#initialising flask based app
app = Flask(__name__)


@app.route('/')
#This function will be called on landing up to the above endpoint.
def home():
"""
This function returns a template named home.html.
"""
    return render_template('home.html')

class main():
"""
This class is defined to instantiate ObjectDetection class and load Yolov3 model through the constructor.
"""
    def __init__(self):
        self.detector = ObjectDetection() #creating object of Object Detection class.
        self.model_path = "static/yolo.h5" #specifying path of yolo model.
        self.detector.setModelTypeAsYOLOv3() #selecting model type
        self.detector.setModelPath(self.model_path) #setting model path
        self.detector.loadModel()#loading Yolo model
      
url="http://192.168.43.225:8080/shot.jpg" # url for IP Web Camera App server       
        
@app.route('/index', methods=['POST'])
#This function will be called on landing up to the above endpoint.
def index_func():
"""
This function upon calling performs object detection task on images obtained from IP Web Camera. 
There after it generates audio instructions containing names of the object classes.
This process gets continued on live images untill the user shuts down the IP Web Camera app.
"""
    try:
        s=main()#initializing main class object
        z=0
        while True:

            res= r.get(url)# hits the IP Web Camera server url for image response 
            arr=np.array(bytearray(res.content), dtype=np.uint8)
            img=cv2.imdecode(arr,-1)
            cv2.imwrite("static/detectionimage/a{}.jpeg".format(z),img)#saving the response image in jpeg format

            input_path = "static/detectionimage/a{}.jpeg".format(z)
            output_path = "static/output/a{}.jpeg".format(z)
            # calling detection function for object detection and storing the object names in a list
            detection = s.detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)
            a=""
            obj=set()
            for d in detection:
                obj.add(d['name'])
            #generating audio instructions according to objects name list
            language = 'en'
            if len(obj)==0:
                sss="It seems to be nothing on your way"
                speech = gTTS(text = sss, lang = language, slow = False)
            else:
                fin='and'.join(obj)
                ss1="Hey!! Their is {} on your way.".format(fin)
                ss2="Hey!! I found {} their.".format(fin)
                ss3="Their is {} in front of you.".format(fin)
                x=random.randrange(1,4)
                if x==1:
                    speech = gTTS(text = ss1, lang = language, slow = False)
                elif x==2:
                    speech = gTTS(text = ss2, lang = language, slow = False)
                elif x==3:
                    speech = gTTS(text = ss3, lang = language, slow = False)

            speech.save("static/audio/a{}.mp3".format(z))#saving generated audio
            playsound.playsound("static/audio/a{}.mp3".format(z),True)#playing generated audio

    except:
            return render_template('output.html')#returns output.html template when the app is closed

if __name__ == '__main__':
    app.run(debug=True)
