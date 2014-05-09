#!/usr/bin/python2.6

"""
@author: Mahipal Choudhary
@since: 07-Dec-2011
@version: 0.1
@note: All database related functions Related log management.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""

# Import modules that contain the function and libraries
import MySQLdb
import xlwt
import csv
from unmp_config import SystemConfig
from common_bll import EventLog
from datetime import datetime
from common_vars import make_list


class Log_bll(object):
    """
    User logs related Model class
    """
# Required data for given user_id
    def get_log_data_bll(self, sEcho, iColumns, iDisplayLength, iDisplayStart, sColumns, sSearch, iSortCol_0,
                         sSortDir_0, month, log_type, selected_user, group="", date_start="", date_end="",
                         time_start="", time_end=""):
        """

        @param sEcho:
        @param iColumns:
        @param iDisplayLength:
        @param iDisplayStart:
        @param sColumns:
        @param sSearch:
        @param iSortCol_0:
        @param sSortDir_0:
        @param month:
        @param log_type:
        @param selected_user:
        @param group:
        @param date_start:
        @param date_end:
        @param time_start:
        @param time_end:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            a_columns = ["timestamp", "time_taken", "username", "description"]
            s_table = "event_log"
            s_index_column = "timestamp"
            # query="Select timestamp, username , description from event_log
            # order by timestamp desc"
            s_limit = ""
            # iDisplayLength,iDisplayStart
            if (iDisplayStart != None and iDisplayLength != '-1'):
                s_limit = "LIMIT %s, %s" % (MySQLdb.escape_string(
                    iDisplayStart), MySQLdb.escape_string(iDisplayLength))
                # Ordering
            # s_order = "ORDER BY timestamp desc,  "
            s_order = "ORDER BY  "
            if iSortCol_0 != None and iSortCol_0 != -1:
                s_order += "%s %s, " % (" 0 + " + a_columns[int(iSortCol_0)] if a_columns[int(
                    iSortCol_0)] == "time_taken" else a_columns[int(iSortCol_0)], sSortDir_0)
                s_order = s_order[:-2]

                # Filtering
            s_where = ""
            if sSearch != "":
                s_where = "WHERE ("
                for i in range(0, len(a_columns)):
                    s_where += "%s LIKE '%%%s%%' OR " % (
                        a_columns[i], MySQLdb.escape_string(sSearch))
                s_where = s_where[:-3]
                s_where += ")"
            if month != "" and month != None and month != "all":
                if str(month) == "20":
                    dat1 = date_start.replace("/", "-")
                    dat2 = date_end.replace("/", "-")
                    dat1 = dat1 + " " + time_start
                    dat2 = dat2 + " " + time_end
                    d1 = datetime.strptime(dat1, "%d-%m-%Y %H:%M")
                    d2 = datetime.strptime(dat2, "%d-%m-%Y %H:%M")
                    date_temp_1 = str(d1)
                    date_temp_2 = str(d2)
                else:
                    month = month.split('_')
                    date_temp_1 = month[0] + "-" + month[1] + "-01 00:00:00"
                    date_temp_2 = month[0] + "-" + month[1] + "-31 23:59:59"
                if s_where == "":
                    s_where = " where timestamp between '%s' and '%s' " % (
                        date_temp_1, date_temp_2)
                else:
                    s_where += " and timestamp between '%s' and '%s' " % (
                        date_temp_1, date_temp_2)

            if log_type == "" or log_type == None:
                log_type = 0
            if log_type != "" and log_type != None and str(log_type) != "10":
                if s_where == "":
                    s_where = " where level='%s' " % (log_type)
                else:
                    s_where += " and level='%s' " % (log_type)
            if selected_user != "" and selected_user != None:
                if s_where == "":
                    s_where = " where username='%s' " % (selected_user)
                else:
                    s_where += " and username='%s' " % (selected_user)
            if group != "" and group != None and group != "superadmin" and group != "admin":
                if s_where == "":
                    s_where = " where level!='3' "
                else:
                    s_where += " and level!='3' "
            cursor = db.cursor()
            query_check = ""
            # SQL queries
            # Get data to display
            sql_query = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s" % (
                ", ".join(a_columns).replace(" , ", " "), s_table, s_where, s_order, s_limit)
            # create sql query - End
            # execute sql query
            query_check = sql_query
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
            sql_query = "SELECT COUNT(%s) FROM %s" % (s_index_column, s_table)

            # execute sql query
            cursor.execute(sql_query)

            # fetch data from executed sql query
            i_total = cursor.fetchone()[0]

            # close the cursor
            cursor.close()

            result_data = []
            for row in r_result:
                result_data.append(make_list(row))
                # Output
            output = {
                "sEcho": sEcho,
                "iTotalRecords": i_total,
                "iTotalDisplayRecords": i_filtered_total,
                "aaData": result_data,
                #"query":query_check
            }

            return output
        except Exception, e:
            output = {
                "sEcho": 0,
                "iTotalRecords": [],
                "iTotalDisplayRecords": [],
                "aaData": [],
                "exception": str(e)
            }

            # Encode Data into JSON
            return output
        finally:
            db.close()

    def get_header_data(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "Select timestamp, username , description from event_log where level=0 order by timestamp desc limit 5"
            cursor.execute(query)
            log_tuple = cursor.fetchall()
            log_list = []
            for row in log_tuple:
                log_list.append(make_list(row))
            return log_list
        except Exception, e:
            return []
        finally:
            conn.close()

    def get_device_type_dict(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "select device_type_id,device_name from device_type;"
            cursor.execute(query)
            log_tuple = cursor.fetchall()
            device_type_dict = {}
            for row in log_tuple:
                # log_list.append(make_list(row))
                device_type_dict[row[0]] = row[1]
            return device_type_dict
        except Exception, e:
            return {}
        finally:
            conn.close()

    def get_user_names(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "Select user_name from user_login"
            cursor.execute(query)
            user_tuple = cursor.fetchall()
            user_list = []
            for row in user_tuple:
                user_list.append(make_list(row))
            return user_list
        except Exception, e:
            return []
        finally:
            conn.close()

    def clear_old_logs(self):
        """


        @return:
        """
        try:
            from datetime import timedelta, datetime

            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "delete from event_log where timestamp <= '%s' " % (
                str(datetime.now() - timedelta(days=30))[:19])
            cursor.execute(query)
            conn.commit()
            return {"success": 0, "result": 1}
        except Exception, e:
            return {"success": 1, "result": str(e)}
        finally:
            conn.close()

    def get_alarm_header_data(self, hostgroup_id_list):
        """

        @param hostgroup_id_list:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "SELECT t.serevity,STR_TO_DATE(t.trap_receive_date,'%a %b %e %H:%i:%s %Y'),t.trap_event_type,t.event_id,h.device_type_id,h.host_alias,t.agent_id,t.description FROM \
    	    			    trap_alarm_current as t \
    	    			INNER JOIN hosts as h ON t.agent_id=h.ip_address \
				INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = h.host_id "
            query += "    	INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id WHERE  hostgroups.hostgroup_id IN (%s) \
				 order by t.trap_receive_date desc limit 5 " % (','.join(hostgroup_id_list))
            cursor.execute(query)
            log_tuple = cursor.fetchall()
            log_list = []
            for row in log_tuple:
                log_list.append(make_list(row))
            return log_list
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def get_log_data_report(self, month, log_type, report_type, username, selected_user, date_start, date_end,
                            time_start, time_end):
        """

        @param month:
        @param log_type:
        @param report_type:
        @param username:
        @param selected_user:
        @param date_start:
        @param date_end:
        @param time_start:
        @param time_end:
        @return:
        """
        try:
            time1 = datetime.now()
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system

            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            s_where = ""
            if month != "" and month != None and month != "all":
                if str(month) == "20":
                    dat1 = date_start.replace("/", "-")
                    dat2 = date_end.replace("/", "-")
                    dat1 = dat1 + " " + time_start
                    dat2 = dat2 + " " + time_end
                    d1 = datetime.strptime(dat1, "%d-%m-%Y %H:%M")
                    d2 = datetime.strptime(dat2, "%d-%m-%Y %H:%M")
                    date_temp_1 = str(d1)
                    date_temp_2 = str(d2)
                else:
                    month = month.split('_')
                    date_temp_1 = month[0] + "-" + month[1] + "-01 00:00:00"
                    date_temp_2 = month[0] + "-" + month[1] + "-31 23:59:59"
                if s_where == "":
                    s_where = " where timestamp between '%s' and '%s' " % (
                        date_temp_1, date_temp_2)
                else:
                    s_where += " and timestamp between '%s' and '%s' " % (
                        date_temp_1, date_temp_2)

            if log_type == "" or log_type == None:
                log_type = 0
            if log_type != "" and log_type != None and str(log_type) != "10":
                if s_where == "":
                    s_where = " where level='%s' " % (log_type)
                else:
                    s_where += " and level='%s' " % (log_type)
            if selected_user != "" and selected_user != None:
                if s_where == "":
                    s_where = " where username='%s' " % (selected_user)
                else:
                    s_where += " and username='%s' " % (selected_user)

            query = "Select timestamp, time_taken, username , description from event_log %s order by timestamp desc" % (
                s_where)
            cursor.execute(query)
            log_tuple = cursor.fetchall()
            log_list = []
            for row in log_tuple:
                log_list.append(make_list(row))

            if report_type == "csv":
                sheet_dict = {
                    "sheet_name": "Log report",
                    "main_title": "Log report",
                    "second_title": "",
                    "headings": ["Time", "Time taken (in sec)", "Username", "Description"],
                    "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                    "name_report": "log_report.csv",
                    "data_report": log_list,
                }
                status = self.get_csv_file(sheet_dict)
                el = EventLog()
                desc = "CSV report generated for logs  "
                el.log_event(desc, username)
                return status
            else:
                sheet_dict = {
                    "sheet_name": "Log report",
                    "main_title": "Log report",
                    "second_title": "",
                    "headings": ["Time", "Time taken (in sec)", "Username", "Description"],
                    "path_report": '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance,
                    "name_report": "log_report.xls",
                    "data_report": log_list,
                }
                status = self.get_excel_sheet(sheet_dict)
                el = EventLog()
                desc = "Excel report generated for logs  "
                el.log_event(desc, username)
                return status
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
                if data_report == []:
                    continue
                else:
                    flag = 1
                sheet_no = 1
                xls_sheet = xls_book.add_sheet(
                    str(sheet_name) + str(sheet_no), cell_overwrite_ok=True)
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
