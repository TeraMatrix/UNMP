#!/usr/bin/python2.6
##################################################################
#
# Author            :   Yogesh Kumar
# Project           :   UNMP
# Version           :   0.1
# File Name         :   example.py
# Creation Date     :   12-September-2011
# Modify Date       :   12-September-2011
# Purpose           :   Example View
# Require           :   Python 2.6 or Higher Version
# Require Library   :   htmllib.py
# Copyright (c) 2011 Codescape Consultant Private Limited
#
##################################################################

"""
This File Use To Show Example of Web UI and CSS which Help Developers to Make Good and User Friendly UI Interface [Author : Yogesh Kumar]. 
"""
# import the modules
import os.path,sys,htmllib,config,MySQLdb,time
from example_model import host
from lib import *
from mysql_collection import mysql_connection
from cgitb import html
from datetime import datetime
from inventory_bll import HostBll,NagioConfigurationBll
from common_bll import Essential
from logs_events_bll import LogsEventsBll
from unmp_config import SystemConfig
from nagios_bll import NagiosBll
# flag for nagios
# if set to 1 means call NagiosBll
# if set to 0 means call old nagios functions
flag_nagios_call = 0


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
        output_dict={'success':2,'output':str(msg)}
        html.write(str(output_dict))


def device_details_example(h):
    global html
    html = h
    css_list = []
    host_id=html.var('host_id')
    user_id =  html.req.session['user_id']   
    es = Essential()

    if es.is_host_allow(user_id,host_id) == 0 or host_id == '1':    # temporary solution for localhost view 
        javascript_list = ["js/device_details.js"]
        search_bar = '\
	    \
	    '
        html.new_header("Manage Device","manage_host.py","",css_list,javascript_list)
        #host_details = {"Last Boot Reason":"Normal","Total Interface":"3","SNMP Status":"Disable","SNMP Status2":"Disable","SNMP Status3":"Disable"}
        #html.write(host_bar(host_id,host_extra_bar(host_details)))
        html.write(host_bar(host_id))
        html.write(tabs2(host_id))
    else:
        html.new_header(" Warning : Page request not granted","","")
        html.write("<div class=\"warning\" > Access Restricted. Please request access from UNMP admin.  </div>")
    html.new_footer()


def view_service_details_example(h):
    global html
    html = h
    css_list = []
    host_id=html.var('host_id')
    user_id =  html.req.session['user_id']   
    es = Essential()

    if es.is_host_allow(user_id,host_id) == 0 or host_id == '1':    # temporary solution for localhost view 
        html.write(service_details_grid(host_id))


def is_service_busy(host_ip):

    return_value = 0
    try:
        query_service = "GET services\nColumns: service_next_check \nFilter: host_address = " + host_ip
        html.live.set_prepend_site(True)
        services = html.live.query(query_service)
        html.live.set_prepend_site(False)
        timestamp = services[0][1]
        dt = datetime.fromtimestamp(timestamp) - datetime.now()
        sec_value = dt.seconds
        if sec_value > 10:
            return_value = 0
        else:
            return_value = 1        
        return return_value

    except Exception,e:
        return str(e)

