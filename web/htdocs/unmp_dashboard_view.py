#!/usr/bin/python2.6
from datetime import datetime
import time


class DashboardView(object):
    """
    UNMP Dashboard
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
        <div style=\"float: right; font-size: 10px; color: rgb(85, 85, 85); font-weight: bold; padding: 10px 20px;\" >\
        <input type=\"hidden\" name=\"sp_start_date\" value=\"%s\" id=\"sp_start_date\" style=\"width:100px;\"/>\
        <input type=\"hidden\" name=\"sp_start_time\" value=\"%s\" id=\"sp_start_time\" style=\"width:80px;\"/>\
        <input type=\"hidden\" name=\"sp_end_date\" value=\"%s\" id=\"sp_end_date\" style=\"width:100px;\"/>\
        <input type=\"hidden\" name=\"sp_end_time\" value=\"%s\" id=\"sp_end_time\" style=\"width:80px;\"/>\
        </div>\
        </div>\
        <table cellspacing="10px" cellpadding="0" width="100%%">\
        <colgroup>\
            <col width="50%%" style="width:50%%;"/>\
            <col width="50%%" style="width:50%%;"/>\
        </colgroup>\
        <tr>\
            <td><div id="dashboard1" class="db-box"></div></td>\
            <td><div id="dashboard2" class="db-box"></div></td>\
        </tr>\
        <tr>\
            <td><div id="dashboard3" class="db-box" style=\"overflow-x:hidden;overflow-y:auto;\"></div></td>\
            <td><div id="dashboard4" class="db-box" style=\"overflow-x:hidden;overflow-y:auto;\"></div></td>\
        </tr>\
		</table>\
		<div id="sp_main_graph"></div>\
        ' % (sp_refresh_time, ip_address, total_count, sp_start_date, sp_start_time, sp_end_date, sp_end_time)
        return dash_str
