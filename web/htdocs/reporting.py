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


class Report(object):
    @staticmethod
    def create_crc_phy_form():
        try:
            now = datetime.now()
            old = now + timedelta(days=-3)
            cday = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
            ctime = str(now.hour) + ":" + str(now.minute)
            oday = str(old.day) + "/" + str(old.month) + "/" + str(old.year)
            otime = "00:00"
            html_view = '\
            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
                    </tr>\
            </table>\
			<form name="get_reporting_data" id="get_reporting_data" action="get_crc_phy_data.py" method=\"get\">\
		<div class="detailPanel" style="width:450px;">\
                 <div class=\"row-elem\">\
					<label class=\"lbl lbl-big\" style="width:100px;" for=\"start_date\">Date-Time Range:</label>\
					<input type="text" id="start_date" name="start_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="start_time" name="start_time" value="%s" style="width:40px" />&nbsp;\
					- &nbsp;&nbsp;<input type="text" id="end_date" name="end_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="end_time" name="end_time" value="%s" style="width:40px"/>\
			     </div><br/>\
                 <div class=\"row-elem\">\
                     <table id=\"search_div\" class=\"row-elem\">\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Group Name:</label></td>\
                             <td><select id="group_search" name="group_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Hosts Name:</label></td>\
                             <td><select id="host_search" name="host_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                     </table>\
                 </div>\
			     <div class=\"row-elem\">\
			    	<label class=\"lbl lbl-big\" style="width:100px;" for=\"no_of_devices\">Number Of Devices:</label>\
			    	<input type=\"text\" id=\"no_of_devices\" name=\"no_of_devices\" title=\"Number of Devices\" value="10" style="width:50px"/> \
			    	<input type=\"hidden\" id=\"host_id\" name=\"host_id\" /> \
				</div>\
			     <div class=\"row-elem\">\
			    <button type=\"submit\" class=\"yo-small yo-button\" id=\"submit\" style="margin-left:220px"><span class=\"ok\">Submit</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" id=\"excel_rpt_crc\"><span class=\"report\">Report</span></button>\
			     </div>\
			</div>\
                        </form>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div class="legend">Groups</div>\
				<div id="groupsList">\
				<ul id="GroupsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
			<div class="detailPanel">\
			    <fieldset  class="themeFieldset">\
				<div  class="legend">Hosts</div>\
				<div id="hostsList">\
				<ul id="HostsList"  class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
            		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id="avg_header" style=\"display: none;\">\
		            	<tr>\
		                <th id=\"form_title\" class=\"cell-title\">Average Per Day:</th>\
		            	</tr>\
                	</table>\
			<table class="display" name="average_report_table" id="average_report_table" width="100%%" >\
			</table>\
                        <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id="total_header" min-height="20px" style=\"display: none;\">\
		            	<tr>\
		                <th id=\"form_title\" class=\"cell-title\">Total Data:</th>\
		            	</tr>\
                	</table>\
			<table class="display" name="total_report_table" id="total_report_table" width="100%%" style=\"display: none;\">\
			</table>' % (oday, otime, cday, ctime)
            return html_view
        except Exception, e:
            return str(e)

    @staticmethod
    def create_rssi_form():
        try:
            now = datetime.now()
            old = now + timedelta(days=-3)
            cday = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
            ctime = str(now.hour) + ":" + str(now.minute)
            oday = str(old.day) + "/" + str(old.month) + "/" + str(old.year)
            otime = "00:00"
            html_view = '\
            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
                    </tr>\
            </table>\
			<form name="get_reporting_data" id="get_reporting_data" action="get_rssi_data.py" method=\"get\">\
		<div class="detailPanel" style="width:500px;">\
                 <div class=\"row-elem\">\
					<label class=\"lbl lbl-big\" style="width:100px;" for=\"start_date\">Date-Time Range:</label>\
					<input type="text" id="start_date" name="start_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="start_time" name="start_time" value="%s" style="width:40px" />&nbsp;\
					- &nbsp;&nbsp;<input type="text" id="end_date" name="end_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="end_time" name="end_time" value="%s" style="width:40px"/>\
			     </div><br/>\
                 <div class=\"row-elem\">\
                     <table id=\"search_div\" class=\"row-elem\">\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Group Name:</label></td>\
                             <td><select  id="group_search" name="group_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Hosts Name:</label></td>\
                             <td><select id="host_search" name="host_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                     </table>\
                 </div>\
			     <div class=\"row-elem\">\
			    	<label class=\"lbl lbl-big\" style="width:100px;" for=\"no_of_devices\">Number Of Devices:</label>\
			    	<input type=\"text\" id=\"no_of_devices\" name=\"no_of_devices\" title=\"Number of Devices\" value="10" style="width:50px"/> \
			    	<input type=\"hidden\" id=\"host_id\" name=\"host_id\" /> \
				</div>\
			     <div class=\"row-elem\">\
			    <button type=\"submit\" class=\"yo-small yo-button\" id=\"submit\" style="margin-left:220px"><span class=\"ok\">Submit</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" id=\"excel_rpt_rssi\"><span class=\"report\">Report</span></button>\
			     </div>\
			</div>\
                        </form>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div  class="legend">Groups</div>\
				<div id="groupsList">\
				<ul id="GroupsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div  class="legend">Hosts</div>\
				<div id="hostsList">\
				<ul id="HostsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
            		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id="avg_header" style=\"display: none;\">\
		            	<tr>\
		                <th id=\"form_title\" class=\"cell-title\">Average RSSI Per Day:</th>\
		            	</tr>\
                	</table>\
			<table class="display" name="average_report_table" id="average_report_table" width="100%%" >\
			</table>\
                        <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id="total_header" min-height="20px" style=\"display: none;\">\
		            	<tr>\
		                <th id=\"form_title\" class=\"cell-title\">Total RSSI Data:</th>\
		            	</tr>\
                	</table>\
			<table class="display" name="total_report_table" id="total_report_table" width="100%%" style=\"display: none;\">\
			</table>' % (oday, otime, cday, ctime)
            return html_view

        except Exception, e:
            return str(e)

    @staticmethod
    def create_network_usage_form():
        try:
            now = datetime.now()
            old = now + timedelta(days=-3)
            cday = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
            ctime = str(now.hour) + ":" + str(now.minute)
            oday = str(old.day) + "/" + str(old.month) + "/" + str(old.year)
            otime = "00:00"
            html_view = '\
            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
                    </tr>\
            </table>\
			<form name="get_reporting_data" id="get_reporting_data" action="get_network_usage_data.py" method=\"get\">\
			<div class="detailPanel" style="width:500px;">\
                 <div class=\"row-elem\">\
					<label class=\"lbl lbl-big\" style="width:100px;" for=\"start_date\">Date-Time Range:</label>\
					<input type="text" id="start_date" name="start_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="start_time" name="start_time" value="%s" style="width:40px" />&nbsp;\
					- &nbsp;&nbsp;<input type="text" id="end_date" name="end_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="end_time" name="end_time" value="%s" style="width:40px"/>\
			     </div><br/>\
                 <div class=\"row-elem\">\
                     <table id=\"search_div\" class=\"row-elem\">\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Group Name:</label></td>\
                             <td><select id="group_search" name="group_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Hosts Name:</label></td>\
                             <td><select id="host_search" name="host_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                     </table>\
                 </div>\
			     <div class=\"row-elem\">\
			    	<label class=\"lbl lbl-big\" style="width:100px;" for=\"no_of_devices\">Number Of Devices:</label>\
			    	<input type=\"text\" id=\"no_of_devices\" name=\"no_of_devices\" title=\"Number of Devices\" value="10" style="width:50px"/> \
			    	<input type=\"hidden\" id=\"host_id\" name=\"host_id\" /> \
				</div>\
			     <div class=\"row-elem\">\
			    <button type=\"submit\" class=\"yo-small yo-button\" id=\"submit\" style="margin-left:220px"><span class=\"ok\">Submit</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" id=\"excel_rpt_nw\"><span class=\"report\">Report</span></button>\
			     </div>\
			</div>\
                        </form>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div  class="legend">Groups</div>\
				<div id="groupsList">\
				<ul id="GroupsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div  class="legend">Hosts</div>\
				<div id="hostsList">\
				<ul id="HostsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
                        <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id="total_header" min-height="20px" style=\"display: none;\">\
		            	<tr>\
		                <th id=\"form_title\" class=\"cell-title\">Total NETWORK USAGE Data:</th>\
		            	</tr>\
                	</table>\
			<table class="display" name="total_report_table" id="total_report_table" width="100%%" style=\"display: none;\">\
			</table>' % (oday, otime, cday, ctime)
            return html_view

        except Exception, e:
            return str(e)

    @staticmethod
    def create_network_outage_form():
        try:
            now = datetime.now()
            old = now + timedelta(days=-3)
            cday = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
            ctime = str(now.hour) + ":" + str(now.minute)
            oday = str(old.day) + "/" + str(old.month) + "/" + str(old.year)
            otime = "00:00"
            html_view = '\
            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
                    </tr>\
            </table>\
			<form name="get_reporting_data" id="get_reporting_data" action="get_network_outage_data.py" method=\"get\">\
			<div class="detailPanel" style="width:500px;">\
                            <div class=\"row-elem\">\
					<label class=\"lbl lbl-big\" style="width:100px;" for=\"start_date\">Date-Time Range:</label>\
					<input type="text" id="start_date" name="start_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="start_time" name="start_time" value="%s" style="width:40px" />&nbsp;\
					- &nbsp;&nbsp;<input type="text" id="end_date" name="end_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="end_time" name="end_time" value="%s" style="width:40px"/>\
			     </div><br/>\
                 <div class=\"row-elem\">\
                     <table id=\"search_div\" class=\"row-elem\">\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Group Name:</label></td>\
                             <td><select id="group_search" name="group_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Hosts Name:</label></td>\
                             <td><select id="host_search" name="host_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                     </table>\
                 </div>\
			     <div class=\"row-elem\">\
			    	<label class=\"lbl lbl-big\" style="width:100px;" for=\"no_of_devices\">Number Of Devices:</label>\
			    	<input type=\"text\" id=\"no_of_devices\" name=\"no_of_devices\" title=\"Number of Devices\" value="10" style="width:50px"/> \
			    	<input type=\"hidden\" id=\"host_id\" name=\"host_id\" /> \
				</div>\
			     <div class=\"row-elem\">\
			    <button type=\"submit\" class=\"yo-small yo-button\" id=\"submit\" style="margin-left:220px"><span class=\"ok\">Submit</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" id=\"excel_rpt_outage\"><span class=\"report\">Report</span></button>\
			     </div>\
			</div>\
                        </form>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div  class="legend">Groups</div>\
				<div id="groupsList">\
				<ul id="GroupsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div  class="legend">Hosts</div>\
				<div id="hostsList">\
				<ul id="HostsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
                        <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id="total_header" min-height="20px" style=\"display: none;\">\
		            	<tr>\
		                <th id=\"form_title\" class=\"cell-title\">Total NETWORK OUTAGE Data:</th>\
		            	</tr>\
                	</table>\
			<table class="display" name="total_report_table" id="total_report_table" width="100%%" style=\"display: none;\">\
			</table>' % (oday, otime, cday, ctime)
            return html_view

        except Exception, e:
            return str(e)

    @staticmethod
    def create_trap_form():
        try:
            now = datetime.now()
            old = now + timedelta(days=-3)
            cday = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
            ctime = str(now.hour) + ":" + str(now.minute)
            oday = str(old.day) + "/" + str(old.month) + "/" + str(old.year)
            otime = "00:00"
            html_view = '\
            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">View/Save Report </th>\
                    </tr>\
            </table>\
			<form name="get_reporting_data" id="get_reporting_data" action="get_trap_data.py" method=\"get\">\
			<div class="detailPanel" style="width:500px;">\
                             <div class=\"row-elem\">\
					<label class=\"lbl lbl-big\" style="width:100px;" for=\"start_date\">Date-Time Range:</label>\
					<input type="text" id="start_date" name="start_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="start_time" name="start_time" value="%s" style="width:40px" />&nbsp;\
					- &nbsp;&nbsp;<input type="text" id="end_date" name="end_date" value="%s" style="width:70px"/>&nbsp;&nbsp;\
                       			<input type="text" id="end_time" name="end_time" value="%s" style="width:40px"/>\
			     </div><br/>\
                 <div class=\"row-elem\">\
                     <table id=\"search_div\" class=\"row-elem\">\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Group Name:</label></td>\
                             <td><select id="group_search" name="group_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                         <tr>\
                             <td><label class=\"lbl lbl-big\" style=\"width: 90px;\">Hosts Name:</label></td>\
                             <td><select id="host_search" name="host_search" style="margin-left:70px;"></select></td>\
                         </tr>\
                     </table>\
                 </div>\
			     <div class=\"row-elem\">\
			    	<label class=\"lbl lbl-big\" style="width:100px;" for=\"no_of_devices\">Number Of Devices:</label>\
			    	<input type=\"text\" id=\"no_of_devices\" name=\"no_of_devices\" title=\"Number of Devices\" value="10" style="width:50px"/> \
			    	<input type=\"hidden\" id=\"host_id\" name=\"host_id\" /> \
				</div>\
			     <div class=\"row-elem\">\
			    <button type=\"submit\" class=\"yo-small yo-button\" id=\"submit\" style="margin-left:220px"><span class=\"ok\">Submit</span></button>\
			    <button type=\"button\" class=\"yo-small yo-button\" id=\"excel_rpt_event\"><span class=\"report\">Report</span></button>\
			     </div>\
			</div>\
                        </form>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div  class="legend">Groups</div>\
				<div id="groupsList">\
				<ul id="GroupsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
			<div class="detailPanel">\
			    <fieldset class="themeFieldset">\
				<div  class="legend">Hosts</div>\
				<div id="hostsList">\
				<ul id="HostsList" class="yo-ul">\
				</ul>\
				</div>\
			    </fieldset>\
			</div>\
                        <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id="total_header" min-height="20px" style=\"display: none;\">\
		            	<tr>\
		                <th id=\"form_title\" class=\"cell-title\">TRAP Data:</th>\
		            	</tr>\
                	</table>\
			<table class="display" name="total_report_table" id="total_report_table" width="100%%" style=\"display: none;\">\
			</table>' % (oday, otime, cday, ctime)
            return html_view

        except Exception, e:
            return str(e)

    @staticmethod
    def invetory_view2():
        html_view = ""\
            "<div class=\"form-div\">"\
            "<table cellspacing=\"0\" cellpadding=\"0\" width=\"100%\" class=\"tt-table\"><tbody><tr><th class=\"cell-title\" >Active Host</th></tr></tbody></table>"\
            "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_active_host\"></table>"\
            "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_active_host\" style=\"text-align:center;\">\
                    <thead><tr><th></th><th></th><th>Host Name</th>\
                    <th>Host Alias</th>\
                    <th>IP Address</th>\
                    <th>Device Type</th>\
                    <th>MAC Address</th>\
                    <th></th></tr></thead>\
                    </table>"
        "<table cellspacing=\"0\" cellpadding=\"0\" width=\"100%\" style=\"margin-top:15px;\" class=\"tt-table\"><tbody><tr><th class=\"cell-title\" >Disabled Host</th></tr></tbody></table>"\
        "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_disable_host\"></table>"\
        "<table cellspacing=\"0\" cellpadding=\"0\" width=\"100%\" style=\"margin-top:15px;\" class=\"tt-table\"><tbody><tr><th class=\"cell-title\" >Discovered Host</th></tr></tbody></table>"\
        "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_discovered_host\"></table>"\
        "<table cellspacing=\"0\" cellpadding=\"0\" width=\"100%\" style=\"margin-top:15px;\" class=\"tt-table\"><tbody><tr><th class=\"cell-title\" >Deleted Host</th></tr></tbody></table>"\
        "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_deleted_host\"></table>"\
        "</div>"\
        "<div class=\"form-div-footer\">"\
        "<button id=\"excel_rpt_inventory\" class=\"yo-small yo-button\" type=\"button\" onclick=\"inventory_report();\"><span class=\"report\">Report</span></button>"\
        "</div>"
        return html_view

    @staticmethod
    def invetory_view():
        html_view = ""\
            "<div id=\"grid_view_div\" class=\"form-div\">"\
            "<div class=\"yo-tabs\" id=\"main_grid_view_div\">"\
            "<ul>"\
            "<li>"\
            "<a class=\"active\" href=\"#content_1\" id=\"active_host_tab\">Enabled Host</a>"\
            "</li>"\
            "<li>"\
            "<a href=\"#content_2\" id=\"disable_host_tab\">Disabled Host</a>"\
            "</li>"\
            "<li>"\
            "<a href=\"#content_3\" id=\"discovered_host_tab\">Discovered Host</a>"\
            "</li>"\
            "<li>"\
            "<a href=\"#content_4\" id=\"deleted_host_tab\">Deleted Host</a>"\
            "</li>"\
            "</ul>"\
            "<div id=\"content_1\" class=\"tab-content\" style=\"display:block;height:100%;\">"\
            "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_active_host\" style=\"text-align:center;width:100%\">\
			<thead><tr><th></th><th></th>\
			<th>Host Alias</th>\
			<th>IP Address</th>\
			<th>Device Type</th>\
			<th>MAC Address</th>\
			<th></th></tr></thead>\
			</table>"\
            "</div>"\
            "<div id=\"content_2\" class=\"tab-content\">"\
            "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_disable_host\" style=\"text-align:center;width:100%\">\
			<thead><tr><th></th><th></th>\
			<th>Host Alias</th>\
			<th>IP Address</th>\
			<th>Device Type</th>\
			<th>MAC Address</th>\
			<th></th></tr></thead>\
			</table>"\
            "</div>"\
            "<div id=\"content_3\" class=\"tab-content\">"\
            "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_discovered_host\" style=\"text-align:center;width:100%\">\
			<thead><tr><th></th><th>Discovery Type</th>\
			<th>IP Address</th>\
			<th>MAC Address</th>\
			<th>Type</th>\
			<th>Discovery Time</th>\
			</tr></thead>\
			</table>"\
            "</div>"\
            "<div id=\"content_4\" class=\"tab-content\">"\
            "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_deleted_host\" style=\"text-align:center;width:100%\">\
			<thead><tr><th></th><th></th>\
			<th>Host Alias</th>\
			<th>IP Address</th>\
			<th>Device Type</th>\
			<th>MAC Address</th>\
			<th>Deleted by</th>\
			<th>Deleted Time</th>\
			</tr></thead>\
			</table>"\
            "</div>"\
            "</div>"\
            "</div>"\
            "<div class=\"form-div-footer\">"\
            "<button id=\"excel_rpt_inventory\" class=\"yo-small yo-button\" type=\"button\" onclick=\"inventory_report();\"><span class=\"report\">Report</span></button>"\
            "</div>"
        return html_view

    @staticmethod
    def page_tip_crc_phy():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>CRC PHY ERROR REPORT</h1>"\
            "<div><strong></strong> This page generates reports for CRC/ PHY Errors occurring while communication.</div>"\
            "<br/>"\
            "<div>On this page you can View reports for different date and time periods .</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"submit\" class=\"yo-small yo-button\"><span class=\"ok\">Submit</span></button> Click here to submit the data.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">Report</span></button>Click here to download the report in EXCEL format.</div></div>"\
            "<div><strong>Note:</strong> You can't choose dates greater than current date and start date sould be less than end date.</div>"\
            "<br/>"\
            "<div><b>Group Name</b>: This search box search the result on group name bases.</div>"\
            "<br/>"\
            "<div><b>Host Name</b>: This search box search the result on IP address,Host name or MAC address bases.</div>"\
            "<br/>"\
            "<div><b>No of device</b>:This provide the result on no of devices and you can adjust the no of devices value,default value is 10 .</div>"\
            "<br/>"\
            "<div><b>Important</b>: If you used searching for information(report) so you get information(report) on search based result instead of no of devices else you get result on no of devices bases.</div>"\
            "</div>"
        return html_view

    @staticmethod
    def page_tip_rssi():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>RSSI REPORT</h1>"\
            "<div><strong></strong> This page generates reports for RSSI Errors occurring while communication.</div>"\
            "<br/>"\
            "<div>On this page you can View reports for different date and time periods .</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"submit\" class=\"yo-small yo-button\"><span class=\"ok\">Submit</span></button> Click here to submit the data.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">Report</span></button>Click here to download the report in EXCEL format.</div></div>"\
            "<div><strong>Note:</strong> You can't choose dates greater than current date and start date sould be less than end date.</div>"\
            "<br/>"\
            "<div><b>Group Name</b>: This search box search the result on group name bases.</div>"\
            "<br/>"\
            "<div><b>Host Name</b>: This search box search the result on IP address,Host name or MAC address bases.</div>"\
            "<br/>"\
            "<div><b>No of device</b>:This provide the result on no of devices and you can adjust the no of devices value,default value is 10 .</div>"\
            "<br/>"\
            "<div><b>Important</b>: If you used searching for information(report) so you get information(report) on search based result instead of no of devices else you get result on no of devices bases.</div>"\
            "</div>"
        return html_view

    @staticmethod
    def page_tip_network_usage():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>NETWORK USAGE REPORT</h1>"\
            "<div><strong></strong> This page generates reports for Network Usage.</div>"\
            "<br/>"\
            "<div>On this page you can View reports for different date and time periods .</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"submit\" class=\"yo-small yo-button\"><span class=\"ok\">Submit</span></button> Click here to submit the data.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">Report</span></button>Click here to download the report in EXCEL format.</div></div>"\
            "<div><strong>Note:</strong> You can't choose dates greater than current date and start date sould be less than end date.</div>"\
            "<br/>"\
            "<div><b>Group Name</b>: This search box search the result on group name bases.</div>"\
            "<br/>"\
            "<div><b>Host Name</b>: This search box search the result on IP address,Host name or MAC address bases.</div>"\
            "<br/>"\
            "<div><b>No of device</b>:This provide the result on no of devices and you can adjust the no of devices value,default value is 10 .</div>"\
            "<br/>"\
            "<div><b>Important</b>: If you used searching for information(report) so you get information(report) on search based result instead of no of devices else you get result on no of devices bases.</div>"\
            "</div>"
        return html_view

    @staticmethod
    def page_tip_network_outage():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>NETWORK OUTAGE REPORT</h1>"\
            "<div><strong></strong> This page generates reports for Network Outage.</div>"\
            "<br/>"\
            "<div>On this page you can View reports for different date and time periods .</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"submit\" class=\"yo-small yo-button\"><span class=\"ok\">Submit</span></button> Click here to submit the data.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">Report</span></button>Click here to download the report in EXCEL format.</div></div>"\
            "<div><strong>Note:</strong> You can't choose dates greater than current date and start date sould be less than end date.</div>"\
            "<br/>"\
            "<div><b>Group Name</b>: This search box search the result on group name bases.</div>"\
            "<br/>"\
            "<div><b>Host Name</b>: This search box search the result on IP address,Host name or MAC address bases.</div>"\
            "<br/>"\
            "<div><b>No of device</b>:This provide the result on no of devices and you can adjust the no of devices value,default value is 10 .</div>"\
            "<br/>"\
            "<div><b>Important</b>: If you used searching for information(report) so you get information(report) on search based result instead of no of devices else you get result on no of devices bases.</div>"\
            "</div>"
        return html_view

    @staticmethod
    def page_tip_trap():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>EVENTS REPORT</h1>"\
            "<div><strong></strong> This page generates reports for Events occurring while communication.</div>"\
            "<br/>"\
            "<div>On this page you can View reports for different date and time periods .</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"submit\" class=\"yo-small yo-button\"><span class=\"ok\">Submit</span></button> Click here to submit the data.</div></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">Report</span></button>Click here to download the report in EXCEL format.</div></div>"\
            "<div><strong>Note:</strong> You can't choose dates greater than current date and start date sould be less than end date.</div>"\
            "<br/>"\
            "<div><b>Group Name</b>: This search box search the result on group name bases.</div>"\
            "<br/>"\
            "<div><b>Host Name</b>: This search box search the result on IP address,Host name or MAC address bases.</div>"\
            "<br/>"\
            "<div><b>No of device</b>:This provide the result on no of devices and you can adjust the no of devices value,default value is 10 .</div>"\
            "<br/>"\
            "<div><b>Important</b>: If you used searching for information(report) so you get information(report) on search based result instead of no of devices else you get result on no of devices bases.</div>"\
            "</div>"
        return html_view

    @staticmethod
    def page_tip_for_inventory():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>INVENTORY REPORT</h1>"\
            "<div><strong></strong> This page generates reports for Inventory like enabled hosts,disabled hosts,discovered hosts and deleted host.</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"txt-div\"><button type=\"button\" class=\"yo-small yo-button\"><span class=\"report\">Report</span></button>Click here to download the report in EXCEL format.</div></div>"\
            "<div><strong>Note:</strong>This page provide the information for <b>Enabled Hosts, Disabled Hosts,Discovered Hosts and Deleted Hosts </b> .</div>"\
            "<br/>"\
            "</div>"
        return html_view
