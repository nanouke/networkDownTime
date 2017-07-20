#!/usr/bin/python
#-------------------------------------------
# Processus permetent de voir si il y a
# internet sur le reseau
#-------------------------------------------

import sys, os ,getopt, datetime, urllib2, time
from daemon import Daemon

class NetworkDonwTimeDaemon(Daemon):
    def run(self):
        while True:

            if checkLocal() != True:
                if localConnection == True:
                    localConnection = False
                    writeLog(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Local", "lost")

            else:
                if localConnection == False:
                    localConnection = True
                    writeLog(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Local", "established")

            if checkInternet() != True:

                if internetConnection == True:
                    internetConnection = False
                    writeLog(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Internet", "lost")

            else:
                if internetConnection == False:
                    internetConnection = True
                    writeLog(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Internet" ,"established")

            time.sleep(1)

#-------------------------------------------------------
# Eccrie dans le fichier de log
#-------------------------------------------------------
def writeLog(messageDate, network ,state):

    with open('/var/log/networkDownTime.log', 'a') as f:
        f.write(messageDate + ';' + network + ';'+ state + '\n')


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
    daemon = NetworkDonwTimeDaemon('/tmp/NetworkDownTimeDaemon.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)

        sys.exit(0)
    else:
        print "Usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)