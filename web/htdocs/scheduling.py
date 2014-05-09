#!/usr/bin/python2.6

import base64
import datetime
import socket
import urllib2

import MySQLdb

from lib import *


################################## Scheduling ############################


def ap_scheduling(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/style.css", "facebox/facebox.css",
                "calendrical/calendrical.css", "fullcalendar/fullcalendar.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "fullcalendar/fullcalendar.min.js",
        "facebox/facebox.js", "calendrical/calendrical.js", "js/unmp/main/ap_scheduling.js"]
    html.new_header("Access Point Scheduling", "", "", css_list, js_list)
    html.write(
        "<div id='calendar' style=\"width:900px;margin:0 auto;\"></div>")
    html.write("<div id=\"eventForm\" style=\"display:none;margin:10px;\">")
    html.write("<form id=\"schedulingForm\">")
    html.write("<table width=\"100%\">")
    html.write("<colgroup><col width='20%'/><col width='80%'/></colgroup>")
    html.write("<tr>")
    html.write(
        "<td>Event<input type=\"hidden\" id=\"scheduleId\" name=\"scheduleId\" value=\"0\" /></td>")
    html.write("<td>")
    html.write(
        "<input type=\"radio\" id=\"radioDown\" name=\"radio\" value=\"Down\" checked/>")
    html.write("<label for=\"radioDown\">Down</label>")
    html.write(
        "<input type=\"radio\" id=\"radioUp\" name=\"radio\" value=\"Up\"/>")
    html.write("<label for=\"radioUp\">UP</label>")
    html.write("</td>")
    html.write("</tr>")

    html.write("<tr>")
    html.write("<td>Range</td>")
    html.write("<td>")
    html.write(
        "<input type=\"text\" id=\"startDate\" name=\"startDate\" /> <input type=\"text\" id=\"startTime\" name=\"startTime\" style=\"width:100px;\" /> To")
    html.write(
        " <input type=\"text\" id=\"endDate\" name=\"endDate\" /> <input type=\"text\" id=\"endTime\" name=\"endTime\" style=\"width:100px;\" />")
    html.write(
        "<label style=\"color:red;display:none;\" id=\"dateError\"> Please enter correct date time range</label>")
    html.write("</td>")
    html.write("</tr>")

    html.write("<tr>")
    html.write("<td>Repeat</td>")
    html.write("<td>")
    html.write(
        "<input type=\"checkbox\" id=\"repeat\" name=\"repeat\" value=\"1\" />")
    html.write("</td>")
    html.write("</tr>")

    html.write("<tr id=\"trRepeatType\" style=\"display:none;\">")
    html.write("<td>Repeat Type</td>")
    html.write("<td>")
    html.write("<select id=\"repeatType\" name=\"repeatType\">")
    html.write("<option value=\"Daily\">Daily</option>")
    html.write("<option value=\"Weekly\">Weekly</option>")
    html.write("<option value=\"Monthly\">Monthly</option>")
    html.write("</select>")
    html.write("</td>")
    html.write("</tr>")

    html.write("<tr id=\"trDay\" style=\"display:none;\">")
    html.write("<td></td>")
    html.write("<td>")
    html.write(" <input type=\"checkbox\" id=\"daysun\" name=\"daysun\" value=\"1\" class=\"day\" />")
    html.write(" <label for=\"daysun\">S</label>")
    html.write(
        " <input type=\"checkbox\" id=\"daymon\" name=\"daymon\" value=\"1\" class=\"day\"/>")
    html.write(" <label for=\"daymon\">M</label>")
    html.write(
        " <input type=\"checkbox\" id=\"daytue\" name=\"daytue\" value=\"1\" class=\"day\"/>")
    html.write(" <label for=\"daytue\">T</label>")
    html.write(
        " <input type=\"checkbox\" id=\"daywed\" name=\"daywed\" value=\"1\" class=\"day\"/>")
    html.write(" <label for=\"daywed\">W</label>")
    html.write(
        " <input type=\"checkbox\" id=\"daythu\" name=\"daythu\" value=\"1\" class=\"day\"/>")
    html.write(" <label for=\"daythu\">T</label>")
    html.write(
        " <input type=\"checkbox\" id=\"dayfri\" name=\"dayfri\" value=\"1\" class=\"day\"/>")
    html.write(" <label for=\"dayfri\">F</label>")
    html.write(
        " <input type=\"checkbox\" id=\"daysat\" name=\"daysat\" value=\"1\" class=\"day\"/>")
    html.write(" <label for=\"daysat\">S</label>")
    html.write("</td>")
    html.write("</tr>")

    html.write("<tr id=\"trDate\" style=\"display:none;\">")
    html.write("<td></td>")
    html.write("<td>Dates: <select id=\"dates\" name=\"dates\">")
    for k in range(1, 32):
        html.write("<option value=\"" + str(k) + "\">" + str(k) + "</option>")
    html.write("</select></td>")
    html.write("</tr>")

    html.write("<tr id=\"trMonth\" style=\"display:none;\">")
    html.write("<td></td>")
    html.write("<td>")
    html.write("Months:<br/>")
    html.write(
        " <input type=\"checkbox\" id=\"monthjan\" name=\"monthjan\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthjan\">Jan</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthfeb\" name=\"monthfeb\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthfeb\">Feb</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthmar\" name=\"monthmar\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthmar\">Mar</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthapr\" name=\"monthapr\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthapr\">Apr</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthmay\" name=\"monthmay\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthmay\">May</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthjun\" name=\"monthjun\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthjun\">Jun</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthjul\" name=\"monthjul\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthjul\">Jul</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthaug\" name=\"monthaug\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthaug\">Aug</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthsep\" name=\"monthsep\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthsep\">Sep</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthoct\" name=\"monthoct\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthoct\">Oct</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthnov\" name=\"monthnov\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthnov\">Nov</label>")
    html.write(
        " <input type=\"checkbox\" id=\"monthdec\" name=\"monthdec\" value=\"1\" class=\"month\"/>")
    html.write(" <label for=\"monthdec\">Dec</label>")
    html.write("</td>")
    html.write("</tr>")

    html.write("<tr>")
    html.write("<td>Access Point</td>")
    html.write("<td>")
    html.write(access_point_multiple_select_list("", "AccessPoint"))
    html.write("</td>")
    html.write("</tr>")

    html.write("<tr>")
    html.write("<td>")
    html.write("</td>")
    html.write("<td>")
    html.write(
        "<input type=\"button\" id=\"submitEve\" onclick=\"eventSubmit()\" value=\"Submit\" />")
    html.write(
        "<input type=\"button\" id=\"updateEve\" style=\"display:none;\" onclick=\"eventUpdate()\" value=\"Update\" />")
    html.write(
        "<input type=\"button\" onclick=\"eventCancel()\" value=\"Cancel\" />")
    html.write("</td>")
    html.write("</tr>")

    html.write("</table>")
    html.write("</form>")
    html.write("</div>")
    html.footer()
    html.write("<div class=\"loading\"></div>")
    html.write(
        "<div class=\"calender-pop-up\" style=\"min-height:20px;width:150px;\" id=\"cEvent\"><a href=\"javascript:createEvent();\">Create Event</a></div>")
    html.write(
        "<div class=\"calender-pop-up\" id=\"dEvent\"><input type=\"hidden\" id=\"scheduleId\" name=\"scheduleId\" value=\"0\" /><a href=\"#viewApDiv\" id=\"showAP\"  rel=\"facebox\">View Access point</a><br/><a href=\"javascript:editSchedule();\">Edit</a><br/><a href=\"javascript:deleteSchedule();\">Delete</a></div>")
    # image uploader div
    # html.write("<div class=\"loading\"></div>")
    # html.write("<div id=\"viewApDiv\" style=\"min-
    # width:500px;height:400px;z-index:2000;position:absolute;top:100px;
    # left:10%;display:none;overflow-x:hidden;overflow-y:auto;\" >")
    html.write("<div id=\"viewApDiv\">")
    html.write("</div>")
    html.new_footer()


