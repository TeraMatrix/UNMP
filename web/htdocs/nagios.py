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


class Nagios(object):
    """
    UNMP Core related class
    """
    @staticmethod
    def advanced_host_settings(result={}):
        """

        @param result:
        @return:
        """
        try:

            service_dict = {}
            service_dict['snmp_uptime'] = result.get(
                'snmp_uptime', ['', '', ''])
            service_dict['statistics_service'] = result.get(
                'statistics_service', ['', '', ''])
            html_view = ['<div style=\"width:98%%\">\
			<div class=\"row-elem\"><h3>Uptime service(Heartbeat Rate):</h3></div>\
			<div class=\"row-elem\">\
				<label class=\"lbl lbl-big\" for=\"advanced_max_check_attempts_snmp_uptime\">max check attempts</label>\
				<input type=\"text\" id=\"advanced_max_check_attempts_snmp_uptime\" name=\"advanced_max_check_attempts_snmp_uptime\" value=\"%s\" />' % (
            str(service_dict["snmp_uptime"][0]))]
            html_view.append('</div>\
			<div class=\"row-elem\">\
			   	<label class=\"lbl lbl-big\" style="width:100px;margin-right:57px" >service check time:</label>\
			   	<select name="advanced_check_interval_snmp_uptime" id="advanced_check_interval_snmp_uptime" class="multiselect" title="Click to select an option">')
            html_view.append(
                '<option value=' + str(service_dict["snmp_uptime"][1]) + '>' + str(service_dict["snmp_uptime"][1]) + ' mins</option>\
					<option value=1>1 mins</option>\
					<option value=5>5 mins</option>\
					<option value=10>10 mins</option>\
					<option value=15>15 mins</option>\
					<option value=30>30 mins</option>\
					<option value=45>45 mins</option>\
					<option value=60>60 mins</option>\
					<option value=720>12 Hours</option>\
					<option value=1440>Daily</option>\
					<option value=43200>Monthly</option>\
					<option value=518400>Yearly</option>\
				</select>\
			</div>\
			<div class=\"row-elem\">\
			   	<label class=\"lbl lbl-big\" style="width:100px;margin-right:57px" >service retry time:</label>\
			   	<select name="advanced_retry_interval_snmp_uptime" id="advanced_retry_interval_snmp_uptime" class="multiselect" title="Click to select an option">')
            html_view.append(
                '<option value=' + str(service_dict["snmp_uptime"][2]) + '>' + str(service_dict["snmp_uptime"][2]) + ' mins</option>\
					<option value=1>1 mins</option>\
					<option value=5>5 mins</option>\
					<option value=10>10 mins</option>\
					<option value=15>15 mins</option>\
					<option value=30>30 mins</option>\
					<option value=45>45 mins</option>\
					<option value=60>60 mins</option>\
					<option value=720>12 Hours</option>\
					<option value=1440>Daily</option>\
					<option value=43200>Monthly</option>\
					<option value=518400>Yearly</option>\
				</select>\
			</div>\
			<div class=\"row-elem\"><h3>Statistics service:</h3></div>\
			<div class=\"row-elem\">\
				<label class=\"lbl lbl-big\" for=\"advanced_max_check_attempts_statistics_service\">max check attempts</label>')

            html_view.append(
                '<input type=\"text\" id=\"advanced_max_check_attempts_statistics_service\" name=\"advanced_max_check_attempts_statistics_service\" value=\"%s\" />' % (
                str(service_dict["statistics_service"][0])))
            html_view.append('</div>\
			<div class=\"row-elem\">\
			   	<label class=\"lbl lbl-big\" style="width:100px;margin-right:57px" >service check time:</label>\
			   	<select name="advanced_check_interval_statistics_service" id="advanced_check_interval_statistics_service" class="multiselect" title="Click to select an option">')

            html_view.append('<option value=' + str(service_dict["statistics_service"][1]) + '>' + str(
                service_dict["statistics_service"][1]) + ' mins</option>\
					<option value=5>5 mins</option>\
					<option value=10>10 mins</option>\
					<option value=15>15 mins</option>\
					<option value=30>30 mins</option>\
					<option value=45>45 mins</option>\
					<option value=60>60 mins</option>\
					<option value=720>12 Hours</option>\
					<option value=1440>Daily</option>\
					<option value=43200>Monthly</option>\
					<option value=518400>Yearly</option>\
				</select>\
			</div>\
			<div class=\"row-elem\">\
			   	<label class=\"lbl lbl-big\" style="width:100px;margin-right:57px" >service retry time:</label>\
			   	<select name="advanced_retry_interval_statistics_service" id="advanced_retry_interval_statistics_service" class="multiselect" title="Click to select an option">')

            html_view.append('<option value=' + str(service_dict["statistics_service"][2]) + '>' + str(
                service_dict["statistics_service"][2]) + ' mins</option>\
					<option value=5>5 mins</option>\
					<option value=10>10 mins</option>\
					<option value=15>15 mins</option>\
					<option value=30>30 mins</option>\
					<option value=45>45 mins</option>\
					<option value=60>60 mins</option>\
					<option value=720>12 Hours</option>\
					<option value=1440>Daily</option>\
					<option value=43200>Monthly</option>\
					<option value=518400>Yearly</option>\
				</select>\
			</div>\
			<button type=\"button\" class=\"yo-small yo-button\" id=\"apply_advanced_host_settings\"><span class=\"edit\">Apply</span></button>\
			<button type=\"button\" class=\"yo-small yo-button\" id=\"close_advanced_host_settings\"><span class=\"cancel\">Cancel</span></button></div>')

            return ''.join(html_view)
        except Exception, e:
            return str(e)

    @staticmethod
    def main_menu():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_hosts\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"host_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"25%\"/>\
			<col width=\"25%\"/>\
			<col width=\"25%\"/>\
			<col width=\"20%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th>Host name</th> \
			<th>Host alias</th> \
			<th>IP Address</th> \
			<th>Parent</th> \
			<th>Hostgroup</th> \
			<th>Action</th> \
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_host.py\" method=\"get\" id=\"edit_nagios_host_form\" name=\"edit_nagios_host_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit Host</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
		        <input type=\"text\" id=\"old_ip_address\" name=\"old_ip_address\" value=\"\" style=\"display:none\" />\
		        <input type=\"text\" id=\"old_host_alias\" name=\"old_host_alias\" value=\"\" style=\"display:none\" />\
			<input type=\"text\" id=\"old_hostgroup\" name=\"old_hostgroup\" value=\"\" style=\"display:none\" />\
			<input type=\"text\" id=\"host_name\" name=\"host_name\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"alias\">Host alias</label>\
                        <input type=\"text\" id=\"alias\" name=\"alias\" readonly=\"readonly\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"address\">IP address</label>\
                        <input type=\"text\" id=\"address\" name=\"address\" readonly=\"readonly\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"hostgroups\">hostgroups</label>\
                        <select name="hostgroups" id="hostgroups" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_period\">check period</label>\
                        <select name="check_period" id="check_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"use\">host templates</label>\
                        <div id="more_options_columns" style="margin-top:10px;"></div>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contact_groups\">contact groups</label>\
                        <select name="contact_groups" id="contact_groups" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contacts\">contacts</label>\
                        <select name="contacts" id="contacts" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"parents\">Parents</label>\
                        <select name="parents" id="parents" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes\">notes</label>\
                        <input type=\"text\" id=\"notes\" name=\"notes\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes_url\">notes url</label>\
                        <input type=\"text\" id=\"notes_url\" name=\"notes_url\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"action_url\">action url</label>\
                        <input type=\"text\" id=\"action_url\" name=\"action_url\" value=\"\" />\
                    </div>\
                    <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">\
                    <tr>\
                        <th class=\"cell-title\">check options host</th>\
                    </tr>\
                    </table>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_command\">check commands</label>\
                         <select name="check_command" id="check_command" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"max_check_attempts\">max check attempts</label>\
                        <input type=\"text\" id=\"max_check_attempts\" name=\"max_check_attempts\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_interval\">check interval</label>\
                        <input type=\"text\" id=\"check_interval\" name=\"check_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retry_interval\">retry interval</label>\
                        <input type=\"text\" id=\"retry_interval\" name=\"retry_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notifications_enabled\">notification enabled</label>\
                        <select name="notifications_enabled" id="notifications_enabled" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_period\">notification period</label>\
                        <select name="notification_period" id="notification_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_interval\">notification interval</label>\
                        <input type=\"text\" id=\"notification_interval\" name=\"notification_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_options\">notification options</label>\
                        <select name="notification_options" id="notification_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"initial_state\">initial state</label>\
                        <select name="initial_state" id="initial_state" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"first_notification_delay\">first notification delay</label>\
                        <input type=\"text\" id=\"first_notification_delay\" name=\"first_notification_delay\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"active_checks_enabled\">active checking</label>\
                        <select name="active_checks_enabled" id="active_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"passive_checks_enabled\">passive checking</label>\
                        <select name="passive_checks_enabled" id="passive_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler_enabled\">event handler enable</label>\
                        <select name="event_handler_enabled" id="event_handler_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler\">event handler</label>\
                        <input type=\"text\" id=\"event_handler\" name=\"event_handler\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_freshness\">check freshness</label>\
                        <select name="check_freshness" id="check_freshness" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"freshness_threshold\">freshness threshold</label>\
                        <input type=\"text\" id=\"freshness_threshold\" name=\"freshness_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"process_perf_data\">process performance data</label>\
                         <select name="process_perf_data" id="process_perf_data" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_enabled\">flap detection enabled</label>\
                        <select name="flap_detection_enabled" id="flap_detection_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_options\">flap detection options</label>\
                         <select name="flap_detection_options" id="flap_detection_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"high_flap_threshold\">high flap threshold</label>\
                        <input type=\"text\" id=\"high_flap_threshold\" name=\"high_flap_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"low_flap_threshold\">low flap threshold</label>\
                        <input type=\"text\" id=\"low_flap_threshold\" name=\"low_flap_threshold\" value=\"\" />\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_host\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_host\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_host_inventory():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_hosts\" style=\"display:none\"/>\
	     <form  action=\"save_nagios_edit_host.py\" method=\"get\" id=\"edit_nagios_host_form\" name=\"edit_nagios_host_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit Host</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
		        <input type=\"text\" id=\"old_ip_address\" name=\"old_ip_address\" value=\"\" style=\"display:none\" />\
		        <input type=\"text\" id=\"old_host_alias\" name=\"old_host_alias\" value=\"\" style=\"display:none\" />\
			<input type=\"text\" id=\"old_hostgroup\" name=\"old_hostgroup\" value=\"\" style=\"display:none\" />\
			<input type=\"text\" id=\"host_name\" name=\"host_name\" value=\"\" style=\"display:none\" />\
			<input type=\"text\" id=\"address\" name=\"address\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"alias\">Host alias</label>\
                        <input type=\"text\" id=\"alias\" name=\"alias\" value=\"\" readonly=\"readonly\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_period\">check period</label>\
                        <select name="check_period" id="check_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"use\">host templates</label>\
                        <div id="more_options_columns" style="margin-top:10px;"></div>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contact_groups\">contact groups</label>\
                        <select name="contact_groups" id="contact_groups" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contacts\">contacts</label>\
                        <select name="contacts" id="contacts" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes\">notes</label>\
                        <input type=\"text\" id=\"notes\" name=\"notes\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes_url\">notes url</label>\
                        <input type=\"text\" id=\"notes_url\" name=\"notes_url\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"action_url\">action url</label>\
                        <input type=\"text\" id=\"action_url\" name=\"action_url\" value=\"\" />\
                    </div>\
                    <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">\
                    <tr>\
                        <th class=\"cell-title\">check options host</th>\
                    </tr>\
                    </table>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_command\">check commands</label>\
                         <select name="check_command" id="check_command" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"max_check_attempts\">max check attempts</label>\
                        <input type=\"text\" id=\"max_check_attempts\" name=\"max_check_attempts\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_interval\">check interval</label>\
                        <input type=\"text\" id=\"check_interval\" name=\"check_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retry_interval\">retry interval</label>\
                        <input type=\"text\" id=\"retry_interval\" name=\"retry_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notifications_enabled\">notification enabled</label>\
                        <select name="notifications_enabled" id="notifications_enabled" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_period\">notification period</label>\
                        <select name="notification_period" id="notification_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_interval\">notification interval</label>\
                        <input type=\"text\" id=\"notification_interval\" name=\"notification_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_options\">notification options</label>\
                        <select name="notification_options" id="notification_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"initial_state\">initial state</label>\
                        <select name="initial_state" id="initial_state" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"first_notification_delay\">first notification delay</label>\
                        <input type=\"text\" id=\"first_notification_delay\" name=\"first_notification_delay\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"active_checks_enabled\">active checking</label>\
                        <select name="active_checks_enabled" id="active_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"passive_checks_enabled\">passive checking</label>\
                        <select name="passive_checks_enabled" id="passive_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler_enabled\">event handler enable</label>\
                        <select name="event_handler_enabled" id="event_handler_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler\">event handler</label>\
                        <input type=\"text\" id=\"event_handler\" name=\"event_handler\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_freshness\">check freshness</label>\
                        <select name="check_freshness" id="check_freshness" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"freshness_threshold\">freshness threshold</label>\
                        <input type=\"text\" id=\"freshness_threshold\" name=\"freshness_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"process_perf_data\">process performance data</label>\
                         <select name="process_perf_data" id="process_perf_data" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_enabled\">flap detection enabled</label>\
                        <select name="flap_detection_enabled" id="flap_detection_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_options\">flap detection options</label>\
                         <select name="flap_detection_options" id="flap_detection_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"high_flap_threshold\">high flap threshold</label>\
                        <input type=\"text\" id=\"high_flap_threshold\" name=\"high_flap_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"low_flap_threshold\">low flap threshold</label>\
                        <input type=\"text\" id=\"low_flap_threshold\" name=\"low_flap_threshold\" value=\"\" />\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_host\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_host\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_host_template():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_host_template\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"host_template_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"25%\"/>\
			<col width=\"20%\"/>\
			<col width=\"20%\"/>\
			<col width=\"30%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th>Template name</th> \
			<th>Notification Interval</th> \
			<th>Max check attempts</th> \
			<th>Check command</th> \
			<th>Action</th> \
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_host_template.py\" method=\"get\" id=\"edit_nagios_host_template_form\" name=\"edit_nagios_host_template_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit Host template</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
			<input type=\"text\" id=\"old_host_template_name\" name=\"old_host_template_name\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"name\">Template name</label>\
                        <input type=\"text\" id=\"name\" name=\"name\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"register\">Register</label>\
                        <select name="register" id="register" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"hostgroups\">hostgroups</label>\
                        <select name="hostgroups" id="hostgroups" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_period\">check period</label>\
                        <select name="check_period" id="check_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"use\">host templates</label>\
                        <div id="more_options_columns" style="margin-top:10px;"></div>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contact_groups\">contact groups</label>\
                        <select name="contact_groups" id="contact_groups" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contacts\">contacts</label>\
                        <select name="contacts" id="contacts" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"parents\">Parents</label>\
                        <select name="parents" id="parents" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes\">notes</label>\
                        <input type=\"text\" id=\"notes\" name=\"notes\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes_url\">notes url</label>\
                        <input type=\"text\" id=\"notes_url\" name=\"notes_url\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"action_url\">action url</label>\
                        <input type=\"text\" id=\"action_url\" name=\"action_url\" value=\"\" />\
                    </div>\
                    <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">\
                    <tr>\
                        <th class=\"cell-title\">check options host</th>\
                    </tr>\
                    </table>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_command\">check commands</label>\
                        <select name="check_command" id="check_command" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"max_check_attempts\">max check attempts</label>\
                        <input type=\"text\" id=\"max_check_attempts\" name=\"max_check_attempts\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_interval\">check interval</label>\
                        <input type=\"text\" id=\"check_interval\" name=\"check_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retry_interval\">retry interval</label>\
                        <input type=\"text\" id=\"retry_interval\" name=\"retry_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notifications_enabled\">notification enabled</label>\
                        <select name="notifications_enabled" id="notifications_enabled" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_period\">notification period</label>\
                        <select name="notification_period" id="notification_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_interval\">notification interval</label>\
                        <input type=\"text\" id=\"notification_interval\" name=\"notification_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_options\">notification options</label>\
                        <select name="notification_options" id="notification_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"initial_state\">initial state</label>\
                        <select name="initial_state" id="initial_state" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"first_notification_delay\">first notification delay</label>\
                        <input type=\"text\" id=\"first_notification_delay\" name=\"first_notification_delay\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"active_checks_enabled\">active checking</label>\
                        <select name="active_checks_enabled" id="active_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"passive_checks_enabled\">passive checking</label>\
                        <select name="passive_checks_enabled" id="passive_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler_enabled\">event handler enable</label>\
                        <select name="event_handler_enabled" id="event_handler_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler\">event handler</label>\
                        <input type=\"text\" id=\"event_handler\" name=\"event_handler\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_freshness\">check freshness</label>\
                        <select name="check_freshness" id="check_freshness" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"freshness_threshold\">freshness threshold</label>\
                        <input type=\"text\" id=\"freshness_threshold\" name=\"freshness_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"process_perf_data\">process performance data</label>\
                         <select name="process_perf_data" id="process_perf_data" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_enabled\">flap detection enabled</label>\
                        <select name="flap_detection_enabled" id="flap_detection_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_options\">flap detection options</label>\
                         <select name="flap_detection_options" id="flap_detection_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"high_flap_threshold\">high flap threshold</label>\
                        <input type=\"text\" id=\"high_flap_threshold\" name=\"high_flap_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"low_flap_threshold\">low flap threshold</label>\
                        <input type=\"text\" id=\"low_flap_threshold\" name=\"low_flap_threshold\" value=\"\" />\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_host_template\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_host_template\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_service():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_service\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"service_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"25%\"/>\
			<col width=\"25%\"/>\
			<col width=\"25%\"/>\
			<col width=\"20%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th></th> \
			<th>service name</th> \
			<th>use</th> \
			<th>host alias</th> \
			<th>normal check interval</th> \
			<th>actions</th>\
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_service.py\" method=\"get\" id=\"edit_nagios_service_form\" name=\"edit_nagios_service_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit service</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
                 <input type=\"text\" id=\"service_unique_key\" name=\"service_unique_key\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"service_description\">service description</label>\
                        <input type=\"text\" id=\"service_description\" name=\"service_description\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"display_name\">display name</label>\
                        <input type=\"text\" id=\"display_name\" name=\"display_name\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"hostgroups\">hostgroups</label>\
                        <select name="hostgroups" id="hostgroups" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"host_name\">hosts</label>\
                        <select name="host_name" id="host_name" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_period\">check period</label>\
                        <select name="check_period" id="check_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"use\">service templates</label>\
                        <div id="more_options_columns" style="margin-top:10px;"></div>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contact_groups\">contact groups</label>\
                        <select name="contact_groups" id="contact_groups" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contacts\">contacts</label>\
                        <select name="contacts" id="contacts" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes\">notes</label>\
                        <input type=\"text\" id=\"notes\" name=\"notes\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes_url\">notes url</label>\
                        <input type=\"text\" id=\"notes_url\" name=\"notes_url\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"action_url\">action url</label>\
                        <input type=\"text\" id=\"action_url\" name=\"action_url\" value=\"\" />\
                    </div>\
                    <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">\
                    <tr>\
                        <th class=\"cell-title\">check options service</th>\
                    </tr>\
                    </table>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_command\">check commands</label>\
                        <input type=\"text\" id=\"check_command\" name=\"check_command\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"max_check_attempts\">max check attempts</label>\
                        <input type=\"text\" id=\"max_check_attempts\" name=\"max_check_attempts\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"normal_check_interval\">check interval</label>\
                        <input type=\"text\" id=\"normal_check_interval\" name=\"normal_check_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retry_interval\">retry interval</label>\
                        <input type=\"text\" id=\"retry_interval\" name=\"retry_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notifications_enabled\">notification enabled</label>\
                        <select name="notifications_enabled" id="notifications_enabled" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_period\">notification period</label>\
                        <select name="notification_period" id="notification_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_interval\">notification interval</label>\
                        <input type=\"text\" id=\"notification_interval\" name=\"notification_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_options\">notification options</label>\
                        <select name="notification_options" id="notification_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"initial_state\">initial state</label>\
                        <select name="initial_state" id="initial_state" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"first_notification_delay\">first notification delay</label>\
                        <input type=\"text\" id=\"first_notification_delay\" name=\"first_notification_delay\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"active_checks_enabled\">active checking</label>\
                        <select name="active_checks_enabled" id="active_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"passive_checks_enabled\">passive checking</label>\
                        <select name="passive_checks_enabled" id="passive_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler_enabled\">event handler enable</label>\
                        <select name="event_handler_enabled" id="event_handler_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler\">event handler</label>\
                        <input type=\"text\" id=\"event_handler\" name=\"event_handler\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_freshness\">check freshness</label>\
                        <select name="check_freshness" id="check_freshness" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"freshness_threshold\">freshness threshold</label>\
                        <input type=\"text\" id=\"freshness_threshold\" name=\"freshness_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"process_perf_data\">process performance data</label>\
                         <select name="process_perf_data" id="process_perf_data" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_enabled\">flap detection enabled</label>\
                        <select name="flap_detection_enabled" id="flap_detection_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_options\">flap detection options</label>\
                         <select name="flap_detection_options" id="flap_detection_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"high_flap_threshold\">high flap threshold</label>\
                        <input type=\"text\" id=\"high_flap_threshold\" name=\"high_flap_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"low_flap_threshold\">low flap threshold</label>\
                        <input type=\"text\" id=\"low_flap_threshold\" name=\"low_flap_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"parallelize_check\">parallelize check</label>\
                         <select name="parallelize_check" id="parallelize_check" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"failure_prediction_enabled\">failure prediction enabled</label>\
                         <select name="failure_prediction_enabled" id="failure_prediction_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"stalking_options\">stalking options</label>\
                         <select name="stalking_options" id="stalking_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retain_status_information\">retain status information</label>\
                         <select name="retain_status_information" id="retain_status_information" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retain_nonstatus_information\">retain nonstatus information</label>\
                         <select name="retain_nonstatus_information" id="retain_nonstatus_information" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"obsess_over_service\">obsess over service</label>\
                         <select name="obsess_over_service" id="obsess_over_service" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"is_volatile\">is volatile</label>\
                         <select name="is_volatile" id="is_volatile" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_service\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_service\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_service_template():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_service_template\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"service_template_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"25%\"/>\
			<col width=\"20%\"/>\
			<col width=\"20%\"/>\
			<col width=\"30%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th>Template name</th> \
			<th>Notification Interval</th> \
			<th>Max check attempts</th> \
			<th>Check command</th> \
			<th>Action</th> \
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_service_template.py\" method=\"get\" id=\"edit_nagios_service_template_form\" name=\"edit_nagios_service_template_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit service template</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
                 <input type=\"text\" id=\"service_unique_key\" name=\"service_unique_key\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"name\">name</label>\
                        <input type=\"text\" id=\"name\" name=\"name\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"register\">register</label>\
                         <select name="register" id="register" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"hostgroups\">hostgroups</label>\
                        <select name="hostgroups" id="hostgroups" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"host_name\">hosts</label>\
                        <select name="host_name" id="host_name" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_period\">check period</label>\
                        <select name="check_period" id="check_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"use\">service templates</label>\
                         <div id="more_options_columns" style="margin-top:10px;"></div>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contact_groups\">contact groups</label>\
                        <select name="contact_groups" id="contact_groups" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contacts\">contacts</label>\
                        <select name="contacts" id="contacts" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes\">notes</label>\
                        <input type=\"text\" id=\"notes\" name=\"notes\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes_url\">notes url</label>\
                        <input type=\"text\" id=\"notes_url\" name=\"notes_url\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"action_url\">action url</label>\
                        <input type=\"text\" id=\"action_url\" name=\"action_url\" value=\"\" />\
                    </div>\
                    <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">\
                    <tr>\
                        <th class=\"cell-title\">check options service</th>\
                    </tr>\
                    </table>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_command\">check commands</label>\
                        <input type=\"text\" id=\"check_command\" name=\"check_command\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"max_check_attempts\">max check attempts</label>\
                        <input type=\"text\" id=\"max_check_attempts\" name=\"max_check_attempts\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"normal_check_interval\">check interval</label>\
                        <input type=\"text\" id=\"normal_check_interval\" name=\"normal_check_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retry_interval\">retry interval</label>\
                        <input type=\"text\" id=\"retry_interval\" name=\"retry_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notifications_enabled\">notification enabled</label>\
                        <select name="notifications_enabled" id="notifications_enabled" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_period\">notification period</label>\
                        <select name="notification_period" id="notification_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_interval\">notification interval</label>\
                        <input type=\"text\" id=\"notification_interval\" name=\"notification_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_options\">notification options</label>\
                        <select name="notification_options" id="notification_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"initial_state\">initial state</label>\
                        <select name="initial_state" id="initial_state" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"first_notification_delay\">first notification delay</label>\
                        <input type=\"text\" id=\"first_notification_delay\" name=\"first_notification_delay\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"active_checks_enabled\">active checking</label>\
                        <select name="active_checks_enabled" id="active_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"passive_checks_enabled\">passive checking</label>\
                        <select name="passive_checks_enabled" id="passive_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler_enabled\">event handler enable</label>\
                        <select name="event_handler_enabled" id="event_handler_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler\">event handler</label>\
                        <input type=\"text\" id=\"event_handler\" name=\"event_handler\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_freshness\">check freshness</label>\
                        <select name="check_freshness" id="check_freshness" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"freshness_threshold\">freshness threshold</label>\
                        <input type=\"text\" id=\"freshness_threshold\" name=\"freshness_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"process_perf_data\">process performance data</label>\
                         <select name="process_perf_data" id="process_perf_data" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_enabled\">flap detection enabled</label>\
                        <select name="flap_detection_enabled" id="flap_detection_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_options\">flap detection options</label>\
                         <select name="flap_detection_options" id="flap_detection_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"high_flap_threshold\">high flap threshold</label>\
                        <input type=\"text\" id=\"high_flap_threshold\" name=\"high_flap_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"low_flap_threshold\">low flap threshold</label>\
                        <input type=\"text\" id=\"low_flap_threshold\" name=\"low_flap_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"parallelize_check\">parallelize check</label>\
                         <select name="parallelize_check" id="parallelize_check" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"failure_prediction_enabled\">failure prediction enabled</label>\
                         <select name="failure_prediction_enabled" id="failure_prediction_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"stalking_options\">stalking options</label>\
                         <select name="stalking_options" id="stalking_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retain_status_information\">retain status information</label>\
                         <select name="retain_status_information" id="retain_status_information" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retain_nonstatus_information\">retain nonstatus information</label>\
                         <select name="retain_nonstatus_information" id="retain_nonstatus_information" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"obsess_over_service\">obsess over service</label>\
                         <select name="obsess_over_service" id="obsess_over_service" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"is_volatile\">is volatile</label>\
                         <select name="is_volatile" id="is_volatile" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_service_template\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_service_template\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_hostgroup():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_hostgroup\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"hostgroup_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"25%\"/>\
			<col width=\"25%\"/>\
			<col width=\"45%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th>Hostgroup name</th> \
			<th>Hostgroup alias</th> \
			<th>members</th> \
			<th>Action</th> \
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_hostgroup.py\" method=\"get\" id=\"edit_nagios_hostgroup_form\" name=\"edit_nagios_hostgroup_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit hostgroup</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
                        <input type=\"text\" id=\"hostgroup_name_unique\" name=\"hostgroup_name_unique\" value=\"\" style=\"display:none\" />\
                        <input type=\"text\" id=\"old_members\" name=\"old_members\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"hostgroup_name\">Hostgroup Name</label>\
                        <input type=\"text\" id=\"hostgroup_name\" name=\"hostgroup_name\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"members\">Members</label>\
                        <select name="members" id="members" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes\">notes</label>\
                        <input type=\"text\" id=\"notes\" name=\"notes\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes_url\">notes url</label>\
                        <input type=\"text\" id=\"notes_url\" name=\"notes_url\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"action_url\">action url</label>\
                        <input type=\"text\" id=\"action_url\" name=\"action_url\" value=\"\" />\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_hostgroup\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_hostgroup\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_hostgroup_inventory():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_hostgroup\" style=\"display:none\"/>\
	     <form action=\"save_nagios_hostgroup_inventory.py\" method=\"get\" id=\"edit_nagios_hostgroup_inventory_form\" name=\"edit_nagios_hostgroup_inventory_form\" >\
                <div class=\"form-div\">\
        		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
        		    <tr>\
        		        <th class=\"cell-title\">Edit hostgroup</th>\
        		    </tr>\
        		</table>\
                <div class=\"form-body\">\
                        <input type=\"text\" id=\"hostgroup_name_unique\" name=\"hostgroup_name_unique\" value=\"\" style=\"display:none\" />\
                        <input type=\"text\" id=\"old_members\" name=\"old_members\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"hostgroup_name\">Hostgroup Name</label>\
                        <input type=\"text\" id=\"hostgroup_name\" name=\"hostgroup_name\" readonly=\"readonly\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_period\">check period</label>\
                        <select name="check_period" id="check_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contact_groups\">contact groups</label>\
                        <select name="contact_groups" id="contact_groups" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"contacts\">contacts</label>\
                        <select name="contacts" id="contacts" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes\">notes</label>\
                        <input type=\"text\" id=\"notes\" name=\"notes\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes_url\">notes url</label>\
                        <input type=\"text\" id=\"notes_url\" name=\"notes_url\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"action_url\">action url</label>\
                        <input type=\"text\" id=\"action_url\" name=\"action_url\" value=\"\" />\
                    </div>\
                    <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">\
                    <tr>\
                        <th class=\"cell-title\">check options host</th>\
                    </tr>\
                    </table>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_command\">check commands</label>\
                         <select name="check_command" id="check_command" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"max_check_attempts\">max check attempts</label>\
                        <input type=\"text\" id=\"max_check_attempts\" name=\"max_check_attempts\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_interval\">check interval</label>\
                        <input type=\"text\" id=\"check_interval\" name=\"check_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"retry_interval\">retry interval</label>\
                        <input type=\"text\" id=\"retry_interval\" name=\"retry_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notifications_enabled\">notification enabled</label>\
                        <select name="notifications_enabled" id="notifications_enabled" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_period\">notification period</label>\
                        <select name="notification_period" id="notification_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_interval\">notification interval</label>\
                        <input type=\"text\" id=\"notification_interval\" name=\"notification_interval\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_options\">notification options</label>\
                        <select name="notification_options" id="notification_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"initial_state\">initial state</label>\
                        <select name="initial_state" id="initial_state" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"first_notification_delay\">first notification delay</label>\
                        <input type=\"text\" id=\"first_notification_delay\" name=\"first_notification_delay\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"active_checks_enabled\">active checking</label>\
                        <select name="active_checks_enabled" id="active_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"passive_checks_enabled\">passive checking</label>\
                        <select name="passive_checks_enabled" id="passive_checks_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler_enabled\">event handler enable</label>\
                        <select name="event_handler_enabled" id="event_handler_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"event_handler\">event handler</label>\
                        <input type=\"text\" id=\"event_handler\" name=\"event_handler\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"check_freshness\">check freshness</label>\
                        <select name="check_freshness" id="check_freshness" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"freshness_threshold\">freshness threshold</label>\
                        <input type=\"text\" id=\"freshness_threshold\" name=\"freshness_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"process_perf_data\">process performance data</label>\
                         <select name="process_perf_data" id="process_perf_data" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_enabled\">flap detection enabled</label>\
                        <select name="flap_detection_enabled" id="flap_detection_enabled" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"flap_detection_options\">flap detection options</label>\
                         <select name="flap_detection_options" id="flap_detection_options" class="multiselect" multiple="multiple" title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"high_flap_threshold\">high flap threshold</label>\
                        <input type=\"text\" id=\"high_flap_threshold\" name=\"high_flap_threshold\" value=\"\" />\
                    </div>\
                     <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"low_flap_threshold\">low flap threshold</label>\
                        <input type=\"text\" id=\"low_flap_threshold\" name=\"low_flap_threshold\" value=\"\" />\
                    </div>\
                </div>\
            </div>\
        <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_hostgroup_inventory\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_hostgroup_inventory\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view
        return html_view

    @staticmethod
    def main_menu_servicegroup():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_servicegroup\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"servicegroup_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"25%\"/>\
			<col width=\"25%\"/>\
			<col width=\"45%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th>Servicegroup name</th> \
			<th>Servicegroup alias</th> \
			<th>members</th> \
			<th>Action</th> \
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_servicegroup.py\" method=\"get\" id=\"edit_nagios_servicegroup_form\" name=\"edit_nagios_servicegroup_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit hostgroup</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
                        <input type=\"text\" id=\"servicegroup_name_unique\" name=\"servicegroup_name_unique\" value=\"\" style=\"display:none\" />\
                        <input type=\"text\" id=\"old_members\" name=\"old_members\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"servicegroup_name\">Servicegroup Name</label>\
                        <input type=\"text\" id=\"servicegroup_name\" name=\"servicegroup_name\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"alias\">servicegroup alias</label>\
                        <input type=\"text\" id=\"alias\" name=\"alias\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"members\">Members</label>\
                        <select name="members" id="members" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes\">notes</label>\
                        <input type=\"text\" id=\"notes\" name=\"notes\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notes_url\">notes url</label>\
                        <input type=\"text\" id=\"notes_url\" name=\"notes_url\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"action_url\">action url</label>\
                        <input type=\"text\" id=\"action_url\" name=\"action_url\" value=\"\" />\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_servicegroup\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_servicegroup\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_command():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_command\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"command_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"25%\"/>\
			<col width=\"70%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th>Command name</th> \
			<th>Command line</th> \
			<th>Action</th> \
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_command.py\" method=\"get\" id=\"edit_nagios_command_form\" name=\"edit_nagios_command_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit command</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
			<input type=\"text\" id=\"old_command_name\" name=\"old_command_name\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"command_name\">command name</label>\
                        <input type=\"text\" id=\"command_name\" name=\"command_name\" value=\"\" />\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"command_line\">command line</label>\
                        <input type=\"text\" id=\"command_line\" name=\"command_line\" value=\"\" style="width:350px"/>\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_command\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_command\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_hostdependency():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_hostdependency\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"hostdependency_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"25%\"/>\
			<col width=\"70%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th></th> \
			<th>Host name</th> \
			<th>Dependent host name</th> \
			<th>Action</th> \
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_hostdependency.py\" method=\"get\" id=\"edit_nagios_hostdependency_form\" name=\"edit_nagios_hostdependency_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit host dependency</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
			<input type=\"text\" id=\"hostdependency_name\" name=\"hostdependency_name\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"host_name\">Host name</label>\
                        <select name="host_name" id="host_name" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"dependent_host_name\">Dependent host name</label>\
                        <select name="dependent_host_name" id="dependent_host_name" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"dependent_hostgroup_name\">Dependent hostgroup name</label>\
                        <select name="dependent_hostgroup_name" id="dependent_hostgroup_name" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"inherits_parent\">inherits parent dependencies</label>\
                        <select name="inherits_parent" id="inherits_parent" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"dependency_period\">dependency period</label>\
                        <select name="dependency_period" id="dependency_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_failure_criteria\">notification failure criteria</label>\
                        <select name="notification_failure_criteria" id="notification_failure_criteria" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"execution_failure_criteria\">execution failure criteria</label>\
                        <select name="execution_failure_criteria" id="execution_failure_criteria" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_hostdependency\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_hostdependency\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def main_menu_servicedependency():
        """


        @return:
        """
        html_view = '\
 	     <input type=\"text\" id=\"nagios_module\" value=\"nagios_servicedependency\" style=\"display:none\"/>\
	     <div id="div_table_paginate">\
	     	<table cellpadding="0" cellspacing="0" border="0" class=\"display\" id=\"servicedependency_table_paginate\" style=\"text-align:center;\"> \
		<colgroup>\
			<col width=\"23%\"/>\
			<col width=\"24%\"/>\
			<col width=\"24%\"/>\
			<col width=\"24%\"/>\
			<col width=\"5%\"/>\
		</colgroup>\
		<thead> \
		<tr> \
			<th></th> \
			<th>Host name</th> \
			<th>Service name</th> \
			<th>Dependent Host name</th> \
			<th>Dependent Service name</th> \
			<th>Action</th> \
		</tr> \
		</thead> \
		</table>\
	     </div>\
	     <form style=\"display:none;\" action=\"save_nagios_edit_servicedependency.py\" method=\"get\" id=\"edit_nagios_servicedependency_form\" name=\"edit_nagios_servicedependency_form\" >\
                <div class=\"form-div\">\
		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		    <tr>\
		        <th class=\"cell-title\">Edit service dependency</th>\
		    </tr>\
		</table>\
                <div class=\"form-body\">\
			<input type=\"text\" id=\"servicedependency_name\" name=\"servicedependency_name\" value=\"\" style=\"display:none\" />\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"host_name\">Host name</label>\
                        <select name="host_name" id="host_name" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"service_description\">Service name</label>\
                        <select name="service_description" id="service_description" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"dependent_host_name\">Dependent Host name</label>\
                        <select name="dependent_host_name" id="dependent_host_name" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"dependent_service_description\">Dependent Service name</label>\
                        <select name="dependent_service_description" id="dependent_service_description" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"dependent_hostgroup_name\">Dependent hostgroup name</label>\
                        <select name="dependent_hostgroup_name" id="dependent_hostgroup_name" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"inherits_parent\">Inherits parent dependencies</label>\
                        <select name="inherits_parent" id="inherits_parent" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"dependency_period\">Dependency period</label>\
                        <select name="dependency_period" id="dependency_period" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"notification_failure_criteria\">Notification failure criteria</label>\
                        <select name="notification_failure_criteria" id="notification_failure_criteria" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\" for=\"execution_failure_criteria\">Execution failure criteria</label>\
                        <select name="execution_failure_criteria" id="execution_failure_criteria" class="multiselect" multiple="multiple"  title="Click to select an option">\
                        </select>\
                    </div>\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"save_edit_servicedependency\"><span class=\"edit\">Save</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_edit_servicedependency\"><span class=\"cancel\">Cancel</span></button>\
            </div>\
        </form>'
        return html_view

    @staticmethod
    def get_columns(selected_columns, non_selected_columns, heading):
        """

        @param selected_columns:
        @param non_selected_columns:
        @param heading:
        @return:
        """
        liList = ""
        plusList = ""
        if (non_selected_columns != [""]):
            for row in non_selected_columns:
                plusList += "<li>" + row + "<img src=\"images/add16.png\" class=\"plus plus\" alt=\"+\" title=\"Add\" id=\"" + \
                            row + "\" name=\"" + row + "\"/></li>"
        minusList = ""
        if (selected_columns != [""]):
            for row in selected_columns:
                minusList += "<li>" + row + "<img src=\"images/minus16.png\" class=\"minus minus\" alt=\"-\" title=\"Remove\" id=\"" + row + \
                             "\" name=\"" + row + "\"/></li>"
        selectList = []
        selectList.append(
            '<div style="vertical-align: middle; width: 30px; text-align: center; padding-top: 45.5px;margin-left: 120px;"><span id="moveable_vertical"><img onclick="moveElementsUpDown(\'0\', \'top\')" src="images/new_icons/icon_top_24.gif" style="cursor: pointer;" ><img onclick="moveElementsUpDown(\'0\', \'up\')" src="images/new_icons/icon_up_24.gif" style="cursor: pointer;"><img onclick="moveElementsUpDown(\'0\', \'down\')" src="images/new_icons/icon_down_24.gif" style="cursor: pointer;" ><img onclick="moveElementsUpDown(\'0\', \'bottom\')" src="images/new_icons/icon_bottom_24.gif" style="cursor: pointer;"></span></div>')
        selectList.append(
            "<div class=\"multiSelectList\" id=\"multiSelectList\" style=\"margin-left:165px;margin-top:-150px;\" multiple="" >")
        selectList.append("<input type=\"hidden\" id=\"hd\" name=\"hd\" value=\"%s\"/>" % (
            ",".join(selected_columns)))
        selectList.append(
            "<input type=\"hidden\" id=\"hdTemp\" name=\"hdTemp\" />")
        selectList.append("<div class=\"selected\">")
        selectList.append(
            "<div class=\"shead\"><span id=\"count\">%s</span><span>%s</span><a href=\"#\" id=\"rm\">Remove all</a>" % (
            len(
                selected_columns), heading))
        selectList.append("</div>")
        selectList.append("<ul>" + minusList)
        selectList.append("</ul></div>")
        #        selectList.append("</div>"
        selectList.append("<div class=\"nonSelected\">")
        selectList.append(
            "<div class=\"shead\"><a href=\"#\" id=\"add\">Add all</a>")
        selectList.append("</div>")
        selectList.append("<ul>" + plusList)
        selectList.append("</ul>")
        selectList.append("</div>")
        selectList.append("</div>")

        return ''.join(selectList)

    @staticmethod
    def settings_nagios(result):
        """

        @param result:
        @return:
        """
        try:
            s = '<table class="yo-table" width="100%" cellpadding="0" cellspacing="0" style="text-align:left">\
	       <colgroup width="35%"></colgroup>\
	       <colgroup width="15%"></colgroup>\
	       <colgroup width="auto"></colgroup>\
		 <tr class="yo-table-head">\
		    <th>Current Nagios state</th>\
		    <th>State</th>\
		    <th>Actions</th>\
		  </tr>\
		<tr>'
            if result == "Nagios is running":
                s += '  	<td class=" vertline" style="text-align:left"><label id="nagios_label" style="text-align:left">Running</label></td>\
		   <td style="text-align:left">\
                <img src="images/new/status-0.png" style=\"cursor:pointer;\"  title="ON" id="nagios_on" class="daemon-img w-tip-image"/>\
			<img src="images/new/status-2.png" style=\"cursor:pointer;display:none\"  title="OFF" id="nagios_off" class="daemon-img w-tip-image"/>\
		       </td>\
		   <td style="text-align:left">\
			<img src="images/new/play.png" style=\"cursor:pointer;display:none\" title="Start" id="nagios_start"  class="daemon-img start w-tip-image"/>\
			<img src="images/new/restart.png"  style=\"cursor:pointer;\" title="Restart" id="nagios_restart" class="daemon-img restart w-tip-image"/> &nbsp; &nbsp;\
			<img src="images/new/stop.png"  style=\"cursor:pointer;\"title="Stop" id="nagios_stop" class="daemon-img stop w-tip-image"/></td>'
            else:
                s += '\
	        <td class=" vertline" style="text-align:left"><label id="nagios_label" style="text-align:left">Stopped</label></td>\
		   <td style="text-align:left">\
		     	<img src="images/new/status-0.png" style=\"cursor:pointer;display:none\"  title="ON" id="nagios_on" class="daemon-img w-tip-image"/>\
			<img src="images/new/status-2.png" style=\"cursor:pointer;\"  title="OFF" id="nagios_off" class="daemon-img w-tip-image"/>\
	           </td>\
		   <td style="text-align:left">\
			<img src="images/new/play.png" style=\"cursor:pointer;\"  title="Start" id="nagios_start" class="daemon-img start w-tip-image"/>\
			<img src="images/new/restart.png"  style=\"cursor:pointer;display:none\" title="Restart" id="nagios_restart"  \
			class="daemon-img restart w-tip-image"/> &nbsp; &nbsp;\
			<img src="images/new/stop.png"  style=\"cursor:pointer;display:none\" title="Stop" id="nagios_stop" class="daemon-img stop w-tip-image"/></td>'
            if result == "Nagios is running":
                s += '\
            </tr>\
            <tr id ="sync_nagios" style="bottom:0;position:absolute;display:none">\
                <td style="text-align:left">\
                    Recommended option:\
                </td>\
            	<td style="text-align:left" colgroup=2>\
            	    <a id = "nagios_force_sync_anchor" href="#" style="text-align:left;width:50%">Repair & Sync nagios configuration files</a> to correct the configuration.\
            	</td>\
            	</tr>\
            </table>\
            <table><td id="error_nagios_info"></td></table>'
            else:
                s += '</tr>\
            <tr id ="sync_nagios" style="bottom:0;position:absolute">\
                <td style="text-align:left">\
                    Recommended option:\
                </td>\
                <td style="text-align:left" colgroup=2>\
                    <a id = "nagios_force_sync_anchor" href="#" style="text-align:left;width:50%">Repair & Sync nagios configuration files</a> to correct the configuration.\
                </td>\
                </tr>\
            </table>\
            <table><td id="error_nagios_info"></td></table>'

            return s
        except Exception, e:
            return str(e)

    @staticmethod
    def restore_config_nagios(backup_di):
        """

        @param backup_di:
        @return:
        """
        try:
            s = ['<div style="height:92%; overflow:auto">\
            <table class="yo-table display" width="100%" cellpadding="0" cellspacing="0" style="text-align:left" id="backup_table">\
            <tbody>\
	       <colgroup width="5%"></colgroup>\
	       <colgroup width="30%"></colgroup>\
	       <colgroup width="auto"></colgroup>\
		 <tr class="yo-table-head">\
		    <th></th>\
		    <th><font style="font-size:14px">Time</font></th>\
		    <th><font style="font-size:14px">Info</font></th>\
		  </tr>']
            if backup_di["success"] == 0:
                file_name_li = backup_di["file_list"]
                log_data_li = backup_di["log_data"]
                for i in range(len(log_data_li)):
                    log_data = log_data_li[i].split('::')
                    time_var = log_data[0].strip()
                    if (time_var + ".tar.bz2") in file_name_li:
                        s.append('<tr><td class=" vertline" style="text-align:left"><input type="radio" value="%s" name="option" id="option%s" class="table_option"/></td>\
		   <td style="text-align:left"><font style="font-size:13px">%s</font></td>\
		   <td style="text-align:left"><font style="font-size:13px">%s</font></td>\
		   </tr>' % (time_var, time_var, time_var, log_data[1]))

            s.append('</tbody></table></div><div style="bottom:0;position:absolute;">\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"restore_config_button\"><span class=\"edit\">Restore</span></button>\
                    <button type=\"button\" class=\"yo-small yo-button\" id=\"close_restore_config\"><span class=\"cancel\">Cancel</span></button>\
            </div>')
            return ' '.join(s)
        except Exception, e:
            return str(e)

            # @staticmethod
            # def view_page_tip_nagios_host():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_host.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_host_template():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_host_template.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_service():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_service.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_service_template():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_service_template.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_hostgroup():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_hostgroup.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_servicegroup():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_servicegroup.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_hostdependency():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_hostdependency.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_servicedependency():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_servicedependency.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_command():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_command.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_inventory_hosts():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_inventory_hosts.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
            #
            # @staticmethod
            # def view_page_tip_nagios_inventory_hostgroups():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_nagios_inventory_hostgroups.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
