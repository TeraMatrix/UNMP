#!/usr/bin/python2.6

import config, htmllib, pprint, sidebar, views, time, defaults, os, cgi, xml.dom.minidom, subprocess, commands, MySQLdb, datetime
from lib import *
from nms_config import *

############################################ NMS Dashboard ######################################
def nms_dashboard(h):
     global html
     html = h
     html.new_header("Dashboard")
     html.write("<script type=\"text/javascript\" src=\"js/jquery-1.4.4.min.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/highcharts.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/jquery.validate.min.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/dashboard.js\"></script>\n")
     html.write("<link type=\"text/css\" href=\"css/style.css\" rel=\"stylesheet\"></link>\n")
     html.write("<input type=\"hidden\" id=\"systemGraphNum\" name=\"systemGraphNum\" value=\"1\"/>")
     html.write("<input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\"/>" % (get_refresh_time()))
     html.write("<table style=\"margin-bottom: 0px;\" class=\"addform\" id=\"apGraphHead\"><colgroup><col width=\"auto\"><col width=\"1%\"><col width=\"5%\"></colgroup><tbody><tr><th>Access Point Bandwidth</th><th>")
     html.write("<img class=\"imgbuttondisable\" src=\"images/previous.png\" alt=\"previous\" title=\"Previous Access Points\" onclick=\"accessPointGraphs('previous');\" style=\"float:right;width:16px;\" id=\"previousAP\"/></th><th>")
     html.write("<img class=\"imgbuttondisable\" src=\"images/next.png\" alt=\"next\" title=\"Next Access Points\" onclick=\"accessPointGraphs('next');\" style=\"float:right;width:16px;\" id=\"nextAP\"/>")
     html.write("</tr></tbody></table>")
     html.write("<div style=\"width:95%;height:250px;float:left;\" id=\"apGraph\"></div>")
     html.write("<table style=\"margin-bottom: 0px;\" class=\"addform\" id=\"apUserGraphHead\"><colgroup><col width=\"auto\"><col width=\"1%\"><col width=\"5%\"></colgroup><tbody><tr><th>Access Point Connected User</th><th>")
     html.write("<img class=\"imgbuttondisable\" src=\"images/previous.png\" alt=\"previous\" title=\"Previous Access Points\" onclick=\"accessPointUserGraphs('previous');\" style=\"float:right;width:16px;\" id=\"previousAPUser\"/></th><th>")
     html.write("<img class=\"imgbuttondisable\" src=\"images/next.png\" alt=\"next\" title=\"Next Access Points\" onclick=\"accessPointUserGraphs('next');\" style=\"float:right;width:16px;\" id=\"nextAPUser\"/>")
     html.write("</tr></tbody></table>")
     html.write("<div style=\"width:95%;height:350px;float:left;\" id=\"apUserGraph\"></div>")

     html.write("<table style=\"margin-bottom: 0px;\" class=\"addform\"><tr><th>System Details</th></tr></table>")
     html.write("<div style=\"width:45%;float:left;margin-left:1%;\">")
     html.write("<div class=\"tab-yo\" style=\"margin:0 10px 15px;\">")