def add_ap_scheduler(h):
    """

    @param h:
    """
    global html
    html = h
    event = "Down"
    startDateTemp = html.var("startDate").split("/")
    startDate = startDateTemp[2] + "-" + startDateTemp[1] + "-" + \
                startDateTemp[0]
    endDateTemp = html.var("endDate").split("/")
    endDate = endDateTemp[2] + "-" + endDateTemp[1] + "-" + endDateTemp[0]
    startTime = html.var("startTime")
    endTime = html.var("endTime")
    repeat = "0"
    repeatType = html.var("repeatType")
    dates = html.var("dates")
    daysun = "0"
    daymon = "0"
    daytue = "0"
    daywed = "0"
    daythu = "0"
    dayfri = "0"
    daysat = "0"
    monthjan = "0"
    monthfeb = "0"
    monthmar = "0"
    monthapr = "0"
    monthmay = "0"
    monthjun = "0"
    monthjul = "0"
    monthaug = "0"
    monthsep = "0"
    monthoct = "0"
    monthnov = "0"
    monthdec = "0"
    accessPoint = html.var("hdAccessPoint").split(",")
    if html.var("radio") is not None:
        event = html.var("radio")
    if html.var("repeat") is not None:
        repeat = "1"
    if html.var("daysun") is not None:
        daysun = "1"
    if html.var("daymon") is not None:
        daymon = "1"
    if html.var("daytue") is not None:
        daytue = "1"
    if html.var("daywed") is not None:
        daywed = "1"
    if html.var("daythu") is not None:
        daythu = "1"
    if html.var("dayfri") is not None:
        dayfri = "1"
    if html.var("daysat") is not None:
        daysat = "1"
    if html.var("monthjan") is not None:
        monthjan = "1"
    if html.var("monthfeb") is not None:
        monthfeb = "1"
    if html.var("monthmar") is not None:
        monthmar = "1"
    if html.var("monthapr") is not None:
        monthapr = "1"
    if html.var("monthmay") is not None:
        monthmay = "1"
    if html.var("monthjun") is not None:
        monthjun = "1"
    if html.var("monthjul") is not None:
        monthjul = "1"
    if html.var("monthaug") is not None:
        monthaug = "1"
    if html.var("monthsep") is not None:
        monthsep = "1"
    if html.var("monthoct") is not None:
        monthoct = "1"
    if html.var("monthnov") is not None:
        monthnov = "1"
    if html.var("monthdec") is not None:
        monthdec = "1"

    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    try:
        cursor = db.cursor()
        # prepare SQL query to insert the scheduling details
        sql = "INSERT INTO schedule (event, startdate, enddate, starttime, endtime, isrepeat, repeattype, sun, mon, tue, wed, thu, fri, sat, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dece, dates) VALUES ('%s','%s','%s','%s','%s',%s,'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (
            event, startDate, endDate, startTime, endTime, repeat, repeatType, daysun, daymon, daytue, daywed, daythu,
            dayfri, daysat, monthjan, monthfeb, monthmar, monthapr, monthmay, monthjun, monthjul, monthaug, monthsep,
            monthoct, monthnov, monthdec, dates)
        cursor.execute(sql)
        newId = cursor.lastrowid
        for apId in accessPoint:
            if apId.strip() != "":
                sql = "INSERT INTO ap_schedule(scheduleid,deviceid) VALUE(%s,%s)" % (
                    newId, apId)
                cursor.execute(sql)

        db.commit()

        # fileData = ""
        # prepare SQL query to get scheduling data
        # sql = "SELECT * FROM schedule"
        # cursor.execute(sql)
        # schedule = cursor.fetchall()

        # for srow in schedule:
        #     sql = "SELECT * FROM ap_schedule WHERE scheduleid = %s" % srow[0]
        #     cursor.execute(sql)
        #     apschedule = cursor.fetchall()
        #     for aprow in apschedule:
        #          sql = "SELECT * FROM nms_devices WHERE id = %s" % aprow[3]
        #          cursor.execute(sql)
        #          device = cursor.fetchall()

        create_crontab_file()
        html.write(str(newId))
    except():
        # Rollback in case there is any error
        db.rollback()
        html.write("-1")
    db.close()