def host_details_grid(host_id):
    try:
        flag=0
        host_last_age=0
        host_next_age=0
        checked=0
        output=''
        # create the data base and cursor object.
        db,cursor=mysql_connection('nms_sample')
        # check the database conection created or not.
        if db ==1:
            raise SelfException(cursor)

        sql = "SELECT  hosts.host_name,hosts.ip_address,hosts.mac_address,host_states.state_name,device_type.device_name,hosts.host_alias,hosts.creation_time,hosts.timestamp,hosts.lock_status,hosts.priority_id,hosts.host_id,host1.ip_address as parent_name,device_type.device_type_id FROM hosts LEFT JOIN host_states ON hosts.host_state_id=host_states.host_state_id LEFT JOIN hosts as host1 ON host1.host_id = hosts.parent_name LEFT JOIN device_type ON hosts.device_type_id=device_type.device_type_id WHERE hosts.host_id='%s'" %  host_id
        # execute the query and fetch the result.
        cursor.execute(sql)
        host_result=cursor.fetchall()

        if host_result is not None:
            if len(host_result)>0:
                # get the host information from get_host_by_id function 
                host_obj=HostBll()
                host_detail_dict=host_obj.get_host_by_id(host_id)
                device_type_id_index=12
                device_type_id=host_result[0][device_type_id_index]


                query_service = "GET hosts\nColumns: host_plugin_output host_has_been_checked host_last_check host_next_check \nFilter: host_address = " + host_result[0][1]
                html.live.set_prepend_site(True)
                services = html.live.query(query_service)
                services.sort()
                html.live.set_prepend_site(False)
                for service_site,output,checked,last_check,next_check in services:
                    host_last_age=last_check
                    host_next_age=next_check
                    checked=checked
                    output=output
                flag=1
                state=str('--' if host_result[0][8]=="" or host_result[0][8]=="None" else host_result[0][8])
                if state=='f':
                    state='Unlocked'
                else:
                    state='Locked'
                # host group details 
                sql="SELECT hostgroups.hostgroup_alias FROM hostgroups INNER JOIN hosts_hostgroups ON hostgroups.hostgroup_id=hosts_hostgroups.hostgroup_id  WHERE hosts_hostgroups.host_id='%s'"%(' ' if host_result[0][10]=="" or host_result[0][10]==None else host_result[0][10])
                cursor.execute(sql)
                group_result=cursor.fetchall()
                group_results=[group_result[i][0] for i in range(len(group_result))]
                grid_str = '\
		<table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
		<colgroup><col width=\"15%%\"/><col width=\"35%%\"/><col width=\"15%%\"/><col width=\"35%%\"/></colgroup>\
		<tbody>\
		    <tr>\
			<th class="cell-title" colspan="4">\
			    Host Details\
			</th>\
		    </tr>\
		    <tr>\
			<td class="cell-label">\
			    Host Name\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
			<td class="cell-label">\
			    Host Alias\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
		    </tr>\
		    <tr>\
			<td class="cell-label">\
			    IP Address\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
			<td class="cell-label">\
			    Mac Address\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
		    </tr>\
		    <tr>\
			<td class="cell-label">\
			    Device Type\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
			<td class="cell-label">\
			    Priority\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
		    </tr>\
		    <tr>\
			<td class="cell-label">\
			    Status\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
			<td class="cell-label">\
			    State\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
		    </tr>\
		    <tr>\
			<td class="cell-label">\
			    Creation Time\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
			<td class="cell-label">\
			    Last Updation Time\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
		    </tr>\
		    <tr>\
			<td class="cell-label">\
			    Parent Name\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
			<td class="cell-label">\
			    Group Name\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
		    </tr>\
		    <tr>\
			<td class="cell-label">\
			    Output\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
			<td class="cell-label">\
			    Last Check / Next Check\
			</td>\
			<td class="cell-info">\
			    %s\
			</td>\
		    </tr>\
		    <tr>\
			<td class="cell-label">\
			    Comment\
			</td>\
			<td class="cell-info" colspan="3">\
			    %s\
			</td>\
		    </tr>\
		</tbody>\
		</table>'%(str('--' if host_result[0][0]=="" or host_result[0][0]==None else host_result[0][0]),\
                           str('--' if host_result[0][5]=="" or host_result[0][5]==None else host_result[0][5]),\
                           str('--' if host_result[0][1]=="" or host_result[0][1]==None else host_result[0][1]),\
                           str('--' if host_result[0][2]=="" or host_result[0][2]==None else host_result[0][2]),\
                           str('--' if host_result[0][4]=="" or host_result[0][4]==None else host_result[0][4]),\
                           str('--' if host_result[0][9]=="" or host_result[0][9]==None else host_result[0][9]),\
                           str('--' if host_result[0][3]=="" or host_result[0][3]==None else host_result[0][3]),\
                           str(state),\
                           str('--' if host_result[0][6]=="" or host_result[0][6]==None else (host_result[0][6]).strftime("%d %b %Y %I:%M %p")),\
                           str('--' if host_result[0][7]=="" or host_result[0][7]==None else (host_result[0][7]).strftime("%d %b %Y %I:%M %p")),\
                           str('--' if host_result[0][11]=="" or host_result[0][11]==None else host_result[0][11]),\
                           str('--' if len(group_result)==0 or group_result==None else ','.join(group_results)),\
                           str('--' if output=="" or output==None else output),\
                           str(str('0' if host_last_age==0 else paint_age(host_last_age, checked == 1, 60 * 10))+" / "+str('0' if host_next_age==0 else paint_future_time(host_next_age))),\
                           str('--' if host_detail_dict['host_comment']=="" or host_detail_dict['host_comment']=="" else host_detail_dict['host_comment']))
                # create the list for 
                if device_type_id=="ap25":
                    host_valus_list=['http_username','snmp_version','read_community','write_community','http_password','http_port','gateway','trap_port','serial_number','dns_state',\
                                     'get_set_port','longitude','latitude','netmask','host_os','host_vendor_name','primary_dns','secondary_dns','hardware_version']
                    host_name_list=['HTTP Username','SNMP Version','Read Community','Write Community','HTTP Port','Gateway','Trap Port','Serial Number','DNS State',\
                                    'Get Set Port','Longitude','Latitude','Netmask','Host OS','Host Vendor','Primary DNS','Secondary DNS','Hardware Version']
                else:
                    host_valus_list=['http_username','snmp_version','read_community','write_community','http_password','http_port','gateway','trap_port','serial_number','dns_state',\
                                     'get_set_port','longitude','latitude','netmask','host_os','host_vendor_name','hardware_version']
                    host_name_list=['HTTP Username','SNMP Version','Read Community','Write Community','HTTP Port','Gateway','Trap Port','Serial Number','DNS State',\
                                    'Get Set Port','Longitude','Latitude','Netmask','Host OS','Host Vendor','Hardware Version']


                details_str = '\
		<div id="more_details_div" style="display:none;">\
		<table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
		<colgroup><col width=\"15%%\"/><col width=\"35%%\"/><col width=\"15%%\"/><col width=\"35%%\"/></colgroup>\
		<tbody>\
		    <tr>\
			<th class="cell-title" colspan="4">\
			    Advanced Host Details\
			</th>\
		    </tr>'

                for i in range(len(host_valus_list)):
                    if i%2==1:
                        details_str+='\
				    <tr>\
					<td class="cell-label">\
					    %s\
					</td>\
					<td class="cell-info">\
					    %s\
					</td>\
					<td class="cell-label">\
					    %s\
					</td>\
					<td class="cell-info">\
					    %s\
					</td>\
				    </tr>'%(host_name_list[i-1],'--' if host_detail_dict[host_valus_list[i-1]]=='' or host_detail_dict[host_valus_list[i-1]]==None else host_detail_dict[host_valus_list[i-1]],host_name_list[i],'--' if host_detail_dict[host_valus_list[i]]=='' or host_detail_dict[host_valus_list[i]]==None else host_detail_dict[host_valus_list[i]])
                details_str+= '</tbody></table></div>'
                grid_str+=details_str
                grid_str+='<button type=\"submit\" class=\"yo-small yo-button\" id=\"host_more_detail_button\" style="float:right;margin-right:15px;"><span>More</span></button>'

        if flag==0:
            grid_str='No host exists'
        return grid_str
        # close the connection
        cursor.close()
        db.close()
    # Exception Handling
    except MySQLdb as e:
        output_dictt={'success':1,'output':str(e[-1])}
        html.write(str(output_dictt))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
    except Exception as e:
        output_dictt={'success':1,'output':str(e)}
        html.write(str(output_dictt))
        if db.open:
            cursor.close()
            db.close()
    finally:
        if db.open:
            cursor.close()
            db.close()

