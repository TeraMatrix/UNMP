#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 20-Apr-2012
@version: 0.1
@note: All Views Related with Logs and Events.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


class LogsEvents(object):
    @staticmethod
    def header_buttons():
        header_btn = ""
        return header_btn

    @staticmethod
    def manage_logs():
        html_view = "" \
                    "<div id=\"serach_form_div\">\
                <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\" id=\"search_form_table\">\
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
                            <td class=\"cell-label\">Host Alias</td>\
                            <td class=\"cell-info\"><input type=\"text\" id=\"host\" name=\"host\" /></td>\
                        </tr>\
                        <tr>\
                            <td class=\"cell-label\">Service</td>\
                            <td class=\"cell-info\"><input type=\"text\" id=\"service\" name=\"service\" /></td>\
                        </tr>\
                        <tr>\
                            <td class=\"cell-label\">Log output</td>\
                            <td class=\"cell-info\"><input type=\"text\" id=\"log_plugin_output\" name=\"log_plugin_output\" /></td>\
                        </tr>\
                        <tr>\
                            <td class=\"cell-label\">Time of log entry</td>\
                            <td class=\"cell-info\">\
                            <label for=\"logtime_sec\">sec</label>\
                            <input type=\"text\" id=\"logtime_sec\" name=\"logtime_sec\" style=\"width:20px;padding-right:4px;\" value=\"0\"/>\
                            <label for=\"logtime_min\">min</label>\
                            <input type=\"text\" id=\"logtime_min\" name=\"logtime_min\" style=\"width:20px;padding-right:4px;\" value=\"0\"/>\
                            <label for=\"logtime_hours\">hours</label>\
                            <input type=\"text\" id=\"logtime_hours\" name=\"logtime_hours\" style=\"width:20px;padding-right:4px;\" value=\"0\"/>\
                            <label for=\"logtime_days\">days</label>\
                            <input type=\"text\" id=\"logtime_days\" name=\"logtime_days\" style=\"width:40px;padding-right:4px;\" value=\"1\"/>\
                            &nbsp; \
                            <label for=\"before\">before</label>\
                            <input type=\"radio\" id=\"before\" name=\"logtime\" value=\"before\" style=\"vertical-align:middle;\"/>\
                            <label for=\"since\">since</label>\
                            <input type=\"radio\" id=\"since\" name=\"logtime\" value=\"since\" style=\"vertical-align:middle;\" checked=\"checked\"/>\
                            </td>\
                        </tr>\
                        <tr>\
                            <td class=\"cell-label\"></td>\
                            <td class=\"cell-info\"><input class=\"yo-button yo-small\" type=\"button\" id=\"submit\" name=\"submit\" value=\"submit\" /></td>\
                        </tr>\
                    </tbody>\
                </table>\
                </div>" \
                    "<div id=\"grid_view_events_div\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_events_table\" style=\"text-align:center;\">\
                         </table>" \
                    "</div>"
        return html_view

    @staticmethod
    def manage_events(host="", service="", log_plugin_output="", logtime_sec=0, logtime_min=0, logtime_hours=0,
                      logtime_days=1, logtime="since"):
        logtime_since = ""
        logtime_before = ""
        if logtime == "before":
            logtime_before = " checked=\"checked\""
        else:
            logtime_since = " checked=\"checked\""
        html_view = "\
        <div id=\"serach_form_div\">\
        <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" id=\"search_form_table\">\
        	<thead>\
        		<tr>\
        			<th colspan=\"2\" class=\"cell-title\">\
        			<span style=\"float:left;padding-top:3px;\">Search Events</span>\
        			<img class=\"img-link\" id=\"hide_show\" src=\"images/new/down.png\" style=\"float: right; margin-right: 10px;\" title=\"Show\">\
        			</th>\
        		</tr>\
        	</thead>\
        	<tbody style=\"display:none;\">\
        		<tr>\
        			<td class=\"cell-label\">Host Alias</td>\
        			<td class=\"cell-info\"><input type=\"text\" id=\"host\" name=\"host\" value=\"%s\" /></td>\
        		</tr>\
        		<tr>\
        			<td class=\"cell-label\">Service</td>\
        			<td class=\"cell-info\"><input type=\"text\" id=\"service\" name=\"service\" value=\"%s\"  /></td>\
        		</tr>\
        		<tr>\
        			<td class=\"cell-label\">Log output</td>\
        			<td class=\"cell-info\"><input type=\"text\" id=\"log_plugin_output\" value=\"%s\"  name=\"log_plugin_output\" /></td>\
        		</tr>\
        		<tr>\
        			<td class=\"cell-label\">Time of log entry</td>\
        			<td class=\"cell-info\">\
        			<label for=\"logtime_sec\">sec</label>\
        			<input type=\"text\" id=\"logtime_sec\" name=\"logtime_sec\" style=\"width:20px;padding-right:4px;\" value=\"%s\"/>\
        			<label for=\"logtime_min\">min</label>\
        			<input type=\"text\" id=\"logtime_min\" name=\"logtime_min\" style=\"width:20px;padding-right:4px;\" value=\"%s\"/>\
        			<label for=\"logtime_hours\">hours</label>\
        			<input type=\"text\" id=\"logtime_hours\" name=\"logtime_hours\" style=\"width:20px;padding-right:4px;\" value=\"%s\"/>\
        			<label for=\"logtime_days\">days</label>\
        			<input type=\"text\" id=\"logtime_days\" name=\"logtime_days\" style=\"width:40px;padding-right:4px;\" value=\"%s\"/>\
        			&nbsp; \
        			<label for=\"before\">before</label>\
        			<input type=\"radio\" id=\"before\" name=\"logtime\" value=\"before\" style=\"vertical-align:middle;\"%s/>\
        			<label for=\"since\">since</label>\
        			<input type=\"radio\" id=\"since\" name=\"logtime\" value=\"since\" style=\"vertical-align:middle;\"%s/>\
        			</td>\
        		</tr>\
        		<tr>\
        			<td class=\"cell-label\"></td>\
        			<td class=\"cell-info\"><input class=\"yo-button yo-small\" type=\"button\" id=\"submit\" name=\"submit\" value=\"submit\" /></td>\
        		</tr>\
        	</tbody>\
        </table>\
        </div>\
        <div id=\"grid_view_events_div\">\
                <table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_events_table\" style=\"text-align:center;\">\
                 </table>\
        </div>" % (
        host, service, log_plugin_output, logtime_sec, logtime_min, logtime_hours, logtime_days, logtime_before,
        logtime_since)
        return html_view
