#!/usr/bin/python

import MySQLdb, time, datetime, threading, commands, subprocess

class ProcessorMonitor():
     def __init__(self):
          self.cpuFile = open("/proc/stat", "r")
          self.cpuUsage = 0
          self.Interval = 2
     def getTimeList(self):
          self.cpuFile = open("/proc/stat", "r")
          timeList = self.cpuFile.readline().split(" ")[2:6]
          self.cpuFile.close()
          for i in range(len(timeList))  :
               timeList[i] = int(timeList[i])
          return timeList
     def getCpuUsage(self):
          now = datetime.datetime.now()
          datestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
          timestamp = str(now.hour) + ":" + str(now.minute) + ":00"
          x = self.getTimeList()
          time.sleep(self.Interval)
          y = self.getTimeList()
          for i in range(len(x))  :
               y[i] -= x[i]
          cpuPct = 100 - (y[len(y) - 1] * 100.00 / sum(y))
          # enter data into database
          # Open database connection
          db = MySQLdb.connect("localhost","root","root","nms" )
          try:
               # prepare a cursor object using cursor() method
               cursor = db.cursor()
               sql = "INSERT INTO nms_processor (datestamp,timestamp,cpuusage) VALUES ('%s','%s',%.2f)" % (datestamp,timestamp,cpuPct)
               cursor.execute(sql)
               db.commit()
          except:
               # Rollback in case there is any error
               db.rollback()
          # disconnect from server
          db.close()

class ProcessorThread(threading.Thread):
     def __init__(self,pm):
          threading.Thread.__init__(self)
          self.pm = pm

     def run(self):
          while True:
               self.pm.getCpuUsage()
               print "cpu"
               time.sleep(58)

if __name__ == "__main__": 
     try:
          pm = ProcessorMonitor()
          thr2 = ProcessorThread(pm)
          thr2.start()
     except:
          print "error"

