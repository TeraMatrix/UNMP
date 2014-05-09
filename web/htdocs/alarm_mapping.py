#!/usr/bin/python2.6

## import module
import os.path
import traceback
from datetime import datetime

import MySQLdb
import config
from mysql_collection import mysql_connection
from common_vars import make_list


global ap25, odu100, idu4, di, device_type_dict, severity_dict, ccu

ap25, odu100, idu4, ccu, di, device_type_dict, severity_dict = {}, {}, {
}, {}, {}, {}, {}

mapping_file = '/omd/daemon/mapping_alarm.rg'

if os.path.isfile(mapping_file):    # getting values of upper defined global variables from file
    execfile(mapping_file)

# import logging
# logging.basicConfig(filename='/omd/daemon/debug.log',format='%(levelname)s:
# %(asctime)s >> %(message)s', level=logging.DEBUG)

# ap25 = {'AP UP':1,'AP DOWN':2}
#
# odu100 = {'CRC_ERROR_THRESHOLD_EXCEEDED': 13203, 'CRC_ERROR_THRESHOLD_OK': 13206, 'DEFAULT_CONFIG_RESTORED': 13009, 'FLASH_COMMITED': 13010, 'FRAMES_RESTORED': 13209,
# 'FRAME_LOSS_THRESHOLD_EXCEEDED': 13204, 'FRAME_LOSS_THRESHOLD_OK': 13207, 'FRAME_LOSS_TIMEOUT': 13208, 'HEALTH_EVENT': 13012, 'HW_CONSISTENCY_ERROR': 13005,
# 'LINK_DOWN': 13002, 'LINK_UP': 13001, 'NEW_NODE': 13003, 'NODE_DOWN': 13015, 'NODE_LEAVE': 13014, 'NODE_UP': 13004, 'RU_LOCKING_EVENT': 13013,
# 'SLAVE_ON_SAME_TIMESLOT': 13011, 'SW_ACTIVATION_FAILED': 13008, 'SW_DOWNLOAD_COMPLETED': 13006, 'SW_DOWNLOAD_FAILED': 13007, 'SYNC_ACHIEVED': 13201,
# 'SYNC_LOSS_THRESHOLD_EXCEEDED': 13202, 'SYNC_LOSS_THRESHOLD_OK': 13205, 'SYNC_LOSS_TIMEOUT': 13200}
#
# idu4 = {'HOTSWAP' :12001, 'FACTORY_DEFAULT' :12002, 'HARDWARE_RESET' :12003, 'IMAGE_UPGRADE' :12004, 'UNKNOWN' :12005, 'WATCHDOG_RESET' :12006,
#'IMAGE_ACTIVATE' :12007, 'TU_LOCKED' :12050, 'TU_UNLOCKED' :12051, 'ETH_LINK' :12053,'INTERNAL_ERROR' :12066,'PORT_CLK_STATE' :12071,
#'PORT_CLK_CONV':12072, 'VOLTAGE_ERROR':12073, 'CPLD_CLOCK_SO':12074, 'CPLD_DATA_SO':12075, 'CPLD_COMBO_SO':12076, 'TEMP_CRITICAL':12079 }
#
# di = {'odu100':odu100,'idu4':idu4}
#
# device_type_dict={'odu100':'UBR/UBRe','idu4':'IDU 4 port'}
#
# severity_dict =
# {0:'Clear',1:'Informational',2:'Normal',3:'Minor',4:'Major',5:'Critical',9:'Default'}