# function to create multiple selection list for access point
def access_point_multiple_select_list(accessPoints, selectListId):
    """

    @param accessPoints:
    @param selectListId:
    @return:
    """
    selectList = ""
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare SQL query to get total access points in this system
    sql = "SELECT id,ipaddress FROM nms_devices \
            WHERE devicetype = 'AP' \
            ORDER BY id DESC"
    cursor.execute(sql)
    result = cursor.fetchall()

    liList = ""
    for row in result:
        liList += "<li>" + row[1] + "<img src=\"images/add16.png\" class=\"plus plus" + selectListId + \
                  "\" alt=\"+\" title=\"Add\" id=\"" + str(
            row[0]) + "\" name=\"" + row[1] + "\"/></li>"

    selectList += "<div class=\"multiSelectList\" id=\"multiSelectList" + \
                  selectListId + "\" style=\"position:;\">"
    selectList += "<input type=\"hidden\" id=\"hd" + selectListId + \
                  "\" name=\"hd" + selectListId + "\" value=\"\" />"
    selectList += "<input type=\"hidden\" id=\"hdTemp" + selectListId + "\" name=\"hdTemp" + \
                  selectListId + "\" value=\"" + accessPoints + "\" />"
    selectList += "<div class=\"selected\">"
    selectList += "<div class=\"shead\"><span id=\"count\">0</span><span> Access Point(s)</span><a href=\"#\" id=\"rm" + \
                  selectListId + \
                  "\">Remove all</a>"
    selectList += "</div>"
    selectList += "<ul>"  # <li>asdf<img src=\"images/minus16.png\" class=\"minus\" alt=\"-\" title=\"Remove\" /></li>
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "<div class=\"nonSelected\">"
    selectList += "<div class=\"shead\"><a href=\"#\" id=\"add" + \
                  selectListId + "\">Add all</a>"
    selectList += "</div>"
    selectList += "<ul>" + liList
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "</div>"
    return selectList


def load_non_repeative_events(h):
    """

    @param h:
    """
    global html
    html = h
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    jsonData = "{events:["
    i = 0
    try:
        # prepare SQL query to get scheduling data
        sql = "SELECT * FROM schedule\
                 WHERE isrepeat = 0"
        cursor.execute(sql)
        schedule = cursor.fetchall()
        for srow in schedule:
            sDate = str(srow[2]).split("-")
            eDate = str(srow[3]).split("-")
            sTime = str(srow[4]).split(":")
            eTime = str(srow[5]).split(":")
            if i > 0:
                jsonData += ","
            jsonData += "{"
            jsonData += "id:" + str(srow[0]) + ","
            jsonData += "title:\"" + srow[1] + "\","
            jsonData += "start: new Date(" + sDate[0] + "," + str(
                int(sDate[1]) - 1) + "," + sDate[2] + "," + sTime[0] + "," + sTime[1] + "),"
            jsonData += "end: new Date(" + eDate[0] + "," + str(
                int(eDate[1]) - 1) + "," + eDate[2] + "," + eTime[0] + "," + eTime[1] + "),"
            jsonData += "allDay: false"
            jsonData += "}"

            i += 1
        jsonData += "]}"
        html.write(jsonData)
    except:
        html.write("{events:[]}")
    db.close()