def log_details_grid(host_id):
    service_status_list = ["Ok","Warning","Critical","Unknown"]
    try:
        flag=0 
        host_alias = ""
        service = ""
        log_plugin_output = ""
        logtime_ = ">"
        logtime_sec = 0
        logtime_min = 0
        logtime_hours = 1
        logtime_days = 0
        time_stamp = int(time.time())
        logtime_sec += logtime_min *60
        logtime_sec += logtime_hours *3600
        logtime_sec += logtime_days *86400
        time_stamp -= logtime_sec

        # create the data base and cursor object.
        db,cursor=mysql_connection('nms_sample')
        # check the database conection created or not.
        if db ==1:
            raise SelfException(cursor)

        sql = "SELECT  hosts.host_name,hosts.host_alias FROM hosts WHERE hosts.host_id='%s'" %  host_id
        # execute the query and fetch the result.
        cursor.execute(sql)
        host_result=cursor.fetchall()
        cursor.close()
        db.close()
        grid_str='''<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">
			<colgroup>
			    <col style="width:30px;">
			    <col style="width:100px;">
			    <col style="width:150px;">
			    <col style="width:150px;">
			    <col style="width:auto;">
			<colgroup\>
			<tbody>
			<tr class="yo-table-head">
			    <th>State</th>
			    <th>Time</th>
			    <th>Service</th>
			    <th>Event Type</th>
			    <th>Log Plugin Output</th>
			</tr>'''

        if host_result is not None:
            if len(host_result)>0:
                # Live query using here.
                host_alias = host_result[0][1]
                query_events = "GET log\nColumns: state log_time log_type host_name service_description log_plugin_output\nFilter: host_name ~~ %s\nFilter: service_description ~~ %s\nFilter: log_plugin_output ~~ %s\nFilter: log_time %s %s" % (host_result[0][0],service,log_plugin_output,logtime_,time_stamp)
                html.live.set_prepend_site(True)
                query_events_data = html.live.query(query_events)
                html.live.set_prepend_site(False)

                for site,state,log_time,log_type,host_name,service_description,log_plugin_output in query_events_data:
                    flag=1
                    grid_str +='<tr>\
					      <td><img src=\"images/new/status-%s.png\" alt=\"%s\"/></td>\
					      <td>%s</td>\
					      <td>%s</td>\
					      <td>%s</td>\
					      <td>%s</td>\
					    </tr>'%(state,service_status_list[state],LogsEventsBll().convert_time(log_time)[1],service_description,log_type,log_plugin_output)

        if flag==0:
            grid_str +='<tr><td colspan=\"5\">No logs exists</td></tr>'
        grid_str +='</tbody>\
		</table>\
		<div class="status_legend">\
		    <span class="span-status-container span-extra-padding icon-0">Ok</span>\
		    <span class="span-status-container span-extra-padding icon-1">Warning</span>\
		    <span class="span-status-container span-extra-padding icon-2">Critical</span>\
		    <span class="span-status-container span-extra-padding icon-3">Unknown</span>\
		    <a href=\"manage_events.py?host=%s\" style=\"float:right;margin:5px;\">more logs >> </a>\
		</div>' % host_alias
        return grid_str
    # Exception Handling
    except MySQLdb as e:
        output_dictt={'success':1,'output':str(e[-1])}
        html.write(str(output_dictt))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
    except Exception as e:
        output_dictt={'success':1,'output':str(e)}
        html.write(str(output_dictt))
        if db.open:
            cursor.close()
            db.close()
    finally:
        if db.open:
            cursor.close()
            db.close()

def get_time_tick(timetick,flag=0):
    import datetime
    last_check=""
    if datetime.datetime.now()>datetime.datetime.fromtimestamp(timetick):
        delta=datetime.datetime.now()-datetime.datetime.fromtimestamp(timetick)
        if flag:
            return " Service check is in progress"
    else:
        delta=datetime.datetime.fromtimestamp(timetick)-datetime.datetime.now()
    second=delta.seconds
    if second<60:
        last_check=str(second)+" sec"
    elif second<3600:
        minute=int(second/60)
        second=second%60
        last_check=str(minute)+" min,"+str(second)+" sec"
    elif second<86400 and delta.days==0:
        hour=int(second/3600)
        minute=int((second-hour*3600)/60)
        last_check=str(hour)+" hour,"+str(minute)+" min"	    
    else:
        hour=int(second/3600)
        minute=int((second-hour*3600)/60)
        last_check=str(delta.days)+" days,"+str(hour)+" hour,"+str(minute)+" min"
    return last_check




def service_details_grid(host_id):
    try:
        result = "0"
        ok=0        # its count the no of state of particular host
        critical=0
        warning=0
        unknown=0    
        host_age=0 # store the host age.
        checked=0 # check the host checked
        flag=0 

        # create the data base and cursor object.
        db,cursor=mysql_connection('nmsp')
        # check the database conection created or not.
        if db ==1:
            raise SelfException(cursor)

        sql = "SELECT  hosts.ip_address,hosts.host_name FROM hosts WHERE hosts.host_id='%s'" %  host_id
        # execute the query and fetch the result.
        cursor.execute(sql)
        host_result=cursor.fetchall()
        cursor.close()
        db.close()
        grid_str='''<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">
			<colgroup>
			    <col style="width:17%">
			    <col style="width:4%;">
			    <col style="width:7%">
			    <col style="width:14%">
			    <col style="width:14%">
			    <col style="width:14%">
			    <col style="width:auto;">
			<colgroup\>
			<tbody>
			<tr class="yo-table-head">
			    <th class=" vertline">Service</th>
			    <th style=\"text-align:left;\">Action</th>
			    <th style=\"text-align:left\">Age</th>
			    <th style=\"text-align:left\">Time since last check of service</th>
			    <th style=\"text-align:left\">Time of next scheduled check</th>
			    <th style=\"text-align:left\">Service check duration(sec)</th>
			    <th style=\"text-align:left\">Output</th>
			</tr>'''

        if host_result is not None:
            if len(host_result)>0:
                # Live query using here. 
                query_service = "GET services\nColumns: state description service_last_state_change service_has_been_checked \
                service_plugin_output service_long_plugin_output  service_last_check service_next_check \
                service_execution_time \nFilter: host_address = " + host_result[0][0]
                html.live.set_prepend_site(True)
                services = html.live.query(query_service)
                services.sort()
                html.live.set_prepend_site(False)
                flag=1 
                for service_site,state,description, age, checked,output,all_output,last_check_time,next_check_time,execution_time in services:
                    if description == 'Alarm Service':
                        all_device_detail = '()'
                    else:
                        all_device_detail=' ('+str(all_output).replace('\\n','')+')'
                    host_age=age
                    checked=checked
                    grid_str +="<tr>\
					      <td style=\"text-align:left\" class=\"vertline\"><span class=\"span-status-container icon-%s\">%s</span></td>\
					      <td style=\"text-align:left;\"><a href=\"#\" onclick=\"performActionService(this, \'reschedule\', \'service\', \'\', \'%s\', \'%s\');\">\
					      <img class=icon title=\"Reschedule an immediate check of this\" src=\"images/icon_reload.gif\" style=\"height:20px;width:20px;\" /></a></td>\
					      <td style=\"text-align:left\">%s</td>\
					      <td style=\"text-align:left\">%s</td>\
					      <td style=\"text-align:left\">%s</td>\
					      <td style=\"text-align:left\">%s</td>\
					      <td style=\"text-align:left\">%s</td>\
					    </tr>"%(state,description,host_result[0][1],description,str('0' if host_age==0 else paint_age(host_age, checked == 1, 60 * 10)),get_time_tick(last_check_time),get_time_tick(next_check_time,1),execution_time,output+str('' if all_device_detail.strip()=='()' else all_device_detail))

        if flag==0:
            grid_str +='<tr><td colspan=\"3\">No services exists</td></tr>'
        grid_str +='</tbody>\
		</table>\
		<div class="status_legend">\
		    <span class="span-status-container span-extra-padding icon-0">Ok</span>\
		    <span class="span-status-container span-extra-padding icon-1">Warning</span>\
		    <span class="span-status-container span-extra-padding icon-2">Critical</span>\
		    <span class="span-status-container span-extra-padding icon-3">Unknown</span>\
		</div>'
        return grid_str
    # Exception Handling
    except MySQLdb as e:
        output_dictt={'success':1,'output':str(e[-1])}
        html.write(str(output_dictt))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
    except Exception as e:
        output_dictt={'success':1,'output':str(e)}
        html.write(str(output_dictt))
        if db.open:
            cursor.close()
            db.close()
    finally:
        if db.open:
            cursor.close()
            db.close()


