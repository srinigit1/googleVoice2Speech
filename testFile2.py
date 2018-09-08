import RPi.GPIO as GPIO
import speech_recognition as sr
import time
import urllib3

from gtts import gTTS
from pygame import mixer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
mixer.init()

def gpioCTRL (pinNumber, pinState):

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pinNumber, GPIO.OUT)
    if pinState == "ON" :
        GPIO.output(pinNumber, GPIO.HIGH)
    elif pinState == "OFF" :
        GPIO.output(pinNumber, GPIO.LOW)

def announce (statement):
    print("I think you said '" + statement + "'")
    #tts = gTTS(text="I think you said "+str(statement), lang='en')
    tts = gTTS(text=str(statement), lang='en')
    tts.save("response.mp3")
    mixer.music.load('response.mp3')
    mixer.music.play()


while (True == True):
# obtain audio from the microphone
  r = sr.Recognizer()
  with sr.Microphone() as source:
    #print("Please wait. Calibrating microphone...")
    # listen for 1 second and create the ambient noise energy level
    r.adjust_for_ambient_noise(source, duration=1)
    print("Say something!")
    audio = r.listen(source,phrase_time_limit=5)
 
# recognize speech using Sphinx/Google
  try:
    #response = r.recognize_sphinx(audio)
    MicResponse = r.recognize_google(audio)
    announce(MicResponse)

    if (MicResponse.find("on") >= 0):
        response = "on"
    elif (MicResponse.find("off") >= 0):
        response = "off"
    elif (MicResponse.find("of") >= 0):
        response = "off"
    elif (MicResponse.find("blink") >= 0):
        response = "toggle"
    elif (MicResponse.find("drink") >= 0):
        response = "toggle"
    elif (MicResponse.find("ink") >= 0):
        response = "toggle"
    elif (MicResponse.find("ynk") >= 0):
        response = "toggle"

    else:
        response = "invalid"

    if response == "on" :
        gpioCTRL(18,pinState="ON")
    elif response == "off" :
        gpioCTRL(18, pinState="OFF")
    elif response == "toggle" :
         for i in range(10):
            gpioCTRL(18, pinState="ON")
            time.sleep(0.5)
            gpioCTRL(18, pinState="OFF")
            time.sleep(0.5)
    else:
        print ("Invalid Instruction")
        announce("Invalid Instruction")

  except sr.UnknownValueError:
    print("Could not understand audio")
  except sr.RequestError as e:
    print("Error; {0}".format(e))

