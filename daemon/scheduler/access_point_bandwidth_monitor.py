#!/usr/bin/python

import MySQLdb, time, datetime, threading, commands, subprocess, urllib2, base64, socket

class AccessPointBandwidthMonitor():
     def __init__(self):
          self.accessPointList = []
          self.tempAccessPointList = []

     def getAccessPointList(self):
          # Open database connection
          db = MySQLdb.connect("localhost","root","root","nms")
          try:
               # prepare a cursor object using cursor() method
               cursor = db.cursor()
               sql = "SELECT id,ipaddress,hostname,username,password FROM nms_devices \
                      WHERE devicetype = 'AP'"
               cursor.execute(sql)
               result = cursor.fetchall()

               if len(self.accessPointList) == 0:
                    for row in result:
                         self.accessPointList.append({"id":row[0],"address":row[1],"hostname":row[2],"check": 0,"username":row[3],"password":row[4]})
               else:
                    self.tempAccessPointList = []
                    for row in result:
                         self.tempAccessPointList.append({"id":row[0],"address":row[1],"hostname":row[2],"check": 0,"username":row[3],"password":row[4]})

                    for i in range(0,len(self.accessPointList)):
                         isExist = 0
                         for tap in self.tempAccessPointList:
                              if tap["id"] == self.accessPointList[i]["id"]:
                                   self.tempAccessPointList.remove(tap)
                                   isExist = 1
                                   break
                         if isExist == 0:
                              self.accessPointList.remove(self.accessPointList[i])
                              i -= 1

                    for tap in self.tempAccessPointList:
                         self.accessPointList.append({"id":tap["id"],"address":tap["address"],"hostname":tap["hostname"],"check": 0,"username":row[3],"password":row[4]})
          except:
               print "database error"
          # disconnect from server
          db.close()

     def setSnmpValues(self):
          socket.setdefaulttimeout(1)
          now = datetime.datetime.now()
          datestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
          timestamp = str(now.hour) + ":" + str(now.minute) + ":00"
          # Open database connection
          db = MySQLdb.connect("localhost","root","root","nms")
          # prepare a cursor object using cursor() method
          cursor = db.cursor()
          sql = ""
          print "\ntime: " + str(now.hour) + ":" + str(now.minute) + "\n"
          for ap in self.accessPointList:
               # call perl script for snmp get
               args = [ap["address"]]
               command = ["/omd/deamon/snmp.pl"]
               command.extend(args)
               pipe = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
               commandResult = pipe.split("\n")
               interfaceName = []
               interfaceTx = []
               interfaceRx = []
               sysUptime = "Down"
               if len(commandResult) == 5:
                    interfaceName = commandResult[1].split(",")
                    interfaceTx = commandResult[2].split(",")
                    interfaceRx = commandResult[3].split(",")
                    sysUptime = commandResult[4]
                    if ap["check"] == 0:
                         for i in range(0,len(commandResult)):
                              sql = "SELECT COUNT(*) from nms_devices_current_bandwidth \
                                     WHERE deviceid = %s AND interface = '%s'" % (ap["id"],interfaceName[i])
                              cursor.execute(sql)
                              result = cursor.fetchall()
                              count = 0
                              for row in result:
                                   count = row[0]
                              if count == 0:
                                   sql = "INSERT INTO nms_devices_current_bandwidth(deviceid,interface,tx,rx) VALUE(%s,'%s',%s,%s)" % (ap["id"],interfaceName[i],interfaceTx[i],interfaceRx[i])
                              else:
                                   sql = "UPDATE nms_devices_current_bandwidth SET \
                                          tx = %s, \
                                          rx = %s \
                                          WHERE deviceid = %s AND interface = '%s'" % (interfaceTx[i],interfaceRx[i],ap["id"],interfaceName[i])
                              cursor.execute(sql)
                              db.commit()
                         ap["check"] = 1
                    else:
                         for i in range(0,len(commandResult)):
                              sql = "SELECT tx,rx from nms_devices_current_bandwidth \
                                     WHERE deviceid = %s AND interface = '%s'" % (ap["id"],interfaceName[i])
                              cursor.execute(sql)
                              result = cursor.fetchall()
                              oldTx = 0
                              oldRx = 0
                              for row in result:
                                  oldTx = row[0]
                                  oldRx = row[1]
                              tx =  long(interfaceTx[i]) - long(oldTx)
                              rx =  long(interfaceRx[i]) - long(oldRx)
                              sql = "INSERT INTO nms_devices_delta_bandwidth (datestamp,timestamp,deviceid,interface,tx,rx) VALUES('%s','%s',%s,'%s',%s,%s)" % (datestamp,timestamp,ap["id"],interfaceName[i],tx,rx)
                              cursor.execute(sql)
                              db.commit()
                              sql = "UPDATE nms_devices_current_bandwidth SET \
                                     tx = %s, \
                                     rx = %s \
                                     WHERE deviceid = %s AND interface = '%s'" % (interfaceTx[i],interfaceRx[i],ap["id"],interfaceName[i])
                              cursor.execute(sql)
                              db.commit()



                              # Get Connected User
                              connectedUser = 0
                              username = ap["username"]
                              password = ap["password"]
                              ip = ap["address"]
               
                              # for VAP 1
                              try:
                                   url = "http://" + ip + "/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=1"
                                   req = urllib2.Request(url)
                                   auth_string = base64.encodestring("%s:%s" % (username,password))
                                   req.add_header("Authorization", "Basic %s" % auth_string)
                                   f = urllib2.urlopen(req)
                                   response = f.read()
                                   countUser = response.count("<TR>") - 2
                                   if  countUser > 0:
                                        connectedUser += countUser
                              except:
                                    connectedUser += 0
               
                              # for VAP 2
                              try:
                                   url = "http://" + ip + "/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=2"
                                   req = urllib2.Request(url)
                                   auth_string = base64.encodestring("%s:%s" % (username,password))
                                   req.add_header("Authorization", "Basic %s" % auth_string)
                                   f = urllib2.urlopen(req)
                                   response = f.read()
                                   countUser = response.count("<TR>") - 2
                                   if  countUser > 0:
                                        connectedUser += countUser
                              except:
                                    connectedUser += 0

                              # for VAP 3
                              try:
                                   url = "http://" + ip + "/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=3"
                                   req = urllib2.Request(url)
                                   auth_string = base64.encodestring("%s:%s" % (username,password))
                                   req.add_header("Authorization", "Basic %s" % auth_string)
                                   f = urllib2.urlopen(req)
                                   response = f.read()
                                   countUser = response.count("<TR>") - 2
                                   if  countUser > 0:
                                        connectedUser += countUser
                              except:
                                    connectedUser += 0
               
                              # for VAP 4
                              try:
                                   url = "http://" + ip + "/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=4"
                                   req = urllib2.Request(url)
                                   auth_string = base64.encodestring("%s:%s" % (username,password))
                                   req.add_header("Authorization", "Basic %s" % auth_string)
                                   f = urllib2.urlopen(req)
                                   response = f.read()
                                   countUser = response.count("<TR>") - 2
                                   if  countUser > 0:
                                        connectedUser += countUser
                              except:
                                    connectedUser += 0

                              # for VAP 5
                              try:
                                   url = "http://" + ip + "/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=5"
                                   req = urllib2.Request(url)
                                   auth_string = base64.encodestring("%s:%s" % (username,password))
                                   req.add_header("Authorization", "Basic %s" % auth_string)
                                   f = urllib2.urlopen(req)
                                   response = f.read()
                                   countUser = response.count("<TR>") - 2               
                                   if  countUser > 0:
                                        connectedUser += countUser
                              except:
                                    connectedUser += 0
               
                              # for VAP 6
                              try:
                                   url = "http://" + ip + "/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=6"
                                   req = urllib2.Request(url)
                                   auth_string = base64.encodestring("%s:%s" % (username,password))
                                   req.add_header("Authorization", "Basic %s" % auth_string)
                                   f = urllib2.urlopen(req)
                                   response = f.read()
                                   countUser = response.count("<TR>") - 2
                                   if  countUser > 0:
                                        connectedUser += countUser
                              except:
                                    connectedUser += 0

                              # for VAP 7
                              try:
                                   url = "http://" + ip + "/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=7"
                                   req = urllib2.Request(url)
                                   auth_string = base64.encodestring("%s:%s" % (username,password))
                                   req.add_header("Authorization", "Basic %s" % auth_string)
                                   f = urllib2.urlopen(req)
                                   response = f.read()
                                   countUser = response.count("<TR>") - 2
                                   if  countUser > 0:
                                        connectedUser += countUser
                              except:
                                    connectedUser += 0

                              # for VAP 8
                              try:
                                   url = "http://" + ip + "/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=8"
                                   req = urllib2.Request(url)
                                   auth_string = base64.encodestring("%s:%s" % (username,password))
                                   req.add_header("Authorization", "Basic %s" % auth_string)
                                   f = urllib2.urlopen(req)
                                   response = f.read()
                                   countUser = response.count("<TR>") - 2
                                   if  countUser > 0:
                                        connectedUser += countUser
                              except:
                                    connectedUser += 0

                              # insert details of conneced users
                              sql = "INSERT INTO nms_devices_connected_user(datestamp,timestamp,deviceid,noofuser) VALUES('%s','%s',%s,%s)" % (datestamp,timestamp,ap["id"],connectedUser)
                              cursor.execute(sql)
                              db.commit()



               else:
                    if ap["check"] == 1:
                         sql = "SELECT interface from nms_devices_current_bandwidth \
                                WHERE deviceid = %s" % (ap["id"])
                         cursor.execute(sql)
                         interfaceList = cursor.fetchall()
                         for inter in interfaceList:
                              sql = "SELECT tx,rx from nms_devices_delta_bandwidth \
                                     WHERE deviceid = %s AND interface = '%s' \
                                     ORDER BY id DESC LIMIT 0,1" % (ap["id"],inter[0])
                              cursor.execute(sql)
                              result = cursor.fetchall()
                              oldTx = 0
                              oldRx = 0
                              for row in result:
                                  oldTx = row[0]
                                  oldRx = row[1]
                              if oldTx < 0:
                                   tx = 0
                              else:
                                   tx = oldTx
                              if oldRx < 0:
                                   rx = 0
                              else:
                                   rx = oldRx
                              sql = "INSERT INTO nms_devices_delta_bandwidth (datestamp,timestamp,deviceid,interface,tx,rx) VALUES('%s','%s',%s,'%s',%s,%s)" % (datestamp,timestamp,ap["id"],inter[0],tx,rx)
                              cursor.execute(sql)
                              db.commit()
               # Insert uptime details
               if sysUptime == "":
                    sysUptime = "Down"
               sql = "SELECT COUNT(*) FROM nms_devices_uptime WHERE deviceid = %s" % (ap["id"])
               cursor.execute(sql)
               result = cursor.fetchall()
               countDevices = 0
               for row in result:
                    countDevices = row[0]
               if countDevices == 0:
                    sql = "INSERT INTO nms_devices_uptime(deviceid,uptime) VALUES(%s,'%s')" % (ap["id"],sysUptime)
               else:
                    sql = "UPDATE nms_devices_uptime SET uptime = '%s' WHERE deviceid = %s" % (sysUptime,ap["id"])

               cursor.execute(sql)
               db.commit()

               print commandResult
               
               #print "id: " + str(ap["id"]) + " ip: " + ap["address"] + " check: " + ap["check"] + "\n"

class AccessPointBandwidthMonitorThread(threading.Thread):
     def __init__(self,apbm):
          threading.Thread.__init__(self)
          self.apbm = apbm

     def run(self):
          while True:
               self.apbm.getAccessPointList()
               self.apbm.setSnmpValues()
               time.sleep(300)

if __name__ == "__main__": 
     try:
          apbm = AccessPointBandwidthMonitor()
          thr4 = AccessPointBandwidthMonitorThread(apbm)
          thr4.start()
     except:
          print "error"