def load_repeative_events(h):
    """

    @param h:
    """
    global html
    html = h
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    daily = "daily:["
    weekly = "weekly:["
    monthly = "monthly:["
    dailyI = 0
    weeklyI = 0
    monthlyI = 0
    try:
        # prepare SQL query to get scheduling data
        sql = "SELECT * FROM schedule\
                 WHERE isrepeat = 1"
        cursor.execute(sql)
        schedule = cursor.fetchall()
        for srow in schedule:
            if srow[7] == "Daily":
                if dailyI > 0:
                    daily += ","
                daily += "{"
                daily += "id:" + str(srow[0]) + ","
                daily += "title:\"" + srow[1] + "\","
                daily += "start:\"" + str(srow[4]) + "\","
                daily += "end: \"" + str(srow[5]) + "\","
                daily += "allDay: false"
                daily += "}"
                dailyI += 1

            elif srow[7] == "Weekly":
                if weeklyI > 0:
                    weekly += ","
                weekly += "{"
                weekly += "id:" + str(srow[0]) + ","
                weekly += "title:\"" + srow[1] + "\","
                weekly += "start:\"" + str(srow[4]) + "\","
                weekly += "end: \"" + str(srow[5]) + "\","
                weekly += "sun: " + str(srow[8]) + ","
                weekly += "mon: " + str(srow[9]) + ","
                weekly += "tue: " + str(srow[10]) + ","
                weekly += "wed: " + str(srow[11]) + ","
                weekly += "thu: " + str(srow[12]) + ","
                weekly += "fri: " + str(srow[13]) + ","
                weekly += "sat: " + str(srow[14]) + ","
                weekly += "allDay: false"
                weekly += "}"
                weeklyI += 1

            elif srow[7] == "Monthly":
                if monthlyI > 0:
                    monthly += ","
                monthly += "{"
                monthly += "id:" + str(srow[0]) + ","
                monthly += "title:\"" + srow[1] + "\","
                monthly += "start:\"" + str(srow[4]) + "\","
                monthly += "end: \"" + str(srow[5]) + "\","
                monthly += "date: " + str(srow[27]) + ","
                monthly += "jan: " + str(srow[15]) + ","
                monthly += "feb: " + str(srow[16]) + ","
                monthly += "mar: " + str(srow[17]) + ","
                monthly += "apr: " + str(srow[18]) + ","
                monthly += "may: " + str(srow[19]) + ","
                monthly += "jun: " + str(srow[20]) + ","
                monthly += "jul: " + str(srow[21]) + ","
                monthly += "aug: " + str(srow[22]) + ","
                monthly += "sep: " + str(srow[23]) + ","
                monthly += "oct: " + str(srow[24]) + ","
                monthly += "nov: " + str(srow[25]) + ","
                monthly += "dec: " + str(srow[26]) + ","
                monthly += "allDay: false"
                monthly += "}"
                monthlyI += 1
        jsonData = "{" + daily + "], " + weekly + "]," + monthly + "]}"
        html.write(jsonData)
    except:
        html.write("{daily:[],weekly:[],monthly:[]}")
        db.close()


def event_resize(h):
    """

    @param h:
    """
    global html
    html = h
    scheduleId = html.var("id")
    day = html.var("day")
    minute = html.var("minute")
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare SQL query to get scheduling data
    sql = "SELECT enddate,endtime FROM schedule\
            WHERE scheduleid = %s" % scheduleId
    cursor.execute(sql)
    endDate = ""
    endTime = ""
    i = 0
    result = cursor.fetchall()
    for row in result:
        endDate = row[0]
        endTime = row[1]
        i += 1
    if i != 0:
        eDate = str(endDate).split("-")
        eTime = str(endTime).split(":")
        eDateObj = datetime.datetime(int(eDate[0]), int(eDate[1]), int(
            eDate[2]), int(eTime[0]), int(eTime[1]), int(eTime[2]))
        eDateObj = eDateObj + datetime.timedelta(minutes=int(minute))
        eDateObj = eDateObj + datetime.timedelta(days=int(day))
        sql = "UPDATE schedule SET \
                 enddate = '%s', \
                 endtime = '%s' \
                 WHERE scheduleid = %s" % ((str(eDateObj.year) + "-" + str(eDateObj.month) + "-" + str(eDateObj.day)),
                                           (str(eDateObj.hour) + ":" + str(eDateObj.minute) + ":00"), scheduleId)
        cursor.execute(sql)
        db.commit()
        create_crontab_file()
        html.write("0")
    else:
        html.write("1")


