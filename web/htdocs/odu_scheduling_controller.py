#!/usr/bin/python2.6

import config, htmllib, pprint, sidebar, views, time, defaults, os, cgi, xml.dom.minidom, subprocess, commands, MySQLdb, urllib2, base64, socket, sys
from lib import *
from nms_config import *
from odu_scheduling import OduScheduling
from odu_scheduling_bll import OduSchedulingBll
import os
from mod_python import apache,util
import StringIO
import datetime
from common_bll import Essential
################################## Scheduling #####################################
def odu_scheduling(h):
    global html
    html = h
    try:
        css_list = ["css/style.css","facebox/facebox.css","calendrical/calendrical.css","fullcalendar/fullcalendar.css","css/jquery.multiselect.css","css/jquery.multiselect.filter.css","css/jquery-ui-1.8.4.custom.css","css/demo_table_jui.css"]
        js_list = ["js/jquery-ui-1.8.6.custom.min.js","fullcalendar/fullcalendar.min.js","facebox/facebox.js","js/calendrical.js","js/jquery.dataTables.min.js","js/odu_scheduling.js","js/pages/jquery.multiselect.min.js","js/pages/jquery.multiselect.filter.js"]
        header_btn = ""
        snapin_list = ["reports","views","Alarm","Inventory","Settings","NetworkMaps","user_management","schedule","Listing"]
        html.new_header("Device Scheduling","odu_scheduling.py",header_btn,css_list,js_list,snapin_list)
        user_id=html.req.session["user_id"]
        es = Essential()
        hostgroup_id_list = es.get_hostgroup_ids(user_id)
        odu_bll_obj=OduSchedulingBll()
        device_list=odu_bll_obj.get_hostgroup_device(user_id,hostgroup_id_list)
        if str(device_list["success"])=="0":
            html_str=OduScheduling.create_scheduling_form(device_list["result"])
        else:
            html_str=OduScheduling.create_scheduling_form("")
        odu_list=""
        selectListId="odu"
        odu_bll_obj=OduSchedulingBll()
        device_type=""
        result=odu_bll_obj.odu_multiple_select_list(odu_list, selectListId,device_type)
        html_str+=OduScheduling.odu_multiple_select_list(odu_list, selectListId,result)
        html_str+=OduScheduling.create_scheduling_form_remain()
        html.write(html_str)
        html.new_footer()
    except Exception,e:
        html.write(str(e))

def odu_scheduling_get_device_info(h):
    global html
    html=h
    odu_bll_obj=OduSchedulingBll()
    odu_list=""
    selectListId="odu"
    odu_bll_obj=OduSchedulingBll()
    device_type=html.var("device_type")
    result=odu_bll_obj.odu_multiple_select_list(odu_list, selectListId,device_type)
    html.write(str(OduScheduling.odu_multiple_select_list(odu_list, selectListId,result)))   

def update_firmware_view(h):
    global html
    html = h
    #host_id=h.var('host_id')
    device_type=h.var('device_type')
    #html.req.session["host_id_session"]=host_id
    html.req.session["device_type"] = device_type
    html.req.session.save()
    upload_form = OduScheduling.upload_form(device_type)
    html.write(str(upload_form))


def view_Scheduling_Details(h):
    global html
    html=h
    odu_bll_obj=OduSchedulingBll()
    result=odu_bll_obj.view_Scheduling_Details()
#    html.write(str(OduScheduling.view_Scheduling_Details(result)))
    html.write(str(result))


def add_odu_scheduler(h):
    global html
    html = h
    event = "Down"
    startDateTemp = html.var("startDate").split("/")
    startDate = startDateTemp[2] + "-" + startDateTemp[1] + "-" + startDateTemp[0]
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
    odu_list = html.var("hdodu").split(",")
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
    odu_bll_obj=OduSchedulingBll()
    if event=="Firmware":
        #firmware_file_name=html.var("selected_firmware")#html.req.session["firmware_file"]
        firmware_file_name=html.req.session["firmware_file"]
    else:
        firmware_file_name=""
    newId=odu_bll_obj.create_scheduler(odu_list,event, startDate, endDate, startTime, endTime, repeat, repeatType, daysun, daymon, daytue, daywed, daythu, dayfri, daysat, monthjan, monthfeb, monthmar, monthapr, monthmay, monthjun, monthjul, monthaug, monthsep, monthoct, monthnov, monthdec, dates,firmware_file_name)
    user_name=html.req.session["username"]
    create_crontab_file(user_name)     
    html.write(str(newId))


