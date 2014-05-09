#!/usr/bin/python2.6

# import the modules
import os.path,sys,htmllib,config,MySQLdb,time
from lib import *
from mysql_exception import mysql_connection
from cgitb import html
from datetime import datetime
from common_bll import Essential

#######################################################################################	 
# Author			:	Rajendra Sharma
# Project			:	UNMP
# Version			:	0.1
# File Name			:	circle_graph.py
# Creation Date			:	18-September-2011
# Purpose			:	This file display the Network  map. This file show  all connected host from NMS.
# Copyright (c) 2011 Codescape Consultant Private Limited 

#######################################################################################

# success 0 means No error
# success 1  Exception or Error
# success 2 means some mysql error(services not running,connection not created)


# global variable for store the json format for all host data for particular  NMS.
json=""
# host chain contain the all host.
host_chain2 = []


#Exception class for own exception handling.
class SelfException(Exception):
        """
        @return: this class return the exception msg.
        @rtype: dictionary
        @requires: Exception class package(module)
        @author: Rajendra Sharma
        @since: 20 sept 2011
        @version: 0.1
        @date: 18 sept 2011
        @organization: Code Scape Consultants Pvt. Ltd.
        @copyright: 2011 Code Scape Consultants Pvt. Ltd.
        """
        def __init__(self,msg):
                output_dict={"success":2,"output":str(msg)}
                html.write(str(output_dict))



def recursive_function(graph, start, parent_len, temp_len):
        global json
        global host_chain2
        host_chain2 = host_chain2 + [start]
        for node in graph[start]:
                json += "{\"id\": \"%s\",\"name\":\"%s\",\"children\":["% (node,node)            # id why we are giving same id to all childern it should be different each 0 time
                parent_len -= 1
                if not node in host_chain2:
                        recursive_function(graph, node,len(graph[node]),parent_len)
        if temp_len == 0:
                json+= "]}"
        else:
                json+= "]},"

        return host_chain2




def graph(h):
        global html
        html=h
        nms_instance = __file__.split("/")[3]
        css_list = ["css/base.css","css/RGraph.css","css/sidepanel.css"]
        js_list = ["js/excanvas.js","js/jit.js","js/RGraph.js"]
        #snapin_list = ["reports","views","Alarm","Inventory","Settings","NetworkMaps","user_management","schedule","Listing"]

        html.new_header("Topology Map","circle_graph.py","",css_list,js_list)
        html.write("""<div id="center-container">\
			<div id="infovis"></div>\
			</div>
			<div id="host_details_div" style="display:none;">\
			<img src="images/close_button.png" alt="close"  style="position:absolute;top:5px;right:5px;" onclick='closeWindow();'/>\
			<div id="inner_details" style="display:none;" ></div>
			</div>
			<div id="log"></div>\
			<div class="cntr">\
			    <div id="ctr" class="s" ></div>\
			        <div id="cnt">\
			            <div id="f" class="inc">\
			                <div class="ftc"><span>NMS</span></div>\
			                <div class="fbc" id="nms_div"></div>\
			            </div>\
			        </div>\
			    </div>\
			</div>\
			""")
        html.write('<input type=\"hidden\" id=\"nms_instance\" name=\"nms_instance\" value=\"%s\" />'%(nms_instance))

        html.new_footer()
