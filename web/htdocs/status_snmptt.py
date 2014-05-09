#/usr/bin/python2.6

######################################################################################	 
# Author			:	Rajendra Sharma
# Project			:	UNMP
# Version			:	0.1
# File Name			:	Trap_inforamtion.py
# Creation Date			:	13-September-2011
# Purpose			:	This file display the Trap information for all devices.
# Copyright (c) 2011 Codescape Consultant Private Limited 

#######################################################################################

# success 0 means No error
# success 1  Exception or Error
# success 2 means some mysql error(services not running,connection not created)


## import module 
import MySQLdb,calendar
import htmllib
from datetime import datetime
from datetime import timedelta
from mysql_exception import mysql_connection
from common_bll import Essential
from json import JSONEncoder 
from error_message import ErrorMessageClass
from unmp_config import SystemConfig

global err_obj 
err_obj=ErrorMessageClass()

device_type_dict={'ap25':'AP25','odu16':'RM18','odu100':'RM','idu4':'IDU'}

#Exception class for own exception handling.
class SelfException(Exception):
	'''
	@author                        : Rajendra Sharma
	@requires                : required text message for display.
	@return: this class return the exception msg.
	@rtype: dictionary
	@note                        : This class used for message display to user.
	@version: 0.1
	@date: 18 sept 2011
	@organisation: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	'''
	def __init__(self,msg):
		output_dict={'success':2,'output':str(msg)}
		html.write(str(output_dict))


