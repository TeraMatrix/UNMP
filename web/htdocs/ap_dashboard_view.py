#!/usr/bin/python2.6
from datetime import datetime


class APView(object):
    """
    Device AP views
    """
    @staticmethod
    def ap_footer_tab(flag):
        """

        @param flag:
        @return:
        """
        if int(flag) == 0:
            html_page = '<div id=\"report_button_div\" class=\"form-div-footer\">\
            <table cellspacing="9px" cellpadding="0">\
            <tr>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"0\" name=\"option\" id=\"current_rept_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"current_rept_div\" width=\"25px\">Current Time</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"1\" name=\"option\" id=\"day1_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day1_rprt_div\" width=\"25px\">1 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"2\" name=\"option\" id=\"day2_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day2_rprt_div\" width=\"25px\">2 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"3\" name=\"option\" id=\"day3_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day3_rprt_div\" width=\"25px\">3 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"4\" name=\"option\" id=\"week_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"week_rprt_div\" width=\"25px\">1 Week</label></td>\
         <td style="text-align:left"><button type=\"submit\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="apExcelReportGeneration();"><span class=\"report\">Report</span></button></td>\
            </tr></table>\
            </div></div>\
            '
        else:
            html_page = '</div>'
        return html_page

    @staticmethod
    def ap_table(ip_address, odu_start_date, odu_start_time, odu_end_date, odu_end_time, ap_refresh_time, total_count):
        """

        @param ip_address:
        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param ap_refresh_time:
        @param total_count:
        @return:
        """
        dash_str = '\
        <input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\" />\
        <input type=\"hidden\" id=\"ip_address\" name=\"ip_address\" value=\"%s\" />\
        <input type=\"hidden\" id=\"total_count\" name=\"total_count\" value=\"%s\" />\
        <div style=\"float: right; font-size: 10px; color: rgb(85, 85, 85); font-weight: bold; padding: 10px 20px;\" >\
        <input type=\"textbox\" name=\"odu_start_date\" value=\"%s\" id=\"odu_start_date\" style=\"width:100px;\"/>\
        <input type=\"textbox\" name=\"odu_start_time\" value=\"%s\" id=\"odu_start_time\" style=\"width:80px;\"/>\
        <lable>--</lable>\
        <input type=\"textbox\" name=\"odu_end_date\" value=\"%s\" id=\"odu_end_date\" style=\"width:100px;\"/>\
        <input type=\"textbox\" name=\"odu_end_time\" value=\"%s\" id=\"odu_end_time\" style=\"width:80px;\"/>\
        <input type=\"button\" class=\"yo-small  yo-button\" name=\"ap_graph_show\" value=\"graph\" id=\"ap_graph_show\" style=\"width:50px;\"/>\
       </div>\
        </div>\
        <div id="ap_host_info_div"></div>\
        <div id="main_graph"></div>' % (
        ap_refresh_time, ip_address, total_count, odu_start_date, odu_start_time, odu_end_date, odu_end_time)
        return dash_str

    @staticmethod
    def device_information_view(result, ip_address, no_of_user):
        """

        @param result:
        @param ip_address:
        @param no_of_user:
        @return:
        """
        channel = [
            'channel-01', 'channel-02', 'channel-03', 'channel-04', 'channel-05', 'channel-06',
            'channel-07', 'channel-08', 'channel-09', 'channel-10', 'channel-11', 'channel-12', 'channel-13',
            'channel-14']
        wifi = ['wifi11g', 'wifi11gnHT20', 'wifi11gnHT40plus',
                'wifi11gnHT40minus']
        radio = ['disabled', 'enabled']
        device_detail = ''
        if len(result) > 0:
            device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
            device_detail += '<tbody>\
                        <tr>\
                        <th class="cell-title" colspan="4">\
                            ' + str(ip_address) + '\
                        </th>\
                        </tr>\
                        <tr>\
                        <th class="cell-title" colspan="4">\
                            Device Details\
                        </th>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            Radio Status\
                        </td>\
                        <td class="cell-info">' + str(
                '--' if result[0][0] == None or result[0][0] == ""  else radio[int(result[0][0])]) + '</td>\
                        <td class="cell-label">\
                            Radio Channel\
                        </td>\
                        <td class="cell-info">' + str(
                '--' if result[0][1] == None or result[0][1] == ""  else channel[int(result[0][1]) - 1]) + '</td>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            No of VAPs\
                        </td>\
                        <td class="cell-info">' + str(
                '--' if result[0][2] == None or result[0][2] == ""  else result[0][2]) + '</td>\
                        <td class="cell-label">\
                            Software Version\
                        </td>\
                        <td class="cell-info">' + str(
                '--' if result[0][3] == None or result[0][3] == ""  else result[0][3]) + '</td>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            Hardware Version\
                        </td>\
                        <td class="cell-info">' + str(
                '--' if result[0][4] == None or result[0][4] == ""  else result[0][4]) + '</td>\
                        <td class="cell-label">\
                            BootLoader Version\
                        </td>\
                        <td class="cell-info">' + str(
                '--' if result[0][5] == None or result[0][5] == ""  else result[0][5]) + '</td>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            WiFi Mode\
                        </td>\
                        <td class="cell-info">' + str(
                '--' if result[0][6] == None or result[0][6] == ""  else wifi[int(result[0][6])]) + '</td>\
                        <td class="cell-label">\
                            MAC Address\
                        </td>\
                        <td class="cell-info">' + str(
                '--' if result[0][7] == None or result[0][7] == ""  else result[0][7]) + '</td>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            No of Connected User\
                        </td>\
                        <td class="cell-info" colspan="3">' + str(
                0 if no_of_user[0][0] == None or no_of_user[0][0] == ""  else no_of_user[0][0]) + '</td>\
                        </tr>\
                        <tr>\
                        <th class="cell-title" colspan="4">\
                            Graphs\
                        </th>\
                        </tr>\
                    <tbody></table>'
        return device_detail

    @staticmethod
    def device_information_view_default(ip_address, user):
        """

        @param ip_address:
        @param user:
        @return:
        """
        device_detail = ''
        device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
        device_detail += '<tbody>\
                    <tr>\
                    <th class="cell-title" colspan="4">\
                        ' + str(ip_address) + '\
                    </th>\
                    </tr>\
                    <tr>\
                    <th class="cell-title" colspan="4">\
                        Device Details\
                    </th>\
                    </tr>\
                    <tr>\
                    <td class="cell-label">\
                        Radio Status\
                    </td>\
                    <td class="cell-info">--</td>\
                    <td class="cell-label">\
                        Radio Channel\
                    </td>\
                    <td class="cell-info">--</td>\
                    </tr>\
                    <tr>\
                    <td class="cell-label">\
                        No of VAPs\
                    </td>\
                    <td class="cell-info">--</td>\
                    <td class="cell-label">\
                        Software Version\
                    </td>\
                    <td class="cell-info">--</td>\
                    </tr>\
                    <tr>\
                    <td class="cell-label">\
                        Hardware Version\
                    </td>\
                    <td class="cell-info">--</td>\
                    <td class="cell-label">\
                        BootLoader Version\
                    </td>\
                    <td class="cell-info">--</td>\
                    </tr>\
                    <tr>\
                    <td class="cell-label">\
                        WiFi Mode\
                    </td>\
                    <td class="cell-info">--</td>\
                    <td class="cell-label">\
                        MAC Address\
                    </td>\
                    <td class="cell-info">--</td>\
                    </tr>\
                        <tr>\
                        <td class="cell-label">\
                            No of Connected User\
                        </td>\
                    <td class="cell-info" colspan="3">%s</td>\
                    <tr>\
                    <th class="cell-title" colspan="4">\
                        Graphs\
                    </th>\
                    </tr>\
                <tbody></table>' % str(user[0][0])
        return device_detail


#        <table id=\"ap_device_graph\" cellspacing="10px" cellpadding="0" width="100%%">\
#            <colgroup>\
#                <col width="50%%" style="width:50%%;"/>\
#                <col width="50%%" style="width:50%%;"/>\
#            </colgroup>\
#            <tr>\
#                <td><div id="dashboard1" class="db-box"></div></td>\
#                <td><div id="dashboard2" class="db-box"></div></td>\
#            </tr>\
#        </table>