def show_network_graph(h):
        global html
        global json
        global host_chain2
        html=h
        relation_dic={}
        temp=[]
        temp2=[]
        temp3=[]
        parent_array=[]
        output_dict={} # this store the output result.
        nms_name=html.var('nms_name') # it store nms_name .

        try:
                # database connection and cursor object creation.
                db,cursor=mysql_connection('nms_sample')
                if db ==1:
                        raise SelfException(cursor)
                # get group id for login user
                userid =  html.req.session['user_id']
                es = Essential()
                hostgroup_ids_list = es.get_hostgroup_ids(userid)
                # end of code
                j=0
                sel_query="SELECT hosts.host_id,hosts.ip_address,hosts.host_name,host1.ip_address as parent_name,hosts.lock_status,hosts.host_state_id,host_states.state_name,host_assets.longitude,host_assets.latitude,hosts.device_type_id FROM \
			nms_instance INNER JOIN hosts ON nms_instance.nms_id=hosts.nms_id \
			INNER JOIN  host_states ON hosts.host_state_id = host_states.host_state_id \
			INNER JOIN host_assets ON host_assets.host_asset_id = hosts.host_asset_id \
			LEFT JOIN hosts as host1 ON host1.host_id = hosts.parent_name \
			WHERE hosts.is_deleted=0 and hosts.ip_address='localhost' and nms_instance.nms_name='%s'"%(nms_name) 
                cursor.execute(sel_query)
                # fetch the result.
                lc_result=cursor.fetchall()

                j=0
                if len(hostgroup_ids_list) > 0:
                        sql="SELECT hosts.host_id,hosts.ip_address,hosts.host_name,host1.ip_address as parent_name,hosts.lock_status,hosts.host_state_id,host_states.state_name,host_assets.longitude,host_assets.latitude,hosts.device_type_id FROM \
			nms_instance INNER JOIN hosts ON nms_instance.nms_id=hosts.nms_id \
			INNER JOIN  host_states ON hosts.host_state_id = host_states.host_state_id \
			INNER JOIN host_assets ON host_assets.host_asset_id = hosts.host_asset_id \
			INNER JOIN hosts as host1 ON host1.host_id = hosts.parent_name \
			INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
			INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
			WHERE hosts.is_deleted=0 and nms_instance.nms_name='%s' AND hostgroups.hostgroup_id IN (%s)"%(nms_name,','.join(hostgroup_ids_list)) 



                        cursor.execute(sql)
                        # fetch the result.
                        results=cursor.fetchall()
                else:
                        results = ()			
                if lc_result is not None:
#		for row in localhost_result:
                        json="{\"id\":\"%s\",\"name\":\"localhost\",\"children\":[" %(lc_result[0][0])


                for row in results:
                        if row[3]!= "" or row[3] != None:
                                parent_array.append([])
                                parent_array[j].append(row[1])
                                parent_array[j].append(row[3])

                        j+=1

                temp=[]
                i=0
                temp.append("localhost")
                while len(temp) > 0 or len(temp) != 0 :		
                        temp2=[]
                        for host in temp:
                                temp3=[]
                                for k in range(len(parent_array)):
                                        if host == parent_array[k][1]:
                                                temp2.append(parent_array[k][0]) 
                                                temp3.append(parent_array[k][0])
                                relation_dic[host]=temp3
                        temp=[]
                        temp=temp2
                host_chain2 = []
                if len(results)>0:
                        recursive_function(relation_dic, 'localhost',len(relation_dic['localhost']),0)
                else:
                        json="{}"

                output_dict={"success":0,"output":json}
                html.write(str(output_dict))

        # Exception Handling
        except MySQLdb as e:
                output_dict={"success":1,"output":str(e[-1])}
                html.write(str(output_dict))
                if db.open:
                        cursor.close()
                        db.close()
        except SelfException:
                pass
        except Exception as e:
                output_dict={"success":1,"output":str(e[-1])}
                html.write(str(output_dict))
                if db.open:
                        cursor.close()
                        db.close()
        finally:
                if db.open:
                        cursor.close()
                        db.close()


# This function is count the no of nms exist in the and create the json format for that nms with detail information.
# this function take the single html argument.
# this function return the dictinoray with nms information.
# Success 0 for No Error 
# Success 1 for Error

def network_nms_details(h):
        """
        @return: this function return the all NMS information.
        @rtype: this function return a dictnoray.
        @requires: this function take one html agrument.
        @author: Rajendra Sharma
        @since: 20 sept 2011
        @version: 0.1
        @date: 18 sept 2011
        @note: this function is count the no of nms exist in the and create the json format for that nms with detail information and its alseo provide the total enable host and disable host and 		NMS status.
        @organization: Code Scape Consultants Pvt. Ltd.
        @copyright: 2011 Code Scape Consultants Pvt. Ltd.
        """
        global html
        html=h
        enable_host=0 # count the total host for each nms.
        total_host=0 # count the enable host for each nms.
        nms_name='' # store the nms name. 
        output_dic={} # output dictinoray.
        try:
                # create the data base and cursor object.
                db,cursor=mysql_connection('nms_sample')
                if db ==1:
                        raise SelfException(cursor)

                sql="SELECT ni.nms_name FROM nms_instance as ni "
                cursor.execute(sql)
                nms_result=cursor.fetchall()
                # close the database and cursor connection.
                cursor.close()
                db.close()

                nms_data_json="" # it store the information in json format.
                nms_data_json+="["

                for  i in range(len(nms_result)):
                        nms_data_json+="{\"type\":\"nms\",\"name\":\"%s\"}%s"%(nms_result[i][0],(',' if i < len(nms_result)-1 else ''))

                nms_data_json+="]"

                output_dict={"success":0,"output":nms_data_json}
                html.write(str(output_dict))
        # Exception Handling
        except MySQLdb as e:
                output_dict={"success":1,"output":str(e[-1])}
                html.write(str(output_dict))
                if db.open:
                        cursor.close()
                        db.close()
        except SelfException:
                pass
        except Exception as e:
                output_dict={"success":1,"output":str(e[-1])}
                html.write(str(output_dict))
                if db.open:
                        cursor.close()
                        db.close()
        finally:
                if db.open:
                        cursor.close()
                        db.close()




