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

from unmp_config import SystemConfig
from common_vars import make_list


class Report_bll(object):
    """
    Main reporting related BLL
    """
# AVERAGE DATA FOR GIVEN DATE PERIOD
    def ubre_get_avg_data_for_two_dates(self, no_of_devices, date1, date2, all_group, all_host):
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
            if all_host == "" and all_group == "":
                while (d1 <= d2):
                    date_temp = str(d1)[:10]
                    query = "Select date(go16.timestamp),hosts.host_name ,hosts.ip_address, AVG(go16.rxPhyError) , AVG(go16.rxCrcErrors),hostgroups.hostgroup_name\
                           from odu100_raTddMacStatisticsTable  as go16\
                           join ( select host_id,host_name,ip_address,mac_address,host_alias from hosts where device_type_id like 'ODU100%%' group by host_id) as hosts\
                           INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                           INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                           where go16.host_id=hosts.host_id and go16.timestamp between '%s 00:00:00' and '%s 23:59:59' and go16.rxPhyError<>123456789 and go16.rxPhyError<>987654321 \
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
                    query = "Select date(go16.timestamp),hosts.host_name,hosts.ip_address,AVG(go16.rxPhyError) , AVG(go16.rxCrcErrors),hostgroups.hostgroup_name\
                           from odu100_raTddMacStatisticsTable  as go16\
                           join ( select host_id,host_name,ip_address,mac_address,host_alias from hosts where device_type_id like 'ODU100%%' group by host_id) as hosts\
                           INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                           INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                           where go16.host_id=hosts.host_id and go16.timestamp between '%s 00:00:00' and '%s 23:59:59' and go16.rxPhyError<>123456789 and go16.rxPhyError<>987654321\
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

        # TOTAL crc phy DATA FOR A GIVEN DATE PERIOD

    def ubre_get_total_data_for_two_dates(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
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
            date_temp_1 = str(d1)
            date_temp_2 = str(d2)
            if all_group == '' and all_host == '':
                query = "Select go16.timestamp,hst.host_name,hst.ip_address,go16.rxPhyError, go16.rxCrcErrors,hostgroups.hostgroup_name from odu100_raTddMacStatisticsTable  as go16\
                        join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU100%%' group by host_id limit %s) as hst\
                        on go16.host_id=hst.host_id\
                       INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id\
                       INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                        where go16.timestamp between '%s' and '%s' \
                       order by go16.timestamp asc  " % (no_of_devices, date_temp_1, date_temp_2)
                cursor.execute(query)
                res = cursor.fetchall()
                li = []
                tr = []
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
                    elif i == 0:
                        li.insert(5, "0")
                        li.insert(6, "0")
                    else:
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
                query = "Select go16.timestamp,hst.host_name,hst.ip_address,go16.rxPhyError, go16.rxCrcErrors,hostgroups.hostgroup_name from odu100_raTddMacStatisticsTable  as go16 \
                    join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU100%%' group by host_id) as hst on go16.host_id=hst.host_id \
                    INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id \
                    INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                    where go16.timestamp between '%s' and '%s' AND hst.host_id IN %s order by go16.timestamp asc " % (
                date_temp_1, date_temp_2, host_data)
                cursor.execute(query)
                res = cursor.fetchall()
                li = []
                tr = []
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
                    elif i == 0:
                        li.insert(5, "0")
                        li.insert(6, "0")
                    else:
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

    def ubre_get_synch_loss_for_two_dates(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
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
            date_temp_1 = str(d1)
            date_temp_2 = str(d2)
            if all_group == '' and all_host == '':
                query = " Select go16.timestamp,hst.host_name,hst.ip_address,hst.host_alias,go16.syncLostCounter,hostgroups.hostgroup_name from odu100_synchStatisticsTable  as go16\
                        join ( select host_id,host_name,ip_address,host_alias from hosts where device_type_id like 'ODU100%%' group by host_id limit %s) as hst\
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
                query = " Select go16.timestamp,hst.host_name,hst.ip_address,hst.host_alias,go16.syncLostCounter,hostgroups.hostgroup_name from odu100_synchStatisticsTable  as go16\
                        join ( select host_id,host_name,ip_address,host_alias from hosts where device_type_id like 'ODU100%%' group by host_id limit %s) as hst\
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

        # TOTAL DATA FOR A GIVEN DATE PERIOD FOR NETWORK USAGE

    def ubre_get_total_data_network_usage(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
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
                query = "SELECT  go16.nwStatsIndex,go16.timestamp,hosts.host_name,hosts.ip_address,go16.rxBytes,go16.txBytes,hostgroups.hostgroup_name FROM odu100_nwInterfaceStatisticsTable AS 				go16 JOIN (SELECT host_id, host_name,ip_address FROM hosts WHERE device_type_id LIKE 'ODU100%%' GROUP BY host_id limit %s) AS hosts INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id WHERE go16.host_id = hosts.host_id and go16.timestamp between '%s' and '%s' order by go16.timestamp asc , go16.nwStatsIndex asc" % (
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
                    j = i + 2
                    if j > len(res):
                        break
                    while i < j:
                        if (i < 2):
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
                            elif str(res[i - 2][4]) == "123456789" or str(res[i - 2][4] == "987654321"):
                                temp1 = float(res[i][4])
                                temp2 = float(res[i][5])
                            else:
                                var1 = float(res[i][4])
                                var2 = float(res[i - 2][4])
                                temp1 = var1 - var2
                                var3 = float(res[i][5])
                                var4 = float(res[i - 2][5])
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
                query = "SELECT  go16.nwStatsIndex,go16.timestamp,hosts.host_name,hosts.ip_address,go16.rxBytes,go16.txBytes,hostgroups.hostgroup_name FROM odu100_nwInterfaceStatisticsTable AS 				go16 JOIN (SELECT host_id, host_name,ip_address FROM hosts WHERE device_type_id LIKE 'ODU100%%' GROUP BY host_id) AS hosts  INNER JOIN hosts_hostgroups ON 				hosts_hostgroups.host_id = hosts.host_id  INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id WHERE go16.host_id = hosts.host_id and 				go16.timestamp between '%s' AND '%s' AND hosts.host_id IN %s order by go16.timestamp asc ,hosts.host_name asc, go16.nwStatsIndex asc" % (
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
                    j = i + 2
                    if j > len(res):
                        break
                    while i < j:
                        if (i < 2):
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
                            elif str(res[i - 2][4]) == "123456789" or str(res[i - 2][4] == "987654321"):
                                temp1 = float(res[i][4])
                                temp2 = float(res[i][5])
                            else:
                                var1 = float(res[i][4])
                                var2 = float(res[i - 2][4])
                                temp1 = var1 - var2
                                var3 = float(res[i][5])
                                var4 = float(res[i - 2][5])
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

        # AVERAGE DATA FOR GIVEN DATE PERIOD  FOR RSSI

    def ubre_get_avg_data_for_two_dates_rssi(self, no_of_devices, date1, date2, all_group, all_host):
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
        signal_interface9 = []
        signal_interface10 = []
        signal_interface11 = []
        signal_interface12 = []
        signal_interface13 = []
        signal_interface14 = []
        signal_interface15 = []
        signal_interface16 = []
        time_stamp_signal1 = []
        default_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            date1 = date1.replace("/", "-")
            date2 = date2.replace("/", "-")
            d1 = datetime.strptime(date1, "%d-%m-%Y")
            d2 = datetime.strptime(date2, "%d-%m-%Y")
            average_list = []
            if all_group == '' and all_host == '':
                while (d1 <= d2):
                    flag = 0
                    date_temp = str(d1)[:10]
                    query = "Select date(go16.timestamp), hosts.host_name , hosts.ip_address , AVG(go16.sigStrength1), go16.timeSlotIndex,hostgroups.hostgroup_name,go16.ssIdentifier \
			from odu100_peerNodeStatusTable AS go16\
			join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU100%%' group by host_id limit %s ) as hosts\
			INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
			INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
			where go16.host_id=hosts.host_id and go16.timestamp between '%s 00:00:00' and '%s 23:59:59' and go16.sigStrength1<>'-110' and go16.sigStrength1<>'-111' \
			group by go16.host_id,go16.timeSlotIndex " % (no_of_devices, date_temp, date_temp)
                    cursor.execute(query)
                    signal_strength = cursor.fetchall()
                    d1 = d1 + timedelta(days=1)
                    i = 0
                    for k in range(0, len(signal_strength) - 1):
                        i = k
                        flag = 1
                        if signal_strength[k][6] == '-1' or str(signal_strength[k][4]).strip() == '' or str(
                                signal_strength[k][3]).strip() == '':
                            pass
                        #		                    grp_name.append(signal_strength[k][5])
                        #		                    host_name.append(signal_strength[k][1])
                        #		                    ip_address.append(signal_strength[k][2])
                        #				    signal_interface1.append(0)
                        #				    signal_interface2.append(0)
                        #				    signal_interface3.append(0)
                        #				    signal_interface4.append(0)
                        #				    signal_interface5.append(0)
                        #				    signal_interface6.append(0)
                        #				    signal_interface7.append(0)
                        #				    signal_interface8.append(0)
                        #				    signal_interface9.append(0)
                        #				    signal_interface10.append(0)
                        #				    signal_interface11.append(0)
                        #				    signal_interface12.append(0)
                        #				    signal_interface13.append(0)
                        #				    signal_interface14.append(0)
                        #				    signal_interface15.append(0)
                        #				    signal_interface16.append(0)
                        # time_stamp_signal1.append(str((signal_strength[k][0]).strftime('%d-%m-%Y
                        # %H:%M')))
                        else:
                            # index=1 if signal_strength[k][4]=='' else
                            # int(signal_strength[k][4])
                            if signal_strength[k][0] == signal_strength[k + 1][0]:
                                default_list[int(
                                    signal_strength[k][4]) - 1] = int(signal_strength[k][3])
                            else:
                                default_list[int(
                                    signal_strength[k][4]) - 1] = int(signal_strength[k][3])
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
                                signal_interface9.append(default_list[8])
                                signal_interface10.append(default_list[9])
                                signal_interface11.append(default_list[10])
                                signal_interface12.append(default_list[11])
                                signal_interface13.append(default_list[12])
                                signal_interface14.append(default_list[13])
                                signal_interface15.append(default_list[14])
                                signal_interface16.append(default_list[15])
                                time_stamp_signal1.append(str(
                                    (signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                                default_list = [
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    if len(signal_strength) > 0 and flag == 0:
                        index = 1 if signal_strength[0][
                                         4] == '' else int(signal_strength[0][4])
                        default_list[int(index) -
                                     1] = int(signal_strength[0][3])
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
                        signal_interface9.append(default_list[8])
                        signal_interface10.append(default_list[9])
                        signal_interface11.append(default_list[10])
                        signal_interface12.append(default_list[11])
                        signal_interface13.append(default_list[12])
                        signal_interface14.append(default_list[13])
                        signal_interface15.append(default_list[14])
                        signal_interface16.append(default_list[15])
                        time_stamp_signal1.append(
                            str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    if len(signal_strength) > 0 and flag == 1:
                        index = 1 if signal_strength[i + 1][
                                         4] == '' else int(signal_strength[i + 1][4])
                        default_list[int(index) -
                                     1] = int(signal_strength[0][3])
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
                        signal_interface9.append(default_list[8])
                        signal_interface10.append(default_list[9])
                        signal_interface11.append(default_list[10])
                        signal_interface12.append(default_list[11])
                        signal_interface13.append(default_list[12])
                        signal_interface14.append(default_list[13])
                        signal_interface15.append(default_list[14])
                        signal_interface16.append(default_list[15])
                        time_stamp_signal1.append(
                            str((signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                for k in range(0, len(time_stamp_signal1)):
                    average_list.append(
                        [time_stamp_signal1[k], host_name[k], ip_address[k], signal_interface1[k], signal_interface2[k],
                         signal_interface3[k], signal_interface4[k], signal_interface5[k], signal_interface6[k],
                         signal_interface7[k], signal_interface8[k], signal_interface9[k], signal_interface10[k],
                         signal_interface11[k], signal_interface12[k], signal_interface13[k], signal_interface14[k],
                         signal_interface15[k], signal_interface16[k], grp_name[k]])
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                while (d1 <= d2):
                    flag = 0
                    date_temp = str(d1)[:10]
                    query = "Select date(go16.timestamp), hosts.host_name , hosts.ip_address , AVG(go16.sigStrength1), go16.timeSlotIndex,hostgroups.hostgroup_name,go16.ssIdentifier \
        			       from odu100_peerNodeStatusTable AS go16\
        			       join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU100%%' group by host_id ) as hosts\
        		               INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
        		               INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
        			       where go16.host_id=hosts.host_id and go16.timestamp between '%s 00:00:00' and '%s 23:59:59' and go16.sigStrength1<>'-110' and go16.sigStrength1<>'-111' \
        			       AND hosts.host_id IN %s group by go16.host_id,go16.timeSlotIndex " % (
                    date_temp, date_temp, host_data)
                    cursor.execute(query)
                    signal_strength = cursor.fetchall()
                    d1 = d1 + timedelta(days=1)
                    for k in range(0, len(signal_strength) - 1):
                        i = k
                        flag = 1
                        if signal_strength[k][6] == '-1' or str(signal_strength[k][4]).strip() == '' or str(
                                signal_strength[k][3]).strip() == '':
                            pass
                            #		                    grp_name.append(signal_strength[k][5])
                            #		                    host_name.append(signal_strength[k][1])
                            #		                    ip_address.append(signal_strength[k][2])
                            #				    signal_interface1.append(0)
                            #				    signal_interface2.append(0)
                            #				    signal_interface3.append(0)
                            #				    signal_interface4.append(0)
                            #				    signal_interface5.append(0)
                            #				    signal_interface6.append(0)
                            #				    signal_interface7.append(0)
                            #				    signal_interface8.append(0)
                            #				    signal_interface9.append(0)
                            #				    signal_interface10.append(0)
                            #				    signal_interface11.append(0)
                            #				    signal_interface12.append(0)
                            #				    signal_interface13.append(0)
                            #				    signal_interface14.append(0)
                            #				    signal_interface15.append(0)
                            #				    signal_interface16.append(0)
                            #		                    time_stamp_signal1.append(str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                            #		                else:
                            #		                    #index=1 if signal_strength[k][4]=='' else int(signal_strength[k][4])
                            if signal_strength[k][0] == signal_strength[k + 1][0]:
                                default_list[int(
                                    signal_strength[k][4]) - 1] = int(signal_strength[k][3])
                            else:
                                default_list[int(
                                    signal_strength[k][4]) - 1] = int(signal_strength[k][3])
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
                                signal_interface9.append(default_list[8])
                                signal_interface10.append(default_list[9])
                                signal_interface11.append(default_list[10])
                                signal_interface12.append(default_list[11])
                                signal_interface13.append(default_list[12])
                                signal_interface14.append(default_list[13])
                                signal_interface15.append(default_list[14])
                                signal_interface16.append(default_list[15])
                                time_stamp_signal1.append(str(
                                    (signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                                default_list = [
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    if len(signal_strength) > 0 and flag == 0:
                        if signal_strength[k][6] == '-1' and str(signal_strength[k][4]).strip() == '' and str(
                                signal_strength[k][3]).strip() == '':
                            index = 1 if signal_strength[0][
                                             4] == '' else int(signal_strength[0][4])
                            default_list[int(
                                index) - 1] = int(signal_strength[0][3])
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
                            signal_interface9.append(default_list[8])
                            signal_interface10.append(default_list[9])
                            signal_interface11.append(default_list[10])
                            signal_interface12.append(default_list[11])
                            signal_interface13.append(default_list[12])
                            signal_interface14.append(default_list[13])
                            signal_interface15.append(default_list[14])
                            signal_interface16.append(default_list[15])
                            time_stamp_signal1.append(
                                str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    if len(signal_strength) > 0 and flag == 1:
                        if signal_strength[k][6] == '-1' and str(signal_strength[k][4]).strip() == '' and str(
                                signal_strength[k][3]).strip() == '':
                            index = 1 if signal_strength[i + 1][
                                             4] == '' else int(signal_strength[i + 1][4])
                            default_list[int(
                                index) - 1] = int(signal_strength[0][3])
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
                            signal_interface9.append(default_list[8])
                            signal_interface10.append(default_list[9])
                            signal_interface11.append(default_list[10])
                            signal_interface12.append(default_list[11])
                            signal_interface13.append(default_list[12])
                            signal_interface14.append(default_list[13])
                            signal_interface15.append(default_list[14])
                            signal_interface16.append(default_list[15])
                            time_stamp_signal1.append(str(
                                (signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for k in range(0, len(time_stamp_signal1)):
                    average_list.append(
                        [time_stamp_signal1[k], host_name[k], ip_address[k], signal_interface1[k], signal_interface2[k],
                         signal_interface3[k], signal_interface4[k], signal_interface5[k], signal_interface6[k],
                         signal_interface7[k], signal_interface8[k], signal_interface9[k], signal_interface10[k],
                         signal_interface11[k], signal_interface12[k], signal_interface13[k], signal_interface14[k],
                         signal_interface15[k], signal_interface16[k], grp_name[k]])

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

    def ubre_get_total_data_for_two_dates_rssi(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
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
        signal_interface9 = []
        signal_interface10 = []
        signal_interface11 = []
        signal_interface12 = []
        signal_interface13 = []
        signal_interface14 = []
        signal_interface15 = []
        signal_interface16 = []
        time_stamp_signal1 = []
        default_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
            date_temp_1 = str(d1)
            date_temp_2 = str(d2)
            if all_group == '' and all_host == '':
                query = "Select go16.timestamp , hst.host_name , hst.ip_address , go16.sigStrength1, go16.timeSlotIndex,hostgroups.hostgroup_name,go16.ssIdentifier from odu100_peerNodeStatusTable  as go16\
                    join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU100%%' group by host_id limit %s) as hst ON go16.host_id=hst.host_id\
                    INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id\
                    INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                    where go16.timestamp between '%s' and '%s'\
                    order by go16.timestamp asc,hst.host_name asc,go16.timeSlotIndex asc" % (
                no_of_devices, date_temp_1, date_temp_2)
                flag = 1
                cursor.execute(query)
                signal_strength = cursor.fetchall()
                i = 0
                for k in range(0, len(signal_strength) - 1):
                    i = k
                    flag = 1
                    if str(signal_strength[k][3]).strip() == '-110':
                    #    pass
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
                        signal_interface9.append("DEVICE WAS OFF")
                        signal_interface10.append("DEVICE WAS OFF")
                        signal_interface11.append("DEVICE WAS OFF")
                        signal_interface12.append("DEVICE WAS OFF")
                        signal_interface13.append("DEVICE WAS OFF")
                        signal_interface14.append("DEVICE WAS OFF")
                        signal_interface15.append("DEVICE WAS OFF")
                        signal_interface16.append("DEVICE WAS OFF")
                        time_stamp_signal1.append(
                            str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                    elif str(signal_strength[k][3]).strip() == '-111':
                    #    pass
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
                        signal_interface9.append("DEVICE WAS DISABLED")
                        signal_interface10.append("DEVICE WAS DISABLED")
                        signal_interface11.append("DEVICE WAS DISABLED")
                        signal_interface12.append("DEVICE WAS DISABLED")
                        signal_interface13.append("DEVICE WAS DISABLED")
                        signal_interface14.append("DEVICE WAS DISABLED")
                        signal_interface15.append("DEVICE WAS DISABLED")
                        signal_interface16.append("DEVICE WAS DISABLED")
                        time_stamp_signal1.append(
                            str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                    else:
                        # index=1 if signal_strength[k][4]=='' else
                        # int(signal_strength[k][4])
                        if signal_strength[k][0] == signal_strength[k + 1][0]:
                            default_list[int(signal_strength[
                                k][4]) - 1] = int(signal_strength[k][3])
                        else:
                            default_list[int(signal_strength[
                                k][4]) - 1] = int(signal_strength[k][3])
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
                            signal_interface9.append(default_list[8])
                            signal_interface10.append(default_list[9])
                            signal_interface11.append(default_list[10])
                            signal_interface12.append(default_list[11])
                            signal_interface13.append(default_list[12])
                            signal_interface14.append(default_list[13])
                            signal_interface15.append(default_list[14])
                            signal_interface16.append(default_list[15])
                            time_stamp_signal1.append(
                                str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                if len(signal_strength) > 0 and flag == 0:
                    if signal_strength[k][6] == '-1' and str(signal_strength[k][4]).strip() == '' and str(
                            signal_strength[k][3]).strip() == '':
                        index = 1 if signal_strength[0][
                                         4] == '' else int(signal_strength[0][4])
                        default_list[int(index) -
                                     1] = int(signal_strength[0][3])
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
                        signal_interface9.append(default_list[8])
                        signal_interface10.append(default_list[9])
                        signal_interface11.append(default_list[10])
                        signal_interface12.append(default_list[11])
                        signal_interface13.append(default_list[12])
                        signal_interface14.append(default_list[13])
                        signal_interface15.append(default_list[14])
                        signal_interface16.append(default_list[15])
                        time_stamp_signal1.append(
                            str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                if len(signal_strength) > 0 and flag == 1:
                    if signal_strength[k][6] == '-1' and str(signal_strength[k][4]).strip() == '' and str(
                            signal_strength[k][3]).strip() == '':
                        index = 1 if signal_strength[i + 1][
                                         4] == '' else int(signal_strength[i + 1][4])
                        default_list[int(index) -
                                     1] = int(signal_strength[0][3])
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
                        signal_interface9.append(default_list[8])
                        signal_interface10.append(default_list[9])
                        signal_interface11.append(default_list[10])
                        signal_interface12.append(default_list[11])
                        signal_interface13.append(default_list[12])
                        signal_interface14.append(default_list[13])
                        signal_interface15.append(default_list[14])
                        signal_interface16.append(default_list[15])
                        time_stamp_signal1.append(
                            str((signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                        # make the RSSI 2'd list
                for k in range(0, len(time_stamp_signal1)):
                    total_list.append(
                        [time_stamp_signal1[k], host_name[k], ip_address[k], signal_interface1[k], signal_interface2[k],
                         signal_interface3[k], signal_interface4[k], signal_interface5[k], signal_interface6[k],
                         signal_interface7[k], signal_interface8[k], signal_interface9[k], signal_interface10[k],
                         signal_interface11[k], signal_interface12[k], signal_interface13[k], signal_interface14[k],
                         signal_interface15[k], signal_interface16[k], grp_name[k]])
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query = "Select go16.timestamp , hst.host_name , hst.ip_address , go16.sigStrength1, go16.timeSlotIndex,hostgroups.hostgroup_name,go16.ssIdentifier from odu100_peerNodeStatusTable  as go16\
                join ( select host_id,host_name,ip_address from hosts where device_type_id like 'ODU100%%' group by host_id) as hst ON go16.host_id=hst.host_id\
                INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hst.host_id\
                INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                where go16.timestamp between '%s' and '%s' AND hst.host_id IN %s order by go16.timestamp asc ,hst.host_name asc, go16.timeSlotIndex asc" % (
                date_temp_1, date_temp_2, host_data)
                cursor.execute(query)
                signal_strength = cursor.fetchall()
                flag = 0
                i = 0
                for k in range(0, len(signal_strength) - 1):
                    i = k
                    flag = 1
                    if str(signal_strength[k][3]).strip() == '-110':
                    #    pass
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
                        signal_interface9.append("DEVICE WAS OFF")
                        signal_interface10.append("DEVICE WAS OFF")
                        signal_interface11.append("DEVICE WAS OFF")
                        signal_interface12.append("DEVICE WAS OFF")
                        signal_interface13.append("DEVICE WAS OFF")
                        signal_interface14.append("DEVICE WAS OFF")
                        signal_interface15.append("DEVICE WAS OFF")
                        signal_interface16.append("DEVICE WAS OFF")
                        time_stamp_signal1.append(
                            str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                    elif str(signal_strength[k][3]).strip() == '-111':
                    #    pass
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
                        signal_interface9.append("DEVICE WAS DISABLED")
                        signal_interface10.append("DEVICE WAS DISABLED")
                        signal_interface11.append("DEVICE WAS DISABLED")
                        signal_interface12.append("DEVICE WAS DISABLED")
                        signal_interface13.append("DEVICE WAS DISABLED")
                        signal_interface14.append("DEVICE WAS DISABLED")
                        signal_interface15.append("DEVICE WAS DISABLED")
                        signal_interface16.append("DEVICE WAS DISABLED")
                        time_stamp_signal1.append(
                            str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                    else:
                        # index=1 if signal_strength[k][4]=='' else
                        # int(signal_strength[k][4])
                        if signal_strength[k][0] == signal_strength[k + 1][0]:
                            default_list[int(signal_strength[
                                k][4]) - 1] = int(signal_strength[k][3])
                        else:
                            default_list[int(signal_strength[
                                k][4]) - 1] = int(signal_strength[k][3])
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
                            signal_interface9.append(default_list[8])
                            signal_interface10.append(default_list[9])
                            signal_interface11.append(default_list[10])
                            signal_interface12.append(default_list[11])
                            signal_interface13.append(default_list[12])
                            signal_interface14.append(default_list[13])
                            signal_interface15.append(default_list[14])
                            signal_interface16.append(default_list[15])
                            time_stamp_signal1.append(
                                str((signal_strength[k][0]).strftime('%d-%m-%Y %H:%M')))
                            default_list = [0,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                if len(signal_strength) > 0 and flag == 0:
                    if signal_strength[k][6] == '-1' and str(signal_strength[k][4]).strip() == '' and str(
                            signal_strength[k][3]).strip() == '':
                        index = 1 if signal_strength[0][
                                         4] == '' else int(signal_strength[0][4])
                        default_list[int(index) -
                                     1] = int(signal_strength[0][3])
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
                        signal_interface9.append(default_list[8])
                        signal_interface10.append(default_list[9])
                        signal_interface11.append(default_list[10])
                        signal_interface12.append(default_list[11])
                        signal_interface13.append(default_list[12])
                        signal_interface14.append(default_list[13])
                        signal_interface15.append(default_list[14])
                        signal_interface16.append(default_list[15])
                        time_stamp_signal1.append(
                            str((signal_strength[0][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                if len(signal_strength) > 0 and flag == 1:
                    if signal_strength[k][6] == '-1' and str(signal_strength[k][4]).strip() == '' and str(
                            signal_strength[k][3]).strip() == '':
                        index = 1 if signal_strength[i + 1][
                                         4] == '' else int(signal_strength[i + 1][4])
                        default_list[int(index) -
                                     1] = int(signal_strength[0][3])
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
                        signal_interface9.append(default_list[8])
                        signal_interface10.append(default_list[9])
                        signal_interface11.append(default_list[10])
                        signal_interface12.append(default_list[11])
                        signal_interface13.append(default_list[12])
                        signal_interface14.append(default_list[13])
                        signal_interface15.append(default_list[14])
                        signal_interface16.append(default_list[15])
                        time_stamp_signal1.append(
                            str((signal_strength[i + 1][0]).strftime('%d-%m-%Y %H:%M')))
                        default_list = [0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for k in range(0, len(time_stamp_signal1)):
                    total_list.append(
                        [time_stamp_signal1[k], host_name[k], ip_address[k], signal_interface1[k], signal_interface2[k],
                         signal_interface3[k], signal_interface4[k], signal_interface5[k], signal_interface6[k],
                         signal_interface7[k], signal_interface8[k], signal_interface9[k], signal_interface10[k],
                         signal_interface11[k], signal_interface12[k], signal_interface13[k], signal_interface14[k],
                         signal_interface15[k], signal_interface16[k], grp_name[k]])
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

    # reporting create fucntionaltiy started from here.
    def ubre_crc_excel_creating(self, crc_avg, crc_total):
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
            # check the data exists or not
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

    def ubre_nw_bandwith_excel_creating(self, nw_total):
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
            nw_total = sorted(nw_total, key=itemgetter(7))
            for k in range(len(nw_total) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet('%s(Bandwith_data),' % (
                        nw_total[k][7]), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 8, "Bandwith Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 8, "%s(Group Name)" % (nw_total[k][7]), style)
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
                                'Eth0(Rx)', 'Eth0(Tx)', 'Eth1(Rx)', 'Eth1(Tx)']

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)

                if nw_total[k][7] == nw_total[k + 1][7]:
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
                if nw_total[len(nw_total) - 1][7] == nw_total[len(nw_total) - 2][7]:
                    for j in range(len(nw_total[len(nw_total) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, nw_total[len(nw_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(nw_total) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Bandwith_data),' % (
                    nw_total[0][7]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 3, "Bandwith Information", style)
                xls_sheet.write_merge(
                    1, 1, 0, 3, "%s(Group Name)" % (nw_total[0][7]), style)
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
                            'Eth0(Rx)', 'Eth0(Tx)', 'Eth1(Rx)', 'Eth1(Tx)']

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

    def ubre_rssi_excel_creating(self, rssi_avg, rssi_total):
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
            rssi_avg = sorted(rssi_avg, key=itemgetter(19))
            for k in range(len(rssi_avg) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet('%s(Aerage_rssi),' % (
                        rssi_avg[k][19]), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 18, "Average RSSI Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 18, "%s(Group Name)" % (rssi_avg[k][19]), style)
                    xls_sheet.write_merge(2, 2, 0, 18, "")
                    i = 4
                    # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                    # horiz center,color grey25')
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = [
                        'Data', 'Hostname', 'IP Address', 'Peer1', 'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7',
                        'Peer8', 'Peer9',
                        'Peer10', 'Peer11', 'Peer12', 'Peer13', 'Peer14', 'Peer15', 'Peer16']

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)

                if rssi_avg[k][19] == rssi_avg[k + 1][19]:
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
                if rssi_avg[len(rssi_avg) - 1][19] == rssi_avg[len(rssi_avg) - 2][19]:
                    for j in range(len(rssi_avg[len(rssi_avg) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, rssi_avg[len(rssi_avg) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(rssi_avg) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Average_rssi),' % (
                    rssi_avg[0][19]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 18, "Average RSSI Information", style)
                xls_sheet.write_merge(
                    1, 1, 0, 18, "%s(Group Name)" % (rssi_avg[0][19]), style)
                xls_sheet.write_merge(2, 2, 0, 18, "")
                i = 4
                # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                # horiz center,color grey25')
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = [
                    'Data', 'Hostname', 'IP Address', 'Peer1', 'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7',
                    'Peer8', 'Peer9',
                    'Peer10', 'Peer11', 'Peer12', 'Peer13', 'Peer14', 'Peer15', 'Peer16']

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
            rssi_total = sorted(rssi_total, key=itemgetter(19))
            for k in range(len(rssi_total) - 1):
                if flag == 0:
                    i = 0
                    xls_sheet = xls_book.add_sheet('%s(Total_rssi),' % (
                        rssi_total[k][19]), cell_overwrite_ok=True)
                    xls_sheet.row(0).height = 521
                    xls_sheet.row(1).height = 421
                    xls_sheet.write_merge(
                        0, 0, 0, 18, "Total RSSI Information", style)
                    xls_sheet.write_merge(
                        1, 1, 0, 18, "%s(Group Name)" % (rssi_total[k][19]), style)
                    xls_sheet.write_merge(2, 2, 0, 18, "")
                    i = 4
                    # heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre,
                    # horiz center,color grey25')
                    heading_xf = xlwt.easyxf(
                        'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                    headings = [
                        'Data', 'Hostname', 'IP Address', 'Peer1', 'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7',
                        'Peer8', 'Peer9',
                        'Peer10', 'Peer11', 'Peer12', 'Peer13', 'Peer14', 'Peer15', 'Peer16']

                    xls_sheet.set_panes_frozen(
                        True)  # frozen headings instead of split panes
                    xls_sheet.set_horz_split_pos(
                        i)  # in general, freeze after last heading row
                    xls_sheet.set_remove_splits(
                        True)  # if user does unfreeze, don't leave a split there
                    for colx, value in enumerate(headings):
                        xls_sheet.write(i - 1, colx, value, heading_xf)

                if rssi_total[k][19] == rssi_total[k + 1][19]:
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
                if rssi_total[len(rssi_total) - 1][19] == rssi_total[len(rssi_total) - 2][19]:
                    for j in range(len(rssi_total[len(rssi_total) - 1]) - 1):
                        width = 5000
                        xls_sheet.write(
                            i, j, rssi_total[len(rssi_total) - 1][j], style1)
                        xls_sheet.col(j).width = width
            elif len(rssi_total) > 0:
                i = 0
                xls_sheet = xls_book.add_sheet('%s(Total_rssi),' % (
                    rssi_total[0][19]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 18, "Total RSSI Information", style)
                xls_sheet.write_merge(1, 1, 0, 18,
                                      "%s(Group Name)" % (rssi_total[0][19]), style)
                xls_sheet.write_merge(2, 2, 0, 18, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = [
                    'Data', 'Hostname', 'IP Address', 'Peer1', 'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7',
                    'Peer8', 'Peer9',
                    'Peer10', 'Peer11', 'Peer12', 'Peer13', 'Peer14', 'Peer15', 'Peer16']
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

    def ubre_group_data(self, search_text):
        """

        @param search_text:
        @return:
        """
        try:
            output_list = []
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sel_query = "SELECT hostgroups.hostgroup_id, hostgroups.hostgroup_name FROM hosts\
                        INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                        INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                        WHERE hostgroups.hostgroup_name LIKE '%%%s%%' AND hosts.device_type_id='ODU100'" % (search_text)
            cursor.execute(sel_query)
            group_result = cursor.fetchall()
            # close the cursor and database connection
            return group_result, 0
        except Exception, e:
            return e, 1
        finally:
            cursor.close()
            conn.close()

    def ubre_host_data(self, search_text):
        """

        @param search_text:
        @return:
        """
        try:
            host_result = ''
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            if (cursor.execute("SELECT hosts.host_id, hosts.ip_address,hosts.host_alias,hosts.mac_address FROM hosts\
                                INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                                INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
                                WHERE hostgroups.hostgroup_id LIKE '%s' AND hosts.device_type_id like 'ODU100%%' " % (
            search_text))):
                host_result = cursor.fetchall()
            if len(host_result) == 0:
                cursor.execute("SELECT hosts.host_id, hosts.ip_address,hosts.host_alias,hosts.mac_address FROM hosts\
	                                INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
	                                INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id\
	                                WHERE (hosts.mac_address LIKE '%%%s%%' OR hosts.ip_address LIKE '%%%s%%' OR hosts.host_alias LIKE '%%%s%%'\
	                                OR hostgroups.hostgroup_id LIKE '%s') AND hosts.device_type_id like 'ODU100%%'" % (
                search_text, search_text, search_text, search_text))
                host_result = cursor.fetchall()
            return host_result, 0
            # close the cursor and database connection
        except Exception, e:
            return e, 1
        finally:
            cursor.close()
            conn.close()
