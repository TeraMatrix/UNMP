#!/usr/bin/python2.6

"""
@author:   Mahipal Choudhary
@date:     07-11-2011
@version:  0.1
@summary:  this is the View for the user to give inputs and generate a report for it
@organisation:  Codescape Consultants Pvt ltd
"""
#<span class="search-input"><input type="text" /></span>
# this is used for searching

from datetime import datetime, timedelta
import calendar


class Report(object):
    @staticmethod
    def get_month(year_month, status):
        if year_month != "":
            temp = year_month.split("_")
            month_value = calendar.month_name[int(temp[1])] + " " + temp[0]
        else:
            month_value = ""
        now = datetime.now()
        month_str = ""
        month_var = now.month - 2
        year_var = now.year
        if month_var <= 0:
            year_var = year_var - 1
            month_var = -month_var
            month_var = 12 - month_var
        d = datetime.now()
        m = d.month
        y = d.year
        n = 10  # month till before you want
        li = []
        for i in range(2):
            m -= 1
        if m < 0:
            y = d.year - 1
            m = 12 - abs(m)
        elif m > 0:
            for i in range(0, m):
                li.append(str(y) + "_" + str(m))
                m -= 1
            y = y - 1

        for i in range(0, 12 - m - n):
            li.append(str(y) + "_" + str(12 - i))

        li.reverse()
        for i in li:
            temp = i.split("_")
            month_str += "<option value=%s>%s %s</option>" % (
                i, calendar.month_name[int(temp[1])], temp[0])

        html_view = '\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
            <tr>\
                <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
            </tr>\
		</table>\
		<form name="get_history_reporting_data" id="get_history_reporting_data" action="history_reporting_get_excel.py"  method=\"get\">\
		  <div class=\"row-elem\">\
		      <label class=\"lbl lbl-big\" style="width:100px;">Select Action:</label>\
		      <select name="multiselect_action" id="multiselect_action" class="multiselect" multiple="multiple" title="Click to select an option">\
		          <option value="backup">Backup Data</option>\
		          <option value="restore">Restore Data</option>\
		          <option value="clean">Clean Data</option>\
		      </select>\
          </div>\
		  <div class=\"row-elem\">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Select Month:</label>\
		    <select name="multiselect_month" id="multiselect_month" class="multiselect" multiple="multiple" title="Click to select an option">\
		      %s\
		    </select>\
		  </div>\
		  <div class=\"row-elem\">\
	        <button type=\"button\" class=\"yo-small yo-button\" id=\"restore_db_button\" style=\"display:none;width:54px;margin-left:121px\" onclick=\"checkDb();\">Restore data</button>\
	        <button type=\"button\" class=\"yo-small yo-button\" id=\"backup_db_button\" style=\"display:none;width:54px;margin-left:121px\" onclick=\"backDb();\">Backup data</button>\
	        <button type=\"button\" class=\"yo-small yo-button\" id=\"clean_db_button\" style=\"display:none;width:54px;margin-left:121px\" onclick=\"cleanDb();\">Clean data</button></div>\
		' % (month_str)
        # return html_view
        if year_month != "":
            temp = year_month.split("_")
            month_name = calendar.month_name[int(temp[1])] + " " + (temp[0])
            html_view += '\
    		<div id=\"last_loaded_info_div\" style=\"display:none;\">\
    			<div class=\"row-elem\" id=\"row_view_month_label\">\
    				<label class=\"lbl lbl-big\" style="width:120px;margin-top:10px;" id="view_month_label">Last restored month:</label>\
    				<label class=\"lbl lbl-big\" style="width:120px;margin-top:10px;" id="view_month_label_value">%s</label>\
    			</div>\
    			<div class=\"row-elem\" id=\"row_view_data_label\">\
    				<label class=\"lbl lbl-big\" style="width:104px;margin-top:10px;" id="view_data_label">View last restored data:</label>\
    				<button type=\"button\" class=\"yo-small yo-button\" id=\"view_data\" style=\"width:120px;\"  onclick=\"redirect();\">view last restored data</button>\
    			</div>\
    			<input type=\"hidden\" id="status_value" value=\"%s\"/>\
    			<div class=\"row-elem\" id=\"row_clear_data_label\">\
    				<label class=\"lbl lbl-big\" style="width:104px;margin-top:10px;" id="clean_data_label">Clear last restored data:</label>\
    				<button type=\"button\" class=\"yo-small yo-button\" id=\"clean_data\" style=\"width:120px;\"  onclick=\"cleanup_data();\">clear last restored data</button>\
    			</div>\
    		<input type=\"hidden\" id=\"view_month_value\" value=\"%s\"/>\
    		</div>\
    		</form>' % (month_value, status, month_name)
        else:
            html_view += '\
    		<div id=\"last_loaded_info_div\" style=\"display:none;\">\
    			<div class=\"row-elem\">\
    				<label class=\"lbl lbl-big\" style="width:120px;margin-top:10px;" id="view_month_label">Last loaded month:</label>\
    				<label class=\"lbl lbl-big\" style="width:120px;margin-top:10px;" id="view_month_label_value">%s</label>\
    			</div>\
    			<div class=\"row-elem\">\
    				<label class=\"lbl lbl-big\" style="width:104px;margin-top:10px;" id="view_data_label">View last loaded data:</label>\
    				<button type=\"button\" class=\"yo-small yo-button\" id=\"view_data\" style=\"width:120px;\" onclick=\"redirect();\">view last loaded data</button>\
    			</div>\
    			<input type=\"hidden\" id="status_value" value=\"%s\"/>\
    			<div class=\"row-elem\">\
    				<label class=\"lbl lbl-big\" style="width:104px;margin-top:10px;" id="clean_data_label">Clear last loaded data:</label>\
    				<button type=\"button\" class=\"yo-small yo-button\" id=\"clean_data\" style=\"width:120px;\" onclick=\"cleanup_data();\">clear last loaded data</button>\
    			</div>\
    		</div>\
    		</form>' % (month_value, status)
        return html_view

    @staticmethod
    def list_form(result, host_data, device_type_user_selected_id, device_type_user_selected_name, month_str):
        now = datetime.now()
        old = now + timedelta(minutes=-30)
        cday = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
        ctime = str(now.hour) + ":" + str(now.minute)
        oday = str(old.day) + "/" + str(old.month) + "/" + str(old.year)
        otime = str(old.hour) + ":" + str(old.minute)
        month_str = "<option value=%s>%s %s</option>" % (
            month_str, calendar.month_name[int(month_str.split("_")[1])], month_str.split("_")[0])
        html_view = '\
            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
                    </tr>\
            </table><div id="host_data_mapping" style="display:none">%s</div><div id="all_data" style="display:none">%s</div>\
	        <div id="device_type_user_selected_id" style="display:none">%s</div>\
	        <div id="device_type_user_selected_name" style="display:none">%s</div>\
		<form name="get_history_reporting_data" id="get_history_reporting_data" action="history_reporting_get_excel.py"  method=\"get\">\
		<div class=\"row-elem\">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Select Month:</label>\
		<select name="multiselect_month" id="multiselect_month" class="multiselect">\
		%s\
		</select></div>\
		<div class="row-elem">\
		<label class=\"lbl lbl-big\" style="width:100px;">Hostgroup:</label>\
		<select name="multiselect_hostgroup" id="multiselect_hostgroup" class="multiselect" multiple="multiple" title="Click to select an option">' % (
        str(host_data), str(result), device_type_user_selected_id, device_type_user_selected_name, month_str)
        dict_hg = {}
        for i in result:
            if (str(i[0]) in dict_hg):
                pass
            else:
                html_view += '<option value="%s">%s</option>' % (
                    str(i[0]), str(i[1]))
                dict_hg[str(i[0])] = str(i[1])
        html_view += '</select></div>'
        html_view += '<div class=\"row-elem\">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Device Type:</label>\
		<select name="multiselect_device" id="multiselect_device" class="multiselect" multiple="multiple" title="Click to select an option">\
		</select></div>\
		<div class=\"row-elem\">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Report Type:</label>\
		<select name="multiselect_report" id="multiselect_report" class="multiselect" multiple="multiple" title="Click to select an option">\
		</select></div>\
		<div class="row-elem">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Host Name:</label>\
		<select name="multiselect_hosts" id="multiselect_hosts" class="multiselect" multiple="multiple" title="Click to select an option">\
		</select></div>\
	   	<div class=\"row-elem\">\
	   	<label class=\"lbl lbl-big\" style="width:100px;" >Time Range:</label>\
		<select name="multiselect_dates" id="multiselect_dates" class="multiselect" title="Click to select an option">\
		<option value=1>First 7 Days</option>\
		<option value=2>First 15 Days</option>\
		<option value=3>Complete Month</option>\
		</select>\
		</div>\
		<div class=\"row-elem\" id="div_time_select" style="display:none;">\
	   	<label class=\"lbl lbl-big\" style="width:100px">Select Custom Time:</label>\
		<input type="text" id="start_date" name="start_date" value="%s" style="width:70px;" disabled="disabled"/>&nbsp;&nbsp;\
		<input type="text" id="start_time" name="start_time" value="%s" style="width:40px;display:none;" disabled="disabled" />&nbsp;\
		 &nbsp;&nbsp;<input type="text" id="end_date" name="end_date" value="%s" style="width:70px;" disabled="disabled"/>&nbsp;&nbsp;\
		<input type="text" id="end_time" name="end_time" value="%s" style="width:40px;display:none;" disabled="disabled" readonly="readonly"/>\
	        </div>\
	     <div class=\"row-elem\">\
	     <div class=\"user-header-icon\"><button class=\"yo-button disabled\" id= "more_options" type=\"button\" onclick="toggle_options();" disabled="disabled" style="width:90px;">\
        		More Options >>:</button></div>\
		     <div id="more_options_columns" style="margin-top:10px;"></div>\
             </div>\
	     <div class=\"row-elem\" >\
			    <button type=\"submit\" class=\"yo-small yo-button\" id=\"submit\" style=\"margin-left:180px\"><span class=\"ok\">View</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" onclick="excel_report(1);" id=\"excel_rpt\" disabled=\"disabled\"><span class=\"report\">Excel Report</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" onclick="excel_report(2);" id=\"csv_rpt\" disabled=\"disabled\"><span class=\"report\">CSV Report</span></button>\
	     </div>\
	     <div id="div_table_paginate"><table cellpadding="0" cellspacing="0" border="0" class="display" id="table_paginate"></table></div>\
	</form>\
	<div class="detailPanel" style="top:27px;left:600px;position:absolute;">\
			<fieldset  class="themeFieldset">\
				<div  class="legend">Hosts</div>\
				<div id="hostsList">\
					<ul id="HostsList"  class="yo-ul">\
					</ul>\
				</div>\
			</fieldset>\
		</div>' % (oday, otime, cday, ctime)
        return html_view
        #<div id="selectedList"></div>\

    @staticmethod
    def get_columns(selected_columns, non_selected_columns):
        liList = ""
        plusList = ""
        if (non_selected_columns != [""]):
            for row in non_selected_columns:
                plusList += "<li>" + row + "<img src=\"images/add16.png\" class=\"plus plus\" alt=\"+\" title=\"Add\" id=\"" + \
                            row + "\" name=\"" + row + "\"/></li>"
        minusList = ""
        for row in selected_columns:
            minusList += "<li>" + row + "<img src=\"images/minus16.png\" class=\"minus minus\" alt=\"-\" title=\"Remove\" id=\"" + row + "\" name=\"" + \
                         row + "\"/></li>"
        selectList = ""
        selectList += "<div class=\"multiSelectList\" id=\"multiSelectList\" style=\"margin-left:120px;margin-top:-10px;\">"
        selectList += "<input type=\"hidden\" id=\"hd\" name=\"hd\" value=\"%s\"/>" % (
            ",".join(selected_columns))
        selectList += "<input type=\"hidden\" id=\"hdTemp\" name=\"hdTemp\" />"
        selectList += "<div class=\"selected\">"
        selectList += "<div class=\"shead\"><span id=\"count\">%s</span><span> Select Columns</span><a href=\"#\" id=\"rm\">Remove all</a>" % (
        len(selected_columns))
        selectList += "</div>"
        selectList += "<ul>" + minusList
        selectList += "</ul></div>"
        #        selectList += "</div>"
        selectList += "<div class=\"nonSelected\">"
        selectList += "<div class=\"shead\"><a href=\"#\" id=\"add\">Add all</a>"
        selectList += "</div>"
        selectList += "<ul>" + plusList
        selectList += "</ul>"
        selectList += "</div>"
        selectList += "</div>"
        return selectList
        #
        # @staticmethod
        # def page_tip_history_reporting():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_history_reporting.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)
        #
        # @staticmethod
        # def page_tip_main_history_reporting():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_main_history_reporting.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)
        #