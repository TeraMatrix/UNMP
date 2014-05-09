#!/usr/bin/python2.6
#######################################################################################	 
# Author			:	Rajendra Sharma
# Project			:	UNMP
# Version			:	0.1
# File Name			:	googlemap.py
# Creation Date			:	18-September-2011
# Purpose			:	This file display the google map. This file show the all NMS and all connected host from NMS.
# Copyright (c) 2011 Codescape Consultant Private Limited 

#######################################################################################

# success 0 means No error
# success 1  Exception or Error
# success 2 means some mysql error(services not running,connection not created)



# import the modules(pakesges)
import config, htmllib, MySQLdb,time
from compiler.pycodegen import EXCEPT
from mysql_exception import mysql_connection
import  uuid
from datetime import datetime
from utility import Validation
from common_bll import EventLog
from common_bll import Essential
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
		output_dictt={"success":2,"output":str(msg)}
		html.write(str(output_dictt))



def recursive_function(graph1, start, parent_len,service, temp_len):
	"""
	@return: this function return all host detail of a particular NMS.
	@rtype: this function return json format
	@requires: this function take four argument,1. graph1 is contain all relation ship of host to parent, 2. parent node(host) name , 3. its contain the only parent child relation ship    	hosts.,  4. its contain the services of all host, 5. it contain the length of host array(Node).
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@note: this function create the json format with  all host(node) information for particular NMS.
	@organization: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html
	global json
	global host_chain2
	host_chain2 = host_chain2 + [start]
	for node in graph1[start]:
		json += "{\"type\": \"host\",\"name\":\"%s\",\"id\":\"%s\",\"state\":\"%s\",\"lt\":\"%s\",\"lg\":\"%s\",\"lck\":\"%s\",\"device_type\":\"%s\", \"child\":["% (service[node][1],service[node][0], service[node][5], service[node][8],service[node][7],service[node][4],service[node][9])           
		parent_len -= 1
		if not node in host_chain2:
			recursive_function(graph1, node,len(graph1[node]),service,parent_len)
	if temp_len == 0:
		json+= "]}"
	else:
		json+= "]},"

	return host_chain2




# This function display the some silver information of particular host.
# this function take the single html argument.
# this function return dictinoray of result.
# Success 0 for No Error 
# Success 1 for Error
def google_host_graph(h):
	"""
	@return: this function return all host detail of a particular NMS in json format to another file(javascript).
	@rtype: this function return dictnoray.
	@requires: this function take one html agrument.
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@note: this function create a dictnoray of all host information and that information bring form database.
	@organization: Code Scape Consultants Pvt. Ltd. 
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html
	html=h
	global json
	global host_chain2
	sitename = __file__.split("/")[3]
	service_dic={}
	relation_dic={}
	temp=[]
	temp2=[]
	temp3=[]
	parent_array=[]

	output_dictt={} # this store the output result.
	nms_name=html.var('nms_name') # it store nms_name .
	
	try:
		# database connection and cursor object creation.
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)


		sel_query="SELECT hosts.host_id,hosts.ip_address,hosts.host_name,host1.ip_address as parent_name,hosts.lock_status,hosts.host_state_id,host_states.state_name,host_assets.longitude,host_assets.latitude,hosts.device_type_id FROM \
			nms_instance LEFT JOIN hosts ON nms_instance.nms_id=hosts.nms_id \
			LEFT JOIN  host_states ON hosts.host_state_id = host_states.host_state_id \
			LEFT JOIN host_assets ON host_assets.host_asset_id = hosts.host_asset_id \
			LEFT JOIN hosts as host1 ON host1.host_id = hosts.parent_name \
			WHERE hosts.is_deleted=0 and hosts.ip_address='localhost' and nms_instance.nms_name='%s'"%(nms_name) 
		cursor.execute(sel_query)
		# fetch the result.
		lc_result=cursor.fetchall()

		j=0
		# code provided by rahul
		userid =  html.req.session['user_id']
		es = Essential()
		hostgroup_ids_list = es.get_hostgroup_ids(userid)
		# end

		if len(hostgroup_ids_list) > 0:
		    #
		    sql="SELECT hosts.host_id,hosts.ip_address,hosts.host_name,host1.ip_address as parent_name,hosts.lock_status,hosts.host_state_id,host_states.state_name,host_assets.longitude,host_assets.latitude,hosts.device_type_id FROM \
			nms_instance LEFT JOIN hosts ON nms_instance.nms_id=hosts.nms_id \
			LEFT JOIN  host_states ON hosts.host_state_id = host_states.host_state_id \
			LEFT JOIN host_assets ON host_assets.host_asset_id = hosts.host_asset_id \
			LEFT JOIN hosts as host1 ON host1.host_id = hosts.parent_name \
			INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
			INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
			WHERE hosts.is_deleted=0 and nms_instance.nms_name='%s' AND hostgroups.hostgroup_id IN (%s)"%(nms_name,','.join(hostgroup_ids_list)) 
		    cursor.execute(sql)
		    # fetch the result.
		    results=cursor.fetchall()
		else:
		    results=()

		# close the cursor and database connection.
		cursor.close()
		db.close()
		if lc_result is not None:
#		for row in localhost_result:
			service_dic[lc_result[0][1]]=[i for i in lc_result[0]]
			json="[{\"type\":\"host\",\"name\":\"localhost\",\"id\":\"%s\",\"state\":\"%s\",\"lt\":\"%s\",\"lg\":\"%s\",\"lck\":\"f\",\"device_type\":\"%s\", \"child\" : [" %(lc_result[0][0],lc_result[0][5],lc_result[0][8],lc_result[0][7],lc_result[0][9])

		for row in results:
			if row[3]!= "" or row[3] != None:
				parent_array.append([])
				parent_array[j].append(row[1])
				parent_array[j].append(row[3])
				service_dic[row[1]]=[i for i in row]
				
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
			recursive_function(relation_dic, 'localhost',len(relation_dic['localhost']),service_dic,0)
			json+="]"
		else:
			json="[]"

		output_dictt={"success":0,"output":json}
		html.write(str(output_dictt))

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





def graph(h):
	"""
	@return: this function create the page for google map.
	@rtype: this function return the html page for google map display.
	@requires: this function take one html agrument.
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@note: this function display the page for show the google map.
	@organization: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html
	html=h
	css_list = ["css/style.css"]
	javascript_list = []
	#    header_btn = SPDashboardView.header_buttons()
	#snapin_list = ["reports","views","Alarm","Inventory","Settings","NetworkMaps","user_management","schedule","Listing"]
	html.new_header("Google Map","googlemap.py","",css_list,javascript_list)
	html.write("""
<style>
		#customtooltip {display: none;position:absolute;top:0;left:0;z-index:49;-moz-border-radius:8px;-webkit-border-radius:8px;border-radius:8px;padding:10px 15px;background-color:#6A6A6A;}
		#customtooltip1 {display: none;position:absolute;top:0;left:0;z-index:49;-moz-border-radius:8px;-webkit-border-radius:8px;border-radius:8px;padding:10px 15px;background-color:#6A6A6A;}
		.map3saveloc {z-index:50;left: 0; margin-left: auto; margin-right: auto; position: absolute; right: 0;top: 0;width: 20em; z-index: 100;display:none;}
		.map4saveloc {z-index:50;left: 0; margin-left: auto; margin-right: auto; position: absolute; right: 0;top: 0;width: 20em; z-index: 100;display:none;}
		.map5saveloc {z-index:50;left: 0; margin-left: auto; margin-right: auto; position: absolute; right: 0;top: 0;width: 20em; z-index: 100;display:none;}
		.table_map3saver {background-color: white;border: 1px solid black;border-spacing: 1px;margin: 8px auto;}
		.td_map3saver {color: black;font-size: 13px;padding: 2px 8px;}
 		 .map3saveloc td {font-size:11px;}
 		 .table_map4saver {background-color: white;border: 1px solid black;border-spacing: 1px;margin: 8px auto;}
		.td_map4saver {color: black;font-size: 13px;padding: 2px 8px;}
 		 .map4saveloc td {font-size:11px;}
 		 .table_map5saver {background-color: white;border: 1px solid black;border-spacing: 1px;margin: 8px auto;}
		.td_map5saver {color: black;font-size: 13px;padding: 2px 8px;}
 		 .map5saveloc td {font-size:11px;}
    </style>
    	 <link href="css/sidepanel.css" rel="stylesheet" type="text/css" />
	<!--[if IE]>
	       <link rel="stylesheet" type="text/css" href="css/ie_example.css" />
	<![endif]-->
	<script type="text/javascript" src="js/nms.js"></script>	
	<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
	<script src="http://code.jquery.com/jquery-latest.js"></script>
	<script type="text/javascript" src="js/ccpl_map.js"></script>
	<script type="text/javascript" src="js/sidepanel.js"></script>
	
    
