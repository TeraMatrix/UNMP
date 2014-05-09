#!/usr/bin/python
import urllib2, base64, sys, datetime, MySQLdb, os

# 30 1 * * * python /omd/daemon/scheduler/scheduling.py admin password -1 192.168.1.205 Down 0 -1
# m h D M w command username password port ip event re-Execute retry-id
arg = sys.argv

username = arg[1]
password = arg[2]
port = arg[3]
reExecute = arg[6]
retryId = arg[7]
tempUrl = ""
response = ""
message = ""
if arg[5] == "Up":
     tempUrl = "/cgi-bin/ServerFuncs?Method=EnableRadio"
elif arg[5] == "Down":
     tempUrl = "/cgi-bin/ServerFuncs?Method=DisableRadio"
else:
     tempUrl = "/cgi-bin/ServerFuncs?Method=RadioStatus"

url = "http://" + arg[4] + tempUrl


def delete_retry_entry(retryId):
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms")

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # prepare SQL query to create repeated schedule
     sql = "DELETE FROM repeat_ap_schedule WHERE repeatapscheduleid = %s" % (retryId)
     cursor.execute(sql)
     db.commit()

def create_retry_entry(ipAddress,message,event):
     now = datetime.datetime.now()
     now = now + datetime.timedelta(minutes = 5)
     datestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
     timestamp = str(now.hour) + ":" + str(now.minute) + ":00"

     i = 0
     deviceId = 0

     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms")

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # prepare SQL query to get deviceId
     sql = "SELECT id FROM nms_devices WHERE ipaddress = '%s'" % (ipAddress)
     cursor.execute(sql)
     result = cursor.fetchall()
     for row in result:
          deviceId = row[0]
          i += 1

     if i > 0:
          # prepare SQL query to create repeated schedule
          sql = "INSERT INTO repeat_ap_schedule (datestamp,timestamp,deviceid,message,event) VALUES('%s','%s',%s,'%s','%s')" % (datestamp,timestamp,deviceId,message,event)
          cursor.execute(sql)
          db.commit()

