#!/usr/bin/python2.6
"""
@author: Mahipal Choudhary
@since: 07-Nov-2011
@version: 0.1
@note: All database related functions Related with analyzed Reporting.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""
from copy import deepcopy
import csv
from datetime import datetime
import os
import subprocess
import tarfile
import time

import MySQLdb
import xlwt
from common_bll import EventLog
from common_vars import make_list
from unmp_config import SystemConfig
from defaults import site as nms_instance


def create_backup():
    """


    @return:
    """
    try:
        ye = datetime.now().year
        mon = datetime.now().month
        mon = mon - 1
        if mon <= 0:
            ye = ye - 1
            mon = -mon
            mon = 12 - mon
        path_backup = '/omd/daemon/mysql_backup'
        path_temp = '/omd/daemon/mysql_temp/%s_%s' % (ye, mon)
        str_time = "timestamp between '%s-%s-01 00:00:00' and '%s-%s-31 23:59:59' " % (
            ye, mon, ye, mon)
        path_sh = '/omd/sites/%s/share/check_mk/web/htdocs/mysql_backup.sh %s %s' % (
            nms_instance, path_temp, str_time)
        subprocess.Popen("sh %s" % path_sh, shell=True)
        dstfolder = path_backup  # where backup will be stored
        fileorfolder = path_temp  # which file you want backup of
        time.sleep(5)
        dst = '%s.tar.bz2' % os.path.join(
            dstfolder, os.path.basename(fileorfolder))
        out = tarfile.TarFile.open(dst, 'w:bz2')
        out.add(fileorfolder, arcname=os.path.basename(fileorfolder))
        out.close()
        return "done"
    except Exception, e:
        return str(e)


def restore_backup():
    """


    @return:
    """
    try:
        ye = datetime.now().year
        mon = datetime.now().month
        mon = mon - 1
        if mon <= 0:
            ye = ye - 1
            mon = -mon
            mon = 12 - mon
        path_backup = '/omd/daemon/mysql_backup/%s_%s.tar.bz2' % (ye, mon)
        path_temp = '/omd/daemon/mysql_temp/'
        dst = path_backup  # where backup will be stored
        fileorfolder = path_backup  # which file you want backup of
        out = tarfile.TarFile.open(dst, 'r:bz2')
        cwd = os.getcwd()
        to_directory = path_temp
        os.chdir(to_directory)
        out.extractall(".")
        out.close()
        path_temp = '/omd/daemon/mysql_temp/%s_%s' % (ye, mon)
        path_sh = '/omd/sites/%s/share/check_mk/web/htdocs/mysql_restore.sh %s' % (
            nms_instance, path_temp)
        subprocess.Popen("sh %s" % path_sh, shell=True)
        return "done"
    except Exception, e:
        return str(e)

# print create_backup()
# print restore_backup()


class AnalyzedReportBll(object):
    """
    get sql data using query dict
    """
    def get_sql_data(self, query_dict):
        """

        @param query_dict:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select %s from %s %s %s %s %s" % (
            query_dict["columns"], query_dict["table_name"], query_dict["join"], query_dict[
                "where"], query_dict["group_by"], query_dict["order_by"])
            cursor.execute(sql)
            li_result = [make_list(row) for row in cursor.fetchall()]
            cursor.close()
            db.close()
            result_dict = {"success": "0", "result": li_result}
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(sql)}
        finally:
            return result_dict

    # get selected columns and non selected columns from report template
    def analyzed_reporting_get_column_template(self, device_type_id, report_type):
        """

        @param device_type_id:
        @param report_type:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select column_selected,column_non_selected from report_template_analyzed where device_type='%s' and report_type='%s' " % (
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

    # get selected columns and non selected columns from report template
    def analyzed_reporting_get_column_range(self, device_type_id, report_type, range_type):
        """

        @param device_type_id:
        @param report_type:
        @param range_type:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            if (str(range_type) == "1"):
                range_type = "Minimum"
            elif (str(range_type) == "2"):
                range_type = "Maximum"
            elif (str(range_type) == "3"):
                range_type = "Average"
            elif (str(range_type) == "4"):
                range_type = "Total"
            elif (str(range_type) == "5"):
                range_type = "All"
                # if(report_type=="RSSI" and range_type=="Average"):
            #	range_type="Range"
            sql = " select column_selected,column_non_selected from report_template_analyzed where device_type='%s' and report_type='%s' and type='%s' " % (
                device_type_id, report_type, range_type)
            cursor = db.cursor()
            if cursor.execute(sql):
                result = cursor.fetchall()
                lis = [result[0][0], result[0][1]]
            else:
                lis = []
            cursor.close()
            db.close()
            result_dict = {"success": "0", "result": lis}
            return result_dict
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(sql)}
            return result_dict

    # get all data from report template for given device type and report type
    def analyzed_reporting_get_mapping_column(self, device_type_id, report_type, range_type):
        """

        @param device_type_id:
        @param report_type:
        @param range_type:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select column_selected,column_non_selected,mapping_selected,mapping_non_selected, \
                  sheet_name,main_title,second_title,report_name,generate_method from report_template_analyzed where device_type='%s' and report_type='%s' and type='%s'" % (
            device_type_id, report_type, range_type)
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            db.close()
            lis = []
            # return sql
            if len(result) > 0:
                for i in range(len(result[0])):
                    lis.append(result[0][i])
            result_dict = {"success": "0", "result": lis}
            return result_dict
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(e)}
            return result_dict

    # get a query dict for diven data
    def get_query_dict(self, device_type, report_type, date_temp_1, date_temp_2, all_host, range_type, range_duration):
        """

        @param device_type:
        @param report_type:
        @param date_temp_1:
        @param date_temp_2:
        @param all_host:
        @param range_type:
        @param range_duration:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            if ((report_type == "RSSI" or report_type == "RSL") and range_type == "Average"):
                range_type = "Total"
            sql = " select * from report_query_dict_analyzed where report_type='%s' and device_type='%s' and range_type='%s'" % (
                report_type, device_type, range_type)
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            query_dict = {
                "table_name": result[0][5],
                "columns": result[0][4],
                "join": result[0][6],
                "where": str(result[0][7]) % (
                date_temp_1, date_temp_2, "' , '".join(all_host.split(',')), range_duration),
                "group_by": result[0][8],
                "order_by": result[0][9],
            }
            result_dict = {"success": "0", "result": query_dict}
            db.close()
            return result_dict
        except Exception, e:
            db.close()
            result_dict = {"success": "1", "result": str(sql)}
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
            query2 = "SELECT device_type,report_Type FROM `report_template_analyzed` group by device_type,report_type order by device_type,report_type"
            cursor.execute(query2)
            di = {}
            li = []
            for t in cursor.fetchall():
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
            cursor.close()
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

    # get host data ie device name and host id
    def analyzed_reporting_get_host_data(self, hostgroup_id, device_type_id):
        """

        @param hostgroup_id:
        @param device_type_id:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "select h.host_id,host_alias from hosts_hostgroups  as hhg \
			join (select host_id,device_type_id,host_name,host_alias from hosts where is_deleted = 0) as h on h.host_id=hhg.host_id \
			where hhg.hostgroup_id='%s' and h.device_type_id='%s' order by h.host_name" % (hostgroup_id, device_type_id)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            result_dict = {"success": 0, "result": result}
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

    def pagination_create_table(self, query_dict, i_display_start, i_display_length, s_search, sEcho, req_vars):
        """

        @param query_dict:
        @param i_display_start:
        @param i_display_length:
        @param s_search:
        @param sEcho:
        @param req_vars:
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
        # sql=" select %s from %s %s %s %s
        # %s"%(query_dict["columns"],query_dict["table_name"],query_dict["join"],query_dict["where"],query_dict["group_by"],query_dict["order_by"])
        try:
            # sql = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s" % (" , ".join(a_columns),s_table,s_join,s_where,s_group_by,s_order)#,s_limit)
            # i_total=cursor.execute(sql)
            s_limit = ""
            # Ordering
            s_limit = ""
            i_display_start = req_vars.get("iDisplayStart", 0)
            i_display_length = req_vars.get("iDisplayLength", 0)
            if (i_display_start != None and i_display_length != '-1'):
                s_limit = "LIMIT %s, %s" % (MySQLdb.escape_string(
                    i_display_start), MySQLdb.escape_string(i_display_length))

            # Ordering
            i_sort_col_0 = req_vars.get("iSortCol_0", None)
            if i_sort_col_0 != None:
                s_order = "ORDER BY  "
                for i in range(0, int(req_vars.get("iSortingCols", 0))):
                    i_sort_col_i = int(req_vars.get("iSortCol_%s" % i, -1))
                    b_sortable_ = req_vars.get(
                        "bSortable_%s" % i_sort_col_i, None)
                    if b_sortable_ == "true":
                        s_sort_dir_i = req_vars.get("sSortDir_%s" % i, "asc")
                        s_order += "%s %s, " % (
                            a_columns[i_sort_col_i], MySQLdb.escape_string(s_sort_dir_i))

                s_order = s_order[:-2]
                if s_order == "ORDER BY":
                    s_order = ""

            # Filtering
            # s_where = "";
            s_search = req_vars.get("sSearch", None)
            if s_search != None:
                s_where += "AND ("
                for i in range(0, len(a_columns)):
                    s_where += "%s LIKE '%%%s%%' OR " % (
                        a_columns[i], MySQLdb.escape_string(s_search))
                s_where = s_where[:-3]
                s_where += ")"

            # Individual column filtering
            for i in range(0, len(a_columns)):
                b_searchable_i = req_vars.get("bSearchable_%s" % i, None)
                s_search_i = req_vars.get("sSearch_%s" % i, "")
                if (b_searchable_i == "true" and s_search_i != ""):
                    if s_where == "":
                        s_where = "WHERE "
                    else:
                        s_where += " AND "
                    s_where += "%s LIKE '%%%s%%' " % (
                        a_columns[i], MySQLdb.escape_string(s_search_i))

            # prepare a cursor object using cursor() method
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()

            # SQL queries
            # Get data to display
            sql_query = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s" % (
                ", ".join(a_columns).replace(" , ", " "), s_table, s_join, s_where, s_order, s_limit)
            # return sql_query
            sql_query22 = sql_query
            # create sql query - End
            # execute sql query
            cursor.execute(sql_query)

            # fetch data from executed sql query
            r_result = cursor.fetchall()

            # close the cursor
            cursor.close()

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            # Data set length after filtering
            sql_query = "SELECT FOUND_ROWS()"

            # execute sql query
            cursor.execute(sql_query)

            # fetch data from executed sql query
            i_filtered_total = cursor.fetchone()[0]

            # close the cursor
            cursor.close()

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            # Total data set length
            sql_query = "SELECT COUNT(%s) FROM %s %s %s " % (
                s_index_column, s_table, s_join, s_where)

            # execute sql query
            cursor.execute(sql_query)

            # fetch data from executed sql query
            i_total = cursor.fetchone()[0]

            # close the cursor
            cursor.close()

            result_data = []
            if (r_result != ()):
                for a_row in r_result:
                    row = []
                    for i in a_row:
                        row.append(str(i))
                    result_data.append(list(row))

            output = {
                "success": 0,
                "sEcho": int(req_vars.get("sEcho", 0)),
                "iTotalRecords": int(i_total), # i_filtered_total,#i_total,
                "iTotalDisplayRecords": int(i_filtered_total), # i_filtered_total,
                "aaData": result_data,
                "result": result_data,
                "sql": sql_query22
            }
            db.close()
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
                "exception": str(sql_query22)
            }
            return output

    def get_description(self, all_host):
        """

        @param all_host:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "SELECT host_alias FROM hosts WHERE host_id IN ('%s')" % (
                "' , '".join(all_host.split(',')))
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            desc = " report generated for  "
            len_host = 0
            if result != ():
                for i in result:
                    len_host += 1
                    desc += str(i[0]) + " , "
                    if len_host > 5:
                        desc += " and others , "
                        break
                desc = desc[:-2]
                return {"success": 0, "result": desc}

            return {"success": 1, "result": str(e)}
        except Exception, e:
            return {"success": 1, "result": str(e)}

    # common function for all reports
    def analyzed_reporting_get_excel(self, date1, date2, time1, time2, all_host, report_type, column_user, device_type,
                                     all_group, view_type, range_type, range_duration, i_display_start,
                                     i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, html_req, username):
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
        @param range_type:
        @param range_duration:
        @param i_display_start:
        @param i_display_length:
        @param s_search:
        @param sEcho:
        @param sSortDir_0:
        @param iSortCol_0:
        @param html_req:
        @param username:
        @return:
        """
        try:
            direct = ""
            iTotalDisplayRecords = 0
            iTotalRecords = 0
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
            analyzed_repo = AnalyzedReportBll()
            #	   getting values column_selected,column_non_selected,mapping_selected,mapping_non_selected
            # sheet_name,main_title,second_title,report_name,generate_method
            result_columns = analyzed_repo.analyzed_reporting_get_mapping_column(
                device_type, report_type, range_type)
            column_value = []
            column_key = []
            key_user = []
            data_report = {}
            data_report["success"] = "0"
            # return result_columns
            if (result_columns["success"] == 0 or result_columns["success"] == "0"):
                # get columns name for both selected & non selected
                column_value = result_columns["result"][0].split(",")
                if result_columns["result"][1] != "":
                    column_value += result_columns["result"][1].split(",")
                    # get table column  names for both selected &  non selected
                column_key = result_columns["result"][2].split(";")
                if result_columns["result"][3] != "":
                    column_key += result_columns["result"][3].split(";")
                    # for i in range column in table if user selected the column
                # then add in key_user
                for i in range(len(column_user)):
                    if (column_value.count(column_user[i]) >= 1):
                        index = column_value.index(column_user[i])
                        key_user.append(column_key[index])
                    # we use key_user for generating sql query only
                # but we use column_user for generating report headings
                if 1 == 1:
                    different_report = 0
                    # not a special report ... follow the steps
                    # 1 . find the query dict corresponding to this report
                    query_dict = analyzed_repo.get_query_dict(
                        device_type, report_type, date_temp_1, date_temp_2, all_host, range_type, range_duration)
                    if (str(query_dict["success"]) == "0"):
                        if view_type == "data_table":
                            res_sql = analyzed_repo.pagination_create_table(
                                query_dict["result"], i_display_start, i_display_length, s_search, sEcho, html_req)
                            # return res_sql
                        else:
                            res_sql = analyzed_repo.get_sql_data(query_dict["result"])
                        if (str(res_sql["success"]) == "0"):
                            if (view_type == "data_table"):
                                if (res_sql["result"] == []):
                                # status={"success":0,"aaData":[],
                                #"sEcho":int(sEcho),"iTotalRecords":res_sql["iTotalRecords"],"iTotalDisplayRecords":res_sql["iTotalDisplayRecords"]}
                                    status = {"success": 0, "aaData": [],
                                              "sEcho": 1, "iTotalRecords": 0, "iTotalDisplayRecords": 0}
                                    return status
                                data_report = res_sql["result"]
                                sEcho = res_sql["sEcho"]
                                iTotalRecords = res_sql["iTotalRecords"]
                                iTotalDisplayRecords = res_sql[
                                    "iTotalDisplayRecords"]
                            else:
                                data_report = res_sql["result"]
                        else:
                            return res_sql  # for exception
                            #######################################-----GROUP THE DATA
                        # common algo for all special reports
                    inpt = data_report
                given = deepcopy(column_value)
                req = deepcopy(key_user)
                outdata = []
                if req != given:
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
                else:
                    outdata = inpt
                report_data_list = outdata
                # if(data_report["success"]=="0"):
                if (view_type == "data_table"):
                    status = {"success": 0, "aaData": report_data_list,
                              #"datstart":i_display_start,"dataend":int(i_display_start)+int(i_display_length),
                              #"sEcho":int(sEcho),"iTotalRecords":len(report_data_list2),"iTotalDisplayRecords":len(report_data_list2)}
                              "sEcho": int(sEcho), "iTotalRecords": int(iTotalRecords),
                              "iTotalDisplayRecords": int(iTotalDisplayRecords)}
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
                    status = analyzed_repo.get_excel_sheet(sheet_dict)
                    if str(status["success"]) == "0":
                        el = EventLog()
                        # desc="Excel Report Generated for Hosts  "
                        desc = self.get_description(all_host)
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
                    status = analyzed_repo.get_csv_file(sheet_dict)
                    if str(status["success"]) == "0":
                        el = EventLog()
                        # desc="Excel Report Generated for Hosts  "
                        desc = self.get_description(all_host)
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
            result_dict = {"success": "0", "result":
                "report successfully generated", "file": name_report}
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
            result_dict = {"success": "0", "result":
                "report successfully generated", "file": name_report}
            return result_dict
        except Exception, e:
            result_dict = {"success": "1", "result": str(e)}
            return result_dict