def event_drop(h):
    """

    @param h:
    """
    global html
    html = h
    scheduleId = html.var("id")
    day = html.var("day")
    minute = html.var("minute")
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare SQL query to get scheduling data
    sql = "SELECT startdate,starttime,enddate,endtime,isrepeat,repeattype,sun,mon,tue,wed,thu,fri,sat,dates FROM schedule\
            WHERE scheduleid = %s" % scheduleId
    cursor.execute(sql)
    startDate = ""
    startTime = ""
    endDate = ""
    endTime = ""
    isRepeat = 0
    repeatType = "Daily"
    sun = 0
    mon = 0
    tue = 0
    wed = 0
    thu = 0
    fri = 0
    sat = 0
    tempSun = 0
    tempMon = 0
    tempTue = 0
    tempWed = 0
    tempThu = 0
    tempFri = 0
    tempSat = 0
    dates = 0
    i = 0
    result = cursor.fetchall()
    for row in result:
        startDate = row[0]
        startTime = row[1]
        endDate = row[2]
        endTime = row[3]
        isRepeat = row[4]
        repeatType = row[5]
        sun = int(row[6])
        mon = int(row[7])
        tue = int(row[8])
        wed = int(row[9])
        thu = int(row[10])
        fri = int(row[11])
        sat = int(row[12])
        dates = int(row[13])
        i += 1
    if i != 0:
        sDate = str(startDate).split("-")
        sTime = str(startTime).split(":")
        eDate = str(endDate).split("-")
        eTime = str(endTime).split(":")
        sDateObj = datetime.datetime(int(sDate[0]), int(sDate[1]), int(
            sDate[2]), int(sTime[0]), int(sTime[1]), int(sTime[2]))
        sDateObj = sDateObj + datetime.timedelta(minutes=int(minute))
        sDateObj = sDateObj + datetime.timedelta(days=int(day))
        eDateObj = datetime.datetime(int(eDate[0]), int(eDate[1]), int(
            eDate[2]), int(eTime[0]), int(eTime[1]), int(eTime[2]))
        eDateObj = eDateObj + datetime.timedelta(minutes=int(minute))
        eDateObj = eDateObj + datetime.timedelta(days=int(day))
        if int(day) != 0:
            if int(isRepeat) == 1:
                if repeatType == "Weekly":
                    for i in range(0, int(day)):
                        tempSun = sat
                        tempMon = sun
                        tempTue = mon
                        tempWed = tue
                        tempThu = wed
                        tempFri = thu
                        tempSat = fri
                        sun = tempSun
                        mon = tempMon
                        tue = tempTue
                        wed = tempWed
                        thu = tempThu
                        fri = tempFri
                        sat = tempSat
                    for i in range(int(day), 0):
                        tempSun = mon
                        tempMon = tue
                        tempTue = wed
                        tempWed = thu
                        tempThu = fri
                        tempFri = sat
                        tempSat = sun
                        sun = tempSun
                        mon = tempMon
                        tue = tempTue
                        wed = tempWed
                        thu = tempThu
                        fri = tempFri
                        sat = tempSat
                if repeatType == "Monthly":
                    dates = int(dates) + int(day)

        sql = "UPDATE schedule SET \
                 startdate = '%s', \
                 starttime = '%s', \
                 enddate = '%s', \
                 endtime = '%s', \
                 sun = %s, \
                 mon = %s, \
                 tue = %s, \
                 wed = %s, \
                 thu = %s, \
                 fri = %s, \
                 sat = %s, \
                 dates = %s \
                 WHERE scheduleid = %s" % ((str(sDateObj.year) + "-" + str(sDateObj.month) + "-" + str(sDateObj.day)),
                                           (str(sDateObj.hour) + ":" + str(sDateObj.minute) + ":00"),
                                           (str(eDateObj.year) + "-" + str(eDateObj.month) + "-" + str(eDateObj.day)),
                                           (str(eDateObj.hour) + ":" + str(eDateObj.minute) + ":00"), sun, mon, tue,
                                           wed, thu, fri, sat, dates, scheduleId)
        cursor.execute(sql)
        db.commit()
        create_crontab_file()
        html.write("0")
    else:
        html.write("1")


def delete_ap_scheduler(h):
    """

    @param h:
    """
    global html
    html = h
    scheduleId = html.var("scheduleId")
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare SQL query to get scheduling data
    sql = "delete FROM schedule\
            WHERE scheduleid = %s" % scheduleId
    cursor.execute(sql)
    db.commit()
    db.close()
    create_crontab_file()
    html.write("0")


def view_access_point_list(h):
    """

    @param h:
    """
    global html
    html = h
    scheduleId = html.var("scheduleId")
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare SQL query to get scheduling data
    sql = "select nms_devices.devicetype,nms_devices.ipaddress,nms_devices.hostname FROM nms_devices \
            INNER JOIN ap_schedule on ap_schedule.deviceid = nms_devices.id \
            WHERE ap_schedule.scheduleid = %s" % scheduleId
    cursor.execute(sql)
    result = cursor.fetchall()
    tableString = """
<div><table width=\"100%\">
	<tbody>
<tr><th colspan=\"4\">Access Point</th></tr>
		<tr>
			<th>S.No.</th>
			<th>IP Address</th>
			<th>Device type</th>
			<th>Host Name</th>
		</tr>
"""
    i = 0
    for row in result:
        i += 1
        tableString += "<tr><td>" + str(i) + "</td><td>" + row[1] + "</td><td>" + \
                       row[0] + "</td><td>" + \
                       row[2] + "</td></tr>"
    tableString += "</tbody></table>"
    html.write(tableString)


def get_ap_schedule_details(h):
    """

    @param h:
    """
    global html
    html = h
    scheduleId = html.var("scheduleId")
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare SQL query to get scheduling data
    sql = "select * FROM schedule \
            WHERE scheduleid = %s" % scheduleId
    cursor.execute(sql)
    result = cursor.fetchall()
    jsonData = "{"
    for row in result:
        jsonData += "scheduleid:" + str(row[0]) + ","
        jsonData += "event:\"" + str(row[1]) + "\","
        jsonData += "startdate:\"" + str(row[2]) + "\","
        jsonData += "enddate:\"" + str(row[3]) + "\","
        jsonData += "starttime:\"" + str(row[4]) + "\","
        jsonData += "endtime:\"" + str(row[5]) + "\","
        jsonData += "isrepeat:" + str(row[6]) + ","
        jsonData += "repeattype:\"" + str(row[7]) + "\","
        jsonData += "sun:" + str(row[8]) + ","
        jsonData += "mon:" + str(row[9]) + ","
        jsonData += "tue:" + str(row[10]) + ","
        jsonData += "wed:" + str(row[11]) + ","
        jsonData += "thu:" + str(row[12]) + ","
        jsonData += "fri:" + str(row[13]) + ","
        jsonData += "sat:" + str(row[14]) + ","
        jsonData += "jan:" + str(row[15]) + ","
        jsonData += "feb:" + str(row[16]) + ","
        jsonData += "mar:" + str(row[17]) + ","
        jsonData += "apr:" + str(row[18]) + ","
        jsonData += "may:" + str(row[19]) + ","
        jsonData += "jun:" + str(row[20]) + ","
        jsonData += "jul:" + str(row[21]) + ","
        jsonData += "aug:" + str(row[22]) + ","
        jsonData += "sep:" + str(row[23]) + ","
        jsonData += "oct:" + str(row[24]) + ","
        jsonData += "nov:" + str(row[25]) + ","
        jsonData += "dece:" + str(row[26]) + ","
        jsonData += "dates:\"" + str(row[27]) + "\""
        break
    sql = "SELECT * FROM ap_schedule \
            WHERE scheduleid = %s" % scheduleId
    cursor.execute(sql)
    result = cursor.fetchall()
    apList = ""
    i = 0
    for row in result:
        if i > 0:
            apList += ","
        apList += str(row[2])
        i += 1
    if i > 0:
        jsonData += ",aplist:\"" + apList + "\""
    jsonData += "}"
    html.write(jsonData)