def load_non_repeative_events_odu(h):
    global html
    html = h
    odu_bll_obj=OduSchedulingBll()
    schedule=odu_bll_obj.load_non_repeative_events()
    html.write(OduScheduling.load_non_repeative_events(schedule))

def load_repeative_events_odu(h):
    global html
    html = h
    odu_bll_obj=OduSchedulingBll()
    schedule=odu_bll_obj.load_repeative_events()
    html.write(OduScheduling.load_repeative_events(schedule))


def event_resize_odu(h):
    global html
    html = h
    scheduleId = html.var("id")
    day = html.var("day")
    minute = html.var("minute")
    endDate = ""
    endTime = ""
    i = 0
    odu_bll_obj=OduSchedulingBll()
    result = odu_bll_obj.event_resize(scheduleId)
    if(len(result)!=0):
        for row in result:
            endDate = row[0]
            endTime = row[1]
            i += 1
    if i != 0:
        eDate = str(endDate).split("-")
        eTime = str(endTime).split(":")
        eDateObj = datetime.datetime(int(eDate[0]),int(eDate[1]),int(eDate[2]),int(eTime[0]),int(eTime[1]),int(eTime[2]))
        eDateObj = eDateObj + datetime.timedelta(minutes = int(minute))
        eDateObj = eDateObj + datetime.timedelta(days = int(day))
        odu_bll_obj.event_resize_update(scheduleId,eDateObj)
        user_name=html.req.session["username"]
        create_crontab_file(user_name)
        html.write("0")
    else:
        html.write("1")


def event_drop_odu(h):
    global html
    html = h
    scheduleId = html.var("id")
    day = html.var("day")
    minute = html.var("minute")
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
    odu_bll_obj=OduSchedulingBll()
    result = odu_bll_obj.event_drop(scheduleId)
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
        sDateObj = datetime.datetime(int(sDate[0]),int(sDate[1]),int(sDate[2]),int(sTime[0]),int(sTime[1]),int(sTime[2]))
        sDateObj = sDateObj + datetime.timedelta(minutes = int(minute))
        sDateObj = sDateObj + datetime.timedelta(days = int(day))
        eDateObj = datetime.datetime(int(eDate[0]),int(eDate[1]),int(eDate[2]),int(eTime[0]),int(eTime[1]),int(eTime[2]))
        eDateObj = eDateObj + datetime.timedelta(minutes = int(minute))
        eDateObj = eDateObj + datetime.timedelta(days = int(day))
        sTempnow=datetime.datetime.now()
        sTempObj=sTempnow.replace(day=sTempnow.day-1)
        if(sDateObj<sTempObj and isRepeat !=1):
            html.write("2")
        else :
            if int(day) != 0:
                if int(isRepeat) == 1:
                    if repeatType == "Weekly":
                        for i in range(0,int(day)):
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
                        for i in range(int(day),0):
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
            odu_bll_obj=OduSchedulingBll()
            result = odu_bll_obj.event_drop_update(scheduleId,(str(sDateObj.year) + "-" + str(sDateObj.month) + "-" + str(sDateObj.day)),(str(sDateObj.hour) + ":" + str(sDateObj.minute) + ":00"),(str(eDateObj.year) + "-" + str(eDateObj.month) + "-" + str(eDateObj.day)),(str(eDateObj.hour) + ":" + str(eDateObj.minute) + ":00"),sun,mon,tue,wed,thu,fri,sat,dates)
            user_name=html.req.session["username"]
            create_crontab_file(user_name)
            html.write("0")
    else:
        html.write("1")



def delete_odu_scheduler(h):
    global html
    html = h
    scheduleId = html.var("scheduleId")
    odu_bll_obj=OduSchedulingBll()
    result = odu_bll_obj.delete_odu_scheduler(scheduleId)
    user_name=html.req.session["username"]
    create_crontab_file(user_name)
    html.write("0")


def view_access_point_list_odu(h):
    global html
    html = h
    scheduleId = html.var("scheduleId")
    odu_bll_obj=OduSchedulingBll()
    result = odu_bll_obj.view_odu_list(scheduleId)
    html.write(OduScheduling.view_odu_list(result))


