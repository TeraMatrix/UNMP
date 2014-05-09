#!/usr/bin/python2.6


class ClientDashboardView(object):
    @staticmethod
    def header_buttons():
        add_btn = "<div class=\"header-icon\"><img onclick=\"hostInformation();\" class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"host_info\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Show Status\"></div>"
        del_btn = "<div class=\"header-icon\"><img onclick=\"delHost();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Host\"></div>".format(
            theme)
        header_btn = del_btn + add_btn
        return header_btn

    @staticmethod
    def sp_footer_tab(flag):
        if int(flag) == 0:
            html_page = '<div id=\"report_button_div\" class=\"form-div-footer\">\
            <table cellspacing="9px" cellpadding="0">\
            <tr>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"0\" name=\"option\" id=\"current_rept_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"current_rept_div\" width=\"25px\">Current Time</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"1\" name=\"option\" id=\"day1_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day1_rprt_div\" width=\"25px\">Today</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"2\" name=\"option\" id=\"day2_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day2_rprt_div\" width=\"25px\">2 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"3\" name=\"option\" id=\"day3_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day3_rprt_div\" width=\"25px\">3 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"4\" name=\"option\" id=\"week_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"week_rprt_div\" width=\"25px\">1 Week</label></td>\
         <td style="text-align:left"><button type=\"submit\" id=\"sp_excel_report\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="spExcelReportGeneration();"><span class=\"report\">Excel</span></button></td>\
         <td style="text-align:left"><button type=\"submit\" id=\"sp_csv_report\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="spCSVReportGeneration();"><span class=\"report\">CSV</span></button></td>\
            </tr></table>\
            </div></div>\
            '
        else:
            html_page = '</div>'
        return html_page

    #         <td style="text-align:left"><button type=\"submit\" id=\"sp_pdf_report\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="spPDFReportGeneration();"><span class=\"save\">PDF</span></button></td>\

    @staticmethod
    def sp_table(mac_address, sp_refresh_time, total_count, path, host_id):
        dash_str = '\
        <input type=\"hidden\" id=\"sp_refresh_time\" name=\"refresh_time\" value=\"%s\" />\
        <input type=\"hidden\" id=\"sp_mac_address\" name=\"mac_address\" value=\"%s\" />\
        <input type=\"hidden\" id=\"sp_total_count\" name=\"total_count\" value=\"%s\" />\
        <input type=\"hidden\" id=\"path_no\" name=\"path_no\" value=\"%s\" />\
        <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\" />\
        <div>\
        <table cellspacing="10px" cellpadding="0" width="100%%" style="margin-top:20px;"><tr><td>\
        <div id="more_graph_columns" style=\"float:right;\"></div>\
        </td><td style=\"vertical-align:bottom;\">\
        <input type=\"button\" id=\"apply_graph\" name=\"apply_graph\"  value=\"Apply\" onClick="show_graph_click();" class="yo-small yo-button"/>\
        </td></tr></table>\
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
        <span>Client State Information</span>\
        </div>\
        <div class="db-body">\
        <div class="db-container" style="height: 250px;overflow-y:auto;" id="client_dashboard">\
        </div>\
        </div>\
        </div>\
        </td>\
        <tr>\
        </table>\
        ' % (sp_refresh_time, mac_address, total_count, path, host_id, theme)
        return dash_str

    @staticmethod
    def client_information_view(result):
        # this is common list
        device_detail = ''
        if len(result['result']) > 0:
            result = result['result'][0]
            device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
            device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Client Status\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                AP Alias\
                            </td>\
                            <td class="cell-info">' + str(
                '--' if result[0] == None or result[0] == ""  else result[0]) + '</td>\
                            <td class="cell-label">\
                                Client Alias\
                            </td>\
                            <td class="cell-info">' + str(
                '--' if result[1] == None or result[1] == ""  else result[1]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                MAC Address\
                            </td>\
                            <td class="cell-info">' + str(
                '--' if result[2] == None or result[2] == ""  else result[2]) + '</td>\
                            <td class="cell-label">\
                                RSSI\
                            </td>\
                            <td class="cell-info">' + str(
                '--' if result[3] == None or result[3] == ""  else result[3]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                VAP\
                            </td>\
                            <td class="cell-info">' + str(
                '--' if result[4] == None or result[4] == ""  else result[4]) + '</td>\
                            <td class="cell-label">\
                                Total Tx(Mbps)\
                            </td>\
                            <td class="cell-info">' + str('--' if result[5] == None or result[5] == "" else result[5]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Total Rx(Mbps)\
                            </td>\
                            <td class="cell-info">' + str(
                '--' if result[6] == None or result[6] == ""  else result[6]) + '</td>\
                            </tr>\
                        <tbody></table>'
        else:
            device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
            device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Client Status\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                AP\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Client Alias\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                MAC Address\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                RSSI\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                VAP\
                            </td>\
                            <td class="cell-info">--</td>\
                            <td class="cell-label">\
                                Total Tx(Mbps)\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
			   <tr>\
                            <td class="cell-label">\
                                Total Rx(Mbps)\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                        <tbody></table>'
        return device_detail

    @staticmethod
    def sp_ap_client_table_view(result):
        Client_table = '<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
        Client_table += '\
			<colgroup><col style="width:3%;"/><col style="width:11%;"/><col style="width:10%;"/><col style="width:6%;"/><col style="width:6%;"/><col style="width:10%;"/><col style="width:10%;"/><col style="width:10%;"/><col style="width:10%;"/><col style="width:10%;"/>\
  </colgroup>\
        <tr class="yo-table-head">\
            <th >No.</th>\
            <th >Client Alias</th>\
            <th >MAC Adddress</th>\
            <th >Total Tx(Mbps)</th>\
            <th >Total Rx(Mbps)</th>\
            <th >First Seen Time</th>\
            <th >First Seen AP</th>\
            <th >Last Seen Time</th>\
            <th >Last Seen AP</th>\
            <th >Current Client Connectivity status</th>\
        </tr>'
        new_result = result['result']
        count_no = 1
        for i in new_result:
            Client_table += '<tr><td>%s</td>' % count_no
            Client_table += '<td>%s</td>' % (
                "--" if i[0] == None or i[0] == "" else i[0])
            Client_table += '<td>%s</td>' % (
                "--" if i[1] == None or i[1] == "" else i[1])
            Client_table += '<td>%s</td>' % (
                "--" if i[2] == None or i[2] == "" else i[2])
            Client_table += '<td>%s</td>' % (
                "--" if i[3] == None or i[3] == "" else i[3])
            Client_table += '<td>%s</td>' % (
                "--" if i[4] == None or i[4] == "" else i[4])
            Client_table += '<td>%s</td>' % (
                "--" if i[5] == None or i[5] == "" else i[5])
            Client_table += '<td>%s</td>' % (
                "--" if i[6] == None or i[6] == "" else i[6])
            Client_table += '<td>%s</td>' % (
                "--" if i[7] == None or i[7] == "" else i[7])
            Client_table += '<td>%s</td></tr>' % (
                "--" if i[8] == None or i[8] == "" else i[8])
            count_no += 1
        if len(new_result) < 1:
            Client_table += '<tr ><td colspan="10"><b>Client Information does not exists.</b></td></tr>'
        return {'success': 0, 'client_table': Client_table}

    @staticmethod
    def sp_get_graph(selected_columns, non_selected_columns):
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
