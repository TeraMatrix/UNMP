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
from copy import deepcopy
from datetime import datetime

import MySQLdb
from unmp_config import SystemConfig
from common_vars import make_list


class APReportBll(object):
    """
    AP reports related model
    """
# TOTAL DATA FOR TX RX
    def ap_get_statistics_data(self, no_of_devices, date1, date2, time1, time2, all_group, all_host):
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
                query = "SELECT ap.timestamp,hst.host_name,hst.host_alias,hst.ip_address,ap.index,ap.statisticsInterface,ap.statisticsRxPackets,ap.statisticsTxPackets \
					FROM ap25_statisticsTable as ap \
					join (select host_name,host_id,host_alias,ip_address from hosts limit %s) as hst on hst.host_id=ap.host_id  \
					where ap.timestamp between '%s' and '%s' \
					order by hst.host_name,ap.timestamp,ap.index" % (no_of_devices, date_temp_1, date_temp_2)
            else:
                host_data = str(
                    all_host.split(',')).replace('[', '(').replace(']', ')')
                query = "SELECT ap.timestamp,hst.host_name,hst.host_alias,hst.ip_address,ap.index,ap.statisticsInterface,ap.statisticsRxPackets,ap.statisticsTxPackets \
					FROM ap25_statisticsTable as ap \
					join (select host_name,host_id,host_alias,ip_address from hosts limit %s) as hst on hst.host_id=ap.host_id  \
					where ap.timestamp between '%s' and '%s' \
					AND hst.host_id IN %s order by hst.host_name,ap.timestamp,ap.index " % (
                no_of_devices, date_temp_1, date_temp_2, host_data)
            cursor.execute(query)
            res = cursor.fetchall()
            if (len(res) == 0):
                result_dict = {"success": 0, "result": []}
                return result_dict
            tr = []
            li = []
            values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0]
            host = res[0][1]
            for i in range(len(res) - 1):
                li = make_list(res[i])
                if host == res[i + 1][1]:
                    if (str(res[i][0])[:16] == str(res[i + 1][0])[:16]):
                        values[int(res[i][4])] = str(res[i][6])
                        values[2 * int(res[i][4]) + 1] = str(res[i][7])
                    else:
                        temp = li[:4] + values
                        tr.append(temp)
                        values = [0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                else:
                    temp = li[:4] + values
                    tr.append(temp)
                    values = [0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                host = res[i][1]
            li = []
            ltr = []
            result = tr
            for i in range(len(result)):
                li = deepcopy(result[i])
                if (i == 0):
                    for j in range(4, 24):
                        li[j] = '0'
                elif (result[i][1] == result[i - 1][1]):
                    for j in range(4, 24):
                        tmp = int(result[i][j]) - int(result[i - 1][j])
                        if tmp < 0:
                            tmp = 0
                        li[j] = str(tmp)
                ltr.append(li)
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = ltr
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()