def start_page(h):
	'''
	@author: Rajendra Sharma
	@return: this function display the html page for trap information.
	@rtype: return type html page.
	@requires: Its take html object as a argument.
	@var css_list: This is array of all css file used in it.
	@var js_list: This is array of all js file used in it.
	@var ip_address: This is store the ip address from h(html) object.
	@var now: This is store current datetime.
	@since: 20 sept 2011
	@version: 0.1
	@note: this function display the trap information page on browser.
	@organisation: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	'''
	global html
	html=h
	ip_address=html.var("ip_address")
	user_id =  html.req.session['user_id']
	agent_id=html.var("agent_id")
	hostgroup_id_list = []
	es = Essential()
	flag_value = 0
	hostgroup_id_list = es.get_hostgroup_ids(user_id)
	if len(hostgroup_id_list) < 1:
		flag_value = 1
	if flag_value == 0:
	#"css/demo_table_jui.css
		css_list = ["css/demo_table_jui.css","css/custom.css","css/style12.css","css/jquery-ui-1.8.4.custom.css",'css/ccpl_jquery_combobox.css',"facebox/facebox.css","css/calendrical.css"]
		js_list = ["js/jquery-ui-1.8.6.custom.min.js","js/jquery.dataTables.min.js","js/ccpl_utility.js","js/calendrical.js","facebox/facebox.js","js/snmptt_status1.js",'js/ccpl_jquery_autocomplete.js']
		h.new_header("Events Details","status_snmptt.py","",css_list,js_list)
		
		end_date=datetime.date(datetime.now()).strftime("%d/%m/%Y")
		start_date=datetime.date(datetime.now()+timedelta(days=-30)).strftime("%d/%m/%Y")
		html.write("<div id=\"top_image_div\">")
		html.write("<table class=\"addform\" style=\"border:0px None;height:43px;border-bottom:1px solid #AAA;\"><tr class=\"odd\">")

		html.write("<td style=\"font-weight: bold;width:70px;\">Alarm Type")
		html.write("</td>")

		html.write("<td style=\"width:20px;\">")
		html.write("<input type=\"radio\" value=\"1\" name=\"option\" id=\"option1\" checked=\"checked\" class=\"table_option\"/>")
		html.write("</td>")

		html.write("<td style=\"width:45px;\">")
		html.write("<label for=\"option1\">Current</label>")
		html.write("</td>")

		html.write("<td style=\"width:20px;\">")
		html.write("<input type=\"radio\" value=\"2\" name=\"option\" id=\"option2\" class=\"table_option\"/>")
		html.write("</td>")

		html.write("<td style=\"width:40px;\">")
		html.write("<label for=\"option2\">Clear</label>")
		html.write("</td>")

		html.write("<td style=\"width:20px;\">")
		html.write("<input type=\"radio\" value=\"3\" name=\"option\" id=\"option3\" class=\"table_option\"/>")
		html.write("</td>")

		html.write("<td style=\"width:45px;\">")
		html.write("<label for=\"option3\">History</label>")
		html.write("</td>")

		html.write("<td style=\"width:auto;text-align:right;margin-right:10px;\">")
		html.write("<input class=\"yo-button yo-small\" type=\"button\" value=\"Advanced Search\" id=\"btn_filter\" name=\"btn_filter\"/>")
		html.write("</td>")
		html.write("</tr></table>")
		html.write("</div>")

		html.write("<div id=\"main_div\" class='form-div' style='margin-top:44px;margin-bottom:27px;'>")
		trap_status=html.var('trap_status')
		html_form='<form id=\"alarm_info_form\" action=\"alarm_current_detail.py\" method=\"get\" style="padding:0;" >\
			    <div>\
				<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
				    <tr>\
				        <th id=\"form_title\" class=\"cell-title\">Events Search</th>\
				    </tr>\
				</table>\
				<input type=\"hidden\" value=\"%s\"  id=\"trap_status_id\"/>\
				<div class=\"row-elem\">\
				    <label class=\"lbl lbl-big\" for=\"agentId\">IP Address</label>\
				    <input type=\"text\" id=\"agentId\" name=\"agent_id\" value=\"%s\"/>\
				</div>\
				<div class=\"row-elem\">\
				    <label class=\"lbl lbl-big\" for=\"eventType\">Event Type</label>\
				    <input type=\"text\" id=\"eventType\" name=\"eventType\"/>\
				</div>\
				<div class=\"row-elem\">\
				    <label class=\"lbl lbl-big\" for=\"M_obj\">Manage Object ID</label>\
				    <input type=\"text\" id=\"M_obj\" name=\"M_obj\"/>\
				</div>\
				<div class=\"row-elem\">\
				    <label class=\"lbl lbl-big\" for=\"M_name\">Manage Object Name</label>\
				    <input type=\"text\" id=\"M_name\" name=\"M_name\"/>\
				</div>\
				<div class=\"row-elem\">\
				    <label class=\"lbl lbl-big\" for=\"camponent_id\">Component ID</label>\
				    <input type=\"text\" id=\"camponent_id\" name=\"camponent_id\"/>\
				</div>\
				<div class=\"row-elem\">\
				    <label class=\"lbl lbl-big\" for=\"start_date\">Date</label>\
				    <input type=\"text\" name=\"event_start_date\" value=\"%s\" id=\"event_start_date\" style=\"width:70px;\"/>\
				    <input type=\"hidden\" name=\"odu_start_time\" value=\"%s\" id=\"odu_end_time\" style=\"width:80px;\"/>\
				    <lable>--</lable>\
				    <input type=\"text\" name=\"event_end_date\" value=\"%s\" id=\"event_end_date\" style=\"width:70px;\"/>\
				    <input type=\"hidden\" name=\"odu_end_time\" value=\"%s\" id=\"odu_end_time\" style=\"width:80px;\"/>\
				</div>\
				<div class=\"row-elem\">\
				  <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"30%%\">\
				    <tr>\
				    <td style=\"vertical-align:middle;\">\
					    <label class=\"lbl lbl-big\" for=\"serevity\">Severity</label>\
				    </td>\
				    <td style=\"vertical-align:middle;\">\
					    <input type=\"checkbox\" name=\"serevity\" id=\"serevity1\" value=\"1\" />\
				    </td >\
				    <td style=\"vertical-align:middle;\">\
					    <label for=\"serevity1\" >Informational</label>\
				    </td>\
				    <td style=\"vertical-align:middle;\">\
					    <input type=\"checkbox\" name=\"serevity\" id=\"serevity2\" value=\"2\" />\
				    </td>\
				    <td style=\"vertical-align:middle;\">\
					    <label for=\"serevity2\" >Normal</label>\
				    </td>\
				    <td style=\"vertical-align:middle;\">\
					    <input type=\"checkbox\" name=\"serevity\" value=\"3\" id=\"serevity3\"/>\
				    </td>\
				    <td style=\"vertical-align:middle;\">\
					    <label for=\"serevity3\" >Minor</label>\
				    </td>\
				    <td style=\"vertical-align:middle;\">\
					    <input type=\"checkbox\" name=\"serevity\" value=\"4\" id=\"serevity4\"/>\
				    </td style=\"vertical-align:middle;\">\
				    <td style=\"vertical-align:middle;\">\
					    <label for=\"serevity4\" >Major</label>\
				    </td>\
				    <td style=\"vertical-align:middle;\">\
				 	    <input type=\"checkbox\" name=\"serevity\" value=\"5\" id=\"serevity5\"/>\
				    </td>\
				    <td style=\"vertical-align:middle;\">\
					    <label for=\"serevity5\" >Critical</label>\
				   </td>\
				   </tr>\
				</table>\
				</div>\
				<div class=\"row-elem\">\
				    <input type=\"submit\" name=\"submit\" class=\"yo-small yo-button\" id=\"submit_html\" value=\"Submit\" />\
				    <input type=\"button\" class=\"yo-small yo-button\"  id=\"btn_hide\" name=\"btn_hide\" value=\"Hide Search\" />\
				</div></div></form><div id="div_table_paginate"><table cellpadding="0" cellspacing="0" border="0" class="display" id="table_paginate" style="text-align:center;">\
						<thead>\
						<tr>\
							<th></th>\
							<th>Received Time</th>\
							<th>Event Type</th>\
							<th>Event Name</th>\
							<th>Device Type</th>\
							<th>Host Alias</th>\
							<th>IP Address</th>\
							<th>Description</th>\
						</tr>\
					</thead></table></div>'%(trap_status,("" if ip_address == "" or ip_address == None else ip_address.replace("-","")),start_date,'00:00',end_date,'00:00')
		html.write(str(html_form))
		html.write("<div id=\"trap_data_table\">\
		<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"trap_detail\" class=\"display\">\
		</table></div>\
		<div id=\"detail_info_id\"></div></div>")
		# modified by yogesh 
		html.write("<div class='form-div-footer'>")
		html.write("<table class=\"addform\" style=\"border:0px none;width:auto;\"><tr class=\"odd\">")
		html.write("<td style=\"text-align:left;vertical-align:middle;\"><button type=\"submit\"  class=\"yo-button\" style=\"margin-top:5px;margin-bottom:5px;\" onclick=\"trapExcelReportGeneration();\"><span class=\"report\">Excel</span></button>")
		html.write("</td>")
		html.write("<td style=\"text-align:left;vertical-align:middle;\"><button type=\"submit\" class=\"yo-button\" style=\"margin-top:5px;margin-bottom:5px;\" onclick=\"trapCSVReportGeneration();\"><span class=\"report\">CSV</span></button>")
		html.write("</td>")
		html.write("<td style=\"text-align:left;vertical-align:middle;\">")
		html.write("&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp")
		html.write("</td>")
		html.write("<td style=\"vertical-align:middle;\">")
		html.write("<div class=\"trap_select_option_div\" style=\" width: 130px;\" id=\"informational_div\">")
		html.write("<img src=\"images/status-0.png\"  name=\"select_option_div\" alt=\"Informational\" title=\"Informational\" style=\"width:12px\" class=\"imgbutton\" /><span style=\"line-height:20px; padding:0px 12px;cursor:pointer;cursor:hand;\">Informational</span>")
		html.write("</div>")
		html.write("</td>")

		html.write("<td>")
		html.write("<div class=\"trap_select_option_div\" style=\" width:100px;\" id=\"normal_div\">")
		html.write("<img src=\"images/status-7.png\"  name=\"select_option_div\" alt=\"Normal\" title=\"Normal\" style=\"width:12px\" class=\"imgbutton\"/><span  style=\"line-height:20px; padding:0px 12px;cursor:pointer;cursor:hand; \" >Normal</span>")
		html.write("</div>")
		html.write("</td>")

		html.write("<td>")
		html.write("<div class=\"trap_select_option_div\" style=\" width:100px;\" id=\"minor_div\">")
		html.write("<img src=\"images/status-4.png\" alt=\"Minor\" name=\"select_option_div\" title=\"Minor\" class=\"imgbutton\" style=\"width:12px\" /><span  style=\"line-height:20px; padding:0px 12px;cursor:pointer;cursor:hand; \">Minor</span>")
		html.write("</div>")
		html.write("</td>")

		html.write("<td>")
		html.write("<div class=\"trap_select_option_div\" style=\" width:100px;\" id=\"major_div\">")
		html.write("<img src=\"images/minor.png\" alt=\"Major\" name=\"select_option_div\" title=\"Major\"  class=\"imgbutton\" style=\"width:12px\"  /><span style=\"line-height:20px; padding:0px 12px;cursor:pointer;cursor:hand; \">Major</span>")
		html.write("</div>")
		html.write("</td>")

		html.write("<td>")
		html.write("<div class=\"trap_select_option_div\" style=\" width:110px;\" id=\"critical_div\">")
		html.write("<img src=\"images/critical.png\" alt=\"Critical\" name=\"select_option_div\" title=\"Critical\" class=\"imgbutton\" style=\"width:12px\"/><span  style=\"line-height:20px; padding:0px 12px; cursor:pointer;cursor:hand; \">Critical</span>")
		html.write("</div>")
		html.write("</td>")
		html.write("</tr>")
		html.write("</table>")
		html.write("</div>")
		
	else:
		html.new_header(" Warning : Page request not granted","","")
		html.write("<div class=\"warning\" > Access Restricted. Please request access from UNMP admin.</div>")
	html.new_footer()