</head>
""")
	html.write("""<body onload="loadMap()">
    <div id="map_canvas"></div>
    <div id="customtooltip">
    <input type="checkbox" name="lock" id="chkLock" onchange="javascript:deviceLockUnlock(this);" />
    <label id="lblLock">
    Lock
    </div>
    <div id="customtooltip1">
    <input type="checkbox" name="lock" id="chkMoveOut" onchange="javascript:checkMoveOut(this);" />
    <label id="lblMoveOut">
    Move OutSide
    </div>
    <div class="map3saveloc">
      <table class="table_map3saver">
        <tbody>
          <tr>
            <td class="td_map3saver">Move saved.</td>
            <td class="td_map3saver"><button class="b_map3saver undo" onclick="javascript:undoMove();">Undo</button>
              &nbsp;
              <button class="b_map3saver ok" onclick="javascript:saveMove();">Save</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="map4saveloc" id="newHostSaver" >
      <table class="table_map4saver">
        <tbody>
          <tr>
            <td class="td_map4saver">Add New Host.</td>
            <td class="td_map4saver"><button class="b_map3saver undo" onclick="javascript:undoAdd();">Undo</button>
              &nbsp;
              <button class="b_map3saver ok" onclick="javascript:saveAdd();">Add</button></td>
          </tr>
        </tbody>
      </table>
    </div>
     <div class="map5saveloc" id="newHostSaver" >
      <table class="table_map5saver">
        <tbody>
          <tr>
            <td class="td_map5saver">Save Site Move.</td>
            <td class="td_map5saver"><button class="b_map3saver undo" onclick="javascript:undoSiteMove();">Undo</button>
              &nbsp;
              <button class="b_map3saver ok" onclick="javascript:saveSiteMove();">save</button></td>
          </tr>
        </tbody>
      </table>
    </div>
<div class="cntr hide">
    <div id="ctr" class="h"></div>
        <div id="cnt">
            <div id="f" class="inc">
                <div class="ftc"><span>NMS</span><input type="text" style="width:80px;height:20px;" value="" name="searchNMS" id="searchNMS" onkeyup="searchNMSResult(event)" /></div>
                <div class="fbc" id="ffbc"></div>
            </div>
            <div id="s" class="inc">
                <div class="ftc"><span>Hosts</span><input type="text" value=""  name="searchHost" id="searchHost" onkeyup="searchHostResult(event)" style="width:80px;height:20px;"/></div>
                <div class="fbc" id="sfbc"></div>
            </div>
            <div id="t" class="inc">
                <div class="ftc"><span>New Discover Devices</span></div>
                <div class="fbc" id="tfbc">
                	<!--<div class="nImg"><img src="img.png" alt="hi" /><span>img1</span></div>-->
                </div>
            </div>
        </div>
    </div>
