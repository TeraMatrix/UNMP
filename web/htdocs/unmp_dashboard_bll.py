#!/usr/bin/python2.6
from datetime import datetime, timedelta
import time

import MySQLdb
from common_controller import *
from error_message import ErrorMessageClass
from mysql_collection import mysql_connection
from nms_config import *
from odu_controller import *
from unmp_dashboard_config import DashboardConfig

global err_obj
err_obj = ErrorMessageClass()


class SelfException(Exception):
    """
    @return: this class return the exception msg.
    @rtype: dictionary
    @requires: Exception class package(module)
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """

    def __init__(self, msg):
        pass


class DashboardBll(object):
    def get_dashboard_data(self):
        devcie_type_attr = ['id', 'refresh_time', 'time_diffrence']
        get_data = DashboardConfig.get_config_attributes(
            'odu_dashboard', devcie_type_attr)
        odu_refresh_time = 10  # default time
        total_count = 180      # default count showing record
        if get_data is not None:
            if get_data[0][0] == 'odu_dashboard':
                odu_refresh_time = get_data[0][1]
                total_count = get_data[0][2]
        return str(odu_refresh_time), str(total_count)

    def common_graph_json(self, device_type, graph_id):
        time_list = []
        output_dic = {}
        json_data = []
        graph_title = "Device Reachability"
        graph_sub_title = ""
        normal = []
        inforamtional = []
        minor = []
        major = []
        critical = []
        table_html = ""
        image_dic = {0: "images/gr.png", 1: "images/lb.png", 2: "images/gr.png", 3:
            "images/yel.png", 4: "images/or.png", 5: "images/red.png"}
        image_title_name = {0: "Normal", 1: "Informationl", 2:
            "Normal", 3: "Minor", 4: "Major", 5: "Critical"}

        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)
            display_type = "graph"

            default_value = {'y': 0, 'marker': {'symbol':
                                                    'url(images/ab.png)'}}
            if display_type == 'table' or display_type == 'excel' or display_type == 'csv':
                default_value = 'Device Unreachable'
            elif display_type == 'pdf':
                default_value = 'DU'
            if str(graph_id).strip() == 'mouReachablity':
                sql = "SELECT agent_id,trap_event_id FROM system_alarm_table  inner join hosts on system_alarm_table.host_id = hosts.host_id \
                where hosts.is_deleted = 0 \
                group by  system_alarm_table.host_id order by system_alarm_table.timestamp"
                cursor.execute(sql)
                result = cursor.fetchall()
                result_list = [int(row[1]) for row in result]
                up_count = result_list.count(50002)
                down_count = result_list.count(50001)
                json_data.append({'up': up_count, 'down': down_count})
                graph_title = "Device Reachability"
                graph_sub_title = ""
            elif str(graph_id).strip() == 'mouEventGraph':
                sql = " SELECT count(ta.trap_event_id),ta.timestamp ,ta.serevity FROM trap_alarms as ta \
		inner join hosts on ta.agent_id = hosts.ip_address \
		 where  ta.timestamp <= NOW() and  ta.timestamp > DATE_SUB(NOW(), INTERVAL 180 MINUTE) and hosts.is_deleted = 0 \
		 group by serevity,ta.timestamp order by  ta.timestamp desc "
                cursor.execute(sql)
                trap_result = cursor.fetchall()
                if trap_result is not None:
                    # store the information in list.
                    for i in range(0, 6):
                        normal1 = 0
                        inforamtional1 = 0
                        minor1 = 0
                        major1 = 0
                        critical1 = 0
                        for row in trap_result:
                            if row[1] >= datetime.now() + timedelta(minutes=-(i + 1) * 30) and row[
                                1] <= datetime.now() + timedelta(minutes=-i * 30):
                                if int(row[2]) == 0:
                                    normal1 += int(row[0])
                                elif int(row[2]) == 2:
                                    normal1 += int(row[0])
                                elif int(row[2]) == 1:
                                    inforamtional1 += int(row[0])
                                elif int(row[2]) == 3:
                                    minor1 += int(row[0])
                                elif int(row[2]) == 4:
                                    major1 += int(row[0])
                                elif int(row[2]) == 5:
                                    critical1 += int(row[0])
                        time_list.append(time.mktime((datetime.now(
                        ) + timedelta(minutes=-(i + 1) * 30)).timetuple()) * 1000)
                        # time_list.append(str(datetime.now()+timedelta(minutes=-(i+1)*10)))
                        # time_list.append(str(time.mktime(datetime.now()+timedelta(minutes=-(i+1)*10))))
                        normal.append(normal1)
                        inforamtional.append(inforamtional1)
                        minor.append(minor1)
                        major.append(major1)
                        critical.append(critical1)

                # reverse the list
                # normal.reverse()
                # inforamtional.reverse()
                # minor.reverse()
                # major.reverse()
                # critical.reverse()
                # time_list.reverse()
                json_data.append(
                    {'normal': normal, 'inforamtional': inforamtional, 'minor': minor,
                     'major': major, 'critical': critical})
            elif str(graph_id).strip() == 'mouReachabilityTable':
                sql = " SELECT ta.serevity,ta.agent_id,device_type.device_name,ta.timestamp,ta.trap_alarm_current_id FROM trap_alarm_current as ta \
		inner join hosts on ta.agent_id = hosts.ip_address \
		inner join device_type on hosts.device_type_id = device_type.device_type_id \
		where  ta.trap_event_id = '50001' and hosts.is_deleted = 0 \
		order by  ta.timestamp desc limit 10"
                cursor.execute(sql)
                unreachable_device = cursor.fetchall()
                reachable_table = ""
                reachable_table += "\
		<table class=\"yo-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		<colgroup>\
		    <col style=\"width:5%%;\"/>\
		    <col style=\"width:20%%;\"/>\
		    <col style=\"width:25%%;\"/>\
		    <col style=\"width:20%%;\"/>\
		    <col style=\"width:30%%;\"/>\
		</colgroup>\
		<tr>\
		    <th >Status</th>\
		    <th >IP Address</th>\
		    <th >Device Type</th>\
		    <th >Time Duration</th>\
		    <th >Timestamp</th>\
		</tr>"
                if len(unreachable_device) > 0:
                    for row in unreachable_device:
                        hour = 0
                        minute = 0
                        second = 0
                        duration = "New"
                        minute, second = (0, 0) if (datetime.now() - row[3]).seconds < 60 else (
                            (datetime.now() - row[3]).seconds / 60, (datetime.now() - row[3]).seconds % 60)
                        hour, minute = (0, minute) if minute < 60 else (
                            minute / 60, minute % 60)

                        if int(hour) != 0 or int(minute) != 0:
                            duration = str(
                                hour) + " Hr " + str(minute) + " Min"
                        img = "<img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:12px\" onclick=\"alarmDetail(\'%s\',1)\"/>" % (
                            image_dic[int(row[0])], image_title_name[int(row[0])], image_title_name[int(row[0])],
                            int(row[4]))
                        reachable_table += "\
				<tr>\
				    <td >" + img + "</td>\
				    <td >" + row[1] + "</td>\
				    <td >" + row[2] + "</td>\
				    <td >" + str(paint_age(time.mktime(row[3].timetuple()), True, 60)) + "</td>\
				    <td >" + str(row[3].strftime("%c")) + "</td>\
				</tr>"
                else:
                    reachable_table += "\
			<tr>\
			    <td colspan=5>No Data exist.</td>\
			</tr>"

                reachable_table += "</table>"
                table_html = reachable_table
            elif str(graph_id).strip() == 'mouEventTable':
                sql = " SELECT ta.serevity,ta.agent_id,device_type.device_name,ta.trap_event_id,ta.trap_event_type,ta.timestamp,ta.trap_alarm_current_id \
		FROM trap_alarm_current as ta \
		inner join hosts on ta.agent_id = hosts.ip_address \
		inner join device_type on hosts.device_type_id = device_type.device_type_id \
		where  ta.trap_event_id <> '50001' and ta.trap_event_id <> '50002' and hosts.is_deleted = 0 \
		order by  ta.timestamp desc limit 7"
                cursor.execute(sql)
                unreachable_device = cursor.fetchall()
                reachable_table = ""
                reachable_table += "\
		<table class=\"yo-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		<colgroup>\
		    <col  style=\"width:2%%;\"/>\
		    <col  style=\"width:12%%;\"/>\
		    <col  style=\"width:12%%;\"/>\
		    <col  style=\"width:12%%;\"/>\
		    <col  style=\"width:28%%;\"/>\
		    <col  style=\"width:36%%;\"/>\
		</colgroup>\
		<tr>\
		    <th >Status</th>\
		    <th >IP Address</th>\
		    <th >Device Type</th>\
		    <th >Event ID</th>\
		    <th >Event Type</th>\
		    <th >Timestamp</th>\
		</tr>"

                if len(unreachable_device) > 0:
                    for row in unreachable_device:
                        img = "<img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:12px\" onclick=\"alarmDetail(\'%s\',1)\"/>" % (
                            image_dic[int(row[0])], image_title_name[int(row[0])], image_title_name[int(row[0])],
                            int(row[6]))
                        reachable_table += "\
				<tr>\
				    <td >" + img + "</td>\
				    <td >" + row[1] + "</td>\
				    <td >" + row[2] + "</td>\
				    <td >" + row[3] + "</td>\
				    <td >" + row[4] + "</td>\
				    <td >" + str(row[5].strftime("%c")) + "</td>\
				</tr>"
                else:
                    reachable_table += "\
			<tr>\
			    <td colspan=6>No Data exist.</td>\
			</tr>"

                reachable_table += "</table>"
                table_html = reachable_table
            elif table_name.strip() == 'outage':
                pass
            output_dic = {
                'success': 0, 'timestamp': time_list, 'data': json_data,
                'graph_title': graph_title, 'graph_sub_title': graph_sub_title, 'table_html': table_html}
            return output_dic
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if conn.open:
                conn.close()


def paint_age(timestamp, has_been_checked, bold_if_younger_than):
    """
    @return: this function return the host host status age.
    @rtype: this function return type string.
    @requires: this function take three argument 1. timestamp(total up tiem) , 2. this process checked or not(boolean value) , 3. total up time is grether than 10 min or not. .
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function return the host host status age.
    @organization: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    if not has_been_checked:
        return "age", "-"

    age = time.time() - timestamp
    if age < bold_if_younger_than:
        age_class = "age recent"
    else:
        return age_text(age)


    #    if age >= 48 * 3600 or age < -48 * 3600:
    #        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    # Time delta less than two days => make relative time

#    if age < 0:
#        age = -age
#        prefix = "in "
#    else:
#        prefix = ""
#    if age < bold_if_younger_than:
#        age_class = "age recent"
#    else:
#        age_class = "age"
#    return prefix + age_text(age)


def age_text(timedif):
    timedif = int(timedif)
    if timedif < 60:
        return "%d sec" % timedif

    minutes = timedif / 60
    if minutes < 60:
        return "%d min %d sec" % (minutes, timedif % 60)

    hours = minutes / 60
    if hours < 48:
        return "%d hrs %d min" % (hours, minutes % 60)

    days = hours / 24
    return "%d days" % days
