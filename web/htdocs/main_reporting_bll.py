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

from copy import deepcopy
import csv
from datetime import timedelta, datetime  # ,date
from operator import itemgetter
import shelve

import MySQLdb
import xlwt

from common_bll import EventLog
from common_controller import logme
from common_vars import make_list
from config_report import get_configuration_details
from unmp_config import SystemConfig


class MainReportBll(object):
    """
    Main reporting related BLL class
    """
    # get sql data using query dict
    def get_sql_data(self, query_dict, date_temp_1, date_temp_2):
        """

        @param query_dict:
        @param date_temp_1:
        @param date_temp_2:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            # date1,2 not using right now
            # but could be useful
            # date1 = datetime.strptime(date_temp_1, "%Y-%m-%d %H:%M:%S")
            # date2 = datetime.strptime(date_temp_2, "%Y-%m-%d %H:%M:%S")
            # nw = datetime.now()
            sql = "( select %s from %s %s %s %s %s )" % (
            query_dict["columns"], query_dict["table_name"], query_dict["join"], query_dict[
                "where"], query_dict["group_by"], query_dict["order_by"])
            cursor.execute(sql)
            li_result = []
            for row in cursor.fetchall():
                li_result.append(make_list(row))
            result_dict = {"success": "0", "result": li_result}
            db.close()
            return result_dict
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

    # get selected columns and non selected columns from report template
    def main_reporting_get_column_template(self, device_type_id, report_type):
        """

        @param device_type_id:
        @param report_type:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select column_selected,column_non_selected from report_template where device_type='%s' and report_type='%s'" % (
                device_type_id, report_type)
            cursor.execute(sql)
            result = cursor.fetchall()
            lis = []
            lis.append(result[0][0])
            lis.append(result[0][1])
            db.close()
            result_dict = {"success": "0", "result": lis}
            return result_dict
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

    # get all data from report template for given device type and report type
    def main_reporting_get_mapping_column(self, device_type_id, report_type):
        """

        @param device_type_id:
        @param report_type:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select column_selected,column_non_selected,mapping_selected,mapping_non_selected, \
                  sheet_name,main_title,second_title,report_name,generate_method from report_template where device_type='%s' and report_type='%s'" % (
            device_type_id, report_type)
            cursor.execute(sql)
            result = cursor.fetchall()
            lis = []
            if len(result) > 0:
                for i in range(len(result[0])):
                    lis.append(result[0][i])
                db.close()
            result_dict = {"success": "0", "result": lis}
            return result_dict
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

    # get a query dict for diven data
    def get_query_dict(self, device_type, report_type, date_temp_1, date_temp_2, all_host):
        """

        @param device_type:
        @param report_type:
        @param date_temp_1:
        @param date_temp_2:
        @param all_host:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select * from report_query_dict where report_type='%s' and device_type='%s'" % (
                report_type, device_type)
            cursor.execute(sql)
            result = cursor.fetchall()
            query_dict = {
                "table_name": result[0][4],
                "columns": result[0][3],
                "join": result[0][5],
                "where": str(result[0][6]) % (date_temp_1, date_temp_2, "' , '".join(all_host.split(','))),
                "group_by": result[0][7],
                "order_by": result[0][8],
                "group_the_data": result[0][9],
                "find_delta": result[0][10],
                "default_data": result[0][11],
                "group_the_data_variables": result[0][12],
                "find_delta_variables": result[0][13],
                "default_data_variables": result[0][14]
            }
            result_dict = {"success": "0", "result": query_dict}
            db.close()
            return result_dict
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

    # get host group name and id with device type and their report type ..this
    # is called initially
    def get_hostgroup_device(self, user_id, hostgroup_id_list):
        """

        @param user_id:
        @param hostgroup_id_list:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "select hg.hostgroup_id,hg.hostgroup_name,dt.device_type_id,dt.device_name from hostgroups as hg \
			join (select hostgroup_id,host_id from hosts_hostgroups)  as hhg on hhg.hostgroup_id=hg.hostgroup_id \
			join (select host_id,device_type_id from hosts) as h on h.host_id=hhg.host_id \
			join (select device_type_id,device_name,is_deleted from device_type) as dt on dt.device_type_id=h.device_type_id \
			where hhg.hostgroup_id IN (%s) and dt.is_deleted<>1 group  by hg.hostgroup_id ,dt.device_type_id order by dt.device_name" % ','.join(
                hostgroup_id_list)
            cursor.execute(query)
            result = cursor.fetchall()
            query2 = "SELECT device_type,report_Type FROM `report_template` order by device_type,report_type"
            cursor.execute(query2)
            tp = cursor.fetchall()
            di = {}
            li = []
            for t in tp:
                if t[0] in di:
                    li = di[t[0]]
                    li.append(t[1])
                    di[t[0]] = li
                else:
                    li = make_list(t)
                    li.pop(0)
                    di[t[0]] = li
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = result
            result_dict["host_data"] = di
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

    # get host data ie device name and host id
    def main_reporting_get_host_data(self, hostgroup_id, device_type_id):
        """

        @param hostgroup_id:
        @param device_type_id:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "select h.host_id,h.host_alias from hosts_hostgroups  as hhg \
			join (select host_id,device_type_id,host_name,host_alias from hosts where is_deleted = 0) as h on h.host_id=hhg.host_id \
			where hhg.hostgroup_id='%s' and h.device_type_id='%s' order by h.host_name" % (hostgroup_id, device_type_id)
            cursor.execute(query)
            result = cursor.fetchall()
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = result
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

    # Function to form Default Data set ie fill values like '0' when values
    # are not present
    def get_and_form_data_default(self, res, host_index, values_length, time_index, key, data_length, values1_index,
                                  values2_index, val1, val2, val3, val4, default_value):
        """

        @param res:
        @param host_index:
        @param values_length:
        @param time_index:
        @param key:
        @param data_length:
        @param values1_index:
        @param values2_index:
        @param val1:
        @param val2:
        @param val3:
        @param val4:
        @param default_value:
        @return:
        """
        try:
            total_list = []
            if (len(res) == 0):
                result_dict = {"success": 0, "result": []}
                return result_dict
            tr = []
            li = []
            values = []
            # fill default values in the list
            for i in range(values_length):
                values.append(default_value)
                # find the first host
            host = res[0][host_index]
            for i in range(len(res)):
                li = make_list(res[i])
                # IF ITS THE LAST RECORD OF THE INPUT
                if (i == len(res) - 1):
                # if host are same
                    if str(res[i][host_index]) == str(res[i - 1][host_index]) and str(res[i][time_index])[:16] == str(
                            res[i - 1][time_index])[:16]:
                        # if time is same till same minute
                        # fill the first value in the value list
                        values[int(res[i][key]) *
                               val1 + val2] = int(res[i][values1_index])
                        # fill the second value in the value list
                        if (int(values2_index) >= 0):
                            values[int(res[i][key])
                                   * val3 + val4] = int(res[i][values2_index])
                        temp = li[:data_length] + values
                        # append this is the tr ie final result
                        tr.append(temp)
                    else:
                        # temp list is equal to host details + values list
                        values[int(res[i][key]) *
                               val1 + val2] = int(res[i][values1_index])
                        # fill the second value in the value list
                        if (int(values2_index) >= 0):
                            values[int(res[i][key])
                                   * val3 + val4] = int(res[i][values2_index])
                        temp = li[:data_length] + values
                        # append this is the tr ie final result
                        tr.append(temp)
                # if host are same
                elif str(res[i][host_index]) == str(res[i + 1][host_index]):
                    # if time is same till same minute
                    if ((str(res[i][time_index])[:16] == str(res[i + 1][time_index])[:16])):
                        # fill the first value in the value list
                        values[int(res[i][key]) *
                               val1 + val2] = int(res[i][values1_index])
                        # fill the second value in the value list
                        if (int(values2_index) >= 0):
                            values[int(res[i][key])
                                   * val3 + val4] = int(res[i][values2_index])
                    else:
                        # temp list is equal to host details + values list
                        values[int(res[i][key]) *
                               val1 + val2] = int(res[i][values1_index])
                        # fill the second value in the value list
                        if (int(values2_index) >= 0):
                            values[int(res[i][key])
                                   * val3 + val4] = int(res[i][values2_index])
                        temp = li[:data_length] + values
                        # append this is the tr ie final result
                        tr.append(temp)
                        # reset values to default
                        values = []
                        for k in range(values_length):
                            values.append(default_value)
                else:
                    # same as above
                    values[int(
                        res[i][key]) * val1 + val2] = int(res[i][values1_index])
                    # fill the second value in the value list
                    if (int(values2_index) >= 0):
                        values[int(res[i][key]) *
                               val3 + val4] = int(res[i][values2_index])
                    temp = li[:data_length] + values
                    tr.append(temp)
                    values = []
                    for k in range(values_length):
                        values.append(default_value)
                        # reset the host
                    host = res[i][host_index]
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = tr
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict

        #   Function to find Delta between Successive Values

    def get_delta_for_values(self, inpt, host_index, data_length, values_length, default_value, is_append, off_value,
                             port_index=-1):
        """

        @param inpt:
        @param host_index:
        @param data_length:
        @param values_length:
        @param default_value:
        @param is_append:
        @param off_value:
        @param port_index:
        @return:
        """
        try:
            li = []
            result_list = []
            flag = 1
            # result=inpt
            # this code is to get differences for consecutive values
            for i in range(len(inpt)):
                flag = 1
                # make a deepcopy of the list
                li = deepcopy(inpt[i])
                # for first value ie i=0
                if (i == 0):
                    # fill with 0 in li
                    for j in range(data_length, data_length + values_length):
                        if is_append == 1:
                            li.append(int(default_value))
                        else:
                            li[j] = int(default_value)
                # else if hosts are same
                else:
                    if port_index != -1 and port_index != 0:
                        if (inpt[i][port_index] == inpt[i - 1][port_index]):
                            flag = 1
                        else:
                            flag = 0
                    else:
                        flag = 1
                    if (inpt[i][host_index] == inpt[i - 1][host_index]) and flag == 1:
                    # fill with difference
                        for j in range(data_length, data_length + values_length):
                            if (str(inpt[i][j]) == str(default_value)):
                                tmp = int(default_value)
                            elif (str(inpt[i][j]) == str(off_value)):
                                tmp = int(off_value)
                            elif (str(inpt[i - 1][j]) == str(default_value) or str(inpt[i - 1][j]) == str(off_value)):
                                tmp = 0
                            else:
                                tmp = int(inpt[i][j]) - int(inpt[i - 1][j])
                                if tmp < 0:
                                    tmp = 0
                            if is_append == 1:
                                li.append(int(tmp))
                            else:
                                li[j] = int(tmp)
                                # append to final result
                    else:
                        for j in range(data_length, data_length + values_length):
                            if is_append == 1:
                                li.append(int(default_value))
                            else:
                                li[j] = int(default_value)
                                # append to final result
                result_list.append(li)
                # return result
            result_dict = {}
            result_dict["success"] = 0
            if port_index != -1:
                result_list = sorted(
                    result_list, key=itemgetter(host_index, 0, port_index))
            result_dict["result"] = result_list
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict

    # Function to form Default Data set like if values contain default data
    # value ie '1111111' then it will be replaced by 'Device Unreachable'
    def form_the_default_data(self, inpt, start_index, end_index, default_value, do_repeat, report_type=""):
        """

        @param inpt:
        @param start_index:
        @param end_index:
        @param default_value:
        @param do_repeat:
        @param report_type:
        @return:
        """
        try:
            li = []
            result_list = []
            # result=inpt
            # this code is to get differences for consecutive values
            for i in range(len(inpt)):
                # make a deepcopy of the list
                li = deepcopy(inpt[i])
                count = 0
                for j in range(start_index, end_index):
                    if (str(li[j]) == str(default_value)):
                        count = count + 1
                    if count == (end_index - start_index) or ((report_type == "RSL" or report_type == "RSSI" or (
                            report_type == 'CRC PHY' and count == 2)) and count != 0):
                        if (do_repeat == 1):
                            for k in range(start_index, end_index):
                                li[k] = "DEVICE WAS UNREACHABLE"
                            break
                        else:
                            li[j] = "DEVICE WAS UNREACHABLE"
                result_list.append(li)
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = result_list
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict

        #   Function to get the description of report generated

    def get_description(self, all_host, report_name):
        """

        @param all_host:
        @param report_name:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "SELECT host_alias FROM hosts WHERE host_id IN ('%s')" % (
                "' , '".join(all_host.split(',')))
            cursor.execute(sql)
            result = cursor.fetchall()
            desc = " report (%s) generated for  " % (report_name)
            len_host = 0
            if result != ():
                for i in result:
                    len_host += 1
                    desc += str(i[0]) + " , "
                    if len_host > 5:
                        desc += " and others ,"
                        break
                desc = desc[:-2]
                return {"success": 0, "result": desc}

            return {"success": 0, "result": "report (%s) generated" % (report_name)}
            # return {"success":0,"result":"Excel report generated "}
        except Exception, e:
            return {"success": 1, "result": str(e)}

    # common and main function for all reports.. It will be called first.
    def main_reporting_get_excel(self, date1, date2, time1, time2, all_host, report_type, column_user, device_type,
                                 all_group, view_type, i_display_start, i_display_length, s_search, sEcho, sSortDir_0,
                                 iSortCol_0, new_user_report_dict, username):
        """

        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_host:
        @param report_type:
        @param column_user:
        @param device_type:
        @param all_group:
        @param view_type:
        @param i_display_start:
        @param i_display_length:
        @param s_search:
        @param sEcho:
        @param sSortDir_0:
        @param iSortCol_0:
        @param new_user_report_dict:
        @param username:
        @return:
        """
        try:
            direct = ""
            dat1 = date1.replace("/", "-")
            dat2 = date2.replace("/", "-")
            different_report = 0
            dat1 = dat1 + " " + time1
            dat2 = dat2 + " " + time2
            d1 = datetime.strptime(dat1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(dat2, "%d-%m-%Y %H:%M")
            date_temp_1 = str(d1)
            date_temp_2 = str(d2)
            aaData = []
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system
            # creating the object
            re = MainReportBll()
            #	   getting values column_selected,column_non_selected,mapping_selected,mapping_non_selected
            # sheet_name,main_title,second_title,report_name,generate_method
            result_columns = re.main_reporting_get_mapping_column(
                device_type, report_type)
            column_value = []
            column_key = []
            key_user = []
            data_report = {}
            data_report["success"] = "0"
            if (result_columns["success"] == 0 or result_columns["success"] == "0"):
                # get columns name for both selected & non selected
                column_value = result_columns["result"][0].split(",")
                if result_columns["result"][1].split(",") != [""]:
                    column_value += result_columns["result"][1].split(",")
                    # get table column  names for both selected &  non selected
                column_key = result_columns["result"][2].split(";")
                if result_columns["result"][3].split(";") != [""]:
                    column_key += result_columns["result"][3].split(";")
                    # column_key+=result_columns["result"][3].split(";")
                # for i in range column in table if user selected the column
                # then add in key_user
                for i in range(len(column_user)):
                    if (column_value.count(column_user[i]) >= 1):
                        index = column_value.index(column_user[i])
                        key_user.append(column_key[index])
                    # we use key_user for generating sql query only
                # but we use column_user for generating report headings
                # here is code for special reports like Device
                # Reachability,Traps,Clients,Configuration.
                if (str(result_columns["result"][8]) == '1'):
                    different_report = 1
                    # generate method for network outage
                    if (report_type.upper() == "DEVICE REACHABILITY" or report_type.upper() == "NETWORK OUTAGE"):
                        # report_obj=UbrReportBll()
                        # outage_data=report_obj.get_total_data_network_outage(3000,date1,date2,time1,time2,all_group,all_host)
                        outage_data = get_outage(
                            3000, date1, date2, time1, time2, all_group, all_host)
                        if (str(outage_data["success"]) == "0"):
                            inpt = deepcopy(outage_data["result"])
                        else:
                            return outage_data
                    elif (report_type.upper() == "TRAP" or report_type.upper() == "EVENTS"):
                        # report_obj=UbrReportBll()
                        # trap_data=report_obj.get_total_data_trap(3000,date1,date2,time1,time2,all_group,all_host)
                        trap_data = get_total_data_trap(
                            3000, date1, date2, time1, time2, all_group, all_host)
                        if (str(trap_data["success"]) == "0"):
                            inpt = deepcopy(trap_data["result"])
                        else:
                            return trap_data
                    elif (report_type.upper() == "CLIENT" or report_type.upper() == "CLIENTS"):
                        client_data = client_data_ap()
                        if (str(client_data["success"]) == "0"):
                            inpt = deepcopy(client_data["result"])
                        else:
                            return client_data
                    elif (report_type.upper() == "CONFIGURATION"):
                        configuration_data = get_configuration_details(
                            all_host.split(','))
                        return configuration_data
                        # if configuration_data['success']==0:
                        #    return configuration_data
                        # else:
                        #    return configuration_data
                else:
                    different_report = 0
                    # not a special report ... follow the steps
                    # 1 . find the query dict corresponding to this report
                    query_dict = re.get_query_dict(
                        device_type, report_type, date_temp_1, date_temp_2, all_host)
                    if (str(query_dict["success"]) == "0"):
                        # 2 . get the data for the report
                        # res_sql=re.get_sql_data(query_dict["result"])
                        if (view_type == "data_table"):
                            dict_shelve = shelve.open(
                                '/omd/sites/%s/share/check_mk/web/htdocs/download/%s.db' % (nms_instance,
                                                                                            new_user_report_dict[
                                                                                                "user_id"]))
                            dict_shelve_data = shelve.open(
                                '/omd/sites/%s/share/check_mk/web/htdocs/download/%s_data.db' %
                                (nms_instance, new_user_report_dict["user_id"]))
                            if ("user_info_dict" in dict_shelve):
                                user_report_dict = dict_shelve[
                                    "user_info_dict"]
                            else:
                                user_report_dict = {}
                            flag_dict = (user_report_dict != {}
                                         and user_report_dict == new_user_report_dict)
                            if flag_dict == True and str(sEcho) != "1":
                                res_sql = dict_shelve_data["res_sql"]
                                dict_shelve.close()
                                dict_shelve_data.close()
                            else:
                                res_sql = re.get_sql_data(
                                    query_dict["result"], date_temp_1, date_temp_2)
                                dict_shelve_data["res_sql"] = res_sql
                                dict_shelve[
                                    "user_info_dict"] = new_user_report_dict
                                dict_shelve.close()
                                dict_shelve_data.close()
                        else:
                            res_sql = re.get_sql_data(
                                query_dict["result"], date_temp_1, date_temp_2)
                        query_dict = query_dict["result"]
                        if (str(res_sql["success"]) == "0"):
                            if (view_type == "data_table"):
                                if (res_sql["result"] == []):
                                # status={"success":0,"aaData":[],
                                #"sEcho":int(sEcho),"iTotalRecords":res_sql["iTotalRecords"],"iTotalDisplayRecords":res_sql["iTotalDisplayRecords"]}
                                    status = {"success": 0, "aaData": [],
                                              "sEcho": 1, "iTotalRecords": 0, "iTotalDisplayRecords": 0}
                                    return status
                                data_report = res_sql["result"]
                                aaData = data_report
                                # sEcho=1#res_sql["sEcho"]
                                iTotalRecords = 100  # res_sql["iTotalRecords"]
                                iTotalDisplayRecords = 100  # res_sql["iTotalDisplayRecords"]
                            else:
                                data_report = res_sql["result"]
                        else:
                            return res_sql  # for exception
                            # should we group the data like in RSSI
                        #######################################-----GROUP THE DATA

                        if (str(query_dict["group_the_data"]) == "1"):
                            # get required variables for grouping
                            var = str(query_dict[
                                "group_the_data_variables"]).split(",")
                            # get_and_form_data_default(self,res,host_index,values_length,time_index,key,data_length,values1_index,values2_index):
                            if (len(var) == 12):
                                # 3. call function to group the data
                                # return data_report
                                res_group = re.get_and_form_data_default(data_report, int(var[0]), int(
                                    var[1]), int(var[2]), int(var[3]), int(var[4]), int(var[5]), int(var[6]),
                                                                         int(var[7]), int(var[8]), int(var[9]),
                                                                         int(var[10]), int(var[11]))
                                if (str(res_group["success"]) == "0"):
                                    data_report = res_group["result"]
                                else:
                                    return res_group  # for exception
                            #######################################-----END GROUPING THE DATA
                        #######################################-----FIND THE DELTA
                        if str(query_dict["find_delta"]) == "1":
                            # get_delta_for_values(self,inpt,host_index,data_length,values_length):
                            var_delta = str(
                                query_dict["find_delta_variables"]).split(",")
                            if (len(var_delta) == 7):
                                # 4 . find the delta
                                # return data_report
                                res_delta = re.get_delta_for_values(data_report, int(
                                    var_delta[0]), int(var_delta[1]), int(var_delta[2]), int(var_delta[3]),
                                                                    int(var_delta[4]), int(var_delta[5]),
                                                                    int(var_delta[6]))
                                # return res_delta
                                if (str(res_delta["success"]) == "0"):
                                    data_report = res_delta["result"]
                                else:
                                    return res_delta  # for exception
                            #######################################-----END DELTA
                        #######################################-----FORM THE DEFAULT DATA
                        if str(query_dict["default_data"]) == "1":
                            # get_delta_for_values(self,inpt,host_index,data_length,values_length):
                            var_default = str(
                                query_dict["default_data_variables"]).split(",")
                            if (len(var_default) == 4):
                                # 4 . find the delta
                                res_default = re.form_the_default_data(data_report, int(var_default[0]), int(
                                    var_default[1]), int(var_default[2]), int(var_default[3]), report_type)
                                # return res_default
                                if (str(res_default["success"]) == "0"):
                                    data_report = res_default["result"]
                                else:
                                    return res_default  # for exception
                                    #######################################-----END DEFAULT DATA
                    else:
                        return query_dict  # for exception
                        # common algo for all special reports
                    inpt = data_report
                given = deepcopy(column_value)
                req = deepcopy(key_user)
                outdata = []
                for i in inpt:
                    li = []
                    for k in req:
                        li.append("0")
                    for j in given:
                        if (req.count(j) >= 1):
                            loc = given.index(j)
                            wloc = req.index(j)
                            temp = i[loc]
                            li.pop(wloc)
                            li.insert(wloc, temp)
                    outdata.append(li)
                report_data_list = outdata
                # if(data_report["success"]=="0"):
                if (view_type == "data_table"):
                    if (different_report == 0):
                        if (str(sSortDir_0) == "asc"):
                            report_data_list2 = sorted(report_data_list, key=lambda report_data_list: report_data_list[
                                int(iSortCol_0)], reverse=False)
                        else:
                            report_data_list2 = sorted(report_data_list, key=lambda report_data_list:
                            report_data_list[int(iSortCol_0)], reverse=True)
                        if (str(s_search) != "" and s_search != "None" and s_search != "Null"):
                            report_data_list3 = []
                            for i in report_data_list2:
                                for j in i:
                                    if str(j).find(s_search) != -1:
                                        report_data_list3.append(i)
                                        break
                            report_data_list2 = report_data_list3

                        status = {"success": 0, "aaData": report_data_list2[
                                                          int(i_display_start):int(i_display_start) + int(
                                                              i_display_length)],
                                  "sEcho": int(sEcho), "iTotalRecords": len(report_data_list2),
                                  "iTotalDisplayRecords": len(report_data_list2)}
                        return status
                    else:
                        if (str(sSortDir_0) == "asc"):
                            report_data_list2 = sorted(report_data_list, key=lambda report_data_list: report_data_list[
                                int(iSortCol_0)], reverse=False)
                        else:
                            report_data_list2 = sorted(report_data_list, key=lambda report_data_list:
                            report_data_list[int(iSortCol_0)], reverse=True)
                        if (str(s_search) != "" and s_search != "None" and s_search != "Null"):
                            report_data_list3 = []
                            for i in report_data_list2:
                                for j in i:
                                    if str(j).find(s_search) != -1:
                                        report_data_list3.append(i)
                                        break
                            report_data_list2 = report_data_list3
                        status = {"success": 0, "aaData": report_data_list2[
                                                          int(i_display_start):int(i_display_start) + int(
                                                              i_display_length)],
                                  "sEcho": int(sEcho), "iTotalRecords": len(report_data_list2),
                                  "iTotalDisplayRecords": len(report_data_list2)}
                        return status
                if view_type == "excel":
                    sheet_dict = {
                        "sheet_name": result_columns["result"][4],
                        "main_title": result_columns["result"][5],
                        "second_title": result_columns["result"][6],
                        "headings": column_user,
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": result_columns["result"][7],
                        "data_report": report_data_list,
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    status = re.get_excel_sheet(sheet_dict)
                    if str(status["success"]) == "0":
                        el = EventLog()
                        # desc="Excel Report Generated for Hosts  "
                        desc = self.get_description(
                            all_host, result_columns["result"][4])
                        if str(desc["success"]) == "0":
                            el.log_event("Excel " + desc["result"], username)
                    return status
                else:
                    sheet_dict = {
                        "sheet_name": result_columns["result"][4],
                        "main_title": result_columns["result"][5],
                        "second_title": result_columns["result"][6],
                        "headings": column_user,
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": result_columns["result"][7],
                        "data_report": report_data_list,
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    status = re.get_csv_file(sheet_dict)
                    if str(status["success"]) == "0":
                        el = EventLog()
                        # desc="Excel Report Generated for Hosts  "
                        desc = self.get_description(
                            all_host, result_columns["result"][4])
                        if str(desc["success"]) == "0":
                            el.log_event("CSV " + desc["result"], username)
                    return status
            else:
                return result_columns
        except Exception, e:
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

    def get_excel_sheet(self, *params):
        """

        @param params:
        @return:
        """
        try:
            i = 4
            flag = 0
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
            # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4
            # = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark
            # Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 =
            # Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the
            # list goes on...
            style.pattern = pattern  # Add Pattern to Style

            font = xlwt.Font()  # Create Font
            font.bold = True  # Set font to Bold
            #        style = xlwt.XFStyle() # Create Style
            font.colour_index = 0x09
            style.font = font  # Add Bold Font to Style

            alignment = xlwt.Alignment()  # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
            alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
            #        style = xlwt.XFStyle() # Create Style
            style.alignment = alignment  # Add Alignment to Style

            style1 = xlwt.XFStyle()  # Create Style
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style1.alignment = alignment  # Add Alignment to Style
            xls_book = xlwt.Workbook(encoding='ascii')
            for par in params:
                sheet_dict = par
                i = 4
                sheet_name = sheet_dict["sheet_name"]
                main_title = sheet_dict["main_title"]
                second_title = sheet_dict["second_title"]
                headings = sheet_dict["headings"]
                name_report = sheet_dict["name_report"]
                path_report = sheet_dict["path_report"]
                data_report = sheet_dict["data_report"]
                date1 = sheet_dict["date1"]
                date2 = sheet_dict["date2"]
                time1 = sheet_dict["time1"]
                time2 = sheet_dict["time2"]
                device_type = sheet_dict["device_type"]
                dat1 = date1.replace("/", "-")
                dat2 = date2.replace("/", "-")
                # dat1 = dat1 + "(" + time1 + ")"
                # dat2 = dat2 + "(" + time2 + ")"
                name_report = main_title + "_from_" + str(dat1) + ' ' + str(time1) + ' to_' + str(dat2) + ' ' + str(
                    time2) + "_excel.xls"
                if data_report:
                    flag = 1
                sheet_no = 1
                xls_sheet = xls_book.add_sheet(
                    str(sheet_name), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421

                xls_sheet.write_merge(0, 0, 0, 6, main_title, style)
                xls_sheet.write_merge(1, 1, 0, 6, second_title, style)
                xls_sheet.write_merge(2, 2, 0, 6, "")
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')

                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for row in data_report:
                    for idx, elem in enumerate(row):
                        width = 5000
                        xls_sheet.write(i, idx, str(elem), style1)
                        xls_sheet.col(idx).width = width
                    if i == 60000:
                        i = 4
                        sheet_no += 1
                        xls_sheet = xls_book.add_sheet(str(
                            sheet_name) + str(sheet_no), cell_overwrite_ok=True)
                        xls_sheet.row(0).height = 521
                        xls_sheet.row(1).height = 421

                        xls_sheet.write_merge(0, 0, 0, 6, main_title, style)
                        xls_sheet.write_merge(1, 1, 0, 6, second_title, style)
                        xls_sheet.write_merge(2, 2, 0, 6, "")
                        heading_xf = xlwt.easyxf(
                            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')

                        xls_sheet.set_panes_frozen(
                            True)  # frozen headings instead of split panes
                        xls_sheet.set_horz_split_pos(
                            i)  # in general, freeze after last heading row
                        xls_sheet.set_remove_splits(
                            True)  # if user does unfreeze, don't leave a split there
                        for colx, value in enumerate(headings):
                            xls_sheet.write(i - 1, colx, value, heading_xf)
                    i = i + 1
            if flag == 0:
                result_dict = {"success": "1", "result": "data not available"}
                return result_dict
            xls_book.save(path_report + name_report)
            result_dict = {
                "success": "0", "result": "report successfully generated",
                "file": name_report, "filename": name_report, "path_report": path_report}
            return result_dict
        except Exception, e:
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

    def get_csv_file(self, *params):
        """

        @param params:
        @return:
        """
        try:
            for par in params:
                sheet_dict = par
                i = 4
                sheet_name = sheet_dict["sheet_name"]
                main_title = sheet_dict["main_title"]
                second_title = sheet_dict["second_title"]
                headings = sheet_dict["headings"]
                name_report = sheet_dict["name_report"]
                path_report = sheet_dict["path_report"]
                name_report = name_report.split(".")[0]
                name_report = name_report.split("excel")[0] + "csv.csv"
                data_report = sheet_dict["data_report"]
                date1 = sheet_dict["date1"]
                date2 = sheet_dict["date2"]
                time1 = sheet_dict["time1"]
                time2 = sheet_dict["time2"]
                device_type = sheet_dict["device_type"]
                dat1 = date1.replace("/", "_")
                dat2 = date2.replace("/", "_")
                different_report = 0
                dat1 = dat1 + "(" + time1 + ")"
                dat2 = dat2 + "(" + time2 + ")"
                name_report = main_title + "_" + dat1 + dat2 + "_csv.csv"
                if data_report:
                    flag = 1
                ofile = open(path_report + name_report, "wb")
                writer = csv.writer(ofile, delimiter=',', quotechar='"')
                blank_row = ["", "", ""]
                i = len(data_report[0])
                if i % 2 == 0:
                    j = i / 2
                    i = i + 1
                else:
                    j = (i - 1) / 2
                main_row = []
                second_row = []
                for m in range(i):
                    main_row.append("")
                    second_row.append("")
                main_row[j] = main_title
                second_row[j] = second_title
                i = 0
                for row1 in data_report:
                    if i == 0:
                        writer.writerow(main_row)
                        writer.writerow(second_row)
                        writer.writerow(blank_row)
                        writer.writerow(headings)
                    i += 1
                    writer.writerow(row1)
                ofile.close()
            if flag == 0:
                result_dict = {"success": "1", "result": "data not available"}
                return result_dict
                # xls_book.save(path_report+name_report)
            result_dict = {"success": "0", "result": "report successfully generated", "file":
                name_report, "filename": name_report, "path_report": path_report + "/" + name_report}
            return result_dict
        except Exception, e:
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

    def pagination_create_table(self, query_dict, i_display_start, i_display_length, s_search, sEcho):
        """

        @param query_dict:
        @param i_display_start:
        @param i_display_length:
        @param s_search:
        @param sEcho:
        @return:
        """
        a_columns = query_dict["columns"].split(",")
        s_index_column = a_columns[0]  # "ap.timestamp";
        s_table = query_dict["table_name"]  # " ap25_statisticsTable as ap "
        s_join = query_dict["join"]
        s_order = query_dict["order_by"]
        s_where = query_dict["where"]
        s_group_by = query_dict["group_by"]
        # a_columns will store table columns ... Not necessarily same as on HTML
        # s_index_column is the index column
        # s_table will store table name
        # s_join will store join query
        # s_order = variable which stores order by query
        # s_where = variable which stores where condition
        # s_group_by = group by query
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s" % (
                " , ".join(a_columns), s_table, s_join, s_where, s_group_by, s_order)  # ,s_limit)
            i_total = cursor.execute(sql)
            s_limit = ""
            # Filtering by where for searching
            if s_search != "" and s_search != "None":
                if s_where == "":
                    s_where += "WHERE ("
                else:
                    s_where += " AND ( "
                for i in range(0, len(a_columns)):
                    s_where += "%s LIKE '%%%s%%' OR " % (
                        a_columns[i], MySQLdb.escape_string(s_search))
                s_where = s_where[:-3]
                s_where += ")"
                # query to get data according to searching condition given by user
            # i_filtered_total= number of total records for searching condition
            cursor = db.cursor()
            sql_query1 = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s" % (
                " , ".join(a_columns), s_table, s_join, s_where, s_group_by, s_order)  # ,s_limit)
            cursor.execute(sql_query1)
            cursor.execute("SELECT FOUND_ROWS()")
            res_filter = cursor.fetchone()
            cursor.close()
            # if no record found
            if (res_filter == ()):
                output = {
                    "success": 0,
                    "sEcho": int(sEcho),
                    "iTotalRecords": i_total, # i_total,#i_filtered_total,#i_total,
                    "iTotalDisplayRecords": 0, # i_filtered_total,
                    "aaData": [],
                    "result": [],
                }
                # Encode Data into JSON
                # req.write(JSONEncoder().encode(output))
                return output
            i_filtered_total = res_filter[0]
            s_limit = ""
            if (i_display_start != "None" and i_display_length != '-1'):
                s_limit = "LIMIT %s, %s" % (MySQLdb.escape_string(
                    i_display_start), MySQLdb.escape_string(i_display_length))
                # query to get data according to searching condition given by user
            # but with limit like 0,10 or 10,10
            cursor = db.cursor()
            sql_query2 = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s %s" % (
                " , ".join(a_columns), s_table, s_join, s_where, s_group_by, s_order, s_limit)
            cursor.execute(sql_query2)
            r_result = cursor.fetchall()
            cursor.close()
            result_data = []
            if (r_result != ()):
                for a_row in r_result:
                    row = []
                    for i in a_row:
                        row.append(str(i))
                    result_data.append(list(row))
            if (result_data == []):
                output = {
                    "success": 0,
                    "result": [],
                    "sEcho": int(sEcho),
                    "iTotalRecords": i_total, # i_total,#i_filtered_total,#i_total,
                    "iTotalDisplayRecords": 0, # i_filtered_total,
                    "aaData": []
                }
                # Encode Data into JSON
                return output
                # query to get number of total records
            output = {
                "success": 0,
                "sEcho": int(sEcho),
                "iTotalRecords": int(i_total), # i_filtered_total,#i_total,
                "iTotalDisplayRecords": int(i_filtered_total), # i_filtered_total,
                #			"aaData":result_data,
                "result": result_data
            }
            # Encode Data into JSON
            # req.write(JSONEncoder().encode(output))
            return output
        except Exception, e:
        #		return {"succcess" : 1 , "result":str(e) }
            output = {
                "success": 0,
                "sEcho": int(sEcho),
                "iTotalRecords": 0, # i_total,#i_filtered_total,#i_total,
                "iTotalDisplayRecords": 0, # i_filtered_total,
                "aaData": [],
                "result": [],
                "exception": str(e)
            }
            return output

        finally:
            # Close database connection
            db.close()

    def trap_main_reporting_get_excel(
            self, date1, date2, time1, time2, all_host, report_type, device_type, all_group, view_type, i_display_start,
            i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, new_user_report_dict, username,
            hostgroup_id_list):
        """

        @param date1:
        @param date2:
        @param time1:
        @param time2:
        @param all_host:
        @param report_type:
        @param device_type:
        @param all_group:
        @param view_type:
        @param i_display_start:
        @param i_display_length:
        @param s_search:
        @param sEcho:
        @param sSortDir_0:
        @param iSortCol_0:
        @param new_user_report_dict:
        @param username:
        @param hostgroup_id_list:
        @return:
        """
        try:
            if device_type != "":
                db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
                cursor = db.cursor()
                sql = "SELECT `device_name` FROM `device_type` WHERE `device_type_id`='%s' " % (
                    device_type)
                cursor.execute(sql)
                result = cursor.fetchall()
                device_name = result[0][0]
                cursor.close()
                db.close()
            else:
                device_name = "Common Report"

            direct = ""
            dat1 = date1.replace("/", "-")
            dat2 = date2.replace("/", "-")
            different_report = 0
            dat1 = dat1 + " " + time1
            dat2 = dat2 + " " + time2
            d1 = datetime.strptime(dat1, "%d-%m-%Y %H:%M")
            d2 = datetime.strptime(dat2, "%d-%m-%Y %H:%M")
            date_temp_1 = str(d1)
            date_temp_2 = str(d2)
            aaData = []
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system
            re = MainReportBll()
            # report_obj=UbrReportBll()
            trap_data = trap_get_total_data_trap(
                report_type, 3000, date1, date2, time1, time2, all_group,
                all_host, hostgroup_id_list, device_type)
            if (str(trap_data["success"]) == "0" or trap_data["success"] == 0):
                report_data_dict = deepcopy(trap_data["result"])
            else:
                return trap_data  # in case of error return
            if (view_type == "data_table"):
                report_data_list = []
                if report_type == "all":
                    for table in report_data_dict:
                        report_data_list += report_data_dict[table]
                else:
                    report_data_list = report_data_dict
                if (trap_data["result"] == [] or report_data_list == []):
                    status = {"success": 0, "aaData": [],
                              "sEcho": 1, "iTotalRecords": 0, "iTotalDisplayRecords": 0}
                    return status
                    # report_data_list=report_data_list#trap_data["result"]
                if (str(sSortDir_0) == "asc"):
                    report_data_list2 = sorted(report_data_list, key=lambda report_data_list:
                    report_data_list[int(iSortCol_0)], reverse=False)
                else:
                    report_data_list2 = sorted(report_data_list, key=lambda report_data_list:
                    report_data_list[int(iSortCol_0)], reverse=True)
                if (str(s_search) != "" and s_search != "None" and s_search != "Null"):
                    report_data_list3 = []
                    for i in report_data_list2:
                        for j in i:
                            if str(j).find(s_search) != -1:
                                report_data_list3.append(i)
                                break
                    report_data_list2 = report_data_list3
                status = {"success": 0, "aaData": report_data_list2[
                                                  int(i_display_start):int(i_display_start) + int(i_display_length)],
                          "sEcho": int(sEcho), "iTotalRecords": len(report_data_list2),
                          "iTotalDisplayRecords": len(report_data_list2)}
                return status
            if report_type != "all":
                report_data_list = report_data_dict
                if view_type == "excel":
                    sheet_dict = {
                        "sheet_name": "Event_Report",
                        "main_title": "Event Report(%s)" % (report_type[0].upper() + report_type[1:]),
                        "second_title": device_name,
                        "headings": ["Timestamp", "IP Address", "Host Alias", "Hostgroup", "Device Type", "Severity",
                                     "Event Name", "Event ID", "Event Type", "Manage Object ID", "Manage Object Name",
                                     "Component ID", "Description"],
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": "event_report.xls",
                        "data_report": report_data_list,
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    status = re.get_excel_sheet(sheet_dict)
                    if str(status["success"]) == "0":
                        el = EventLog()
                        desc = self.get_description(all_host, "Event report")
                        if str(desc["success"]) == "0":
                            el.log_event("Excel " + desc["result"], username)
                    return status
                else:
                    sheet_dict = {
                        "sheet_name": "Event_Report",
                        "main_title": "Event Report(%s)" % (report_type[0].upper() + report_type[1:]),
                        "second_title": device_name,
                        "headings": ["Timestamp", "IP Address", "Host Alias", "Hostgroup", "Device Type", "Severity",
                                     "Event Name", "Event ID", "Event Type", "Manage Object ID", "Manage Object Name",
                                     "Component ID", "Description"],
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": "event_report.csv",
                        "data_report": report_data_list,
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    status = re.get_csv_file(sheet_dict)
                    if str(status["success"]) == "0":
                        el = EventLog()
                        # desc="Excel Report Generated for Hosts  "
                        desc = self.get_description(all_host, "Event report")
                        if str(desc["success"]) == "0":
                            el.log_event("CSV " + desc["result"], username)
                    return status
            else:
                if view_type == "excel":
                    sheet_dict_current = {
                        "sheet_name": "Event_Report_current",
                        "main_title": "Event Report(%s)" % (report_type[0].upper() + report_type[1:]),
                        "second_title": device_name,
                        "headings": ["Timestamp", "IP Address", "Host Alias", "Hostgroup", "Device Type", "Severity",
                                     "Event Name", "Event ID", "Event Type", "Manage Object ID", "Manage Object Name",
                                     "Component ID", "Description"],
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": "event_report.xls",
                        "data_report": report_data_dict["current"],
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    sheet_dict_clear = {
                        "sheet_name": "Event_Report_clear",
                        "main_title": "Event Report(%s)" % (report_type[0].upper() + report_type[1:]),
                        "second_title": device_name,
                        "headings": ["Timestamp", "IP Address", "Host Alias", "Hostgroup", "Device Type", "Severity",
                                     "Event Name", "Event ID", "Event Type", "Manage Object ID", "Manage Object Name",
                                     "Component ID", "Description"],
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": "event_report.xls",
                        "data_report": report_data_dict["clear"],
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    sheet_dict_history = {
                        "sheet_name": "Event_Report_history",
                        "main_title": "Event Report(%s)" % (report_type[0].upper() + report_type[1:]),
                        "second_title": device_name,
                        "headings": ["Timestamp", "IP Address", "Host Alias", "Hostgroup", "Device Type", "Severity",
                                     "Event Name", "Event ID", "Event Type", "Manage Object ID", "Manage Object Name",
                                     "Component ID", "Description"],
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": "event_report.xls",
                        "data_report": report_data_dict["history"],
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    status = re.get_excel_sheet(
                        sheet_dict_current, sheet_dict_clear, sheet_dict_history)
                    if str(status["success"]) == "0":
                        el = EventLog()
                        desc = self.get_description(all_host, "Event report")
                        if str(desc["success"]) == "0":
                            el.log_event("Excel " + desc["result"], username)
                    return status
                else:
                    sheet_dict_current = {
                        "sheet_name": "Event_Report_current",
                        "main_title": "Event Report(%s)" % (report_type[0].upper() + report_type[1:]),
                        "second_title": device_name,
                        "headings": ["Timestamp", "IP Address", "Host Alias", "Hostgroup", "Device Type", "Severity",
                                     "Event Name", "Event ID", "Event Type", "Manage Object ID", "Manage Object Name",
                                     "Component ID", "Description"],
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": "event_report.csv",
                        "data_report": report_data_dict["current"],
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    sheet_dict_clear = {
                        "sheet_name": "Event_Report_clear",
                        "main_title": "Event Report(%s)" % (report_type[0].upper() + report_type[1:]),
                        "second_title": device_name,
                        "headings": ["Timestamp", "IP Address", "Host Alias", "Hostgroup", "Device Type", "Severity",
                                     "Event Name", "Event ID", "Event Type", "Manage Object ID", "Manage Object Name",
                                     "Component ID", "Description"],
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": "event_report.csv",
                        "data_report": report_data_dict["clear"],
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    sheet_dict_history = {
                        "sheet_name": "Event_Report_history",
                        "main_title": "Event Report(%s)" % (report_type[0].upper() + report_type[1:]),
                        "second_title": device_name,
                        "headings": ["Timestamp", "IP Address", "Host Alias", "Hostgroup", "Device Type", "Severity",
                                     "Event Name", "Event ID", "Event Type", "Manage Object ID", "Manage Object Name",
                                     "Component ID", "Description"],
                        "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                        "name_report": "event_report.csv",
                        "data_report": report_data_dict["history"],
                        "date1": date1,
                        "date2": date2,
                        "time1": time1,
                        "time2": time2,
                        "device_type": device_type}
                    status = re.get_csv_file(
                        sheet_dict_current, sheet_dict_clear, sheet_dict_history)
                    if str(status["success"]) == "0":
                        el = EventLog()
                        # desc="Excel Report Generated for Hosts  "
                        desc = self.get_description(all_host, "Event report")
                        if str(desc["success"]) == "0":
                            el.log_event("CSV " + desc["result"], username)
                    return status
        except Exception, e:
            result_dict = {"success": "1", "result": str(e)}
            return result_dict


# Function for Device Reachability final calculation
# MainOutage class has main logic for device reachablity
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
                # t_date=result[0][2]
                t_date = datetime.strptime(
                    start_date, "%Y-%m-%d %H:%M:%S")  # status_result[0][2]
                t_date = t_date.replace(hour=0, minute=0, second=0)
                t_list = ((status_result[0][0], status_result[0][1], t_date, status_result[0][3], status_result[0][
                    4], status_result[0][5], status_result[0][6]),)
                result = t_list + result
            elif status_result != ():
                # t_date=status_result[0][2]
                t_date = datetime.strptime(
                    start_date, "%Y-%m-%d %H:%M:%S")  # status_result[0][2]
                t_date = t_date.replace(hour=0, minute=0, second=0)
                t_list = ((status_result[0][0], status_result[0][1], t_date, status_result[0][3], status_result[0][
                    4], status_result[0][5], status_result[0][6]),)
                result = t_list

            m = MainOutage(result, datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"), datetime.strptime(
                start_date, "%Y-%m-%d %H:%M:%S"))
            temp_res = m.get_outage()

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
                        i[-2] = round((float(uptime) * 100 / float(total)), 2)
                        i[-1] = round((float(downtime) * 100 / float(total)), 2)

                        tr.append(i)

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


# TOTAL TRAP DATA FOR A GIVEN DATE PERIOD BY SERVITY
def get_total_data_trap(no_of_devices, date1, date2, time1, time2, all_group, all_host):
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
        host_data = str(
            all_host.split(',')).replace('[', '(').replace(']', ')')
        query = "SELECT date(ta.timestamp) ,hosts.host_alias,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
 			 FROM trap_alarms as ta join (select host_name,host_id,ip_address,host_alias from hosts ) as hosts on hosts.ip_address=ta.agent_id  \
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
        conn.close()
        while i < length:
            host = str(res[i][1])
            ls.append(str(res[i][0]))
            ls.append(str(res[i][1]))
            ls.append(str(res[i][2]))
            group_name = res[i][5]
            ls.append(group_name)
            lst = [0, 0, 0, 0, 0, 0]
            while (i < length and str(res[i][1]) == str(res[i + 1][1]) and str(res[i][0]) == str(res[i + 1][0])):
                lst[int(res[i][4])] = int(res[i][3])
                i = i + 1
            lst[int(res[i][4])] = int(res[i][3])
            ls.append(lst[0] + lst[2])
            ls.append(lst[1])
            ls.append(lst[3])
            ls.append(lst[4])
            ls.append(lst[5])
            tr.append(ls)
            ls = []
            lst = [0, 0, 0, 0, 0, 0]
            i = i + 1
        if i <= length:  # and str(res[i][1])==str(res[i-1][1]) and str(res[i][0])==str(res[i-1][0]):
            ls.append(str(res[i][0]))
            ls.append(str(res[i][1]))
            ls.append(str(res[i][2]))
            lst = [0, 0, 0, 0, 0, 0]
            group_name = res[i][5]
            ls.append(group_name)
            lst[int(res[i][4])] = int(res[i][3])
            lst[int(res[i][4])] = int(res[i][3])
            ls.append(lst[0] + lst[2])
            ls.append(lst[1])
            ls.append(lst[3])
            ls.append(lst[4])
            ls.append(lst[5])
            tr.append(ls)
        result_dict["result"] = tr
        return result_dict
    except Exception, e:
        result_dict = {}
        result_dict["success"] = 1
        result_dict["result"] = str(e)
        return result_dict


def trap_get_total_data_trap(report_type, no_of_devices, date1, date2, time1, time2, all_group, all_host,
                             hostgroup_id_list, device_type):
    """

    @param report_type:
    @param no_of_devices:
    @param date1:
    @param date2:
    @param time1:
    @param time2:
    @param all_group:
    @param all_host:
    @param hostgroup_id_list:
    @param device_type:
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
        host_data = str(
            all_host.split(',')).replace('[', '(').replace(']', ')')
        table_dict = {"clear": "trap_alarm_clear", "current":
            "trap_alarm_current", "history": "trap_alarms"}
        if device_type != "":
            device_type = "AND hosts.device_type_id='%s'" % (device_type)
        else:
            device_type = ''

        if report_type != "all":
            table_name = table_dict[report_type]
            if all_host != "":
                query = "SELECT ta.timestamp,ta.agent_id,hosts.host_alias,hostgroups.hostgroup_name,device_type.device_name,if(ta.serevity=0,'Normal',if(ta.serevity=1,'Informational',\
if(ta.serevity=2,'Normal',if(ta.serevity=3,'Minor', \
if(ta.serevity=4,'Major','Critical'))))) as serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,ta.manage_obj_id,ta.manage_obj_name,ta.component_id, \
ta.description From  %s as ta \
join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts where is_deleted = 0 ) as hosts on hosts.ip_address=ta.agent_id \
INNER JOIN device_type ON device_type.device_type_id = hosts.device_type_id \
INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id \
INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id  and hostgroups.hostgroup_id IN (%s) \
where  ta.timestamp between '%s' AND '%s' AND hosts.host_id IN %s %s \
order by  ta.timestamp desc ,device_type.device_name,hosts.host_name,ta.serevity" % (
                table_name, ','.join(hostgroup_id_list), date_temp1, date_temp2, host_data, device_type)

            # query="SELECT date(ta.timestamp) ,hosts.host_alias,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
            #	FROM %s as ta join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts ) as hosts on hosts.ip_address=ta.agent_id\
            #	INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
            #	INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id  and hostgroups.hostgroup_id IN (%s)\
            #	where  ta.timestamp between '%s' AND '%s' AND hosts.host_id IN %s %s group by  hosts.host_id,serevity,date(ta.timestamp)\
            # order by  hosts.host_name,ta.timestamp,ta.serevity
            # "%(table_name,','.join(hostgroup_id_list),date_temp1,date_temp2,host_data,device_type)
            else:
                query = "SELECT ta.timestamp,ta.agent_id,hosts.host_alias,hostgroups.hostgroup_name,device_type.device_name,if(ta.serevity=0,'Normal',if(ta.serevity=1,'Informational',\
if(ta.serevity=2,'Normal',if(ta.serevity=3,'Minor', \
if(ta.serevity=4,'Major','Critical'))))) as serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,ta.manage_obj_id,ta.manage_obj_name,ta.component_id, \
ta.description From  %s as ta  \
join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts where is_deleted = 0 ) as hosts on hosts.ip_address=ta.agent_id \
INNER JOIN device_type ON device_type.device_type_id = hosts.device_type_id \
INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id \
INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id and hostgroups.hostgroup_id IN (%s) \
where  ta.timestamp between '%s' AND '%s' %s \
order by ta.timestamp desc,device_type.device_name,hosts.host_name,ta.serevity " % (
                table_name, ','.join(hostgroup_id_list), date_temp1, date_temp2, device_type)

            # query="SELECT date(ta.timestamp) ,hosts.host_alias,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
            # FROM %s as ta join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts ) as hosts on hosts.ip_address=ta.agent_id\
            # INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
            # INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id and hostgroups.hostgroup_id IN (%s)\
            # where  ta.timestamp between '%s' AND '%s' %s group by hosts.host_id,serevity,date(ta.timestamp)\
            # order by  hosts.host_name,ta.timestamp,ta.serevity
            # "%(table_name,','.join(hostgroup_id_list),date_temp1,date_temp2,device_type)
            cursor.execute(query)
            res = cursor.fetchall()
            conn.close()
            if (len(res) == 0):
                return result_dict
            tr = []
            for row in res:
                tr.append(make_list(row))
            result_dict["result"] = tr
            return result_dict
        else:
            complete_dict = {}
            for table in table_dict:
                table_name = table_dict[table]
                if all_host != "":
                    query = "SELECT ta.timestamp,ta.agent_id,hosts.host_alias,hostgroups.hostgroup_name,device_type.device_name,if(ta.serevity=0,'Normal',if(ta.serevity=1,'Informational',\
if(ta.serevity=2,'Normal',if(ta.serevity=3,'Minor', \
if(ta.serevity=4,'Major','Critical'))))) as serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,ta.manage_obj_id,ta.manage_obj_name,ta.component_id, \
ta.description From  %s as ta \
join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts where is_deleted = 0 ) as hosts on hosts.ip_address=ta.agent_id \
INNER JOIN device_type ON device_type.device_type_id = hosts.device_type_id \
INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id \
INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id  and hostgroups.hostgroup_id IN (%s) \
where  ta.timestamp between '%s' AND '%s' AND hosts.host_id IN %s %s \
order by  ta.timestamp desc ,device_type.device_name,hosts.host_name,ta.serevity" % (
                    table_name, ','.join(hostgroup_id_list), date_temp1, date_temp2, host_data, device_type)

                    # query="SELECT date(ta.timestamp) ,hosts.host_alias,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
                    #	FROM %s as ta join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts ) as hosts on hosts.ip_address=ta.agent_id\
                    #	INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                    #	INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id  and hostgroups.hostgroup_id IN (%s)\
                    #	where  ta.timestamp between '%s' AND '%s' AND hosts.host_id IN %s %s group by  hosts.host_id,serevity,date(ta.timestamp)\
                    # order by  hosts.host_name,ta.timestamp,ta.serevity
                    # "%(table_name,','.join(hostgroup_id_list),date_temp1,date_temp2,host_data,device_type)
                else:
                    query = "SELECT ta.timestamp,ta.agent_id,hosts.host_alias,hostgroups.hostgroup_name,device_type.device_name,if(ta.serevity=0,'Normal',if(ta.serevity=1,'Informational',\
if(ta.serevity=2,'Normal',if(ta.serevity=3,'Minor', \
if(ta.serevity=4,'Major','Critical'))))) as serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,ta.manage_obj_id,ta.manage_obj_name,ta.component_id, \
ta.description From  %s as ta  \
join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts where is_deleted = 0 ) as hosts on hosts.ip_address=ta.agent_id \
INNER JOIN device_type ON device_type.device_type_id = hosts.device_type_id \
INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id \
INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id and hostgroups.hostgroup_id IN (%s) \
where  ta.timestamp between '%s' AND '%s' %s \
order by ta.timestamp desc,device_type.device_name,hosts.host_name,ta.serevity " % (
                    table_name, ','.join(hostgroup_id_list), date_temp1, date_temp2, device_type)

                    # query="SELECT date(ta.timestamp) ,hosts.host_alias,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
                    # FROM %s as ta join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts ) as hosts on hosts.ip_address=ta.agent_id\
                    # INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
                    # INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id and hostgroups.hostgroup_id IN (%s)\
                    # where  ta.timestamp between '%s' AND '%s' %s group by hosts.host_id,serevity,date(ta.timestamp)\
                    # order by  hosts.host_name,ta.timestamp,ta.serevity
                    # "%(table_name,','.join(hostgroup_id_list),date_temp1,date_temp2,device_type)
                cursor.execute(query)
                res = cursor.fetchall()
                # conn.close()
                if (len(res) == 0):
                    complete_dict[table] = []
                    continue
                tr = []
                for row in res:
                    tr.append(make_list(row))
                complete_dict[table] = tr
            result_dict["result"] = complete_dict
            return result_dict
    except Exception, e:
        result_dict = {}
        result_dict["success"] = 1
        result_dict["result"] = str(e)
        return result_dict