def trap_filter_function(h):
	'''
	@author: Rajendra Sharma
	@return: this function display the html page for trap information.
	@rtype: return type html page.
	@requires: Its take html object as a argument.
	@var css_list: This is array of all css file used in it.
	@var js_list: This is array of all js file used in it.
	@var ip_address: This is store the ip address from h(html) object.
	@var now: This is store current datetime.
	@since: 20 sept 2011
	@version: 0.1
	@note: this function display the trap information page on browser.
	@organisation: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	'''

	global html
	html=h
	image_dic={0:"images/status-7.png",1:"images/status-0.png",2:"images/status-7.png",3:"images/status-4.png",4:"images/minor.png",5:"images/critical.png"}
	image_title_name={0:"Normal",1:"Informationl",2:"Normal",3:"Minor",4:"Major",5:"Critical"}
	option=html.var("option")        # option take (current,clear,history)status number by html object(Trap_information page).
	#event_id=html.var("eventId")    # event_id take Event Type name id by html object(Trap_information page).
	event_type=html.var("eventType") # event_type take Event Type name name by html object(Trap_information page).
	m_object=html.var("M_obj")       # M_object take Manage object id by html object(Trap_information page).
	m_name=html.var("M_name")        # M_name take Manage object name by html object(Trap_information page).
	trap_ip=html.var("ip")           # trap_ip take trap ip by html object(Trap_information page).
	st_date=html.var("event_start_date")
	start_date=datetime.strptime(st_date,"%d/%m/%Y")		
	and_date=html.var("event_end_date")
	end_date=datetime.strptime(and_date,"%d/%m/%Y")		

	user_id =  html.req.session['user_id']
	agent_id=html.var("agent_id")
	hostgroup_id_list = []
	es = Essential()
	flag_value = 0
	if agent_id != None != agent_id != '':
	    host_id = es.get_host_id(agent_id,"ip_address")
	    if es.is_host_allow(user_id,host_id) != 0:
	        flag_value = 1
	if flag_value == 0:
	    hostgroup_id_list = es.get_hostgroup_ids(user_id)
	    if len(hostgroup_id_list) < 1:
	        flag_value = 2
	#html.write(str(agent_id))
	#html.write(str(hostgroup_id_list))
	#html.write(str(flag_value))
	if flag_value == 0:
		camponent_id=html.var("camponent_id")  # camponent_id take camponent id by html object(Trap_information page).
		serevity1=html.var("serevity1",None)   # serevity variable take serevity value by html object(Trap_information page).
		serevity2=html.var("serevity2",None)
		serevity3=html.var("serevity3",None)
		serevity4=html.var("serevity4",None)
		serevity5=html.var("serevity5",None)
		last_time=html.var("last_execution_time") 
		time_interval=html.var("time_interval_value")
		search_flag=html.var('searchFlag')
		count_times=html.var('countTimes')
		sql=""              # its store the sql query for filter the database.
		sql_1=""
		sql_i = 1           # sql_i make the sql query for trap field.
		sql_j = 1           # sql+j make the fields for serevity value.
		primary_key_id=""   # it store the primary_key_id for particular table according to selected option(ratio button on the trap information page.)
		table_name=""       # it store the table name  for particular table according to selected option(ratio button on the trap information page.)
		if (event_type)!=None:
		         if sql_i > 1:
		             sql +=" and" 
		         sql+=" trap_event_type like '%" + event_type + "%'" 
		         sql_i+=1
		if (m_object)!=None:
		         if sql_i > 1:
		             sql +=" and" 
		         sql+=" manage_obj_id like '%" + m_object + "%'" 
		         sql_i+=1
		if (m_name)!=None:
		         if sql_i > 1:
		             sql +=" and" 
		         sql+=" manage_obj_name like '%" + m_name + "%'" 
		         sql_i+=1
		if (camponent_id)!=None:
		         if sql_i > 1:
		             sql +=" and" 
		         sql+=" component_id like '%" + camponent_id + "%'" 
		         sql_i+=1
		# it store the some field according to filter option
		filter_option=''
		if option == "1": 					# 1 Stand for Current Alarm Details
		    table_name="trap_alarm_current"
		    primary_key_id="trap_alarm_current_id"
		    filter_option="trap_alarm_current_id"
		if option=="2":						# 2 Stand for Clear Alarm Details
		    table_name="trap_alarm_clear"
		    primary_key_id="trap_alarm_clear_id"
		    filter_option="trap_alarm_clear_id"
		if option == "3":					# 3 Stand for All alarm details
		    table_name="trap_alarms"
		    primary_key_id="trap_alarm_id"
		    filter_option="trap_alarm_id"

		if (serevity1)!=None and (serevity1)!="None":
		         if sql_j > 1:
		             sql_1 +=" or" 
		         sql_1+=" serevity like '%" + serevity1 + "%'" 
		         sql_j+=1
		if (serevity2)!=None and (serevity2)!="None":
		         if sql_j > 1:
		             sql_1 +=" or" 
		         sql_1+=" serevity like '%" + serevity2 + "%'"
		         sql_1 +=" or" 
		         sql_1+=" serevity like '%"+('None' if serevity2==None or serevity2.strip()=='' else '0') +"%'"
		         sql_j+=1
		if (serevity3)!=None and (serevity3)!="None":
		         if sql_j > 1:
		             sql_1 +=" or" 
		         sql_1+=" serevity like '%" + serevity3 + "%'" 
		         sql_j+=1
		if (serevity4)!=None and (serevity4)!="None":
		         if sql_j > 1:
		             sql_1 +=" or" 
		         sql_1+=" serevity like '%" + serevity4 + "%'" 
		         sql_j+=1
		if (serevity5)!=None and (serevity5)!="None":
		         if sql_j > 1:
		             sql_1 +=" or" 
		         sql_1+=" serevity like '%" + serevity5 + "%'" 
		         sql_j+=1

		if sql_j > 1:
		    sql=sql+" and ("+sql_1+")"
		try:
		    a_columns=["ta.serevity","STR_TO_DATE(ta.trap_receive_date,'%a %b %e %H:%i:%s %Y')","ta.trap_event_type","ta.event_id","hosts.device_type_id","hosts.host_alias",
		    	       "ta.agent_id","ta.manage_obj_id","ta.manage_obj_name","ta.component_id","ta.description","ta.serevity","ta."+primary_key_id,]
		    s_index_column = "ta."+primary_key_id
		    s_table = table_name
		    s_join = "as ta INNER JOIN hosts ON ta.agent_id=hosts.ip_address \
				INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
				INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id "
		    #s_order= "order by %s desc "%(filter_option)
		    s_order=""
		    s_where= "WHERE  hostgroups.hostgroup_id IN (%s) and %s AND DATE(ta.timestamp) >= '%s' and  DATE(ta.timestamp) <='%s'"%(','.join(hostgroup_id_list),sql,start_date,end_date)
		    if agent_id == "" or agent_id == None:
			s_where="WHERE  hostgroups.hostgroup_id IN (%s) and  %s AND DATE(ta.timestamp) >= '%s' and  DATE(ta.timestamp) <='%s'"%(','.join(hostgroup_id_list),sql,start_date,end_date)
		    else:
		        if "-" in agent_id:
		            s_where="WHERE  hostgroups.hostgroup_id IN (%s) AND agent_id='%s' AND %s AND DATE(ta.timestamp) >= '%s' and  DATE(ta.timestamp) <='%s'"%(','.join(hostgroup_id_list),(agent_id.replace("-","")),sql,start_date,end_date)
			else:
		            s_where="WHERE hostgroups.hostgroup_id IN (%s) AND agent_id like  '%s%%' AND %s AND DATE(ta.timestamp) >= '%s' and  DATE(ta.timestamp) <='%s'"%(','.join(hostgroup_id_list),agent_id,sql,start_date,end_date)
		    s_group_by=""
	            s_limit = "";
		    i_display_start = html.var("iDisplayStart",None)
		    i_display_length = html.var("iDisplayLength",None)
		    i_filtered_total=0
		    i_total=0
    		    sEcho = html.var("sEcho",None)
		    db=MySQLdb.connect(*SystemConfig.get_mysql_credentials())
           	    cursor=db.cursor()
		    query = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s" % (" , ".join(a_columns),s_table,s_join,s_where,s_group_by,s_order)#,s_limit)
    		    i_total=cursor.execute(query)	
		    if (i_display_start != None and i_display_length != '-1'):
			s_limit = "LIMIT %s, %s" % (MySQLdb.escape_string(i_display_start),MySQLdb.escape_string(i_display_length))
	            s_order=""
		    # Ordering
		    i_sort_col_0 = html.var("iSortCol_0",None)
    		    s_order = ""
		    if i_sort_col_0 != None:
			#s_order = "ORDER BY ta.%s desc, "%(filter_option)
			s_order="ORDER BY  "
			for i in range(0,int(html.var("iSortingCols",0))):
				i_sort_col_i = int(html.var("iSortCol_%s" % i,-1))
				b_sortable_ = html.var("bSortable_%s" % i_sort_col_i,None)
				if b_sortable_ == "true":
					s_sort_dir_i = html.var("sSortDir_%s" % i,"asc")
					s_order += " %s %s, " % (a_columns[i_sort_col_i],MySQLdb.escape_string(s_sort_dir_i))
		
			s_order = s_order[:-2]
			if s_order == "ORDER BY":
				s_order = ""
	
		    # Filtering
		    s_search = html.var("sSearch",None)
		    if s_search != "":
    			if s_where == "":
			    s_where +="WHERE ("
			else:
			    s_where += " AND ( "
			for i in range(0,len(a_columns)):
				s_where += "%s LIKE '%%%s%%' OR " % (a_columns[i],MySQLdb.escape_string(s_search))
			s_where = s_where[:-3]
			s_where += ")"
		    # Individual column filtering
		    for i in range(0,len(a_columns)):
			b_searchable_i = html.var("bSearchable_%s" % i,None)
			s_search_i = html.var("sSearch_%s" % i,"")
			if (b_searchable_i == "true" and s_search_i != ""):
    			    if s_where == "":
			        s_where +="WHERE ("
			    else:
			        s_where += " AND "
			    s_where += "%s LIKE '%%%s%%' " % (a_columns[i],MySQLdb.escape_string(s_search_i))
		    cursor.close()
		    cursor=db.cursor() 
		    sql_query2 = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s %s" % (" , ".join(a_columns),s_table,s_join,s_where,s_group_by,s_order,s_limit)
		    #que=sql_query2
		    cursor.execute(sql_query2)
		    result=cursor.fetchall()
    		    cursor.execute("SELECT FOUND_ROWS()")
		    i_filtered_total=cursor.fetchone()[0]
		    cursor.close()
		    db.close()
		    #if last_time !="":
		    #    sql+=" and ta.timestamp < '%s' and ta.timestamp >= '%s'"%(datetime.strptime(last_time,'%Y-%m-%d %H:%M:%S.%f')+timedelta(minutes=1),last_time)

		    # database connection and cursor object creation.
		   # db,cursor=mysql_connection('nmsp')
		    # check the connection created or not.
		    #if db ==1:
		     #   raise SelfException(cursor)
		    #cursor.execute(sql)
		    #result=cursor.fetchall()
		    data_table=[]
		    i=0
		    if result is not None:
		        if len(result)>0:
			        for row in result:
				        i+=1
