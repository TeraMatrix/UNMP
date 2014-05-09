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
import csv
from datetime import timedelta, datetime
from operator import itemgetter
import os
import shelve
import subprocess
import tarfile
import time

import MySQLdb
import xlwt
from common_bll import EventLog
from common_vars import make_list
from defaults import site as nms_instance
from main_reporting_bll import MainOutage
from unmp_config import SystemConfig


class HistoryReportBll(object):
    """
    Historical report related Model class
    """
    def restore_backup(self, month_var, db_backup):
        """

        @param month_var:
        @param db_backup:
        @return:
        """
        try:
            month_var = month_var.split('_')
            year = month_var[0]
            month = month_var[1]
            cur_db = SystemConfig.get_mysql_credentials()[3]
            #            cur_db="nmsp"
            path_backup = '/omd/daemon/mysql_backup/%s_%s.tar.bz2' % (
                year, month)
            path_temp = '/omd/daemon/mysql_temp/'
            dst = path_backup  # where backup will be stored
            fileorfolder = path_backup  # which file you want backup of
            out = tarfile.TarFile.open(dst, 'r:bz2')
            cwd = os.getcwd()
            to_directory = path_temp
            os.chdir(to_directory)
            out.extractall(".")
            out.close()
            path_temp = '/omd/daemon/mysql_temp/%s_%s' % (year, month)
            path_sh = '/omd/daemon/mysql_scripts/mysql_restore.sh'
            proc = subprocess.Popen(['sh', path_sh, path_temp, db_backup,
                                     cur_db], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, err = proc.communicate()
            buf_data = output
            # code = proc.wait()
            # bufData = proc.stdout.read()
            return buf_data
        except Exception, e:
            return str(e)

    def create_backup(self, month_var):
        """

        @param month_var:
        @return:
        """
        try:
            month_var = month_var.split('_')
            year = month_var[0]
            month = month_var[1]
            cur_db = SystemConfig.get_mysql_credentials()[3]
            #            cur_db="nmsp"
            path_backup = '/omd/daemon/mysql_backup'
            path_temp = '/omd/daemon/mysql_temp/%s_%s' % (year, month)
            str_time = " timestamp between '%s-%s-01 00:00:00' and '%s-%s-31 23:59:59'  " % (
                year, month, year, month)
            path_sh = '/omd/daemon/mysql_scripts/mysql_backup.sh'
            proc = subprocess.Popen(['sh', path_sh, path_temp, str(
                str_time), cur_db], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, err = proc.communicate()
            buf_data = output
            # code = proc.wait()
            # bufData = proc.stdout.read()
            dstfolder = path_backup  # where backup will be stored
            fileorfolder = path_temp  # which file you want backup of
            #	    time.sleep(5)
            dst = '%s.tar.bz2' % os.path.join(
                dstfolder, os.path.basename(fileorfolder))
            out = tarfile.TarFile.open(dst, 'w:bz2')
            out.add(fileorfolder, arcname=os.path.basename(fileorfolder))
            out.close()
            return "done"
        except Exception, e:
            return str(e)

    def cleanup_data_historical(self, month_var):
        """

        @param month_var:
        @return:
        """
        try:
            month_var = month_var.split('_')
            year = month_var[0]
            month = month_var[1]
            cur_db = SystemConfig.get_mysql_credentials()[3]
            str_time = " where timestamp between '%s-%s-01 00:00:00' and '%s-%s-31 23:59:59' " % (
                year, month, year, month)
            path_sh = '/omd/daemon/mysql_scripts/mysql_remove_data.sh'
            proc = subprocess.Popen(['sh', path_sh, str_time, cur_db],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, err = proc.communicate()
            buf_data = output
            # code = proc.wait()
            # bufData = proc.stdout.read()
            return {'success': 0, 'result': 0}
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def backup_data_check_historical(self, month_var):
        """

        @param month_var:
        @return:
        """
        try:
            filename = '/omd/daemon/mysql_backup/%s.tar.bz2' % (month_var)
            if os.path.isfile(filename):
                return {'success': 0, 'result': filename}
            else:
                return {'success': 1, 'result': filename}
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def backup_data_historical(self, month_var):
        """

        @param month_var:
        @return:
        """
        try:
            result = self.create_backup(month_var)
            if result == "done":
                return {'success': 0, 'result': 0}
            else:
                return {'success': 1, 'result': str(result)}

        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def check_db_status_historical(self, user_id):
        """

        @param user_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            time.sleep(1)
            sql = "select status from historical_info where user_id='%s' " % (
                user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            db.close()
            if result != ():
                return {'success': 0, 'result': str(result[0][0])}
            else:
                return {'success': 0, 'result': '5'}
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def update_db_status_historical(self, user_id):
        """

        @param user_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "update historical_info set status=3 where user_id='%s' " % (
                user_id)
            cursor.execute(sql)
            db.commit()
            db.close()
            return {'success': 0, 'result': '0'}
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def set_last_access_time_historical(self, user_id):
        """

        @param user_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "update historical_info set last_access_time='%s' where user_id='%s' " % (
                datetime.now(), user_id)
            cursor.execute(sql)
            db.commit()
            db.close()
            return {'success': 0, 'result': '0'}
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def get_year_month_historical(self, user_id):
        """

        @param user_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "select `year_month` from historical_info where user_id='%s' " % (
                user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            db.close()
            if result != ():
                return result[0][0]
            else:
                return '2011_11'
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def clear_data_historical(self, user_id):
        """

        @param user_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "select database_name from historical_info where user_id='%s' " % (
                user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result != ():
                try:
                    db_name = result[0][0]
                    sql = "delete from historical_info where user_id='%s' " % (
                        user_id)
                    cursor.execute(sql)
                    db.commit()
                    db.select_db(db_name)
                    sql = "DROP DATABASE %s " % (db_name)
                    cursor.execute(sql)
                    db.commit()
                    db.close()
                except Exception, e:
                    pass
            else:
                sql = "delete from historical_info where user_id='%s' " % (
                    user_id)
                cursor.execute(sql)
                db.commit()
                db.close()
            return {'success': 0, 'result': 0}
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def get_year_month_status_historical(self, user_id):
        """

        @param user_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "select `year_month`,status from historical_info where user_id='%s' " % (
                user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            db.close()
            if result != ():
                return result
            else:
                return ''
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    def history_reporting_make_db(self, user_id, user_name, month_var, db_name):
        """

        @param user_id:
        @param user_name:
        @param month_var:
        @param db_name:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "DELETE FROM historical_info where user_id='%s' " % (user_id)
            cursor.execute(sql)
            db.commit()
            filename = '/omd/daemon/mysql_backup/%s.tar.bz2' % (month_var)
            if os.path.isfile(filename) == False:
                return {'success': 5, 'result': filename}
            sql = "INSERT INTO historical_info (historical_info_id, user_id, user_name, database_name, `year_month`, start_time, status, last_access_time) VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s')" % (
                user_id, user_name, db_name, month_var, datetime.now(), 0, datetime.now())
            cursor.execute(sql)
            db.commit()
            res = self.restore_backup(month_var, db_name)

            if res.find("ok") != -1:
                sql = "UPDATE historical_info set status=1 , last_access_time='%s' where user_id='%s' " % (
                    datetime.now(), user_id)
                cursor.execute(sql)
                db.commit()
                db.close()
                return {'success': 0, 'result': '1', 'data': str(res)}
            else:
                sql = "UPDATE historical_info set status=2 , last_access_time='%s' where user_id='%s' " % (
                    datetime.now(), user_id)
                cursor.execute(sql)
                db.commit()
                db.close()
                return {'success': 0, 'result': res}
        except Exception, e:
            return {'success': 1, 'result': str(e)}

    # get sql data using query dict
    def get_sql_data(self, query_dict, date_temp_1, date_temp_2, db_historical):
        """

        @param query_dict:
        @param date_temp_1:
        @param date_temp_2:
        @param db_historical:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            db.select_db(db_historical)
            cursor = db.cursor()
            date1 = datetime.strptime(date_temp_1, "%Y-%m-%d %H:%M:%S")
            date2 = datetime.strptime(date_temp_2, "%Y-%m-%d %H:%M:%S")
            nw = datetime.now()
            sql = ""
            # if nw.month==date1.month and nw.month==date2.month:
            #    sql="( select %s from %s %s %s %s %s )"%(query_dict["columns"],query_dict["table_name"],query_dict["join"],query_dict["where"],query_dict["group_by"],query_dict["order_by"])
            #    cursor.execute(sql)
            #    result=cursor.fetchall()
            # elif nw.month>date1.month:
            #    sql2="( select %s from history_%s %s %s %s %s )"%(query_dict["columns"],query_dict["table_name"].strip(),query_dict["join"],query_dict["where"],query_dict["group_by"],query_dict["order_by"])
            #    cursor.execute(sql2)
            #    res1=cursor.fetchall()
            #    if nw.month==date2.month:
            #        sql="( select %s from %s %s %s %s %s )"%(query_dict["columns"],query_dict["table_name"],query_dict["join"],query_dict["where"],query_dict["group_by"],query_dict["order_by"])
            #        cursor.execute(sql)
            #        res2=cursor.fetchall()
            #        result=res1+res2
            #    else:
            #       result=res1
            sql = "( select %s from %s %s %s %s %s )" % (
            query_dict["columns"], query_dict["table_name"], query_dict["join"], query_dict[
                "where"], query_dict["group_by"], query_dict["order_by"])
            cursor.execute(sql)
            result = cursor.fetchall()
            li_result = []
            for row in result:
                li_result.append(make_list(row))
            result_dict = {"success": "0", "result": li_result}
            db.close()
            return result_dict
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

        # get selected columns and non selected columns from report template

    def history_reporting_get_column_template(self, device_type_id, report_type, db_historical):
        """

        @param device_type_id:
        @param report_type:
        @param db_historical:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            db.select_db(db_historical)
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

    def history_reporting_get_mapping_column(self, device_type_id, report_type, db_historical):
        """

        @param device_type_id:
        @param report_type:
        @param db_historical:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            db.select_db(db_historical)
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
    def get_query_dict(self, device_type, report_type, date_temp_1, date_temp_2, all_host, db_historical):
        """

        @param device_type:
        @param report_type:
        @param date_temp_1:
        @param date_temp_2:
        @param all_host:
        @param db_historical:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            db.select_db(db_historical)
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
    def get_hostgroup_device(self, user_id, hostgroup_id_list, db_historical):
        """

        @param user_id:
        @param hostgroup_id_list:
        @param db_historical:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            conn.select_db(db_historical)
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
    def history_reporting_get_host_data(self, hostgroup_id, device_type_id, db_historical):
        """

        @param hostgroup_id:
        @param device_type_id:
        @param db_historical:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            conn.select_db(db_historical)
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

    def form_the_default_data(self, inpt, start_index, end_index, default_value, do_repeat):
        """

        @param inpt:
        @param start_index:
        @param end_index:
        @param default_value:
        @param do_repeat:
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
                    if count == (end_index - start_index):
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

    def get_description(self, all_host, db_historical):
        """

        @param all_host:
        @param db_historical:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            db.select_db(db_historical)
            cursor = db.cursor()
            sql = "SELECT host_alias FROM hosts WHERE host_id IN ('%s')" % (
                "' , '".join(all_host.split(',')))
            cursor.execute(sql)
            result = cursor.fetchall()
            desc = " report generated for  "
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

            return {"success": 1, "result": str(e)}
        except Exception, e:
            return {"success": 1, "result": str(e)}

    # common function for all reports
    # def history_reporting_get_excel(self,date1,date2,time1,time2,all_host,report_type,column_user,device_type,all_group,
    # view_type,i_display_start,i_display_length,s_search,sEcho,sSortDir_0,iSortCol_0,new_user_report_dict,db_historical,username):
    # common function for all reports
    def history_reporting_get_excel(
            self, date1, date2, time1, time2, all_host, report_type, column_user, device_type, all_group,
            view_type, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, new_user_report_dict,
            db_historical, username):
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
        @param db_historical:
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
            # creating the object
            re = HistoryReportBll()
            #	   getting values column_selected,column_non_selected,mapping_selected,mapping_non_selected
            # sheet_name,main_title,second_title,report_name,generate_method
            result_columns = re.history_reporting_get_mapping_column(
                device_type, report_type, db_historical)
            column_value = []
            column_key = []
            key_user = []
            data_report = {}
            data_report["success"] = "0"
            if (result_columns["success"] == 0 or result_columns["success"] == "0"):
                # get columns name for both selected & non selected
                column_value = result_columns["result"][0].split(",")
                column_value += result_columns["result"][1].split(",")
                # get table column  names for both selected &  non selected
                column_key = result_columns["result"][2].split(";")
                column_key += result_columns["result"][3].split(";")
                # for i in range column in table if user selected the column
                # then add in key_user
                for i in range(len(column_user)):
                    if (column_value.count(column_user[i]) >= 1):
                        index = column_value.index(column_user[i])
                        key_user.append(column_key[index])
                    # we use key_user for generating sql query only
                # but we use column_user for generating report headings
                if (str(result_columns["result"][8]) == '1'):
                    different_report = 1
                    # generate method for network outage
                    if (report_type.upper() == "NETWORK OUTAGE" or report_type.upper() == "DEVICE REACHABILITY"):
                        # outage_data=report_obj.get_total_data_network_outage(3000,date1,date2,time1,time2,all_group,all_host)
                        outage_data = get_outage(3000, date1, date2, time1,
                                                 time2, all_group, all_host, db_historical)
                        if (str(outage_data["success"]) == "0"):
                            inpt = deepcopy(outage_data["result"])
                        else:
                            return outage_data
                    elif (report_type.upper() == "TRAP" or report_type.upper() == "EVENTS"):
                        # report_obj=UbrReportBll()
                        # trap_data=report_obj.get_total_data_trap(3000,date1,date2,time1,time2,all_group,all_host)
                        trap_data = get_total_data_trap(
                            3000, date1, date2, time1,
                            time2, all_group, all_host, db_historical)
                        if (str(trap_data["success"]) == "0"):
                            inpt = deepcopy(trap_data["result"])
                        else:
                            return trap_data
                else:
                    different_report = 0
                    # not a special report ... follow the steps
                    # 1 . find the query dict corresponding to this report
                    query_dict = re.get_query_dict(device_type, report_type,
                                                   date_temp_1, date_temp_2, all_host, db_historical)
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
                            if flag_dict == True:
                                res_sql = dict_shelve_data["res_sql"]
                                dict_shelve.close()
                                dict_shelve_data.close()
                            else:
                                res_sql = re.get_sql_data(
                                    query_dict["result"], date_temp_1, date_temp_2, db_historical)
                                dict_shelve_data["res_sql"] = res_sql
                                dict_shelve[
                                    "user_info_dict"] = new_user_report_dict
                                dict_shelve.close()
                                dict_shelve_data.close()
                        else:
                            res_sql = re.get_sql_data(
                                query_dict["result"], date_temp_1, date_temp_2, db_historical)
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
                                res_delta = re.get_delta_for_values(data_report, int(
                                    var_delta[0]), int(var_delta[1]), int(var_delta[2]), int(var_delta[3]),
                                                                    int(var_delta[4]), int(var_delta[5]),
                                                                    int(var_delta[6]))
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
                                res_default = re.form_the_default_data(
                                    data_report, int(var_default[0]), int(var_default[1]), int(var_default[2]),
                                    int(var_default[3]))
                                if (str(res_default["success"]) == "0"):
                                    data_report = res_default["result"]
                                else:
                                    return res_default  # for exception
                                    #######################################-----END DELTA
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
                                  #"datstart":i_display_start,"dataend":int(i_display_start)+int(i_display_length),
                                  "sEcho": int(sEcho), "iTotalRecords": len(report_data_list2),
                                  "iTotalDisplayRecords": len(report_data_list2)}
                        return status
                    else:
                        # report_data_list=inpt
                        # status={"success":0,"aaData":report_data_list2[int(i_display_start):int(i_display_start)+int(i_display_length)],
                        #		"sEcho":int(sEcho),"iTotalRecords":len(report_data_list2),"iTotalDisplayRecords":len(report_data_list2)}
                        # return status
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
                                  #"datstart":i_display_start,"dataend":int(i_display_start)+int(i_display_length),
                                  "sEcho": int(sEcho), "iTotalRecords": len(report_data_list2),
                                  "iTotalDisplayRecords": len(report_data_list2)}
                        return status
                        # else:
                        #    status={"success":0,"aaData":report_data_list,
                        #			"sEcho":int(sEcho),"iTotalRecords":len(report_data_list),"iTotalDisplayRecords":len(report_data_list)}
                        # return status
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
                        desc = self.get_description(all_host, db_historical)
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
                        desc = self.get_description(all_host, db_historical)
                        if str(desc["success"]) == "0":
                            el.log_event("Excel " + desc["result"], username)
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
                dat1 = date1.replace("/", "_")
                dat2 = date2.replace("/", "_")
                dat1 = dat1 + "(" + time1 + ")"
                dat2 = dat2 + "(" + time2 + ")"
                name_report = main_title + "_" + dat1 + dat2 + "_excel.xls"
                if data_report == []:
                    continue
                else:
                    flag = 1
                xls_sheet = xls_book.add_sheet(
                    sheet_name, cell_overwrite_ok=True)
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
                    for k in range(len(row)):
                        width = 5000
                        xls_sheet.write(i, k, str(row[k]), style1)
                        xls_sheet.col(k).width = width
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
                if data_report == []:
                    continue
                else:
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
            temp_ip = tpl[4]
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
                                main_list.append([leftout_date, tpl_temp[4],
                                                  tpl_temp[5], tpl_temp[6], timedelta(0, 86399), None])
                            elif prev_value == '50001':
                                main_list.append([leftout_date, tpl_temp[4],
                                                  tpl_temp[5], tpl_temp[6], None, timedelta(0, 86399)])

                else:
                    if temp_value == '50002':
                        if uptime is None:
                            uptime = (temp_date - main_date)
                        else:
                            uptime += (temp_date - main_date)

                    elif temp_value == '50001':
                        if downtime is None:
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
                if uptime is None or downtime is None:
                    mid_date = datetime(main_date.year,
                                        main_date.month, main_date.day, 23, 59, 59)
                    delta = mid_date - main_date
                    if prev_value == '50002':
                        uptime = delta
                    elif prev_value == '50001':
                        downtime = delta
                main_list.append([main_date, tpl_temp[4],
                                  tpl_temp[5], tpl_temp[6], uptime, downtime])
                main_date = temp_date
                uptime = None
                downtime = None
                is_date = 0

            prev_value = temp_value

        if uptime is None or downtime is None:
            mid_date = datetime(
                main_date.year, main_date.month, main_date.day, 23, 59, 59)
            delta = mid_date - main_date
            if prev_value == '50002':
                uptime = delta
            elif prev_value == '50001':
                downtime = delta
        main_list.append([main_date, tpl_temp[4], tpl_temp[5],
                          tpl_temp[6], uptime, downtime])

        day_diff = (end_date - main_date).days
        if day_diff > 1:
            for i in range(1, day_diff + 1):
                leftout_date = main_date + timedelta(days=i)
                if prev_value == '50002':
                    main_list.append([leftout_date, tpl_temp[4],
                                      tpl_temp[5], tpl_temp[6], timedelta(0, 86399), None])
                elif prev_value == '50001':
                    main_list.append([leftout_date, tpl_temp[4],
                                      tpl_temp[5], tpl_temp[6], None, timedelta(0, 86399)])
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


def get_outage(no_of_devices, date1, date2, time1, time2, all_group, all_host, db_historical):
    """

    @param no_of_devices:
    @param date1:
    @param date2:
    @param time1:
    @param time2:
    @param all_group:
    @param all_host:
    @param db_historical:
    @return:
    """
    try:
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        conn.select_db(db_historical)
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
                    if i[-2] is None:
                        uptime = 0
                    else:
                        uptime = i[-2].seconds
                    if i[-1] is None:
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
        conn.close()
        return result_dict
    except Exception, e:
        main_dict = {}
        main_dict['success'] = 1
        main_dict['result'] = str(e)
        return main_dict

# TOTAL TRAP DATA FOR A GIVEN DATE PERIOD BY SERVITY


def get_total_data_trap(no_of_devices, date1, date2, time1, time2, all_group, all_host, db_historical):
    """

    @param no_of_devices:
    @param date1:
    @param date2:
    @param time1:
    @param time2:
    @param all_group:
    @param all_host:
    @param db_historical:
    @return:
    """
    try:
        conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        conn.select_db(db_historical)
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
            lst = [0, 0, 0, 0, 0, 0]
            while (str(res[i][1]) == str(res[i + 1][1]) and str(res[i][0]) == str(res[i + 1][0]) and (i < length - 1)):
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
