#!/usr/bin/python2.6
from datetime import datetime
from datetime import timedelta

from advanced_status_bll import AdvancedStatusBll
from advanced_status_bll import get_master_slave_value


class AdvancedStatusView(object):
    """
    Device specific Status page
    """
    @staticmethod
    def ap_set_variable(ip_address, device_type_id, user_id):
        """

        @param ip_address:
        @param device_type_id:
        @param user_id:
        @return:
        """
        now = datetime.now()
        odu_end_date = now.strftime("%d/%m/%Y")
        odu_end_time = now.strftime("%H:%M")
        now = now + timedelta(minutes=-300)
        odu_start_date = now.strftime("%d/%m/%Y")
        odu_start_time = now.strftime("%H:%M")
        bll_object = AdvancedStatusBll()
        result = bll_object.get_host_id(ip_address, device_type_id)
        if result['success'] == 1:
            host_id = 1
        else:
            host_id = result['host_id']

        html_data = "<div class=\"form-div\"><div id='timeDiv' style=\"margin-left:10px;margin-top:10px;\"><input type=\"text\" name=\"odu_start_date\" value=\"%s\" id=\"odu_start_date\" style=\"width:100px;\"/>\
                    <input type=\"text\" name=\"odu_start_time\" value=\"%s\" id=\"odu_start_time\" style=\"width:80px;\"/>\
                    <lable>--</lable>\
                    <input type=\"text\" name=\"odu_end_date\" value=\"%s\" id=\"odu_end_date\" style=\"width:100px;\"/>\
                    <input type=\"text\" name=\"odu_end_time\" value=\"%s\" id=\"odu_end_time\" style=\"width:80px;\"/>\
                    <button id=\"advancedSrh\" type=\"submit\" class=\"yo-button yo-small\" style=\"margin-top:5px;\" onclick=\"advancedSrchBtn();\"><span>Go</span></button>\
                    <div class=\"header-icon\" style=\"float:right\"><a href=\"sp_status_profiling.py?host_id=%s&device_type=%s&device_list_state=enabled\"><img id=\"page_tip\" class=\"n-tip-image\" original-title=\"Back To Current Status\" style=\"width: 21px; height: 21px; margin: 6px 20px 6px 10px;\" name=\"Back\" src=\"images/back.jpeg\"/></a></div></div>\
                    <table border=\"0\" cellspacing=\"10px\" cellpadding=\"0\" width=\"100%%\" id=\"graph_name_table\" ><tbody>\
		    <tr><td><div id='apGraphNameTable'></div></td></tr></tbody></table>\
                    <div id='apAdvanceGraphDiv'></div>\
                    <div id=\"apAdvancedDataTable\"></table></div>\
                    <input type=\"hidden\" id='advaced_device_type'  name='advaced_device_type'  value=%s />\
                    <input type=\"hidden\" id='advaced_ip_address'  name='advaced_ip_address'  value=%s />\
                    <input type=\"hidden\" id='user_id'  name='user_id'  value=%s />" % (
        odu_start_date, odu_start_time, odu_end_date, odu_end_time, host_id, device_type_id, device_type_id, ip_address,
        user_id)
        html_data += '</div><div id=\"report_button_div\" class=\"form-div-footer\">\
            <table cellspacing="9px" cellpadding="0">\
            <tr>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"0\" name=\"option\" id=\"current_rept_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"current_rept_div\" width=\"25px\">Selected Date</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"1\" name=\"option\" id=\"day1_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day1_rprt_div\" width=\"25px\">Today</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"2\" name=\"option\" id=\"day2_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day2_rprt_div\" width=\"25px\">7 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"3\" name=\"option\" id=\"day3_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day3_rprt_div\" width=\"25px\">15 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"4\" name=\"option\" id=\"week_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"week_rprt_div\" width=\"25px\">30 Day</label></td>\
     <td style="text-align:left"><button id="excel_report" type=\"submit\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="advacedExcelReportGeneration();"><span class=\"report\">Excel</span></button></td>\
     <td style="text-align:left"><button id="csv_report" type=\"submit\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="advacedCSVReportGeneration();"><span class=\"report\">CSV</span></button></td>\
            </tr></table>\
        </div></div>'
        return html_data

    @staticmethod
    def graph_name_listing(result_dict, ip_address):
        """

        @param result_dict:
        @param ip_address:
        @return:
        """
        if int(result_dict['success']) == 0:
            graph_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%"><colgroup><col width="50%" style="width:50%;"/><col width="49%" style="width:49%;"/><col width="1%" style="width:1%;"/></colgroup>'
            graph_detail += '<tbody>\
                        <tr>\
			<th class="cell-title">\
                            Device Status\
			</th>\
			<th class="cell-title" style="border-right:0px none;"></th>\
                        <th class="cell-title header-tab-button">\
<img class=\"n-tip-image image-link\" src=\"images/%s/round_minus.png\" id=\"device_status\" style=\"float:right;margin-right:5px;width:22px;cursor: pointer;\" original-title=\"Show Status\"></th>\
                        </tr>' % theme
            graph_detail += '<tr class="tr-graph">'
            i = 1
            # check the deivce is master or not.
            master_slave_status = get_master_slave_value(ip_address)
            # this is check the master or slave for sync lsot graph showing or
            # not.

            for graph in result_dict['result']:
                if master_slave_status['success'] == 0 and int(master_slave_status['status']) == 0:
                    if graph[1] == 'odu100synclost123':
                        pass
                    else:
                    #                        graph_json.append(graph_dict)
                        if i % 2 == 0:
                            graph_detail += '\
                        <td colspan="2" class="cell-label" style="text-align:left"><a href=\'#\'  value=\'%s\'><strong>%s</strong></a></td>' % (
                            ('--' if graph[1] == None or graph[1] == "" else graph[1]),
                            ('--' if graph[0] == None or graph[0] == "" else graph[0]))
                            graph_detail += '</tr>'
                            graph_detail += '<tr class="tr-graph">'
                        else:
                            graph_detail += '\
                        <td class="cell-label" style="text-align:left"><a href=\'#\'  value=\'%s\'><strong>%s</strong></a></td>' % (
                            ('--' if graph[1] == None or graph[1] == "" else graph[1]),
                            ('--' if graph[0] == None or graph[0] == "" else graph[0]))
                else:
                    if i % 2 == 0:
                        graph_detail += '\
			<td colspan="2" class="cell-label" style="text-align:left"><a href=\'#\'  value=\'%s\'><strong>%s</strong></a></td>' % (
                        ('--' if graph[1] == None or graph[1] == "" else graph[1]),
                        ('--' if graph[0] == None or graph[0] == "" else graph[0]))
                        graph_detail += '</tr>'
                        graph_detail += '<tr class="tr-graph">'
                    else:
                        graph_detail += '\
			<td class="cell-label" style="text-align:left"><a href=\'#\'  value=\'%s\'><strong>%s</strong></a></td>' % (
                        ('--' if graph[1] == None or graph[1] == "" else graph[1]),
                        ('--' if graph[0] == None or graph[0] == "" else graph[0]))
                i += 1
            graph_detail += '</tr><tbody></table>'
            output_dict = {'success': 0, 'result': graph_detail}
            return output_dict
        else:
            return result_dict

    @staticmethod
    def graph_name_listing123(result_dict, ip_address):
        """

        @param result_dict:
        @param ip_address:
        @return:
        """
        if int(result_dict['success']) == 0:
            graph_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
            graph_detail += '<tbody>\
                        <tr>\
                        <th class="cell-title" colspan="2">\
                            Graph Name\
                        </th>\
                        </tr>'
            graph_detail += '<tr>'
            i = 0
            # check the deivce is master or not.
            master_slave_status = get_master_slave_value(ip_address)
            # this is check the master or slave for sync lsot graph showing or
            # not.

            for graph in result_dict['result']:
                if master_slave_status['success'] == 0 and int(master_slave_status['status']) == 0:
                    if graph[1] == 'odu100synclost':
                        pass
                    else:
                    #                        graph_json.append(graph_dict)
                        if i % 2 == 0 and i != 0:
                            graph_detail += '</tr>'
                            graph_detail += '<tr>'
                        graph_detail += '\
                        <td class="cell-label" style="text-align:left"><a href=\'#\'  value=\'%s\'><strong>%s</strong></a></td>' % (
                        ('--' if graph[1] == None or graph[1] == "" else graph[1]),
                        ('--' if graph[0] == None or graph[0] == "" else graph[0]))
                else:
                    if i % 2 == 0 and i != 0:
                        graph_detail += '</tr>'
                        graph_detail += '<tr>'
                    graph_detail += '\
			<td class="cell-label" style="text-align:left"><a href=\'#\'  value=\'%s\'><strong>%s</strong></a></td>' % (
                    ('--' if graph[1] == None or graph[1] == "" else graph[1]),
                    ('--' if graph[0] == None or graph[0] == "" else graph[0]))

                i += 1
            graph_detail += '</tr><tbody></table>'
            output_dict = {'success': 0, 'result': graph_detail}
            return output_dict
        else:
            return result_dict
