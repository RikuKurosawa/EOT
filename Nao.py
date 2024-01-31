# -*- coding: utf-8 -*

from naoqi import ALProxy
import time
import threading
import argparse
import os
#from ahk import AHK
import pyautogui
import subprocess
from sys import stdin
import ConfigParser



def main():
        import Values

        global PP
        global naoip
        global naoport
        global setting_ini
        global setting_ini_path

        #PP = None
        #naoport = None
        naoip = Values.naoip

        setting_ini = ConfigParser.ConfigParser()
        setting_ini_path = 'setting.ini'

        if not os.path.exists(setting_ini_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), setting_ini_path)

        setting_ini.read(setting_ini_path)

        PP  = setting_ini.get('NORMAL','powerpoint_name')
        naoport = setting_ini.get('NORMAL','naoport')
        naoport = int(naoport)


        first()

        performance()


        print("SOLID AIR!!!!!")


def first():
    global orivol
    global PP
    global naoip
    global naoport
    global tts
    global leds

    print("first3")
    print(naoport)

    path = os.getcwd()

    print(path)

    #パワポ起動
    subprocess.Popen(['start',PP],shell=True)

    ALmanagerProxy = ALProxy("ALBehaviorManager", naoip, naoport)
    ALAutonomousLifeProxy = ALProxy("ALAutonomousLife",naoip,naoport)
    motionProxy  = ALProxy("ALMotion",naoip, naoport)
    motion = ALProxy("ALMotion", naoip, naoport)
    tracker = ALProxy("ALTracker", naoip, naoport)
    leds = ALProxy("ALLeds",naoip,naoport)
    basic_awareness = ALProxy("ALBasicAwareness", naoip, naoport)
    ALAudioDeviceProxy = ALProxy("ALAudioDevice",naoip,naoport)
    tts = ALProxy("ALTextToSpeech",naoip,naoport) 

    ALmanagerProxy.stopAllBehaviors
    ALAutonomousLifeProxy.setState("disabled")
    faceSize = 1
    motion.wakeUp()
    
    leds.setIntensity("FaceLeds", 1)
    leds.fadeRGB("FaceLeds","white",0.1)
    leds.setIntensity("EarLeds",0)

    targetName = "Face"
    faceWidth = faceSize
    tracker.registerTarget(targetName, faceWidth)   
    tracker.track(targetName)

    motionProxy.setBreathEnabled('Body', True)
    motionProxy.setFallManagerEnabled(True)  

    basic_awareness.startAwareness()

    orivol = ALAudioDeviceProxy.getOutputVolume()

    def setParameterF(str1):

        global tts
        global setting_ini

        tts.setParameter(str1,float(setting_ini.get('NORMAL',str1)))


    #tts.getAvailableVoices()
    #tts.setParameter("pitchShift", 1.5)
    setParameterF("pitch")
    setParameterF("doubleVoice")
    setParameterF("doubleVoiceLevel")
    setParameterF("enableCompression")
    setParameterF("emph")#アクセント 0-2
    setParameterF("pauseMiddle")#一つのコマンドの最後
    setParameterF("pauseLong")#読点での待ち時間
    setParameterF("pauseSentence")#文と文の間の長さ
    setParameterF("volume")#しゃべりの大きさ
    setParameterF("doubleVoiceTimeShift")
    setParameterF("speed")

    print("Done first")

def performance():

    import Values
    global data

    def animesay(str1):
        global leds
        global setting_ini
        global naoip
        global naoport
        global data
       
        leds.setIntensity("EarLeds",float(setting_ini.get('NORMAL','ear_talking_led_brightness')))
        leds.fadeRGB("FaceLeds",int(setting_ini.get('NORMAL','eye_talking_color'),16),float(setting_ini.get('NORMAL','eye_talking_brightness')))

        print("nao",str1)

        ALAnimatedSpeechProxy = ALProxy("ALAnimatedSpeech",naoip,naoport)

        def blink():
            global naoip
            global leds

            rDuration = 0

            eye = int(setting_ini.get('NORMAL','eye_talking_color'),16)

            leds.fadeRGB( "FaceLed0", 0x000000, rDuration, _async=True )
            leds.fadeRGB( "FaceLed1", 0x000000, rDuration, _async=True )
            leds.fadeRGB( "FaceLed2", eye, rDuration, _async=True )
            leds.fadeRGB( "FaceLed3", 0x000000, rDuration, _async=True )
            leds.fadeRGB( "FaceLed4", 0x000000, rDuration, _async=True )
            leds.fadeRGB( "FaceLed5", 0x000000, rDuration, _async=True )
            leds.fadeRGB( "FaceLed6", eye, rDuration, _async=True )
            leds.fadeRGB( "FaceLed7", 0x000000, rDuration, _async=True )
            time.sleep( 0.1 )
            leds.fadeRGB( "FaceLeds", eye, rDuration )


        blink()

        ALAnimatedSpeechProxy.say(str1)

        leds.fadeRGB("FaceLeds",int(setting_ini.get('NORMAL','eye_normal_color'),16),float(setting_ini.get('NORMAL','eye_normal_brightness')))
        leds.setIntensity("EarLeds",0)

    if Values.mode == 15:
        f = open('scripts_15.txt','r')

    else:
        f = open('scripts_5.txt', 'r')

    while True:
      data = f.readline()
      data = data.rstrip('\n')

      if data == '':
        break

      if 'ENTER' in data:
        target = ':'
        idx = data.find(target)
        data = data[:idx]
        print(data)
        continue

      if 'WAITPOINT' in data:
          waitpoint()
          continue


      else:
         animesay(data)

    f.close()



       


        

if __name__ == '__main__':
    main()