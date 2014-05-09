#!/usr/bin/python2.6

## import module 
import MySQLdb
import htmllib


def start_page(h):
	global html
	html=h
	h.new_header("Alarm")
	html.write("<script src=\"js/jquery-1.4.4.min.js\" type=\"text/javascript\"></script>")
	html.write("<script src=\"js/jquery.validate.min.js\" type=\"text/javascript\"></script>")
	html.write("<script src=\"js/alarm_information.js\" type=\"text/javascript\"></script>")
	html.write("<link href=\"css/alarm_masking.css\" type=\"text/css\" rel=\"stylesheet\"></link>")

	html_content1="<div id=\"alarmTableContainer\">\
		<div id=\"header\">\
		    <span>Alarm Table</span>\
		    <div id=\"alarm-type\">\
		    	<ul id=\"alarm-type-list\">\
	        	<li class=\"selected filCmd\" id=\"current\">Current</li>\
		            <li id=\"history\" class=\"filCmd\">History</li>\
		            <li id=\"clear\" class=\"filCmd\">Clear</li>\
			        </ul>\
	       	    		</div>\
			</div>\
			<div id=\"alarm-table-wrapper\">\
		<form id=\"alarm_info_form\" action=\"alarm_current_detail.py\" method=\"POST\">"
	html_content1+="<table width=\"100%\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\">\
	<thead>\
	<tr>\
	<td>&nbsp;</td>\
	    <td><div>Trap IP</div></td>\
	    <td><div>Severity</div></td>\
	    <td><div>Event Id</div></td>\
	    <td><div>Up Time</div></td>\
	    <td><div>Trap Receive Time</div></td>\
	    <td><div>Event Type</div></td>\
	    <td><div>Object Name</div></td>\
	    <td><div>Description</div></td>\
		</tr>\
		</thead>\
		<tbody id=\"event_body\">\
	<tr id=\"tableFilter\">\
		<td><input type=\"checkbox\" class=\"event_chk\" name=\"event_chk\" id=\"main_chk_box\" /></td>\
		   <td><input type=\"text\" name=\"trap_ip\" id=\"trap_ip\" ></td>\
		    <td><select name=\"servity_check\" id=\"servity_check\" >\
				<option value=\" \">...</option>\
				<option value=\"1\">Information</option>\
				<option value=\"2\">Normal</option>\
				<option value=\"3\">Minor</option>\
				<option value=\"4\">Major</option>\
				<option value=\"5\">Critical</option>\
			</select></td>\
		    <td ><input type=\"text\" name=\"event_id\" id=\"event_id\" ></td>\
		    <td><input type=\"text\" name=\"up_tym\" id=\"up_tym\"></td>\
		    <td><input type=\"text\" name=\"trap_rcv\" id=\"trap_rcv\"></td>\
		    <td><input type=\"text\" name=\"eve_typ\" id=\"eve_typ\"></td>\
		    <td><input type=\"text\" name=\"obj_typ\" id=\"obj_typ\"></td>\
		   <td><input type=\"text\" name=\"eve_dscr\" id=\"eve_dscr\"></td></tr>"
	html.write(html_content1)
	alarm_datail_function(h)
	html_content2="</tbody></table></form></div>\
	</div>"
	html.write(html_content2)
	html.new_footer()




def alarm_datail_function(h):
	global html
	html=h
	serevity_value=['Normal','Informational','Normal','Minor','Major','Critical']
	##event_id+"&up_tym="+up_time+"&trap_rcv="+trap_rcv+"&eve_typ="+event_type+"&obj_typ="+object_type+"&event_dscr="+event_dscr+"&alarm_status="+alarm_status,
	option=html.var("servity_check")
	event_id=html.var("event_id")
	up_tym=html.var("up_tym")
	trap_rcv=html.var("trap_rcv")
	eve_typ=html.var("eve_typ")
	obj_typ=html.var("obj_typ")
	event_dscr=html.var("event_dscr")
	alarm_status=html.var("alarm_status")