def write_mask_file(tuple2d):
    """

    @param tuple2d:
    """
    if len(tuple2d) > 0:  # mask_dict = dict(zip(map(lambda x: x[0],tuple2d),map(lambda x: x[1],tuple2d))) other way
        if len(tuple2d[0]) == 7:
            mask_dict = {}
            mask_severity_dict = {}
            real_alarm_list = []
            clear_alarm_dict = {}
            odu16_mask_dict = {}
            odu16_mask_severity_dict = {}
            odu16_real_alarm_list = []
            odu16_clear_alarm_dict = {}

            for tp in tuple2d:
                if tp[6] != 'odu16':
                    mask_dict[tp[0]] = tp[1]
                    clear_alarm_dict[tp[1]] = tp[5]
                    # This is for clear event type dict.
                    if str(tp[2]) != '9':
                        mask_severity_dict[tp[0]] = str(tp[2])
                    if str(tp[3]) != '9':
                        mask_severity_dict[tp[1]] = str(tp[3])
                    if str(tp[4]) == '1':
                        real_alarm_list.append(tp[0])
                else:
                    odu16_mask_dict[tp[0]] = tp[1]
                    odu16_clear_alarm_dict[tp[1]] = tp[
                        5]  # This is for clear event type dict.
                    if str(tp[2]) != '9':
                        odu16_mask_severity_dict[tp[0]] = str(tp[2])
                    if str(tp[3]) != '9':
                        odu16_mask_severity_dict[tp[1]] = str(tp[3])
                    if str(tp[4]) == '1':
                        odu16_real_alarm_list.append(tp[0])

            # real_alarm_list=['SYNC_LOSS_THRESHOLD_EXCEEDED',
            # 'SYNC_LOSS_TIMEOUT', 'CRC_ERROR_THRESHOLD_EXCEEDED']
            f = open('/omd/daemon/alarm_mask.rg', 'w')
            f.write('mask_alarm_dict=' + str(mask_dict))
            f.write('\n')
            f.write('mask_severity_dict=' + str(mask_severity_dict))
            f.write('\n')
            f.write('real_alarm_list=' + str(real_alarm_list))
            f.write('\n')
            f.write('clear_alarm_dict=' + str(clear_alarm_dict))
            f.write('\n')
            f.write('odu16_mask_alarm_dict=' + str(odu16_mask_dict))
            f.write('\n')
            f.write(
                'odu16_mask_severity_dict=' + str(odu16_mask_severity_dict))
            f.write('\n')
            f.write('odu16_real_alarm_list=' + str(odu16_real_alarm_list))
            f.write('\n')
            f.write('odu16_clear_alarm_dict=' + str(odu16_clear_alarm_dict))
            f.close()


# Exception class for own created exception.
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
        output_dict = {'success': 2, 'output': str(msg)}
        html.write(str(output_dict))


#---- This is starting page of alarm mapping,it design the page . ----#

def start_page(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = [
        "css/jquery.multiselect.css", "css/jquery.multiselect.filter.css",
        "css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/alarmMapping.js"]
    header_btn = "<div class=\"header-icon\"><img class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"add_alarm\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Alarm\"></div>".format(
        theme)
    html.new_header(
        "Alarm Masking", "alarm_mapping.py", header_btn, css_list, js_list)
    html_content1 = "<div id=\"alarmTableContainer\">\
        <div id=\"alarm_editable_div\"></div>"

    html.write(html_content1)
    table_content2 = "<div id=\"demo_id\">\
    <table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\">\
    </table>\
    </div>\
    </div>"
    html.write(table_content2)
    html.new_footer()

#---- Its create the data table and display tha all alarm mapping informatin in data table -----#


def alarm_datail_function(h):
    """

    @param h:
    @return:
    """
    global html

    html = h
    try:
        db, cursor = mysql_connection(
            'mahimws')  # hard coded. need to be changed
        if db == 1:
            SelfException(cursor)
        sql = "SELECT trap_id_mapping_id, trap_event_type, trap_severity, trap_clear_mapping_type, clear_severity, device_type, is_alarm, is_deleted \
                From trap_id_mapping \
                where device_type in (select device_type_id from device_type  where is_deleted = 0)"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        result_list = []
        opac = 0.9
        debug = 0
        if len(result) < 1:
            output = {'success': 0, 'output': []}
            html.write(str(output))
            return
        else:
            for detail in result:
                result_list.append(make_list(detail))
            for row in result_list:
                trap_severity = severity_dict.get(int(row[2]))
                clear_severity = severity_dict.get(int(row[4]))
                device = device_type_dict.get(row[5])
                row[2] = trap_severity
                row[4] = clear_severity
                row[5] = device
                if row[6] == '1':
                    row[6] = 'True'
                else:
                    row[6] = 'False'
                if (row[7] == "1"):
                    flag = "falseclick"
                    opac = 0.4
                else:
                    flag = "trueclick"
                    opac = 0.9
                row.pop()
                debug = 11
                actions = ""
                actions += "<img src=\"images/edit16.png\" alt=\"edit\" style=\"opacity: %s\" \
                title=\"Edit Alarm\" class=\"imgbutton\" onclick=\"editAlarm(\'%s\',\'%s\')\" />" % (
                str(opac), row[0], flag)
                actions += "&nbsp; &nbsp; &nbsp;<img src=\"images/delete16.png\" alt=\"delete\" style=\"opacity: %s\" \
                title=\"Delete Alarm\" class=\"imgbutton\" onclick=\"checkDeleteAlarm(\'%s\',\'%s\')\" />" % (
                str(opac), row[0], flag)
                debug = 1
                row.append(actions)
                debug = 2
        output = {'success': 0, 'output': result_list}
        html.write(str(output))
    # Exception Handling
    except Exception as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e) + str(debug)}
        html.write(str(output_dict))
    finally:
        if db.open:
            cursor.close()
            db.close()