#				        a_columns=["ta.trap_receive_date","hosts.device_type_id","hosts.host_alias",
#		    	       "ta.event_id","ta.agent_id","ta.serevity","ta.trap_event_id","ta.trap_event_type","ta."+primary_key_id,]
				        img = '<label style="display:none;">%s</label><img src="%s" alt="%s" title="%s" class="imgbutton" style="width:12px" onclick="alarmDetail(\'%s\')"/>'%(row[11],image_dic[int(row[11])],image_title_name[int(row[11])],image_title_name[int(row[11])],int(row[12]))
				        #datetime_object=datetime.strptime(row[3],'%a %b %d %H:%M:%S %Y')
				        #data_table.append([img,datetime_object.strftime("%d %B %Y"),datetime_object.strftime("%I:%M:%S %p"),row[7],row[8],row[1],row[2],row[5],row[6]])
				        #data_table.append([img,row[3],row[3],row[7],row[8],row[1],row[2],row[5],row[6]])
				        row=list(row)
				        row[0]=img
				        row[1]=row[1].strftime("%d-%b-%Y %I:%M:%S %p")
				        row[4]=device_type_dict[row[4]]
				        data_table.append(row)

		    else:
		        data_table=""
		    # close the database connection
		    output = {
			"success":0,
			"sEcho": int(sEcho),
			"iTotalRecords": int(i_total),#i_filtered_total,#i_total,
			"iTotalDisplayRecords": int(i_filtered_total),#i_filtered_total,
			"aaData":data_table
			#"query":que
			}
		# Encode Data into JSON
		    html.write(JSONEncoder().encode(output))
		#		if (int(count_times)<1 and int(search_flag)==1) or (int(count_times)<1 and int(search_flag)==0):
		#			output_dict={'success':0,'data_table':data_table,'last_execution_time':"","sql":str(sql)}
		#		else:
		#    output_dict={'success':0,'data_table':data_table,'last_execution_time':str(datetime.now())}
		#    html.write(str(output_dict))
		# Exception Handling  
		# Exception Handling  
		except MySQLdb as e:
		    output = {
			"success":0,
			"sEcho": int(sEcho),
			"iTotalRecords": int(i_total),#i_filtered_total,#i_total,
			"iTotalDisplayRecords": int(i_filtered_total),#i_filtered_total,
			"aaData":[],
			"except":str(e)
			}
		# Encode Data into JSON
		    html.write(JSONEncoder().encode(output))
		except SelfException:
			pass
		except Exception as e:
		    output = {
			"success":0,
			"sEcho": int(sEcho),
			"iTotalRecords": int(i_total), #i_filtered_total,#i_total,
			"iTotalDisplayRecords": int(i_filtered_total),#i_filtered_total,
			"aaData":[],
			"except":str(e),
			"query":""#sql_query2
			}
		    # Encode Data into JSON
		    html.write(JSONEncoder().encode(output))
	elif flag_value == 2:
		output_dict = {'success':4,'output':'Access Restricted. Please request access from UNMP admin',"sEcho": 1,
			"iTotalRecords": 0,
			"iTotalDisplayRecords": 0,
			"aaData":[]}
		html.write(JSONEncoder().encode(output_dict))
	else:
		output_dict = {'success':4,'output':'Access Restricted. Please request access from UNMP admin.',"sEcho": 1,
			"iTotalRecords": 0,
			"iTotalDisplayRecords": 0,
			"aaData":[]}
		html.write(JSONEncoder().encode(output_dict))
    

