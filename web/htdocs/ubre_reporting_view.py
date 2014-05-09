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
    def ubre_create_crc_phy_form():
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
            <form name="get_reporting_data" id="get_reporting_data" action="ubre_get_crc_phy_data.py" method=\"get\">\
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
    def ubre_create_rssi_form():
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
			<form name="get_reporting_data" id="get_reporting_data" action="ubre_get_rssi_data.py" method=\"get\">\
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
    def ubre_create_network_usage_form():
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
			<form name="get_reporting_data" id="get_reporting_data" action="ubre_get_network_usage_data.py" method=\"get\">\
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
            #
            # @staticmethod
            # def ubre_page_tip_crc_phy():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/ubre_page_tip_crc_phy.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def ubre_page_tip_rssi():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/ubre_page_tip_rssi.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def ubre_page_tip_network_usage():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/ubre_page_tip_network_usage.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
