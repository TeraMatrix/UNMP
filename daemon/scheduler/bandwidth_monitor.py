#!/usr/bin/python

import MySQLdb, time, datetime, threading, commands, subprocess

class BandwidthMonitor():
     def __init__(self):
          self.netFile = open("/proc/net/dev",'r')
          self.interface = []
          self.lastRxByte = []
          self.lastTxByte = []
          self.rxByte = []
          self.txByte = []
          self.firstTime = True
     def getInterfacesTxRx(self):
          self.netFile = open("/proc/net/dev",'r')
          lineNum = 0
          arrayIndex = 0
          for line in self.netFile:
               lineNum += 1
               if lineNum > 3:
                    if len(self.interface) < arrayIndex + 1:
                         self.interface.insert(arrayIndex,"")
                         self.lastRxByte.insert(arrayIndex,0)
                         self.lastTxByte.insert(arrayIndex,0)
                         self.rxByte.insert(arrayIndex,0)
                         self.txByte.insert(arrayIndex,0)
                    interfaceDetails = line.split()
                    self.interface[arrayIndex] = interfaceDetails[0]
                    self.rxByte[arrayIndex] = float(interfaceDetails[1]) - float(self.lastRxByte[arrayIndex])
                    self.txByte[arrayIndex] = float(interfaceDetails[9]) - float(self.lastTxByte[arrayIndex])
                    self.lastRxByte[arrayIndex] = float(interfaceDetails[1])
                    self.lastTxByte[arrayIndex] = float(interfaceDetails[9])
                    arrayIndex += 1
          now = datetime.datetime.now()
          #print "\nDate: " + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + " Time: " + str(now.hour) + ":" + str(now.minute)
          if self.firstTime == True:
               self.firstTime = False
          else:
               datestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
               timestamp = str(now.hour) + ":" + str(now.minute) + ":00"
               # enter data into database
               # Open database connection
               db = MySQLdb.connect("localhost","root","root","nms" )
               try:
                    # prepare a cursor object using cursor() method
                    cursor = db.cursor()
                    for arrayIndex in range(0,len(self.interface)):
                         rx = self.rxByte[arrayIndex]/(1024 * 1024)
                         tx = self.txByte[arrayIndex]/(1024 * 1024)
                         # print "Inteface: " + self.interface[arrayIndex] + "\tRX: " + str(rx) + "\tTX: " + str(tx)

                         # Prepare SQL query to INSERT a record into the database.
                         sql = "INSERT INTO nms_bandwidth (datestamp,timestamp,interface,tx,rx) VALUES ('%s','%s','%s',%.2f,%.2f)" % (datestamp,timestamp,self.interface[arrayIndex],tx,rx)
                         cursor.execute(sql)
                    db.commit()
               except:
                    # Rollback in case there is any error
                    db.rollback()
               # disconnect from server
               db.close()
          self.netFile.close()

class BandwidthThread(threading.Thread):
     def __init__(self,bm):
          threading.Thread.__init__(self)
          self.bm = bm

     def run(self):
          while True:
               self.bm.getInterfacesTxRx()
               print "band"
               time.sleep(60)

if __name__ == "__main__": 
     try:
          bm = BandwidthMonitor()
          thr1 = BandwidthThread(bm)
          thr1.start()
     except:
          print "error"