#---- This function show the add edit form. ------#
def add_edit_form_show(h):
    """

    @param h:
    @raise:
    """
    global html
    global di, severity_dict
    html = h

    option = html.var(
        "option")  # -- its define the add or edit form diplay --#
    try:
        db, cursor = mysql_connection('mahimws')
        if db == 1:
            raise SelfException(cursor)

        html_form = ""
        uniqe_id = html.var("uniqe_id")

        sql = "SELECT trap_event_type,trap_clear_mapping_type From trap_id_mapping where device_type in (select device_type_id from device_type  where is_deleted = 0)"
        cursor.execute(sql)
        tp = cursor.fetchall()
        tp1 = sum(tp, ())
        sql = "select device_type_id from device_type where is_deleted = 0"
        cursor.execute(sql)
        tp = cursor.fetchall()
        device_tp = sum(tp, ())

        if option == "ADD":
            html_form = "<div id=\"Columns\">\
                  <form id=\"alarm_form_detail\" action=\"add_form_entry.py\" method=\"get\">\
                  <div class=\"form-div\">\
                    <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">\
                        <tr>\
                        <th id=\"form_title\" class=\"cell-title\">Add Alarm</th>\
                        </tr>\
                    </table>\
                    <div class=\"row-elem\">\
                        <label  class = \"lbl lbl-big\" for=\"device_type\" align=\"right\">Device Type</label >\
                        <select name=\"device_type\" id=\"device_type\" class=\"multiselect\" multiple=\"multiple\" \
                            title=\"Select Device Type\"> "

            for key in device_tp:
                if key in device_type_dict:
                    html_form += "<option value=\"%s\">%s</option>" % (
                        key, device_type_dict[key])

            html_form += "</select></div>\
                        <div class=\"row-elem\">\
                            <label  class = \"lbl lbl-big\" for=\"trap_event_type\" align=\"right\">Alarm Type</label >\
                            <select  class=\"multiselect\" multiple=\"multiple\" id=\"trap_event_type\" name=\"trap_event_type\" \
                                title=\"Select Trap Event Type\"> "

            html_form += "</select></div>\
                    <div class=\"row-elem\">\
                        <label  class = \"lbl lbl-big\" for=\"trap_severity\" align=\"right\">Severity</label >\
                        <select  class=\"multiselect\" multiple=\"multiple\" id=\"trap_severity\" name=\"trap_severity\" \
                            title=\"Select Severity\"> "

            for i in severity_dict:
                html_form += "<option value=\"%s\">%s</option>" % (
                    i, severity_dict[i])

            html_form += "</select></div>\
                        <div class=\"row-elem\">\
                            <label  class = \"lbl lbl-big\" for=\"trap_event_clear_type\" align=\"right\">Alarm Clear Type</label >\
                            <select  class=\"multiselect\" multiple=\"multiple\" id=\"trap_event_clear_type\" name=\"trap_event_clear_type\" > "

            html_form += "</select></div>\
                    <div class=\"row-elem\">\
                        <label  class = \"lbl lbl-big\" for=\"clear_severity\" align=\"right\">Clear Severity</label >\
                        <select  class=\"multiselect\" multiple=\"multiple\" id=\"clear_severity\" name=\"clear_severity\" \
                            title=\"Select Clear type Severity\"> "

            for i in severity_dict:
                html_form += "<option value=\"%s\">%s</option>" % (
                    i, severity_dict[i])

            html_form += "</select></div>\
                    <div class=\"row-elem\">\
                        <label  class = \"lbl lbl-big\" for=\"is_alarm\" align=\"right\">IS Alarm</label >\
                        <input type=\"checkbox\" name=\"is_alarm\" id=\"is_alarm\" width=\"5\" value=\"1\"/>\
                    </div>\
                </div>\
                    <div class=\"form-div-footer\">\
                        <button type=\"submit\" class=\"yo-small yo-button\"  name=\"submit_button\" id=\"submit_button\">\
                            <span class=\"add\">Submit</span></button>\
                            <button type=\"button\" class=\"yo-small yo-button\" name=\"cancel_button\" id=\"cancel_button\">\
                            <span class=\"cancel\">Cancel</span></button>\
                    </div>\
                </form></div>"

        #-- its select the information from trap_mapping_id for show on the edit form ----#
        elif option == "Edit":

            sql = "select trap_id_mapping_id, trap_event_type, trap_clear_mapping_type, trap_severity, clear_severity, is_alarm, device_type \
            from trap_id_mapping where trap_id_mapping_id ='%s'" % (uniqe_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            temp_di = di[result[6]]

            html_form = "<div id=\"Columns\">\
                   <form id=\"alarm_form_detail\" action=\"add_form_entry.py\" method=\"get\">\
                        <div class=\"form-div\">\
                            <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
                                <tr>\
                                    <th id=\"form_title\" class=\"cell-title\">Edit Alarm</th>\
                                </tr>\
                            </table>\
                            <div class=\"row-elem\">\
                                <label  class = \"lbl lbl-big\" for=\"device_type\" align=\"right\">Device Type</label >\
                                <select  class=\"multiselect\" multiple=\"multiple\" id=\"device_type\" name=\"device_type\" \
                                    title=\"Select Device Type\">\
                                <option selected=\"selected\" value=\"%s\">%s</option>\
                        " % (result[6], device_type_dict[result[6]])

            html_form += "</select></div>\
                        <div class=\"row-elem\">\
                            <label  class = \"lbl lbl-big\" for=\"trap_event_type\" align=\"right\">Alarm Type</label >\
                            <select  class=\"multiselect\" multiple=\"multiple\" id=\"trap_event_type\" name=\"trap_event_type\" >\
                            <option selected=\"selected\" value=\"%s\">%s</option>" % (result[1], result[1])

            for i in temp_di:
                if tp1.count(i):
                    pass
                else:
                    html_form += "<option value=\"%s\">%s</option>" % (i, i)

            html_form += "</select></div>\
                    <div class=\"row-elem\">\
                       <label  class = \"lbl lbl-big\" for=\"trap_severity\" align=\"right\">Severity</label >\
                        <select  class=\"multiselect\" multiple=\"multiple\" id=\"trap_severity\" name=\"trap_severity\" \
                            title=\"Select Severity\">\
                        <option selected=\"selected\" value=\"%s\">%s</option>" % (result[3], severity_dict[result[3]])

            for i in severity_dict:
                if i == result[3]:
                    pass
                else:
                    html_form += "<option value=\"%s\">%s</option>" % (
                        i, severity_dict[i])

            html_form += "</select></div>\
                    <div class=\"row-elem\">\
                        <label  class = \"lbl lbl-big\" for=\"trap_event_clear_type\" align=\"right\">Alarm Clear Type</label >\
                        <select  class=\"multiselect\" multiple=\"multiple\" id=\"trap_event_clear_type\" name=\"trap_event_clear_type\" >\
                        <option selected=\"selected\" value=\"%s\">%s</option>" % (result[2], result[2])

            for i in temp_di:
                if tp1.count(i):
                    pass
                else:
                    html_form += "<option value=\"%s\">%s</option>" % (i, i)

            html_form += "</select></div>\
                    <div class=\"row-elem\">\
                        <label  class = \"lbl lbl-big\" for=\"clear_severity\" align=\"right\">Clear Severity</label >\
                        <select  class=\"multiselect\" multiple=\"multiple\" id=\"clear_severity\" name=\"clear_severity\" \
                            title=\"Select Clear type Severity\">\
                        <option selected=\"selected\" value=\"%s\">%s</option>" % (result[4], severity_dict[result[4]])

            for i in severity_dict:
                if i == result[4]:
                    pass
                else:
                    html_form += "<option value=\"%s\">%s</option>" % (
                        i, severity_dict[i])

            html_form += "</select></div>\
                        <input type=\"hidden\" name=\"mapping_id\" id=\"mapping_id\" value = \"%s\" />" % (
            str(result[0]))

            html_form += "<div class=\"row-elem\">\
                            <label  class=\"lbl lbl-big\" for=\"is_alarm\" align=\"right\">IS Alarm</label >\
                            <input type=\"checkbox\" name=\"is_alarm\" id=\"is_alarm\" %s width=\"5\" value=\"1\"/>\
                        </div >\
                    </div>\
                    <div class=\"form-div-footer\">\
                        <button type=\"submit\" class=\"yo-small yo-button\"  name=\"submit_button\" id=\"submit_button\">\
                            <span class=\"edit\">Edit</span></button>\
                        <button type=\"button\" class=\"yo-small yo-button\" name=\"cancel_button\" id=\"cancel_button\">\
                            <span class=\"cancel\">Cancel</span></button>\
                    </div>\
                </form></div>" % (('checked=\"checked\"' if result[5] == 1 else ''))

        cursor.close()
        db.close()
        html.write("{output:{table:'" + str(html_form).replace("\"",
                                                               "\\\"") + "'},success:0}")
    # Exception Handling
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': 'db connection not found'}
        html.write(str(output_dict))
    except Exception as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    finally:
        if db.open:
            cursor.close()
            db.close()


def get_trap_lists(h):
    """

    @param h:
    @raise:
    """
    try:
        global html
        html = h
        device_type = html.var("device_type")
        global di
        db, cursor = mysql_connection('mahimws')
        if db == 1:
            raise SelfException(cursor)
        html_form = ""
        sql = "SELECT trap_event_type,trap_clear_mapping_type From trap_id_mapping where device_type = '%s'" % (
            device_type)
        cursor.execute(sql)
        tp = cursor.fetchall()
        tp1 = sum(tp, ())
        temp_di = di.get(device_type)
        if temp_di:
            for i in temp_di:
                if tp1.count(i):
                    pass
                else:
                    html_form += "<option value=\"%s\">%s</option>" % (i, i)
        output_dict = {"success": 0, 'output': html_form}
        html.write(str(output_dict))
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
    except AttributeError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except NameError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except MySQLdb as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {'success': 1, 'output': str(e)}
        html.write(str(output_dict))
    except Exception as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except DatabaseError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except DisconnectionError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    finally:
        if db.open:
            cursor.close()
            db.close()

#---- This function is use for add the new entry in mapping table ------#


def add_form_entry(h):
    """

    @param h:
    @return: @raise:
    """
    global html
    global di, severity_dict
    html = h
    cr_by = config.user
    event_type = html.var("trap_event_type")
    event_clear_type = html.var("trap_event_clear_type")
    is_alarm = html.var("is_alarm")
    trap_severity = html.var("trap_severity")
    clear_severity = html.var("clear_severity")
    device_type = html.var("device_type")
    temp_di = di.get(device_type, {})
    event_id = temp_di.get(event_type)
    clear_event_id = temp_di.get(event_clear_type)
    error_no = 0

    try:
        if len(temp_di) < 0 and event_type == None and device_type == None:
            html.write(
                "{output:{Exception:'Arguments are not proper, Please refresh your webpage and retry again'},success:'1'}")
            return
    except Exception, e:
        html.write(
            "{output:{Exception:'Arguments missing, Please refresh your webpage and retry again'},success:'1'}")
        return

    try:
        db, cursor = mysql_connection('nms')
        if db == 1:
            raise SelfException(cursor)
        sql = "SELECT trap_event_type,trap_event_id from trap_id_mapping where trap_event_type='%s' and device_type = '%s'\
            " % (event_type, device_type)
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) < 1:
            sql = "INSERT INTO trap_id_mapping(trap_event_type, trap_event_id, trap_clear_mapping_type, trap_clear_mapping_id, \
                trap_severity, clear_severity, is_alarm, device_type, created_by, creation_time) values \
            ('%s', '%s',  '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s')\
            " % (event_type, event_id, event_clear_type, clear_event_id, trap_severity, clear_severity,
                 (0 if is_alarm is None or is_alarm == "" else 1), device_type, cr_by, datetime.now())

            cursor.execute(sql)
            db.commit()
        else:
            if result[0][0].upper() == event_type.upper():
                error_no = 13
            elif result[0][0].upper() == event_type.upper():
                error_no = 11

        cursor.execute("select trap_event_id, trap_clear_mapping_id, trap_severity, clear_severity, is_deleted, \
                        trap_clear_mapping_type, device_type from trap_id_mapping where is_alarm = 1")
        tp2d = cursor.fetchall()

        if len(tp2d) > 0:
            write_mask_file(tp2d)  # MASK FILE WRITE CODE alarm_mask.rg
        cursor.close()
        db.close()
        html.write("{output:{table:'" + "success full add" +
                   "'},success:'" + str(error_no) + "'}")

    # Exception Handling
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
        pass
    except AttributeError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except NameError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except MySQLdb as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {'success': 1, 'output': str(e)}
        html.write(str(output_dict))
    except Exception as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except DatabaseError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except DisconnectionError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    finally:
        if db.open:
            cursor.close()
            db.close()