#     html.write("<div class=\"tab-head\">")
#     html.write("<h2>System Details")
#     html.write("</h2>")
#     html.write("</div>")
     html.write("<div class=\"tab-body\">")
     html.write("<table style=\"width:100%;margin-top:10px;\" cellpadding=\"2\">")
     html.write("<colgroup><col width='25%'/><col width='60%'/><col width='15%'/></colgroup>")
     html.write("<tr><td style=\"padding:5px 10px;font-weight:bold;\">Uptime</td><td id=\"upTimeDetails\">")
     system_uptime(h)
     html.write("</td><td></td></tr>")
     html.write("<tr><td style=\"padding:5px 10px;font-weight:bold;\">Memory</td><td id=\"hdDetails\"></td><td><a href=\"javascript:harddiskDetailsClick();\"><img src=\"images/pie-chart-icon.png\" alt=\"Graph\" title=\"Graph\"/></a></td></tr>")
     html.write("<tr><td style=\"padding:5px 10px;font-weight:bold;\">RAM</td><td id=\"rmDetails\"></td><td><a href=\"javascript:ramDetailsClick();\"><img src=\"images/pie-chart-icon.png\" alt=\"Graph\" title=\"Graph\"/></a></td></tr>")
     html.write("<tr><td style=\"padding:5px 10px;font-weight:bold;\">Processor</td><td id=\"proDetails\"></td><td><a href=\"javascript:proDetails();\"><img src=\"images/pie-chart-icon.png\" alt=\"Graph\" title=\"Graph\"/></a></td></tr>")
     html.write("<tr><td style=\"padding:5px 10px;font-weight:bold;\">Bandwidth</td><td id=\"interface1Details\"></td><td><a href=\"javascript:bandDetails(1);\"><img src=\"images/pie-chart-icon.png\" alt=\"Graph\"/ title=\"Graph\"></a></td></tr>")
     html.write("<tr style=\"display:none;\" id=\"interface2\"><td></td><td id=\"interface2Details\"></td><td><a href=\"javascript:bandDetails(2);\"><img src=\"images/pie-chart-icon.png\" alt=\"Graph\" title=\"Graph\"/></a></td></tr>")
     html.write("</table>")
     html.write("</div>")
     html.write("</div>")
     html.write("</div>")
     html.write("<div style=\"width:50%;float:left;height:200px;\" id=\"nmsGraph\"></div>")
     html.footer()
     html.write("<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")

def harddisk_details(h):
     global html
     html = h
     details = commands.getoutput("df /").split("\n")
     if len(details) > 1:
          harddisk = details[1].split()
          if len(harddisk) > 5:
               print "Directory: " + harddisk[5]
               total = float(harddisk[1])/(1024*1024)
               free = float(float(harddisk[1])-float(harddisk[2]))/(1024*1024)
               available = float(harddisk[3])/(1024*1024)
               used = float(harddisk[2])/(1024*1024)
               html.write(str('%.2f' %total) + "," + str('%.2f' %free) + "," + str('%.2f' %available) + "," + str('%.2f' %used))

def system_uptime(h):
     global html
     html = h
     details = commands.getoutput("uptime")
     sysTime = details.split()[0]
     uptime = ""
     #print "System Time: " + sysTime

     # get uptime of system
     uptimedetails = details.split("users")
     uptimedetails = uptimedetails[0].split("up")
     uptimedetails = uptimedetails[1].split(",")
     for i in range(0,len(uptimedetails)-1):
          uptime += uptimedetails[i]
     html.write(uptime.strip())

def ram_details(h):
     global html
     html = h
     usedMemory = 0
     freeMemory = 0
     details = commands.getoutput("free -m -t").split("\n")
     if len(details) > 2:
          ram = details[2].split()
          if len(ram) > 2:
               usedMemory = float(ram[2])
               freeMemory = float(ram[3])
          else:
               usedMemory = 0
               freeMemory = 0
     else:
          usedMemory = 0
          freeMemory = 0
     html.write(str(usedMemory) + "," + str(freeMemory))

def processor_details(h):
     global html
     html = h
     now = datetime.datetime.now()
     now = now + datetime.timedelta(minutes = -30)
     datestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
     timestamp = str(now.hour) + ":" + str(now.minute) + ":00"
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # Prepare SQL query to INSERT a record into the database.
     sql = "SELECT * FROM nms_processor \
       WHERE datestamp = '%s' AND timestamp > '%s'" % (datestamp,timestamp)
     jsonData = "{processor:["
     try:
          # Execute the SQL command
          cursor.execute(sql)
          # Fetch all the rows in a list of lists.
          results = cursor.fetchall()
          i = 0
          for row in results:
               if i > 0:
                    jsonData += ","
               jsonData += "{id:" + str(row[0]) + ",datestamp:\"" + str(row[1]) + "\",timestamp:\"" + str(row[2]) + "\",cpuusage:" + str(row[3]) + "}"
               i += 1
          jsonData += "]}"
          html.write(jsonData)
     except:
          html.write("{processor:[]}")

     # disconnect from server
     db.close()

