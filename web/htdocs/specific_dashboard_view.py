#!/usr/bin/python2.6
from datetime import datetime
import time
from specific_dashboard_bll import get_master_slave_value


class SPDashboardView(object):
    """
    AP Dashboard view
    """
    @staticmethod
    def header_buttons():
        """


        @return:
        """
        add_btn = "<div class=\"header-icon\"><img onclick=\"hostInformation();\" class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"host_info\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Show Status\"></div>"
        del_btn = "<div class=\"header-icon\"><img onclick=\"delHost();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Host\"></div>"
        del_btn = "<div class=\"header-icon\"><img onclick=\"delHost();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Host\"></div>"
        cancel_btn = "<div class=\"header-icon\"><img onclick=\"backListing();\" class=\"n-tip-image\" src=\"images/back.png\" id=\"del_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Back To Lising\"></div>".format(
            theme)
        header_btn = cancel_btn  # del_btn + add_btn
        return header_btn

    @staticmethod
    def sp_footer_tab(flag):
        """

        @param flag:
        @return:
        """
        if int(flag) == 0:
            html_page = '<div id=\"report_button_div\" class=\"form-div-footer\">\
            <table cellspacing="9px" cellpadding="0">\
            <tr>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"0\" name=\"option\" id=\"current_rept_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"current_rept_div\" width=\"25px\">Current Time<label style="font-size: 9px; color: rgb(85, 85, 85);"> (Last 3 Hr)</label></label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"1\" name=\"option\" id=\"day1_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day1_rprt_div\" width=\"25px\">Today</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"2\" name=\"option\" id=\"day2_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day2_rprt_div\" width=\"25px\">2 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"3\" name=\"option\" id=\"day3_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day3_rprt_div\" width=\"25px\">3 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"4\" name=\"option\" id=\"week_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"week_rprt_div\" width=\"25px\">1 Week</label></td>\
         <td style="text-align:left"><button type=\"submit\" id=\"sp_pdf_report\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="spPDFReportGeneration();"><span class=\"save\">PDF</span></button></td>\
         <td style="text-align:left"><button type=\"submit\" id=\"sp_excel_report\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="spExcelReportGeneration();"><span class=\"report\">Excel</span></button></td>\
         <td style="text-align:left"><button type=\"submit\" id=\"sp_csv_report\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="spCSVReportGeneration();"><span class=\"report\">CSV</span></button></td>\
            </tr></table>\
            </div></div>\
            '
        else:
            html_page = '</div>'
        return html_page

    @staticmethod
    def sp_table(ip_address, sp_start_date, sp_start_time, sp_end_date, sp_end_time, sp_refresh_time, total_count):
        """

        @param ip_address:
        @param sp_start_date:
        @param sp_start_time:
        @param sp_end_date:
        @param sp_end_time:
        @param sp_refresh_time:
        @param total_count:
        @return:
        """
        dash_str = '\
        <input type=\"hidden\" id=\"sp_refresh_time\" name=\"refresh_time\" value=\"%s\" />\
        <input type=\"hidden\" id=\"sp_ip_address\" name=\"ip_address\" value=\"%s\" />\
        <input type=\"hidden\" id=\"sp_total_count\" name=\"total_count\" value=\"%s\" />\
        <div>\
        <table cellspacing="10px" cellpadding="0" width="100%%" style="margin-top:20px;"><tr><td>\
        <div id="more_graph_columns" style=\"float:right;\"></div>\
        </td><td style=\"vertical-align:bottom;\">\
        <input type=\"button\" id=\"apply_graph\" name=\"apply_graph\"  value=\"Apply\" onClick="show_graph_click();" class="yo-small yo-button"/>\
        </td></tr></table>\
        </div>\
        <div style=\"float: right; font-size: 10px; color: rgb(85, 85, 85); font-weight: bold; padding: 10px 20px;\" >\
        <input type=\"hidden\" name=\"sp_start_date\" value=\"%s\" id=\"sp_start_date\" style=\"width:100px;\"/>\
        <input type=\"hidden\" name=\"sp_start_time\" value=\"%s\" id=\"sp_start_time\" style=\"width:80px;\"/>\
        <input type=\"hidden\" name=\"sp_end_date\" value=\"%s\" id=\"sp_end_date\" style=\"width:100px;\"/>\
        <input type=\"hidden\" name=\"sp_end_time\" value=\"%s\" id=\"sp_end_time\" style=\"width:80px;\"/>\
        </div>\
        </div>\
        <div style="position:relative;" id="main_host_info_div">\
        <div id="sp_host_info_div"></div>\
        <div class=\"header-icon header-tab-button1\"><img onclick=\"hostInformation();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"host_info\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 5px;\" original-title=\"Show Status\"></div>\
        <table class="tt-table" cellspacing="0px" cellpadding="0" width="100%%">\
        <tbody>\
        </tr>\
        <tr>\
        <th class="cell-title" colspan="4" style="padding-left:10px;">\
            Graphs\
        </th>\
        </tr>\
        </tbody>\
        </table>\
        </div>\
        <div id="sp_main_graph"></div>\
        <table cellspacing="10px" cellpadding="0" width="100%%" >\
        <tr>\
        <td width="100%%">\
        <div class="db-box" id=\"client_rsl_table\">\
        <div class="db-head">\
        <span>Connected Client RSL</span>\
        </div>\
        <div class="db-body">\
        <div class="db-container" style="height: 250px;overflow-y:auto;" id="client_dashboard">\
        </div>\
        </div>\
        </div>\
        </td>\
        <tr>\
        <tr>\
        <td width="100%%">\
        <div class="db-box" id=\"event_table\">\
        <div class="db-head">\
        <span>Device Events<label style="font-size: 9px; color: rgb(85, 85, 85);"> - Last 7 Events</label></span>\
        </div>\
        <div class="db-body">\
        <div class="db-container" style="height: 250px;" id="event_dashboard">\
        </div>\
        </div>\
        </div>\
        </td>\
        <tr>\
        </table>\
        ' % (sp_refresh_time, ip_address, total_count, sp_start_date, sp_start_time, sp_end_date, sp_end_time, theme)
        return dash_str

    @staticmethod
    def device_information_view(result, ip_address):
        """

        @param result:
        @param ip_address:
        @return:
        """
        last_reboot_time = ''
        column_list = {
        'odu16': ['Frequency', 'Slave', 'Active Version', 'Hardware Version', 'Last Reboot Reason', 'Channel',
                  'Operation state',
                  'Node Type', 'MAC Address', 'Last Reboot Time'],
        'odu100': ['Frequency', 'Slave', 'Active Version', 'Hardware Version', 'Last Reboot Reason',
                   'Channel', 'Operation state', 'Node Type', 'MAC Address', 'Last Reboot Time']}
        last_reboot_resion = {0: 'Power cycle', 1: 'Watchdog reset', 2: 'Normal', 3:
            'Kernel crash reset', 4: 'Radio count mismatch reset', 5: 'Unknown-Soft', 6: 'Unknown reset'}
        default_node_type = {0: 'rootRU', 1: 't1TDN', 2: 't2TDN', 3: 't2TEN'}
        operation_state = {0: 'disabled', 1: 'enabled'}
        channel = {0: 'raBW5MHz', 1: 'raBW10MHz', 2: 'raBW20MHz',
                   3: 'raBW40MHz', 4: 'raBW40SGIMHz'}

        wifi = ['wifi11g', 'wifi11gnHT20', 'wifi11gnHT40plus',
                'wifi11gnHT40minus']
        radio = ['disabled', 'enabled']
        device_detail = ''
        if result['device_type'] == 'odu16' or result['device_type'] == 'odu100':
            master_slave_status = '--'
            master_slave_result = get_master_slave_value(ip_address)
            if int(master_slave_result['success']) == 0 and int(master_slave_result['status']) == 0:
                master_slave_status = str('--' if result['result'][1] == None or result[
                    'result'][1] == "" else result['result'][1])
            else:
                master_slave_status = 'N/A'
            if len(result['result']) > 0:
                last_reboot_time = '--' if result['last_reboot_time'] == None or len(
                    result['last_reboot_time']) == 0 else result['last_reboot_time'][0][0]
                result = result['result']
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                ' + str(
                    '--' if result[len(result) - 1] == None or result[len(result) - 1] == ""  else result[
                        len(result) - 1]) + '\
                            </th>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Device Status\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Frequency\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0] == None or result[0] == ""  else result[0]) + '</td>\
                            <td class="cell-label">\
                                Time Slot\
                            </td>\
                            <td class="cell-info">' + master_slave_status + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Active Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[2] == None or result[2] == ""  else result[2]) + '</td>\
                            <td class="cell-label">\
                                Hardware Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[3] == None or result[3] == ""  else result[3]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Last Reboot Reason\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[4] == None or result[4] == ""  else last_reboot_resion[int(result[4])]) + '</td>\
                            <td class="cell-label">\
                                Channel\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[5] == None or result[5] == "" or result[5] < 0   else channel[int(result[5])]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Operation State\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[6] == None or result[6] == ""  else operation_state[int(result[6])]) + '</td>\
                            <td class="cell-label">\
                                Node Type\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[7] == None or result[7] == ""  else default_node_type[int(result[7])]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                MAC Address\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[8] == None or result[8] == ""  else result[8]) + '</td>\
                            <td class="cell-label">\
                                Last Reboot Time\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if last_reboot_time == None or last_reboot_time == ""  else last_reboot_time) + '</td>\
                            </tr>\
                        <tbody></table>'
            else:
                last_reboot_time = '--' if result['last_reboot_time'] == None or len(
                    result['last_reboot_time']) == 0 else result['last_reboot_time'][0][0]
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                ' + str(ip_address) + '\
                            </th>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Device Status\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Frequency\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Time Slot\
                            </td>\
                            <td class="cell-info">N/A</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Active Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Hardware Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Last Reboot Reason\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Channel\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Operation State\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Node Type\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                MAC Address\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Last Reboot Time\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if last_reboot_time == None or last_reboot_time == ""  else last_reboot_time) + '</td>\
                            </tr>\
                        <tbody></table>'
        elif result['device_type'].strip() == 'ccu':
            ccu_type = ['ccu100', 'ccu250', 'ccu500']
            result = result['result']
            if result != None and len(result) > 0:
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                ' + str(ip_address) + '\
                            </th>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Device Status\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                CCU Type\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][0] == None or result[0][0] == ""  else ccu_type[int(result[0][0])]) + '</td>\
                            <td class="cell-label">\
                                Serial Number\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][1] == None or result[0][1] == ""  else result[0][1]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Hardware Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][2] == None or result[0][2] == ""  else result[0][2]) + '</td>\
                            <td class="cell-label">\
                                Active Software Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][3] == None or result[0][3] == ""  else result[0][3]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                BootLoader Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][4] == None or result[0][4] == ""  else result[0][4]) + '</td>\
                            <td class="cell-label">\
                                Backup Software Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][5] == None or result[0][5] == ""  else result[0][5]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Last Reboot Reason\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][6] == None or result[0][6] == ""  else result[0][6]) + '</td>\
                            <td class="cell-label">\
                                MAC Address\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][7] == None or result[0][7] == ""  else result[0][7]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Protocol Version\
                            </td>\
                            <td class="cell-info" colspan="3">' + str(
                    '--' if result[0][8] == None or result[0][8] == ""  else result[0][8]) + '</td>\
                            </tr>\
                        <tbody></table>'
            else:
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                ' + str(ip_address) + '\
                            </th>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Device Status\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                CCU Type\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Serial Number\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Hardware Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Active Software Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                backup Software Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                BootLoader Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Last Reboot Reason\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                MAC Address\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Protocol Version\
                            </td>\
                            <td class="cell-info" colspan="3">--</td>\
                            </tr>\
                        <tbody></table>'

        elif result['device_type'].strip() == 'ap25':
            channel = [
                'channel-01', 'channel-02', 'channel-03', 'channel-04', 'channel-05', 'channel-06', 'channel-07',
                'channel-08', 'channel-09',
                'channel-10', 'channel-11', 'channel-12', 'channel-13', 'channel-14']
            connected_user = 0
            if len(result['no_of_uesr']) > 0 and result['no_of_uesr'] != None:
                user = result['no_of_uesr']
                connected_user = user[0][0]
            result = result['result']
            if result != None and len(result) > 0:
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                ' + str(ip_address) + '\
                            </th>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Device Status\
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
                                No Of VAPs\
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
                                No Of Connected User\
                            </td>\
                            <td class="cell-info" colspan="3">' + str(connected_user) + '</td>\
                            </tr>\
                        <tbody></table>'
            else:
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                ' + str(ip_address) + '\
                            </th>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Device Status\
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
                                No Of VAPs\
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
                                    No Of Connected User\
                                </td>\
                            <td class="cell-info" colspan="3">%s</td>\
                        <tbody></table>' % connected_user
        elif result['device_type'].strip() == 'idu4':
            hour = 0
            minute = 0
            second = 0
            device_detail = ''
            result = result['result']
            if len(result) > 0:
                if result != None and result[0][7] != None:
                    hour = result[0][7] / 3600
                    minute = (result[0][7] / 60) % 60
                    second = result[0][7] % 60
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                ' + str(ip_address) + '\
                            </th>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Device Status\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                H/W Serial Number\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][0] == None or result[0][0] == ""  else result[0][0]) + '</td>\
                            <td class="cell-label">\
                                System MAC\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][1] == None or result[0][1] == ""  else result[0][1]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                TDMOIP Interface MAC\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][2] == None or result[0][2] == ""  else result[0][2]) + '</td>\
                            <td class="cell-label">\
                                Active Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][3] == None or result[0][3] == ""  else result[0][3]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Passive Version\
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
                                Temperature(C)\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0][6] == None or result[0][6] == ""  else result[0][6]) + '</td>\
                            <td class="cell-label">\
                                Uptime\
                            </td>\
                            <td class="cell-info">' + str(
                    str(hour) + "Hr " + str(minute) + "Min " + str(second) + "Sec") + '</td>\
                            </tr>\
                        <tbody></table>'
            else:
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
                                Device Status\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                H/W Serial Number\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                System MAC\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                TDMOIP Interface MAC\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Active Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Passive Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                BootLoader Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Temperature(C)\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Uptime\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                        <tbody></table>'
        return device_detail

    @staticmethod
    def sp_ap_client_table_view(result):
        """

        @param result:
        @return:
        """
        Client_table = '<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
        Client_table += '\
			<colgroup><col style="width:5%;"/><col style="width:12%;"/><col style="width:10%;"/><col style="width:5%;"/><col style="width:5%;"/><col style="width:9%;"/><col style="width:9%;"/><col style="width:10%;"/><col style="width:10%;"/><col style="width:10%;"/><col style="width:10%;"/><col style="width:5%;"/>\
  </colgroup>\
        <tr class="yo-table-head">\
            <th >No.</th>\
            <th >Client Alias</th>\
            <th >MAC Adddress</th>\
            <th >RSL</th>\
            <th >VAP</th>\
            <th >Total Tx(Packets)</th>\
            <th >Total Rx(Packets)</th>\
            <th >First seen AP</th>\
            <th >First seen time</th>\
            <th >Last seen AP</th>\
            <th >Last seen time</th>\
            <th >Connected</th>\
        </tr>'
        new_result = result['result']
        count_no = 1
        for i in new_result:
            Client_table += '<tr><td>%s</td>' % count_no
            Client_table += '<td><a href="client_dashboard_profiling.py?client_mac=%s&device_type=ap25&path=1&host_id=%s">%s</a></td>' \
                            % (str("--" if i[1] == None or i[1] == "" else i[1]), result['host_id'],
                               str("--" if i[0] == None or i[0] == "" else i[0]))
            Client_table += '<td>%s</td>' % str(
                "--" if i[1] == None or i[1] == "" else i[1])
            Client_table += '<td>%s</td>' % str(
                "--" if i[2] == None or i[2] == "" else i[2])
            Client_table += '<td>%s</td>' % str(
                "--" if i[3] == None or i[3] == "" else 0 - int(i[3]))
            Client_table += '<td>%s</td>' % str(
                "--" if i[4] == None or i[4] == "" else i[4])
            Client_table += '<td>%s</td>' % str(
                "--" if i[5] == None or i[5] == "" else i[5])
            Client_table += '<td>%s</td>' % str(
                "--" if i[6] == None or i[6] == "" else i[6])
            Client_table += '<td>%s</td>' % str(
                "--" if i[7] == None or i[7] == "" else i[7])
            Client_table += '<td>%s</td>' % str(
                "--" if i[8] == None or i[8] == "" else i[8])
            Client_table += '<td>%s</td>' % str(
                "--" if i[9] == None or i[9] == "" else i[9])
            Client_table += '<td><img src="images/%s" alt="Yes" title="Status"/></td></tr>' % str(
                "host_status_ap_1.png" if i[10] == None or i[10] == "" or i[10] == "No" else "host_status_ap_0.png")
            count_no += 1
        if len(new_result) < 1:
            Client_table += '<tr ><td colspan="12"><b>Client Information does not exists.</b></td></tr>'
        return {'success': 0, 'client_table': Client_table}

    @staticmethod
    def sp_event_alarm_table_view(result, ip_address):
        """

        @param result:
        @param ip_address:
        @return:
        """
        image_title_name = {0: "Normal", 1: "Informational", 2:
            "Normal", 3: "Minor", 4: "Major", 5: "Critical"}
        image_dic = {0: "images/gr.png", 1: "images/lb.png", 2: "images/gr.png", 3:
            "images/yel.png", 4: "images/or.png", 5: "images/red.png"}
        # image_dic={0:"images/status-7.png",1:"images/status-0.png",2:"images/status-7.png",3:"images/status-4.png",4:"images/minor.png",5:"images/critical.png"}
        # image_dic={0:"images/status-4.png",1:"images/status-7.png.png",2:"images/status-4.png",3:"images/minor.png",4:"images/status-0.png",5:"images/critical.png"}
        length = 7
        history_trap_detail = {}
        all_traps = result['Event']
        current_alarm = result['Alarm']
        if len(all_traps) < 7:
            length = len(all_traps)

        history_trap = '<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
        history_trap += '\
			<colgroup><col style="width:5%;" /><col style="width:15%;" /><col style="width:12%;" /><col style="width:12%;" /><col style="width:12%;" /><col style="width:35%;" />\
  </colgroup>\
        <tr class="yo-table-head">\
            <th class=" vertline">&nbsp;</th>\
            <th >Received Date</th>\
            <th >Event Name</th>\
            <th >Event ID</th>\
            <th >Event Type</th>\
            <th>Description</th>\
        </tr>'

        for i in range(length):
            if i < 6:
                history_trap += '<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>' % (
                    image_dic[all_traps[i][0]], image_title_name[all_traps[i][0]], image_title_name[all_traps[i][0]])
                history_trap += '<td>%s</td>' % (datetime.strptime(
                    all_traps[i][5], '%a %b %d %H:%M:%S %Y')).strftime('%d %b %Y %H:%M:%S')
                history_trap += '<td>%s</td>' % all_traps[i][1]
                history_trap += '<td>%s</td>' % all_traps[i][2]
                history_trap += '<td>%s</td>' % all_traps[i][3]
                history_trap += '<td>%s</td></tr>' % all_traps[i][6]
            else:
                history_trap += '<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>' % (
                    image_dic[all_traps[i][0]], image_title_name[all_traps[i][0]], image_title_name[all_traps[i][0]])
                history_trap += '<td >%s</td>' % (datetime.strptime(
                    all_traps[i][5], '%a %b %d %H:%M:%S %Y')).strftime('%d %b %Y %H:%M:%S')
                history_trap += '<td>%s</td>' % all_traps[i][1]
                history_trap += '<td>%s</td>' % all_traps[i][2]
                history_trap += '<td>%s</td>' % all_traps[i][3]
                history_trap += '<td>%s&nbsp&nbsp&nbsp&nbsp%s</td></tr>' % (
                    all_traps[i][6], ((
                                      "<a href=\"status_snmptt.py?trap_status=history&ip_address=" + ip_address + "\">more>></a>" if len(
                                          all_traps) > 6 else "")))

        if len(all_traps) < 1:
            history_trap += '<tr ><td colspan="6"><b>Events does not exists.</b></td></tr>'

        length = 5
        if len(current_alarm) < 6:
            length = len(current_alarm)

        current_alarm_html = '<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
        current_alarm_html += '\
			<colgroup><col style="width:5%;" /><col style="width:15%;" /><col style="width:25%;" /><col style="width:40%;" />\
  </colgroup>\
        <tr class="yo-table-head">\
            <th class=" vertline">&nbsp;</th>\
            <th>Received Date</th>\
            <th>Event Type</th>\
            <th style="text-align:left;">Description</th>\
        </tr>'
        for i in range(length):
            if i < 5:
                current_alarm_html += '<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>' % (
                    image_dic[current_alarm[i][0]], image_title_name[current_alarm[i][0]],
                    image_title_name[current_alarm[i][0]])
                current_alarm_html += '<td>%s</td>' % (datetime.strptime(
                    current_alarm[i][5], '%a %b %d %H:%M:%S %Y')).strftime('%d %b %Y %H:%M:%S')
                current_alarm_html += '<td>%s</td>' % current_alarm[i][3]
                current_alarm_html += '<td style="text-align:left;">%s</td></tr>' % current_alarm[
                    i][6]
            else:
                current_alarm_html += '<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>' % (
                    image_dic[current_alarm[i][0]], image_title_name[current_alarm[i][0]],
                    image_title_name[current_alarm[i][0]])
                current_alarm_html += '<td>%s</td>' % (datetime.strptime(
                    current_alarm[i][5], '%a %b %d %H:%M:%S %Y')).strftime('%d %b %Y %H:%M:%S')
                current_alarm_html += '<td>%s</td>' % current_alarm[i][3]
                current_alarm_html += '<td style="text-align:left;">%s&nbsp&nbsp%s</td></tr>' % (
                    current_alarm[i][6], ((
                                          "<a href=\"status_snmptt.py?trap_status=history&ip_address=" + ip_address + "\">more>></a>" if len(
                                              current_alarm) > 6 else "")))
        if len(current_alarm) < 1:
            current_alarm_html += '<tr ><td colspan="6"><b>Alarm does not exists.</b></td></tr>'

        return {'success': 0, 'alarm_table': current_alarm_html, 'event_table': history_trap}

    @staticmethod
    def sp_get_graph(selected_columns, non_selected_columns):
        """

        @param selected_columns:
        @param non_selected_columns:
        @return:
        """
        liList = ""
        plusList = ""
        if (len(non_selected_columns) > 0):
            for row in non_selected_columns:
                plusList += "<li>" + row[
                    0] + "<img src=\"images/add16.png\" class=\"plus plus\" alt=\"+\" title=\"Add\" id=\"" + \
                            row[1] + "\" name=\"" + row[0] + "\"/></li>"
        minusList = ""
        sel_col_list = []
        for row in selected_columns:
            sel_col_list.append(row[1])
            minusList += "<li>" + row[
                0] + "<img src=\"images/minus16.png\" class=\"minus minus\" alt=\"-\" title=\"Remove\" id=\"" + row[
                             1] + "\" name=\"" + row[
                             0] + "\"/></li>"
        selectList = ""
        selectList += "<div class=\"multiSelectList\" id=\"multiSelectList\" style=\"margin-left:120px;margin-top:-10px;\">"
        selectList += "<input type=\"hidden\" id=\"sp\" name=\"sp\" value=\"%s\"/>" % (
            ",".join(sel_col_list))
        selectList += "<input type=\"hidden\" id=\"spTemp\" name=\"spTemp\" />"
        selectList += "<div class=\"selected\">"
        selectList += "<div class=\"shead\"><span id=\"count\">%s</span><span> Select Graphs</span><a href=\"#\" id=\"rm\">Remove all</a>" % (
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