def get_odu_schedule_details(h):
    global html
    html = h
    scheduleId = html.var("scheduleId")
    odu_bll_obj=OduSchedulingBll()
    result = odu_bll_obj.get_odu_schedule_details(scheduleId)
    jsonData = {}
    for row in result:
        jsonData["scheduleid"]= str(row[0]) 
        jsonData["event"] =  str(row[1])  
        jsonData["startdate"] =  str(row[2])  
        jsonData["enddate"] =  str(row[3])  
        jsonData["starttime"] =  str(row[4])  
        jsonData["endtime"] =  str(row[5])  
        jsonData["isrepeat"] =  str(row[6])  
        jsonData["repeattype"] =  str(row[7])  
        jsonData["sun"] =  str(row[8])  
        jsonData["mon"] =  str(row[9])  
        jsonData["tue"] =  str(row[10])  
        jsonData["wed"] =  str(row[11])  
        jsonData["thu"] =  str(row[12])  
        jsonData["fri"] =  str(row[13])  
        jsonData["sat"] =  str(row[14])  
        jsonData["jan"] =  str(row[15])  
        jsonData["feb"] =  str(row[16])  
        jsonData["mar"] =  str(row[17])  
        jsonData["apr"] =  str(row[18])  
        jsonData["may"] =  str(row[19])  
        jsonData["jun"] =  str(row[20])  
        jsonData["jul"] =  str(row[21])  
        jsonData["aug"] =  str(row[22])  
        jsonData["sep"] =  str(row[23])  
        jsonData["oct"] =  str(row[24])  
        jsonData["nov"] =  str(row[25])  
        jsonData["dece"] =  str(row[26])  
        jsonData["dates"] =  str(row[27])
        if str(row[1])=="Firmware":
            jsonData["firmware_file"] =  str(result[1][0])
        jsonData["device_type_id"] =  str(result[1][1])
        jsonData["device_type_name"] =  str(result[1][2])
        break
    result = odu_bll_obj.get_odu_schedule_details_odu(scheduleId)
    apList = ""
    i = 0
    for row in result:
        if i > 0:
            apList += ","
        apList += str(row[2])
        i += 1
    if i > 0:
        jsonData["aplist"]= apList
    res=odu_bll_obj.get_odu_schedule_details_make_list(scheduleId)
    html_list=OduScheduling.odu_multiple_select_list("", "odu",res)
    jsonData["html_list"]=html_list
    html.write(str(jsonData))




def update_odu_scheduler(h):
    global html
    html = h
    sitename = __file__.split("/")[3]
    scheduleId = html.var("scheduleId")
    event = "Down"
    startDateTemp = html.var("startDate").split("/")
    startDate = startDateTemp[2] + "-" + startDateTemp[1] + "-" + startDateTemp[0]
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
    accessPoint = html.var("hdodu").split(",")
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

    try:
        odu_bll_obj=OduSchedulingBll()
        result = odu_bll_obj.update_odu_scheduler(event, startDate, endDate, startTime, endTime, repeat, repeatType, daysun, daymon, daytue, daywed, daythu, dayfri, daysat, monthjan, monthfeb, monthmar, monthapr, monthmay, monthjun, monthjul, monthaug, monthsep, monthoct, monthnov, monthdec, dates, scheduleId)
        result2 = odu_bll_obj.update_odu_scheduler_delete(scheduleId)
        for apId in accessPoint:
            if apId.strip() != "":
                if event=="Firmware":
#                       firmware_file_name=html.var("selected_firmware")#html.req.session["firmware_file"]
                    firmware_file_name=html.req.session["firmware_file"]
                else:
                    firmware_file_name=""
                result3 = odu_bll_obj.update_odu_scheduler_insert(scheduleId,apId,event,firmware_file_name)
        user_name=html.req.session["username"]
        create_crontab_file(user_name)
        html.write(str(scheduleId))
    except():
        # Rollback in case there is any error
        html.write("-1")

