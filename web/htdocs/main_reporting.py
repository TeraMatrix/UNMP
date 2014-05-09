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

from datetime import datetime,timedelta
class Report(object):
    @staticmethod
    def list_form(result,host_data,device_type_user_selected_id,device_type_user_selected_name):
        now = datetime.now()
        old=now+timedelta(minutes=-30)
        cday=str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        ctime=str(now.hour)+":"+str(now.minute)
        oday=str(old.day)+"/"+str(old.month)+"/"+str(old.year)
        otime=str(old.hour)+":"+str(old.minute)
        html_view='\
            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
                    </tr>\
            </table><div id="host_data_mapping" style="display:none">%s</div><div id="all_data" style="display:none">%s</div>\
	        <div id="device_type_user_selected_id" style="display:none">%s</div>\
	        <div id="device_type_user_selected_name" style="display:none">%s</div>\
		<form name="get_main_reporting_data" id="get_main_reporting_data" action="main_reporting_get_excel.py"  method=\"get\">\
		<div class="row-elem">\
		<label class=\"lbl lbl-big\" style="width:100px;">Hostgroup:</label>\
		<select name="multiselect_hostgroup" id="multiselect_hostgroup" class="multiselect" multiple="multiple" title="Click to select an option">'%(str(host_data),str(result),device_type_user_selected_id,device_type_user_selected_name)
        dict_hg={}		    
        for i in result:
            if(dict_hg.has_key(str(i[0]))):
                pass
            else:
                html_view+='<option value="%s">%s</option>'%(str(i[0]),str(i[1]))
                dict_hg[str(i[0])]=str(i[1])
        html_view+='</select></div>'
        html_view+='<div class=\"row-elem\">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Device Type:</label>\
		<select name="multiselect_device" id="multiselect_device" class="multiselect" multiple="multiple" title="Click to select an option">\
		</select></div>\
		<div class=\"row-elem\">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Report Type:</label>\
		<select name="multiselect_report" id="multiselect_report" class="multiselect" multiple="multiple" title="Click to select an option">\
		</select></div>\
		<div class="row-elem">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Host Alias:</label>\
		<select name="multiselect_hosts" id="multiselect_hosts" class="multiselect" multiple="multiple" title="Click to select an option">\
		</select></div>\
	   	<div class=\"row-elem\">\
	   	<label class=\"lbl lbl-big\" style="width:100px;" >Time Range:</label>\
		<select name="multiselect_dates" id="multiselect_dates" class="multiselect" title="Click to select an option">\
		<option value=1>Last 30 minutes</option>\
		<option value=2>Last 60 minutes</option>\
		<option value=3>Last 2 hours</option>\
		<option value=4>Last 3 hours</option>\
		<option value=5>Last 6 hours</option>\
		<option value=6>Last 12 hours</option>\
		<option value=7>Last 24 hours</option>\
		<option value=8>Last 1 week</option>\
		<option value=9>Last 2 weeks</option>\
		<option value=15>Current month</option>\
		<option value=10>Previous month</option>\
		<option value=11>Previous 2 months</option>\
		<option value=20>Custom Time Range</option>\
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
		</div>'%(oday,otime,cday,ctime)
        return html_view
        #<div id="selectedList"></div>\

    @staticmethod
    def get_columns(selected_columns,non_selected_columns):
        liList = ""
        plusList=""
        if(non_selected_columns!=[""]):
            for row in non_selected_columns:
                plusList += "<li>" + row + "<img src=\"images/add16.png\" class=\"plus plus\" alt=\"+\" title=\"Add\" id=\"" + row + "\" name=\"" + row + "\"/></li>"
        minusList = ""
        for row in selected_columns:
            minusList += "<li>" + row + "<img src=\"images/minus16.png\" class=\"minus minus\" alt=\"-\" title=\"Remove\" id=\"" + row + "\" name=\"" + row + "\"/></li>"
        selectList=""
        selectList += "<div class=\"multiSelectList\" id=\"multiSelectList\" style=\"margin-left:120px;margin-top:-10px;\">"
        selectList += "<input type=\"hidden\" id=\"hd\" name=\"hd\" value=\"%s\"/>"%(",".join(selected_columns))
        selectList += "<input type=\"hidden\" id=\"hdTemp\" name=\"hdTemp\" />"
        selectList += "<div class=\"selected\">"
        selectList += "<div class=\"shead\"><span id=\"count\">%s</span><span> Select Columns</span><a href=\"#\" id=\"rm\">Remove all</a>"%(len(selected_columns))
        selectList += "</div>"
        selectList += "<ul>"+minusList 
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

    @staticmethod
    def page_tip_main_reporting():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>GENERAL REPORT</h1>"\
            "<br/>"\
            "<div>On this page you can view and generate report for different date and time periods alongwith different hostgroups,device types and different hosts .</div>"\
            "<br/>"\
            "<div>Delta stands for the change in the consecutive values of fields .</div>"\
            "<br/>"\
            "<div><b>Hostgroup</b>: This drop down selects hostgroups for the report.</div>"\
            "<br/>"\
            "<div><b>Device Type</b>: This drop down selects device type for the report.</div>"\
            "<br/>"\
            "<div><b>Report Type</b>:This drop down selects report type for the selected device type.</div>"\
            "<br/>"\
            "<div><b>Host Alias</b>:This drop down selects Hosts for the selected device type . You can also search hosts here.</div>"\
            "<br/>"\
            "<div><b>Date-Time Range</b>:Here you select the date-time range for the report to be generated.</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"submit\" class=\"yo-small yo-button\"><span class=\"ok\">View</span></button> Click here to submit the data.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">Excel Report</span></button>Click here to download the report in Excel format.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">CSV Report</span></button>Click here to download the report in CSV format.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button class=\"yo-button disabled\"type=\"button\" disabled=\"disabled\" style=\"width:90px;\">\
        		More Options >>:</button>:Click and select the headings for which report will be generated.</div></div>"\
            "<br/>"\
            "<div><strong>Note:</strong> You can't choose dates greater than current date and start date should be less than end date.</div>"\
            "<br/>"\
            "</div>"
        return html_view

    @staticmethod    
    def trap_list_form(result,host_data):
        now = datetime.now()
        old=now+timedelta(minutes=-30)
        cday=str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        ctime=str(now.hour)+":"+str(now.minute)
        oday=str(old.day)+"/"+str(old.month)+"/"+str(old.year)
        otime=str(old.hour)+":"+str(old.minute)
        html_view='\
            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
                    </tr>\
            </table><div id="host_data_mapping" style="display:none">%s</div><div id="all_data" style="display:none">%s</div>\
		<form name="trap_get_main_reporting_data" id="trap_get_main_reporting_data" action="trap_main_reporting_get_excel.py"  method=\"get\">\
		<div class=\"row-elem\">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Report Type:</label>\
		<select name="multiselect_report" id="multiselect_report" class="multiselect" multiple="multiple" title="Click to select an option">\
		<option value="current">Current</option>\
		<option value="clear">Clear</option>\
		<option value="history">History</option>\
		<option value="all">All</option>\
		</select></div>\
		<div class="row-elem">\
		<label class=\"lbl lbl-big\" style="width:100px;">Hostgroup ** :</label>\
		<select name="multiselect_hostgroup" id="multiselect_hostgroup" class="multiselect" multiple="multiple" title="Click to select an option">'%(str(host_data),str(result))
        dict_hg={}		    
        for i in result:
            if(dict_hg.has_key(str(i[0]))):
                pass
            else:
                html_view+='<option value="%s">%s</option>'%(str(i[0]),str(i[1]))
                dict_hg[str(i[0])]=str(i[1])
        html_view+='</select></div>'
        html_view+='<div class=\"row-elem\">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Device Type ** :</label>\
		<select name="multiselect_device" id="multiselect_device" class="multiselect" multiple="multiple" title="Click to select an option">\
		</select></div>\
		<div class="row-elem">\
	        <label class=\"lbl lbl-big\" style="width:100px;">Host Alias ** :</label>\
		<select name="multiselect_hosts" id="multiselect_hosts" class="multiselect" multiple="multiple" title="Click to select an option">\
		</select></div>\
	   	<div class=\"row-elem\">\
	   	<label class=\"lbl lbl-big\" style="width:100px;" >Time Range:</label>\
		<select name="multiselect_dates" id="multiselect_dates" class="multiselect" title="Click to select an option">\
		<option value=1>Last 30 minutes</option>\
		<option value=2>Last 60 minutes</option>\
		<option value=3>Last 2 hours</option>\
		<option value=4>Last 3 hours</option>\
		<option value=5>Last 6 hours</option>\
		<option value=6>Last 12 hours</option>\
		<option value=7>Last 24 hours</option>\
		<option value=8>Last 1 week</option>\
		<option value=9>Last 2 weeks</option>\
		<option value=15>Current month</option>\
		<option value=10>Previous month</option>\
		<option value=11>Previous 2 months</option>\
		<option value=20>Custom Time Range</option>\
		</select>\
		</div>\
		<div class=\"row-elem\" id="div_time_select" style="display:none;">\
	   	<label class=\"lbl lbl-big\" style="width:100px">Select Custom Time:</label>\
		<input type="text" id="start_date" name="start_date" value="%s" style="width:70px;" disabled="disabled"/>&nbsp;&nbsp;\
		<input type="text" id="start_time" name="start_time" value="%s" style="width:40px;display:none;" disabled="disabled" />&nbsp;\
		 &nbsp;&nbsp;<input type="text" id="end_date" name="end_date" value="%s" style="width:70px;" disabled="disabled"/>&nbsp;&nbsp;\
		<input type="text" id="end_time" name="end_time" value="%s" style="width:40px;display:none;" disabled="disabled" readonly="readonly"/>\
	        </div>\
	     <div class=\"row-elem\" >\
	     <label class=\"lbl lbl-big\" style="width:100px">**Optional</label>\
	     </div>\
	     <div class=\"row-elem\" >\
			    <button type=\"submit\" class=\"yo-small yo-button\" id=\"submit\" style=\"margin-left:180px\"><span class=\"ok\">View</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" onclick="excel_report(1);" id=\"excel_rpt\" disabled=\"disabled\"><span class=\"report\">Excel</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" onclick="excel_report(2);" id=\"csv_rpt\" disabled=\"disabled\"><span class=\"report\">CSV</span></button>\
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
		</div>'%(oday,otime,cday,ctime)
        return html_view
        #<div id="selectedList"></div>\


    @staticmethod
    def trap_page_tip_main_reporting():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>EVENTS REPORT</h1>"\
            "<br/>"\
            "<div>On this page you can view and generate Event report for different date and time periods alongwith different hostgroups,device types and different hosts .</div>"\
            "<br/>"\
            "<div><b>Report Type</b>:This drop down selects report type of events.</div>"\
            "<br/>"\
            "<div><b>Hostgroup</b>: This drop down selects hostgroups for the report.</div>"\
            "<br/>"\
            "<div><b>Device Type</b>: This drop down selects device type for the report.</div>"\
            "<br/>"\
            "<div><b>Host Alias</b>:This drop down selects Hosts for the selected device type . You can also search hosts here.</div>"\
            "<br/>"\
            "<div><b>Time Range</b>:Here you select the date-time range for the report to be generated.</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"submit\" class=\"yo-small yo-button\"><span class=\"ok\">View</span></button> Click here to submit the data.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">Excel Report</span></button>Click here to download the report in Excel format.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">CSV Report</span></button>Click here to download the report in CSV format.</div></div>"\
            "<br/>"\
            "<div><strong>Note:</strong> You can generate a general events report by selecting the report type.</div>"\
            "<br/>"\
            "</div>"
        return html_view
