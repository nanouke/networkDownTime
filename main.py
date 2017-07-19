#!/usr/bin/python
#-------------------------------------------
# Processus permetent de voir si il y a
# internet sur le reseau
#-------------------------------------------

import sys
import os
import getopt
import datetime
import urllib2
import time


def main():

    internetConnection = True
    localConnection = True

    verbose = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:v", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:

        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False

    print("Programme start...")
    print("Start checking internet connection...")

    try:
        while True:

            if checkLocal() != True:
                if localConnection == True:
                    localConnection = False
                    writeLog(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Local", "lost")
                    print('Local network connection lost at : %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )

                if verbose:
                    print("Local network connection : Error")
            else:
                if localConnection == False:
                    localConnection = True
                    writeLog(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Local", "established")
                    print('Local network connection established at : %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )

                if verbose:
                    print("Local network connection : Ok")

            if checkInternet() != True:

                if internetConnection == True:
                    internetConnection = False
                    print('Internet connection lost at : %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
                    writeLog(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Internet", "lost")
                else:
                    if verbose:
                        print("Internet connexion : Error")

            else:
                if internetConnection == False:
                    internetConnection = True
                    print('Internet connection established at : %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
                    writeLog(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Internet" ,"established")
                else:
                    if verbose:
                        print('Internet connection : OK')

            time.sleep(1)


    except KeyboardInterrupt:
        print('Programme end')

#-------------------------------------------------------
# Eccrie dans le fichier de log
#-------------------------------------------------------
def writeLog(messageDate, network ,state):

    with open('/var/log/networkDownTime.log', 'a') as f:
        f.write(messageDate + ';' + network + ';'+ state + '\n')

#-------------------------------------------------------
# Affiche le Help
#-------------------------------------------------------
def usage():
    print('------------------------------------')
    print('Network down loging system')
    print('------------------------------')
    print('Parameters')
    print('------------------------------------')
    print('-h   help')
    print('-v   verbose')
    print('------------------------------------')


#-------------------------------------------------------
# Vererifi si internet est disponible
#-------------------------------------------------------
def checkInternet():
    for timeout in [1,5,10,15]:
        try:
            response = urllib2.urlopen('https://google.com', timeout=timeout)
            return True
        except urllib2.URLError as err: pass
    return False

#-------------------------------------------------------
# Vererifi si le reseau local est disponible
#-------------------------------------------------------
def checkLocal():
    for timeout in [1,5,10,15]:
        try:
            response = urllib2.urlopen('http://192.168.1.1', timeout=timeout)
            return True
        except urllib2.URLError as err: pass
    return False


if __name__ == "__main__":
    main()