def tabs():
    tab_str = ''
    tab_str += '\
    <div class="yo-tabs">\
        <ul>\
            <li>\
                <a class="active" href="#content_1">Host Details</a>\
            </li>\
            <li>\
                <a href="#content_2">Service Details</a>\
            </li>\
            <li>\
                <a href="#content_3">Group Details</a>\
            </li>\
        </ul>\
        <div id="content_1" class="tab-content">\
            <p>Host Details</p>\
        </div>\
        <div id="content_2" class="tab-content">\
            <p>Service Details</p>\
        </div>\
        <div id="content_3" class="tab-content">\
            <p>Dashboard</p>\
        </div>\
    </div>'
    return tab_str

def tabs2(host_id):
    tab_str = ''
    tab_str += '\
    <div class="yo-tabs">\
        <ul>\
            <li><a class="active" href="#content_1">Host Details</a></li><li><a href="#content_2">Service Details</a></li><li><a href="#content_3">Logs</a></li>\
        </ul>\
        <div id="content_1" class="tab-content">\
            %s\
        </div>\
        <div id="content_2" class="tab-content" style="display:none;">\
            %s\
        </div>\
        <div id="content_3" class="tab-content" style="display:none;">\
            %s\
        </div>\
    </div>' % (host_details_grid(host_id),service_details_grid(host_id),log_details_grid(host_id))
    return tab_str



def host_bar(host_id):

    # status dictionary
    host_status_name = {"0":"Up","1":"Down","2":"Down","3":"Down"}  
    # fetch all the info and details through host_id.
    #host_name="ap104"
    #host_alias = "Rajendra Point [CCPL-1]"
    #ip_address = "172.22.0.101"
    #ac_address = "11:22:33:44:55:77"
    #device_type = "Access Point"
    #device_icon = "linux.png"
    #host_status = "0"
    #age = "4 hrs"

    # status dictionary
    # fetch all the info and details through host_id.
    host_name="--"
    host_alias = "--"
    ip_address = "--"
    mac_address = "--"
    device_type = "--"
    device_icon = "linux.png"
    host_status = "3"
    age = "--"


    result = "0"
    ok=0        # its count the no of state of particular host
    total=0
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

        sql = "SELECT  hosts.host_name,hosts.ip_address,hosts.mac_address,hosts.host_state_id,hosts.device_type_id,hosts.host_alias,hosts.creation_time,hosts.timestamp,hosts.lock_status FROM hosts LEFT JOIN host_states ON hosts.host_state_id=host_states.host_state_id WHERE hosts.host_id='%s'" %  host_id
        # execute the query and fetch the result.
        cursor.execute(sql)
        host_result=cursor.fetchall()
        cursor.close()
        db.close()
        # close the cursor and database connection.

        if host_result is not None:
            if len(host_result)>0:
                # Live query using here.
                query_service = "GET services\nColumns: state description  host_last_state_change host_has_been_checked \nFilter: host_address = " + host_result[0][1]
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
                total=ok+warning+critical+unknown
                host_name=str(host_result[0][0])
                host_alias =str(host_result[0][5])
                ip_address = host_result[0][1]
                mac_address = host_result[0][2]
                #device_type = host_result[0][4]
                #device_icon ="linux.png"
                host_status = "0"
                age = str('0' if host_age==0 else paint_age(host_age, checked == 1, 60 * 10))

                # Live query using here for host state
                query_service = "GET hosts\nColumns: state  \nFilter: host_address = " + host_result[0][1]
                html.live.set_prepend_site(True)
                services = html.live.query(query_service)
                services.sort()
                html.live.set_prepend_site(False)
                for service_site,state in services:
                    host_status=str(state)