def processor_last_details(h):
     global html
     html = h
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # Prepare SQL query to INSERT a record into the database.
     sql = "SELECT * FROM nms_processor \
            ORDER BY id DESC LIMIT 0,1"
     jsonData = "{processor:["
     try:
          # Execute the SQL command
          cursor.execute(sql)
          # Fetch all the rows in a list of lists.
          results = cursor.fetchall()
          i = 0
          for row in results:
               if i > 0:
                    jsonData += ","
               jsonData += "{id:" + str(row[0]) + ",datestamp:\"" + str(row[1]) + "\",timestamp:\"" + str(row[2]) + "\",cpuusage:" + str(row[3]) + "}"
               i += 1
          jsonData += "]}"
          html.write(jsonData)
     except:
          html.write("{processor:[]}")

     # disconnect from server
     db.close()

def bandwidth_last_details(h):
     global html
     html = h
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # Prepare SQL query to INSERT a record into the database.
     sql = "SELECT * FROM nms_bandwidth \
            ORDER BY id DESC LIMIT 0,2 "
     jsonData = "{bandwidth:["
     try:
          # Execute the SQL command
          cursor.execute(sql)
          # Fetch all the rows in a list of lists.
          results = cursor.fetchall()
          i = 0
          for row in results:
               if i > 0:
                    jsonData += ","
               jsonData += "{id:" + str(row[0]) + ",datestamp:\"" + str(row[1]) + "\",timestamp:\"" + str(row[2]) + "\",inter:\"" + str(row[3]) + "\",tx:"+ str(row[4]) + ",rx:" + str(row[5]) + "}"
               i += 1
          jsonData += "]}"
          html.write(jsonData)
     except:
          html.write("{bandwidth:[]}")

     # disconnect from server
     db.close()

def bandwidth_details(h):
     global html
     html = h
     interface = html.var("inter")
     now = datetime.datetime.now()
     now = now + datetime.timedelta(minutes = -10)
     datestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
     timestamp = str(now.hour) + ":" + str(now.minute) + ":00"
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # Prepare SQL query to INSERT a record into the database.
     sql = "SELECT * FROM nms_bandwidth \
       WHERE datestamp = '%s' AND timestamp > '%s' AND interface = '%s'" % (datestamp,timestamp,interface)
     jsonData = "{bandwidth:["
     try:
          # Execute the SQL command
          cursor.execute(sql)
          # Fetch all the rows in a list of lists.
          results = cursor.fetchall()
          i = 0
          for row in results:
               if i > 0:
                    jsonData += ","
               jsonData += "{id:" + str(row[0]) + ",datestamp:\"" + str(row[1]) + "\",timestamp:\"" + str(row[2]) + "\",inter:\"" + str(row[3]) + "\",tx:"+ str(row[4]) + ",rx:" + str(row[5]) + "}"
               i += 1
          jsonData += "]}"
          html.write(jsonData)
     except:
          html.write("{bandwidth:[]}")

     # disconnect from server
     db.close()

def get_number_of_aps(h):
     global html
     html = h
     totalAccessPoint = 0
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()
     
     # prepare SQL query to get total number of access points in this system
     sql = "SELECT COUNT(*) FROM nms_devices \
            WHERE devicetype = 'AP'"
     cursor.execute(sql)
     result = cursor.fetchall()
     for row in result:
          totalAccessPoint = row[0]
     html.write(str(totalAccessPoint))

def ap_graph(h):
     global html
     html = h
     start = html.var("start")
     limit = html.var("limit")
     refresh_time = get_refresh_time()
     device_type = "AP"
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()
     
     # prepare SQL query to get total number of access points in this system
     # 1 is time diffrence (1 minute)
     cursor.callproc("dashboard_ap_graph",(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),refresh_time,device_type,start,limit))
     result = cursor.fetchall()
     name = ""
     tx = ""
     rx = ""
     totalTx = 0.0
     totalRx = 0.0
     avrg = ""
     i = 0
     for row in result:
          if row[5] == "eth0":
               tx_value = float(row[3]/(float(refresh_time)*60.0*1024))
               rx_value = float(row[4]/(float(refresh_time)*60.0*1024))
               if i > 0:
                    name += ","
                    tx += ","
                    rx += ","
                    avrg += ","
               name += "\"" + str(row[1]) + "\""
               totalTx += tx_value
               totalRx += rx_value
               tx += "%.2f" % float(tx_value)
               rx += "%.2f" % float(rx_value)
               avrg += "%.2f" % float((tx_value + rx_value)/2.0)
               i += 1
     jsonData = "{"
     jsonData += "name:[" + name + "],"
     jsonData += "tx:[" + tx + "],"
     jsonData += "rx:[" + rx + "],"
     jsonData += "totalTx:%.2f," % (totalTx)
     jsonData += "totalRx:%.2f," % (totalRx)
     jsonData += "avrg:[" + avrg + "]"
     jsonData += "}"
     html.write(jsonData);

