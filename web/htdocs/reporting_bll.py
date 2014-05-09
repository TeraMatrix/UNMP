#!/usr/bin/python2.6
"""
@author: Mahipal Choudhary
@since: 07-Nov-2011
@version: 0.1
@note: All database related functions Related with Reporting.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""

# Import modules that contain the function and libraries
from datetime import timedelta, datetime
from operator import itemgetter

import MySQLdb
import xlwt
from inventory_bll import HostBll
from main_reporting_bll import MainOutage
from mysql_collection import mysql_connection
from unmp_config import SystemConfig


class Report_bll(object):
    """
    Main reporting related BLL class
    """
# AVERAGE DATA FOR GIVEN DATE PERIOD
    def get_avg_data_for_two_dates(self, no_of_devices, date1, date2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param all_group:
        @param all_host:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            d1 = datetime.strptime(date1, "%d-%m-%Y")
            d2 = datetime.strptime(date2, "%d-%m-%Y")
            average_list = []
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            if all_host == "" and all_group == "":
                while (d1 <= d2):
                    date_temp = str(d1)[:10]
                    query = "Select date(go16.timestamp),hosts.host_name ,hosts.ip_address, AVG(go16.rx_phy_error) , AVG(go16.rx_crc_errors),hostgroups.hostgroup_name\
        	               from get_odu16_ra_tdd_mac_statistics_entry  as go16\
        	               join ( select host_id,host_name,ip_address,mac_address,host_alias from hosts where device_type_id like 'ODU16%%' group by host_id) as hosts\
                           INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                           INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
        	               where go16.host_id=hosts.host_id and go16.timestamp between '%s 00:00:00' and '%s 23:59:59' and go16.rx_phy_error<>123456789 and go16.rx_phy_error<>987654321\
        	               group by go16.host_id limit %s " % (date_temp, date_temp, no_of_devices)
                    cursor.execute(query)
                    avg_result = cursor.fetchall()
                    d1 = d1 + timedelta(days=1)
                    for avg in avg_result:
                        average_list.append(make_list(avg))
            else:
                while (d1 <= d2):
                    date_temp = str(d1)[:10]
                    host_data = str(all_host.split(
                        ',')).replace('[', '(').replace(']', ')')
                    query = "Select date(go16.timestamp),hosts.host_name,hosts.ip_address, AVG(go16.rx_phy_error) , AVG(go16.rx_crc_errors),hostgroups.hostgroup_name\
        	               from get_odu16_ra_tdd_mac_statistics_entry  as go16\
        	               join ( select host_id,host_name,ip_address,mac_address,host_alias from hosts where device_type_id like 'ODU16%%' group by host_id) as hosts\
                           INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                           INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
        	               where go16.host_id=hosts.host_id and go16.timestamp between '%s 00:00:00' and '%s 23:59:59' and go16.rx_phy_error<>123456789 and go16.rx_phy_error<>987654321\
				AND hosts.host_id IN %s\
        	               group by go16.host_id " % (date_temp, date_temp, host_data)
                    cursor.execute(query)
                    avg_result = cursor.fetchall()
                    d1 = d1 + timedelta(days=1)
                    for avg in avg_result:
                        average_list.append(make_list(avg))
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = average_list
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

        # TOTAL DATA FOR A GIVEN DATE PERIOD

    def get_total_data_for_two_dates(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_group:
        @param all_host:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            date1 = date1 + " " + time1
            date2 = date2 + " " + time2
            d1 = datetime.strptime(date1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(date2, "%d-%m-%Y %H:%M")
            total_list = []
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            date_temp_1 = str(d1)
            date_temp_2 = str(d2)
            if all_group == '' and all_host == '':
                query = "Select go16.timestamp,hst.host_name,hst.ip_address,go16.rx_phy_error,go16.rx_crc_errors,hostgroups.hostgroup_name from get_odu16_ra_tdd_mac_statistics_entry  as go16\
                        join ( select host_id,host_name,ip_address,host_alias from hosts where device_type_id like 'ODU16%%' group by host_id limit %s) as hst\
                        on go16.host_id=hst.host_id\
                       INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id\
                       INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                        where go16.timestamp between '%s' and '%s' \
                       order by hst.host_id,go16.timestamp asc  " % (no_of_devices, date_temp_1, date_temp_2)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    result_dict = {"success": 0, "result": []}
                    return result_dict
                li = []
                tr = []
                host = res[0][1]
                for i in range(len(res)):
                    li = make_list(res[i])
                    if (str(li[3]) == "123456789" or str(li[4]) == "123456789"):
                        li[3] = "DEVICE WAS OFF"
                        li[4] = "DEVICE WAS OFF"
                        li.insert(5, "0")
                        li.insert(6, "0")
                    elif str(li[3]) == "987654321" or str(li[4]) == "987654321":
                        li[3] = "DEVICE WAS DISABLED"
                        li[4] = "DEVICE WAS DISABLED"
                        li.insert(5, "0")
                        li.insert(6, "0")
                    elif i == 0 or host != li[1]:
                        li[3] = "0"
                        li[4] = "0"
                        li.insert(5, "0")
                        li.insert(6, "0")
                    elif host == li[1]:
                        var_phy_cur = res[i][3]
                        var_crc_cur = res[i][4]
                        var_phy_old = res[i - 1][3]
                        var_crc_old = res[i - 1][4]
                        if str(var_crc_old) == "123456789" or str(var_phy_old) == "123456789" or str(
                                var_crc_old) == "987654321" or str(var_phy_old) == "987654321":
                            temp_crc = var_crc_cur
                            temp_phy = var_phy_cur
                        else:
                            temp_crc = var_crc_cur - var_crc_old
                            temp_phy = var_phy_cur - var_phy_old
                            if (temp_crc < 0):
                                temp_crc = 0
                            if (temp_phy < 0):
                                temp_phy = 0
                        li.insert(5, str(temp_phy))
                        li.insert(6, str(temp_crc))
                    tr.append(li)
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query = "Select go16.timestamp,hst.host_name,hst.ip_address,go16.rx_phy_error,go16.rx_crc_errors,hostgroups.hostgroup_name from get_odu16_ra_tdd_mac_statistics_entry  as go16 \
                    join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU16%%' group by host_id) as hst on go16.host_id=hst.host_id \
                    INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id \
                    INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                    where go16.timestamp between '%s' and '%s' AND hst.host_id IN %s order by hst.host_id,go16.timestamp asc " % (
                date_temp_1, date_temp_2, host_data)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    result_dict = {"success": 0, "result": []}
                    return result_dict
                li = []
                tr = []
                host = res[0][1]
                for i in range(len(res)):
                    li = make_list(res[i])
                    if (str(li[3]) == "123456789" or str(li[4]) == "123456789"):
                        li[3] = "DEVICE WAS OFF"
                        li[4] = "DEVICE WAS OFF"
                        li.insert(5, "0")
                        li.insert(6, "0")
                    elif str(li[3]) == "987654321" or str(li[4]) == "987654321":
                        li[3] = "DEVICE WAS DISABLED"
                        li[4] = "DEVICE WAS DISABLED"
                        li.insert(5, "0")
                        li.insert(6, "0")
                    elif i == 0 or host != li[1]:
                        li[3] = "0"
                        li[4] = "0"
                        li.insert(5, "0")
                        li.insert(6, "0")
                    elif host == li[1]:
                        var_phy_cur = res[i][3]
                        var_crc_cur = res[i][4]
                        var_phy_old = res[i - 1][3]
                        var_crc_old = res[i - 1][4]
                        if str(var_crc_old) == "123456789" or str(var_phy_old) == "123456789" or str(
                                var_crc_old) == "987654321" or str(var_phy_old) == "987654321":
                            temp_crc = var_crc_cur
                            temp_phy = var_phy_cur
                        else:
                            temp_crc = var_crc_cur - var_crc_old
                            temp_phy = var_phy_cur - var_phy_old
                            if (temp_crc < 0):
                                temp_crc = 0
                            if (temp_phy < 0):
                                temp_phy = 0
                        li.insert(5, str(temp_phy))
                        li.insert(6, str(temp_crc))
                    tr.append(li)
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = tr
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

        # TOTAL DATA FOR A GIVEN DATE PERIOD FOR SYNC LOSS COUNTER

    def get_synch_loss_for_two_dates(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_group:
        @param all_host:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            date1 = date1 + " " + time1
            date2 = date2 + " " + time2
            d1 = datetime.strptime(date1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(date2, "%d-%m-%Y %H:%M")
            total_list = []
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            date_temp_1 = str(d1)
            date_temp_2 = str(d2)
            if all_group == '' and all_host == '':
                query = " Select go16.timestamp,hst.host_name,hst.ip_address,hst.host_alias,go16.sysc_lost_counter,hostgroups.hostgroup_name from get_odu16_synch_statistics_table  as go16\
                        join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU16%%' group by host_id limit %s) as hst\
                        on go16.host_id=hst.host_id\
                       INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id\
                       INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                        where go16.timestamp between '%s' and '%s' \
                       order by hst.host_id,go16.timestamp asc " % (no_of_devices, date_temp_1, date_temp_2)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    result_dict = {"success": 0, "result": []}
                    return result_dict
                li = []
                tr = []
                host = res[0][1]
                for i in range(len(res)):
                    li = make_list(res[i])  # work from here
                    if (str(li[4]) == "123456789"):
                        li[4] = "DEVICE WAS OFF"
                    elif str(li[4]) == "987654321":
                        li[4] = "DEVICE WAS DISABLED"
                    elif i == 0:
                        continue
                    elif host == res[i][1]:
                        var_synch_cur = res[i][4]
                        var_synch_old = res[i - 1][4]
                        if str(var_synch_old) == "123456789" or str(var_synch_old) == "987654321":
                            temp_synch = 0
                        else:
                            temp_synch = var_synch_cur - var_synch_old
                            if (temp_synch < 0):
                                temp_synch = 0
                        li[4] = str(temp_synch)
                    else:
                        li[4] = "0"
                    tr.append(li)
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query = " Select go16.timestamp,hst.host_name,hst.ip_address,hst.host_alias,go16.sysc_lost_counter,hostgroups.hostgroup_name from get_odu16_synch_statistics_table  as go16\
                        join ( select host_id,host_name,ip_address,host_alias from hosts where device_type_id like 'ODU16%%' group by host_id limit %s) as hst\
                        on go16.host_id=hst.host_id\
                       INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id\
                       INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                       where go16.timestamp between '%s' and '%s' AND hst.host_id IN %s   \
                       order by hst.host_id,go16.timestamp asc " % (no_of_devices, date_temp_1, date_temp_2, host_data)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    result_dict = {"success": 0, "result": []}
                    return result_dict
                li = []
                tr = []
                host = res[0][1]
                for i in range(len(res)):
                    li = make_list(res[i])  # work from here
                    if (str(li[4]) == "123456789"):
                        li[4] = "DEVICE WAS OFF"
                    elif str(li[4]) == "987654321":
                        li[4] = "DEVICE WAS DISABLED"
                    elif i == 0:
                        continue
                    elif host == res[i][1]:
                        var_synch_cur = res[i][4]
                        var_synch_old = res[i - 1][4]
                        if str(var_synch_old) == "123456789" or str(var_synch_old) == "987654321":
                            temp_synch = 0
                        else:
                            temp_synch = var_synch_cur - var_synch_old
                            if (temp_synch < 0):
                                temp_synch = 0
                        li[4] = str(temp_synch)
                    else:
                        li[4] = "0"
                    tr.append(li)
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = tr
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

        # AVERAGE DATA FOR GIVEN DATE PERIOD  FOR RSSI

    def get_avg_data_for_two_dates_rssi(self, no_of_devices, date1, date2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param all_group:
        @param all_host:
        @return:
        """
        host_name = []
        ip_address = []
        grp_name = []
        signal_interface1 = []
        signal_interface2 = []
        signal_interface3 = []
        signal_interface4 = []
        signal_interface5 = []
        signal_interface6 = []
        signal_interface7 = []
        signal_interface8 = []
        time_stamp_signal1 = []
        default_list = [0, 0, 0, 0, 0, 0, 0, 0]
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            d1 = datetime.strptime(date1, "%d-%m-%Y")
            d2 = datetime.strptime(date2, "%d-%m-%Y")
            average_list = []
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            if all_group == '' and all_host == '':
                while (d1 <= d2):
                    flag = 0
                    date_temp = str(d1)[:10]
                    query = "Select date(go16.timestamp), hosts.host_name , hosts.ip_address , AVG(go16.sig_strength), go16.timeslot_index , hostgroups.hostgroup_name , go16.ssidentifier \
                    from get_odu16_peer_node_status_table AS go16\
                    join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU16%%' group by host_id limit %s ) as hosts\
                    INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                    INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                    where go16.host_id=hosts.host_id and go16.timestamp between '%s 00:00:00' and '%s 23:59:59' and go16.sig_strength<>'-110' and go16.sig_strength<>'-111' \
                    group by go16.host_id,go16.timeslot_index " % (no_of_devices, date_temp, date_temp)
                    cursor.execute(query)
                    signal_strength = cursor.fetchall()
                    d1 = d1 + timedelta(days=1)
                    i = 0
                    for k in range(0, len(signal_strength) - 1):
                        i = k
                        flag = 1
                        if signal_strength[k][6] == '-1' or str(signal_strength[k][3]).strip() == '' or str(
                                signal_strength[0][4]).strip() == '':
                            pass
                        #			    grp_name.append(signal_strength[k][5])
                        #			    host_name.append(signal_strength[k][1])
                        #			    ip_address.append(signal_strength[k][2])
                        #			    signal_interface1.append(0)
                        #			    signal_interface2.append(0)
                        #			    signal_interface3.append(0)
                        #			    signal_interface4.append(0)
                        #			    signal_interface5.append(0)
                        #			    signal_interface6.append(0)
                        #			    signal_interface7.append(0)
                        #			    signal_interface8.append(0)
                        # time_stamp_signal1.append(str((signal_strength[k][0]).strftime('%d-%m-%Y
                        # %H:%M')))
                        else:
                            index = 1 if signal_strength[k][
                                             4] == '' else int(signal_strength[k][4])
                            if signal_strength[k][0] == signal_strength[k + 1][0]:
                                default_list[
                                    int(index) - 1] = int(signal_strength[k][3])
                            else:
                                default_list[
                                    int(index) - 1] = int(signal_strength[k][3])
                                grp_name.append(signal_strength[k][5])
                                host_name.append(signal_strength[k][1])
                                ip_address.append(signal_strength[k][2])
                                signal_interface1.append(default_list[0])
                                signal_interface2.append(default_list[1])
                                signal_interface3.append(default_list[2])
                                signal_interface4.append(default_list[3])
                                signal_interface5.append(default_list[4])
                                signal_interface6.append(default_list[5])
                                signal_interface7.append(default_list[6])
                                signal_interface8.append(default_list[7])
                                time_stamp_signal1.append(str(
                                    (signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                                default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                    if len(signal_strength) > 0 and flag == 0:
                        if signal_strength[0][6] == '-1' or str(signal_strength[0][3]).strip() == '' or str(
                                signal_strength[0][4]).strip() == '':
                            grp_name.append(signal_strength[0][5])
                            host_name.append(signal_strength[0][1])
                            ip_address.append(signal_strength[0][2])
                            signal_interface1.append(0)
                            signal_interface2.append(0)
                            signal_interface3.append(0)
                            signal_interface4.append(0)
                            signal_interface5.append(0)
                            signal_interface6.append(0)
                            signal_interface7.append(0)
                            signal_interface8.append(0)
                            time_stamp_signal1.append(
                                str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                        else:
                            default_list[int(signal_strength[
                                0][4]) - 1] = int(signal_strength[0][3])
                            grp_name.append(signal_strength[0][5])
                            host_name.append(signal_strength[0][1])
                            ip_address.append(signal_strength[0][2])
                            signal_interface1.append(default_list[0])
                            signal_interface2.append(default_list[1])
                            signal_interface3.append(default_list[2])
                            signal_interface4.append(default_list[3])
                            signal_interface5.append(default_list[4])
                            signal_interface6.append(default_list[5])
                            signal_interface7.append(default_list[6])
                            signal_interface8.append(default_list[7])
                            time_stamp_signal1.append(
                                str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                    if len(signal_strength) > 0 and flag == 1:
                        if signal_strength[i + 1][6] == '-1' or str(signal_strength[i + 1][3]).strip() == '' or str(
                                signal_strength[i + 1][4]).strip() == '':
                            grp_name.append(signal_strength[i + 1][5])
                            host_name.append(signal_strength[i + 1][1])
                            ip_address.append(signal_strength[i + 1][2])
                            signal_interface1.append(0)
                            signal_interface2.append(0)
                            signal_interface3.append(0)
                            signal_interface4.append(0)
                            signal_interface5.append(0)
                            signal_interface6.append(0)
                            signal_interface7.append(0)
                            signal_interface8.append(0)
                            time_stamp_signal1.append(str(
                                (signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                        else:
                            default_list[int(signal_strength[
                                i + 1][4]) - 1] = int(signal_strength[0][3])
                            grp_name.append(signal_strength[i + 1][5])
                            host_name.append(signal_strength[i + 1][1])
                            ip_address.append(signal_strength[i + 1][2])
                            signal_interface1.append(default_list[0])
                            signal_interface2.append(default_list[1])
                            signal_interface3.append(default_list[2])
                            signal_interface4.append(default_list[3])
                            signal_interface5.append(default_list[4])
                            signal_interface6.append(default_list[5])
                            signal_interface7.append(default_list[6])
                            signal_interface8.append(default_list[7])
                            time_stamp_signal1.append(str(
                                (signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                for k in range(0, len(time_stamp_signal1)):
                    average_list.append(
                        [time_stamp_signal1[k], host_name[k], ip_address[k], signal_interface1[k], signal_interface2[k],
                         signal_interface3[k], signal_interface4[k],
                         signal_interface5[k], signal_interface6[k], signal_interface7[k], signal_interface8[k],
                         grp_name[k]])
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                while (d1 <= d2):
                    flag = 0
                    date_temp = str(d1)[:10]
                    query = "Select date(go16.timestamp), hosts.host_name , hosts.ip_address , AVG(go16.sig_strength), go16.timeslot_index,hostgroups.hostgroup_name,go16.ssidentifier \
			       from get_odu16_peer_node_status_table AS go16\
			       join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU16%%' group by host_id ) as hosts\
			       INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
			       INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
			       where go16.host_id=hosts.host_id and go16.timestamp between '%s 00:00:00' and '%s 23:59:59' and go16.sig_strength<>'-110' and go16.sig_strength<>'-111' \
			       AND hosts.host_id IN %s group by go16.host_id,go16.timeslot_index " % (
                    date_temp, date_temp, host_data)
                    cursor.execute(query)
                    signal_strength = cursor.fetchall()
                    d1 = d1 + timedelta(days=1)
                    i = 0
                    for k in range(0, len(signal_strength) - 1):
                        i = k
                        flag = 1
                        if signal_strength[k][6] == '-1' or str(signal_strength[k][3]).strip() == '' or str(
                                signal_strength[0][4]).strip() == '':
                            pass
                        #				    grp_name.append(signal_strength[k][5])
                        #				    host_name.append(signal_strength[k][1])
                        #				    ip_address.append(signal_strength[k][2])
                        #				    signal_interface1.append(0)
                        #				    signal_interface2.append(0)
                        #				    signal_interface3.append(0)
                        #				    signal_interface4.append(0)
                        #				    signal_interface5.append(0)
                        #				    signal_interface6.append(0)
                        #				    signal_interface7.append(0)
                        #				    signal_interface8.append(0)
                        # time_stamp_signal1.append(str((signal_strength[k][0]).strftime('%d-%m-%Y
                        # %H:%M')))
                        else:
                            index = 1 if signal_strength[k][
                                             4] == '' else int(signal_strength[k][4])
                            if signal_strength[k][0] == signal_strength[k + 1][0]:
                                default_list[
                                    int(index) - 1] = int(signal_strength[k][3])
                            else:
                                default_list[
                                    int(index) - 1] = int(signal_strength[k][3])
                                grp_name.append(signal_strength[k][5])
                                host_name.append(signal_strength[k][1])
                                ip_address.append(signal_strength[k][2])
                                signal_interface1.append(default_list[0])
                                signal_interface2.append(default_list[1])
                                signal_interface3.append(default_list[2])
                                signal_interface4.append(default_list[3])
                                signal_interface5.append(default_list[4])
                                signal_interface6.append(default_list[5])
                                signal_interface7.append(default_list[6])
                                signal_interface8.append(default_list[7])
                                time_stamp_signal1.append(str(
                                    (signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                                default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                    if len(signal_strength) > 0 and flag == 0:
                        if signal_strength[0][6] == '-1' or str(signal_strength[0][3]).strip() == '' or str(
                                signal_strength[0][4]).strip() == '':
                            grp_name.append(signal_strength[0][5])
                            host_name.append(signal_strength[0][1])
                            ip_address.append(signal_strength[0][2])
                            signal_interface1.append(0)
                            signal_interface2.append(0)
                            signal_interface3.append(0)
                            signal_interface4.append(0)
                            signal_interface5.append(0)
                            signal_interface6.append(0)
                            signal_interface7.append(0)
                            signal_interface8.append(0)
                            time_stamp_signal1.append(
                                str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                        else:
                            default_list[int(signal_strength[
                                0][4]) - 1] = int(signal_strength[0][3])
                            grp_name.append(signal_strength[0][5])
                            host_name.append(signal_strength[0][1])
                            ip_address.append(signal_strength[0][2])
                            signal_interface1.append(default_list[0])
                            signal_interface2.append(default_list[1])
                            signal_interface3.append(default_list[2])
                            signal_interface4.append(default_list[3])
                            signal_interface5.append(default_list[4])
                            signal_interface6.append(default_list[5])
                            signal_interface7.append(default_list[6])
                            signal_interface8.append(default_list[7])
                            time_stamp_signal1.append(
                                str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                    if len(signal_strength) > 0 and flag == 1:
                        if signal_strength[i + 1][6] == '-1' or str(signal_strength[i + 1][3]).strip() == '' or str(
                                signal_strength[i + 1][4]).strip() == '':
                            grp_name.append(signal_strength[i + 1][5])
                            host_name.append(signal_strength[i + 1][1])
                            ip_address.append(signal_strength[i + 1][2])
                            signal_interface1.append(0)
                            signal_interface2.append(0)
                            signal_interface3.append(0)
                            signal_interface4.append(0)
                            signal_interface5.append(0)
                            signal_interface6.append(0)
                            signal_interface7.append(0)
                            signal_interface8.append(0)
                            time_stamp_signal1.append(str(
                                (signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                        else:
                            default_list[int(signal_strength[
                                i + 1][4]) - 1] = int(signal_strength[0][3])
                            grp_name.append(signal_strength[i + 1][5])
                            host_name.append(signal_strength[i + 1][1])
                            ip_address.append(signal_strength[i + 1][2])
                            signal_interface1.append(default_list[0])
                            signal_interface2.append(default_list[1])
                            signal_interface3.append(default_list[2])
                            signal_interface4.append(default_list[3])
                            signal_interface5.append(default_list[4])
                            signal_interface6.append(default_list[5])
                            signal_interface7.append(default_list[6])
                            signal_interface8.append(default_list[7])
                            time_stamp_signal1.append(str(
                                (signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                for k in range(0, len(time_stamp_signal1)):
                    average_list.append(
                        [time_stamp_signal1[k], host_name[k], ip_address[k], signal_interface1[k], signal_interface2[k],
                         signal_interface3[k], signal_interface4[k],
                         signal_interface5[k], signal_interface6[k], signal_interface7[k], signal_interface8[k],
                         grp_name[k]])
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = average_list
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

        # TOTAL DATA FOR A GIVEN DATE PERIOD FOR RSSI

    def get_total_data_for_two_dates_rssi(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_group:
        @param all_host:
        @return:
        """
        flag = 1
        host_name = []
        ip_address = []
        grp_name = []
        signal_interface1 = []
        signal_interface2 = []
        signal_interface3 = []
        signal_interface4 = []
        signal_interface5 = []
        signal_interface6 = []
        signal_interface7 = []
        signal_interface8 = []
        time_stamp_signal1 = []
        default_list = [0, 0, 0, 0, 0, 0, 0, 0]
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            date1 = date1 + " " + time1
            date2 = date2 + " " + time2
            d1 = datetime.strptime(date1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(date2, "%d-%m-%Y %H:%M")
            total_list = []
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            date_temp_1 = str(d1)
            date_temp_2 = str(d2)
            if all_group == '' and all_host == '':
                query = "Select go16.timestamp , hst.host_name , hst.ip_address , go16.sig_strength, go16.timeslot_index,hostgroups.hostgroup_name,go16.ssidentifier from get_odu16_peer_node_status_table  as go16\
                    join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU16%%' group by host_id limit %s) as hst ON go16.host_id=hst.host_id\
                    INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id\
                    INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                    where go16.timestamp between '%s' and '%s'\
                    order by go16.timestamp asc,hst.host_name asc,go16.timeslot_index asc" % (
                no_of_devices, date_temp_1, date_temp_2)
                cursor.execute(query)
                #                total_result=cursor.fetchall()
                # 		sig_strength=3 , timeslot_index=4 , ssidentifier=6
                signal_strength = cursor.fetchall()
                i = 0
                for k in range(0, len(signal_strength) - 1):
                    i = k
                    flag = 1
                    # if signal_strength[k][6]=='-1' or
                    # str(signal_strength[k][3]).strip()=='-110' or
                    # str(signal_strength[0][4]).strip()=='':
                    if str(signal_strength[k][3]).strip() == '-110':
                    #			    pass
                        grp_name.append(signal_strength[k][5])
                        host_name.append(signal_strength[k][1])
                        ip_address.append(signal_strength[k][2])
                        signal_interface1.append("DEVICE WAS OFF")
                        signal_interface2.append("DEVICE WAS OFF")
                        signal_interface3.append("DEVICE WAS OFF")
                        signal_interface4.append("DEVICE WAS OFF")
                        signal_interface5.append("DEVICE WAS OFF")
                        signal_interface6.append("DEVICE WAS OFF")
                        signal_interface7.append("DEVICE WAS OFF")
                        signal_interface8.append("DEVICE WAS OFF")
                        time_stamp_signal1.append(
                            str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                    elif str(signal_strength[k][3]).strip() == '-111':
                    #			    pass
                        grp_name.append(signal_strength[k][5])
                        host_name.append(signal_strength[k][1])
                        ip_address.append(signal_strength[k][2])
                        signal_interface1.append("DEVICE WAS DISABLED")
                        signal_interface2.append("DEVICE WAS DISABLED")
                        signal_interface3.append("DEVICE WAS DISABLED")
                        signal_interface4.append("DEVICE WAS DISABLED")
                        signal_interface5.append("DEVICE WAS DISABLED")
                        signal_interface6.append("DEVICE WAS DISABLED")
                        signal_interface7.append("DEVICE WAS DISABLED")
                        signal_interface8.append("DEVICE WAS DISABLED")
                        time_stamp_signal1.append(
                            str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                    else:
                        index = 1 if signal_strength[k][
                                         4] == '' else int(signal_strength[k][4])
                        if signal_strength[k][0].strftime('%d-%m-%Y %H:%M') == signal_strength[k + 1][0].strftime(
                                '%d-%m-%Y %H:%M'):
                            default_list[int(
                                index) - 1] = int(signal_strength[k][3])
                        else:
                            default_list[int(
                                index) - 1] = int(signal_strength[k][3])
                            grp_name.append(signal_strength[k][5])
                            host_name.append(signal_strength[k][1])
                            ip_address.append(signal_strength[k][2])
                            signal_interface1.append(default_list[0])
                            signal_interface2.append(default_list[1])
                            signal_interface3.append(default_list[2])
                            signal_interface4.append(default_list[3])
                            signal_interface5.append(default_list[4])
                            signal_interface6.append(default_list[5])
                            signal_interface7.append(default_list[6])
                            signal_interface8.append(default_list[7])
                            time_stamp_signal1.append(
                                str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                if len(signal_strength) > 0 and flag == 0:  # single entry flag!=-1
                    if signal_strength[0][6] == '-1' or str(signal_strength[0][3]).strip() == '' or str(
                            signal_strength[0][4]).strip() == '':
                        grp_name.append(signal_strength[0][5])
                        host_name.append(signal_strength[0][1])
                        ip_address.append(signal_strength[0][2])
                        signal_interface1.append(0)
                        signal_interface2.append(0)
                        signal_interface3.append(0)
                        signal_interface4.append(0)
                        signal_interface5.append(0)
                        signal_interface6.append(0)
                        signal_interface7.append(0)
                        signal_interface8.append(0)
                        time_stamp_signal1.append(
                            str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                    else:
                        default_list[int(
                            signal_strength[0][4]) - 1] = int(signal_strength[0][3])
                        grp_name.append(signal_strength[0][5])
                        host_name.append(signal_strength[0][1])
                        ip_address.append(signal_strength[0][2])
                        signal_interface1.append(default_list[0])
                        signal_interface2.append(default_list[1])
                        signal_interface3.append(default_list[2])
                        signal_interface4.append(default_list[3])
                        signal_interface5.append(default_list[4])
                        signal_interface6.append(default_list[5])
                        signal_interface7.append(default_list[6])
                        signal_interface8.append(default_list[7])
                        time_stamp_signal1.append(
                            str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                if len(signal_strength) > 0 and flag == 1:  # loop sey out , for last entry
                    if signal_strength[i + 1][6] == '-1' or str(signal_strength[i + 1][3]).strip() == '' or str(
                            signal_strength[i + 1][4]).strip() == '':
                        grp_name.append(signal_strength[i + 1][5])
                        host_name.append(signal_strength[i + 1][1])
                        ip_address.append(signal_strength[i + 1][2])
                        signal_interface1.append(0)
                        signal_interface2.append(0)
                        signal_interface3.append(0)
                        signal_interface4.append(0)
                        signal_interface5.append(0)
                        signal_interface6.append(0)
                        signal_interface7.append(0)
                        signal_interface8.append(0)
                        time_stamp_signal1.append(
                            str((signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                    else:
                        default_list[int(signal_strength[
                            i + 1][4]) - 1] = int(signal_strength[0][3])
                        grp_name.append(signal_strength[i + 1][5])
                        host_name.append(signal_strength[i + 1][1])
                        ip_address.append(signal_strength[i + 1][2])
                        signal_interface1.append(default_list[0])
                        signal_interface2.append(default_list[1])
                        signal_interface3.append(default_list[2])
                        signal_interface4.append(default_list[3])
                        signal_interface5.append(default_list[4])
                        signal_interface6.append(default_list[5])
                        signal_interface7.append(default_list[6])
                        signal_interface8.append(default_list[7])
                        time_stamp_signal1.append(
                            str((signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                    # make the RSSI 2'd list
                for k in range(0, len(time_stamp_signal1)):
                    total_list.append(
                        [time_stamp_signal1[k], host_name[k], ip_address[k], signal_interface1[k], signal_interface2[k],
                         signal_interface3[k], signal_interface4[k],
                         signal_interface5[k], signal_interface6[k], signal_interface7[k], signal_interface8[k],
                         grp_name[k]])
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query = "Select go16.timestamp , hst.host_name , hst.ip_address , go16.sig_strength, go16.timeslot_index,hostgroups.hostgroup_name,go16.ssidentifier from get_odu16_peer_node_status_table  as go16\
                join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU16%%' group by host_id) as hst ON go16.host_id=hst.host_id\
                INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id\
                INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                where go16.timestamp between '%s' and '%s' AND hst.host_id IN %s order by go16.timestamp asc ,hst.host_name asc, go16.timeslot_index asc" % (
                date_temp_1, date_temp_2, host_data)
                cursor.execute(query)
                signal_strength = cursor.fetchall()
                i = 0
                for k in range(0, len(signal_strength) - 1):
                    i = k
                    flag = 1
                    #			if signal_strength[k][6]=='-1' or str(signal_strength[k][3]).strip()=='' or str(signal_strength[0][4]).strip()=='':
                    #			    pass
                    if str(signal_strength[k][3]).strip() == '-110':
                    #			    pass
                        grp_name.append(signal_strength[k][5])
                        host_name.append(signal_strength[k][1])
                        ip_address.append(signal_strength[k][2])
                        signal_interface1.append("DEVICE WAS OFF")
                        signal_interface2.append("DEVICE WAS OFF")
                        signal_interface3.append("DEVICE WAS OFF")
                        signal_interface4.append("DEVICE WAS OFF")
                        signal_interface5.append("DEVICE WAS OFF")
                        signal_interface6.append("DEVICE WAS OFF")
                        signal_interface7.append("DEVICE WAS OFF")
                        signal_interface8.append("DEVICE WAS OFF")
                        time_stamp_signal1.append(
                            str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                    elif str(signal_strength[k][3]).strip() == '-111':
                    #			    pass
                        grp_name.append(signal_strength[k][5])
                        host_name.append(signal_strength[k][1])
                        ip_address.append(signal_strength[k][2])
                        signal_interface1.append("DEVICE WAS DISABLED")
                        signal_interface2.append("DEVICE WAS DISABLED")
                        signal_interface3.append("DEVICE WAS DISABLED")
                        signal_interface4.append("DEVICE WAS DISABLED")
                        signal_interface5.append("DEVICE WAS DISABLED")
                        signal_interface6.append("DEVICE WAS DISABLED")
                        signal_interface7.append("DEVICE WAS DISABLED")
                        signal_interface8.append("DEVICE WAS DISABLED")
                        time_stamp_signal1.append(
                            str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                    #			    grp_name.append(signal_strength[k][5])
                    #			    host_name.append(signal_strength[k][1])
                    #			    ip_address.append(signal_strength[k][2])
                    #			    signal_interface1.append(0)
                    #			    signal_interface2.append(0)
                    #			    signal_interface3.append(0)
                    #			    signal_interface4.append(0)
                    #			    signal_interface5.append(0)
                    #			    signal_interface6.append(0)
                    #			    signal_interface7.append(0)
                    #			    signal_interface8.append(0)
                    # time_stamp_signal1.append(str((signal_strength[k][0]).strftime('%d-%m-%Y
                    # %H:%M')))
                    else:
                        index = 1 if signal_strength[k][
                                         4] == '' else int(signal_strength[k][4])
                        if signal_strength[k][0] == signal_strength[k + 1][0]:
                            default_list[int(
                                index) - 1] = int(signal_strength[k][3])
                        else:
                            default_list[int(
                                index) - 1] = int(signal_strength[k][3])
                            grp_name.append(signal_strength[k][5])
                            host_name.append(signal_strength[k][1])
                            ip_address.append(signal_strength[k][2])
                            signal_interface1.append(default_list[0])
                            signal_interface2.append(default_list[1])
                            signal_interface3.append(default_list[2])
                            signal_interface4.append(default_list[3])
                            signal_interface5.append(default_list[4])
                            signal_interface6.append(default_list[5])
                            signal_interface7.append(default_list[6])
                            signal_interface8.append(default_list[7])
                            time_stamp_signal1.append(
                                str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                if len(signal_strength) > 0 and flag == 0:
                    if signal_strength[0][6] == '-1' or str(signal_strength[0][3]).strip() == '' or str(
                            signal_strength[0][4]).strip() == '':
                        grp_name.append(signal_strength[0][5])
                        host_name.append(signal_strength[0][1])
                        ip_address.append(signal_strength[0][2])
                        signal_interface1.append(0)
                        signal_interface2.append(0)
                        signal_interface3.append(0)
                        signal_interface4.append(0)
                        signal_interface5.append(0)
                        signal_interface6.append(0)
                        signal_interface7.append(0)
                        signal_interface8.append(0)
                        time_stamp_signal1.append(
                            str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                    else:
                        default_list[int(
                            signal_strength[0][4]) - 1] = int(signal_strength[0][3])
                        grp_name.append(signal_strength[0][5])
                        host_name.append(signal_strength[0][1])
                        ip_address.append(signal_strength[0][2])
                        signal_interface1.append(default_list[0])
                        signal_interface2.append(default_list[1])
                        signal_interface3.append(default_list[2])
                        signal_interface4.append(default_list[3])
                        signal_interface5.append(default_list[4])
                        signal_interface6.append(default_list[5])
                        signal_interface7.append(default_list[6])
                        signal_interface8.append(default_list[7])
                        time_stamp_signal1.append(
                            str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                if len(signal_strength) > 0 and flag == 1:
                    if signal_strength[i + 1][6] == '-1' or str(signal_strength[i + 1][3]).strip() == '' or str(
                            signal_strength[i + 1][4]).strip() == '':
                        grp_name.append(signal_strength[i + 1][5])
                        host_name.append(signal_strength[i + 1][1])
                        ip_address.append(signal_strength[i + 1][2])
                        signal_interface1.append(0)
                        signal_interface2.append(0)
                        signal_interface3.append(0)
                        signal_interface4.append(0)
                        signal_interface5.append(0)
                        signal_interface6.append(0)
                        signal_interface7.append(0)
                        signal_interface8.append(0)
                        time_stamp_signal1.append(
                            str((signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                    else:
                        default_list[int(signal_strength[
                            i + 1][4]) - 1] = int(signal_strength[0][3])
                        grp_name.append(signal_strength[i + 1][5])
                        host_name.append(signal_strength[i + 1][1])
                        ip_address.append(signal_strength[i + 1][2])
                        signal_interface1.append(default_list[0])
                        signal_interface2.append(default_list[1])
                        signal_interface3.append(default_list[2])
                        signal_interface4.append(default_list[3])
                        signal_interface5.append(default_list[4])
                        signal_interface6.append(default_list[5])
                        signal_interface7.append(default_list[6])
                        signal_interface8.append(default_list[7])
                        time_stamp_signal1.append(
                            str((signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0, 0, 0, 0, 0]
                    # make the RSSI 2'd list
                for k in range(0, len(time_stamp_signal1)):
                    total_list.append(
                        [time_stamp_signal1[k], host_name[k], ip_address[k], signal_interface1[k], signal_interface2[k],
                         signal_interface3[k], signal_interface4[k],
                         signal_interface5[k], signal_interface6[k], signal_interface7[k], signal_interface8[k],
                         grp_name[k]])

            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = total_list
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

        # TOTAL DATA FOR A GIVEN DATE PERIOD FOR NETWORK USAGE

    def get_total_data_network_usage(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_group:
        @param all_host:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            date1 = date1 + " " + time1
            date2 = date2 + " " + time2
            d1 = datetime.strptime(date1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(date2, "%d-%m-%Y %H:%M")
            date_temp1 = str(d1)
            date_temp2 = str(d2)
            i = 0
            hrt = ''
            ls = []
            tr = []
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = tr
            if all_group == '' and all_host == '':
                query = "SELECT  go16.index,go16.timestamp,hosts.host_name,hosts.ip_address,go16.rx_bytes,go16.tx_bytes,hostgroups.hostgroup_name FROM get_odu16_nw_interface_statistics_table AS 				go16 JOIN (SELECT host_id, host_name,ip_address FROM hosts WHERE device_type_id LIKE 'ODU16%%' GROUP BY host_id limit %s) AS hosts INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id WHERE go16.host_id = hosts.host_id and go16.timestamp between '%s' and '%s' order by go16.timestamp asc , go16.index asc" % (
                no_of_devices, date_temp1, date_temp2)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    return result_dict
                while i < (len(res)):
                    ls.append(str(res[i][1]))
                    ls.append(str(res[i][2]))
                    ls.append(str(res[i][3]))
                    hrt = str(res[i][6])
                    j = i + 3
                    if j > len(res):
                        break
                    while i < j:
                        if (i < 3):
                            if str(res[i][4]) == "123456789":
                                ls.append("DEVICE WAS OFF")
                                ls.append("DEVICE WAS OFF")
                            elif str(res[i][4]) == "987654321":
                                ls.append("DEVICE WAS DISABLED")
                                ls.append("DEVICE WAS DISABLED")
                            else:
                                var1 = float(res[i][4])
                                var3 = float(res[i][5])
                                ls.append(str(var1))
                                ls.append(str(var3))
                            i = i + 1
                        else:
                            if str(res[i][4]) == "123456789":
                                temp1 = "DEVICE WAS OFF"
                                temp2 = "DEVICE WAS OFF"
                            elif str(res[i][4]) == "987654321":
                                temp1 = "DEVICE WAS DISABLED"
                                temp2 = "DEVICE WAS DISABLED"
                            elif str(res[i - 3][4]) == "123456789" or str(res[i - 3][4] == "987654321"):
                                temp1 = float(res[i][4])
                                temp2 = float(res[i][5])
                            else:
                                var1 = float(res[i][4])
                                var2 = float(res[i - 3][4])
                                temp1 = var1 - var2
                                var3 = float(res[i][5])
                                var4 = float(res[i - 3][5])
                                temp2 = var3 - var4
                            if (temp1 < 0):
                                temp1 = 0
                            if (temp2) < 0:
                                temp2 = 0
                            ls.append(str(temp1))
                            ls.append(str(temp2))
                            i = i + 1
                    ls.append(hrt)
                    tr.append(ls)
                    ls = []
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query = "SELECT  go16.index,go16.timestamp,hosts.host_name,hosts.ip_address,go16.rx_bytes,go16.tx_bytes,hostgroups.hostgroup_name FROM get_odu16_nw_interface_statistics_table AS 				go16 JOIN (SELECT host_id, host_name,ip_address FROM hosts WHERE device_type_id LIKE 'ODU16%%' GROUP BY host_id) AS hosts  INNER JOIN hosts_hostgroups ON 				hosts_hostgroups.host_id = hosts.host_id  INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id WHERE go16.host_id = hosts.host_id and 				go16.timestamp between '%s' AND '%s' AND hosts.host_id IN %s order by go16.timestamp asc ,hosts.host_name asc, go16.index asc" % (
                    date_temp1, date_temp2, host_data)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    return result_dict

                while i < (len(res)):
                    ls.append(str(res[i][1]))
                    ls.append(str(res[i][2]))
                    ls.append(str(res[i][3]))
                    hrt = str(res[i][6])
                    j = i + 3
                    if j > len(res):
                        break
                    while i < j:
                        if (i < 3):
                            if str(res[i][4]) == "123456789":
                                ls.append("DEVICE WAS OFF")
                                ls.append("DEVICE WAS OFF")
                            elif str(res[i][4]) == "987654321":
                                ls.append("DEVICE WAS DISABLED")
                                ls.append("DEVICE WAS DISABLED")
                            else:
                                var1 = float(res[i][4])
                                var3 = float(res[i][5])
                                ls.append(str(var1))
                                ls.append(str(var3))
                            i = i + 1
                        else:
                            if str(res[i][4]) == "123456789":
                                temp1 = "DEVICE WAS OFF"
                                temp2 = "DEVICE WAS OFF"
                            elif str(res[i][4]) == "987654321":
                                temp1 = "DEVICE WAS DISABLED"
                                temp2 = "DEVICE WAS DISABLED"
                            elif str(res[i - 3][4]) == "123456789" or str(res[i - 3][4] == "987654321"):
                                temp1 = float(res[i][4])
                                temp2 = float(res[i][5])
                            else:
                                var1 = float(res[i][4])
                                var2 = float(res[i - 3][4])
                                temp1 = var1 - var2
                                var3 = float(res[i][5])
                                var4 = float(res[i - 3][5])
                                temp2 = var3 - var4
                            if (temp1 < 0):
                                temp1 = 0
                            if (temp2) < 0:
                                temp2 = 0
                            ls.append(str(temp1))
                            ls.append(str(temp2))

                            i = i + 1
                    ls.append(hrt)
                    tr.append(ls)
                    ls = []
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = tr
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

        # TOTAL DATA FOR A GIVEN DATE PERIOD FOR NETWORK OUTAGE

    def get_total_data_network_outage(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_group:
        @param all_host:
        @return:
        """
        try:
            main_res = get_outage(no_of_devices, date1, date2,
                                  time1, time2, all_group, all_host)
            return main_res
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            date1 = date1 + " " + time1
            date2 = date2 + " " + time2
            d1 = datetime.strptime(date1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(date2, "%d-%m-%Y %H:%M")
            date_temp1 = str(d1)
            date_temp2 = str(d2)
            all_host = all_host.split(',')
            li_result = []
            for i in all_host:
                temp_res = outage_graph(i, date_temp1, date_temp2)
                if str(temp_res['success']) == "0":
                    li_result += temp_res['list']
            result_dict = {}
            result_dict['success'] = 0
            result_dict['result'] = li_result
            return result_dict
            now = datetime.now()
            chour = int(now.hour)
            cminute = int(now.minute)
            csecond = int(now.second)
            cday = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
            i = 0
            ls = []
            tr = []
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = tr
            nsds = []
            if all_group == '' and all_host == '':
                query1 = "SELECT host_object_id FROM nagios_hosts GROUP BY host_object_id"
                query2 = "SELECT object_id FROM nagios_statehistory JOIN ( \
				SELECT host_object_id \
				FROM nagios_hosts \
				GROUP BY host_object_id) AS host \
				WHERE nagios_statehistory.object_id = host.host_object_id and state_time between '%s' and '%s' group by object_id " % (
                date_temp1, date_temp2)
                query3 = "SELECT nagios_hoststatus.host_object_id FROM nagios_hoststatus JOIN ( \
				SELECT host_object_id \
				FROM nagios_hosts  \
				GROUP BY host_object_id ) AS \
				host \
				WHERE nagios_hoststatus.host_object_id = host.host_object_id and  status_update_time between '%s' and '%s' GROUP BY nagios_hoststatus.host_object_id" % (
                date_temp1, date_temp2)
                cursor.execute(query1)
                r1 = cursor.fetchall()
                cursor.execute(query2)
                r2 = cursor.fetchall()
                cursor.execute(query3)
                r3 = cursor.fetchall()
                for i in range(len(r1)):
                    if str(r2).find(str(r1[i])) == -1:
                        if str(r3).find(str(r1[i])) == -1:
                            pass
                        else:
                            query4 = "SELECT nagstat.status_update_time,nagstat.current_state,host.alias,host.address, hostgroups.hostgroup_name from nagios_hoststatus as nagstat \
				JOIN ( \
				SELECT alias, address , host_object_id \
				FROM nagios_hosts WHERE host_object_id=%s \
				GROUP BY host_object_id limit %s) AS host\
				INNER JOIN hosts ON hosts.ip_address = host.address\
				INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
				INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				WHERE nagstat.host_object_id = host.host_object_id and  status_update_time between '%s' and '%s' GROUP BY nagstat.host_object_id " % (
                            str(r1[i])[1:-3], no_of_devices, date_temp1, date_temp2)
                            cursor.execute(query4)
                            res2 = cursor.fetchall()
                            if (len(res2) == 0):
                                continue
                            tmp = str(res2[0][0])[:-3]
                            d1 = datetime.strptime(tmp, "%Y-%m-%d %H:%M")
                            while (d1 < d2):
                                hstgroup = str(res2[0][4])
                                ls.append(str(d1)[:-9])
                                ls.append(str(res2[0][2]))
                                ls.append(str(res2[0][3]))
                                if (str(res2[0][1])) == '0':
                                    uptime_perc = "100.00"
                                    downtime_perc = "0.00"
                                elif (str(res2[0][1])) == '1':
                                    downtime_perc = "100.00"
                                    uptime_perc = "0.00"
                                else:
                                    uptime_perc = "0.00"
                                    downtime_perc = "100.00"
                                ls.append(uptime_perc)
                                ls.append(downtime_perc)
                                ls.append(hstgroup)
                                tr.append(ls)
                                ls = []
                                d1 = d1 + timedelta(days=1)
                query = "SELECT nagstat.state_time,nagstat.state_type,host.alias,host.address, hostgroups.hostgroup_name from nagios_statehistory as nagstat \
				JOIN ( \
				SELECT alias, address , host_object_id \
				FROM nagios_hosts \
				GROUP BY host_object_id limit %s) AS \
				host \
				INNER JOIN hosts ON hosts.ip_address = host.address \
				INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id \
				INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id \
				WHERE nagstat.object_id = host.host_object_id and nagstat.state_time between '%s' and '%s' order by host.alias asc,nagstat.state_time asc " % (
                no_of_devices, date_temp1, date_temp2)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    # return []
                    result_dict["result"] = []
                    return result_dict
                host = str(res[0][2])
                length = len(res) - 1
                i = 0
                while i < length:
                    host = str(res[i][2])
                    hstgroup = str(res[i][4])
                    ls.append(str(res[i][0])[:10])
                    ls.append(str(res[i][2]))
                    ls.append(str(res[i][3]))
                    while (host == str(res[i][2]) and i < length):
                        time1 = str(res[i][0])
                        time2 = str(res[i + 1][0])
                        uptime = 0
                        downtime = 0
                        h1 = int(time1[11:13])
                        m1 = int(time1[14:16])
                        sec1 = int(time1[17:])
                        time_diff = float((h1) * 3600 + (m1) * 60 + (sec1))
                        if (i != 0):
                            if (last == "0"):
                                uptime += time_diff
                            else:
                                downtime += time_diff
                        s1 = str(res[i][1])
                        while ((time1[:10]) == (time2[:10]) and (i < length - 1) and host == str(res[i][2])):
                            h1 = int(time1[11:13])
                            h2 = int(time2[11:13])
                            m1 = int(time1[14:16])
                            m2 = int(time2[14:16])
                            sec1 = int(time1[17:])
                            sec2 = int(time2[17:])
                            time_diff = float((h1) * 3600 + (m1) * 60 + (sec1))
                            s1 = str(res[i][1])
                            time_diff = float(
                                (h2 - h1) * 3600 + (m2 - m1) * 60 + (sec2 - sec1))
                            s1 = str(res[i][1])
                            s2 = str(res[i + 1][1])
                            if (s1 == '0'):
                                uptime += time_diff
                            else:
                                downtime += time_diff
                            i = i + 1
                            time1 = str(res[i][0])
                            time2 = str(res[i + 1][0])

                        last = str(res[i][1])
                        i = i + 1
                        if (time1[:10] != time2[:10]):
                            if (cday != time1[:10]):
                                h1 = int(time1[11:13])
                                m1 = int(time1[14:16])
                                sec1 = int(time1[17:])
                                s1 = str(res[i][1])
                                time_diff = float(
                                    (23 - h1) * 3600 + (59 - m1) * 60 + (59 - sec1))
                            else:
                                time_diff = float((chour - h1) * 3600 + (
                                    cminute - m1) * 60 + (csecond - sec1))
                            if (s1 == '0'):
                                uptime += time_diff
                            else:
                                downtime += time_diff

                        else:
                            h1 = int(time1[11:13])
                            m1 = int(time1[14:16])
                            sec1 = int(time1[17:])
                            time_diff = float((
                                                  chour - h1) * 3600 + (cminute - m1) * 60 + (csecond - sec1))
                            if (s1 == '0'):
                                uptime += time_diff
                            else:
                                downtime += time_diff
                        if (uptime == 0 and downtime == 0):
                            uptime_perc = 0
                            downtime_perc = 0
                        else:
                            uptime_perc = (
                                100 * (uptime) / (uptime + downtime))
                            if (uptime_perc < 0):
                                uptime_perc = 0.0
                            elif (uptime_perc > 100):
                                uptime_perc = 100.0
                            downtime_perc = 100 - uptime_perc
                        ls.append(
                            str(uptime_perc)[:str(uptime_perc).find(".") + 2])
                        ls.append(str(
                            downtime_perc)[:str(downtime_perc).find(".") + 2])
                        ls.append(hstgroup)
                        tr.append(ls)
                        ls = []
                        if (host != str(res[i][2])):
                            last = "3"
                        break
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query1 = "SELECT host_object_id FROM nagios_hosts GROUP BY host_object_id"
                query2 = "SELECT object_id FROM nagios_statehistory JOIN ( \
				SELECT host_object_id \
				FROM nagios_hosts  \
				GROUP BY host_object_id) AS host \
				WHERE nagios_statehistory.object_id = host.host_object_id and state_time between '%s' and '%s' group by object_id " % (
                date_temp1, date_temp2)
                query3 = "SELECT nagios_hoststatus.host_object_id FROM nagios_hoststatus JOIN ( \
				SELECT host_object_id \
				FROM nagios_hosts  \
				GROUP BY host_object_id ) AS \
				host \
				WHERE nagios_hoststatus.host_object_id = host.host_object_id and  status_update_time between '%s' and '%s' GROUP BY nagios_hoststatus.host_object_id" % (
                date_temp1, date_temp2)
                cursor.execute(query1)
                r1 = cursor.fetchall()
                cursor.execute(query2)
                r2 = cursor.fetchall()
                cursor.execute(query3)
                r3 = cursor.fetchall()
                for i in range(len(r1)):
                    if str(r2).find(str(r1[i])) == -1:
                        if str(r3).find(str(r1[i])) == -1:
                            pass
                        else:
                            query4 = "SELECT nagstat.status_update_time,nagstat.current_state,host.alias,host.address,hostgroups.hostgroup_name from nagios_hoststatus as nagstat \
				JOIN ( \
				SELECT alias, address , host_object_id \
				FROM nagios_hosts WHERE host_object_id=%s \
				GROUP BY host_object_id) AS host \
				INNER JOIN hosts ON hosts.ip_address = host.address\
				INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
				INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				WHERE nagstat.host_object_id = host.host_object_id and  status_update_time between '%s' and '%s' AND hosts.host_id IN %s GROUP BY nagstat.host_object_id " % (
                            str(i), date_temp1, date_temp2, host_data)
                            cursor.execute(query4)
                            res2 = cursor.fetchall()
                            if (len(res2) == 0):
                                continue
                            tmp = str(res2[0][0])[:-3]
                            d1 = datetime.strptime(tmp, "%Y-%m-%d %H:%M")
                            while (d1 < d2):
                                hstgroup = res2[0][4]
                                ls.append(str(d1)[:-9])
                                ls.append(str(res2[0][2]))
                                ls.append(str(res2[0][3]))
                                if (str(res2[0][1])) == '0':
                                    uptime_perc = "100.00"
                                    downtime_perc = "0.00"
                                elif (str(res2[0][1])) == '1':
                                    downtime_perc = "100.00"
                                    uptime_perc = "0.00"
                                else:
                                    uptime_perc = "0.00"
                                    downtime_perc = "100.00"
                                ls.append(uptime_perc)
                                ls.append(downtime_perc)
                                ls.append(hstgroup)
                                tr.append(ls)
                                ls = []
                                d1 = d1 + timedelta(days=1)
                query = "SELECT nagstat.state_time,nagstat.state_type,host.alias,host.address,hostgroups.hostgroup_name from nagios_statehistory as nagstat \
				JOIN ( \
				SELECT alias, address , host_object_id \
				FROM nagios_hosts \
				GROUP BY host_object_id ) AS \
				host \
				INNER JOIN hosts ON hosts.ip_address = host.address\
				INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
				INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				WHERE nagstat.object_id = host.host_object_id and nagstat.state_time between '%s' and '%s' AND hosts.host_id IN %s order by host.alias asc,nagstat.state_time asc " % (
                date_temp1, date_temp2, host_data)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    # return []
                    result_dict["result"] = []
                    return result_dict
                host = str(res[0][2])
                length = len(res) - 1
                i = 0
                while i < length:
                    host = str(res[i][2])
                    hstgroup = str(res[i][4])
                    ls.append(str(res[i][0])[:10])
                    ls.append(str(res[i][2]))
                    ls.append(str(res[i][3]))
                    while (host == str(res[i][2]) and i < length):
                        time1 = str(res[i][0])
                        time2 = str(res[i + 1][0])
                        uptime = 0
                        downtime = 0
                        h1 = int(time1[11:13])
                        m1 = int(time1[14:16])
                        sec1 = int(time1[17:])
                        time_diff = float((h1) * 3600 + (m1) * 60 + (sec1))
                        if (i != 0):
                            if (last == "0"):
                                uptime += time_diff
                            else:
                                downtime += time_diff
                        s1 = str(res[i][1])
                        while ((time1[:10]) == (time2[:10]) and (i < length - 1) and host == str(res[i][2])):
                            h1 = int(time1[11:13])
                            h2 = int(time2[11:13])
                            m1 = int(time1[14:16])
                            m2 = int(time2[14:16])
                            sec1 = int(time1[17:])
                            sec2 = int(time2[17:])
                            time_diff = float((h1) * 3600 + (m1) * 60 + (sec1))
                            s1 = str(res[i][1])
                            time_diff = float(
                                (h2 - h1) * 3600 + (m2 - m1) * 60 + (sec2 - sec1))
                            s1 = str(res[i][1])
                            s2 = str(res[i + 1][1])
                            if (s1 == '0'):
                                uptime += time_diff
                            else:
                                downtime += time_diff
                            i = i + 1
                            time1 = str(res[i][0])
                            time2 = str(res[i + 1][0])

                        last = str(res[i][1])
                        i = i + 1
                        if (time1[:10] != time2[:10]):
                            if (cday != time1[:10]):
                                h1 = int(time1[11:13])
                                m1 = int(time1[14:16])
                                sec1 = int(time1[17:])
                                s1 = str(res[i][1])
                                time_diff = float(
                                    (23 - h1) * 3600 + (59 - m1) * 60 + (59 - sec1))
                            else:
                                time_diff = float((chour - h1) * 3600 + (
                                    cminute - m1) * 60 + (csecond - sec1))
                            if (s1 == '0'):
                                uptime += time_diff
                            else:
                                downtime += time_diff

                        else:
                            h1 = int(time1[11:13])
                            m1 = int(time1[14:16])
                            sec1 = int(time1[17:])
                            time_diff = float((
                                                  chour - h1) * 3600 + (cminute - m1) * 60 + (csecond - sec1))
                            if (s1 == '0'):
                                uptime += time_diff
                            else:
                                downtime += time_diff
                        if (uptime == 0 and downtime == 0):
                            uptime_perc = 0
                            downtime_perc = 0
                        else:
                            uptime_perc = (
                                100 * (uptime) / (uptime + downtime))
                            if (uptime_perc < 0):
                                uptime_perc = 0.0
                            elif (uptime_perc > 100):
                                uptime_perc = 100.0
                            downtime_perc = 100 - uptime_perc
                        ls.append(
                            str(uptime_perc)[:str(uptime_perc).find(".") + 2])
                        ls.append(str(
                            downtime_perc)[:str(downtime_perc).find(".") + 2])
                        ls.append(hstgroup)
                        tr.append(ls)
                        ls = []
                        if (host != str(res[i][2])):
                            last = "3"
                        break

            result_dict["result"] = tr
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict

    # reporting create fucntionaltiy started from here.
    def crc_excel_creating(self, crc_avg, crc_total):
        """

        @param crc_avg:
        @param crc_total:
        @return:
        """
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        try:
            flag = 0
            if (crc_avg["success"] == 1):
                return crc_avg["result"]
            if (crc_total["success"] == 1):
                return crc_total["result"]
            crc_avg = crc_avg["result"]
            crc_total = crc_total["result"]
            if len(crc_total) == 0:
                return 1
            xls_book = xlwt.Workbook(encoding='ascii')
            # styling part start of excel file.
            style = xlwt.XFStyle()  # Create Style
            borders = xlwt.Borders()  # Create Borders
            borders.left = xlwt.Borders.THIN  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 23
            borders.right_colour = 23
            borders.top_colour = 23
            borders.bottom_colour = 23
            style.borders = borders  # Add
            pattern = xlwt.Pattern()  # Create the Pattern
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern_fore_colour = 16
            # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 =
            # Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark
            # Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark
            # Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes
            # on...
            style.pattern = pattern  # Add Pattern to Style

            font = xlwt.Font()  # Create Font
            font.bold = True  # Set font to Bold
            #	    style = xlwt.XFStyle() # Create Style
            font.colour_index = 0x09
            style.font = font  # Add Bold Font to Style

            alignment = xlwt.Alignment()  # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
            alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
            #	    style = xlwt.XFStyle() # Create Style
            style.alignment = alignment  # Add Alignment to Style

            style1 = xlwt.XFStyle()  # Create Style
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style1.alignment = alignment  # Add Alignment to Style

            #           pattern = xlwt.Pattern() # Create the Pattern
            #            pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            #            pattern.pattern_fore_colour= 0x0A
            # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost 			brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
            #            style1.pattern = pattern # Add Pattern to Style

            # create another style for header
            #	    font = xlwt.Font() # Create Font
            # font.family = xlwt.Font.FAMILY_ROMAN
            #	    font.bold = True # Set font to Bold
            #	    font.colour_index = 0x09
            #	    font.get_biff_record = ?
            #	    font.height = 0x00C8 # C8 in Hex (in decimal) = 10 points in height.
            #	    font.name = 'Arial'
            #	    font.outline = ?
            #	    font.shadow = True
            #	    style1.font = font # Add Bold Font to Style

            # -----------   End of style ---------#
            # average crc and phy error creation start.
            crc_avg = sorted(crc_avg, key=itemgetter(5))
            for k in range(len(crc_avg) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet('%s(Average_Data),' % (
                        crc_avg[k][5]), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 4, "Average Error Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 4, "%s(Group Name)" % (crc_avg[k][5]), style)
                    xls_sheet.write_merge(2, 2, 0, 4, "")
                    #		    xls_sheet.write(3,0,"Date",style1)
                    #		    xls_sheet.write(3,1,"Hostname",style1)
                    #		    xls_sheet.write(3,2,"No. of phy error",style1)
                    #		    xls_sheet.write(3,3,"No. of crc error",style1)
                    i = 4
                    # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                    # horiz center,color grey25')
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = ['Data', 'Hostname',
                                'IP Address', 'No. of phy error', 'No. of crc error']

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)

                if crc_avg[k][5] == crc_avg[k + 1][5]:
                    flag = 1
                    for j in range(len(crc_avg[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, crc_avg[k][j], style1)
                        xls_sheet.col(j).width = width
                    i = i + 1
                else:
                    flag = 0
                    for j in range(len(crc_avg[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, crc_avg[k][j], style1)
                        xls_sheet.col(j).width = width

            if len(crc_avg) > 1:
                if crc_avg[len(crc_avg) - 1][5] == crc_avg[len(crc_avg) - 2][5]:
                    for j in range(len(crc_avg[len(crc_avg) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, crc_avg[len(crc_avg) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(crc_avg) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Average_Data),' % (
                    crc_avg[0][5]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 4, "Average Error Information", style)
                xls_sheet.write_merge(
                    1, 1, 0, 4, "%s(Group Name)" % (crc_avg[0][5]), style)
                xls_sheet.write_merge(2, 2, 0, 4, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = ['Data', 'Hostname',
                            'IP Address', 'No. of phy error', 'No. of crc error']

                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                i = 4
                for j in range(len(crc_avg[len(crc_avg) - 1]) - 1):
                    width = 5000
                    xls_sheet.write(i, j, crc_avg[len(crc_avg) - 1][j], style1)
                    xls_sheet.col(j).width = width

            # average crc and phy error creation end .
            flag = 0
            # total crc and phy error creation start from here.
            crc_total = sorted(crc_total, key=itemgetter(5))
            for k in range(len(crc_total) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet(
                        '%s(Total_Data)' % (crc_total[k][5]))
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 4, "Total Error Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 4, "%s(Group Name)" % (crc_total[k][5]), style)
                    xls_sheet.write_merge(2, 2, 0, 4, "")
                    i = 4
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = ['Data', 'Hostname',
                                'IP Address', 'No. of phy error', 'No. of crc error']

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)
                if crc_total[k][5] == crc_total[k + 1][5]:
                    flag = 1
                    for j in range(len(crc_total[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, crc_total[k][j], style1)
                        xls_sheet.col(j).width = width
                    i = i + 1
                else:
                    flag = 0
                    for j in range(len(crc_total[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, crc_total[k][j], style1)
                        xls_sheet.col(j).width = width

            if len(crc_total) > 1:
                if crc_total[len(crc_total) - 1][5] == crc_total[len(crc_total) - 2][5]:
                    for j in range(len(crc_total[len(crc_total) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, crc_total[len(crc_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(crc_total) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet(
                    '%s(Total_Data)' % (crc_total[0][5]))
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 4, "Total Error Information", style)
                xls_sheet.write_merge(
                    1, 1, 0, 4, "%s(Group Name)" % (crc_total[0][5]), style)
                xls_sheet.write_merge(2, 2, 0, 4, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = ['Data', 'Hostname',
                            'IP Address', 'No. of phy error', 'No. of crc error']

                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                i = 4
                for j in range(len(crc_total[len(crc_total) - 1]) - 1):
                    width = 5000
                    xls_sheet.write(
                        i, j, crc_total[len(crc_total) - 1][j], style1)
                    xls_sheet.col(j).width = width

            # total crc and phy error creation end .
            xls_book.save(
                '/omd/sites/%s/share/check_mk/web/htdocs/download/error_excel.xls' % nms_instance)
            return '0'
        except Exception, e:
            return str(e)

    def nw_bandwith_excel_creating(self, nw_total):
        """

        @param nw_total:
        @return:
        """
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        try:
            flag = 0
            if (nw_total["success"] == 1):
                return nw_total["result"]
            nw_total = nw_total["result"]
            if len(nw_total) == 0:
                return 1
            xls_book = xlwt.Workbook(encoding='ascii')
            # styling part start of excel file.
            style = xlwt.XFStyle()  # Create Style
            borders = xlwt.Borders()  # Create Borders
            borders.left = xlwt.Borders.THIN  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 23
            borders.right_colour = 23
            borders.top_colour = 23
            borders.bottom_colour = 23
            style.borders = borders  # Add
            pattern = xlwt.Pattern()  # Create the Pattern
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern_fore_colour = 16
            # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 =
            # Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 =
            # Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow ,
            # almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray,
            # 23 = Dark Gray, the list goes on...
            style.pattern = pattern  # Add Pattern to Style
            font = xlwt.Font()  # Create Font
            font.bold = True  # Set font to Bold
            # style = xlwt.XFStyle() # Create Style
            font.colour_index = 0x09
            style.font = font  # Add Bold Font to Style
            alignment = xlwt.Alignment()  # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
            alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
            # style = xlwt.XFStyle() # Create Style
            style.alignment = alignment  # Add Alignment to Style

            style1 = xlwt.XFStyle()  # Create Style
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style1.alignment = alignment  # Add Alignment to Style
            # -----------   End of style ---------#
            # average crc and phy error creation start.
            nw_total = sorted(nw_total, key=itemgetter(9))
            for k in range(len(nw_total) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet('%s(Bandwith_data),' % (
                        nw_total[k][9]), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 8, "Bandwith Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 8, "%s(Group Name)" % (nw_total[k][9]), style)
                    xls_sheet.write_merge(2, 2, 0, 8, "")
                    #		    xls_sheet.write(3,0,"Date",style1)
                    #		    xls_sheet.write(3,1,"Hostname",style1)
                    #		    xls_sheet.write(3,2,"No. of phy error",style1)
                    #		    xls_sheet.write(3,3,"No. of crc error",style1)
                    i = 4
                    # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                    # horiz center,color grey25')
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = ['Data', 'Hostname', 'IP Address',
                                'Eth0(Rx)', 'Eth0(Tx)', 'Eth1(Rx)', 'Eth1(Tx)', 'Br0(Rx)', 'Br0(Tx)']

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)

                if nw_total[k][9] == nw_total[k + 1][9]:
                    flag = 1
                    for j in range(len(nw_total[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, nw_total[k][j], style1)
                        xls_sheet.col(j).width = width
                    i = i + 1
                else:
                    flag = 0
                    for j in range(len(nw_total[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, nw_total[k][j], style1)
                        xls_sheet.col(j).width = width

            if len(nw_total) > 1:
                if nw_total[len(nw_total) - 1][9] == nw_total[len(nw_total) - 2][9]:
                    for j in range(len(nw_total[len(nw_total) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, nw_total[len(nw_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(nw_total) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Bandwith_data),' % (
                    nw_total[0][9]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 3, "Bandwith Information", style)
                xls_sheet.write_merge(
                    1, 1, 0, 3, "%s(Group Name)" % (nw_total[0][9]), style)
                xls_sheet.write_merge(2, 2, 0, 3, "")
                #		    xls_sheet.write(3,0,"Date",style1)
                #		    xls_sheet.write(3,1,"Hostname",style1)
                #		    xls_sheet.write(3,2,"No. of phy error",style1)
                #		    xls_sheet.write(3,3,"No. of crc error",style1)
                i = 4
                # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                # horiz center,color grey25')
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = ['Data', 'Hostname', 'IP Address',
                            'Eth0(Rx)', 'Eth0(Tx)', 'Eth1(Rx)', 'Eth1(Tx)', 'Br0(Rx)', 'Br0(Tx)']

                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                i = 4
                for j in range(len(nw_total[len(nw_total) - 1]) - 1):
                    width = 5000
                    xls_sheet.write(
                        i, j, nw_total[len(nw_total) - 1][j], style1)
                    xls_sheet.col(j).width = width
            xls_book.save(
                '/omd/sites/%s/share/check_mk/web/htdocs/download/nw_bandwidth_excel.xls' % nms_instance)
            return '0'
        except Exception, e:
            return str(e[-1])

    def rssi_excel_creating(self, rssi_avg, rssi_total):
        """

        @param rssi_avg:
        @param rssi_total:
        @return:
        """
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        try:
            flag = 0
            if (rssi_avg["success"] == 1):
                return rssi_avg["result"]
            if (rssi_total["success"] == 1):
                return rssi_total["result"]

            rssi_avg = rssi_avg["result"]
            rssi_total = rssi_total["result"]
            if len(rssi_total) == 0:
                return 1

            xls_book = xlwt.Workbook(encoding='ascii')
            # styling part start of excel file.
            style = xlwt.XFStyle()  # Create Style
            borders = xlwt.Borders()  # Create Borders
            borders.left = xlwt.Borders.THIN  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 23
            borders.right_colour = 23
            borders.top_colour = 23
            borders.bottom_colour = 23
            style.borders = borders  # Add
            pattern = xlwt.Pattern()  # Create the Pattern
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern_fore_colour = 16
            # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 =
            # Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 =
            # Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow ,
            # almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray,
            # 23 = Dark Gray, the list goes on...
            style.pattern = pattern  # Add Pattern to Style
            font = xlwt.Font()  # Create Font
            font.bold = True  # Set font to Bold
            # style = xlwt.XFStyle() # Create Style
            font.colour_index = 0x09
            style.font = font  # Add Bold Font to Style
            alignment = xlwt.Alignment()  # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
            alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
            # style = xlwt.XFStyle() # Create Style
            style.alignment = alignment  # Add Alignment to Style

            style1 = xlwt.XFStyle()  # Create Style
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style1.alignment = alignment  # Add Alignment to Style

            # -----------   End of style ---------#
            # average crc and phy error creation start.
            rssi_avg = sorted(rssi_avg, key=itemgetter(11))
            for k in range(len(rssi_avg) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet('%s(Aerage_rssi),' % (
                        rssi_avg[k][11]), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 10, "Average RSSI Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 10, "%s(Group Name)" % (rssi_avg[k][11]), style)
                    xls_sheet.write_merge(2, 2, 0, 10, "")
                    i = 4
                    # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                    # horiz center,color grey25')
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = ['Data', 'Hostname', 'IP Address', 'Peer1',
                                'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7', 'Peer8', ]

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)

                if rssi_avg[k][11] == rssi_avg[k + 1][11]:
                    flag = 1
                    for j in range(len(rssi_avg[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, rssi_avg[k][j], style1)
                        xls_sheet.col(j).width = width
                    i = i + 1
                else:
                    flag = 0
                    for j in range(len(rssi_avg[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, rssi_avg[k][j], style1)
                        xls_sheet.col(j).width = width

            if len(rssi_avg) > 1:
                if rssi_avg[len(rssi_avg) - 1][11] == rssi_avg[len(rssi_avg) - 2][11]:
                    for j in range(len(rssi_avg[len(rssi_avg) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, rssi_avg[len(rssi_avg) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(rssi_avg) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Average_rssi),' % (
                    rssi_avg[0][11]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 10, "Average RSSI Information", style)
                xls_sheet.write_merge(
                    1, 1, 0, 10, "%s(Group Name)" % (rssi_avg[0][11]), style)
                xls_sheet.write_merge(2, 2, 0, 10, "")
                i = 4
                # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                # horiz center,color grey25')
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = ['Data', 'Hostname', 'IP Address', 'Peer1',
                            'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7', 'Peer8', ]

                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for j in range(len(rssi_avg[len(rssi_avg) - 1]) - 1):
                    width = 5000
                    xls_sheet.write(
                        i, j, rssi_avg[len(rssi_avg) - 1][j], style1)
                    xls_sheet.col(j).width = width

            flag = 0
            rssi_total = sorted(rssi_total, key=itemgetter(11))
            for k in range(len(rssi_total) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet('%s(Total_rssi),' % (
                        rssi_total[k][11]), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 10, "Total RSSI Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 10, "%s(Group Name)" % (rssi_total[k][11]), style)
                    xls_sheet.write_merge(2, 2, 0, 10, "")
                    i = 4
                    # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                    # horiz center,color grey25')
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = ['Data', 'Hostname', 'IP Address', 'Peer1',
                                'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7', 'Peer8', ]

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)

                if rssi_total[k][11] == rssi_total[k + 1][11]:
                    flag = 1
                    for j in range(len(rssi_total[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, rssi_total[k][j], style1)
                        xls_sheet.col(j).width = width
                    i = i + 1
                else:
                    flag = 0
                    for j in range(len(rssi_total[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, rssi_total[k][j], style1)
                        xls_sheet.col(j).width = width

            if len(rssi_total) > 1:
                if rssi_total[len(rssi_total) - 1][11] == rssi_total[len(rssi_total) - 2][11]:
                    for j in range(len(rssi_total[len(rssi_total) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, rssi_total[len(rssi_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(rssi_total) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Total_rssi),' % (
                    rssi_total[0][11]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 10, "Total RSSI Information", style)
                xls_sheet.write_merge(1, 1, 0, 10,
                                      "%s(Group Name)" % (rssi_total[0][11]), style)
                xls_sheet.write_merge(2, 2, 0, 10, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = ['Data', 'Hostname', 'IP Address', 'Peer1',
                            'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7', 'Peer8', ]
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for j in range(len(rssi_total[len(rssi_total) - 1]) - 1):
                    width = 5000
                    xls_sheet.write(
                        i, j, rssi_total[len(rssi_total) - 1][j], style1)
                    xls_sheet.col(j).width = width

            xls_book.save(
                '/omd/sites/%s/share/check_mk/web/htdocs/download/rssi_excel.xls' % nms_instance)
            return '0'
        except Exception, e:
            return str(e)

    def outage_excel_creating(self, outage_total):
        """

        @param outage_total:
        @return:
        """
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        try:
            flag = 0
            if (outage_total["success"] == 1):
                return outage_total["result"]
            outage_total = outage_total["result"]
            if len(outage_total) == 0:
                return 1
            xls_book = xlwt.Workbook(encoding='ascii')
            # styling part start of excel file.
            style = xlwt.XFStyle()  # Create Style
            borders = xlwt.Borders()  # Create Borders
            borders.left = xlwt.Borders.THIN  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 23
            borders.right_colour = 23
            borders.top_colour = 23
            borders.bottom_colour = 23
            style.borders = borders  # Add
            pattern = xlwt.Pattern()  # Create the Pattern
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern_fore_colour = 16
            # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 =
            # Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 =
            # Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow ,
            # almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray,
            # 23 = Dark Gray, the list goes on...
            style.pattern = pattern  # Add Pattern to Style
            font = xlwt.Font()  # Create Font
            font.bold = True  # Set font to Bold
            # style = xlwt.XFStyle() # Create Style
            font.colour_index = 0x09
            style.font = font  # Add Bold Font to Style
            alignment = xlwt.Alignment()  # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
            alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
            # style = xlwt.XFStyle() # Create Style
            style.alignment = alignment  # Add Alignment to Style

            style1 = xlwt.XFStyle()  # Create Style
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style1.alignment = alignment  # Add Alignment to Style
            # -----------   End of style ---------#
            # average crc and phy error creation start.
            outage_total = sorted(outage_total, key=itemgetter(9))
            for k in range(len(outage_total) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet('%s(Network_Outage),' % (
                        outage_total[k][5]), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 4, "Devcie Outage Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 4, "%s(Group Name)" % (outage_total[k][5]), style)
                    xls_sheet.write_merge(2, 2, 0, 4, "")
                    #		    xls_sheet.write(3,0,"Date",style1)
                    #		    xls_sheet.write(3,1,"Hostname",style1)
                    #		    xls_sheet.write(3,2,"No. of phy error",style1)
                    #		    xls_sheet.write(3,3,"No. of crc error",style1)
                    i = 4
                    # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                    # horiz center,color grey25')
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = ['Data', 'Hostname',
                                'IP Address', 'Up Time(%)', 'Down Time(%)']

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)

                if outage_total[k][9] == outage_total[k + 1][5]:
                    flag = 1
                    for j in range(len(outage_total[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, outage_total[k][j], style1)
                        xls_sheet.col(j).width = width
                    i = i + 1
                else:
                    flag = 0
                    for j in range(len(outage_total[k]) - 1):
                        width = 5000
                        xls_sheet.write(i, j, outage_total[k][j], style1)
                        xls_sheet.col(j).width = width

            if len(outage_total) > 1:
                if outage_total[len(outage_total) - 1][9] == outage_total[len(outage_total) - 2][9]:
                    for j in range(len(outage_total[len(outage_total) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, outage_total[len(outage_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(outage_total) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Network_Outage),' % (
                    outage_total[0][5]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 4, "Devcie Outage Information", style)
                xls_sheet.write_merge(
                    1, 1, 0, 4, "%s(Group Name)" % (outage_total[0][5]), style)
                xls_sheet.write_merge(2, 2, 0, 4, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = ['Data', 'Hostname',
                            'IP Address', 'Up Time(%)', 'Down Time(%)']
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for j in range(len(outage_total[len(outage_total) - 1]) - 1):
                    width = 5000
                    xls_sheet.write(
                        i, j, outage_total[len(outage_total) - 1][j], style1)
                    xls_sheet.col(j).width = width
                # save the excel report
            xls_book.save(
                '/omd/sites/%s/share/check_mk/web/htdocs/download/outage_excel.xls' % nms_instance)
            return '0'
        except Exception, e:
            return str(e)

        # TOTAL TRAP DATA FOR A GIVEN DATE PERIOD BY SERVITY

    def get_total_data_trap(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_group:
        @param all_host:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            date1 = date1 + " " + time1
            date2 = date2 + " " + time2
            d1 = datetime.strptime(date1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(date2, "%d-%m-%Y %H:%M")
            date_temp1 = str(d1)
            date_temp2 = str(d2)
            i = 0
            ls = []
            tr = []
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = tr
            if all_host == "" and all_group == "":
                query = "SELECT date(ta.timestamp) ,hosts.host_name,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
	 			 FROM trap_alarms as ta join (select host_name,host_id,ip_address from hosts limit %s) as hosts on hosts.ip_address=ta.agent_id\
		                 INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
		                 INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				 where  ta.timestamp between '%s' AND '%s' group by serevity,date(ta.timestamp) \
				 order by  ta.timestamp,hosts.host_name,ta.serevity " % (no_of_devices, date_temp1, date_temp2)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    return result_dict
                length = len(res) - 1
                ls = []
                tr = []
                i = 0
                while i < length:
                    host = str(res[i][1])
                    ls.append(str(res[i][0]))
                    ls.append(str(res[i][1]))
                    ls.append(str(res[i][2]))
                    group_name = res[i][5]
                    lst = [0, 0, 0, 0, 0, 0]
                    while (str(res[i][1]) == str(res[i + 1][1]) and str(res[i][0]) == str(res[i + 1][0]) and (
                        i < length - 1)):
                        lst[int(res[i][4])] = int(res[i][3])
                        i = i + 1
                    lst[int(res[i][4])] = int(res[i][3])
                    ls.append(lst[0] + lst[2])
                    ls.append(lst[1])
                    ls.append(lst[3])
                    ls.append(lst[4])
                    ls.append(lst[5])
                    ls.append(group_name)
                    tr.append(ls)
                    ls = []
                    lst = [0, 0, 0, 0, 0, 0]
                    i = i + 1
                ls.append(str(res[i][0]))
                ls.append(str(res[i][1]))
                ls.append(str(res[i][2]))
                group_name = res[i][5]
                lst = [0, 0, 0, 0, 0, 0]
                lst[int(res[i][4])] = int(res[i][3])
                ls.append(lst[0] + lst[2])
                ls.append(lst[1])
                ls.append(lst[3])
                ls.append(lst[4])
                ls.append(lst[5])
                ls.append(group_name)
                tr.append(ls)
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query = "SELECT date(ta.timestamp) ,hosts.host_name,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
	 			 FROM trap_alarms as ta join (select host_name,host_id,ip_address from hosts ) as hosts on hosts.ip_address=ta.agent_id  \
		                 INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
		                 INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				 where  ta.timestamp between '%s' AND '%s' AND hosts.host_id IN %s group by serevity,date(ta.timestamp) \
				 order by  ta.timestamp,hosts.host_name,ta.serevity " % (date_temp1, date_temp2, host_data)
                cursor.execute(query)
                res = cursor.fetchall()
                if (len(res) == 0):
                    return result_dict
                length = len(res) - 1
                ls = []
                tr = []
                i = 0
                while i < length:
                    host = str(res[i][1])
                    ls.append(str(res[i][0]))
                    ls.append(str(res[i][1]))
                    ls.append(str(res[i][2]))
                    group_name = res[i][5]
                    lst = [0, 0, 0, 0, 0, 0]
                    while (str(res[i][1]) == str(res[i + 1][1]) and str(res[i][0]) == str(res[i + 1][0]) and (
                        i < length - 1)):
                        lst[int(res[i][4])] = int(res[i][3])
                        i = i + 1
                    lst[int(res[i][4])] = int(res[i][3])
                    ls.append(lst[0] + lst[2])
                    ls.append(lst[1])
                    ls.append(lst[3])
                    ls.append(lst[4])
                    ls.append(lst[5])
                    ls.append(group_name)
                    tr.append(ls)
                    ls = []
                    lst = [0, 0, 0, 0, 0, 0]
                    i = i + 1
                ls.append(str(res[i][0]))
                ls.append(str(res[i][1]))
                ls.append(str(res[i][2]))
                group_name = res[i][5]
                lst = [0, 0, 0, 0, 0, 0]
                lst[int(res[i][4])] = int(res[i][3])
                ls.append(lst[0] + lst[2])
                ls.append(lst[1])
                ls.append(lst[3])
                ls.append(lst[4])
                ls.append(lst[5])
                ls.append(group_name)
                tr.append(ls)

            result_dict["result"] = tr
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

        # TOTAL TRAP DATA EXCEL FOR A GIVEN DATE PERIOD BY SERVITY

    def get_total_trap_data_excel(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
        """

        @param no_of_devices:
        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_group:
        @param all_host:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            date1 = date1 + " " + time1
            date2 = date2 + " " + time2
            d1 = datetime.strptime(date1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(date2, "%d-%m-%Y %H:%M")
            date_temp1 = str(d1)
            date_temp2 = str(d2)
            total_trap = []
            currrent_alarm = []
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            if all_host == "" and all_group == "":
                query = "SELECT date(ta.trap_receive_date),time(ta.trap_receive_date),ta.trap_receive_date,device_type.device_name,hostgroups.hostgroup_name,hosts.host_name,ta.agent_id,ta.trap_event_id,ta.trap_event_type,ta.description,ta.serevity\
	 			 FROM trap_alarms as ta join (select host_name,host_id,ip_address,device_type_id from hosts limit %s) as hosts on hosts.ip_address=ta.agent_id\
			         INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
			         INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				 INNER JOIN device_type ON device_type.device_type_id=hosts.device_type_id\
				 where  ta.timestamp between '%s' AND '%s' group by ta.serevity,ta.timestamp \
				 order by  ta.serevity,ta.timestamp " % (no_of_devices, date_temp1, date_temp2)
                cursor.execute(query)
                total_result = cursor.fetchall()
                # current alarm calculation start here.
                for total in total_result:
                    total_trap.append(make_list(total))
                query = "SELECT date(ta.trap_receive_date),time(ta.trap_receive_date),ta.trap_receive_date,device_type.device_name,hostgroups.hostgroup_name,hosts.host_name,ta.agent_id,ta.trap_event_id,ta.trap_event_type,ta.description,ta.serevity\
	 			 FROM trap_alarm_current as ta join (select host_name,host_id,ip_address,device_type_id from hosts limit %s) as hosts on hosts.ip_address=ta.agent_id\
			         INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
			         INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				 INNER JOIN device_type ON device_type.device_type_id=hosts.device_type_id\
				 where  ta.timestamp between '%s' AND '%s' group by ta.serevity,ta.timestamp \
				 order by  ta.serevity,ta.timestamp " % (no_of_devices, date_temp1, date_temp2)
                cursor.execute(query)
                alarm_result = cursor.fetchall()
                for alarm in alarm_result:
                    currrent_alarm.append(make_list(alarm))

            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query = "SELECT date(ta.timestamp),time(ta.timestamp),ta.trap_receive_date,device_type.device_name,hostgroups.hostgroup_name,hosts.host_name,ta.agent_id,ta.trap_event_id,ta.trap_event_type,ta.description,ta.serevity\
	 			 FROM trap_alarms as ta join (select host_name,host_id,ip_address,device_type_id from hosts ) as hosts on hosts.ip_address=ta.agent_id\
		                 INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
		                 INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				 INNER JOIN device_type ON device_type.device_type_id=hosts.device_type_id\
				 where  ta.timestamp between '%s' AND '%s' AND hosts.host_id IN %s group by ta.serevity,ta.timestamp \
				 order by  ta.serevity,ta.timestamp " % (date_temp1, date_temp2, host_data)
                cursor.execute(query)
                total_result = cursor.fetchall()
                for total in total_result:
                    total_trap.append(make_list(total))
                    # this code calculate current alarm for devices
                query = "SELECT date(ta.timestamp),time(ta.timestamp),ta.trap_receive_date,device_type.device_name,hostgroups.hostgroup_name,hosts.host_name,ta.agent_id,ta.trap_event_id,ta.trap_event_type,ta.description,ta.serevity\
	 			 FROM trap_alarm_current as ta join (select host_name,host_id,ip_address,device_type_id from hosts ) as hosts on hosts.ip_address=ta.agent_id\
		                 INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
		                 INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
				 INNER JOIN device_type ON device_type.device_type_id=hosts.device_type_id\
				 where  ta.timestamp between '%s' AND '%s' AND hosts.host_id IN %s group by ta.serevity,ta.timestamp \
				 order by  ta.serevity,ta.timestamp " % (date_temp1, date_temp2, host_data)
                cursor.execute(query)
                alarm_result = cursor.fetchall()
                for alarm in alarm_result:
                    currrent_alarm.append(make_list(alarm))
            return total_trap, currrent_alarm
        except Exception, e:
            return str(e), 1
        finally:
            conn.close()

    def event_excel_creating(self, event_total, alarm_result):
        """

        @param event_total:
        @param alarm_result:
        @return:
        """
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        try:
            if len(event_total) == 0:
                return 1
            flag = 0
            xls_book = xlwt.Workbook(encoding='ascii')
            # styling part start of excel file.
            style = xlwt.XFStyle()  # Create Style
            borders = xlwt.Borders()  # Create Borders
            borders.left = xlwt.Borders.THIN  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 23
            borders.right_colour = 23
            borders.top_colour = 23
            borders.bottom_colour = 23
            style.borders = borders  # Add
            pattern = xlwt.Pattern()  # Create the Pattern
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern_fore_colour = 16
            # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 =
            # Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 =
            # Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow ,
            # almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray,
            # 23 = Dark Gray, the list goes on...
            style.pattern = pattern  # Add Pattern to Style
            font = xlwt.Font()  # Create Font
            font.bold = True  # Set font to Bold
            # style = xlwt.XFStyle() # Create Style
            font.colour_index = 0x09
            style.font = font  # Add Bold Font to Style
            alignment = xlwt.Alignment()  # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
            alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
            # style = xlwt.XFStyle() # Create Style
            style.alignment = alignment  # Add Alignment to Style

            style1 = xlwt.XFStyle()  # Create Style
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style1.alignment = alignment  # Add Alignment to Style

            # -----------   End of style ---------#
            # average crc and phy error creation start.
            # event_total=sorted(event_total, key=itemgetter(5))
            count = 0
            event_name = ['Informational(0)', 'Normal(1)', 'Informational(2)',
                          'Minor(3)', 'Major(4)', 'Critical(5)']
            for k in range(len(event_total) - 1):
                if flag == 0:
                    i = 0
                    # count+=1
                    xls_sheet = xls_book.add_sheet('%s,' % (str(event_name[int(
                        event_total[k][10])])), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(0, 0, 0, 9, "%s Events Information" % (str(
                        event_name[int(event_total[k][10])])), style)
                    xls_sheet.write_merge(2, 2, 0, 9, "")
                    i = 4
                    # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                    # horiz center,color grey25')
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = [
                        'system receive date', 'system receive time', 'Event receive date', 'device type', 'group name',
                        'host name', 'agent id', 'event id', 'event type', 'description']

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)
                    count = i
                if int(event_total[k][10]) == int(event_total[k + 1][10]):
                    flag = 1
                    count += 1
                    for j in range(len(event_total[k]) - 1):
                        if j < 8:
                            width = 7000
                            xls_sheet.write(i, j, event_total[k][j], style1)
                            xls_sheet.col(j).width = width
                        elif j == 8:
                            width = 10000
                            xls_sheet.write(i, j, event_total[k][j], style1)
                            xls_sheet.col(j).width = width
                        else:
                            width = 20000
                            xls_sheet.write(i, j, event_total[k][j], style1)
                            xls_sheet.col(j).width = width
                    i = i + 1
                else:
                    flag = 0
                    for j in range(len(event_total[k]) - 1):
                        if j < 8:
                            width = 7000
                            xls_sheet.write(i, j, event_total[k][j], style1)
                            xls_sheet.col(j).width = width
                        elif j == 8:
                            width = 10000
                            xls_sheet.write(i, j, event_total[k][j], style1)
                            xls_sheet.col(j).width = width
                        else:
                            width = 20000
                            xls_sheet.write(i, j, event_total[k][j], style1)
                            xls_sheet.col(j).width = width

            if flag == 1:
                for j in range(len(event_total[len(event_total) - 1]) - 1):
                    if j < 8:
                        width = 7000
                        xls_sheet.write(count, j, event_total[k][j], style1)
                        xls_sheet.col(j).width = width
                    elif j == 8:
                        width = 10000
                        xls_sheet.write(count, j, event_total[k][j], style1)
                        xls_sheet.col(j).width = width
                    else:
                        width = 20000
                        xls_sheet.write(count, j, event_total[k][j], style1)
                        xls_sheet.col(j).width = width
            else:
                i = 0
                xls_sheet = xls_book.add_sheet('%s,' % (str(event_name[int(
                    event_total[len(event_total) - 1][10])])), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(0, 0, 0, 9, "%s Events Information" % (
                    str(event_name[int(event_total[k][10])])), style)
                xls_sheet.write_merge(2, 2, 0, 9, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = [
                    'system receive date', 'system receive time', 'Event receive date',
                    'device type', 'group name', 'host name', 'agent id', 'event id', 'event type', 'description']

                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for j in range(len(event_total[len(event_total) - 1]) - 1):
                    if j < 8:
                        width = 7000
                        xls_sheet.write(
                            i, j, event_total[len(event_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
                    elif j == 8:
                        width = 10000
                        xls_sheet.write(
                            i, j, event_total[len(event_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
                    else:
                        width = 20000
                        xls_sheet.write(
                            i, j, event_total[len(event_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
            if len(event_total) > 1:
                if event_total[len(event_total) - 1][10] == event_total[len(event_total) - 2][10]:
                    for j in range(len(event_total[len(event_total) - 1]) - 1):
                        if j < 8:
                            width = 7000
                            xls_sheet.write(
                                i, j, event_total[len(event_total) - 1][j], style1)
                            xls_sheet.col(j).width = width
                        elif j == 8:
                            width = 10000
                            xls_sheet.write(
                                i, j, event_total[len(event_total) - 1][j], style1)
                            xls_sheet.col(j).width = width
                        else:
                            width = 20000
                            xls_sheet.write(
                                i, j, event_total[len(event_total) - 1][j], style1)
                            xls_sheet.col(j).width = width
            elif len(event_total) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Total_event)%s,' % (event_total[k][10], str(
                    event_name[int(event_total[k][10])])), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 9, "Informational Events", style)
                xls_sheet.write_merge(2, 2, 0, 9, "")
                i = 4
                # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                # horiz center,color grey25')
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = [
                    'system receive date', 'system receive time', 'Event receive date',
                    'device type', 'group name', 'host name', 'agent id', 'event id', 'event type', 'description']

                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for j in range(len(event_total[len(event_total) - 1])):
                    if j < 8:
                        width = 7000
                        xls_sheet.write(
                            i, j, event_total[len(event_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
                    elif j == 8:
                        width = 10000
                        xls_sheet.write(
                            i, j, event_total[len(event_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
                    else:
                        width = 20000
                        xls_sheet.write(
                            i, j, event_total[len(event_total) - 1][j], style1)
                        xls_sheet.col(j).width = width

            # report generating for current alarm
            i = 0
            xls_sheet = xls_book.add_sheet(
                "Alarm Information", cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, 9, "Alarm Information", style)
            xls_sheet.write_merge(2, 2, 0, 9, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = [
                'system receive date', 'system receive time', 'Event receive date',
                'device type', 'group name', 'host name', 'agent id', 'event id', 'event type', 'description']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(alarm_result)):
                for j in range(len(alarm_result[k]) - 1):
                    if j < 8:
                        width = 7000
                        xls_sheet.write(i, j, alarm_result[k][j], style1)
                        xls_sheet.col(j).width = width
                    elif j == 8:
                        width = 10000
                        xls_sheet.write(i, j, alarm_result[k][j], style1)
                        xls_sheet.col(j).width = width
                    else:
                        width = 20000
                        xls_sheet.write(i, j, alarm_result[k][j], style1)
                        xls_sheet.col(j).width = width
                i = i + 1
            xls_book.save(
                '/omd/sites/%s/share/check_mk/web/htdocs/download/Event_excel_report.xls' % nms_instance)
            return '0'
        except Exception, e:
            return str(e)

    def group_data(self, search_text, common):
        """

        @param search_text:
        @param common:
        @return:
        """
        try:
            output_list = []
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            if common == True or common == 'true':
                sel_query = "SELECT hostgroups.hostgroup_id, hostgroups.hostgroup_name FROM hosts\
                        INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                        INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                        WHERE hostgroups.hostgroup_name LIKE '%%%s%%'" % (search_text)
            else:
                sel_query = "SELECT hostgroups.hostgroup_id, hostgroups.hostgroup_name FROM hosts\
                        INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                        INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                        WHERE hostgroups.hostgroup_name LIKE '%%%s%%' AND hosts.device_type_id='ODU16'" % (search_text)
            cursor.execute(sel_query)
            group_result = cursor.fetchall()
            # close the cursor and database connection
            return group_result, 0
        except Exception, e:
            return e, 1
        finally:
            cursor.close()
            conn.close()

    def host_data(self, search_text, common):
        """

        @param search_text:
        @param common:
        @return:
        """
        try:
            host_result = ''
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            if common == 'true' or common == True:
                if (cursor.execute("SELECT hosts.host_id, hosts.ip_address,hosts.host_alias,hosts.mac_address FROM hosts\
		                        INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
		                        INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
		                        WHERE hostgroups.hostgroup_id LIKE '%s'" % (search_text))):
                    host_result = cursor.fetchall()
                if len(host_result) == 0:
                    cursor.execute("SELECT hosts.host_id, hosts.ip_address,hosts.host_alias,hosts.mac_address FROM hosts\
			                        INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
			                        INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
			                        WHERE (hosts.mac_address LIKE '%%%s%%' OR hosts.ip_address LIKE '%%%s%%' OR hosts.host_alias LIKE '%%%s%%'\
			                        OR hostgroups.hostgroup_id LIKE '%s')" % (
                    search_text, search_text, search_text, search_text))
                    host_result = cursor.fetchall()
            else:
                if (cursor.execute("SELECT hosts.host_id, hosts.ip_address,hosts.host_alias,hosts.mac_address FROM hosts\
		                        INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
		                        INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
		                        WHERE hostgroups.hostgroup_id LIKE '%s' AND hosts.device_type_id like 'ODU16%%' " % (
                search_text))):
                    host_result = cursor.fetchall()
                if len(host_result) == 0:
                    cursor.execute("SELECT hosts.host_id, hosts.ip_address,hosts.host_alias,hosts.mac_address FROM hosts\
			                        INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
			                        INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
			                        WHERE (hosts.mac_address LIKE '%%%s%%' OR hosts.ip_address LIKE '%%%s%%' OR hosts.host_alias LIKE '%%%s%%'\
			                        OR hostgroups.hostgroup_id LIKE '%s') AND hosts.device_type_id like 'ODU16%%' " % (
                    search_text, search_text, search_text, search_text))
                    host_result = cursor.fetchall()
            return host_result, 0
            # close the cursor and database connection
        except Exception, e:
            return e, 1
        finally:
            cursor.close()
            conn.close()

    def inventory_excel_report_creation(self, user_id):
        """

        @param user_id:
        @return: @raise:
        """
        try:
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system
            # create the excel file
            xls_book = xlwt.Workbook(encoding='ascii')

            # Excel reproting Style part
            style = xlwt.XFStyle()
            borders = xlwt.Borders()
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 23
            borders.right_colour = 23
            borders.top_colour = 23
            borders.bottom_colour = 23
            style.borders = borders
            pattern = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = 16
            style.pattern = pattern
            font = xlwt.Font()
            font.bold = True
            font.colour_index = 0x09
            style.font = font
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style.alignment = alignment

            style1 = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style1.alignment = alignment
            # -----------   End of style ---------#

            ra_mac = '--'
            freq = '--'
            gr_name = '--'
            ac_ver = '--'
            hw_ver = '--'
            hw_sr_no = '--'
            # create the database connection
            db, cursor = mysql_connection()
            if db == 1:
                raise Exception()

            hst_bll = HostBll(user_id)
            # creating the HostBll object
            # Active hosts information
            all_hosts = hst_bll.grid_view_active_host_report(
            )     # fetching all hosts data from database
            hosts_list = []
            # creating empty list [we will use this in datatables]
            tdmoip = 'N/A'
            for hst in all_hosts:
                if (hst.device_name).strip() == 'UBR' or (hst.device_name).strip() == 'RM18':
                    sql = "SELECT ra.ra_mac_address,fm.rf_channel_frequency,hostgroups.hostgroup_name,sw.active_version ,hw.hw_version,hw.hw_serial_no FROM hosts LEFT JOIN \
						  get_odu16_ra_status_table as ra ON ra.host_id=hosts.host_id \
						LEFT JOIN set_odu16_ra_tdd_mac_config as fm ON fm.config_profile_id = hosts.config_profile_id \
						LEFT JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
						LEFT JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
						LEFT JOIN  get_odu16_sw_status_table as sw ON sw.host_id=hosts.host_id LEFT JOIN get_odu16_hw_desc_table as hw ON hw.host_id=hosts.host_id\
						 WHERE hosts.ip_address='%s'" % str(hst.ip_address)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ra_mac = '--' if result[0][
                                             0] == None or result[0][0] == '' else result[0][0]
                        freq = '--' if result[0][
                                           1] == None or result[0][1] == '' else result[0][1]
                        gr_name = '--' if result[0][
                                              2] == None or result[0][2] == '' else result[0][2]
                        ac_ver = '--' if result[0][
                                             3] == None or result[0][3] == '' else result[0][3]
                        hw_ver = '--' if result[0][
                                             4] == None or result[0][4] == '' else result[0][4]
                        hw_sr_no = '--' if result[0][
                                               5] == None or result[0][5] == '' else result[0][5]
                        tdmoip = 'N/A'

                elif (hst.device_name).strip() == 'UBRe' or (hst.device_name).strip() == 'RM':
                    sql = """SELECT ra.raMacAddress, fm.rafrequency, hostgroups.hostgroup_name, sw.activeVersion, hw.hwVersion, hw.hwSerialNo
						FROM hosts LEFT JOIN odu100_raStatusTable AS ra ON ra.host_id = hosts.host_id
						JOIN odu100_raPreferredRFChannelTable AS fm ON hosts.config_profile_id = fm.config_profile_id
						LEFT JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id
						LEFT JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id
						LEFT JOIN odu100_swStatusTable AS sw ON sw.host_id = hosts.host_id
						LEFT JOIN odu100_hwDescTable AS hw ON hw.host_id = hosts.host_id
						WHERE hosts.ip_address =  '%s'
						ORDER BY hosts.timestamp DESC
						LIMIT 0 , 1""" % str(hst.ip_address)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ra_mac = '--' if result[0][
                                             0] == None or result[0][0] == '' else result[0][0]
                        freq = '--' if result[0][
                                           1] == None or result[0][1] == '' else result[0][1]
                        gr_name = '--' if result[0][
                                              2] == None or result[0][2] == '' else result[0][2]
                        ac_ver = '--' if result[0][
                                             3] == None or result[0][3] == '' else result[0][3]
                        hw_ver = '--' if result[0][
                                             4] == None or result[0][4] == '' else result[0][4]
                        hw_sr_no = '--' if result[0][
                                               5] == None or result[0][5] == '' else result[0][5]
                        tdmoip = 'N/A'

                elif (hst.device_name).strip() == 'IDU4' or (hst.device_name).strip() == 'IDU':
                    sql = "SELECT hostgroups.hostgroup_name,sw.activeVersion ,sw.passiveVersion,hw.hwSerialNumber,hw.tdmoipInterfaceMac FROM hosts \
						LEFT JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
						LEFT JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
						LEFT JOIN  idu_swStatusTable as sw ON sw.host_id=hosts.host_id LEFT JOIN idu_iduInfoTable as hw ON hw.host_id=hosts.host_id\
						 WHERE hosts.ip_address='%s'" % str(hst.ip_address)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ra_mac = 'N/A'
                        freq = 'N/A'
                        gr_name = '--' if result[0][
                                              0] == None or result[0][0] == '' else result[0][0]
                        ac_ver = '--' if result[0][
                                             1] == None or result[0][1] == '' else result[0][1]
                        hw_ver = '--' if result[0][
                                             2] == None or result[0][2] == '' else result[0][2]
                        hw_sr_no = '--' if result[0][
                                               3] == None or result[0][3] == '' else result[0][3]
                        tdmoip = '--' if result[0][
                                             4] == None or result[0][4] == '' else result[0][4]

                elif (hst.device_name).strip() == 'Access Point' or (hst.device_name).strip() == 'AP':
                    sql = "SELECT hostgroups.hostgroup_name,sw.softwareVersion ,sw.hardwareVersion FROM hosts \
						LEFT JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
						LEFT JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
						LEFT JOIN  ap25_versions as sw ON sw.host_id=hosts.host_id \
						 WHERE hosts.ip_address='%s'" % str(hst.ip_address)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ra_mac = 'N/A'
                        freq = 'N/A'
                        gr_name = '--' if result[0][
                                              0] == None or result[0][0] == '' else result[0][0]
                        ac_ver = '--' if result[0][
                                             1] == None or result[0][1] == '' else result[0][1]
                        hw_ver = '--' if result[0][
                                             2] == None or result[0][2] == '' else result[0][2]
                        hw_sr_no = '--'
                        tdmoip = 'N/A'
                else:
                    ra_mac = '--'
                    freq = '--'
                    ac_ver = '--'
                    hw_ver = '--'
                    hw_sr_no = '--'
                    tdmoip = 'N/A'
                hosts_list.append([
                    hst.host_alias != None and hst.host_alias or "-",
                    hst.ip_address != None and hst.ip_address or "-",
                    hst.device_name != None and hst.device_name or "-",
                    hst.mac_address != None and hst.mac_address or "-",
                    gr_name, ac_ver, hw_ver, hw_sr_no,
                    hst.creation_time != None and hst.creation_time.strftime(
                        "%d-%m-%Y %H:%M") or "-",
                    hst.created_by != None and hst.created_by or "-", ra_mac, freq,
                    tdmoip])       # creating 2D List of host details

            xls_sheet = xls_book.add_sheet(
                'Active Host(s)', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 10, "Active Host(s) Information", style)
            xls_sheet.write_merge(1, 1, 0, 10, "")
            xls_sheet.write_merge(2, 2, 0, 10, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            # headings = ['Host Alias','IP Address','Device Name','MAC','RA
            # MAC','Frequency','Group Name','Active Software Version','Hardware
            # Version','Hardware Serial No.','Active Since (Date -
            # Time)','Added By']
            headings = [
                'Host Alias', 'IP Address', 'Device Name', 'MAC', 'Group Name', 'Active Software Version',
                'Hardware Version', 'Hardware Serial No.',
                'Active Since (Date - Time)', 'Added By', 'RA MAC', 'Frequency', 'TDMOIP MAC']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(hosts_list)):
                for j in range(len(hosts_list[k])):
                    width = 5000
                    xls_sheet.write(i, j, hosts_list[k][j], style1)
                    xls_sheet.col(j).width = width
                i = i + 1

            # this is for disable hosts information
            all_hosts = hst_bll.grid_view_disable_host_report(
            )     # fetching all hosts data from database
            disable_host = []
            # creating empty list [we will use this in datatables]
            for hst in all_hosts:
                if (hst.device_name).strip() == 'UBR':
                    sql = "SELECT ra.ra_mac_address,fm.rf_channel_frequency,hostgroups.hostgroup_name,sw.active_version ,hw.hw_version,hw.hw_serial_no FROM hosts LEFT JOIN \
						  get_odu16_ra_status_table as ra ON ra.host_id=hosts.host_id \
						LEFT JOIN set_odu16_ra_tdd_mac_config as fm ON fm.config_profile_id = hosts.config_profile_id \
						LEFT JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
						LEFT JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
						LEFT JOIN  get_odu16_sw_status_table as sw ON sw.host_id=hosts.host_id LEFT JOIN get_odu16_hw_desc_table as hw ON hw.host_id=hosts.host_id\
						 WHERE hosts.ip_address='%s'" % str(hst.ip_address)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ra_mac = '--' if result[0][
                                             0] == None or result[0][0] == '' else result[0][0]
                        freq = '--' if result[0][
                                           1] == None or result[0][1] == '' else result[0][1]
                        gr_name = '--' if result[0][
                                              2] == None or result[0][2] == '' else result[0][2]
                        ac_ver = '--' if result[0][
                                             3] == None or result[0][3] == '' else result[0][3]
                        hw_ver = '--' if result[0][
                                             4] == None or result[0][4] == '' else result[0][4]
                        hw_sr_no = '--' if result[0][
                                               5] == None or result[0][5] == '' else result[0][5]

                elif (hst.device_name).strip() == 'UBRe':
                    sql = """SELECT ra.raMacAddress, fm.rafrequency, hostgroups.hostgroup_name, sw.activeVersion, hw.hwVersion, hw.hwSerialNo
						FROM hosts LEFT JOIN odu100_raStatusTable AS ra ON ra.host_id = hosts.host_id
						JOIN odu100_raPreferredRFChannelTable AS fm ON hosts.config_profile_id = fm.config_profile_id
						LEFT JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id
						LEFT JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id
						LEFT JOIN odu100_swStatusTable AS sw ON sw.host_id = hosts.host_id
						LEFT JOIN odu100_hwDescTable AS hw ON hw.host_id = hosts.host_id
						WHERE hosts.ip_address =  '%s'
						ORDER BY hosts.timestamp DESC
						LIMIT 0 , 1""" % str(hst.ip_address)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ra_mac = '--' if result[0][
                                             0] == None or result[0][0] == '' else result[0][0]
                        freq = '--' if result[0][
                                           1] == None or result[0][1] == '' else result[0][1]
                        gr_name = '--' if result[0][
                                              2] == None or result[0][2] == '' else result[0][2]
                        ac_ver = '--' if result[0][
                                             3] == None or result[0][3] == '' else result[0][3]
                        hw_ver = '--' if result[0][
                                             4] == None or result[0][4] == '' else result[0][4]
                        hw_sr_no = '--' if result[0][
                                               5] == None or result[0][5] == '' else result[0][5]

                disable_host.append([
                    hst.host_alias != None and hst.host_alias or "-",
                    hst.ip_address != None and hst.ip_address or "-",
                    hst.device_name != None and hst.device_name or "-",
                    hst.mac_address != None and hst.mac_address or "-",
                    ra_mac, freq, gr_name, ac_ver, hw_ver, hw_sr_no,
                    hst.timestamp != None and hst.timestamp.strftime(
                        "%d-%m-%Y %H:%M") or "-",
                    hst.updated_by != None and hst.updated_by or "-"])       # creating 2D List of host details
            xls_sheet = xls_book.add_sheet(
                'Disabled Host(s)', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 11, "Disabled Host(s) Information", style)
            xls_sheet.write_merge(1, 1, 0, 11, "")
            xls_sheet.write_merge(2, 2, 0, 11, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = [
                'Host Alias', 'IP Address', 'Device Name', 'MAC', 'RA MAC', 'Frequency', 'Group Name',
                'Active Software Version', 'Hardware Version',
                'Hardware Serial No.', 'Disabled Since (Date - Time)', 'Disabled By']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(disable_host)):
                for j in range(len(disable_host[k])):
                    width = 5000
                    xls_sheet.write(i, j, disable_host[k][j], style1)
                    xls_sheet.col(j).width = width
                i = i + 1

            # deleted host information
            all_hosts = hst_bll.grid_view_deleted_host_report(
            )     # fetching all hosts data from database
            deleted_host = []
            # creating empty list [we will use this in datatables]
            for hst in all_hosts:
                deleted_host.append([
                    # hst.host_name != None and hst.host_name or "-",
                    hst.host_alias != None and hst.host_alias or "-",
                    hst.ip_address != None and hst.ip_address or "-",
                    hst.device_name != None and hst.device_name or "-",
                    hst.mac_address != None and hst.mac_address or "-",
                    hst.updated_by != None and hst.updated_by or "-",
                    hst.timestamp != None and hst.timestamp.strftime(
                        "%d-%m-%Y %H:%M") or "-"])       # creating 2D List of host details

            xls_sheet = xls_book.add_sheet(
                'Deleted Host(s)', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 6, "Deleted Host(s) Information", style)
            xls_sheet.write_merge(1, 1, 0, 6, "")
            xls_sheet.write_merge(2, 2, 0, 6, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Host Alias', 'IP Address',
                        'Device Name', 'MAC Address', 'Updated By', 'Time']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(deleted_host)):
                for j in range(len(deleted_host[k])):
                    width = 7000
                    xls_sheet.write(i, j, deleted_host[k][j], style1)
                    xls_sheet.col(j).width = width
                i = i + 1

            # Discovered host information
            # get the ra MAC address from user.

            all_hosts = hst_bll.grid_view_tcp_discovered_host_report(
            )     # fetching all hosts data from database
            hosts_list = []
            # creating empty list [we will use this in datatables]
            s_no = 0
            temp_list = []
            for hst in all_hosts:
                if hst.ip_address in temp_list:
                    pass
                else:
                    s_no += 1
                    hosts_list.append([str(hst.ne_id),
                                       "TCP",
                                       hst.ip_address != None and hst.ip_address or "",
                                       hst.site_mac != None and hst.site_mac or "",
                                       hst.product_id == 6021 and "Master" or "Slave",
                                       hst.timestamp != None and hst.timestamp.strftime(
                                           "%d-%m-%Y %H:%M") or ""])       # creating 2D List of host details
                    temp_list.append(hst.ip_address)

            all_hosts2 = hst_bll.grid_view_discovered_host_report(
            )     # fetching all hosts data from database
            for hst in all_hosts2:
                if hst.ip_address in temp_list:
                    pass
                else:
                    s_no += 1
                    hosts_list.append([str(hst.discovered_host_id),
                                       hst.discovery_type_id,
                                       hst.ip_address != None and hst.ip_address or "",
                                       hst.mac_address != None and hst.mac_address or "",
                                       " - ",
                                       hst.timestamp != None and hst.timestamp.strftime(
                                           "%d-%m-%Y %H:%M") or ""])       # creating 2D List of host details
                    temp_list.append(hst.ip_address)

                    # creating empty list [we will use this in datatables]
            discovered_host = []
            for hst in hosts_list:
            #			cursor.execute("SELECT ra.raMacAddress FROM hosts INNER JOIN  odu100_raStatusTable as ra ON ra.host_id=hosts.host_id WHERE hosts.ip_address='%s'"%str(hst[2]))
            #			ra_mac=cursor.fetchall()
                discovered_host.append([str(hst[1]), str(hst[2]), str(
                    hst[3]), str(hst[4]), str(hst[5])])       # creating 2D List of host details
            xls_sheet = xls_book.add_sheet(
                'Discovered Host(s)', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 4, "Discovered Host(s) Information", style)
            xls_sheet.write_merge(1, 1, 0, 4, "")
            xls_sheet.write_merge(2, 2, 0, 4, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Discover Type', 'IP Address',
                        'Site MAC', 'Type', 'Time']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(discovered_host)):
                for j in range(len(discovered_host[k])):
                    width = 5000
                    xls_sheet.write(i, j, discovered_host[k][j], style1)
                    xls_sheet.col(j).width = width
                i = i + 1

            xls_book.save(
                '/omd/sites/%s/share/check_mk/web/htdocs/download/inventory_report.xls' % nms_instance)
            return 0
            # Exception Handling
        except Exception as e:
            return str(e)


def outage_graph(host_id, start_date, end_date):
    """this function create the outage graph field and show the outage graph.
    @param host_id:
    @param start_date:
    @param end_date:
    """
    date_days = []  # this list store the days information with date.
    up_state = []  # Its store the total up state of each day in percentage.
    down_state = []
    # Its store the total down state of each day in percentage.
    output_dict = {}  # its store the actual output for display in graph.
    last_status = 0

    try:
        current_date = datetime.date(
            datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
        current_datetime = datetime.strptime(str(
            current_date) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        last_datetime = datetime.strptime(
            str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        start_time = current_datetime
        temp_date = current_datetime
        temp_li = []
        total_li = []
        #        current_datetime=datetime.strptime(str(current_date+timedelta(days=-5))+" 00:00:00",'%Y-%m-%d %H:%M:%S') # convert the string in  datetime.
        # last_datetime=datetime.strptime(str(current_date+timedelta(days=-1))+" 23:59:59",'%Y-%m-%d %H:%M:%S') # convert the string in  datetime.
        # this datetime last status calculation
        #        last_status_current_time=datetime.strptime(str(current_date+timedelta(days=-6))+" 00:00:00",'%Y-%m-%d %H:%M:%S') # convert the string in  datetime.
        # last_status_end_time=datetime.strptime(str(current_date+timedelta(days=-5))+"
        # 23:59:59",'%Y-%m-%d %H:%M:%S') # convert the string in  datetime.

        # connection from mysql

        # db=MySQLdb.Connect('172.22.0.94','root','root','nmsp')
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        #        if db ==1:
        #            raise SelfException(cursor)

        ip_address = ""
        # sel_query="SELECT trap_event_id,trap_event_type,timestamp FROM
        # system_alarm_table WHERE timestamp>='%s' and timestamp<='%s' and
        # agent_id='%s' order by timestamp "%(start_date,end_date,ip_address)
        sel_query = "SELECT trap_event_id,trap_event_type,timestamp,host.host_name,host.ip_address,host.host_alias,hostgroups.hostgroup_name FROM system_alarm_table as go16 \
	join ( select host_id,host_name,ip_address,host_alias from hosts ) as host on go16.agent_id=host.ip_address \
	INNER JOIN (select host_id,hostgroup_id from hosts_hostgroups) as  hosts_hostgroups ON hosts_hostgroups.host_id = host.host_id  \
	INNER JOIN (select hostgroup_id , hostgroup_name from hostgroups) as  hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id \
	where host.host_id='%s' and go16.timestamp>='%s' and go16.timestamp<='%s'" % (host_id, start_date, end_date)
        cursor.execute(sel_query)
        result = cursor.fetchall()
        if result != ():
            ip_address = result[0][4]
        sel_query = "SELECT trap_event_id,trap_event_type FROM system_alarm_table WHERE timestamp<='%s' and agent_id='%s' order by timestamp limit 1" % (
            start_date, ip_address)
        cursor.execute(sel_query)
        status_result = cursor.fetchall()

        if len(status_result) > 0:
            last_status = status_result[0][0]
        else:
            if len(result) > 0:
                last_status = result[0][0]
                start_time = result[0][2]
        i = 0
        flag = 0
        total_down_time = 0
        total_up_time = 0
        total = 0
        for no in range(len(result)):
            if str(datetime.date(temp_date) + timedelta(days=i)) == datetime.strptime(str(result[no][2]),
                                                                                      '%Y-%m-%d %H:%M:%S').strftime(
                    '%Y-%m-%d'):
                flag = 1
                if int(last_status) == 50002:
                    total_up_time += abs((result[no][2] - start_time).days * 1440 + (
                        result[no][2] - start_time).seconds / 60)
                    start_time = result[no][2]
                    last_status = result[no][0]
                else:
                    total_down_time += abs((result[no][2] - start_time).days * 1440 + (
                        result[no][2] - start_time).seconds / 60)
                    start_time = result[no][2]
                    last_status = result[no][0]
            else:
                if flag == 1 and (int(last_status) == 50001 or int(last_status) == 50002):
                    temp_datetime = datetime.strptime(str(datetime.date(
                        start_time)) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                    start_time = temp_datetime
                    if int(last_status) == 50002:
                        total_up_time += abs((temp_datetime - result[no - 1][2]).days *
                                             1440 + (temp_datetime - result[no - 1][2]).seconds / 60)
                    else:
                        total_down_time += abs((temp_datetime - result[no - 1][2]).days *
                                               1440 + (temp_datetime - result[no - 1][2]).seconds / 60)
                    date_days.append((temp_date + timedelta(days=(i))))
                    total = total_down_time + total_up_time
                    up_state.append(
                        round((total_up_time * 100) / float(total), 2))
                    down_state.append(
                        round((total_down_time * 100) / float(total), 2))
                    temp_li = []
                    temp_li.append(str(date_days[-1]))
                    temp_li.append(result[0][3])
                    temp_li.append(result[0][4])
                    temp_li.append(result[0][5])
                    temp_li.append(result[0][6])
                    temp_li.append("%.2f" % up_state[-1])
                    temp_li.append("%.2f" % down_state[-1])
                    total_li.append(temp_li)
                    total_down_time = 0
                    total_up_time = 0
                    if int(last_status) == 50002:
                        total_up_time += abs((result[no][2] - temp_datetime).days *
                                             1440 + (result[no][2] - temp_datetime).seconds / 60)
                        start_time = result[no][2]
                        last_status = result[no][0]
                    else:
                        total_down_time += abs((result[no][2] - temp_datetime).days *
                                               1440 + (result[no][2] - temp_datetime).seconds / 60)
                        start_time = result[no][2]
                        last_status = result[no][0]

                if flag == 0 and (int(last_status) == 50001 or int(last_status) == 50002):
                    temp_datetime = datetime.strptime(str(datetime.date(
                        start_time)) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                    temp_start_datetime = datetime.strptime(str(datetime.date(
                        start_time)) + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                    start_time = temp_datetime
                    if int(last_status) == 50002:
                        total_up_time += abs((temp_datetime - temp_start_datetime).days * 1440 +
                                             (temp_datetime - temp_start_datetime).seconds / 60)
                    else:
                        total_down_time += abs((temp_datetime - temp_start_datetime).days *
                                               1440 + (temp_datetime - temp_start_datetime).seconds / 60)
                    date_days.append((temp_date + timedelta(days=(i))))
                    total = total_down_time + total_up_time
                    up_state.append(
                        round((total_up_time * 100) / float(total), 2))
                    down_state.append(
                        round((total_down_time * 100) / float(total), 2))
                    temp_li = []
                    temp_li.append(str(date_days[-1]))
                    temp_li.append(result[0][3])
                    temp_li.append(result[0][4])
                    temp_li.append(result[0][5])
                    temp_li.append(result[0][6])
                    temp_li.append("%.2f" % up_state[-1])
                    temp_li.append("%.2f" % down_state[-1])
                    total_li.append(temp_li)
                    total_down_time = 0
                    total_up_time = 0
                    if int(last_status) == 50002:
                        total_up_time += abs((result[no][2] - temp_datetime).days *
                                             1440 + (result[no][2] - temp_datetime).seconds / 60)
                        start_time = result[no][2]
                        last_status = result[no][0]
                    else:
                        total_down_time += abs((result[no][2] - temp_datetime).days *
                                               1440 + (result[no][2] - temp_datetime).seconds / 60)
                        start_time = result[no][2]
                        last_status = result[no][0]
                i += 1
                flag = 0

        for j in range(i, (datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_date,
                                                                                                '%Y-%m-%d %H:%M:%S')).days):
            up_state.append(0)
            down_state.append(100)
            date_days.append(str(temp_date + timedelta(days=(i))))
            temp_li = []
            temp_li.append(str(date_days[-1]))
            temp_li.append(result[0][3])
            temp_li.append(result[0][4])
            temp_li.append(result[0][5])
            temp_li.append(result[0][6])
            temp_li.append("%.2f" % up_state[-1])
            temp_li.append("%.2f" % down_state[-1])
            total_li.append(temp_li)
            i += 1
            # close the database and cursor connection.
        cursor.close()
        db.close()
        output_dict = {'success': 0, 'UpTime': up_state,
                       'DownTime': down_state, 'date_days': date_days, 'list': total_li}
        return output_dict
    # Exception Handling
    except Exception as e:
        output_dict = {'success': 1, 'real_msg': str(e[-1])}
        return output_dict


def main_outage(result_tuple, end_date):
    """

    @param result_tuple:
    @param end_date:
    @return:
    """
    try:
        is_date = 0
        main_date = ''
        main_ip = ''
        main_list = []
        uptime = None
        downtime = None
        prev_value = ''
        temp_temp = []
        for tpl in result_tuple:
            tpl_temp = tpl
            temp_ip = tpl[3]
            temp_date = tpl[2]
            temp_value = tpl[0]
            if temp_ip == main_ip:
                if temp_date.month > main_date.month or temp_date.day > main_date.day:
                    is_date = 1
                    day_diff = (temp_date - main_date).days
                    if day_diff > 1:
                        for i in range(1, day_diff + 1):
                            leftout_date = main_date + timedelta(days=i)
                            if prev_value == '50002':
                                main_list.append([leftout_date, main_ip, tpl_temp[
                                    4], tpl_temp[5], tpl_temp[6], timedelta(0, 86399), None])
                            elif prev_value == '50001':
                                main_list.append([leftout_date, main_ip, tpl_temp[
                                    4], tpl_temp[5], tpl_temp[6], None, timedelta(0, 86399)])

                else:
                    if temp_value == '50002':
                        if uptime == None:
                            uptime = (temp_date - main_date)
                        else:
                            uptime += (temp_date - main_date)

                    elif temp_value == '50001':
                        if downtime == None:
                            downtime = (temp_date - main_date)
                        else:
                            downtime += (temp_date - main_date)
            else:
                is_new = 1

            if is_new:
                if prev_value != '':
                    is_date = 1
                else:
                    main_date = temp_date
                main_ip = temp_ip
                is_new = 0

            if is_date:
                if uptime == None or downtime == None:
                    mid_date = datetime(main_date.year,
                                        main_date.month, main_date.day, 23, 59, 59)
                    delta = mid_date - main_date
                    if prev_value == '50002':
                        uptime = delta
                    elif prev_value == '50001':
                        downtime = delta
                main_list.append([main_date, main_ip, tpl_temp[4],
                                  tpl_temp[5], tpl_temp[6], uptime, downtime])
                main_date = temp_date
                uptime = None
                downtime = None
                is_date = 0

            prev_value = temp_value

        if uptime == None or downtime == None:
            mid_date = datetime(
                main_date.year, main_date.month, main_date.day, 23, 59, 59)
            delta = mid_date - main_date
            if prev_value == '50002':
                uptime = delta
            elif prev_value == '50001':
                downtime = delta
        main_list.append([main_date, main_ip, tpl_temp[4],
                          tpl_temp[5], tpl_temp[6], uptime, downtime])

        day_diff = (end_date - main_date).days
        if day_diff > 1:
            for i in range(1, day_diff + 1):
                leftout_date = main_date + timedelta(days=i)
                if prev_value == '50002':
                    main_list.append([leftout_date, main_ip, tpl_temp[
                        4], tpl_temp[5], tpl_temp[6], timedelta(0, 86399), None])
                elif prev_value == '50001':
                    main_list.append([leftout_date, main_ip, tpl_temp[
                        4], tpl_temp[5], tpl_temp[6], None, timedelta(0, 86399)])
        main_dict = {}
        main_dict['success'] = 0
        main_dict['result'] = main_list
        main_dict['outage'] = "main_outage"
        return main_dict
    except Exception, e:
        main_dict = {}
        main_dict['success'] = 1
        main_dict['result'] = str(e)
        return main_dict


def get_outage(no_of_devices, date1, date2, time1, time2, all_group, all_host):
    """

    @param no_of_devices:
    @param date1:
    @param date2:
    @param time1:
    @param time2:
    @param all_group:
    @param all_host:
    @return:
    """
    try:
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = conn.cursor()
        date1 = date1.replace("/", "-")
        date2 = date2.replace("/", "-")
        date1 = date1 + " " + time1
        date2 = date2 + " " + time2
        d1 = datetime.strptime(date1, "%d-%m-%Y %H:%M")
        d2 = datetime.strptime(date2, "%d-%m-%Y %H:%M")
        date_temp1 = str(d1)
        date_temp2 = str(d2)
        start_date = date_temp1
        end_date = date_temp2
        all_host = all_host.split(',')
        li_result = []
        # main_outage(result_tuple,end_date):
        main_result = []
        for j in all_host:
            sel_query = "SELECT trap_event_id,trap_event_type,timestamp,host.host_name,host.ip_address,host.host_alias,hostgroups.hostgroup_name FROM system_alarm_table as go16 \
		join ( select host_id,host_name,ip_address,host_alias from hosts ) as host on go16.agent_id=host.ip_address \
		INNER JOIN (select host_id,hostgroup_id from hosts_hostgroups) as  hosts_hostgroups ON hosts_hostgroups.host_id = host.host_id  \
		INNER JOIN (select hostgroup_id , hostgroup_name from hostgroups) as  hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id \
		where host.host_id='%s' and go16.timestamp>='%s' and go16.timestamp<='%s' order by timestamp" % (
            j, start_date, end_date)
            cursor.execute(sel_query)
            result = cursor.fetchall()

            sel_query = "SELECT trap_event_id,trap_event_type,timestamp,host.host_name,host.ip_address,host.host_alias,hostgroups.hostgroup_name FROM system_alarm_table as go16 \
		join ( select host_id,host_name,ip_address,host_alias from hosts ) as host on go16.agent_id=host.ip_address \
		INNER JOIN (select host_id,hostgroup_id from hosts_hostgroups) as  hosts_hostgroups ON hosts_hostgroups.host_id = host.host_id  \
		INNER JOIN (select hostgroup_id , hostgroup_name from hostgroups) as  hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id \
		 WHERE timestamp<='%s' and host.host_id='%s' order by timestamp desc limit 1" % (start_date, j)
            cursor.execute(sel_query)
            status_result = cursor.fetchall()
            if status_result != () and result != ():
                t_date = result[0][2]
                t_date = t_date.replace(hour=0, minute=0, second=0)
                t_list = ((status_result[0][0], status_result[0][1], t_date, status_result[0][3], status_result[0][
                    4], status_result[0][5], status_result[0][6]),)
                result = t_list + result

            m = MainOutage(result, datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"), datetime.strptime(
                start_date, "%Y-%m-%d %H:%M:%S"))
            temp_res = m.get_outage()
            # temp_res = main_outage(
            #     result, datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"))
            if str(temp_res['success']) == "0":
                li_res = temp_res['result']
                tr = []
                for i in li_res:
                    if i[-2] == None:
                        uptime = 0
                    else:
                        uptime = i[-2].seconds
                    if i[-1] == None:
                        downtime = 0
                    else:
                        downtime = i[-1].seconds
                    total = uptime + downtime
                    if total != 0:
                        i[0] = str(i[0])[:11]
                        i[-2] = (uptime * 100) / total
                        i[-1] = (downtime * 100) / total
                        if int(i[-2]) + int(i[-1]) != 100:
                            i[-2] = int(i[-2]) + 1
                        tr.append(i)
                        #[leftout_date,main_ip,tpl_temp[4],tpl_temp[5],tpl_temp[6],None,timedelta(0, 86399)])
                        main_result.append(i)

        result_dict = {}
        result_dict['success'] = 0
        result_dict['result'] = main_result
        result_dict['outage'] = "get_outage"
        return result_dict
    except Exception, e:
        main_dict = {}
        main_dict['success'] = 1
        main_dict['result'] = str(e)
        return main_dict
