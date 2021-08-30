from sys import exit
import time
import datetime #import date
import shutil
import sys
import os
import glob
import paramiko
from threading import Thread

paramiko.util.log_to_file("D:\\upgradeCygwin\\putFiles\\paramiko_put.log")
log = open("D:\\upgradeCygwin\\putFiles\\putdata_logs.log", "a")
dest = '/cygdrive/C/Tools/Cygwin'
filestosend = "D:\\upgradeCygwin\\putFiles\\fileput.txt"
wkslist = "D:\\upgradeCygwin\\putFiles\\all_ip.csv"
username = "Administrator"
password = "#Jldjs978089T"

run = 0

def write_data(teststr, *args):
    index = args[0]
    
    tmp = index.split(",")
    host = tmp[2]
    cso = tmp[0]
    port = 38105
    while run == 0:
        print "Waiting 5secs" + index
        time.sleep(5)
    notok = 1
    error = 0
    while notok <= 3:
        error = 0
        try:
            transport = paramiko.Transport((host, port))
            transport.connect(username = username, password = password)
            sftp = paramiko.SFTPClient.from_transport(transport)
        except:
            print index + " Could not connect."
            log.write(index + " Could not connect.\n")
            log.flush()
            error = error + 1
            notok = notok + 1
        if error == 0:
            try:
                 sftp.chdir(dest)
                 pwd = sftp.getcwd()
                 for filenam in open(filestosend):
                     filenam = filenam.rstrip("\n\r")
                     print filenam, dest + '/' + os.path.basename(filenam) 
                     sftp.put(filenam, dest + '/' + os.path.basename(filenam) )
            except Exception, e:
                print index + " Could not upload data.", e
                log.write(index + " Could not upload data.\n")
                log.flush()
                error = error + 1
                notok = notok + 1
        try:
            sftp.close()
            transport.close()
        except Exception, e:
            print index + "Error closing connection.", e
        if error == 0:
            notok = 0
            print index + " Successfully transferred file \n"
            log.write(index + " Successfully transferred file \n")
            log.flush()
            notok = 4
        elif error == 3:
            log.write(index + " Could not connect.\n")
            log.flush()
        if error > 0 and error <= 3:
            time.sleep(5)


thrlist = []

print "Running threads"
for row in open(wkslist):
    thr = Thread(target=write_data,args=('teststr', row))
    thr.start()
    thrlist.append(thr)


run = 1
for thr in thrlist:
    thr.join()


    
log.close()