def ap_user_graph(h):
     global html
     html = h
     start = html.var("start")
     limit = html.var("limit")
     refresh_time = get_refresh_time()
     device_type = "AP"
     now = datetime.datetime.now() #datetime.timedelta(minutes = -10)
     start_time = now.strftime('%Y-%m-%d %H:%M:%S')
     now = now + datetime.timedelta(minutes = -int(refresh_time))
     end_time = now.strftime('%Y-%m-%d %H:%M:%S')
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()
     
     # prepare SQL query to get total number of access points in this system
     sql = "SELECT nms_devices.id,nms_devices.ipaddress,count(nms_devices_connected_user.mac) \
            FROM nms_devices_connected_user RIGHT JOIN nms_devices on nms_devices.id = nms_devices_connected_user.deviceid \
            AND timestamp BETWEEN '%s' and '%s' WHERE devicetype = '%s' group by nms_devices.id LIMIT %s,%s;" % (end_time,start_time,device_type,start,limit)
     cursor.execute(sql)
     result = cursor.fetchall()
     name = ""
     user = ""
     i = 0
     for row in result:
          if i > 0:
               name += ","
               user += ","
          name += "\"" + str(row[1]) + "\""
          user += str(row[2])
          i += 1
     jsonData = "{"
     jsonData += "name:[" + name + "],"
     jsonData += "user:[" + user + "]"
     jsonData += "}"
     html.write(jsonData);

############################################ End NMS Dashboard ######################################

############################################ AP Dashboard ######################################
def ap_dashboard(h):
     global html
     html = h
     html.new_header("AP Dashboard")
     html.write("<script type=\"text/javascript\" src=\"js/jquery-1.4.4.min.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/highcharts.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/jquery.validate.min.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/ap_dashboard.js\"></script>\n")
     html.write("<link type=\"text/css\" href=\"css/style.css\" rel=\"stylesheet\"></link>\n")
     # create tabs for manage configuration
     html.write("<div class=\"tab-yo\">")
     html.write("<div class=\"tab-head\">")
     html.write("<h2 id=\"ap_name\">Access Point")
     html.write("<input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\" />" % get_refresh_time())
     html.write("</h2>")
     html.write("<div id=\"ap_details\" style=\"float:right;font-size:10px;color:#555;font-weight:bold;padding:10px 20px;\"></div>")
     html.write("</div>")
     
     # graph division
     html.write("<div id=\"ap_graph_div\" class=\"tab-body\" style=\"overflow: auto;padding-top:20px;\">")
     html.write("<table class=\"addform teth0\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"eth0\"></div></td></tr></table>")
     #html.write("")
     html.write("<table class=\"addform tbr0\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"br0\"></div></td></tr></table>")
     html.write("<table class=\"addform tath0\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"ath0\"></div></td></tr></table>")
     html.write("<table class=\"addform tath1\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"ath1\"></div></td></tr></table>")
     html.write("<table class=\"addform tath2\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"ath2\"></div></td></tr></table>")
     html.write("<table class=\"addform tath3\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"ath3\"></div></td></tr></table>")
     html.write("<table class=\"addform tath4\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"ath4\"></div></td></tr></table>")
     html.write("<table class=\"addform tath5\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"ath5\"></div></td></tr></table>")
     html.write("<table class=\"addform tath6\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"ath6\"></div></td></tr></table>")
     html.write("<table class=\"addform tath7\" style=\"display:none;\"><tr><td class=\"button\"><div style=\"width:98%;height:180px;\" id=\"ath7\"></div></td></tr></table>")
     html.write("<p id=\"msg\"></p>")
     html.write("<div id='apTableDiv' style=\"width:100%;\"></div>")
     html.write("<div style=\"clear:both;float:left;width:98%;\" id=\"connectedUserDiv\"></div>")
     html.write("</div>")
     html.write("</div>")
     html.footer()
     html.write("<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")
     html.new_footer()

