#!/usr/bin/python2.6

from datetime import datetime, timedelta


class Log(object):
    @staticmethod
    def create_log_form():
        try:
            html_view = ' <table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"log_table\" style=\"text-align:center;\"> \
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
        except Exception, e:
            return str(e)

    @staticmethod
    def manage_events(group="", user_details=[]):
        from datetime import datetime, timedelta
        import calendar
        now = datetime.now()
        month_str = ""
        month_var = now.month
        year_var = now.year
        d = datetime.now()
        m = d.month
        y = d.year
        n = m - 2 if m > 2 else 0  # month till before you want
        li = []
        if m < 0:
            y = d.year - 1
            m = 12 - abs(m)
        elif m > 0:
            for i in range(n, m):
                li.append(str(y) + "_" + str(m))
                m -= 1
            y = y - 1

        # for i in range(0,12-m-n):
        #    li.append(str(y)+"_"+str(12-i))

        # li.reverse()
        user_menu = ""
        user_display_option = "style=\"display:none\" "

        for i in li:
            temp = i.split("_")
            month_str += "<option value=%s>%s %s</option>" % (
                i, calendar.month_name[int(temp[1])], temp[0])

        month_str += "<option value='all'>All months</option>\
        <option value=20>Custom Date Range</option>"

        now = datetime.now()
        old = now + timedelta(minutes=-30)
        cday = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
        ctime = str(now.hour) + ":" + str(now.minute)
        oday = str(old.day) + "/" + str(old.month) + "/" + str(old.year)
        otime = str(old.hour) + ":" + str(old.minute)

        if group.lower() == "superadmin" or group.lower() == "admin":
            log_html = '<option value=\"0\">Information log</option>\
		<option value=\"1\">Warning log</option>\
		<option value=\"2\">Error log</option>\
		<option value=\"3\">User trail</option>\
		<option value=\"10\">All logs</option>'
            for user in user_details:
                user_menu += "<option value=\"%s\">%s</option>" % (
                    user[0], user[0])
            user_display_option = ""
        else:
            log_html = '<option value=\"0\">User log</option>\
		<option value=\"1\">Warning log</option>\
		<option value=\"2\">Error log</option>\
		<option value=\"10\">All logs</option>'

        html_view = '\
	<div id=\"serach_form_div\">\
	<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id=\"search_form_table\">\
		<thead>\
		<tr>\
		<th colspan=\"2\" class=\"cell-title\">\
		<span style=\"float:left;padding-top:3px;\">Search Logs</span>\
		<img class=\"img-link\" id=\"hide_show\" src=\"images/new/down.png\" style=\"float: right; margin-right: 10px;\" title=\"Show\">\
	</th>\
	</tr>\
	</thead>\
	<tbody style=\"display:none;\">\
	<tr>\
	<td class=\"cell-label\">Select Month</td>\
	<td class=\"cell-info\"><select name="multiselect_month" id="multiselect_month" class="multiselect" multiple="multiple" title="Click to select an option">\
		%s</select></td>\
	</tr>\
	<tr>\
	<td class=\"cell-label\">Select Log type</td>\
	<td class=\"cell-info\"><select name="multiselect_log" id="multiselect_log" class="multiselect" multiple="multiple" title="Click to select an option">\
		%s\
		</select></td>\
	</tr>\
	<tr>\
	<td class=\"cell-label\" %s>Select User</td>\
	<td class=\"cell-info\"  %s><select name="multiselect_users" id="multiselect_users" class="multiselect" multiple="multiple" title="Click to select an option" >\
		%s\
		</select></td>\
	</tr>\
	<tr>\
	<td class=\"cell-label\" id=\"time_select_label_id\" style=\"display:none\" >Select Custom Date:</td>\
	<td class=\"cell-info\"  id=\"time_select_info_id\" style=\"display:none\">\
		<input type="text" id="start_date" name="start_date" value="%s" style="width:70px;" />&nbsp;&nbsp;\
		<input type="text" id="start_time" name="start_time" value="%s" style="width:40px;display:none;" />&nbsp;-\
		 &nbsp;&nbsp;<input type="text" id="end_date" name="end_date" value="%s" style="width:70px;" />&nbsp;&nbsp;\
		<input type="text" id="end_time" name="end_time" value="%s" style="width:40px;display:none;" readonly="readonly"/>\
	</td>\
	</tr>\
	<tr>\
	<td class=\"cell-label\"></td>\
	<td class=\"cell-info\">\
	<button type=\"submit\" class=\"yo-small yo-button\" id=\"submit\" ><span class=\"ok\">View</span></button>\
	<button type=\"button\" class=\"yo-small yo-button\" onclick="excel_report(1);" id=\"excel_rpt\" ><span class=\"report\">Excel Report</span></button>\
	<button type=\"button\" class=\"yo-small yo-button\" onclick="excel_report(2);" id=\"csv_rpt\" style=\"display:none\"  ><span class=\"report\">CSV Report</span></button>\
	</td>\
	</tr>\
	</tbody>\
	</table>\
	</div>\
	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"log_table\" style=\"text-align:center;\"> \
	<colgroup>\
	<col width=\"15%%\"/>\
	<col width=\"15%%\"/>\
	<col width=\"15%%\"/>\
	<col width=\"auto\"/>\
	</colgroup>\
	<thead> \
	<tr> \
	<th>Time</th> \
	<th>Time taken (in sec)</th> \
	<th>User Name</th> \
	<th>Description</th> \
	</tr> \
	</thead> \
	</table>' % (month_str, log_html, user_display_option, user_display_option, user_menu, oday, otime, cday, ctime)
        return html_view

    @staticmethod
    def make_header_log(log_data):
        try:
            html_str = "<table id=\"header_log_table\" cellspacing=\"0\" cellpadding=\"0\" >\
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
                html_str += "<tr>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		   </tr>" % (i[0], i[1], i[2])
            html_str += "</table><a style=\"color:#fff;clear:both;margin-top:-5px;display:block;\" href=\"log_user.py\">More Details</a>"
            return html_str
        except Exception, e:
            return str(e)

    @staticmethod
    def make_alarm_header_log(log_data, device_type_dict):
        try:
            alarm_dic = {"1": "Informational", "0": "Normal",
                         "2": "Normal", "3": "Minor", "4": "Major", "5": "Crititcal"}
# device_type_dict={'odu16':'UBR','odu100':'UBRe','idu4':'IDU','ap25':'Access
# Point'}
            if device_type_dict == {}:
                device_type_dict = {'odu16': 'RM18', 'odu100': 'RM',
                                    'idu4': 'IDU', 'ap25': 'Access Point', 'ccu': 'CCU'}
            html_str = "<table id=\"header_log_table\" cellspacing=\"0\" cellpadding=\"0\">\
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
                html_str += "<tr>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		  	<td align=\"center\">%s</td>\
	    		   </tr>" % (alarm_dic[str(i[0])], i[1], i[2], i[3], device_type_dict.get(i[4], ""), i[5], i[6], i[7])
            html_str += "</table><a style=\"color:#fff;clear:both;padding:10px;display:block;\" href=\"status_snmptt.py\">More Details</a>"
            return html_str
        except Exception, e:
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
            "<div>The top panel provided advanced searching options categorized by months, log type or users for Superadmin/Admin role. </div>"\
            "<br/>"\
            "<div>User can view and generate CSV or Excel reports of logs. </div>"\
            "<br/>"\
            "<div>Superadmin/Admins can view the user trail of different users. </div>"\
            "<br/>"\
            "</div>"
        return html_view