#        main_extra_bar = 
#        <div id="extra_host_bar" class=\"host_bar\" style="display:none;">\
#            <div class="device_info device_info2">\
#                <p class="text"><strong>Priority</strong></p>\
#                <p class="text">Normal</p>\
#                <p class="text"><strong>Last Update</strong></p>\
#                <p class="text">30-Sept-2011 1:45 PM</p>\
#            </div>\
#            <div class="device_info device_info2">\
#                <p class="text"><strong>Hardware Version</strong></p>\
#                <p class="text">Rev0.4</p>\
#                <p class="text"><strong>Software Version</strong></p>\
#                <p class="text">5.2.0801v</p>\
#            </div>\
#            <div class="device_info device_info2">\
#                <p class="text"><strong>Mac Address</strong></p>\
#                <p class="text">11:22:33:44</p>\
#                <p class="text"><strong>Device Type</strong></p>\
#                <p class="text">AP25</p>\
#            </div>\
#            %s\
#        </div>' % (extra_bar)


        bar = '<div id="host_bar" class=\"host_bar\">\
            <div id="device_icon">\
                <img src="images/devices/%(device_icon)s" alt="%(device_type)s" />\
            </div>\
            <div class="device_info">\
                <p class="head">%(host_alias)s</p>\
                <p class="text">%(ip_address)s</p>\
                <p class="space"></p>\
                <span class="span-status-container icon-%(host_status)s" style="margin-left:5px;"><strong>%(host_status_name)s</strong> (%(age)s)</span>\
            </div>\
            <div id="host_bar_side_button" class="host_bar_side_button" style="display:none;"></div>\
            <div class="device_info" style=\"border-left:0px none;\">\
                <p class="head"><strong>&nbsp;</strong></p>\
                <p class="text">Total Services: %(total)s</p>\
                <p class="text" style="height:auto;">\
                    <a href="#" class="service-bar">\
                        <span class="s-bar s-0"><span class="text">%(ok)s</span><span class="ss"></span></span>\
                        <span class="s-bar s-1"><span class="text">%(warning)s</span><span class="ss"></span></span>\
                        <span class="s-bar s-2"><span class="text">%(critical)s</span><span class="ss"></span></span>\
                        <span class="s-bar s-3"><span class="text">%(unknown)s</span><span class="ss"></span></span>\
                    </a>\
                </p>\
            </div>\
        </div>' % {"device_icon":device_icon,"device_type":device_type,"host_alias":host_alias,"ip_address":ip_address,"host_status":host_status,"host_status_name":host_status_name[host_status],"age":age,"total":total,"ok":ok,"warning":warning,"critical":critical,"unknown":unknown}

#            <div class=\"bar-btn-div\">\
#                <a class=\"ft active n-tip-image\" href=\"#" title=\"Home\"><span class=\"host-hm\"></span></a><a class=\"n-tip-image\" href=\"#" title=\"Services\"><span class=\"host-sr\"></span></a><a class=\"n-tip-image\" href=\"#" title=\"Dashboard\"><span class=\"host-db\"></span></a><a class=\"n-tip-image\" href=\"#" title=\"Configuration\"><span  class=\"host-cn\"></span></a><a class=\"n-tip-image\" href=\"#" title=\"Edit\"><span  class=\"host-edt\"></span></a><a class=\"n-tip-image\" href=\"#" title=\"Delete\"><span  class=\"host-del\"></span></a><a class=\"n-tip-image\" href=\"#" title=\"Alerts\"><span  class=\"host-al\"></span></a><a class=\"lt n-tip-image\" href=\"#" title=\"Refresh\"><span  class=\"host-rf\"></span></a>\
#            </div>\

        #bar += main_extra_bar
        return bar
    # Exception Handling
    except MySQLdb as e:
        output_dictt={'success':1,'output':str(e[-1])}
        html.write(str(output_dictt))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
    except Exception as e:
        output_dictt={'success':1,'output':str(e)}
        html.write(str(output_dictt))
        if db.open:
            cursor.close()
            db.close()
    finally:
        if db.open:
            cursor.close()
            db.close()

def host_full_details(hs):
    return "\
    <table class=\"yo-table\">\
        <tr>\
            <td>\
            \
            </td>\
        </tr>\
    </table>"

def host_extra_bar(host_details_dic={}):
    extra_bar = ''
    total_dic_item = 0
    bar = ''
    for dic in host_details_dic:
        total_dic_item += 1
        bar += '<p class="text"><strong>%s</strong></p><p class="text">%s</p>' % (dic,host_details_dic[dic])
        if total_dic_item % 2 == 0:
            extra_bar += '<div class="device_info device_info2">' + bar + '</div>'
            bar = ''
    if total_dic_item % 2 != 0:
        bar += '<p class="text"><strong>&nbsp;</strong></p><p class="text">&nbsp;</p>'
        extra_bar += '<div class="device_info device_info2">' + bar + '</div>'
    return extra_bar


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


def paint_future_time(timestamp):
    if timestamp <= 0:
        return "", "-"
    else:
        return paint_age(timestamp, True, 0)

def page_tip_device_detail(h):
    global html
    html = h
    html_view = ""\
        "<div id=\"help_container\">"\
        "<h1>Manage Device</h1>"\
        "<div><strong>Manage Device</strong> On this Page.You can View the Host Details and Service Details.</div>"\
        "<br/>"\
        "<div><strong><u>Host Details</u></strong>You can view the Host Detail like Host Name,Host Alias,IP Address,MAC Address,Device Type etc.</div>"\
        "<div><strong><u>Service Details</u></strong> You can View the service details like Services Name,Service Age and Service Output.</div>"\
        "</div>"
    html.write(str(html_view))




