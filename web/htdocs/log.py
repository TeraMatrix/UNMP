#!/usr/bin/python2.6

from datetime import datetime,timedelta
class Log(object):
    @staticmethod
    def create_log_form():
        try:
            html_view=' <table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"log_table\" style=\"text-align:center;\"> \
					<colgroup>\
					<col width=\"15%\"/>\
					<col width=\"15%\"/>\
					<col width=\"auto\"/>\
				</colgroup>\
					<thead> \
						<tr> \
							<th>Time</th> \
							<th>User Name</th> \
							<th>Description</th> \
						</tr> \
					</thead> \
				</table>'
            return html_view
        except Exception,e:
            return str(e)
            
            
    @staticmethod
    def make_header_log(log_data):
	try:
	    html_str="<table id=\"header_log_table\" cellspacing=\"0\" cellpadding=\"0\" >\
			<colgroup>\
				<col width=\"15%\"/>\
				<col width=\"15%\"/>\
				<col width=\"auto\"/>\
			</colgroup>\
		     <tr><th>Time</th>\
		     	<th>User Name</th>\
		     	<th>Description</th>\
		     </tr>"
	    for i in log_data:
	    	html_str+="<tr>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		   </tr>"%(i[0],i[1],i[2])
	    html_str+="</table><a style=\"color:#fff;clear:both;margin-top:-5px;display:block;\" href=\"log_user.py\">More Details</a>"
            return html_str
        except Exception,e:
            return str(e)
            
            
    @staticmethod
    def make_alarm_header_log(log_data):
	try:
	    alarm_dic={"1":"Informational","0":"Normal","2":"Normal","3":"Minor","4":"Major","5":"Crititcal"}
	    device_type_dict={'odu16':'RM18','odu100':'RM','idu4':'IDU','ap25':'Access Point'}
	    html_str="<table id=\"header_log_table\" cellspacing=\"0\" cellpadding=\"0\">\
			<colgroup>\
				<col width=\"6%\"/>\
				<col width=\"10%\"/>\
				<col width=\"15%\"/>\
				<col width=\"10%\"/>\
				<col width=\"10%\"/>\
				<col width=\"10%\"/>\
				<col width=\"10%\"/>\
				<col width=\"34%\"/>\
			</colgroup>\
		     <tr><th>Alarm Type</th>\
		     	<th>Recieve Time</th>\
		     	<th>Event Type</th>\
		     	<th>Event Name</th>\
		     	<th>Device Type</th>\
		     	<th>Host Alias</th>\
		     	<th>IP Address</th>\
		     	<th>Description</th>\
		     </tr>"
	    for i in log_data:
	    	html_str+="<tr>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		   </tr>"%(alarm_dic[str(i[0])],i[1],i[2],i[3],device_type_dict[i[4]],i[5],i[6],i[7])
	    html_str+="</table><a style=\"color:#fff;clear:both;padding:10px;display:block;\" href=\"status_snmptt.py\">More Details</a>"
            return html_str
        except Exception,e:
            return str(e)            
            
    @staticmethod
    def view_page_tip_log_user():
	html_view = ""\
	"<div id=\"help_container\">"\
	"<h1>USER LOGS</h1>"\
	"<div>This page displays user logs activities done by users </div>"\
	"<br/>"\
	"<div>On this page user can  view the activities performed by different users </div>"\
	"<br/>"\
	"</div>"
	return html_view                         