def scheduling_firmware_file_upload(h):
    try:
        global html
        html = h
        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        user_id=html.req.session["user_id"]
        file_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/%s%s.img" %(nms_instance,str(datetime.datetime.now()),user_id)
        form = util.FieldStorage(h.req,keep_blank_values=1)
        upfile = form.getlist('file_uploader')[0]
        filename = upfile.filename
        filedata = upfile.value
        fobj = open(file_path,'w')#'w' is for 'write'
        fobj.write(filedata)
        fobj.close()
        if filename != None or len(filename) > 2:
            filesplit = filename.split(".")
        if filename == None or filename == "":
            html.write("<p style=\"font-size:10px;\">Please Choose the file for Upgrade<br/><br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")    
        elif filesplit[-1] != "img":
            html.write("<p style=\"font-size:10px;\">Please Choose right image file for upgrade<br/><br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
        else:
            html.write("<p style=\"font-size:10px;\">Firmware Uploading....<br/>Please Wait....<p/>")
            time.sleep(1)
            html.write("<p style=\"font-size:10px;\">Firmware Upload Successfully<p/>")        
            time.sleep(1)
            html.write("<p style=\"font-size:10px;\">Image Verified Successfully.. you can continue with scheduling..<p/><div id=\"file_uploader_div\" name=\"file_uploader_div\" style=\"display:none\">hello</div>")
            html.req.session["firmware_file"]=file_path
            html.req.session.save()
        #time.sleep(3)
        #html.write("<p style=\"font-size:10px;\">Firmware Upgrade Successfully.<p/>")
    except Exception,e:
        html.write(str(e))

def device_firmware_view(h):
    global html
    html = h
    html.write("<form method=\"post\" name=\"scheduling_firmware_file_upload\"enctype=\"multipart/form-data\" action=\"scheduling_firmware_file_upload.py\" style=\"font-size:10px;\"><label style=\"margin-top: 15px;margin-right: 25px;\" class=\"lbl\">Firmware File</label><input style=\"font-size:10px;\" type=\"file\" name=\"file_uploader\" id=\"file_uploader\"><button name=\"button_uploader\" id=\"button_uploader\" type=\"file\" style=\"font-size:10px;\" class=\"yo-button yo-small\"><span class=\"upload\">Upload</span></button></form>")

def create_crontab_file(user_name):
    commands = "python2.6 /omd/daemon/odu_scheduling.py "
    crontabString = ""
    commandString = ""
    event1 = "Down"
    event2 = "Up"
    event3="Firmware"
    apI1 = 0
    apI2 = 0
    device_type=""
    sitename = __file__.split("/")[3]
    odu_bll_obj=OduSchedulingBll()
    schedule_id="0"
    try:
        result = odu_bll_obj.crontab_select_schedule()
        for row in result:
            apI1 = 0
            apI2 = 0
            if row[1] =="Firmware":
                event1 = "Firmware"
                event2 = "Firmware"
            elif row[1] == "Down":
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
            schedule_id=str(row[0])
            sDateObj = datetime.datetime(int(sDate[0]),int(sDate[1]),int(sDate[2]),int(sTime[0]),int(sTime[1]),int(sTime[2]))
            eDateObj = datetime.datetime(int(eDate[0]),int(eDate[1]),int(eDate[2]),int(eTime[0]),int(eTime[1]),int(eTime[2]))
            if row[6] == 0:            # this is for non repeated scheduling
                if sDateObj > now:
                    commandString = sTime[1] + " " + sTime[0] + " " + sDate[2] + " " + sDate[1] + " * "
                    apresult=odu_bll_obj.crontab_details(row[0])
                    schedule_id=str(row[0])
                    port = "-1"
                    username = "username"
                    password = "password"
                    ip = "255.255.255.255"
                    for aprow in apresult:
                        if apI1 > 0:
                            crontabString += " 0 -1\n"
                        if str(aprow[0]) != "":
                            ip = str(aprow[0])
                        if str(aprow[4]) !="":
                            device_type =str(aprow[4])
#                              if str(aprow[1]) != "":
#                                   username = str(aprow[1])
#                              if str(aprow[2]) != "":
#                                   password = str(aprow[2])
#                              if str(aprow[3]).strip() != "":
#                                   port = str(aprow[3]).strip()
                        crontabString += commandString + commands +  ip + " "  + device_type + " " + event1 + " " + str(schedule_id) + " " + user_name
                        apI1 += 1
                    crontabString += " 1 -1\n"
                if eDateObj > now and event2!="Firmware":
                    commandString = eTime[1] + " " + eTime[0] + " " + eDate[2] + " " + eDate[1] + " * " 
                    apresult=odu_bll_obj.crontab_details(row[0])
                    schedule_id=row[0]
                    port = "-1"
                    username = "username"
                    password = "password"
                    ip = "255.255.255.255"
                    for aprow in apresult:
                        if apI2 > 0:
                            crontabString += " 0 -1\n"
                        if str(aprow[0]) != "":
                            ip = str(aprow[0])
                        if str(aprow[4]) !="":
                            device_type =str(aprow[4])
#                              if str(aprow[1]) != "":
#                                   username = str(aprow[1])
#                              if str(aprow[2]) != "":
#                                   password = str(aprow[2])
#                              if str(aprow[3]).strip() != "":
#                                   port = str(aprow[3]).strip()
                        crontabString += commandString + commands + ip + " " +  device_type + " " + event2 + " " + str(schedule_id) + " " + user_name
                        apI2 += 1
                    crontabString += " 1 -1\n"

            else:                # this is for repeated scheduling
                if row[7] == "Daily":
                    commandString1 = sTime[1] + " " + sTime[0] + " * * * "
                    commandString2 = eTime[1] + " " + eTime[0] + " * * * "
                    apresult=odu_bll_obj.crontab_details(row[0])
                    schedule_id=str(row[0])
                    port = "-1"
                    username = "username"
                    password = "password"
                    ip = "255.255.255.255"
                    for aprow in apresult:
                        if str(aprow[0]) != "":
                            ip = str(aprow[0])
                        if str(aprow[4]) !="":
                            device_type =str(aprow[4])
                        crontabString += commandString1 + commands + ip + " " +  device_type + " " + event1 +  " " + str(schedule_id)  + " " + user_name + " 0 -1\n"
                        if event2!="Firmware":
                            crontabString += commandString2 + commands + ip + " " +  device_type + " " + event2 +  " " + str(schedule_id)   + " " + user_name + " 0 -1\n"

                elif row[7] == "Weekly":
                    apresult=odu_bll_obj.crontab_details(row[0])
                    schedule_id=str(row[0])
                    port = "-1"
                    username = "username"
                    password = "password"
                    ip = "255.255.255.255"
                    dayI = 0
                    for aprow in apresult:
                        if str(aprow[0]) != "":
                            ip = str(aprow[0])
                        if str(aprow[4]) !="":
                            device_type =str(aprow[4])


                        commandString1 = sTime[1] + " " + sTime[0] + " * * "
                        commandString2 = eTime[1] + " " + eTime[0] + " * * "
                        dayI = 0
                        if row[8] == 1:    # sunday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "0" 
                            commandString2 += "0" 
                            dayI += 1
                        if row[9] == 1:    # monday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "1" 
                            commandString2 += "1"
                        if row[10] == 1:    # tuesday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "2" 
                            commandString2 += "2" 
                            dayI += 1
                        if row[11] == 1:    # wednusday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "3" 
                            commandString2 += "3"
                            dayI += 1
                        if row[12] == 1:    # thrusday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "4" 
                            commandString2 += "4" 
                            dayI += 1
                        if row[13] == 1:    # friday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "5" 
                            commandString2 += "5" 
                            dayI += 1
                        if row[14] == 1:    # saturday
                            if dayI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "6" 
                            commandString2 += "6" 
                            dayI += 1

                        crontabString += commandString1 + " " + commands  + ip + " " +  device_type + " " + event1 +  " " + str(schedule_id)  + " " + user_name +  " 0 -1\n"
                        if event2!="Firmware":
                            crontabString += commandString2 + " " + commands  + ip + " " +  device_type + " " + event2 +  " " + str(schedule_id)   + " " + user_name + " 0 -1\n"

                elif row[7] == "Monthly":
                    apresult=odu_bll_obj.crontab_details(row[0])
                    schedule_id=str(row[0])
                    port = "-1"
                    username = "username"
                    password = "password"
                    ip = "255.255.255.255"
                    monthI = 0
                    for aprow in apresult:
                        if str(aprow[0]) != "":
                            ip = str(aprow[0])
                        if str(aprow[4]) !="":
                            device_type =str(aprow[4])

                        monthI = 0
                        commandString1 = sTime[1] + " " + sTime[0] + " " + str(row[27]) + " "
                        commandString2 = sTime[1] + " " + sTime[0] + " " + str(row[27]) + " "
                        if row[15] == 1:    # jan
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "1" 
                            commandString2 += "1"
                            monthI += 1
                        if row[16] == 1:    # feb
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "2" 
                            commandString2 += "2"
                            monthI += 1
                        if row[17] == 1:    # mar
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "3" 
                            commandString2 += "3"
                            monthI += 1
                        if row[18] == 1:    # apr
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "4" 
                            commandString2 += "4" 
                            monthI += 1
                        if row[19] == 1:    # may
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "5" 
                            commandString2 += "5" 
                            monthI += 1
                        if row[20] == 1:    # jun
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "6" 
                            commandString2 += "6" 
                            monthI += 1
                        if row[21] == 1:    # jul
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "7" 
                            commandString2 += "7" 
                            monthI += 1
                        if row[22] == 1:    # aug
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "8" 
                            commandString2 += "8" 
                            monthI += 1
                        if row[23] == 1:    # sep
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "9" 
                            commandString2 += "9" 
                            monthI += 1
                        if row[24] == 1:    # oct
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "10" 
                            commandString2 += "10" 
                            monthI += 1
                        if row[25] == 1:    # nov
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "11" 
                            commandString2 += "11" 
                            monthI += 1
                        if row[26] == 1:    # dec
                            if monthI > 0:
                                commandString1 += ","
                                commandString2 += ","
                            commandString1 += "12" 
                            commandString2 += "12" 
                            monthI += 1

                        crontabString += commandString1 + " * " + commands  + ip + " " +  device_type + " " + event1 +  " " + str(schedule_id)  + " " + user_name + " 0 -1\n"
                        if event2!="Firmware":
                            crontabString += commandString2 + " * " + commands  + ip + " " +  device_type + " " + event2 +  " " + str(schedule_id)  + " " + user_name + " 0 -1\n"
        # prepare SQL query to create crontab
        #result = odu_bll_obj.crontab_repeat_schedule()
        #if (len(result)!=0):
            #    for row in result:
            #        port = "-1"
    #	   username = "username"
    #	   password = "password"
    #	   ip = "255.255.255.255"
    #	   event = "Unknown"

    #	   sDate = str(row[1]).split("-")
    #	   sTime = str(row[2]).split(":")
    #	commandString = sTime[1] + " " + sTime[0] + " " + sDate[2] + " " + sDate[1] + " * "
#
    #	   if str(row[3]) != "":
    #	       ip = str(row[3])
    #           if str(aprow[4]) !="":
    #                device_type =str(aprow[4])
    #	   if str(row[8]).strip() != "":
    #	       event = str(row[8]).strip()
    #	   crontabString += commandString + commands + ip + " "  +  device_type + " " + event + " 0 " + str(row[0]) + "\n"

        fobj = open("/omd/sites/%s/etc/cron.d/crontab"%(sitename),"w")
        fobj.write(crontabString)
        fobj.close()
        os.popen('sh /omd/sites/%s/etc/init.d/crontab start'%(sitename))
        #f=open("/home/cscape/Desktop/acb.txt","a")
        #f.write(user_name)
        #f.close()

    except Exception ,e:
        #f=open("/home/cscape/Desktop/acb.txt","a")
        #f.write(str(e))
        #f.close()
        error = "some error occur"



################################## Scheduling #####################################

#################################### AP Radio Status ##############################
def radio_status(h):
    socket.setdefaulttimeout(1)
    global html
    html = h
    css_list = ["css/style.css","fullcalendar/fullcalendar.css"]
    js_list = ["js/jquery-ui-1.8.6.custom.min.js","fullcalendar/fullcalendar.min.js","js/radio_status.js"]
    header_btn = ""
    html.new_header("Radio Status","manage_ap_configuration.py",header_btn,css_list,js_list)
    odu_bll_obj=OduSchedulingBll()
    result = odu_bll_obj.radio_status()
    tableString=OduScheduling.radio_status(result)
    html.write(tableString)
    html.new_footer()
    # image uploader div
    html.write("<div class=\"loading\"><img src='images/loading.gif' alt='loading...'/></div>")


def change_redio(h):
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
        auth_string = base64.encodestring("%s:%s" % (username,password))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
    except urllib2.HTTPError, e:
        response = str(e.code)    # send http error code
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
        message = "UBR not connected"
    html.write(message)

#################################### AP Radio Status ##############################




def view_page_tip_scheduling(h):
    global html
    html = h
    html.write(OduScheduling.view_page_tip_scheduling())          