# This fuction is responsible for the showing the details of all the hosts on the google map we will show this result in table format  on host click event.
# This function take single html argument.
# This function return  cliclable host inforamtion in dictionary.
# Success 0 for No Error.
# Success 1 for Error.
def show_host_details(h):
        """
        @return: this function return the host details like ipaddres,MAC address,services etc.
        @rtype: this function return a dictnoray.
        @requires: this function take one html agrument.
        @author: Rajendra Sharma
        @since: 20 sept 2011
        @version: 0.1
        @date: 18 sept 2011
        @note: this function return the services and information of host.
        @organization: Code Scape Consultants Pvt. Ltd.
        @copyright: 2011 Code Scape Consultants Pvt. Ltd.
        """
        global html
        html = h
        host_ip=html.var("hostIp")
        result = "0"
        ok=0        # its count the no of state of particular host
        critical=0
        warning=0
        unknown=0	
        host_age=0 # store the host age.
        checked=0 # check the host checked
        try:
                # create the data base and cursor object.
                db,cursor=mysql_connection('nms_sample')
                # check the database conection created or not.
                if db ==1:
                        raise SelfException(cursor)

		sel_query = "select device_type_id,device_name from device_type"
		cursor.execute(sel_query)
		device_type_result=cursor.fetchall()
		device_name_dict =dict((row[0],row[1]) for row in device_type_result)

                #device_name_dict={'odu100':'RM','odu16':'RM18','ap25':'Access Point','idu4':'IDU','idu8':'IDU','unknown':'Generic','ccu':'CCU'}

                sql = "SELECT  hosts.host_name,hosts.ip_address,hosts.mac_address,host_states.state_name,hosts.timestamp,hosts.host_id,hosts.device_type_id,hosts.host_alias FROM hosts INNER JOIN host_states ON hosts.host_state_id=host_states.host_state_id WHERE hosts.ip_address='%s'" %  host_ip
                # execute the query and fetch the result.
                cursor.execute(sql)
                result=cursor.fetchall()
                sql="SELECT trap_event_type FROM trap_alarm_current WHERE agent_id='%s' order by timestamp desc limit 1"%host_ip
                cursor.execute(sql)
                last_alarm=cursor.fetchone()

                # live query for services 
                # Live query using here.
                query_service = "GET services\nColumns: state description  host_last_state_change host_has_been_checked \nFilter: host_address = " + host_ip
                html.live.set_prepend_site(True)
                services = html.live.query(query_service)
                services.sort()
                html.live.set_prepend_site(False)

                for service_site,state, description, age, checked in services:
                        host_age=age
                        checked=checked
                        if state==0:
                                ok+=1
                        elif state==1:
                                warning+=1
                        elif state==2:
                                critical+=1
                        else:
                                unknown+=1


                host_name = "" # it store the host name 
                sevices_status="" # it store the service status.
                some_link="" # it store the dashboard,alarms link html
                host_detail_data="" # it contain the html
                if len(result)>0:
                        for row in result:
                                host_detail_data+="<div><table style=\"width:251px;font-size:11px;margin-bottom:10px;\">\
				<colgroup><col width=\"40%%\"/><col width=\"5%%\"/><col/></colgroup><tr><th align=\"left\" colspan=\"3\">\
				<u><a href=device_details_example.py?host_id=%s>%s(%s)</a></u></th></tr>"%(' ' if row[5]==" " or row[5]==None else row[5],row[7],'-' if row[1]=="" or row[1]==None else row[1])

                                if row[6]=='odu16' or row[6]=='odu100' or row[6]=='idu4' or row[6]=='ap25' or row[6]=='ccu':
                                        redirect_page='sp_dashboard_profiling'
                                else:
                                        redirect_page='localhost_dashboard'

                                host_name = '-' if row[0]=="" or row[0]==None else row[0]

                                sevices_status+="<table style=\"width:251px;font-size:11px;\"><colgroup><col width=\"25%%\"/><col width=\"25%%\"/><col width=\"25%%\"/><col width=\"25%%\"/></colgroup>"
                                sevices_status+="<tr><td title=\"ok\" style=\"background-color:#66C947; height:20px; width:20px; \"><lable><a href=device_details_example.py?host_id=%s alt=\"ok\" style=\"algin:center;\">%s</td>"%(' ' if row[5]==" " or row[5]==None else row[5],ok)
                                sevices_status+="<td title=\"warning\" style=\"background-color:#EEC72B; height:20px; width:20px;\"><lable><a href=device_details_example.py?host_id=%s alt=\"warning\">%s</td>"%(' ' if row[5]==" " or row[5]==None else row[5],warning)
                                sevices_status+="<td title=\"critical\" style=\"background-color:#F07546; height:20px; width:20px;\"><lable><a href=device_details_example.py?host_id=%s alt=\"critical\">%s</td>"%(' ' if row[5]==" " or row[5]==None else row[5],critical)
                                sevices_status+="<td title=\"unknown\" style=\"background-color:#1999CF; height:20px; width:20px;\"><lable><a href=device_details_example.py?host_id=%s alt=\"unknown\">%s</td></tr>"%(' ' if row[5]==" " or row[5]==None else row[5],unknown)


                                # This is for enabled the device
                                enable_html="<table style=\"width:251px;font-size:11px;\"><colgroup><col width=\"33%%\"/><col width=\"33%%\"/><col/><tr>\
				<td style=\"width:30px\"><lable style=\" width:100px; font-size:13px;\">\
				<img src=\"images/new/alert.png\" alt=\"Alarm\" title=\"Alarm\" style=\"width:12px;\"/>\
				<a href=status_snmptt.py?ip_address=%s- alt=\"Alarms\">Alarms</td>\
				<td><a href='javascript:enabledDevice(\"%s\");'> <img src=\"images/alert_restart.png\" alt=\"Enabled Device\" \
				title=\"Enabled Device\" style=\"width:12px;\"/> Enabled Device</a></td></tr></table>"%('' if row[1]=="" or row[1]==None else row[1],row[1])


                                some_link+="<table style=\"width:251px;font-size:11px;\"><colgroup><col width=\"33%%\"/><col width=\"33%%\"/><col/></colgroup><tr>"

                                if row[6]=='mou' or row[6] == 'rou':
                                        some_link+="<td style=\"width:30px\"><lable style=\" width:100px; font-size:13px;\">\
					    <img src=\"images/new/alert.png\" alt=\"Alarm\" title=\"Alarm\" style=\"width:12px;\"/>\
					    <a href=status_snmptt.py?ip_address=%s- alt=\"Alarms\">Alarms</td>"%('' if row[1]=="" or row[1]==None else row[1])
                                elif redirect_page=='localhost_dashboard':
                                        some_link+="<td style=\"width:30px\"><lable style=\" width:100px; font-size:13px;\">\
					<img src=\"images/new/graph.png\" alt=\"Alarm\" title=\"Alarm\" style=\"width:12px;\"/>\
					<a href=%s.py?host_id=%s&device_type=%s&device_list_state=enabled alt=\"Dashboard\">Dashboard</td></tr>\
					</table>"%(redirect_page,' ' if row[5]=="" or row[5]==None else row[5],' ' if row[6]=="" or row[6]==None else row[6])

                                else:
                                        some_link+="<td style=\"width:30px\"><lable style=\" width:100px; font-size:13px;\">\
					    <img src=\"images/new/alert.png\" alt=\"Alarm\" title=\"Alarm\" style=\"width:12px;\"/>\
					    <a href=status_snmptt.py?ip_address=%s- alt=\"Alarms\">Alarms</td>"%('' if row[1]=="" or row[1]==None else row[1])

                                        some_link+="<td style=\"width:30px\"><lable style=\" width:100px; font-size:13px;\">\
					<img src=\"images/new/graph.png\" alt=\"Alarm\" title=\"Alarm\" style=\"width:12px;\"/>\
					<a href=%s.py?host_id=%s&device_type=%s&device_list_state=enabled alt=\"Dashboard\">Dashboard</td></tr>\
					</table>"%(redirect_page,' ' if row[5]=="" or row[5]==None else row[5],' ' if row[6]=="" or row[6]==None else row[6])

                                host_detail_data+="<tr><td>Device Type </td><td>:</td><td> %s </td></tr>"%('-' if row[6]=="" or row[6]==None else device_name_dict[row[6].strip()])
                                if row[6]=='ap25':
                                        sel_query="SELECT count(*) FROM ap_connected_client inner join hosts on ap_connected_client.host_id=hosts.host_id  WHERE state='1' and hosts.ip_address='%s'"%(row[1])
                                        cursor.execute(sel_query)
                                        result=cursor.fetchall()
                                        host_detail_data+="<tr><td>Connected Client </td><td>:</td><td> %s </td></tr>"%('-' if result[0][0]=="" or result[0][0]==None else result[0][0])

                                host_detail_data+="<tr><td>MAC Address </td><td>:</td><td> %s </td></tr>"%('-' if row[2]=="" or row[2]==None else row[2])
                                host_detail_data+="<tr><td>Host Age </td><td>:</td><td> %s </td></tr>"%('-' if host_age==0 else paint_age(host_age, checked == 1, 60 * 10))
                                host_detail_data+="<tr><td>Last Update </td><td>:</td><td> %s </td></tr>"%('-' if row[4]=="" or row[4]==None else datetime.strftime(row[4],"%d %B %Y"))
                                host_detail_data+="<tr><td>Current Alarm</td><td>:</td><td>%s</td></tr></table>"%('-' if last_alarm==None else last_alarm[0])
                                if str(row[3]).strip()=='Disable':
                                        host_detail_data+=enable_html
                                else:
                                        host_detail_data+=some_link+sevices_status



                else:
                        host_detail_data+="<div><table style=\"width:300px;font-size:11px;margin-bottom:10px;\"><colgroup><col width=\"30%%\"/><col width=\"5%%\"/><col/></colgroup><tr><th align=\"left\" colspan=\"3\">No host inforamtion exits.</tr></th></table>"		

                host_detail_data+="</div>"
                output_dictt={"success":0,"output":str(host_detail_data)}
                html.write(str(output_dictt))
                # close the cursor and database connection.
                cursor.close()
                db.close()
        # Exception Handling
        except MySQLdb as e:
                output_dictt={"success":1,"output":str(e[-1])}
                html.write(str(output_dictt))
                if db.open:
                        cursor.close()
                        db.close()
        except SelfException:
                pass
        except Exception as e:
                output_dictt={"success":1,"output":str(e[-1])}
                html.write(str(output_dictt))
                if db.open:
                        cursor.close()
                        db.close()
        finally:
                if db.open:
                        cursor.close()
                        db.close()



