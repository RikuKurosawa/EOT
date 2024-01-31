# -*- coding: utf-8 -*-
import socket
import os
import time
from sys import stdin
import time
import ConfigParser
import errno
#import win32gui
#import ahk


def main():

    import Values

    setting_ini = ConfigParser.ConfigParser()
    setting_ini_path = 'setting.ini'

    if not os.path.exists(setting_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), setting_ini_path)

    setting_ini.read(setting_ini_path)

    Values.naoip  = setting_ini.get('NORMAL','naoip')
    Values.mode = setting_ini.get('NORMAL','mode')


    print("Hi! I will hepl your job with my lovely NAO!")

    print("Is this IP correct?",Values.naoip)

    print("Press input y to continue, or you can input the correct IP here")

    
    am = stdin.readline()
    am = am.strip()
    if am== "y":

     pass

    else:
        while True:
            print("OK?[y/n]",am)
            aa = stdin.readline()
            aa = aa.strip()
            if aa == "y":
                Values.naoip = am
                break
            else:
                print("Please input the correct IP")
                am = stdin.readline()
                am = am.strip()

                if am == "default":
                    Values.naoip  = setting_ini.get('NORMAL','naoip')
                    break

    print("Defined the IP to",Values.naoip)

    while True:
        print("5 or 15?")
        am = stdin.readline()
        am = am.strip()

        if am == "5":
            mode = 5
            Values.mode = 5
            break

        if am == "15":
            mode = 15
            Values.mode = 15
            break

    #from Nao import main as Nao
    import Nao
    Nao.main()



if __name__ == '__main__':
    main()








  