#--- This function is use for check the edit the existing record in mapping  table ---- #
def edit_form_entry(h):
    """

    @param h:
    @return: @raise:
    """
    global html
    global di
    html = h
    event_type = html.var("trap_event_type")
    event_clear_type = html.var("trap_event_clear_type")
    is_alarm = html.var("is_alarm")
    trap_severity = html.var("trap_severity")
    clear_severity = html.var("clear_severity")
    device_type = html.var("device_type")
    temp_di = di.get(device_type, {})
    event_id = temp_di.get(event_type)
    clear_event_id = temp_di.get(event_clear_type)
    up_by = config.user
    uniqe_id = html.var("uniqe_id")
    error_no = 0

    try:
        if len(temp_di) < 0 and uniqe_id == None and device_type == None:
            html.write(
                "{output:{Exception:'Arguments are not proper, Please refresh your webpage and retry again'},success:'1'}")
            return
    except Exception, e:
        html.write(
            "{output:{Exception:'Arguments missing, Please refresh your webpage and retry again'},success:'1'}")
        return

    try:
    #=-- database connection creation  and cursor creation --- #
        db, cursor = mysql_connection('nms_copy')
        if db == 1:
            raise SelfException(cursor)
        sql = "UPDATE trap_id_mapping SET trap_event_type = '%s' ,trap_event_id = '%s' , trap_severity = '%s', trap_clear_mapping_id = '%s', \
            trap_clear_mapping_type='%s', clear_severity = '%s', updated_by='%s', is_alarm=%s where trap_id_mapping_id = '%s'\
            " % (event_type, event_id, trap_severity, clear_event_id, event_clear_type, clear_severity, up_by,
                 (0 if is_alarm == None or is_alarm == "" else 1), uniqe_id)
        cursor.execute(sql)
        db.commit()
        cursor.execute("select trap_event_id, trap_clear_mapping_id, trap_severity, clear_severity, is_deleted, \
            trap_clear_mapping_type, device_type from trap_id_mapping where is_alarm = 1")
        tp2d = cursor.fetchall()
        if len(tp2d) > 0:
            write_mask_file(tp2d)
        cursor.close()
        db.close()
        html.write("{output:{Exception:'data updated'},success:'0'}")
    # Exception Handling
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
    except AttributeError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except NameError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except MySQLdb as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {'success': 1, 'output': str(e)}
        html.write(str(output_dict))
    except Exception as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except DatabaseError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except DisconnectionError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    finally:
        if db.open:
            cursor.close()
            db.close()


#---- This function is used for delete the record from trap_mapping_table . -------#

def delete_alarm_id(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    alarm_delete_id = html.var("alarm_delete_id")
    try:
        db, cursor = mysql_connection('nms')
        if db == 1:
            raise SelfException(cursor)
        sql = "DELETE from trap_id_mapping where trap_id_mapping_id = '%s' " % (
            alarm_delete_id)
        cursor.execute(sql)
        db.commit()
        cursor.execute("select trap_event_id, trap_clear_mapping_id, trap_severity, clear_severity, is_deleted, \
           trap_clear_mapping_type, device_type from trap_id_mapping where is_alarm = 1")
        tp2d = cursor.fetchall()
        if len(tp2d) > 0:
            write_mask_file(tp2d)
        cursor.close()
        db.close()

        html.write("{output:{table:1},")
        html.write("success:'" + str("0") + "'}")
    # Exception Handling
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
        pass
    except AttributeError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except NameError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except MySQLdb as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {'success': 1, 'output': str(e)}
        html.write(str(output_dict))
    except Exception as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except DatabaseError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except DisconnectionError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    finally:
        if db.open:
            cursor.close()
            db.close()


# def page_tip_alarm_mapping(h):
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_alarm_mapping.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))