</div>
</body>
""")
	html.new_footer()
	

def save_updates(h):
	"""
	@return: this function return the updated latitude and longitude of host.
	@rtype: this function return a dictnoray of updated host location.
	@requires: this function take one html agrument.
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@note: this function return the updated location by user of host in dictnoray format.
	@organization: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html
	html = h
	host_id = html.var("host_id") # updated host id
	host_log = html.var("host_log") # updated host longitude value.
	host_lat = html.var("host_lat") # updated host latitude value.
	try:
		# create the data base and cursor object.
		db,cursor=mysql_connection('nms_sample')
		# check the database conection created or not.
		if db ==1:
			raise SelfException(cursor)
		if Validation.is_valid_ip(host_id) or host_id.strip()=='localhost':
			sql = "SELECT hosts.host_asset_id,hosts.ip_address,asset.longitude,assets.latitude FROM hosts LEFT JOIN host_assets as asset ON hosts.host_asset_id=asset.host_asset_id WHERE hosts.ip_address='%s'" % host_id
		else:
			sql = "SELECT hosts.host_asset_id,hosts.ip_address,asset.longitude,asset.latitude FROM hosts LEFT JOIN host_assets as asset ON hosts.host_asset_id=asset.host_asset_id WHERE hosts.host_id='%s'" % host_id

		cursor.execute(sql)
                host_asset_info = cursor.fetchall()
		host_asset_id=''
		if len(host_asset_info)>0:
			host_asset_id=host_asset_info[0][0]
			info_str = "Device %s localtion has changed from old longitude:%s,old latitude:%s to new longitude:%s,new latitude:%s"%(host_asset_info[0][1],host_asset_info[0][2],host_asset_info[0][3],host_log,host_lat)

		sql = "UPDATE host_assets SET longitude=%s, latitude=%s WHERE host_asset_id='%s'" % (host_log,host_lat,host_asset_id)
		cursor.execute(sql)
		db.commit()
		# entry in log file for relocaltion
		session_user = html.req.session['username']
		if session_user:
			pass
		else:
			session_user = "NotAvailable"
		info_str+= ' by  %s '%(session_user)
		el = EventLog()
		el.log_event(info_str,session_user)
		cursor.close()
		db.close()
		output_dictt={"success":0,"output":"Successfully updated host location."}
		html.write(str(output_dictt))

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