def create_crontab_file():
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms")
          
     commands = "python /omd/daemon/scheduler/scheduling.py "
     crontabString = ""
     commandString = ""
     event1 = "Down"
     event2 = "Up"
     apI1 = 0
     apI2 = 0
     try:
          # prepare a cursor object using cursor() method
          cursor = db.cursor()
          # prepare SQL query to create crontab
          sql = "SELECT * FROM schedule"
          cursor.execute(sql)
          result = cursor.fetchall()
          for row in result:
               apI1 = 0
               apI2 = 0
               if row[1] == "Down":
                    event1 = "Down"
                    event2 = "Up"
               else:
                    event1 = "Up"
                    event2 = "Down"
               sDate = str(row[2]).split("-")
               sTime = str(row[4]).split(":")
               eDate = str(row[3]).split("-")
               eTime = str(row[5]).split(":")
               now = datetime.datetime.now()
               sDateObj = datetime.datetime(int(sDate[0]),int(sDate[1]),int(sDate[2]),int(sTime[0]),int(sTime[1]),int(sTime[2]))
               eDateObj = datetime.datetime(int(eDate[0]),int(eDate[1]),int(eDate[2]),int(eTime[0]),int(eTime[1]),int(eTime[2]))

               if row[6] == 0:			# this is for non repeated scheduling
                    if sDateObj > now:
                         commandString = sTime[1] + " " + sTime[0] + " " + sDate[2] + " " + sDate[1] + " * "
                         sql = "SELECT nms_devices.ipaddress, nms_devices.username, nms_devices.password, nms_devices.port FROM ap_schedule \
                                INNER JOIN nms_devices on ap_schedule.deviceid = nms_devices.id \
                                WHERE ap_schedule.scheduleid = %s" % (row[0])
                         cursor.execute(sql)
                         apresult = cursor.fetchall()
                         port = "-1"
                         username = "username"
                         password = "password"
                         ip = "255.255.255.255"
                         for aprow in apresult:
                              if apI1 > 0:
                                   crontabString += " 0 -1\n"
                              if str(aprow[0]) != "":
                                   ip = str(aprow[0])
                              if str(aprow[1]) != "":
                                   username = str(aprow[1])
                              if str(aprow[2]) != "":
                                   password = str(aprow[2])
                              if str(aprow[3]).strip() != "":
                                   port = str(aprow[3]).strip()
                              crontabString += commandString + commands + username + " " + password + " " + port + " " + ip + " "  + event1
                              apI1 += 1
                         crontabString += " 1 -1\n"

                    if eDateObj > now:
                         commandString = eTime[1] + " " + eTime[0] + " " + eDate[2] + " " + eDate[1] + " * "
                         sql = "SELECT nms_devices.ipaddress, nms_devices.username, nms_devices.password, nms_devices.port FROM ap_schedule \
                                INNER JOIN nms_devices on ap_schedule.deviceid = nms_devices.id \
                                WHERE ap_schedule.scheduleid = %s" % (row[0])
                         cursor.execute(sql)
                         apresult = cursor.fetchall()
                         port = "-1"
                         username = "username"
                         password = "password"
                         ip = "255.255.255.255"
                         for aprow in apresult:
                              if apI2 > 0:
                                   crontabString += " 0 -1\n"
                              if str(aprow[0]) != "":
                                   ip = str(aprow[0])
                              if str(aprow[1]) != "":
                                   username = str(aprow[1])
                              if str(aprow[2]) != "":
                                   password = str(aprow[2])
                              if str(aprow[3]).strip() != "":
                                   port = str(aprow[3]).strip()
                              crontabString += commandString + commands + username + " " + password + " " + port + " " + ip + " " + event2
                              apI2 += 1
                         crontabString += " 1 -1\n"

               else:				# this is for repeated scheduling
                    if row[7] == "Daily":
                         commandString1 = sTime[1] + " " + sTime[0] + " * * * "
                         commandString2 = eTime[1] + " " + eTime[0] + " * * * "
                         sql = "SELECT nms_devices.ipaddress, nms_devices.username, nms_devices.password, nms_devices.port FROM ap_schedule \
                                INNER JOIN nms_devices on ap_schedule.deviceid = nms_devices.id \
                                WHERE ap_schedule.scheduleid = %s" % (row[0])
                         cursor.execute(sql)
                         apresult = cursor.fetchall()
                         port = "-1"
                         username = "username"
                         password = "password"
                         ip = "255.255.255.255"
                         for aprow in apresult:
                              if str(aprow[0]) != "":
                                   ip = str(aprow[0])
                              if str(aprow[1]) != "":
                                   username = str(aprow[1])
                              if str(aprow[2]) != "":
                                   password = str(aprow[2])
                              if str(aprow[3]).strip() != "":
                                   port = str(aprow[3]).strip()
                              crontabString += commandString1 + commands + username + " " + password + " " + port + " " + ip + " " + event1 + " 0 -1\n"
                              crontabString += commandString2 + commands + username + " " + password + " " + port + " " + ip + " " + event2 + " 0 -1\n"

                    elif row[7] == "Weekly":
                         sql = "SELECT nms_devices.ipaddress, nms_devices.username, nms_devices.password, nms_devices.port FROM ap_schedule \
                                INNER JOIN nms_devices on ap_schedule.deviceid = nms_devices.id \
                                WHERE ap_schedule.scheduleid = %s" % (row[0])
                         cursor.execute(sql)
                         apresult = cursor.fetchall()
                         port = "-1"
                         username = "username"
                         password = "password"
                         ip = "255.255.255.255"
                         dayI = 0
                         for aprow in apresult:
                              if str(aprow[0]) != "":
                                   ip = str(aprow[0])
                              if str(aprow[1]) != "":
                                   username = str(aprow[1])
                              if str(aprow[2]) != "":
                                   password = str(aprow[2])
                              if str(aprow[3]).strip() != "":
                                   port = str(aprow[3]).strip()

                              commandString1 = sTime[1] + " " + sTime[0] + " * * "
                              commandString2 = eTime[1] + " " + eTime[0] + " * * "
                              dayI = 0
                              if row[8] == 1:	# sunday
                                   if dayI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "0" 
                                   commandString2 += "0" 
                                   dayI += 1
                              if row[9] == 1:	# monday
                                   if dayI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "1" 
                                   commandString2 += "1"
                              if row[10] == 1:	# tuesday
                                   if dayI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "2" 
                                   commandString2 += "2" 
                                   dayI += 1
                              if row[11] == 1:	# wednusday
                                   if dayI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "3" 
                                   commandString2 += "3"
                                   dayI += 1
                              if row[12] == 1:	# thrusday
                                   if dayI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "4" 
                                   commandString2 += "4" 
                                   dayI += 1
                              if row[13] == 1:	# friday
                                   if dayI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "5" 
                                   commandString2 += "5" 
                                   dayI += 1
                              if row[14] == 1:	# saturday
                                   if dayI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "6" 
                                   commandString2 += "6" 
                                   dayI += 1

                              crontabString += commandString1 + " " + commands + username + " " + password + " " + port + " " + ip + " " + event1 + " 0 -1\n"
                              crontabString += commandString2 + " " + commands + username + " " + password + " " + port + " " + ip + " " + event2 + " 0 -1\n"

                    elif row[7] == "Monthly":
                         sql = "SELECT nms_devices.ipaddress, nms_devices.username, nms_devices.password, nms_devices.port FROM ap_schedule \
                                INNER JOIN nms_devices on ap_schedule.deviceid = nms_devices.id \
                                WHERE ap_schedule.scheduleid = %s" % (row[0])
                         cursor.execute(sql)
                         apresult = cursor.fetchall()
                         port = "-1"
                         username = "username"
                         password = "password"
                         ip = "255.255.255.255"
                         monthI = 0
                         for aprow in apresult:
                              if str(aprow[0]) != "":
                                   ip = str(aprow[0])
                              if str(aprow[1]) != "":
                                   username = str(aprow[1])
                              if str(aprow[2]) != "":
                                   password = str(aprow[2])
                              if str(aprow[3]).strip() != "":
                                   port = str(aprow[3]).strip()

                              monthI = 0
                              commandString1 = sTime[1] + " " + sTime[0] + " " + row[27] + " "
                              commandString2 = sTime[1] + " " + sTime[0] + " " + row[27] + " "
                              if row[15] == 1:	# jan
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "1" 
                                   commandString2 += "1"
                                   monthI += 1
                              if row[16] == 1:	# feb
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "2" 
                                   commandString2 += "2"
                                   monthI += 1
                              if row[17] == 1:	# mar
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "3" 
                                   commandString2 += "3"
                                   monthI += 1
                              if row[18] == 1:	# apr
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "4" 
                                   commandString2 += "4" 
                                   monthI += 1
                              if row[19] == 1:	# may
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "5" 
                                   commandString2 += "5" 
                                   monthI += 1
                              if row[20] == 1:	# jun
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "6" 
                                   commandString2 += "6" 
                                   monthI += 1
                              if row[21] == 1:	# jul
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "7" 
                                   commandString2 += "7" 
                                   monthI += 1
                              if row[22] == 1:	# aug
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "8" 
                                   commandString2 += "8" 
                                   monthI += 1
                              if row[23] == 1:	# sep
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "9" 
                                   commandString2 += "9" 
                                   monthI += 1
                              if row[24] == 1:	# oct
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "10" 
                                   commandString2 += "10" 
                                   monthI += 1
                              if row[25] == 1:	# nov
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "11" 
                                   commandString2 += "11" 
                                   monthI += 1
                              if row[26] == 1:	# dec
                                   if monthI > 0:
                                        commandString1 += ","
                                        commandString2 += ","
                                   commandString1 += "12" 
                                   commandString2 += "12" 
                                   monthI += 1

                              crontabString += commandString1 + " * " + commands + username + " " + password + " " + port + " " + ip + " " + event1 + " 0 -1\n"
                              crontabString += commandString2 + " * " + commands + username + " " + password + " " + port + " " + ip + " " + event2 + " 0 -1\n"

          # prepare SQL query to create crontab
          sql = "SELECT repeat_ap_schedule.repeatapscheduleid, repeat_ap_schedule.datestamp, repeat_ap_schedule.timestamp, nms_devices.ipaddress, nms_devices.username, nms_devices.password, nms_devices.port, repeat_ap_schedule.message, repeat_ap_schedule.event FROM repeat_ap_schedule \
                 INNER JOIN nms_devices on repeat_ap_schedule.deviceid = nms_devices.id"
          cursor.execute(sql)
          result = cursor.fetchall()
          for row in result:
               port = "-1"
               username = "username"
               password = "password"
               ip = "255.255.255.255"
               event = "Unknown"

               sDate = str(row[1]).split("-")
               sTime = str(row[2]).split(":")
               commandString = sTime[1] + " " + sTime[0] + " " + sDate[2] + " " + sDate[1] + " * "

               if str(row[3]) != "":
                    ip = str(row[3])
               if str(row[4]) != "":
                    username = str(row[4])
               if str(row[5]) != "":
                    password = str(row[5])
               if str(row[6]).strip() != "":
                    port = str(row[6]).strip()
               if str(row[8]).strip() != "":
                    event = str(row[8]).strip()
               crontabString += commandString + commands + username + " " + password + " " + port + " " + ip + " "  + event + " 1 " + str(row[0]) + "\n"

          fobj = open("/omd/daemon/scheduler/crontab","w")
          fobj.write(crontabString)
          fobj.close()
     except:
          error = "some error occur"
     db.close()


