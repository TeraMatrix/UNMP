#!/usr/bin/python2.6
import urllib2, base64, sys, datetime, MySQLdb, os
import socket
import pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.api import v2c
import pycurl
import StringIO
from datetime import datetime
import time


# 30 1 * * * python /omd/daemon/odu_scheduling.py admin password -1 192.168.1.205 Down 0 -1
# m h D M w command username password port ip event re-Execute retry-id
arg = sys.argv
ip = arg[1]
device_type=arg[2]

tempUrl = ""
response = ""
message = ""
state=arg[3]
schedule_id=arg[4]
user_name=arg[5]
#ap state .1.3.6.1.4.1.26149.10.2.2.1.0
#ap save .1.3.6.1.4.1.26149.10.5.3.0
#ap reboot .1.3.6.1.4.1.26149.10.5.1.0
MySql_file = '/omd/daemon/config.rg'
dict_details_on={}
dict_details_off={}
dict_save={}
dict_reboot={}
dict_details_on["odu16"]= ["161", "private", ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1','Integer32','1']]
dict_details_on["odu100"]=["161", "private", ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1','Integer32','1']]
dict_details_off["odu16"]= ["161", "private", ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1','Integer32','0']]
dict_details_off["odu100"]=["161", "private", ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1','Integer32','0']]

dict_details_off["idu4"]= ["8001", "private", ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1','Integer32','0']]
dict_details_on["idu4"]=["8001", "private", ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1','Integer32','0']]

dict_details_on["ap25"]=["161", "private", ['1.3.6.1.4.1.26149.10.2.2.1.0','Integer32','1']]
dict_details_off["ap25"]= ["161", "private", ['1.3.6.1.4.1.26149.10.2.2.1.0','Integer32','0']]
dict_save["ap25"]=["161", "private", ['1.3.6.1.4.1.26149.10.5.3.0','Integer32','1']]
dict_reboot["ap25"]=["161", "private", ['1.3.6.1.4.1.26149.10.5.1.0','Integer32','1']]

opt={}
opt['success']=1
opt['message']=""
opt['result']=""
if(os.path.isfile(MySql_file)):    # getting variables from config file    
    execfile(MySql_file)
else:
    hostname = "localhost"
    username = "root"
    password = "root"
    schema = "nmsp"


def firmware_file_upload_ap_odu(ip_address,file_path,hostname_db,username_db,password_db,schema,device_type):#ap25 , odu16 , odu100
    try:
        success=0
        str_msg=""
        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        #file_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/image.img" %(nms_instance)
        #form = util.FieldStorage(h.req,keep_blank_values=1)
        #upfile = form.getlist('file_uploader')[0]
        #filename = upfile.filename
        #filedata = upfile.value
        #fobj = open(file_path,'w')#'w' is for 'write'
        #fobj.write(filedata)
        #fobj.close()
        password=''
        user_name=''
        #if filename == None or filename == "":
            #html.write("<p style=\"font-size:10px;\">Please Choose the file for Upgrade<br/><br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
        #else:
           # db,cursor=mysql_connection('midnms')
            #if db ==1:
            #    raise SelfException(cursor)
        # get the ip address of ap correspondence
        db = MySQLdb.connect(hostname_db,username_db,password_db,schema)   
	cursor = db.cursor()
	sel_query="SELECT ip_address,http_username,http_password FROM hosts WHERE ip_address='%s'"%(ip_address)
	cursor.execute(sel_query)
	result=cursor.fetchall()
	if len(result)>0:
	        ip_address=result[0][0]
	        user_name='' if  result[0][1]==None else result[0][1] 
	        password='' if  result[0][2]==None else result[0][2]
	        c = pycurl.Curl()
	        b = StringIO.StringIO()
	        file =file_path
	        #print file_path
	        values = [('image' , (c.FORM_FILE,  file))]
	        if device_type=="ap25":
	            c.setopt(pycurl.URL, "http://%s/cgi-bin/FirmwareUpgrade"%ip_address)
	        elif device_type=="odu16":
	            c.setopt(pycurl.URL, "http://%s:5555/cgi-bin/index"%ip_address)
	        else:
	            c.setopt(pycurl.URL, "http://%s/cgi-bin/index"%ip_address)
	        #c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])http://172.22.0.101/cgi-bin/FirmwareUpgrade
	        c.setopt(c.HTTPPOST,  values)
	        c.setopt(pycurl.VERBOSE, 0)
	        c.setopt(pycurl.USERPWD, user_name+':'+password)
	        c.setopt(c.WRITEFUNCTION, b.write)
	        c.perform()
	        responseCode = c.getinfo(pycurl.RESPONSE_CODE)
                responseString =  b.getvalue()
	        c.close()
	        if int(responseCode)==404:
	            success=1
	            str_msg="The path of firmware upload is not correct"
	            #html.write("<p style=\"font-size:10px;font-wight:bold;\">The path of firmware upload is not correct.<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
	        elif int(responseCode)==401:
		    success=1
		    str_msg="Username and Password are wrong"
	            #html.write("<p style=\"font-size:10px;font-wight:bold;\">Username and Password are wrong.<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
	        elif int(responseCode)==200:
	            result = responseString.find("Firmware image has bad magic number")
	            if result != -1:
	                success=1
	                str_msg="Wrong File is Uploaded"
	                #html.write("<p style=\"font-size:10px;font-wight:bold;\">Wrong File is Uploaded<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
	            result = responseString.find("Firmware upgrade complete")
	            if result != -1:
	                success=0
	                str_msg="Firmware Update Successfully"
	                #html.write("<p style=\"font-size:10px;font-wight:bold;\">Firmware Update Successfully</p>")
	            result = responseString.find("Device is now being automatically rebooted")
	            if result != -1:
	                success=0
	                str_msg="Firmware Update Successfully"
	                #html.write("<p style=\"font-size:10px;font-wight:bold;\">Firmware Update Successfully</p>")
                
                else:
                    success=1
                    str_msg="Host does not exists so check the host and try again"
                    #html.write("<p style=\"font-size:10px;font-wight:bold;\">Host does not exists so check the host and try again.</p>")
	db.close()
    except pycurl.error,e:
        if int(e[0])==7:
            success=1
            str_msg="Device is not Connected"
            #html.write("<p style=\"font-size:10px;font-wight:bold;\">Device is not Connected.</p>")
        elif int(e[0])==26:
            success=1
            str_msg="The Firmware file is missing"
            #html.write("<p style=\"font-size:10px;font-wight:bold;\">The Firmware file is missing.</p>")
        else:
            success=1
            str_msg="Unkown Problem Occured"
            #html.write("Unkown Problem Occured")
    except Exception,e:
        success=1
        str_msg="Firmware update not done.Please try again.."#html.write("<p style=\"font-size:10px;font-wight:bold;\">Firmware update not done.Please try again...</p>")
    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success 
        final_responce_dict['message'] = str_msg 
        #final_responce_dict['result'] = response_dict
        print final_responce_dict
        return final_responce_dict
                


   
def firmware_file_upload_idu(ip_address,file_path,hostname_db,username_db,password_db,schema):#### idu
    try:
        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        flag = 0
        activate = 0
        idu_reboot = 0
        success=1
        str_msg=""
        current_time = datetime.now()
#        form = util.FieldStorage(h.req,keep_blank_values=1)
#        upfile = form.getlist('fufile')[0]
#        filename = upfile.filename
#        filedata = upfile.value
#        file_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/%s" %(nms_instance,filename)
#        fobj = open(file_path,'w')#'w' is for 'write'
#        fobj.write(filedata)
#        fobj.close()
        password=''
        user_name=''
        cgi_result = ""
        i = 0
        j = 0
        # get the ip address of ap correspondence
        db = MySQLdb.connect(hostname_db,username_db,password_db,schema)    
	cursor = db.cursor()    
        sel_query="SELECT ip_address,http_username,http_password,http_port FROM hosts WHERE ip_address='%s'"%(ip_address)
        cursor.execute(sel_query)
        result=cursor.fetchall()
        print result
        cursor.close()
        if len(result)>0:
            ip_address=result[0][0]
            user_name='' if  result[0][1]==None else result[0][1] 
            password='' if  result[0][2]==None else result[0][2]
            port = result[0][3]
            c = pycurl.Curl()
            b = StringIO.StringIO()
            file =file_path
            values = [('fufile' , (c.FORM_FILE,  file))]
            c.setopt(pycurl.URL, "http://%s:%s/cgi-bin/uploadfile.cgi"%(ip_address,port))
            c.setopt(c.HTTPPOST,  values)
            c.setopt(pycurl.VERBOSE, 0)
            c.setopt(pycurl.USERPWD, user_name+':'+password)
            c.setopt(c.WRITEFUNCTION, b.write)
            c.perform()
            responseCode = c.getinfo(pycurl.RESPONSE_CODE)
            responseString =  b.getvalue()
            c.close()
            if int(responseCode)==404:
                success=1
                str_msg="The path of firmware upload is not correct"
                #html.write("<p style=\"font-size:10px;font-wight:bold;\">The path of firmware upload is not correct.<br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
            elif int(responseCode)==401:
                success=1
                str_msg="Username and Password are wrong"
                #html.write("<p style=\"font-size:10px;font-wight:bold;\">Username and Password are wrong.<br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
            elif int(responseCode)==200:
                if responseString.find("File Transfer Complete")!=-1:
                    success=1
                    str_msg="File Transfer Complete.Please wait while system Saves the file.Activating the new image file.Please Wait..."
                    #html.write("<p style=\"font-size:10px;\">File Transfer Complete.Please wait while system Saves the file.<br/>Activating the new image file.Please Wait...</p>")
                
                    while(1):
                        #db,cursor=mysql_connection('midnms')
                        db = MySQLdb.connect(hostname_db,username_db,password_db,schema)   
			cursor = db.cursor() 
                        query = "select trap_event_id,description,timestamp from midnms.trap_alarms where trap_event_id = '%s' and agent_id = '%s' and timestamp>='%s'"%('4',str(ip_address),str(current_time)[:19])  
                        cursor.execute(query)
                        cgi_result = cursor.fetchall()
                        cursor.close()           
                        if i<10:                               
                            if len(cgi_result)>0:
                                current_time = cgi_result[0][2]
                                flag = 0
                                break
                            else:
                                i=i+1
                                time.sleep(15)
                                flag = 1
                                continue
                        else:
                            break
                   
                    if flag == 0:
                        if cgi_result[0][1] == "Image Upgrade Failure":
                	    success=1
                	    str_msg="Image Upload Failed.Please try again with right image"
                            #html.write("<p style=\"font-size:10px;\">Image Upload Failed.Please try again with right image<br/><br/><a href=\"javascript:history.go(-1)\">Back</a></p>")                 
                        elif cgi_result[0][1] == "New Image Upgrade Success":
                            success=1
                            str_msg="Image Upload Successfully.Plase wait for activating the image"
                            #html.write("<p style=\"font-size:10px;\">Image Upload Successfully.Plase wait for activating the image</p>")
                            c = pycurl.Curl()
                            b = StringIO.StringIO()
                            values = [('activate' , 'Activate')]
                            c.setopt(pycurl.URL, "http://%s:%s/cgi-bin/activateimage.cgi"%(ip_address,port))
                            c.setopt(c.HTTPPOST,  values)
                            c.setopt(pycurl.VERBOSE, 0)
                            c.setopt(pycurl.USERPWD, user_name+':'+password)
                            c.setopt(c.WRITEFUNCTION, b.write)
                            c.perform()
                            responseCode = c.getinfo(pycurl.RESPONSE_CODE)
                            responseString =  b.getvalue()
                            c.close()
                            if int(responseCode)==404:
                                success=1
                                str_msg="The path of firmware upload is not correct"
                                #html.write("<p style=\"font-size:10px;font-wight:bold;\">The path of firmware upload is not correct.<br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
                            elif int(responseCode)==401:
                                success=1
                                str_msg="Username and Password are wrong"
                                #html.write("<p style=\"font-size:10px;font-wight:bold;\">Username and Password are wrong.<br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
                            elif int(responseCode)==200:                          
                                while(1):
                                    #db,cursor=mysql_connection('midnms')
                                    db = MySQLdb.connect(hostname_db,username_db,password_db,schema)   
				    cursor = db.cursor() 
                                    query = "select trap_event_id,description,timestamp from midnms.trap_alarms where trap_event_id in ('%s','%s') and agent_id = '%s' and timestamp>'%s'"%('7','67',str(ip_address),str(current_time))  
                                    cursor.execute(query)
                                    cgi_final_result = cursor.fetchall()
                                    cursor.close()           
                                    j = 0
                                    if j<20:
                                        if len(cgi_final_result)>0:
                                            current_time = cgi_final_result[0][2]
                                            if activate == 0:
                                                if cgi_final_result[0][1].find("Activating passive image")!=-1:
                                        	    str_msg="Activating image"
                                                    #html.write("<p style=\"font-size:10px;font-wight:bold;\">Activating image.<br/></p>")
                                                    #html.write("<p style=\"font-size:10px;font-wight:bold;\">Device is rebooting.Please wait.....<br/></p>")
                                                    activate = 1                              
                                            if idu_reboot == 0:
                                                if cgi_final_result[0][1].find("IDU started")!=-1:
                                                    idu_reboot = 1
                                            if cgi_final_result[0][1].find("Image passed approval period. Image activation success")!=-1:
                                                str_msg="Firmware upgrade successfully"
                                                #html.write("<p style=\"font-size:10px;font-wight:bold;\">Firmware upgrade successfully.<br/></p>")
                                                flag = 0
                                                break
                                        else:
                                            j=j+1
                                            time.sleep(30)
                                            flag = 1
                                            continue
                                    else:
                                        flag = 1
                                        break
                            if flag == 0:
                                if idu_reboot == 1:
                                    str_msg="Device rebooted successfully"
                                    #html.write("<p style=\"font-size:10px;\">Device rebooted successfully</p>")  
                                    success=0               
                            else:
                                str_msg="Image Activation Failed.Please Try again"
                                #html.write("<p style=\"font-size:10px;\">Image Activation Failed.Please Try again<br/><br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
                                success=1
                        else:
                            str_msg="Host Not Exist"
                            #html.write("<p style=\"font-size:10px;\">Host Not Exist<br/><br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
                            success=1
	db.close()
    except pycurl.error,e:
        if int(e[0])==7:
	    success=1
	    str_msg="Device is not Connected"
            #html.write("<p style=\"font-size:10px;font-wight:bold;\">Device is not Connected.</p>")
        elif int(e[0])==26:
            success=1
            str_msg="The Firmware file is missing"
            #html.write("<p style=\"font-size:10px;font-wight:bold;\">The Firmware file is missing.</p>")
        else:
            success=1
            str_msg="Unkown Problem Occured"
            #html.write("Unkown Problem Occured")
    except Exception,e:
        print str(e)
        str_msg=str(e)
        success=1
    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success 
        final_responce_dict['message'] = str_msg
        #final_responce_dict['result'] = response_dict
        print final_responce_dict
        return final_responce_dict
        

def set_on_device(ip_address,port,community,received_list):
    """
    received_list = [ oid_str, datatype, value ]
    
    """
    try:
        make_tuple = lambda x: tuple(int(i) for i in x.split('.'))      #@note: this lambda function used to convert a oid string to oid tuple (in a format required by pysnmp)  
        success = 0
        if ip_address != None and port != None and community != None:
            response_dict = {}
            set_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s))"%(community,ip_address,port)

            oid_str,datatype,value = received_list
            oid_tuple = make_tuple(oid_str) 
            set_str = set_str+",(%s,v2c.%s('%s'))"%(oid_tuple,datatype,value)
                            
            set_str = set_str+')'
            
            try:               
                exec set_str in locals(),globals()
                                
                if errorIndication:
                    success = 1
                    response_dict[553] = str(errorIndication)
                      
                else:             
                    if errorStatus > 0 and errorIndex != None:
                        success = 1
                        response_dict[oid_str] = int(errorStatus)  
                                          
                    elif errorStatus == 0:
                        #response_dict[0] = 'all_field_set_sucessfully' 
                        for name, val in varBinds:
                            response_dict[oid_str] = " ok "
                        
            
            
            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[551] = sock_errstr                
            except pysnmp.proto.error.ProtocolError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'pyproto err '+str(err)
            except TypeError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'type err '+str(err)
            except Exception as e:
                response_dict = {}
                success = 1
                response_dict[99] = 'pysnmp exception '+str(e)
        else:
            response_dict = {}
            success = 1
            response_dict[97] = 'IP or Port or community not present'
    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer err '+str(e)
    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success 
        final_responce_dict['result'] = response_dict
        return final_responce_dict

# is_deleted=0 means event has occurred ... time of event is old than current time
#is_success=0 means event occurred successfully 
#is_success=1 means event failed 
#update_time=time of event occurrence 
#print set_on_device("172.22.0.102", "161", "private", ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1','Integer32','1'])
status_msg="Scheduling done successfully for host with ip %s"%(ip)
if state=="Firmware":
    db = MySQLdb.connect(hostname,username,password,schema)    
    cursor = db.cursor()    
    ssql = "select firmware_file_name from odu_host_schedule as ohs inner join (select host_id,ip_address from hosts) as h on h.host_id=ohs.host_id  \
		where h.ip_address='%s' and ohs.schedule_id = '%s' " % (str(ip),schedule_id)
    cursor.execute(ssql)
    res=cursor.fetchall()
    
    file_path=res[0][0]
    if device_type=="ap25" or device_type=="odu16" or device_type=="odu100" :
	output=firmware_file_upload_ap_odu(ip,file_path,hostname,username,password,schema,device_type)
	opt=output
    else:
	output=firmware_file_upload_idu(ip,file_path,hostname,username,password,schema)
	opt=output
    #print output
elif device_type!="ap25":
    if state=="Down":
        output=set_on_device(ip,dict_details_off[device_type][0],dict_details_off[device_type][1],dict_details_off[device_type][2])
        opt=output
    if state=="Up":
        output=set_on_device(ip,dict_details_on[device_type][0],dict_details_on[device_type][1],dict_details_on[device_type][2])
        opt=output
    #print output
else:
    if state=="Down":
        output=set_on_device(ip,dict_details_off[device_type][0],dict_details_off[device_type][1],dict_details_off[device_type][2])
        print output
        opt=output
        if(str(output['success'])=='0'):
            output=set_on_device(ip,dict_save[device_type][0],dict_save[device_type][1],dict_save[device_type][2])
            print output
            opt=output
            if(str(output['success'])=='0'):
                output=set_on_device(ip,dict_reboot[device_type][0],dict_reboot[device_type][1],dict_reboot[device_type][2])
                print output
                opt=output
    if state=="Up":
        output=set_on_device(ip,dict_details_on[device_type][0],dict_details_on[device_type][1],dict_details_on[device_type][2])
        print output
        opt=output
        if(str(output['success'])=='0'):
            output=set_on_device(ip,dict_save[device_type][0],dict_save[device_type][1],dict_save[device_type][2])
            print output
            opt=output
            if(str(output['success'])=='0'):
                output=set_on_device(ip,dict_reboot[device_type][0],dict_reboot[device_type][1],dict_reboot[device_type][2])
                print output
                opt=output
    
try:
    db = MySQLdb.connect(hostname,username,password,schema)    
    cursor = db.cursor()    
    sql = "UPDATE odu_schedule set is_deleted=0,is_success=%s,update_time='%s' WHERE schedule_id = %s" % (opt['success'],str(datetime.now())[:19],schedule_id)
    cursor.execute(sql)
    mesg=""
    if state=="Firmware":
	ssql = "UPDATE odu_host_schedule as ohs inner join (select host_id,ip_address from hosts) as h on h.host_id=ohs.host_id set ohs.is_success='%s',ohs.message='%s' \
		where h.ip_address='%s' and ohs.schedule_id = '%s' " % (opt['success'],opt["message"],str(ip),schedule_id)
	mesg=opt["message"]
    else:
	ssql = "UPDATE odu_host_schedule as ohs inner join (select host_id,ip_address from hosts) as h on h.host_id=ohs.host_id set ohs.is_success='%s' \
		where h.ip_address='%s' and ohs.schedule_id = '%s' " % (opt['success'],str(ip),schedule_id)
	try:
	    mesg=opt["result"].keys()[0]
	except Exception,e:
	    mesg=""
    cursor.execute(ssql)
    try:
        if str(opt['success'])=='0':
            sql = "INSERT INTO event_log values('null','%s',null,'Scheduling done successfully for host with ip %s','%s')" % (user_name,ip,str(datetime.now())[:19])
        else:
            if mesg=="":
                sql = "INSERT INTO event_log values('null','%s',null,'Scheduling failed for host with ip %s','%s')" % (user_name,ip,str(datetime.now())[:19])
            else:
                sql = "INSERT INTO event_log values('null','%s',null,'Scheduling failed for host with ip %s (error : %s)','%s')" % (user_name,ip,mesg,str(datetime.now())[:19])
    except Exception,e:
        sql = "INSERT INTO event_log values('null','%s',null,'Scheduling done successfully for host with ip %s','%s')" % (user_name,ip,str(datetime.now())[:19])
    cursor.execute(sql)
    db.commit()
    db.close()
except Exception ,e :
    print str(e)
    #db.close()
    
 
        #html.write(str(e))
        #html.write("<p style=\"font-size:10px;font-wight:bold;\">Firmware update not done.Please try again...</p>")    

    #f=open("/home/cscape/Desktop/acb.txt","w")
    #f.write(str(e))
    #f.write(sql)
    #f.close()
#
#def delete_retry_entry(retryId):
#     # Open database connection
#     db = MySQLdb.connect(hostname,username,password,schema)
#
#     # prepare a cursor object using cursor() method
#     cursor = db.cursor()
#
#     # prepare SQL query to create repeated schedule
#     sql = "DELETE FROM repeat_odu_schedule WHERE repeatapscheduleid = %s" % (retryId)
#     cursor.execute(sql)
#     db.commit()
#
#def create_retry_entry(ipAddress,message,event):
#     now = datetime.datetime.now()
#     now = now + datetime.timedelta(minutes = 5)
#     datestamp = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
#     timestamp = str(now.hour) + ":" + str(now.minute) + ":00"
#     
#     i = 0
#     deviceId = 0
#
#     # Open database connection
#     db = MySQLdb.connect(hostname,username,password,schema)
#     # prepare a cursor object using cursor() method
#     cursor = db.cursor()
#     # prepare SQL query to get deviceId
#     sql = "SELECT id FROM nms_devices WHERE ipaddress = '%s'" % (ipAddress)
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     for row in result:
#          deviceId = row[0]
#          i += 1
#
#     if i > 0:
#          # prepare SQL query to create repeated schedule
#          sql = "INSERT INTO repeat_odu_schedule(datestamp,timestamp,deviceid,message,event) VALUES('%s','%s',%s,'%s','%s')" % (datestamp,timestamp,deviceId,message,event)
#          cursor.execute(sql)
#          db.commit()
#     db.close()
#     
#     
#     
#
#def create_crontab_file():
#     commands = "python /omd/daemon/odu_scheduling.py "
#     crontabString = ""
#     commandString = ""
#     event1 = "Down"
#     event2 = "Up"
#     apI1 = 0
#     apI2 = 0
#     device_type=""
#     sitename = __file__.split("/")[3]
#     odu_bll_obj=OduSchedulingBll()
#     try:
#          result = odu_bll_obj.crontab_select_schedule()
#          for row in result:
#               apI1 = 0
#               apI2 = 0
#               if row[1] == "Down":
#                    event1 = "Down"
#                    event2 = "Up"
#               else:
#                    event1 = "Up"
#                    event2 = "Down"
#               sDate = str(row[2]).split("-")
#               sTime = str(row[4]).split(":")
#               eDate = str(row[3]).split("-")
#               eTime = str(row[5]).split(":")
#               now = datetime.datetime.now()
#               sDateObj = datetime.datetime(int(sDate[0]),int(sDate[1]),int(sDate[2]),int(sTime[0]),int(sTime[1]),int(sTime[2]))
#               eDateObj = datetime.datetime(int(eDate[0]),int(eDate[1]),int(eDate[2]),int(eTime[0]),int(eTime[1]),int(eTime[2]))
#
#               if row[6] == 0:            # this is for non repeated scheduling
#                    if sDateObj > now:
#                         commandString = sTime[1] + " " + sTime[0] + " " + sDate[2] + " " + sDate[1] + " * "
#                         apresult=odu_bll_obj.crontab_details(row[0])
#                         port = "-1"
#                         username = "username"
#                         password = "password"
#                         ip = "255.255.255.255"
#                         for aprow in apresult:
#                              if apI1 > 0:
#                                   crontabString += " 0 -1\n"
#                              if str(aprow[0]) != "":
#                                   ip = str(aprow[0])
#                              if str(aprow[4]) !="":
#                                  device_type =str(aprow[4])
##                              if str(aprow[1]) != "":
##                                   username = str(aprow[1])
##                              if str(aprow[2]) != "":
##                                   password = str(aprow[2])
##                              if str(aprow[3]).strip() != "":
##                                   port = str(aprow[3]).strip()
#                              crontabString += commandString + commands +  ip + " "  + device_type + " " + event1
#                              apI1 += 1
#                         crontabString += " 1 -1\n"
#             
#                    if eDateObj > now:
#                         commandString = eTime[1] + " " + eTime[0] + " " + eDate[2] + " " + eDate[1] + " * "
#                         apresult=odu_bll_obj.crontab_details(row[0])
#                         port = "-1"
#                         username = "username"
#                         password = "password"
#                         ip = "255.255.255.255"
#                         for aprow in apresult:
#                              if apI2 > 0:
#                                   crontabString += " 0 -1\n"
#                              if str(aprow[0]) != "":
#                                   ip = str(aprow[0])
#                              if str(aprow[4]) !="":
#                                   device_type =str(aprow[4])
##                              if str(aprow[1]) != "":
##                                   username = str(aprow[1])
##                              if str(aprow[2]) != "":
##                                   password = str(aprow[2])
##                              if str(aprow[3]).strip() != "":
##                                   port = str(aprow[3]).strip()
#                              crontabString += commandString + commands + ip + " " +  device_type + " " + event2
#                              apI2 += 1
#                         crontabString += " 1 -1\n"
#
#               else:                # this is for repeated scheduling
#                    if row[7] == "Daily":
#                         commandString1 = sTime[1] + " " + sTime[0] + " * * * "
#                         commandString2 = eTime[1] + " " + eTime[0] + " * * * "
#                         apresult=odu_bll_obj.crontab_details(row[0])
#                         port = "-1"
#                         username = "username"
#                         password = "password"
#                         ip = "255.255.255.255"
#                         for aprow in apresult:
#                              if str(aprow[0]) != "":
#                                   ip = str(aprow[0])
#                              if str(aprow[4]) !="":
#                                   device_type =str(aprow[4])
#                              crontabString += commandString1 + commands + ip + " " +  device_type + " " + event1 + " 0 -1\n"
#                              crontabString += commandString2 + commands + ip + " " +  device_type + " " + event2 + " 0 -1\n"
#
#                    elif row[7] == "Weekly":
#                         apresult=odu_bll_obj.crontab_details(row[0])
#                         port = "-1"
#                         username = "username"
#                         password = "password"
#                         ip = "255.255.255.255"
#                         dayI = 0
#                         for aprow in apresult:
#                              if str(aprow[0]) != "":
#                                   ip = str(aprow[0])
#                              if str(aprow[4]) !="":
#                                   device_type =str(aprow[4])
#
#
#                              commandString1 = sTime[1] + " " + sTime[0] + " * * "
#                              commandString2 = eTime[1] + " " + eTime[0] + " * * "
#                              dayI = 0
#                              if row[8] == 1:    # sunday
#                                   if dayI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "0" 
#                                   commandString2 += "0" 
#                                   dayI += 1
#                              if row[9] == 1:    # monday
#                                   if dayI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "1" 
#                                   commandString2 += "1"
#                              if row[10] == 1:    # tuesday
#                                   if dayI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "2" 
#                                   commandString2 += "2" 
#                                   dayI += 1
#                              if row[11] == 1:    # wednusday
#                                   if dayI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "3" 
#                                   commandString2 += "3"
#                                   dayI += 1
#                              if row[12] == 1:    # thrusday
#                                   if dayI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "4" 
#                                   commandString2 += "4" 
#                                   dayI += 1
#                              if row[13] == 1:    # friday
#                                   if dayI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "5" 
#                                   commandString2 += "5" 
#                                   dayI += 1
#                              if row[14] == 1:    # saturday
#                                   if dayI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "6" 
#                                   commandString2 += "6" 
#                                   dayI += 1
#
#                              crontabString += commandString1 + " " + commands  + ip + " " +  device_type + " " + event1 + " 0 -1\n"
#                              crontabString += commandString2 + " " + commands  + ip + " " +  device_type + " " + event2 + " 0 -1\n"
#
#                    elif row[7] == "Monthly":
#                         apresult=odu_bll_obj.crontab_details(row[0])
#                         port = "-1"
#                         username = "username"
#                         password = "password"
#                         ip = "255.255.255.255"
#                         monthI = 0
#                         for aprow in apresult:
#                              if str(aprow[0]) != "":
#                                   ip = str(aprow[0])
#                              if str(aprow[4]) !="":
#                                   device_type =str(aprow[4])
#                                   
#                              monthI = 0
#                              commandString1 = sTime[1] + " " + sTime[0] + " " + row[27] + " "
#                              commandString2 = sTime[1] + " " + sTime[0] + " " + row[27] + " "
#                              if row[15] == 1:    # jan
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "1" 
#                                   commandString2 += "1"
#                                   monthI += 1
#                              if row[16] == 1:    # feb
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "2" 
#                                   commandString2 += "2"
#                                   monthI += 1
#                              if row[17] == 1:    # mar
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "3" 
#                                   commandString2 += "3"
#                                   monthI += 1
#                              if row[18] == 1:    # apr
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "4" 
#                                   commandString2 += "4" 
#                                   monthI += 1
#                              if row[19] == 1:    # may
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "5" 
#                                   commandString2 += "5" 
#                                   monthI += 1
#                              if row[20] == 1:    # jun
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "6" 
#                                   commandString2 += "6" 
#                                   monthI += 1
#                              if row[21] == 1:    # jul
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "7" 
#                                   commandString2 += "7" 
#                                   monthI += 1
#                              if row[22] == 1:    # aug
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "8" 
#                                   commandString2 += "8" 
#                                   monthI += 1
#                              if row[23] == 1:    # sep
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "9" 
#                                   commandString2 += "9" 
#                                   monthI += 1
#                              if row[24] == 1:    # oct
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "10" 
#                                   commandString2 += "10" 
#                                   monthI += 1
#                              if row[25] == 1:    # nov
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "11" 
#                                   commandString2 += "11" 
#                                   monthI += 1
#                              if row[26] == 1:    # dec
#                                   if monthI > 0:
#                                        commandString1 += ","
#                                        commandString2 += ","
#                                   commandString1 += "12" 
#                                   commandString2 += "12" 
#                                   monthI += 1
#
#                              crontabString += commandString1 + " * " + commands  + ip + " " +  device_type + " " + event1 + " 0 -1\n"
#                              crontabString += commandString2 + " * " + commands  + ip + " " +  device_type + " " + event2 + " 0 -1\n"
#          # prepare SQL query to create crontab
#          result = odu_bll_obj.crontab_repeat_schedule()
#          if (len(result)!=0):
#               for row in result:
#                   port = "-1"
#          username = "username"
#          password = "password"
#          ip = "255.255.255.255"
#          event = "Unknown"
#
#          sDate = str(row[1]).split("-")
#          sTime = str(row[2]).split(":")
#          commandString = sTime[1] + " " + sTime[0] + " " + sDate[2] + " " + sDate[1] + " * "
#
#          if str(row[3]) != "":
#              ip = str(row[3])
#              if str(aprow[4]) !="":
#                      device_type =str(aprow[4])
#          if str(row[8]).strip() != "":
#              event = str(row[8]).strip()
#          crontabString += commandString + commands + ip + " "  +  device_type + " " + event + " 0 " + str(row[0]) + "\n"
#
#          fobj = open("/omd/sites/%s/etc/cron.d/crontab"%(sitename),"w")
#          fobj.write(crontabString)
#          fobj.close()
#          os.popen('sh /omd/sites/%s/etc/init.d/crontab start'%(sitename))
#
#     except Exception ,e:
#          #f=open("/home/cscape/Desktop/acb.txt","w")
#          #f.write(str(e))
#          #f.close()
#          error = "some error occur"

#
#try:
#     req = urllib2.Request(url)
#     auth_string = base64.encodestring("%s:%s" % (username,password))
#     req.add_header("Authorization", "Basic %s" % auth_string)
#     f = urllib2.urlopen(req)
#     response = f.read()
#except urllib2.HTTPError, e:
#     response = str(e.code)	# send http error code
#except:
#     response = "Network Unreachable"
#
#
#if retryId != "-1":
#     delete_retry_entry(retryId)
#
#if response == "Enable Radio Request Received":
#     message = "Enable"
#     if reExecute == "1" or retryId != "-1":
#          create_crontab_file()
#elif response == "Disable  Request Received":
#     message = "Disable"
#     if reExecute == "1" or retryId != "-1":
#          create_crontab_file()
#elif response == "400":
#     message = "Bad Request"
#     create_retry_entry(arg[4],message,arg[5])
#     create_crontab_file()
#elif response == "401":
#     message = "User name and Password are wrong"
#     create_retry_entry(arg[4],message,arg[5])
#     create_crontab_file()
#elif response == "404":
#     message = "File Not Found"
#     create_retry_entry(arg[4],message,arg[5])
#     create_crontab_file()
#elif response == "501":
#     message = "Server Error"
#     create_retry_entry(arg[4],message,arg[5])
#     create_crontab_file()
#else:
#     message = "Access Point not connected"
#     create_retry_entry(arg[4],message,arg[5])
#     create_crontab_file()
#