# TOTAL TRAP DATA FOR A GIVEN DATE PERIOD BY SERVITY


def trap_get_total_data_trap_old(report_type, no_of_devices, date1, date2, time1, time2, all_group, all_host,
                                 hostgroup_id_list, device_type):
    """

    @param report_type:
    @param no_of_devices:
    @param date1:
    @param date2:
    @param time1:
    @param time2:
    @param all_group:
    @param all_host:
    @param hostgroup_id_list:
    @param device_type:
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
        host_data = str(
            all_host.split(',')).replace('[', '(').replace(']', ')')
        table_dict = {"clear": "trap_alarm_clear", "current":
            "trap_alarm_current", "history": "trap_alarms"}
        table_name = table_dict[report_type]
        if device_type != "":
            device_type = "AND hosts.device_type_id='%s'" % (device_type)
        else:
            device_type = ''
        if all_host != "":
            query = "SELECT date(ta.timestamp) ,hosts.host_alias,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
	        	FROM %s as ta join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts ) as hosts on hosts.ip_address=ta.agent_id\
	        	INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
	        	INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id  and hostgroups.hostgroup_id IN (%s)\
	        	where  ta.timestamp between '%s' AND '%s' AND hosts.host_id IN %s %s group by  hosts.host_id,serevity,date(ta.timestamp)\
	        	order by  hosts.host_name,ta.timestamp,ta.serevity " % (
            table_name, ','.join(hostgroup_id_list), date_temp1, date_temp2, host_data, device_type)
        else:
            query = "SELECT date(ta.timestamp) ,hosts.host_alias,hosts.ip_address,count(ta.trap_event_id),ta.serevity,hostgroups.hostgroup_name\
	        FROM %s as ta join (select host_name,host_id,ip_address,host_alias,device_type_id from hosts ) as hosts on hosts.ip_address=ta.agent_id\
	        INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = hosts.host_id\
	        INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id and hostgroups.hostgroup_id IN (%s)\
	        where  ta.timestamp between '%s' AND '%s' %s group by hosts.host_id,serevity,date(ta.timestamp)\
	        order by  hosts.host_name,ta.timestamp,ta.serevity " % (
            table_name, ','.join(hostgroup_id_list), date_temp1, date_temp2, device_type)
        cursor.execute(query)
        res = cursor.fetchall()
        if (len(res) == 0):
            return result_dict
        length = len(res) - 1
        ls = []
        tr = []
        i = 0
        conn.close()
        while i < length:
            host = str(res[i][1])
            ls.append(str(res[i][0]))
            ls.append(str(res[i][1]))
            ls.append(str(res[i][2]))
            group_name = res[i][5]
            ls.append(group_name)
            lst = [0, 0, 0, 0, 0, 0]
            while (i < length and str(res[i][1]) == str(res[i + 1][1]) and str(res[i][0]) == str(res[i + 1][0])):
                lst[int(res[i][4])] = int(res[i][3])
                i = i + 1
            lst[int(res[i][4])] = int(res[i][3])
            ls.append(lst[0] + lst[2])
            ls.append(lst[1])
            ls.append(lst[3])
            ls.append(lst[4])
            ls.append(lst[5])
            tr.append(ls)
            ls = []
            lst = [0, 0, 0, 0, 0, 0]
            i = i + 1
        if i <= length:  # and str(res[i][1])==str(res[i-1][1]) and str(res[i][0])==str(res[i-1][0]):
            ls.append(str(res[i][0]))
            ls.append(str(res[i][1]))
            ls.append(str(res[i][2]))
            lst = [0, 0, 0, 0, 0, 0]
            group_name = res[i][5]
            ls.append(group_name)
            lst[int(res[i][4])] = int(res[i][3])
            lst[int(res[i][4])] = int(res[i][3])
            ls.append(lst[0] + lst[2])
            ls.append(lst[1])
            ls.append(lst[3])
            ls.append(lst[4])
            ls.append(lst[5])
            tr.append(ls)
        result_dict["result"] = tr
        return result_dict
    except Exception, e:
        result_dict = {}
        result_dict["success"] = 1
        result_dict["result"] = str(e)
        return result_dict


########## AP Functions
def get_time_ago(date1):
    """

    @param date1:
    @return:
    """
    last_check = ""
    date1 = datetime.strptime(
        date1, "%Y-%m-%d %H:%M:%S")  # mysql datetime syntax
    if datetime.now() > date1:
        delta = datetime.now() - date1
    else:
        delta = date1 - datetime.now()
    second = delta.seconds
    if delta.days != 0:
        last_check = str(delta.days) + " days ago"
    else:
        if second < 60:
            last_check = str(second) + " sec ago"
        elif second < 3600:
            minute = int(second / 60)
            last_check = str(minute) + " min ago"
        else:
            hour = int(second / 3600)
            minute = int((second - hour * 3600) / 60)
            last_check = str(hour) + " hour," + str(minute) + " min ago"
    return last_check


# Client Function For AP Clients
def client_data_ap():
    """


    @return:
    """
    try:
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = conn.cursor()
        query = "select client_name,UPPER(mac),total_tx,total_rx,first_seen_time,ifnull(hosts_first.host_alias,'-') as first_host_alias,last_seen_time,ifnull(hosts_last.host_alias,'-') as last_host_alias,if(ap_connected_client.state='1','Yes','No') from ap_client_details as ap \
left join (select host_id,host_alias,ip_address from hosts) as hosts_first on hosts_first.host_id=ap.first_seen_ap_id \
left join (select host_id,host_alias,ip_address from hosts) as hosts_last on hosts_last.host_id=ap.last_seen_ap_id \
left join (select state,host_id,client_id from ap_connected_client ) as ap_connected_client on ap.client_id=ap_connected_client.client_id and ap.last_seen_ap_id=ap_connected_client.host_id \
order by ap.client_id"
        cursor.execute(query)
        res = cursor.fetchall()
        total_li = []
        for i in range(len(res)):
            li = make_list(res[i])
            li[4] = get_time_ago(li[4])
            li[6] = get_time_ago(li[6])
            total_li.append(li)
        conn.close()
        result_dict = {}
        result_dict["success"] = 0
        result_dict["result"] = total_li
        return result_dict
    except Exception, e:
        result_dict = {}
        result_dict["success"] = 1
        result_dict["result"] = str(e)
        return result_dict


class MainOutage(object):
    """

    @param result_tuple:
    @param end_date:
    @param start_date:
    """
    from copy import deepcopy

    def __init__(self, result_tuple, end_date, start_date):
        self.prev_value = None
        self.prev_date = None
        self.prev_ip = None
        self.main_list = []
        self.prev_tpl = None
        self.result_tuple = result_tuple
        self.end_date = end_date
        if self.result_tuple and start_date < result_tuple[0][2]:
            self.start_date = deepcopy(result_tuple[0][2])
        else:
            self.start_date = start_date
            # logme(" result_tuple  = "+str(result_tuple))
            # logme(" end_date  = "+repr(end_date))
            # logme(" start_date  = "+repr(start_date))

    def fill_leftout_dates(self, leftout_days, mid_date, temp_date, is_last_call):
        """

        @param leftout_days:
        @param mid_date:
        @param temp_date:
        @param is_last_call:
        """
        for i in range(leftout_days):
            self.prev_date = mid_date + timedelta(days=i + 1)
            uptime, downtime = None, None
            if self.prev_tpl[0] == '50002':
                uptime = timedelta(0, 86399)
            else:
                downtime = timedelta(0, 86399)
            if not is_last_call:
                if self.prev_date.year == temp_date.year \
                    and self.prev_date.month == temp_date.month \
                    and self.prev_date.day == temp_date.day:
                    continue
                # logme(" left "+str(self.prev_date)+ "  || "+str(self.prev_value) + "  || "+str(self.prev_tpl[0]) + "\n")
            self.main_list.append([self.prev_date, self.prev_tpl[4],
                                   self.prev_tpl[5], self.prev_tpl[6], uptime, downtime])

        if is_last_call:
            if self.prev_date and self.prev_date < self.end_date:
                uptime, downtime = None, None
                # logme(str(self.prev_value)+" ---------  "+str(self.prev_tpl))
                if self.prev_value == '50002':
                    uptime = timedelta(0, 86399)
                else:
                    downtime = timedelta(0, 86399)
                    #if (self.end_date - temp_date) > timedelta(0, 86399):
                if self.main_list[-1][0].year == self.end_date.year \
                    and self.main_list[-1][0].month == self.end_date.month \
                    and self.main_list[-1][0].day == self.end_date.day:
                    # logme(" in in ")
                    pass
                else:
                    # logme(repr(self.main_list[-1][0])+ "  ***  "+ repr(temp_date))
                    self.main_list.append([self.end_date, self.prev_tpl[4],
                                           self.prev_tpl[5], self.prev_tpl[6], uptime, downtime])


    def fill_first(self, temp_date, uptime, downtime):
        """

        @param temp_date:
        @param uptime:
        @param downtime:
        @return:
        """
        date_to_use = temp_date - timedelta(days=1)
        mid_date = datetime(date_to_use.year,
                            date_to_use.month, date_to_use.day, 23, 59, 59)

        if self.prev_value == '50002':
            if uptime == None:
                uptime = (temp_date - mid_date)
            else:
                uptime += (temp_date - mid_date)

        elif self.prev_value == '50001':
            if downtime == None:
                downtime = (temp_date - mid_date)
            else:
                downtime += (temp_date - mid_date)
        return uptime, downtime

    def fill_end_dates(self, temp_date, temp_value, uptime, downtime):
        """

        @param temp_date:
        @param temp_value:
        @param uptime:
        @param downtime:
        """
        deduct_date = temp_date
        if self.start_date > temp_date:
            deduct_date = self.start_date
        if self.end_date.month > temp_date.month or self.end_date.day > temp_date.day:
            mid_date = datetime(temp_date.year,
                                temp_date.month, temp_date.day, 23, 59, 59)
        else:
            if self.end_date.hour >= temp_date.hour:
                mid_date = self.end_date
            else:
                mid_date = None

        if mid_date:
            if temp_value == '50002':
                if uptime:
                    uptime += (mid_date - deduct_date)
                else:
                    uptime = (mid_date - deduct_date)

            elif temp_value == '50001':
                if downtime:
                    downtime += (mid_date - deduct_date)
                else:
                    downtime = (mid_date - deduct_date)
                # logme(" END "+str(temp_date) + "\n")
            self.main_list.append([temp_date, self.prev_tpl[4],
                                   self.prev_tpl[5], self.prev_tpl[6], uptime, downtime])


    def get_outage(self):
        """


        @return:
        """
        try:
            uptime = None
            downtime = None
            for tpl in self.result_tuple:
                temp_ip = tpl[4]
                temp_date = tpl[2]
                temp_value = tpl[0]
                if self.prev_tpl:
                    self.prev_value = self.prev_tpl[0]
                    self.prev_date = self.prev_tpl[2]

                if temp_ip == self.prev_ip:
                    if temp_date.month > self.prev_date.month or temp_date.day > self.prev_date.day:
                        is_date = 1
                    else:
                        # logme('\n')
                        # logme(" self.start ", str(self.start_date), "self.prev_date", self.prev_date, "temp_date " , str(temp_date), " uptime " , str(uptime), " self.prev_value " , str(self.prev_value), " downtime " , str(downtime))

                        if self.prev_value == '50002':
                            if uptime == None:
                                # check this and temp_date.day == self.start_date.day condition
                                if downtime is None and self.start_date < temp_date and (
                                    temp_date - self.start_date ) < timedelta(0,
                                                                              86399) and temp_date.day == self.start_date.day:
                                    # logme("iiiiiiiiii  ",str(temp_date - self.start_date))
                                    uptime = (temp_date - self.start_date)
                                else:
                                    uptime = (temp_date - self.prev_date)
                            else:
                                uptime += (temp_date - self.prev_date)

                        elif self.prev_value == '50001':
                            if downtime == None:
                                if uptime is None and self.start_date < temp_date and (
                                    temp_date - self.start_date ) < timedelta(0,
                                                                              86399) and temp_date.day == self.start_date.day:
                                    # logme("KKKKKKK  ",str(temp_date - self.start_date))
                                    downtime = (temp_date - self.start_date)
                                else:
                                    downtime = (temp_date - self.prev_date)
                            else:
                                downtime += (temp_date - self.prev_date)

                        # logme(" self.start ", str(self.start_date),"self.prev_date", self.prev_date, " temp_date " , str(temp_date), " uptime " , str(uptime), " self.prev_value " , str(self.prev_value), " downtime " , str(downtime))
                        # logme('\n')
                        self.prev_date = temp_date  # print "jump1"

                else:
                    is_new = 1

                if is_new:
                    is_new = 0
                    self.prev_ip = temp_ip
                    is_date = 1
                    if self.prev_value:
                        # print " IS NEW TESTED "
                        uptime, downtime = self.fill_first(temp_date, uptime, downtime)
                        self.fill_end_dates(temp_date, temp_value, uptime, downtime)

                    self.prev_value = None
                    self.prev_date = None

                if is_date:
                    if uptime == None and downtime == None and not self.prev_value:
                        if self.start_date < temp_date and (temp_date - self.start_date ) < timedelta(0, 86399):
                            # date_to_use = temp_date - timedelta(days = 1)
                            # mid_date = datetime(date_to_use.year,
                            #                 date_to_use.month, date_to_use.day, 23, 59, 59)
                            mid_date = deepcopy(self.start_date)
                            delta = temp_date - mid_date
                            # print "IF temp_date, delta ", temp_date,' || ',  delta
                            # logme("IF temp_date, delta ", temp_date,' || ',  delta)
                            if temp_value == '50001':
                                uptime = delta
                            elif temp_value == '50002':
                                downtime = delta
                    else:
                        mid_date = datetime(self.prev_date.year,
                                            self.prev_date.month, self.prev_date.day, 23, 59, 59)
                        delta = mid_date - self.prev_date
                        # logme(">>>ELSE mid_date ", mid_date, " self.prev_date ",self.prev_date,' temp_date ',  temp_date,' uptime ',  uptime, ' downtime ', downtime)
                        if self.prev_value == '50002':
                            if uptime == None:
                                uptime = delta
                            else:
                                uptime += delta

                        elif self.prev_value == '50001':
                            if downtime == None:
                                downtime = delta
                            else:
                                downtime += delta

                                # print "ELSE temp_date, delta ", self.prev_date,' || ',  temp_date,' || ',  uptime, ' || ', downtime

                    if self.prev_value:
                        # print " ______________ ", self.prev_date,' || ',  uptime,' || ',  downtime
                        self.main_list.append([self.prev_date, self.prev_tpl[4],
                                               self.prev_tpl[5], self.prev_tpl[6], uptime, downtime])
                        uptime = None
                        downtime = None

                        #leftout_days = (temp_date - self.prev_date).days
                        #self.fill_leftout_dates((temp_date - self.prev_date).days, self.prev_date + timedelta(days = 1))
                        self.fill_leftout_dates((temp_date - self.prev_date).days, self.prev_date, temp_date, 0)

                        uptime, downtime = None, None

                if is_date and self.prev_value:
                    # print " ^^^^^^^^^^^^^^^^^^^^^  ", uptime,' || ', temp_date,' || ',  downtime
                    uptime, downtime = self.fill_first(temp_date, uptime, downtime)
                    # print " >>>>>>>>>>>>>>>>>  ", uptime,' || ',  temp_date,' || ',  downtime

                is_date = 0
                self.prev_tpl = tpl[:]

            if self.result_tuple:
                if uptime is None and downtime is None:
                    uptime, downtime = self.fill_first(temp_date, uptime, downtime)

                self.fill_end_dates(temp_date, temp_value, uptime, downtime)
                self.fill_leftout_dates((self.end_date - temp_date).days, temp_date, temp_date, 1)

            main_dict = {}
            main_dict['success'] = 0
            main_dict['result'] = self.main_list
            main_dict['outage'] = "main_outage"
            # logme(" ^^^^^^^^^^  ", main_dict)
            return main_dict
        except Exception:
            import traceback

            main_dict = {}
            main_dict['success'] = 1
            main_dict['result'] = traceback.format_exc()
            logme(traceback.format_exc())
            return main_dict