# This fuction is responsible for the showing the details of all the hosts on the google map we will show this result in table format  on host click event.
# This function take single html argument.
# This function return  cliclable host inforamtion in dictionary.
# Success 0 for No Error.
# Success 1 for Error.
def show_details(h):
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
	host_id = html.var("host_id")
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
		device_name_dict={'odu100':'RM','odu16':'RM18','ap25':'Access Point','idu4':'IDU','idu8':'IDU','unknown':'Generic'}


		sql = "SELECT  hosts.host_name,hosts.ip_address,hosts.mac_address,host_states.state_name,hosts.timestamp,hosts.host_id,hosts.device_type_id,hosts.host_alias FROM hosts LEFT JOIN host_states ON hosts.host_state_id=host_states.host_state_id WHERE host_id='%s'" %  host_id
		# execute the query and fetch the result.
		cursor.execute(sql)
                result=cursor.fetchall()
		sql="SELECT trap_event_type FROM trap_alarm_current WHERE agent_id='%s' order by timestamp limit 1"%host_ip
		cursor.execute(sql)
                last_alarm=cursor.fetchone()
		
		# close the cursor and database connection.
		cursor.close()
		db.close()

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
			host_detail_data+="<div><table style=\"width:300px;font-size:11px;margin-bottom:10px;\"><colgroup><col width=\"30%%\"/><col width=\"5%%\"/><col/></colgroup><tr><th align=\"left\" colspan=\"2\"><img src=\"images/%s\" alt=\"%s\" title=\"%s\" style=\"width:12px;\"/> Host Details<hr/></th><th>Status : %s</th></tr>" % (("host_e.png" if result[0][3]=="Enable" else "host_d.png"),(result[0][3] if result[0][3]=="Enable" else "Disable"),(result[0][3] if result[0][3]=="Enable" else "Disable"),(result[0][3] if result[0][3]=="Enable" else "Disable"))

			for row in result:
				# check for redirecting the page by device_type_id
				if row[6]=='odu16' or row[6]=='odu100' or row[6]=='idu4' or row[6]=='ap25':
					redirect_page='sp_dashboard_profiling'
				else:
					redirect_page='localhost_dashboard'
				# end the checking of code


				host_name = '-' if row[0]=="" or row[0]==None else row[0]

				sevices_status+="<table style=\"width:300px;font-size:11px;\"><colgroup><col width=\"25%%\"/><col width=\"25%%\"/><col width=\"25%%\"/><col width=\"25%%\"/></colgroup>"
				sevices_status+="<tr><td title=\"ok\" style=\"background-color:green; height:20px; width:20px; \"><lable><a href=device_details_example.py?host_id=%s alt=\"ok\" style=\"algin:center;\">%s</td>"%(' ' if row[5]==" " or row[5]==None else row[5],ok)
				sevices_status+="<td title=\"warning\" style=\"background-color:yellow; height:20px; width:20px;\"><lable><a href=device_details_example.py?host_id=%s alt=\"warning\">%s</td>"%(' ' if row[5]==" " or row[5]==None else row[5],warning)
				sevices_status+="<td title=\"critical\" style=\"background-color:red; height:20px; width:20px;\"><lable><a href=device_details_example.py?host_id=%s alt=\"critical\">%s</td>"%(' ' if row[5]==" " or row[5]==None else row[5],critical)
				sevices_status+="<td title=\"unknown\" style=\"background-color:#BBB; height:20px; width:20px;\"><lable><a href=device_details_example.py?host_id=%s alt=\"unknown\">%s</td></tr>"%(' ' if row[5]==" " or row[5]==None else row[5],unknown)



				some_link+="<table style=\"width:300px;font-size:11px;\"><colgroup><col width=\"33%%\"/><col width=\"33%%\"/><col/></colgroup>"
				#some_link+="<tr><td ><lable style=\" width:100px;\"><a href=odu_profiling.py?host_id=%s&device_type=%s&device_list_state=enabled alt=\"Configuration\">Configuration</td>"%(' ' if row[1]=="" or row[5]==None else row[5],' ' if row[6]=="" or row[6]==None else row[6])
				if redirect_page=='localhost_dashboard':
				    pass
				else:
				    some_link+="<tr><td style=\"width:30px\"><lable style=\" width:100px;\"><a href=status_snmptt.py?ip_address=%s- alt=\"Alarms\">Alarms</td>"%('' if row[1]=="" or row[1]==None else row[1])
				some_link+="<td style=\"width:30px\"><lable style=\" width:100px;\"><a href=%s.py?host_id=%s&device_type=%s&device_list_state=enabled alt=\"Dashboard\">Dashboard</td></tr><table>"%(redirect_page,' ' if row[5]=="" or row[5]==None else row[5],' ' if row[6]=="" or row[6]==None else row[6])

				host_detail_data+="<tr><td>Host Alias </td><td>:</td><td><a href=device_details_example.py?host_id=%s>%s</a></td></tr>"%(' ' if row[5]==" " or row[5]==None else row[5],row[7])
			        host_detail_data+="<tr><td>Device Type </td><td>:</td><td> %s </td></tr>"%('-' if row[6]=="" or row[6]==None else device_name_dict[row[6].strip()])
			        host_detail_data+="<tr><td>IP Address </td><td>:</td><td> %s </td></tr>"%('-' if row[1]=="" or row[1]==None else row[1])
			  	host_detail_data+="<tr><td>MAC Address </td><td>:</td><td> %s </td></tr>"%('-' if row[2]=="" or row[2]==None else row[2])
			  	host_detail_data+="<tr><td>Host Age </td><td>:</td><td> %s </td></tr>"%('-' if host_age==0 else paint_age(host_age, checked == 1, 60 * 10))
			  	host_detail_data+="<tr><td>Last Update </td><td>:</td><td> %s </td></tr>"%('-' if row[4]=="" or row[4]==None else datetime.strftime(row[4],"%d %B %Y"))
			  	host_detail_data+="<tr><td>Current Alarm</td><td>:</td><td>%s</td></tr>"%('-' if last_alarm==None else last_alarm[0])
			  	host_detail_data+="<tr><td colspan=\"3\">%s</td></tr></table>"%sevices_status
				host_detail_data+=some_link


		else:
			host_detail_data+="<div><table style=\"width:300px;font-size:11px;margin-bottom:10px;\"><colgroup><col width=\"30%%\"/><col width=\"5%%\"/><col/></colgroup><tr><th align=\"left\" colspan=\"3\">No host inforamtion exits.</tr></th></table>"		

		host_detail_data+="</div>"
		output_dictt={"success":0,"output":str(host_detail_data)}
		html.write(str(output_dictt))

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