def ap_interfaces(h):
     global html
     html = h
     apIp = html.var("apIp")
     now = datetime.datetime.now()
     refresh_time = get_refresh_time()
     now2 = now + datetime.timedelta(minutes = -10*int(refresh_time))

     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # get Interfaces Name
     sql = "select interface from nms_devices_bandwidth inner join nms_devices on nms_devices_bandwidth.deviceid = nms_devices.id where nms_devices.ipaddress = '%s' group by interface" % (apIp)
     cursor.execute(sql)
     interfaceList = cursor.fetchall()
     cursor.close()
     apString = "{"
     i = 0
     for inter in interfaceList:
          cursor = db.cursor()
          if i > 0:
               apString += ","
          apString += inter[0] + ":["
          cursor.callproc("ap_interface_graph",(now.strftime('%Y-%m-%d %H:%M:%S'),now2.strftime('%Y-%m-%d %H:%M:%S'), refresh_time,inter[0],apIp))
          interResult = cursor.fetchall()
          cursor.close()
          j = 0
          txrxString = ""
          for txrx in interResult:
               if j > 0:
                    txrxString += ","
               txrxString += "{timestamp:\"%s\", tx:%.2f, rx:%.2f }" % (txrx[3],float(txrx[2]/(int(refresh_time)*60.0*1024)),float(txrx[1]/(int(refresh_time)*60.0*1024)))
               j += 1
          apString += txrxString + "]"
          i += 1
     apString += "}"
     html.write(apString)


def get_uptime_connected_client(h):
     global html
     html = h
     ip_address = html.var("ap_ip")
     uptime = "Down"
     clients = 0
     refresh_time = get_refresh_time()
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # create query to get uptime
     sql = "select uptime from nms_devices_uptime inner join nms_devices on nms_devices.id = nms_devices_uptime.deviceid where nms_devices.ipaddress = '%s'" % (ip_address)
     cursor.execute(sql)
     result = cursor.fetchall()
     for row in result:
          uptime = row[0]
     cursor.close()

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # create query to get currently connected clients
     sql = "select count(mac) from nms_devices_connected_user inner join nms_devices on nms_devices.id = nms_devices_connected_user.deviceid where nms_devices.ipaddress = '%s' AND timestamp BETWEEN now()-INTERVAL %s MINUTE AND now();" % (ip_address,refresh_time)
     cursor.execute(sql)
     clients = cursor.fetchone()[0]
     html.write("{uptime:\"%s\",clients:\"%s\"}" % (uptime,clients))

def access_point_details_table(h):
     global html
     html = h
     start = 0
     limit = 10000
     refresh_time = get_refresh_time()
     device_type = "AP"
     jsonString = ""
     apId = ""
     apId2 = ""
     ap = ""
     upTime = ""
     connectedUser = ""
     interfaces = ""

     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()
     
     # prepare SQL query to get total number of access points in this system
     # 1 is time diffrence (1 minute)
     cursor.callproc("dashboard_ap_graph",(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),refresh_time,device_type,start,limit))
     result = cursor.fetchall()
     count = count_i = 0
     for row in result:
          if apId2 != row[0]:
               apId2 = row[0]
               if count > 0:
                    apId += ","
                    ap += ","
                    interfaces += "},{"
               else:
                    interfaces += "{"
               apId += str(row[0])
               ap += "'%s'" % str(row[1])
               count += 1
               count_i = 0
          if count_i > 0:
               interfaces += ","
          interfaces += "%s:[%.2f,%.2f]" % (row[5],float(row[3]/(int(refresh_time)*60.0*1024)),float(row[4]/(int(refresh_time)*60.0*1024)))
          count_i += 1
     if count_i > 0:
          interfaces += "}"
     jsonString = "{apId:[" + apId + "],ap:[" + ap + "],upTime:[" + upTime + "],connectedUser:[" + connectedUser + "],interfaces:[" + interfaces + "]}" 
     html.write(jsonString)

############################################ End AP Dashboard ######################################