################################################ new functions #########################################
def get_hostgroup_hosts(user_id,hostgroup_id_list):
    try:
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = conn.cursor()
        query="select hg.hostgroup_id,hg.hostgroup_name,h.host_id,h.host_alias,h.ip_address,h.priority_id,ifnull(h_s.normal_check_interval,'-'),h_s.service_description,h.is_localhost from hostgroups as hg \
			left join (select hostgroup_id,host_id from hosts_hostgroups)  as hhg on hhg.hostgroup_id=hg.hostgroup_id \
			left join (select host_id,device_type_id,ip_address,host_alias,priority_id,is_deleted,host_state_id,is_localhost from hosts) as h on h.host_id=hhg.host_id \
			left join (select normal_check_interval,host_id,service_description from host_services) as h_s on h_s.host_id=h.host_id \
			left join (select device_type_id,device_name,is_deleted from device_type) as dt on dt.device_type_id=h.device_type_id \
			where hhg.hostgroup_id IN (%s) and dt.is_deleted<>1 and h.is_deleted=0 and h.host_state_id='e' order by hg.hostgroup_name,h.host_alias,h_s.service_description desc"%','.join(hostgroup_id_list)

        cursor.execute(query)
        result = cursor.fetchall()
        query2="select hg.hostgroup_id,hg.hostgroup_name from hostgroups as hg where hg.hostgroup_id IN (%s)"%','.join(hostgroup_id_list)
        cursor.execute(query2)
        result2 = cursor.fetchall()
        conn.close()
        result_li = []
        make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
        di={}
        #for row in result:
        # 	result_li.append(make_list(row))
        for row in result:
            if di.has_key(row[0]):
                li = di[row[0]]
                l=row[2:]#[row[2],row[3],row[4],row[5],row[6],row[7],row[8]]
                li.append(l)
                di[row[0]] = li
            else:
                l=make_list(row)
                li=l[0:2]+[l[2:]]
                di[row[0]]=li
        for row in result2:
            if di.has_key(row[0]):
                pass
            else:
                l=make_list(row)
                di[row[0]]=l

        result_dict={}
        result_dict["success"]=0
        result_dict["result"]=di
        return result_dict
    except Exception,e:
        result_dict={}
        result_dict["success"]=1
        result_dict["result"]=str(e)
        return result_dict



def make_service_box(hostgroup_id,hosts_li):#,host_id,host_alias,host_ip,priority,normal_check_interval):
    try:
        priority_dict={'high':'H', 'low':'L', 'normal' : 'N'}
        host_id=hosts_li[0][0]
        host_alias=hosts_li[0][2]
        host_ip=hosts_li[0][3]
        priority=hosts_li[0][4]
        is_localhost=hosts_li[0][7]
        #if host_alias=="UNMP Server System":
        #    return ""
        #query_service = "GET hosts\nColumns: state  \nFilter: host_address = " + host_ip
        query_service = "GET services\nColumns: service_state \nFilter: host_address = " + host_ip
        html.live.set_prepend_site(True)
        services_state = html.live.query(query_service)
        html.live.set_prepend_site(False)
        host_status=str(services_state[0][1])

        html_str='<div class="service-box shoulddraggable" id="%s" parent_id="%s"><img style="z-index:3;float:left;height:15px;width:15px;vertical-align:middle;margin-top:3px;" src="images/new/status-%s.png"/> \
        <a href="#" onclick="viewHostDetails(%s)"><span style="padding:5px;float:left;">%s (%s)</span></a>'%(host_id,"hostgroup"+hostgroup_id,host_status,host_id,host_alias,priority_dict[priority])
        if is_localhost!=1:
            for i in hosts_li:
                normal_check_interval=i[5]
                service_name=i[6].replace(' ','_')
                if str(normal_check_interval)=="518400":
                    normal_check_interval="Y"
                elif str(normal_check_interval)=="43200":
                    normal_check_interval="M"
                elif str(normal_check_interval)=="1440":
                    normal_check_interval="D"
                if service_name.lower().find("uptime")!=-1:
                    html_str+='<div id=\"service_box_%s_uptime\" class=\"service-boxwhite\" style=\"height:12px;float:right;padding:2px 5px 5px 5px;\" >%s</div>'%(host_id,normal_check_interval)
                else:
                    html_str+='<div id=\"service_box_%s_statistics\" class=\"service-boxwhite\" style=\"height:12px;float:right;padding:2px 5px 5px 5px;\" >%s</div>'%(host_id,normal_check_interval)
        html_str+='</div>'
        return {'result':html_str,'success':0}
    except Exception,e:
        if str(e).find('Cannot connect to')!=-1:
            return {'result':'Please start Nagios to continue.','success':1}
        else:
            return {'result':str(e),'success':1}



def nagios_hostgroup(h):
    global html
    html = h
    css_list = ["css/jquery-ui-1.8.21.custom.css","css/jquery.multiselect.css","css/jquery.multiselect.filter.css"]
    js_list = ["js/jquery-ui-1.8.21.custom.min.js","jquery-1.6.1.min.js","js/pages/jquery.multiselect.min.js","js/pages/jquery.multiselect.filter.js","js/pages/nagios_hostgroups.js"]#,
    try:
        user_id =  html.req.session['user_id']   
        es = Essential()
        hostgroup_id_list = es.get_hostgroup_ids(user_id)
        html.new_header("Service Management","nagios_hostgroup.py","",css_list,js_list)
        result=get_hostgroup_hosts(user_id,hostgroup_id_list)
        html_str='<div class="form-div">'
        if result['success']==0:
            data_dict=result['result']
            for data in data_dict.keys():
                html_str+='<div id="hostgroup%s" class="shortcut-icon-div hostgroup_class" style="position:relative;padding: 8px;margin: 16px 16px 0 16px;\
		float:left;width:200px;min-height:100px;height:auto;text-align:center">\
		<span style="font-size:12px;text-transform:capitalize;">%s</span>\
		<a href="javascript:edit_hostgroup_service(\'%s\',\'%s\');" style="float:right"><img class="host_opr" title="Edit Host Details" src="images/new/edit.png" alt="edit"/></a>\
		'%(data_dict[data][0],data_dict[data][1],data_dict[data][0],data_dict[data][1].capitalize())

                if len(data_dict[data])>2:
                    di_hosts={}
                    for hosts in data_dict[data][2:]:
                        if di_hosts.has_key(str(hosts[0])):
                            l=di_hosts[str(hosts[0])]
                            l.append([hosts[0],data_dict[data][0],hosts[1],hosts[2],hosts[3],hosts[4],hosts[5],hosts[6]])
                            di_hosts[str(hosts[0])]=l
                        else:
                            di_hosts[str(hosts[0])]=[[hosts[0],data_dict[data][0],hosts[1],hosts[2],hosts[3],hosts[4],hosts[5],hosts[6]]]
                    #f=open("/home/cscape/Desktop/acb.txt","a")
                    #f.write(str(di_hosts))
                    #f.close()
                    for hst in di_hosts:
                        temp_html_dict = make_service_box(data_dict[data][0],di_hosts[str(hst)])
                        if(temp_html_dict['success']==1):
                            html_str+=temp_html_dict['result']
                        else:
                            html_str+=temp_html_dict['result']

                html_str+='</div>'
        else:
            html_str=result['result']
        html.write(html_str)
        html.write('</div><div class="form-div-footer">\
             <div class="user-header-icon">\
               <button class="yo-small yo-button" id="apply_changes_services_button" type="button" onclick="apply_hostgroup_changes();">Apply Changes</button>\
              </div>\
            </div>')
        html.new_footer()
    except Exception,e:
        if str(e).find('Cannot connect to')!=-1:
            html.write('Please start Nagios to continue.')    
        else:
            html.write(str(e))	