def update_ap_scheduler(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    scheduleId = html.var("scheduleId")
    event = "Down"
    startDateTemp = html.var("startDate").split("/")
    startDate = startDateTemp[2] + "-" + startDateTemp[1] + "-" + \
                startDateTemp[0]
    endDateTemp = html.var("endDate").split("/")
    endDate = endDateTemp[2] + "-" + endDateTemp[1] + "-" + endDateTemp[0]
    startTime = html.var("startTime")
    endTime = html.var("endTime")
    repeat = "0"
    repeatType = html.var("repeatType")
    dates = html.var("dates")
    daysun = "0"
    daymon = "0"
    daytue = "0"
    daywed = "0"
    daythu = "0"
    dayfri = "0"
    daysat = "0"
    monthjan = "0"
    monthfeb = "0"
    monthmar = "0"
    monthapr = "0"
    monthmay = "0"
    monthjun = "0"
    monthjul = "0"
    monthaug = "0"
    monthsep = "0"
    monthoct = "0"
    monthnov = "0"
    monthdec = "0"
    accessPoint = html.var("hdAccessPoint").split(",")
    if html.var("radio") is not None:
        event = html.var("radio")
    if html.var("repeat") is not None:
        repeat = "1"
    if html.var("daysun") is not None:
        daysun = "1"
    if html.var("daymon") is not None:
        daymon = "1"
    if html.var("daytue") is not None:
        daytue = "1"
    if html.var("daywed") is not None:
        daywed = "1"
    if html.var("daythu") is not None:
        daythu = "1"
    if html.var("dayfri") is not None:
        dayfri = "1"
    if html.var("daysat") is not None:
        daysat = "1"
    if html.var("monthjan") is not None:
        monthjan = "1"
    if html.var("monthfeb") is not None:
        monthfeb = "1"
    if html.var("monthmar") is not None:
        monthmar = "1"
    if html.var("monthapr") is not None:
        monthapr = "1"
    if html.var("monthmay") is not None:
        monthmay = "1"
    if html.var("monthjun") is not None:
        monthjun = "1"
    if html.var("monthjul") is not None:
        monthjul = "1"
    if html.var("monthaug") is not None:
        monthaug = "1"
    if html.var("monthsep") is not None:
        monthsep = "1"
    if html.var("monthoct") is not None:
        monthoct = "1"
    if html.var("monthnov") is not None:
        monthnov = "1"
    if html.var("monthdec") is not None:
        monthdec = "1"

    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    try:
        cursor = db.cursor()
        # prepare SQL query to update the scheduling details
        sql = "UPDATE schedule SET event = '%s', startdate = '%s', enddate = '%s', starttime = '%s', endtime = '%s', isrepeat = %s, repeattype = '%s', sun = %s, mon = %s, tue = %s, wed = %s, thu = %s, fri = %s, sat = %s, jan = %s, feb = %s, mar = %s, apr = %s, may = %s, jun = %s, jul = %s, aug = %s, sep = %s, oct = %s, nov = %s, dece = %s, dates = '%s' WHERE scheduleid = %s" % (
            event, startDate, endDate, startTime, endTime, repeat, repeatType, daysun, daymon, daytue, daywed, daythu,
            dayfri, daysat, monthjan, monthfeb, monthmar, monthapr, monthmay, monthjun, monthjul, monthaug, monthsep,
            monthoct, monthnov, monthdec, dates, scheduleId)
        cursor.execute(sql)

        sql = "DELETE FROM ap_schedule WHERE scheduleid = %s" % (scheduleId)
        cursor.execute(sql)

        for apId in accessPoint:
            if apId.strip() != "":
                sql = "INSERT INTO ap_schedule(scheduleid,deviceid) VALUE(%s,%s)" % (
                    scheduleId, apId)
                cursor.execute(sql)
        db.commit()
        create_crontab_file()
        html.write(str(scheduleId))
    except():
        # Rollback in case there is any error
        db.rollback()
        html.write("-1")
    db.close()


def create_crontab_file():

    """
    # Open database connection
    write to crontab of UNMP user
    """
    db = MySQLdb.connect("localhost", "root", "root", "nms")

    commands = "python /omd/deamon/scheduling.py "
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
            sDateObj = datetime.datetime(int(sDate[0]), int(sDate[1]), int(
                sDate[2]), int(sTime[0]), int(sTime[1]), int(sTime[2]))
            eDateObj = datetime.datetime(int(eDate[0]), int(eDate[1]), int(
                eDate[2]), int(eTime[0]), int(eTime[1]), int(eTime[2]))

            if row[6] == 0:            # this is for non repeated scheduling
                if sDateObj > now:
                    commandString = sTime[1] + " " + \
                                    sTime[0] + " " + sDate[2] + " " + sDate[1] + " * "
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
                        crontabString += commandString + commands + \
                                         username + " " + \
                                         password + \
                                         " " + port + " " + ip + " " + event1
                        apI1 += 1
                    crontabString += " 1 -1\n"

                if eDateObj > now:
                    commandString = eTime[1] + " " + \
                                    eTime[0] + " " + eDate[2] + " " + eDate[1] + " * "
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
                        crontabString += commandString + commands + \
                                         username + " " + \
                                         password + " " + port + " " + ip + " " + event2
                        apI2 += 1
                    crontabString += " 1 -1\n"

            else:                # this is for repeated scheduling
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
                        crontabString += commandString1 + commands + username + " " + \
                                         password + " " + \
                                         port + " " + ip + " " + event1 + " 0 -1\n"
                        crontabString += commandString2 + commands + username + " " + \
                                         password + " " + \
                                         port + " " + ip + " " + event2 + " 0 -1\n"

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
                        if row[8] == 1:  # sunday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "0"
                            commandString2 += "0"
                            dayI += 1
                        if row[9] == 1:  # monday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "1"
                            commandString2 += "1"
                        if row[10] == 1:  # tuesday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "2"
                            commandString2 += "2"
                            dayI += 1
                        if row[11] == 1:  # wednusday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "3"
                            commandString2 += "3"
                            dayI += 1
                        if row[12] == 1:  # thrusday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "4"
                            commandString2 += "4"
                            dayI += 1
                        if row[13] == 1:  # friday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "5"
                            commandString2 += "5"
                            dayI += 1
                        if row[14] == 1:  # saturday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "6"
                            commandString2 += "6"
                            dayI += 1

                        crontabString += commandString1 + " " + commands + username + " " + \
                                         password + " " + \
                                         port + " " + ip + " " + event1 + " 0 -1\n"
                        crontabString += commandString2 + " " + commands + username + " " + \
                                         password + " " + \
                                         port + " " + ip + " " + event2 + " 0 -1\n"

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
                        commandString1 = sTime[1] + \
                                         " " + sTime[0] + " " + row[27] + " "
                        commandString2 = sTime[1] + \
                                         " " + sTime[0] + " " + row[27] + " "
                        if row[15] == 1:  # jan
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "1"
                            commandString2 += "1"
                            monthI += 1
                        if row[16] == 1:  # feb
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "2"
                            commandString2 += "2"
                            monthI += 1
                        if row[17] == 1:  # mar
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "3"
                            commandString2 += "3"
                            monthI += 1
                        if row[18] == 1:  # apr
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "4"
                            commandString2 += "4"
                            monthI += 1
                        if row[19] == 1:  # may
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "5"
                            commandString2 += "5"
                            monthI += 1
                        if row[20] == 1:  # jun
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "6"
                            commandString2 += "6"
                            monthI += 1
                        if row[21] == 1:  # jul
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "7"
                            commandString2 += "7"
                            monthI += 1
                        if row[22] == 1:  # aug
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "8"
                            commandString2 += "8"
                            monthI += 1
                        if row[23] == 1:  # sep
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "9"
                            commandString2 += "9"
                            monthI += 1
                        if row[24] == 1:  # oct
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "10"
                            commandString2 += "10"
                            monthI += 1
                        if row[25] == 1:  # nov
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "11"
                            commandString2 += "11"
                            monthI += 1
                        if row[26] == 1:  # dec
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "12"
                            commandString2 += "12"
                            monthI += 1

                        crontabString += commandString1 + " * " + commands + username + " " + \
                                         password + " " + \
                                         port + " " + ip + " " + event1 + " 0 -1\n"
                        crontabString += commandString2 + " * " + commands + username + " " + \
                                         password + " " + \
                                         port + " " + ip + " " + event2 + " 0 -1\n"

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
            commandString = sTime[1] + " " + sTime[0] + " " + \
                            sDate[2] + " " + sDate[1] + " * "

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
            crontabString += commandString + commands + username + " " + password + \
                             " " + port + " " + ip + " " + event + \
                             " 0 " + str(row[0]) + "\n"

        fobj = open("/omd/deamon/crontab", "w")
        fobj.write(crontabString)
        fobj.close()
    except:
        error = "some error occur"
    db.close()

################################## Scheduling ############################

#################################### AP Radio Status #####################


def radio_status(h):
    """

    @param h:
    """
    socket.setdefaulttimeout(1)
    global html
    html = h
    css_list = ["css/style.css", "fullcalendar/fullcalendar.css"]
    js_list = ["js/lib/main/jquery-ui-1.8.6.custom.min.js",
               "fullcalendar/fullcalendar.min.js", "js/unmp/main/radio_status.js"]
    html.new_header("Radio Status", "", "", css_list, js_list)

    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # prepare SQL query to create repeated schedule
    sql = "SELECT * FROM nms_devices WHERE devicetype = 'AP'"
    cursor.execute(sql)
    result = cursor.fetchall()

    tableString = "<table style=\"margin-bottom: 0px;\" id=\"iconmeaningtable\" class=\"addform\"><colgroup><col width=\"auto\"><col width=\"1%\"><col width=\"6%\"><col width=\"1%\"><col width=\"6%\"><col width=\"1%\"><col width=\"6%\"></colgroup><tbody><tr><th></th><th style=\"padding: 5px 0px 5px 10px;\"><img width=\"10px\" alt=\"enable\" src=\"images/status-0.png\"></th><th>enable</th><th style=\"padding: 5px 0px 5px 10px;\"><img width=\"10px\" alt=\"disable\" src=\"images/status-2.png\"></th><th>disable</th><th style=\"padding: 5px 0px 5px 10px;\"><img width=\"10px\" alt=\"unknown\" src=\"images/status-3.png\"></th><th>unknown</th></tr></tbody></table>"

    tableString += "<table class=\"addform\"><colgroup><col width=\"5%\"><col width=\"25%\"><col width=\"5%\"><col width=\"25%\"><col width=\"35%\"><col width=\"5%\"></colgroup><tbody>"
    tableString += "<tr><th>S.No.</th><th>IP Address</th><th>Status</th><th>Retry Action Time</th><th>Action Msg</th><th></th></tr>"
    response = ""
    i = 0
    for row in result:
        i += 1
        username = row[3]
        password = row[4]
        port = row[5]
        tempUrl = "/cgi-bin/ServerFuncs?Method=RadioStatus"
        url = "http://" + row[2] + tempUrl

        try:
            req = urllib2.Request(url)
            auth_string = base64.encodestring("%s:%s" % (username, password))
            req.add_header("Authorization", "Basic %s" % auth_string)
            f = urllib2.urlopen(req)
            response = f.read()
        except urllib2.HTTPError, e:
            response = str(e.code)  # send http error code
        except:
            response = "Notwork Unreachable"

        if response == "400":
            message = "Bad Request"
        elif response == "401":
            message = "User name and Password are wrong"
        elif response == "404":
            message = "File Not Found"
        elif response == "501":
            message = "Server Error"
        else:
            message = "Access Point not connected"

        currentStatus = ""
        if response.find("RadioStatus = 11") != -1:
            currentStatus = "Enable"
        if response.find("RadioStatus = 01") != -1:
            currentStatus = "Enable"
        if response.find("RadioStatus = 10") != -1:
            currentStatus = "Disable"
        if response.find("RadioStatus = 00") != -1:
            currentStatus = "Disable"

        sql = "SELECT * FROM repeat_ap_schedule WHERE deviceId = %s" % row[0]
        cursor.execute(sql)
        result2 = cursor.fetchall()
        retryTime = "-"
        retryMsg = "-"
        for row2 in result2:
            retryTime = str(row2[1]) + ", " + str(row2[2])
            retryMsg = str(row2[4]) + " (" + row2[5] + ")"

        tableString += "<tr><td>" + str(i) + "</td>"
        tableString += "<td>" + str(row[2]) + "</td>"
        if currentStatus == "Enable":
            tableString += "<td><img width=\"10px\" alt=\"enable\" title=\"Enable\" src=\"images/status-0.png\"></td>"
            tableString += "<td>" + retryTime + "</td>"
            tableString += "<td>" + retryMsg + "</td>"
            tableString += "<td><a href=\"javascript:disableRadio('" + row[2] + "','" + username + "','" + \
                           password + "','" + \
                           port + \
                           "')\">Disable</a></td>"
        elif currentStatus == "Disable":
            tableString += "<td><img width=\"10px\" alt=\"disable\" title=\"Disable\" src=\"images/status-2.png\"></td>"
            tableString += "<td>" + retryTime + "</td>"
            tableString += "<td>" + retryMsg + "</td>"
            tableString += "<td><a href=\"javascript:enableRadio('" + row[2] + "','" + username + "','" + \
                           password + "','" + \
                           port + \
                           "')\">Enable</a></td>"
        else:
            tableString += "<td><img width=\"10px\" alt=\"unknown\" title=\"" + \
                           message + "\" src=\"images/status-3.png\"></td>"
            tableString += "<td>-</td>"
            tableString += "<td>" + message + "</td>"
            tableString += "<td>-</td>"
        tableString += "</tr>"

    tableString += "</tbody></table>"
    html.write(tableString)
    # image uploader div
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt='loading...'/></div>")
    html.new_footer()


def change_redio(h):
    """

    @param h:
    """
    global html
    html = h
    username = html.var("username")
    password = html.var("password")
    ipaddress = html.var("ipaddress")
    port = html.var("port")
    action = html.var("action")
    tempUrl = ""
    if action == "Enable":
        tempUrl = "/cgi-bin/ServerFuncs?Method=EnableRadio"
    else:
        tempUrl = "/cgi-bin/ServerFuncs?Method=DisableRadio"
    message = ""
    url = "http://" + ipaddress + tempUrl
    try:
        req = urllib2.Request(url)
        auth_string = base64.encodestring("%s:%s" % (username, password))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
    except urllib2.HTTPError, e:
        response = str(e.code)  # send http error code
    except urllib2.URLError, e:
        if action != "Enable":
            action = "Disable"
        response = "URLError"
    except:
        response = "Exception"

    if response == "Enable Radio Request Received":
        message = "Enable"
    elif response == "Disable  Request Received":
        message = "Disable"
    elif response == "URLError":
        message = action + "1"
    elif response == "400":
        message = "Bad Request"
    elif response == "401":
        message = "User name and Password are wrong"
    elif response == "404":
        message = "File Not Found"
    elif response == "501":
        message = "Server Error"
    else:
        message = "Access Point not connected"
    html.write(message)

#################################### AP Radio Status #####################