def paint_age(timestamp, has_been_checked, bold_if_younger_than):
        """
        @return: this function return the host host status age.
        @rtype: this function return type string.
        @requires: this function take three argument 1. timestamp(total up tiem) , 2. this process checked or not(boolean value) , 3. total up time is grether than 10 min or not. .
        @author: Rajendra Sharma
        @since: 20 sept 2011
        @version: 0.1
        @date: 18 sept 2011
        @note: this function return the host host status age.
        @organization: Code Scape Consultants Pvt. Ltd.
        @copyright: 2011 Code Scape Consultants Pvt. Ltd.
        """
        if not has_been_checked:
                return "age", "-"

        age = time.time() - timestamp
        if age >= 48 * 3600 or age < -48 * 3600:
                return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

        # Time delta less than two days => make relative time
        if age < 0:
                age = -age
                prefix = "in "
        else:
                prefix = ""
        if age < bold_if_younger_than:
                age_class = "age recent"
        else:
                age_class = "age"
        return prefix + html.age_text(age)

def page_tip_circle_graph(h):
        global html
        html = h
        html_view = ""\
                "<div id=\"help_container\">"\
                "<h1>Network Map</h1>"\
                "<div><strong>Network Map</strong> On this Map.You can View Every Host Connectivity.How Host Are Connected With Each Other.When Click On Host You Can View Every Host Details</div>"\
                "<br/>"\
                "<div><strong><u>Host Details</u></strong>You can view the Host Detail like Host Name,Host Alias,IP Address,MAC Address,Device Type etc. and its alarm status</div>"\
                "</div>"
        html.write(str(html_view))