try:
     req = urllib2.Request(url)
     auth_string = base64.encodestring("%s:%s" % (username,password))
     req.add_header("Authorization", "Basic %s" % auth_string)
     f = urllib2.urlopen(req)
     response = f.read()
except urllib2.HTTPError, e:
     response = str(e.code)	# send http error code
except:
     response = "Network Unreachable"


if retryId != "-1":
     delete_retry_entry(retryId)

if response == "Enable Radio Request Received":
     message = "Enable"
     if reExecute == "1" or retryId != "-1":
          create_crontab_file()
elif response == "Disable  Request Received":
     message = "Disable"
     if reExecute == "1" or retryId != "-1":
          create_crontab_file()
elif response == "400":
     message = "Bad Request"
     create_retry_entry(arg[4],message,arg[5])
     create_crontab_file()
elif response == "401":
     message = "User name and Password are wrong"
     create_retry_entry(arg[4],message,arg[5])
     create_crontab_file()
elif response == "404":
     message = "File Not Found"
     create_retry_entry(arg[4],message,arg[5])
     create_crontab_file()
elif response == "501":
     message = "Server Error"
     create_retry_entry(arg[4],message,arg[5])
     create_crontab_file()
else:
     message = "Access Point not connected"
     create_retry_entry(arg[4],message,arg[5])
     create_crontab_file()