def update_date_time(h):
	global html
	html=h
	try:
		end_date=datetime.date(datetime.now())
		output_dict={'success':0,'end_date':str(end_date)}
	except Exception as e:
		output_dict={'success':1,'output':str(e[-1])}
	finally:
		html.req.content_type = 'application/json'
		html.req.write(str(JSONEncoder().encode(output_dict)))



def trap_detail_information(h):
	"""
	@return: this function provide the information in detail of particular trap.
	@rtype: dictinoary.
	@requires: Its required a html object that provide the trap_information page information.
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 13 sept 2011
	@note: this function detail trap informaton according to user clickable action on the table.
	@organisation: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html
	html=h
	option=html.var("option")   # option take (current,clear,history)status number by html object(Trap_information page).
	trap_id=html.var("trap_id") # trap_id take trap id by html object(Trap_information page).
	image_title_name={0:"Normal",1:"Informational",2:"Normal",3:"Minor",4:"Major",5:"Critical"}
	try:

		# create the data base and cursor object.
		db,cursor=mysql_connection()
		if db ==1:
			raise SelfException(cursor)

		if option==1 or option == "1":
			table_name="trap_alarm_current"
			primary_key_id="trap_alarm_current_id"

		elif option==2 or option == "2":
			table_name="trap_alarm_clear"
			primary_key_id="trap_alarm_clear_id"

		elif option==3 or option == "3":
			primary_key_id="trap_alarm_id"
			table_name="trap_alarms"

		sql="SELECT * FROM %s WHERE %s='%s'"%(table_name,primary_key_id,trap_id)
		#html.write(str(sql))
		cursor.execute(sql)
		result=cursor.fetchall()
		cursor.close()
		db.close()
		html.write("<div id=\"login_div\" style=\"width:500px;\">")
		html.write("<table class=\"display\" style=\"margin-left: 5px;\">")
		html.write("<thead>")
		html.write("<tr>")
		html.write("<th colspan=\"2\" class=\"ui-state-default\">")
		html.write("Alarm Details")
		html.write("</th>")
		html.write("</tr>")
		html.write("</thead>")
		if len(result)>0:
			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Event OID</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%result[0][2])
			html.write("</tr>")
			html.write("<tr>")
			html.write("<td>")
			html.write("<b>IP Address</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%result[0][3])
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Up Time</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%str(result[0][4]))
			#html.write("<td>%s</td>"%(datetime.strptime(str(result[0][4]),'%Y-%m-%d %H:%M:%S.%f').strftime('%d %b %y %I:%M:%S %p')))
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Received Date Time</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%(datetime.strptime(str(result[0][5]),'%a %b %d %H:%M:%S %Y').strftime('%d %b %y %I:%M:%S %p')))
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Severity</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%image_title_name[result[0][6]])
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Event ID</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%result[0][7])
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Event Type</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%result[0][8])
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Manage Object ID</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%result[0][9])
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Manage Object Name</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%result[0][10])
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Component ID</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%result[0][11])
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Device IP</b>")
			html.write("</td>")
			html.write("<td>%s</td>"%result[0][12])
			html.write("</tr>")

			html.write("<tr>")
			html.write("<td>")
			html.write("<b>Description</b>")
			html.write("</td>")
			#html.write("<td>%s</td>"%" ".join([ele.capitalize() for ele in result[13].split(" ")]))
			html.write("<td>%s</td>"%result[0][13])
			html.write("</tr>")
		else:
			html.write("<tr>")
			html.write("<td colspan=\"2\">")
			html.write("No Data exist for this alarm.")
			html.write("</td>")
			html.write("</tr>")
		html.write("</table>")
		html.write("</div>")

	# Exception Handling  
        except MySQLdb as e:
		output_dict={'success':3,'output':str(e[-1])}
		html.write(str(output_dict))
        except SelfException:
            pass
        except Exception as e:
		output_dict={'success':1,'output':str(e[-1])}
		html.write(str(output_dict))
        finally:
            if db.open:
                db.close()

def trap_search_elements(h):
        global html
        html = h
	search_element=html.var("serarch_item")
	option=html.var("option")
	search_text=html.var("s")
	trap_list=[]
	try:
		# create the data base and cursor object.
		db,cursor=mysql_connection()
		if db ==1:
			raise SelfException(cursor)

		if option==1 or option == "1":
			table_name="trap_alarm_current"

		elif option==2 or option == "2":
			table_name="trap_alarm_clear"

		elif option==3 or option == "3":
			table_name="trap_alarms"
		if search_element!=None or option!=None:
			sql="SELECT DISTINCT(%s) FROM %s WHERE %s Like '%%%s%%' "%(search_element,table_name,search_element,search_text)
			cursor.execute(sql)
			result=cursor.fetchall()
			for row in result:
				trap_list.append({'Hidden':"",'Name': '' if row[0]==None else row[0]})
		output_dict={'items':trap_list}
		h.req.content_type = 'application/json'
		h.req.write(str(JSONEncoder().encode(output_dict)))
	# Exception Handling  
        except MySQLdb as e:
		output_dict={'Hidden':"",'Name':''}
		h.req.content_type = 'application/json'
		h.req.write(str(JSONEncoder().encode(output_dict)))
        except SelfException:
            pass
        except Exception as e:
		#output_dict={'success':1,'output':str(e[-1])}
		output_dict={'Hidden':"",'Name':''}
		h.req.content_type = 'application/json'
		h.req.write(str(JSONEncoder().encode(output_dict)))
        finally:
            if db.open:
                db.close()
	


def trap_report_creating(h):
        global html
        html = h
	h.req.content_type = 'application/json'
	option=html.var("option") 
	event_type=html.var("eventType") 
	agent_id=html.var("agentId") 
	m_object=html.var("M_obj")
	m_name=html.var("M_name") 
	report_type=html.var("report_type")
	camponent_id=html.var("camponent_id")
	serevity1=html.var("serevity1",None) 
	serevity2=html.var("serevity2",None)
	serevity3=html.var("serevity3",None)
	serevity4=html.var("serevity4",None)
	serevity5=html.var("serevity5",None)
	severity_name={0:"Normal",1:"Informational",2:"Normal",3:"Minor",4:"Major",5:"Critical"}
	st_date=html.var("start_date")
	start_date=datetime.strptime(st_date,"%d/%m/%Y")
	and_date=html.var("end_date")
	end_date=datetime.strptime(and_date,"%d/%m/%Y")		

	sql=""    #its store the sql query for filter the database.
	sql_1=""
	sql_i = 1 # sql_i make the sql query for trap field.
	sql_j = 1 # sql+j make the fields for serevity value.
	primary_key_id="" # it store the primary_key_id for particular table according to selected option(ratio button on the trap information page.)
	hostgroup_id_list = []
	es = Essential()
	user_id =  html.req.session['user_id']
	flag_value = 0
	if agent_id != None != agent_id != '':
	    host_id = es.get_host_id(agent_id,"ip_address")
	    if es.is_host_allow(user_id,host_id) != 0:
	        flag_value = 1
	if flag_value == 0:
	    hostgroup_id_list = es.get_hostgroup_ids(user_id)
	    if len(hostgroup_id_list) < 1:
	        flag_value = 2
	# check the user privilege
	if flag_value == 0:
		try:
			# create the data base and cursor object.
			db,cursor=mysql_connection()
			if db ==1:
				raise SelfException(cursor)

			# import the csv and excel packages
			import csv
			import xlwt
			from xlwt import Workbook, easyxf
			xls_book=Workbook(encoding = 'ascii')
			nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system

			# ----- Excel reproting Style part -----#
			
			style = xlwt.XFStyle() 
			borders = xlwt.Borders() 
			borders.left = xlwt.Borders.THIN 
			borders.right = xlwt.Borders.THIN
			borders.top = xlwt.Borders.THIN
			borders.bottom = xlwt.Borders.THIN
			borders.left_colour = 23
			borders.right_colour = 23
			borders.top_colour = 23
			borders.bottom_colour = 23
			style.borders = borders 
			pattern = xlwt.Pattern() 
			pattern.pattern = xlwt.Pattern.SOLID_PATTERN 
			pattern.pattern_fore_colour =16
			style.pattern = pattern 
			font = xlwt.Font() 
			font.bold = True
			font.colour_index = 0x09
			style.font = font 
			alignment = xlwt.Alignment() 
			alignment.horz = xlwt.Alignment.HORZ_CENTER 
			alignment.vert = xlwt.Alignment.VERT_CENTER 
			style.alignment = alignment 

			style1 = xlwt.XFStyle() 
			alignment = xlwt.Alignment()
			alignment.horz = xlwt.Alignment.HORZ_CENTER 
			alignment.vert = xlwt.Alignment.VERT_CENTER 
			style1.alignment = alignment 
			# -----------   End of style ---------#

			if report_type=='csvReport':
				save_file_name=str(start_date)+'_event_report.csv'
				path='/omd/sites/%s/share/check_mk/web/htdocs/download/%s'%(nms_instance,save_file_name)
				ofile = open(path, "wb")
				writer = csv.writer(ofile, delimiter=',', quotechar='"')
				
			if (event_type)!=None:
				 if sql_i > 1:
				     sql +=" and" 
				 sql+=" trap_event_type like '%" + event_type + "%'" 
				 sql_i+=1
			if (m_object)!=None:
				 if sql_i > 1:
				     sql +=" and" 
				 sql+=" manage_obj_id like '%" + m_object + "%'" 
				 sql_i+=1
			if (m_name)!=None:
				 if sql_i > 1:
				     sql +=" and" 
				 sql+=" manage_obj_name like '%" + m_name + "%'" 
				 sql_i+=1
			if (camponent_id)!=None:
				 if sql_i > 1:
				     sql +=" and" 
				 sql+=" component_id like '%" + camponent_id + "%'" 
				 sql_i+=1
			# it store the some field according to filter option
			for option in range(1,4):
				filter_option=''
				if int(option)== 1: 					 # 1 Stand for Current Alarm Details
				    table_name="trap_alarm_current"
				    primary_key_id="trap_alarm_current_id"
				    filter_option="trap_alarm_current_id"
				if int(option)==2:					 # 2 Stand for Clear Alarm Details
				    table_name="trap_alarm_clear"
				    primary_key_id="trap_alarm_clear_id"
				    filter_option="trap_alarm_clear_id"
				if int(option) == 3:					 # 3 Stand for All alarm details
				    table_name="trap_alarms"
				    primary_key_id="trap_alarm_id"
				    filter_option="trap_alarm_id"

				if (serevity1)!=None and (serevity1)!="None":
					 if sql_j > 1:
					     sql_1 +=" or" 
					 sql_1+=" serevity like '%" + serevity1 + "%'" 
					 sql_j+=1
				if (serevity2)!=None and (serevity2)!="None":
					 if sql_j > 1:
					     sql_1 +=" or" 
					 sql_1+=" serevity like '%" + serevity2 + "%'"
					 sql_1 +=" or" 
					 sql_1+=" serevity like '%"+('None' if serevity2==None or serevity2.strip()=='' else '0') +"%'"
					 sql_j+=1
				if (serevity3)!=None and (serevity3)!="None":
					 if sql_j > 1:
					     sql_1 +=" or" 
					 sql_1+=" serevity like '%" + serevity3 + "%'" 
					 sql_j+=1
				if (serevity4)!=None and (serevity4)!="None":
					 if sql_j > 1:
					     sql_1 +=" or" 
					 sql_1+=" serevity like '%" + serevity4 + "%'" 
					 sql_j+=1
				if (serevity5)!=None and (serevity5)!="None":
					 if sql_j > 1:
					     sql_1 +=" or" 
					 sql_1+=" serevity like '%" + serevity5 + "%'" 
					 sql_j+=1

				if sql_j > 1:
				    sql=sql+" and ("+sql_1+")"
				    sel_query=""

				if agent_id == "" or agent_id == None:
					sel_query="SELECT ta."+primary_key_id+",ta.trap_receive_date,hosts.device_type_id,ta.agent_id,hosts.host_alias,ta.serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,\
						ta.manage_obj_id,ta.manage_obj_name,ta.component_id,ta.description From "+table_name+" as ta\
						INNER JOIN hosts ON ta.agent_id=hosts.ip_address \
						INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
						INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
						WHERE  hostgroups.hostgroup_id IN (%s) and %s AND DATE(ta.timestamp) >= '%s' and  DATE(ta.timestamp) <='%s'"%(','.join(hostgroup_id_list),sql,start_date,end_date)
				else:
					if "-" in agent_id:
					    sel_query="SELECT ta."+primary_key_id+",ta.trap_receive_date,hosts.device_type_id,ta.agent_id,hosts.host_alias,ta.serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,\
					    ta.manage_obj_id,ta.manage_obj_name,ta.component_id,ta.description From "+table_name+" as ta\
					    INNER JOIN hosts ON ta.agent_id=hosts.ip_address\INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
					    INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
					     WHERE  hostgroups.hostgroup_id IN (%s) AND agent_id='%s' AND %s AND DATE(ta.timestamp) >= '%s' and  DATE(ta.timestamp) <='%s'"%(','.join(hostgroup_id_list),(agent_id.replace("-","")),sql,start_date,end_date)
					else:
					    sel_query="SELECT ta."+primary_key_id+",ta.trap_receive_date,hosts.device_type_id,ta.agent_id,hosts.host_alias,ta.serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,\
					    ta.manage_obj_id,ta.manage_obj_name,ta.component_id,ta.description From "+table_name+" as ta\
					    INNER JOIN hosts ON ta.agent_id=hosts.ip_address \
					    INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
					    INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
					    WHERE hostgroups.hostgroup_id IN (%s) AND agent_id like  '%s%%' AND %s AND DATE(ta.timestamp) >= '%s' and  DATE(ta.timestamp) <='%s'"%(','.join(hostgroup_id_list),agent_id,sql,start_date,end_date)
				cursor.execute(sel_query)
				result=cursor.fetchall()


				merge_result=[]
				for row in result:
					merge_result.append([(datetime.strptime(str(row[1]),'%a %b %d %H:%M:%S %Y').strftime('%d %b %y %I:%M:%S %p')),device_type_dict[row[2]],row[3],row[4],severity_name[int(row[5])],row[6],row[7],row[8],row[9],row[10],row[11],row[12]])

				report_option_dict={1:'Current',2:'Clear',3:'History'}
				headings=["Recevied Date Time","Device Type","IP Address","Host Alias","Severity","Event Name","Event ID","Event Type","Manage Object ID","Manage Object Name","Component ID","Description"]

				sheet_count=1
				if report_type=='excelReport':
					xls_sheet=xls_book.add_sheet('%s Event Report%s'%(report_option_dict[int(option)],sheet_count),cell_overwrite_ok=True)
					xls_sheet.row(0).height = 521
					xls_sheet.row(1).height = 421
					xls_sheet.write_merge(0,0,0,len(headings)-1,"%s Event Report"%report_option_dict[int(option)],style)
					xls_sheet.write_merge(1,1,0,len(headings)-1," %s -- %s "%(str(start_date)[:11],str(end_date)[:11]),style)
					xls_sheet.write_merge(2,2,0,len(headings)-1,"",style)
					i=4
					heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
					xls_sheet.set_panes_frozen(True)   # frozen headings instead of split panes
					xls_sheet.set_horz_split_pos(i)    # in general, freeze after last heading row
					xls_sheet.set_remove_splits(True)  # if user does unfreeze, don't leave a split there
					for colx, value in enumerate(headings):
					    xls_sheet.write(i-1, colx, value, heading_xf)
					row_count=4
					for k in range(len(merge_result)):
					    for j in range(len(merge_result[k])):
						width = 5000
						xls_sheet.write(i,j,str(merge_result[k][j]),style1)
						xls_sheet.col(j).width = width 
					    if i==60000:
					        sheet_count+=1
						xls_sheet=xls_book.add_sheet('%s Event Report%s'%(report_option_dict[int(option)],sheet_count),cell_overwrite_ok=True)
						xls_sheet.row(0).height = 521
						xls_sheet.row(1).height = 421
						xls_sheet.write_merge(0,0,0,len(headings)-1,"%s Event Report"%report_option_dict[int(option)],style)
						xls_sheet.write_merge(1,1,0,len(headings)-1," %s -- %s "%(str(start_date)[:11],str(end_date)[:11]),style)
						xls_sheet.write_merge(2,2,0,len(headings)-1,"",style)
						i=4
						heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
						xls_sheet.set_panes_frozen(True)   # frozen headings instead of split panes
						xls_sheet.set_horz_split_pos(i)    # in general, freeze after last heading row
						xls_sheet.set_remove_splits(True)  # if user does unfreeze, don't leave a split there
						for colx, value in enumerate(headings):
						    xls_sheet.write(i-1, colx, value, heading_xf)
					    i=i+1
				elif report_type=='csvReport':
					blank_row=["","",""]
					main_row=["%s Event Report    %s -- %s "%(report_option_dict[int(option)],str(start_date)[:11],str(end_date)[:11])]
					second_row=["","",""]
					writer.writerow(second_row)
					writer.writerow(main_row)
					writer.writerow(second_row)
					writer.writerow(blank_row)
					writer.writerow(headings)
					for row1 in merge_result:
						writer.writerow(row1)

			if report_type=='excelReport':
				save_file_name=str(start_date)+'_event_report.xls'
				path='/omd/sites/%s/share/check_mk/web/htdocs/download/%s'%(nms_instance,save_file_name)
				xls_book.save(path)
			elif report_type=='csvReport':
				ofile.close()
			output_dict={'success':0,'output':'Report Generated Successfully.','file_name':str(save_file_name),'path':path}
			h.req.write(str(JSONEncoder().encode(output_dict)))
		# Exception Handling  
		except MySQLdb as e:
		    output_dict={'success':1,'error_msg':'Error No : 102 '+str(err_obj.get_error_msg(102)),'main_msg':str(e[-1])}
		    h.req.write(str(JSONEncoder().encode(output_dict)))
		except ImportError,e:
		    output_dict={'success':1,'error_msg':'Error No : 101 '+str(err_obj.get_error_msg(101)),'main_msg':str(e[-1])}
		    h.req.write(str(JSONEncoder().encode(output_dict)))
		except IOError,e:
		    output_dict={'success':1,'error_msg':'Error No : 103 '+str(err_obj.get_error_msg(103)),'main_msg':str(e[-1])}
		    h.req.write(str(JSONEncoder().encode(output_dict)))
		except SelfException:
		    output_dict={'success':1,'error_msg':'Error No : 104 '+str(err_obj.get_error_msg(104)),'main_msg':str(e[-1])}
		    h.req.write(str(JSONEncoder().encode(output_dict)))
		except Exception as e:
		    output_dict={'success':1,'error_msg':'Error No : 105 '+str(err_obj.get_error_msg(105)),'main_msg':str(e[-1])}
		    h.req.write(str(JSONEncoder().encode(output_dict)))
		finally:
		    if db.open:
			db.close()
	elif flag_value == 2:
		output_dict = {'success':1,'error_msg':'No hostgroup assigned to your usergroup.'}
		h.req.write(str(JSONEncoder().encode(output_dict)))
	else:
		output_dict = {'success':1,'error_msg':'You are not allowed to view requested host .'}
		h.req.write(str(JSONEncoder().encode(output_dict)))
	

def page_tip_event_details(h):
    global html
    html = h
    html_view = ""\
    "<div id=\"help_container\">"\
    "<h1>Events Details</h1>"\
    "<div><strong>Events Details</strong> has shown all Events information for all devices.</div>"\
    "<br/>"\
    "<div>On this page you can also show event information for current,clear and history.</div>"\
    "<div><strong>History</strong>  : All events of devices</div>"\
    "<div><strong>Current</strong> : All Alarms of devices masked in alarm masking</div>"\
    "<div><strong>Clear</strong>   : All events of devices those are clear in respect to alarm defination in alarm masking</div>"\
    "<div><strong>Note</strong>:For more details on Current and Clear please follow alarm masking page tip </div>"\
    "<br/>"\
    "<div><strong>Actions</strong></div>"\
    "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/normal1.png\"/></div><div class=\"txt-div\">Informationl</div></div>"\
    "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/status-7.png\"/></div><div class=\"txt-div\">Normal events</div></div>"\
    "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/status-4.png\"/></div><div class=\"txt-div\">Minor events</div></div>"\
    "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/minor.png\"/></div><div class=\"txt-div\">Major events</div></div>"\
    "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/status-1.png\"/></div><div class=\"txt-div\">Critical</div></div>"\
    "<br/>"\
    "<div><button  class=\"yo-button\" style=\"margin-top: 5px;\" type=\"submit\">Advanced</button>This button provide the customize search window.</div>"\
    "<br/>"\
    "<div><button id=\"odu_report_btn\" class=\"yo-button\" style=\"margin-top: 5px;\" type=\"submit\"><span class=\"report\">Excel</span></button>Download the Excel report.</div>"\
    "<br/>"\
    "<div><button id=\"odu_report_btn\" class=\"yo-button\" style=\"margin-top: 5px;\" type=\"submit\"><span class=\"report\">CSV</span></button>Download the CSV report.</div>"\
"<div><strong>Note:</strong>This Events Details page show all events information for all devices in UNMP, this is also provide advance filtering of Events.\
    </div>"\
    "</div>"
    html.write(str(html_view))