#	html.write(str(alarm_status))
	sql=""
	sql_1=""
	sql_i = 1
	if (event_id)!=None:
             if sql_i > 1:
                 sql +=" and" 
             sql+="( event_id like '%" + event_id + "%')" 
             sql_i+=1
	if (up_tym)!=None:
             if sql_i > 1:
                 sql +=" and" 
             sql+="( trap_date like '%" + up_tym + "%')" 
             sql_i+=1
	if (trap_rcv)!=None:
             if sql_i > 1:
                 sql +=" and" 
             sql+="( trap_receive like '%" + trap_rcv + "%')" 
             sql_i+=1


	if (eve_typ)!=None:
             if sql_i > 1:
                 sql +=" and" 
             sql+="( trap_event_type like '%" + eve_typ + "%')" 
             sql_i+=1

	if (obj_typ)!=None:
             if sql_i > 1:
                 sql +=" and" 
             sql+="( manage_obj_name like '%" + obj_typ + "%')" 
             sql_i+=1

	if (event_dscr)!=None:
             if sql_i > 1:
                 sql +=" and" 
             sql+="( description like '%" + event_dscr + "%')" 
             sql_i+=1


	if option != "":
		if sql_i > 1:
			sql +=" and "
		sql+= "( serevity = 1  or serevity = 2 or serevity = 3 or serevity = 4 or serevity = 5 )"	
		sql_i+=1
	else:
		if sql_i > 1:
			sql +=" and"
		sql += "(serevity = %s)"
		sql_i +=1		


	if str(alarm_status).lower() == "none" or str(alarm_status).lower() == "current":
		sql+=" and (status = 0)"
	elif str(alarm_status).lower() == "clear":
		sql+=" and (status = 1)"		







#################----------- its privious code and its not used here ------------------------------##################3

#	if (m_name)!=None:
#            if sql_i > 1:
#                sql +=" and" 
#            sql+=" manage_obj_name like '%" + m_name + "%'" 
#            sql_i+=1
#	if (trap_ip)!=None:
#             if sql_i > 1:
#                sql +=" and" 
#             sql+=" trap_ip like '%" + trap_ip + "%'" 
#             sql_i+=1




#	if option == "1": 					# 1 Stand for Current Alarm Details
#		sql+=" and status = 0"
#	if option=="2":						# 2 Stand for Clear Alarm Details
#		sql+=" and status = 1"
	
		
#	if (serevity1)!=None:
#             if sql_j > 1:
#                 sql_1 +=" or" 
##             sql_1+=" serevity like '%" + serevity1 + "%'" 
#             sql_j+=1
#	if (serevity2)!=None:
#             if sql_j > 1:
#                 sql_1 +=" or" 
#             sql_1+=" serevity like '%" + serevity2 + "%'" 
#             sql_j+=1
#	if (serevity3)!=None:
#             if sql_j > 1:
#                 sql_1 +=" or" 
#             sql_1+=" serevity like '%" + serevity3 + "%'" 
#             sql_j+=1
#	if (serevity4)!=None:
#             if sql_j > 1:
#                 sql_1 +=" or" 
#             sql_1+=" serevity like '%" + serevity4 + "%'" 
#             sql_j+=1
#	if (serevity5)!=None:
#             if sql_j > 1:
#                 sql_1 +=" or" 
#             sql_1+=" serevity like '%" + serevity5 + "%'" 
#             sql_j+=1
#
#	if sql_j > 1:
#		sql=sql+" and ("+sql_1+")"
####################################---------------------     -----------------------------------##################################




#
#	if sql_j > 1:
#		sql=sql+" and ("+sql_1+")"

	
	
        #sql="SELECT trap_ip,serevity,event_id,trap_date,trap_receive,trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,camponent_id,description FROM snmptt_status WHERE" +sql
	sql="SELECT trap_ip,serevity,event_id,trap_date,trap_receive,trap_event_type,manage_obj_name,description FROM snmptt_status WHERE" +sql
	#html.write(sql)
	#html.write(str(serevity_value[1]))
	row=""
	try:
		db=MySQLdb.connect("localhost","root","root","nms")
		cursor = db.cursor()
		cursor.execute(sql)
		result=cursor.fetchall()
	except Exception,e:
		html.write(str(e))

	i=1
	html_content1 = "<tr>"
	for row in result:	
		html_content1+="<td ><div><input type=\"checkbox\" class=\"event_chk\" /></div></td>\
			<td ><div>%s</div></td>\
			<td ><div>%s</div></td>\
			<td ><div>%s</div></td>\
			<td ><div>%s</div></td>\
			<td ><div>%s</div></td>\
			<td ><div>%s</div></td>\
			<td ><div>%s</div></td>\
			<td ><div>%s</div></td>\
			</tr>"%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
		i+=1	
	html.write(html_content1)




	

		
			