def nagios_host_details(h):
    global html
    html = h
    try:
        host_id=html.var("host_id")
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = conn.cursor()
        query="select hosts.host_alias,hosts.ip_address,hosts.host_name,ifnull(hosts2.host_alias,'N/A'),device_type.device_name as parent from hosts \
left join hosts as hosts2 on hosts2.host_id=hosts.parent_name join device_type on device_type.device_type_id=hosts.device_type_id where hosts.host_id='%s'"%(host_id)
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        host_alias=result[0][0]
        ip_address=result[0][1]
        host_name=result[0][2]
        parent=result[0][3]
        device_type=result[0][4]
        html_str='<table width="100%%" border="0" cellpadding="0" cellspacing="0" class="yo-table">\
			<colgroup>\
			    <col style="width:17%%">\
			    <col style="width:4%%">\
			    <col style="width:7%%">\
			    <col style="width:14%%">\
			    <col style="width:14%%">\
			    <col style="width:14%%">\
			    <col style="width:auto;">\
			<colgroup\>\
			<tbody>\
			<tr>\
			<th class="cell-title" colspan="7">\
			<span style=\"margin-left:30%%;float:left\">%s (%s)</span>\
			<span style=\"margin-left:3%%;float:left\">Parent : %s</span>\
			<span style=\"margin-left:3%%;float:left\">Device Type : %s</span>\
			</th>\
			</tr>\
			<tr class="yo-table-head">\
			    <th class=" vertline">Service</th>\
			    <th style=\"text-align:left;\">Action</th>\
			    <th style=\"text-align:left\">Age</th>\
			    <th style=\"text-align:left\">Time since last check of service</th>\
			    <th style=\"text-align:left\">Time of next scheduled check</th>\
			    <th style=\"text-align:left\">Service check duration(sec)</th>\
			    <th style=\"text-align:left\">Output</th>\
			</tr>'%(host_alias,ip_address,parent,device_type)
                # Live query using here. 
        query_service = "GET services\nColumns: state description service_last_state_change service_has_been_checked service_plugin_output service_long_plugin_output  service_last_check service_next_check service_execution_time \nFilter: host_address = " + ip_address
        html.live.set_prepend_site(True)
        services = html.live.query(query_service)
        services.sort()
        html.live.set_prepend_site(False)
        flag=1 
        for service_site,state,description, age, checked,output,all_output,last_check_time,next_check_time,execution_time in services:
            all_device_detail=' ('+str(all_output).replace('\\n','')+')'
            host_age=age
            checked=checked
            html_str +="<tr>\
					      <td style=\"text-align:left\" class=\"vertline\"><span class=\"span-status-container icon-%s\">%s</span></td>\
					      <td style=\"text-align:left;\"><a href=\"#\" onclick=\"performActionService(this, \'reschedule\', \'service\', \'\', \'%s\', \'%s\');\">\
					      <img class=icon title=\"Reschedule an immediate check of this\" src=\"images/icon_reload.gif\" style=\"height:20px;width:20px;\"/></a></td>\
					      <td style=\"text-align:left\">%s</td>\
					      <td style=\"text-align:left\">%s</td>\
					      <td style=\"text-align:left\">%s</td>\
					      <td style=\"text-align:left\">%s</td>\
					      <td style=\"text-align:left\">%s</td>\
					    </tr>"%(state,description,host_name,description,str('0' if host_age==0 else paint_age(host_age, checked == 1, 60 * 10)),get_time_tick(last_check_time),get_time_tick(next_check_time,1),execution_time,output+str('' if all_device_detail.strip()=='()' else all_device_detail))

        if flag==0:
            html_str +='<tr><td colspan=\"3\">No services exists</td></tr>'
        html_str +='</tbody>\
		</table>\
		<div class="status_legend">\
		    <span class="span-status-container span-extra-padding icon-0">Ok</span>\
		    <span class="span-status-container span-extra-padding icon-1">Warning</span>\
		    <span class="span-status-container span-extra-padding icon-2">Critical</span>\
		    <span class="span-status-container span-extra-padding icon-3">Unknown</span>\
		</div>'
        html.write(html_str)
    except Exception,e:
        html.write(str(e))


