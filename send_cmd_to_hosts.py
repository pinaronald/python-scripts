from sys import exit
import time
import datetime #import date
import shutil
import sys
import os
import glob
import paramiko
import csv
from threading import Thread

log = open("/tmp/command/send_command_logs.log", "a")
command_to_send = "touch /tmp/command/testfile1 &;"
wkslist = "/tmp/command/all_ip.csv"
nok_wkslist = open( "/tmp/command/nok_ip_list.csv", "a" )
writer = csv.writer(nok_wkslist)
username = "root"
password = "fAjkldjsoiu763ht1TfnH#"
port = 22

run = 0

def send_command(*args):
    
    index = args[0]
    tmp = index.split(",")
    host_ip = tmp[2]
    cso = tmp[0]

    while run == 0:
         print "Waiting 5secs | " + index
         time.sleep(5)
	 notok = 1
	 error = 0
   
    while notok <= 3:
         error = 0
        
         try:
           s = paramiko.SSHClient()
	   s.load_system_host_keys()
	   s.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
	   s.connect(host_ip, port, username, password)
	 except:
           print "CSO=" + cso + " | Could not connect. "
           log.write( "CSO=" + cso + "|  Could not connect.\n")
           log.flush()
           error = error + 1
           notok = notok + 1
	   writer.writerow(index)

        
         if error == 0:
            try:
	       stdin, stdout, stderr = s.exec_command(command_to_send)
            except Exception, e:
                print "CSO=" + cso + " Could not execute command.", e
                log.write(index + " | Could not execute command.\n")
                log.flush()
                error = error + 1
                notok = notok + 1
         try:
            s.close()
         except Exception, e:
            print index + "Error closing connection.", e
        
        
         if error == 0:
            notok = 0
            print "CSO=" + cso  + " | Successfully executed command "
            log.write( "CSO=" + cso + " Successfully executed command ")
            log.flush()
            notok = 4
         elif error == 3:
            log.write( "CSO=" + cso + " Could not connect.?????? \n")
            writer.writerow(index)
	    log.flush()
         if error > 0 and error <= 3:
            time.sleep(5)


thread_list = []

print "****Running threads*****"
for row in open(wkslist):
    t = Thread(target=send_command, args=(row, ))
    t.start()
    thread_list.append(t)

run = 1
for t in thread_list:
    t.join()

log.close()

