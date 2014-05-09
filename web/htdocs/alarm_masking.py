#!/usr/bin/python2.6

#######################################################################################	 
# Author			:	Rajendra Sharma
# Project			:	UNMP
# Version			:	0.1
# File Name			:	odu_dashboard.py
# Creation Date			:	11-September-2011
# Purpose			:	This file display the graph for ODU COMMON DASHBOARD.
# Copyright (c) 2011 Codescape Consultant Private Limited 

#######################################################################################



# import module 
import MySQLdb,config,sys
import htmllib
from common_controller import *
from mysql_exception import mysql_connection



#Exception class for own created exception.
class SelfException(Exception):
	"""
	@return: this class return the exception msg.
	@rtype: dictionary
	@requires: Exception class package(module)
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@organisation: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	def __init__(self,msg):
		output_dict={'success':2,'output':str(msg)}
		html.write(str(output_dict))







def start_page(h):
	global html
	html=h
	css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
	js_list = ["js/jquery.dataTables.min.js","js/alarm_masking.js"]
        header_btn = "<div class=\"header-icon\"><img class=\"n-tip-image\" src=\"images/new_icons/round_plus.png\" id=\"add_masking\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Alarm Event\"></div>"
	html.new_header("Alarm Events","",header_btn,css_list,js_list)

	html_content1="<div id=\"alarmTableContainer\">\
		<div id=\"alarm_editable_div\"></div>"

	html.write(html_content1)

	table_content2="<div id=\"demo_id\">\
	<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\">\
	</table>\
	</div>\
	</div>"
	html.write(table_content2)
	html.new_footer()



#------ Its display the table of alarm masking with help oh datatable.-----#

def alarm_masking_information(h):
	global html
	html=h
	try:
		#-- create connection ---- #
		# Open database connection
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)

		sql="SELECT tm.trap_alarm_masking_id,tm.trap_alarm_field,tm.trap_alarm_value,tm.action_id,gp.group_name,tm.scheduling_minutes,tm.is_repeated,tm.acknowledge_id From trap_alarm_masking as tm INNER JOIN groups as gp ON tm.group_id=gp.group_id "

		cursor.execute(sql)
		result=cursor.fetchall()
		data_table="["
		result_len = len(result)
		i = 0
		for row in result:
			i+=1
			data_table+="['%s','%s','%s','%s','%s','%s','%s','<img src=\"images/edit16.png\" alt=\"edit\" title=\"Edit Alarm\" class=\"imgbutton\" onclick=\"editAlarm(\\'%s\\')\" />','<img src=\"images/delete16.png\" alt=\"delete\" title=\"Delete Alarm\" class=\"imgbutton\" onclick=\"checkDeleteAlarm(\\'%s\\')\" />']%s" %(row[1],row[2],row[3],row[4],row[5],("Yes" if 1 == row[6] or '1' == row[6] else "No"),row[7],row[0],row[0],("," if i < result_len else ""))
		data_table+="]"
		cursor.close()
		db.close()
		output_dict={'success':0,'event_table':data_table}
		html.write(str(output_dict))

	# Exception Handling  
	except SelfException:
		if db.open:
			cursor.close()
			db.close()
		pass
	except AttributeError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except NameError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except MySQLdb as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={'success':1,'output':str(e)}
		html.write(str(output_dict))
	except Exception as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DatabaseError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DisconnectionError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	finally:
		if db.open:
			cursor.close()
			db.close()






#----- This function is makes the add and edit form ---- #


def add_edit_masking_table_form(h):
	global html
	html=h
	option=html.var("option") #-- option is show that its add form request  or edit form request------#
	try:
		# Open database connection
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)

		html_form=""
		masking_id=html.var("masking_id")
		if  option == "ADD":
			html_form+="<div id=\"Columns\">\
				 <form id=\"masking_form\" action=\"add_masking_form_entry.py\" method=\"post\">\
				    <div class=\"form-div\">\
					<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
					    <tr>\
						<th id=\"form_title\" class=\"cell-title\">Add Event</th>\
					    </tr>\
					</table>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"trap_alarm_field\" align=\"right\">Event Field</label >\
						<select type=\"text\" id=\"trap_alarm_field\" name=\"trap_alarm_field\" >\
						<option value=\"\">--Select--</option>"
			sql="select trap_alarm_field,field_name from trap_alarm_field_table"
			cursor.execute(sql)
			results=cursor.fetchall()
			for pri in results:
				html_form+="<option value=\"%s\">%s</option>"%(pri[0],pri[1])
			html_form+="</select></div>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"trap_alarm_value\" align=\"right\">Event Value</label >\
						<input type=\"text\" name=\"trap_alarm_value\" id=\"trap_alarm_value\" width=\"5\"/>\
					</div>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"actionid\" align=\"right\">Action Id</label >\
						<select type=\"text\" id=\"actionid\" name=\"actionid\" >\
						<option value=\"\">--Select--</option>"
			sql="select action_id from actions  where is_deleted = 0 order by action_name"
			cursor.execute(sql)
			results=cursor.fetchall()
			for pri in results:
				html_form+="<option value=\"%s\">%s</option>"%(pri[0],pri[0])
			html_form+="</select></div>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"groupid\" align=\"right\">Group Name</label >\
						<select type=\"text\" id=\"groupid\" name=\"groupid\" >\
						<option value=\"\">--Select--</option>"
			sql="select group_id,group_name from groups where is_deleted = 0"
			cursor.execute(sql)
			results=cursor.fetchall()
			for pri in results:
				html_form+="<option value=\"%s\">%s</option>"%(pri[1],pri[1])
			html_form+="</select></div>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"acknowledgeid\" align=\"right\">Acknowledge Status</label >\
						<select type=\"text\" id=\"acknowledgeid\" name=\"acknowledgeid\" >\
						<option value=\"\">--Select--</option>"
			sql="select acknowledge_id,acknowledge_name from acknowledge where is_deleted = 0  order by sequence"
			cursor.execute(sql)
			results=cursor.fetchall()
			for pri in results:
				html_form+="<option value=\"%s\">%s</option>"%(pri[0],pri[1])
			html_form+="</select></div>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"schedule_time\" align=\"right\">Scheduling Time</label >\
						<input type=\"text\" name=\"schedule_time\" id=\"schedule_time\" width=\"5\"/>\
					</div>\
				<div class=\"row-elem\">\
					<label  class = \"lbl lbl-big\"for=\"is_repeted\" align=\"right\">Is Repeated</label >\
					<input type=\"checkbox\" name=\"is_repeted\" id=\"is_repeted\" width=\"5\" value=\"1\"/>\
				</div >\
				<div class=\"row-elem\">\
					<label  class = \"lbl lbl-big\"for=\"desc_id\" align=\"right\">Description</label >\
					<textarea name=\"desc_id\" id=\"desc_id\" ></textarea>\
				</div></div>\
				<div class=\"form-div-footer\">\
					<button type=\"submit\" class=\"yo-small yo-button\"  name=\"submit_button\" id=\"submit_button\"><span class=\"add\">Submit</span></button>\
					<button type=\"button\" class=\"yo-small yo-button\" name=\"cancel_button\" id=\"cancel_button\"><span class=\"cancel\">Cancel</span></button>\
				</div ></form>\
				</div>"

		elif option == "Edit":
	#-- its select the information from trap_mapping_id for show on the edit form ----#
			sql="SELECT 	trap_alarm_masking.trap_alarm_masking_id,trap_alarm_masking.trap_alarm_field,trap_alarm_masking.trap_alarm_value,trap_alarm_masking.action_id,\
			groups.group_name,trap_alarm_masking.acknowledge_id,trap_alarm_masking.is_repeated,trap_alarm_masking.scheduling_minutes ,trap_alarm_masking.description from 				trap_alarm_masking INNER JOIN groups ON groups.group_id=trap_alarm_masking.group_id where trap_alarm_masking_id='%s'"%(masking_id)
 			cursor.execute(sql)
			result=cursor.fetchone()
			html_form+="<div id=\"Columns\">\
				<form id=\"masking_form\" action=\"edit_masking_form_entry.py\" method=\"post\">\
				    <div class=\"form-div\">\
					<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
					    <tr>\
						<th id=\"form_title\" class=\"cell-title\">Edit Event</th>\
					    </tr>\
					</table>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"trap_alarm_field\" align=\"right\">Event Field</label >%s\
					</div>"%(make_alarm_field_select_list(result[1],"enabled","trap_alarm_field",False,"trap field"))
			html_form+="<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"trap_alarm_value\" align=\"right\">Event Value</label >\
						<input type=\"text\" name=\"trap_alarm_value\" id=\"trap_alarm_value\" width=\"5\" value=\"%s\"/>\
					</div>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"actionid\" align=\"right\">Action Id</label >%s\
					</div>"%(result[2],make_action_table_select_list(result[3],"enabled","actionid",False,"action"))
			html_form+="<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"groupid\" align=\"right\">Group Name</label >%s\
					</div>"%(make_group_select_list(result[4],"enabled","groupid",False,"group"))
			html_form+="<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"acknowledgeid\" align=\"right\">Acknowledge Status</label >%s\
					</div>"%(make_acknowledge_table_select_list(result[5],"enabled","acknowledgeid",False,"acknowledge"))
			html_form+="<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"schedule_time\" align=\"right\">Scheduling Time</label >\
						<input type=\"text\" name=\"schedule_time\" id=\"schedule_time\" width=\"5\" value=\"%s\"/>\
					</div>\
					<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"is_repeted\" align=\"right\">Is Repeated</label >\
						<input type=\"checkbox\" name=\"is_repeted\" id=\"is_repeted\" %s width=\"5\" value=\"1\"/>\
					</div >"%(result[7],'checked="checked"' if result[6] == 1  else "")
			html_form+="<div class=\"row-elem\">\
						<label  class = \"lbl lbl-big\"for=\"desc_id\" align=\"right\">Description</label >\
						<textarea name=\"desc_id\" id=\"desc_id\" row=\"5\">%s</textarea>\
					</div ></div >\
					<div class=\"form-div-footer\">\
						<button type=\"submit\" class=\"yo-small yo-button\"  name=\"submit_button\" id=\"submit_button\"><span class=\"edit\">Edit</span></button>\
						<button type=\"button\" class=\"yo-small yo-button\" name=\"cancel_button\" id=\"cancel_button\"><span class=\"cancel\">Cancel</span></button>\
					</div ></form>\
					</div>"%(result[8])


		cursor.close()
		db.close()
		output_dict={'success':0,'html_form':html_form}
		html.write(str(output_dict))

	# Exception Handling  
	except SelfException:
		if db.open:
			cursor.close()
			db.close()
		pass
	except AttributeError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except NameError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except MySQLdb as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={'success':1,'output':str(e)}
		html.write(str(output_dict))
	except Exception as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DatabaseError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DisconnectionError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	finally:
		if db.open:
			cursor.close()
			db.close()


#------ This form is add new entry in alarm_masking_table ----# 


def add_form_entry(h):
	global html
	html=h
	check_entry=0
	cr_by=config.user
	up_by=config.user

	trap_alarm_field=html.var("trap_alarm_field")
	trap_alarm_value=html.var("trap_alarm_value")
	actionid=html.var("actionid")
	groupid=html.var("groupid")
	acknowledgeid=html.var("acknowledgeid")
	is_repeted=html.var("is_repeted")
	desc_id=html.var("desc_id")
	scheduling_min=html.var("schedule_time")
	group_name='Default'

	try:
		# Open database connection
		db,cursor=mysql_connection('nms_copy')
		if db ==1:
			raise SelfException(cursor)

		sel_sql="SELECT groups.group_id FROM groups WHERE groups.group_name='%s'"%(groupid)
		cursor.execute(sel_sql)
		group_id=cursor.fetchall()
		if group_id is not None:
			if len(group_id)>0:
				group_name=group_id[0][0]
		sql="SELECT trap_alarm_field from trap_alarm_masking  where trap_alarm_field='%s' and trap_alarm_value='%s' and group_id='%s'"%(trap_alarm_field,trap_alarm_value,group_name)
		cursor.execute(sql)
		result=cursor.fetchall()
		if len(result) < 1:
			sql="INSERT INTO trap_alarm_masking(trap_alarm_field,trap_alarm_value,action_id,group_id,scheduling_minutes,is_repeated ,acknowledge_id,created_by,creation_time,updated_by,is_deleted,description) values ('%s','%s','%s','%s',%s,%s,'%s','%s',now(),'%s',%s,'%s')"%(trap_alarm_field,trap_alarm_value,actionid,group_name,( 0 if scheduling_min==None or scheduling_min=="" else scheduling_min),(0 if is_repeted == None or is_repeted == "" else 1),acknowledgeid,cr_by,up_by,0,desc_id)
			cursor.execute(sql)
			db.commit()
		else:
			check_entry=3

		output_dict={'success':check_entry}
		html.write(str(output_dict))
		cursor.close()
		db.close()

	# Exception Handling  
	except SelfException:
		if db.open:
			cursor.close()
			db.close()
		pass
	except AttributeError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except NameError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except MySQLdb as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={'success':1,'output':str(e)}
		html.write(str(output_dict))
	except Exception as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DatabaseError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DisconnectionError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	finally:
		if db.open:
			cursor.close()
			db.close()






#--- This function work for delete the record in alarm masking table -------#

def delete_masking_field(h):
	global html
	html=h
	masking_id=html.var("masking_id")
	try:
		# Open database connection
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)

		sql="DELETE from trap_alarm_masking where trap_alarm_masking_id = '%s' "% (masking_id)
		cursor.execute(sql)
		db.commit()
		cursor.close()
		db.close()

	# Exception Handling  
	except SelfException:
		if db.open:
			cursor.close()
			db.close()
		pass
	except AttributeError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except NameError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except MySQLdb as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={'success':1,'output':str(e)}
		html.write(str(output_dict))
	except Exception as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DatabaseError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DisconnectionError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	finally:
		if db.open:
			cursor.close()
			db.close()





#----- This function work on edit the existing entry in alarm table ---- #

def edit_masking_form_entry(h):
	global html
	html=h
	check_entry=0
	cr_by=config.user
	up_by=config.user
	trap_alarm_field=html.var("trap_alarm_field")
	trap_alarm_value=html.var("trap_alarm_value")
	actionid=html.var("actionid")
	groupid=html.var("groupid")
	acknowledgeid=html.var("acknowledgeid")
	is_repeted=html.var("is_repeted")
	desc_id=html.var("desc_id")
	scheduling_min=html.var("schedule_time")
	masking_id=html.var("masking_id")
	try:
		#=-- database connection creation  and cursor creation --- #
		# Open database connection
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)


		sql="SELECT trap_alarm_field from trap_alarm_masking  where trap_alarm_field='%s' and trap_alarm_value='%s' and group_id='%s' and trap_alarm_maSking_id <> '%s'"%(trap_alarm_field,trap_alarm_value,groupid,masking_id)
		cursor.execute(sql)
		result=cursor.fetchone()
		if result==None or result=="":
			result=()
			

		# ----- update the trap_mapping_id table -------#
		if len(result) < 1:
			sql="UPDATE trap_alarm_masking  SET trap_alarm_field = '%s' ,trap_alarm_value = '%s' , action_id = '%s', group_id='%s' , updated_by='%s', scheduling_minutes=%s , is_repeated = %s  ,acknowledge_id='%s',description='%s' where trap_alarm_masking_id = '%s' " %(trap_alarm_field,trap_alarm_value,actionid,groupid,up_by,( 0 if scheduling_min==None or scheduling_min=="" else scheduling_min),(0 if is_repeted == None or is_repeted == "" else 1),acknowledgeid,desc_id,masking_id)
			cursor.execute(sql)
			db.commit()
		else:
			check_entry=3


		cursor.close()
                db.close()
		output_dict={'success':check_entry}
		html.write(str(output_dict))

	# Exception Handling  
	except SelfException:
		if db.open:
			cursor.close()
			db.close()
		pass
	except AttributeError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except NameError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except MySQLdb as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={'success':1,'output':str(e)}
		html.write(str(output_dict))
	except Exception as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DatabaseError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	except DisconnectionError as e:
		if db.open:
			cursor.close()
			db.close()
		output_dict={"success":1,'output':str(e)}
		html.write(str(output_dict))
	finally:
		if db.open:
			cursor.close()
			db.close()


def page_tip_alarm_masking(h):
        global html
        html = h
        html_view = ""\
        "<div id=\"help_container\">"\
        "<h1>Alarm Event</h1>"\
        "<div><strong>Alarm Event</strong> has shows events information for network elements.</div>"\
        "<br/>"\
        "<div>On this page you can Add new event ,Edit event and Delete event.</div>"\
        "<br/>"\
        "<div><strong>Actions</strong></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/edit16.png\"/></div><div class=\"txt-div\">Edit Alarm</div></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/delete16.png\"/></div><div class=\"txt-div\">Delete Alarm</div></div>"\
        "<div class=\"action-tip\"><div class=\"img-div\"><img style=\"width:16px;height:16px;\" src=\"images/new_icons/round_plus.png\"/></div><div class=\"txt-div\">Add Alarm</div></div>"\
        "<br/>"\
 	"<div><strong>Note:</strong>User can add/edit event and as well as he can apply  notification,action,scheduling time.\
	according to this event action is performed by system program.\
        </div>"\
        "</div>"
        html.write(str(html_view))