# function to create link
def link(name,href):
    """
    @return: this function return the host hyperlink.
    @rtype: this function return in html format.
    @requires: this function take two argument 1. hyperlink location  , 2. hyprelink name.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function return the hyperlink html code.
    @organization: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    return "<a class='newlink' href='" + href + "' >" + name + "</a>"




# This function is count the no of nms exist in the and create the json format for that nms with detail information.
# this function take the single html argument.
# this function return the dictinoray with nms information.
# Success 0 for No Error 
# Success 1 for Error

def nms_details(h):
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
	output_dict={} # output dictinoray.
	try:
		# create the data base and cursor object.
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)

		sql="SELECT ni.nms_name,ni.longitude,ni.latitude,hs.host_state_id FROM nms_instance as ni LEFT JOIN hosts as hs ON ni.nms_id=hs.nms_id where hs.is_deleted=0"
		cursor.execute(sql)
		nms_result=cursor.fetchall()
		# close the database and cursor connection.
		cursor.close()
		db.close()


		nms_data_json="" # it store the information in json format.
		nms_data_json+="["
		if len(nms_result)>0:
			nms_name=nms_result[0][0]
			for  i in range(len(nms_result)):
				if nms_name==nms_result[i][0]:
					if nms_result[i][3]=='e':
						enable_host+=1
					total_host+=1
				else:
					nms_data_json+="{\"type\":\"nms\",\"name\":\"%s\",\"tH\":%s,\"eH\":%s,\"lt\":\"%s\",\"lg\":\"%s\"}%s"%(nms_name,total_host,enable_host,nms_result[i-1][2],nms_result[i-1][1],(',' if i < len(nms_result) else ''))
					enable_host=0
					total_host=0
					nms_name=nms_result[i][0]
#			if total_host == 0 or total_host =='0':
			nms_data_json+="{\"type\":\"nms\",\"name\":\"%s\",\"tH\":%s,\"eH\":%s,\"lt\":\"%s\",\"lg\":\"%s\"}"%(nms_name,total_host,enable_host,nms_result[len(nms_result)-1][2],nms_result[len(nms_result)-1][1])
		nms_data_json+="]"

		output_dictt={"success":0,"output":str(nms_data_json)}
		html.write(str(output_dictt))
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



# This function is provide the new discover devices.
# this function take the single html argument.
# this function return the dictinoray of new discover device.
# Success 0 for No Error 
# Success 1 for Error
def new_discover_deviec(h):
	"""
	@return: this function return the all new discover device.
	@rtype: this function return a dictnoray.
	@requires: this function take one html agrument.
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@note: this function provide the new discover devices by ping,tcp server etc. in dictnoray.
	@organization: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html;
	html=h
	output_dict={} # output dictinoray.
	try:
		# create the data base and cursor object.
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)

		# new discover devices ip address.
		sql=" select tcp_discovery.sys_omc_registerne_site_latitude,tcp_discovery.sys_omc_registerne_site_longitude,tcp_discovery.ip_address from tcp_discovery where tcp_discovery.ip_address NOT IN (SELECT ip_address FROM hosts  where hosts.ip_address = tcp_discovery.ip_address)and tcp_discovery.is_set=0"
		cursor.execute(sql)
		new_device_result=cursor.fetchall()
		# close the cursor and database connection.
		cursor.close()
		db.close()

		new_host_json="" # it store the information in json format.
		new_host_json+="["

		for  i in range(len(new_device_result)):
			new_host_json+="{ \"type\":\"host\",\"name\":\"%s\",\"latitude\":%s,\"longitude\":%s}%s"%(("-" if new_device_result[i][2]=="" or new_device_result[i][2]==None else new_device_result[i][2]),(0 if new_device_result[i][0]=="" or new_device_result[i][0]==None else new_device_result[i][0]),(0 if new_device_result[i][1]=="" or new_device_result[i][1]==None else new_device_result[i][1]),(',' if i < len(new_device_result) - 1 else ''))
		new_host_json+="]"

		output_dictt="{\"success\":0,\"output\":%s}" % new_host_json #{"success":0,"output":str(new_host_json)}
		html.write(str(output_dictt))
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