############################################ AP Clients Dashboard ######################################
def ap_clients_dashboard(h):
     global html
     html = h
     html.new_header("AP Clients Dashboard")
     html.write("<script type=\"text/javascript\" src=\"js/jquery-1.4.4.min.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/highcharts.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/grid.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/jquery.validate.min.js\"></script>\n")
     html.write("<script type=\"text/javascript\" src=\"js/ap_clients_dashboard.js\"></script>\n")
     html.write("<link type=\"text/css\" href=\"css/style.css\" rel=\"stylesheet\"></link>\n")
     # create tabs for manage configuration
     html.write("<div class=\"tab-yo\">")
     html.write("<div class=\"tab-head\">")
     html.write("<h2 id=\"ap_name\">Access Point Clients")
     html.write("<input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\" />" % get_refresh_time())
     html.write("</h2>")

     # get total number of access point in  this system
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # prepare a query to get number of aps
     sql = "SELECT COUNT(*) from nms_devices WHERE devicetype = 'AP'"
 
     cursor.execute(sql)
     html.write("<div id=\"ap_details\" style=\"float:right;font-size:10px;color:#555;font-weight:bold;padding:10px 20px;\">Total Access Points: %s</div>" % cursor.fetchone()[0])
     html.write("</div>")
     
     # graph division
     html.write("<div id=\"ap_graph_div\" class=\"tab-body\" style=\"overflow: auto;padding-top:10px;\">")
     html.write("<div id=\"bandwidth_graph_div\" style=\"height:210px;margin:10px;\"></div>")
     #html.write("<div id=\"bandwidth_pie_graph_div\" style=\"width:26%;height:200px;margin:10px;\"></div>")
     html.write("<div id=\"client_div\">")
     ap_connected_user(h)
     html.write("</div>")
     html.write("</div>")
     html.write("</div>")


def ap_connected_user(h):
     global html
     html = h
     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()
     
     # prepare SQL query to get total access points in this system
     sql = "select a.id,a.ipaddress, b.mac,b.timestamp,b.create_timestamp, b.vap, IF(b.timestamp>(now()-INTERVAL 1 MINUTE),0,1) from nms_devices a inner join nms_devices_connected_user as b on a.id = b.deviceid"
     cursor.execute(sql)
     result = cursor.fetchall()
     i = 0
     html.write("<table class=\"addform\">")
     html.write("<colgroup><col width='3%'/><col width='7%'/><col width='30%'/><col width='30%'/><col width='20%'/><col width='10%'/></colgroup>")
     html.write("<tr><th>S.No</th><th>Status</th><th>Client Mac</th><th>Recent Access Point</th><th>Last seen</th><th>Interface</th></tr>")
     for row in result:
          status = "<img width=\"10px\" alt=\"1\" src=\"images/status-2.png\">"
          if int(row[6]) == 0:
               status = "<img width=\"10px\" alt=\"0\" src=\"images/status-0.png\">"
          html.write("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>ath%s</td></tr>" % ((i+1),status,row[2],row[1],row[3],(int(row[5])-1)))
          i += 1
     if i == 0:
          html.write("<tr><td colspan='6'> No Client Exist</td></tr>")
     html.write("</table>")

def get_overall_bandwidth(h):
     global html
     html = h
     now = datetime.datetime.now()
     refresh_time = get_refresh_time()
     now2 = now + datetime.timedelta(minutes = - 60*int(refresh_time))

     # Open database connection
     db = MySQLdb.connect("localhost","root","root","nms" )

     # prepare a cursor object using cursor() method
     cursor = db.cursor()

     # get_overall_bandwidth(now(),now() - INTERVAL 20 MINUTE,1,'eth0','AP')
     cursor.callproc("get_overall_bandwidth",(now.strftime('%Y-%m-%d %H:%M:%S'),now2.strftime('%Y-%m-%d %H:%M:%S'), refresh_time,'eth0','AP'))
     result = cursor.fetchall()
     cursor.close()
     tx = ""
     rx = ""
     i = 0
     for row in result:
          if i > 0:
               tx += ","
               rx += ","
          tx += "%.2f" % float(row[1]/(int(refresh_time)*60.0*1024))
          rx += "%.2f" % float(row[2]/(int(refresh_time)*60.0*1024))
          i += 1
     html.write("{tx:[%s],rx:[%s]}" % (tx,rx))


############################################ End AP Clients Dashboard ######################################