def edit_hostgroup_service_details(h): 
    global html
    html = h
    hostgroup_id=html.var("hostgroup_id")
    child_hosts=html.var("child_hosts")
    hostgroup_alias=html.var("hostgroup_alias")
    try:
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = conn.cursor()
        query="select host_alias,host_id from hosts where host_id in (%s) and is_localhost=0 "%(child_hosts if child_hosts!="" else '" "')
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        html_view='<div style="display:block;overflow:hidden"><h2>%s</h2>\
        	<div class=\"row-elem\">\
		   	<label class=\"lbl lbl-big\" style="width:100px;" >SNMP Uptime (Heartbeat Rate):</label>\
		   	<select name="snmp_uptime_service_time" id="snmp_uptime_service_time" class="multiselect" title="Click to select an option">\
			<option value=1>1 mins</option>\
			<option value=5>5 mins</option>\
			<option value=10>10 mins</option>\
			<option value=15>15 mins</option>\
			<option value=30>30 mins</option>\
			<option value=45>45 mins</option>\
			<option value=60>60 mins</option>\
			<option value=720>12 Hours</option>\
			<option value=1440>Daily</option>\
			<option value=43200>Monthly</option>\
			<option value=518400>Yearly</option>\
			</select>\
		</div>'\
            '<div class=\"row-elem\">\
	   		<label class=\"lbl lbl-big\" style="width:100px;" >Select hosts:</label>\
	   		<select name="snmp_uptime_hosts_list" id="snmp_uptime_hosts_list" class="multiselect" multiple="multiple">'%hostgroup_alias.capitalize()
        for row in result:
            html_view+='<option value=%s>%s</option>'%(row[1],row[0])
        html_view+='\
		</select>\
		</div>\
		<div class=\"row-elem\">\
		   	<label class=\"lbl lbl-big\" style="width:100px;" >Statistics service check time:</label>\
		   	<select name="statistics_service_time" id="statistics_service_time" class="multiselect" title="Click to select an option">\
			<option value=5>5 mins</option>\
			<option value=10>10 mins</option>\
			<option value=15>15 mins</option>\
			<option value=30>30 mins</option>\
			<option value=45>45 mins</option>\
			<option value=60>60 mins</option>\
			<option value=720>12 Hours</option>\
			<option value=1440>Daily</option>\
			<option value=43200>Monthly</option>\
			<option value=518400>Yearly</option>\
			</select>\
		</div>'\
            '<div class=\"row-elem\">\
	   		<label class=\"lbl lbl-big\" style="width:100px;" >Select hosts:</label>\
	   		<select name="statistics_service_hosts_list" id="statistics_service_hosts_list" class="multiselect" multiple="multiple">'
        for row in result:
            html_view+='<option value=%s>%s</option>'%(row[1],row[0])
        html_view+='\
		</select>\
		</div>\
		<button class=\"yo-small yo-button\" id=\"apply_changes_host_services\" type=\"button\">Apply Changes</button>'
        html.write(html_view)
    except Exception,e:
        html.write(str(e))


def apply_nagios_hostgroup_changes(h):
    global html
    html = h
    hostgroup_id=html.var("hostgroup_id")
    hosts_snmp_uptime_array=html.var("hosts_snmp_uptime_array")
    selected_snmp_uptime_time=html.var("selected_snmp_uptime_time")
    hosts_service_hosts_array=html.var("hosts_service_hosts_array")
    selected_service_hosts_time=html.var("selected_service_hosts_time")
    try:
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = conn.cursor()
        if hosts_service_hosts_array!=None:
            query="update host_services set normal_check_interval='%s' where service_description like 'Statictics Service%%' and host_id in ('%s') "%(selected_service_hosts_time, "','".join(hosts_service_hosts_array.split(',')))
            cursor.execute(query)
        if hosts_snmp_uptime_array!=None:
            query="update host_services set normal_check_interval='%s' where service_description like 'SNMP UPTIME%%' and host_id in ('%s') "%(selected_snmp_uptime_time, "','".join(hosts_snmp_uptime_array.split(',')))
            cursor.execute(query)
        conn.commit()
        conn.close()
        #nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        #nagios_config_obj=NagioConfigurationBll()
        #nagios_config_obj.write_nagios_config(nms_instance)
        if(flag_nagios_call==0):
            nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
            nagios_config_obj=NagioConfigurationBll()
            nagios_config_obj.write_nagios_config(nms_instance)

        else:
            n_bll= NagiosBll()
            wnc = n_bll.reload_nagios_service_times()

        html.write(str({"success":0, "result":""}))
    except Exception,e:
        html.write(str({"success":1, "result":str(e)}))


def apply_hostgroup_host_changes(h):
    global html
    html = h
    hostgroup_json=eval(html.var("hostgroup_json"))
    try:
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = conn.cursor()
        for key in hostgroup_json:
            query="update hosts_hostgroups set hostgroup_id='%s' where host_id in ('%s') "%(key[9:],"','".join(hostgroup_json[key]))
            cursor.execute(query)
            conn.commit()
        conn.close()

        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        #nagios_config_obj=NagioConfigurationBll()
        #nagios_config_obj.write_nagios_config(nms_instance)
        if(flag_nagios_call==0):
            nagios_config_obj=NagioConfigurationBll()
            nagios_config_obj.write_nagios_config(nms_instance)	
        else:    
            n_bll= NagiosBll()
            wnc = n_bll.reload_nagios_hostgroup()

        html.write(str({"success":0, "result":""}))
    except Exception,e:
        html.write(str({"success":1, "result":str(e)}))

def help_nagios_hostgroup(h):
    global html
    html = h
    html_view = ""\
        "<div id=\"help_container\">"\
        "<h1> Hostgroup Service Management</h1>"\
        "<div> Drag & Drop hosts from one hostgroup to another to change the hostgroups of hosts.</div>"\
        "<div> Also you can manage services of hosts.</div>"\
        "<div> Click on Edit to modify the service time in the interval of 5, 10, 15, 30 and 60 minutes.</div>"\
        "<div> After making all modifications click on Apply changes to save them.</div>"\
        "<br/>"\
        "<div><strong>Actions</strong></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\"><img style=\"height=\"15\" width=\"15\" \" src=\"images/new/status-0.png\"/></div><div class=\"txt-div\"> Host is in 'ok' state</div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\"><img style=\"height=\"15\" width=\"15\" \" src=\"images/new/status-1.png\"/></div><div class=\"txt-div\"> Host is in 'warning' state</div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\"><img style=\"height=\"15\" width=\"15\" \" src=\"images/new/status-2.png\"/></div><div class=\"txt-div\"> Host is in 'critical' state</div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\"><img style=\"height=\"15\" width=\"15\" \" src=\"images/new/status-3.png\"/></div><div class=\"txt-div\"> Host is in 'unknown' state</div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\" style=\"color:blue\">(H)</div><div class=\"txt-div\">  denotes Priority of host is High.</div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\" style=\"color:blue\">(N)</div><div class=\"txt-div\">  denotes Priority of host is Normal.</div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\" style=\"color:blue\">(L)</div><div class=\"txt-div\">  denotes Priority of host is Low.</div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\"><img style=\"height=\"15\" width=\"15\" \" src=\"images/new/edit.png\"/></div><div class=\"txt-div\"> Edit hostgroup service time</div></div>"\
        "<div class=\"action-tip\"><button class=\"yo-small yo-button\" disabled=\"disabled\" type=\"button\" >Apply Changes</button> Apply all modifications of hostgroups to the system.</div>"\
        "</div>"
    html.write(str(html_view))