# This function is provide the new discover devices.
# this function take the single html argument.
# this function return the dictinoray of new discover device.
# Success 0 for No Error 
# Success 1 for Error
def new_host_update(h):
	"""
	@return: this function update the new device information.
	@rtype: this function return a dictnoray.
	@requires: this function take one html agrument.
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@note: this function add the new device in the NMS and update the information.
	@organization: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html;
	html=h
	output_dict={} # output dictinoray.
	parentIp=html.var("parentIp") # parent Ip address
	new_host_ip=html.var("hostIp") # its store the add host IP in google map.
	latitude=html.var("latitude") # new device latitude position
	langitude=html.var("langitude") # new device langitude position
	nms_name=html.var('nmsName')
	try:
		# create the data base and cursor object.
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)

		#assets_id=uuid.uuid1();
		sql="INSERT INTO host_assets (longitude,latitude,serial_number,hardware_version) values('%s','%s','%s','%s','%s')"%(latitude,langitude,'123548','56132');
		cursor.execute(sql)
		db.commit()
		assets_id=cursor.lastrowid
		sql="SELECT nms_id FROM nms_instance WHERE nms_name='%s'"%(nms_name)
		cursor.execute(sql)
		nms_id=cursor.fetchone()[0]

		sql="SELECT site_mac FROM tcp_discovery WHERE ip_address='%s'"%(new_host_ip)
		cursor.execute(sql)
		mac_address=cursor.fetchone()[0]

		sql="SELECT host_id FROM hosts WHERE ip_address='%s'"%(parentIp)
		cursor.execute(sql)
		host_parent_id=cursor.fetchone()[0]

		sql="INSERT INTO hosts (nms_id,host_name,ip_address,host_alias,mac_address,host_asset_id,is_deleted,host_state_id,lock_status,parent_name,device_type_id) values('%s','%s','%s','%s','%s','%s',0,'%s','%s','%s','%s')"%(nms_id,new_host_ip,new_host_ip,new_host_ip,mac_address,assets_id,'e','f',host_parent_id,'unknown')
		# close the cursor and database connection.
		cursor.execute(sql)
		db.commit()

		# close the database and cursor conection.
		cursor.close()
		db.close()

		output_dictt={"success":0,"output":"Add"}
		html.write(str(output_dictt))
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



def site_show_management(h):
	"""
	@return: this function provide the site information for site draw.
	@rtype: this function return a dictnoray.
	@requires: this function take one html agrument.
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@note: this function given the site information to in dictnoray format.
	@organization: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html;
	html=h
	output_dict={} # output dictinoray.
	group_name=""
	nms_name=html.var('nmsName') 
	member_list="" #  its store the member list
	try:
		# create the data base and cursor object.
		db,cursor=mysql_connection('nms_sample')
		if db ==1:
			raise SelfException(cursor)

		json_format=""
		json_format="["
		sql="SELECT ho.hostgroup_name,h.ip_address,a.latitude,a.longitude,h.host_state_id  FROM hostgroups as ho LEFT JOIN  hosts_hostgroups as hho on ho.hostgroup_id=hho.hostgroup_id LEFT JOIN hosts as h on hho.host_id=h.host_id LEFT JOIN host_assets as a on h.host_asset_id=a.host_asset_id inner join nms_instance as ns on h.nms_id=ns.nms_id where ns.nms_name='%s' and h.is_deleted=0 order by ho.hostgroup_name "%(nms_name)
		#json_format=[{'groupName':'ccplGroup','member':[{'id':'172.22.0.110','latitude':'26.734300492187423','longitude':'78.17298168749994'},{'id':'172.22.0.100','latitude':'8.951621362252927','longitude':'80.25747710156247'},{'id':'172.22.0.104','latitude':'33.40517404653511','longitude':'91.29707331250006'},{'id':'172.22.0.101','latitude':'24.382384023760686','longitude':'53.67152041015629'}]}]
		cursor.execute(sql)
		site_result=cursor.fetchall()
		if len(site_result)>0:
			group_name=site_result[0][0]
			for i in range(len(site_result)):
				flag=1
				if i<len(site_result)-1:
					if site_result[i][0]==site_result[i+1][0]:
						flag=0
				if group_name==site_result[i][0]:
				 	member_list+="{\"id\":\"%s\",\"latitude\":\"%s\",\"longitude\":\"%s\",\"state\":\"%s\"}%s"%(site_result[i][1],site_result[i][2],site_result[i][3],site_result[i][4],(',' if flag==0 else ''))
				else:
				 	json_format+="{\"groupName\":\""+group_name+"\",\"member\":["+member_list+"]}%s"%(',' if i<len(site_result) else '')
				 	group_name=site_result[i][0]
				 	member_list=""
				 	member_list+="{\"id\":\"%s\",\"latitude\":\"%s\",\"longitude\":\"%s\",\"state\":\"%s\"}%s"%(site_result[i][1],site_result[i][2],site_result[i][3],site_result[i][4],(',' if flag==0 else ''))
	
		 	json_format+="{\"groupName\":\""+group_name+"\",\"member\":["+member_list+"]}"

	 	json_format+="]"
		# close the database and cursor conection.
		cursor.close()
		db.close()

		output_dictt={"success":0,"output":json_format}
		html.write(str(output_dictt))
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


def host_status_update_information(h):
	"""
	@return: this function provide the hosts status .
	@rtype: this function return a dictnoray.
	@requires: this function take one html agrument.
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@note: this function return the hosts status in dictnoray format.
	@organization: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	global html
	html=h
	output_dict={} # output dictinoray.
	try:
		# create the data base and cursor object.
		db,cursor=mysql_connection('nms2')
		if db ==1:
			raise SelfException(cursor)
		sql="SELECT nagios_hosts.address,nagios_hoststatus.current_state,nagios_hosts.display_name FROM nagios_hosts LEFT JOIN nagios_hoststatus on nagios_hosts.host_id=nagios_hoststatus.hoststatus_id"
		cursor.execute(sql)
		state_result=cursor.fetchall()
		host_state_json=""
		host_state_json+="["
		if len(state_result)>0:
			for i in range(len(state_result)):
				host_state_json+="{\"id\":\"%s\",\"state\":\"%s\",\"name\":\"%s\"}%s"%(state_result[i][0],state_result[i][1],state_result[i][2],(',' if i<len(state_result)-1 else ''))
		host_state_json+="]"
		cursor.close()
		db.close()
		output_dictt={"success":0,"hosts_states":host_state_json}
		html.write(str(output_dictt))

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


def page_tip_google_map(h):
        global html
        html = h
        html_view = ""
        html_view = ""\
        "<div id=\"help_container\">"\
        "<h1>Google Map</h1>"\
        "<div>Google Map show all device status and device information .</div>"\
        "<br/>"\
        "<br/>"\
        "<div><strong>Note:</strong>User can view device located and also device status, User can view newly discovered device from left panel,Search for the device and its health and also user can redirect to dashboard graphs,Events details page\
        </div>"\
        "</div>"
        html.write(str(html_view))



