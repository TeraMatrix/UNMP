#!/usr/bin/python2.6

"""
@author: Rahul Gautam
@note: User Management bll
@attention: FINAL: 28/dec
"""

import MySQLdb
import uuid
from unmp_config import SystemConfig
from unmp_login import is_account_locked
from datetime import datetime
import traceback

global global_db


def db_connect():
    """
    Used to connect to the database  
    returns database object ed in global_db variable
    """
    db = None
    global global_db
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        global_db = db
    except MySQLdb.Error as e:
        pass  # print "/*/*/* MYSQLdb Exception (db connect) : "+str(e)
    except Exception as e:
        pass  # print "/*/*/* Database Exception (db connect) : "+str(e)


def db_close():
    """
    closes connection with the database
    """
    global global_db
    try:
        global_db.close()
    except Exception as e:
        pass  # print "/*/*/* Database Exception ( db close ) : "+str(e)


def getGroupsData():
    """
    To get the hostgroups related data

    """
    db_connect()
    global global_db
    db_close()


def ap_add_default_data_new_user(user_id):
    """

    @param user_id:
    @return:
    """
    try:
        global global_db
        if global_db.open != 1:
            db_connect()

        cursor = global_db.cursor()

        default_temp_list = [
            ['apNWBandwidth',
             'Network Bandwidth Statistics',
             0, 'ap25', 1, 1, 0, 0, 0, 5,
             180, 250, 1, 1, 1, 1, 1,
             'Network Bandwidth Statistics',
             'Statistics', 600, 0
            ], [
                'ap25outage',
                'Device Reachability Statistics',
                0, 'ap25', 2, 1, 0, 0, 0, 5,
                180, 250, 1, 1, 1, 1, 0,
                'Reachability Statistics',
                '', 600, 0
            ], [
                'vapConnectedClient',
                'Connected Client',
                0, 'ap25', 1, 1, 0, 0, 0, 5,
                180, 250, 1, 1, 1, 1, 1,
                'Connected Client',
                '', 600, 0
            ], [
                'totalConnectedClient',
                'Total Connected Client',
                0, 'ap25', 1, 1, 0, 0, 0, 5,
                180, 250, 1, 1, 1, 1, 1,
                'Total Connected Client',
                '', 600, 0
            ]
        ]
        for default_temp in default_temp_list:
            ins_temp_query = "INSERT INTO  `graph_templet_table` \
            (`graph_display_id` ,`graph_display_name` ,`user_id` ,`is_disabled` ,`device_type_id` ,`graph_id` ,`graph_tab_option` \
            ,`refresh_button` , `next_pre_option` ,`start_value` ,`end_value` ,`graph_width` ,`graph_height` ,`graph_cal_id` ,`show_type` \
            ,`show_field` ,`show_cal_type` ,`show_tab_option`,`graph_title`,`graph_subtitle`,`auto_refresh_time_second`,`is_deleted`)\
            VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'%s','%s' ,'%s',%s,%s)\
            " % (default_temp[0], default_temp[1], user_id, default_temp[2], default_temp[3], default_temp[4],
                 default_temp[5], default_temp[6],
                 default_temp[7], default_temp[8], default_temp[9], default_temp[
                10], default_temp[11], default_temp[12], default_temp[13],
                 default_temp[14], default_temp[15], default_temp[16], default_temp[17], default_temp[18],
                 default_temp[19], default_temp[20])
            cursor.execute(ins_temp_query)
        global_db.commit()

        # Entry for calculation type
        calculation_field = {'apNWBandwidth': ['Total', 'Delta'], 'ap25outage': ['Total'],
                             'vapConnectedClient': ['Total'], 'totalConnectedClient': ['Total']}
        for cal in calculation_field:
            i = 1
            for cal_val in calculation_field[cal]:
                ins_query = "insert into graph_calculation_table (user_id,table_name,graph_cal_id,graph_cal_name) values('%s','%s',%s,'%s')\
                " % (user_id, cal, i, cal_val)
                cursor.execute(ins_query)
                i += 1
        global_db.commit()

        # Entry for interface
        ap_intereface_name = ['eth0', 'br0', 'atho', 'ath1',
                              'ath2', 'ath3', 'ath4', 'ath5', 'ath6', 'ath7']
        interface_field = {'apNWBandwidth': ap_intereface_name}
        for table in interface_field:
            i = 0
            for interface in interface_field[table]:
                if i == 0:
                    ins_query = "insert into graph_interface_table (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)" % (user_id, table, i, interface, 1)
                else:
                    ins_query = "insert into graph_interface_table (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)" % (user_id, table, i, interface, 0)
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        # interface value
        graph_field = {
        'apNWBandwidth': ['statisticsRxPackets', 'statisticsTxPackets', 'statisticsRxError', 'statisticsTxError'],
        'ap25outage': ['Reachable', 'Unreachable'], 'vapConnectedClient': ['1', '2', '3', '4', '5', '6', '7', '8'],
        'totalConnectedClient': ['1']}

        graph_display_name = {'apNWBandwidth': ['Rx Packets', 'Tx Packets', 'Rx Error', 'Tx Error'],
                              'ap25outage': ['Reachable', 'Unreachable'],
                              'vapConnectedClient': ['VAP1', 'VAP2', 'VAP3', 'VAP4', 'VAP5', 'VAP6', 'VAP7', 'VAP8'],
                              'totalConnectedClient': ['Client']}

        tool_tip_name = {'apNWBandwidth': ['(packet)', '(packet)', '(count)', '(count)'],
                         'ap25outage': ['(%)', '(%)'],
                         'vapConnectedClient': ['(count)', '(count)', '(count)', '(count)', '(count)', '(count)',
                                                '(count)', '(count)'],
                         'totalConnectedClient': ['(count)']}

        for field in graph_field:
            i = 0
            for name in graph_field[field]:
                if i < 2:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                else:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 0, tool_tip_name[field][i])
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        ajax_data = {'apNWBandwidth': ['apNWBandwidth', 'sp_common_graph_creation.py', 'post',
                                       'ap25_statisticsTable,timestamp,index,apNWBandwidth'],
                     'ap25outage': ['ap25outage', 'sp_common_graph_creation.py', 'post',
                                    'outage,timestamp,noIndexName,ap25outage'],
                     'vapConnectedClient': ['vapConnectedClient', 'sp_common_graph_creation.py', 'post', 'ap25_vapClientStatisticsTable,\
                   timestamp,vap_id,vapConnectedClient'],
                     'totalConnectedClient': ['totalConnectedClient', 'sp_common_graph_creation.py', 'post',
                                              'ap25_vapClientStatisticsTable,timestamp,vap_id,totalConnectedClient']}
        for data in ajax_data:
            sql = "insert into graph_ajax_call_information (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')" % (
            user_id, ajax_data[data][0], ajax_data[data][1], ajax_data[data][2], ajax_data[data][3])
            cursor.execute(sql)
        global_db.commit()
        total_data = {}
        for count_data in total_data:
            sql = "insert into total_count_item (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')" % (
            user_id, total_data[count_data][0], total_data[count_data][1], total_data[count_data][2],
            total_data[count_data][3])
            cursor.execute(sql)
        global_db.commit()
    except Exception, e:
        output_dict = {'success': 1, 'result': str(e[-1])}
        return output_dict


##
def odu16_add_graph_info_new_user(user_id):
    """

    @param user_id:
    @return:
    """
    try:
        global global_db
        if global_db.open != 1:
            db_connect()

        cursor = global_db.cursor()
        # first graph_id and second value is table name#

        #	global_db=MySQLdb.connect('localhost','root','root','midnms')
        #        cursor=global_db.cursor()

        default_temp_list = [
            ['odu16rssi', 'RSL Statistics', 0, 'odu16', 2, 1, 0, 0, 0, 5, 180,
             250, 1, 1, 1, 1, 0, 'RSL Statistics', '', 600, 0],
            ['odu16outage', 'Device Reachability Statistics', 0, 'odu16', 2, 1, 0, 0, 0, 5,
             180, 250, 1, 1, 1, 1, 0, 'Reachability Statistics', '', 600, 0],
            ['odu16NWBandwidth', 'Network Bandwidth Statistics', 1, 'odu16', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Network Bandwidth Statistics', 'Statistics', 600, 0],
            ['odu16synclost', 'Sync Lost', 1, 'odu16', 0, 1, 0, 0, 0, 5,
             180, 250, 1, 1, 1, 1, 0, 'Sync Lost', '', 600, 0],
            ['odu16crcphy', 'Crc Phy Error Count', 1, 'odu16', 0, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'CRC PHY Error', '', 600, 0]]
        for default_temp in default_temp_list:
            ins_temp_query = "INSERT INTO  `graph_templet_table` \
            (`graph_display_id` ,`graph_display_name` ,`user_id` ,`is_disabled` ,`device_type_id` ,`graph_id` ,\
            `graph_tab_option` ,`refresh_button` , `next_pre_option` ,`start_value` ,`end_value` ,`graph_width` ,\
            `graph_height` ,`graph_cal_id` ,`show_type` ,`show_field` ,`show_cal_type` ,`show_tab_option`,\
            `graph_title`,`graph_subtitle`,`auto_refresh_time_second`,`is_deleted`)\
            VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'%s','%s' ,'%s',%s,%s)\
            " % (default_temp[0], default_temp[1], user_id, default_temp[2], default_temp[3], default_temp[4],
                 default_temp[5], default_temp[6], default_temp[
                7], default_temp[8], default_temp[9], default_temp[10],
                 default_temp[11], default_temp[
                12], default_temp[13], default_temp[14], default_temp[15],
                 default_temp[16], default_temp[17], default_temp[18], default_temp[19], default_temp[20])
            cursor.execute(ins_temp_query)
        global_db.commit()

        # Entry for calculation type
        calculation_field = {'odu16NWBandwidth': ['Total', 'Delta'],
                             'odu16synclost': ['Total', 'Delta'],
                             'odu16crcphy': ['Total', 'Delta'],
                             'odu16outage': ['Total'],
                             'odu16rssi': ['Total']}
        for cal in calculation_field:
            i = 1
            for cal_val in calculation_field[cal]:
                ins_query = "insert into graph_calculation_table \
                (user_id,table_name,graph_cal_id,graph_cal_name) \
                values('%s','%s',%s,'%s')" % (user_id, cal, i, cal_val)
                cursor.execute(ins_query)
                i += 1
        global_db.commit()

        # Entry for interface
        ap_intereface_name = ['eth0', 'br0', 'eth1']
        interface_field = {'odu16NWBandwidth': ap_intereface_name}
        for table in interface_field:
            i = 0
            for interface in interface_field[table]:
                if i == 0:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)" % (user_id, table, i + 1, interface, 1)
                else:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)" % (user_id, table, i + 1, interface, 0)
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        #        get_coloum="SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE graph_name='%s' AND user_id='%s'"%('ap25_statisticsTable',user_id)
        #        cursor.execute(get_coloum)
        #        coloum_result=cursor.fetchall()
        #        table_field_dict=dict((field[0],field[1]) for field in coloum_result)
        # interface value
        graph_field = {
        'odu16NWBandwidth': ['rx_packets', 'tx_packets', 'rx_bytes', 'tx_bytes', 'rx_errors', 'tx_errors'],
        'odu16synclost': ['sysc_lost_counter'], 'odu16crcphy': ['rx_crc_errors', 'rx_phy_error'],
        'odu16outage': ['Reachable', 'Unreachable'], 'odu16rssi': ['1', '2', '3', '4', '5', '6', '7', '8']}
        graph_display_name = {
        'odu16NWBandwidth': ['Rx Packets', 'Tx Packets', 'Rx Bytes', 'Tx Bytes', 'Rx Error', 'Tx Error'],
        'odu16synclost': ['SyncLoss'], 'odu16crcphy': ['CRC Error', 'PHY Error'],
        'odu16outage': ['Reachable', 'Unreachable'],
        'odu16rssi': ["Link1", "Link2", "Link3", "Link4", "Link5", "Link6", "Link7", "Link8"]}
        tool_tip_name = {'odu16NWBandwidth': ['(pps)', '(pps)', '(bps)', '(bps)', '(count)', '(count)'],
                         'odu16synclost': ['(count)'],
                         'odu16crcphy': ['(count)', '(count)'],
                         'odu16outage': ['(%)', '(%)'],
                         'odu16rssi': ['(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)']}
        for field in graph_field:
            i = 0
            for name in graph_field[field]:
                if i < 2:
                    ins_query = "insert into graph_field_table \
                    user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                else:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 0, tool_tip_name[field][i])
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        ajax_data = {'odu16NWBandwidth': ['odu16NWBandwidth', 'sp_common_graph_creation.py', 'post',
                                          'get_odu16_nw_interface_statistics_table,timestamp,index,odu16NWBandwidth'],
                     'odu16synclost': ['odu16synclost', 'sp_common_graph_creation.py', 'post',
                                       'get_odu16_synch_statistics_table,timestamp,index,odu16synclost'],
                     'odu16crcphy': ['odu16crcphy', 'sp_common_graph_creation.py', 'post',
                                     'get_odu16_ra_tdd_mac_statistics_entry,timestamp,index,odu16crcphy'],
                     'odu16outage': ['odu16outage', 'sp_common_graph_creation.py', 'post',
                                     'outage,timestamp,noIndexName,odu16outage'],
                     'odu16rssi': ['odu16rssi', 'sp_common_graph_creation.py', 'post',
                                   'get_odu16_peer_node_status_table,timestamp,timeslot_index,odu16rssi']}
        for data in ajax_data:
            sql = "insert into graph_ajax_call_information \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, ajax_data[data][0], ajax_data[data][1], ajax_data[data][2], ajax_data[data][3])
            cursor.execute(sql)
        global_db.commit()

        # total_data={'apVAPUserConnect':['apVAPUserConnect','ap_total_data_count.py','post','ap25_vapClientStatisticsTable,addressMAC']}
        total_data = {}
        for count_data in total_data:
            sql = "insert into total_count_item \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, total_data[count_data][0], total_data[count_data][1], total_data[count_data][2],
                 total_data[count_data][3])
            cursor.execute(sql)
        global_db.commit()

    except Exception, e:
        output_dict = {'success': 1, 'result': str(e[-1])}
        return output_dict

##


def odu100_add_graph_info_new_user(user_id):
    """

    @param user_id:
    @return:
    """
    try:
        global global_db
        if global_db.open != 1:
            db_connect()

        cursor = global_db.cursor()
        # first graph_id and second value is table name#

        #	global_db=MySQLdb.connect('localhost','root','root','midnms')
        #        cursor=global_db.cursor()

        default_temp_list = [
            ['odu100link', 'Link Quality Statistics', 0, 'odu100', 2, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'Link Quality Statistics', '', 600, 0],
            ['odu100peernode', 'Link Bandwidth Statistics', 0, 'odu100', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Link Bandwidth Statistics', '', 600, 0],
            ['odu100rssi', 'RSL1 Statistics', 0, 'odu100', 2, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'RSL1 Statistics', '', 600, 0],
            ['odu100rssi2', 'RSL2 Statistics', 0, 'odu100', 2, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'RSL2 Statistics', '', 600, 0],
            ['odu100outage', 'Device Reachability Statistics', 0, 'odu100', 2, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'Reachability Statistics', '', 600, 0],
            ['odu100NWBandwidth', 'Network Bandwidth Statistics', 0, 'odu100', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1,
             1,
             'Network Bandwidth Statistics', 'Statistics', 600, 0],
            ['odu100synclost', 'Sync Lost', 1, 'odu100', 1, 1, 0, 0, 0,
             5, 180, 250, 1, 1, 1, 1, 0, 'Sync Lost', '', 600, 0],
            ['odu100crcphy', 'Crc Phy Error Count', 1, 'odu100', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'CRC PHY Error', '', 600, 0]]

        for default_temp in default_temp_list:
            ins_temp_query = "INSERT INTO  `graph_templet_table` \
            (`graph_display_id` ,`graph_display_name` ,`user_id` ,`is_disabled` ,`device_type_id` ,\
            `graph_id` ,`graph_tab_option` ,`refresh_button` , `next_pre_option` ,`start_value` ,\
            `end_value` ,`graph_width` ,`graph_height` ,`graph_cal_id` ,`show_type` ,`show_field` ,\
            `show_cal_type` ,`show_tab_option`,`graph_title`,`graph_subtitle`,`auto_refresh_time_second`,`is_deleted`)\
            VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'%s','%s' ,'%s',%s,%s)\
            " % (default_temp[0], default_temp[1], user_id, default_temp[2], default_temp[3], default_temp[4],
                 default_temp[5],
                 default_temp[6], default_temp[7], default_temp[
                8], default_temp[9], default_temp[10], default_temp[11],
                 default_temp[12], default_temp[13], default_temp[
                14], default_temp[15], default_temp[16], default_temp[17],
                 default_temp[18], default_temp[19], default_temp[20])
            cursor.execute(ins_temp_query)
        global_db.commit()

        # Entry for calculation type
        calculation_field = {'odu100NWBandwidth': ['Total', 'Delta'],
                             'odu100synclost': ['Total', 'Delta'],
                             'odu100crcphy': ['Total', 'Delta'],
                             'odu100outage': ['Total'],
                             'odu100rssi': ['Total'],
                             'odu100rssi2': ['Total'],
                             'odu100link': ['Total'],
                             'odu100peernode': ['Total']}
        for cal in calculation_field:
            i = 1
            for cal_val in calculation_field[cal]:
                ins_query = "insert into graph_calculation_table \
                (user_id,table_name,graph_cal_id,graph_cal_name) \
                values('%s','%s',%s,'%s')\
                " % (user_id, cal, i, cal_val)
                cursor.execute(ins_query)
                i += 1
        global_db.commit()
        # Entry for interface
        ap_intereface_name = ['eth0', 'eth1']
        peer_intereface_name = [
            "Link1", "Link2", "Link3", "Link4", "Link5", "Link6", "Link7", "Link8",
            "Link9", "Link10", "Link11", "Link12", "Link13", "Link14", "Link15", "Link16"]
        interface_field = {'odu100NWBandwidth': ap_intereface_name,
                           'odu100peernode': peer_intereface_name}
        for table in interface_field:
            i = 0
            for interface in interface_field[table]:
                if i == 0:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)\
                    " % (user_id, table, i + 1, interface, 1)
                else:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)\
                    " % (user_id, table, i + 1, interface, 0)
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        #        get_coloum="SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE graph_name='%s' AND user_id='%s'"%('ap25_statisticsTable',user_id)
        #        cursor.execute(get_coloum)
        #        coloum_result=cursor.fetchall()
        #        table_field_dict=dict((field[0],field[1]) for field in coloum_result)

        # interface value
        graph_field = {'odu100NWBandwidth': ['rxPackets', 'txPackets', 'rxBytes', 'txBytes', 'rxErrors', 'txErrors'],
                       'odu100synclost': ['syncLostCounter'],
                       'odu100crcphy': ['rxCrcErrors', 'rxPhyError'],
                       'odu100outage': ['Reachable', 'Unreachable'],
                       'odu100rssi': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                                      '16'],
                       'odu100rssi2': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                                       '16'],
                       'odu100link': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                                      '16'],
                       'odu100peernode': ['allocatedTxBW', 'allocatedRxBW', 'usedTxBW', 'usedRxBW',
                                          'negotiatedMaxUplinkBW', 'negotiatedMaxDownlinkBW']}

        graph_display_name = {
        'odu100NWBandwidth': ['Rx Packets', 'Tx Packets', 'Rx Bytes', 'Tx Bytes', 'Rx Error', 'Tx Error'],
        'odu100synclost': ['SyncLoss'], 'odu100crcphy': ['CRC Error', 'PHY Error'],
        'odu100outage': ['Reachable', 'Unreachable'],
        'odu100rssi': ["Link1", "Link2", "Link3", "Link4", "Link5", "Link6", "Link7",
                       "Link8", "Link9", "Link10", "Link11", "Link12", "Link13", "Link14", "Link15", "Link16"],
        'odu100rssi2': ["Link1", "Link2", "Link3", "Link4", "Link5", "Link6", "Link7", "Link8", "Link9",
                        "Link10", "Link11", "Link12", "Link13", "Link14", "Link15", "Link16"],
        'odu100link': ["Link1", "Link2", "Link3", "Link4", "Link5", "Link6", "Link7", "Link8", "Link9",
                       "Link10", "Link11", "Link12", "Link13", "Link14", "Link15", "Link16"],
        'odu100peernode': ["Allocated Tx BW", "Allocated Rx BW", "Used Tx BW", "Used Rx BW",
                           "Negotiated Max Uplink BW", "Negotiated Max Downlink BW"]}

        tool_tip_name = {'odu100NWBandwidth': ['(pps)', '(pps)', '(bps)', '(bps)', '(count)', '(count)'],
                         'odu100synclost': ['(count)'], 'odu100crcphy': ['(count)', '(count)'],
                         'odu100outage': ['(%)', '(%)'],
                         'odu100rssi': ['(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)',
                                        '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)',
                                        '(dBm)', '(dBm)', '(dBm)', '(dBm)'],
                         'odu100rssi2': ['(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)',
                                         '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)', '(dBm)',
                                         '(dBm)', '(dBm)', '(dBm)', '(dBm)'],
                         'odu100link': ['(%)', '(%)', '(%)', '(%)', '(%)', '(%)', '(%)', '(%)',
                                        '(%)', '(%)', '(%)', '(%)', '(%)', '(%)', '(%)', '(%)'],
                         'odu100peernode': ["(kbps)", "(kbps)", "(kbps)", "(kbps)", "(kbps)", "(kbps)"]}
        for field in graph_field:
            i = 0
            for name in graph_field[field]:
                if i < 2:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')\
                    " % (user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                else:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')\
                    " % (user_id, field, name, graph_display_name[field][i], 0, tool_tip_name[field][i])
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        ajax_data = {'odu100NWBandwidth': ['odu100NWBandwidth', 'sp_common_graph_creation.py', 'post',
                                           'odu100_nwInterfaceStatisticsTable,timestamp,nwStatsIndex,odu100NWBandwidth'],
                     'odu100synclost': ['odu100synclost', 'sp_common_graph_creation.py', 'post', 'odu100_synchStatisticsTable,\
                   timestamp,syncConfigIndex,odu100synclost'],
                     'odu100crcphy': ['odu100crcphy', 'sp_common_graph_creation.py', 'post',
                                      'odu100_raTddMacStatisticsTable,timestamp,raIndex,odu100crcphy'],
                     'odu100outage': ['odu100outage', 'sp_common_graph_creation.py', 'post', 'outage,timestamp,\
                   noIndexName,odu100outage'],
                     'odu100rssi': ['odu100rssi', 'sp_common_graph_creation.py', 'post',
                                    'odu100_peerNodeStatusTable,timestamp,timeSlotIndex,odu100rssi'],
                     'odu100rssi2': ['odu100rssi2', 'sp_common_graph_creation.py', 'post',
                                     'odu100_peerNodeStatusTable,timestamp,timeSlotIndex,odu100rssi2'],
                     'odu100link': ['odu100link', 'sp_common_graph_creation.py', 'post',
                                    'odu100_peerNodeStatusTable,timestamp,timeSlotIndex,odu100link'],
                     'odu100peernode': ['odu100peernode', 'sp_common_graph_creation.py', 'post',
                                        'odu100_peerNodeStatusTable,timestamp,timeSlotIndex,odu100peernode']}
        for data in ajax_data:
            sql = "insert into graph_ajax_call_information \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, ajax_data[data][0], ajax_data[data][1], ajax_data[data][2], ajax_data[data][3])
            cursor.execute(sql)
        global_db.commit()
        # total_data={'apVAPUserConnect':['apVAPUserConnect','ap_total_data_count.py','post','ap25_vapClientStatisticsTable,addressMAC']}
        total_data = {}
        for count_data in total_data:
            sql = "insert into total_count_item \
            (user_id,graph_id,url,method,other_data)\
            values('%s','%s','%s','%s','%s')\
            " % (user_id, total_data[count_data][0], total_data[count_data][1], total_data[count_data][2],
                 total_data[count_data][3])
            cursor.execute(sql)
        global_db.commit()
    except Exception, e:
        output_dict = {'success': 1, 'result': str(e[-1])}
        return output_dict

##


def idu4_add_graph_info_new_user(user_id):
    """

    @param user_id:
    @return:
    """
    try:
        global global_db
        if global_db.open != 1:
            db_connect()

        cursor = global_db.cursor()
        # first graph_id and second value is table name#

        #	global_db=MySQLdb.connect('localhost','root','root','midnms')
        #        cursor=global_db.cursor()
        default_temp_list = [
            ['idu4NWBandwidth', 'Network Bandwidth Statistics', 1, 'idu4', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Network Bandwidth Statistics', 'Statistics', 600, 0],
            ['idu4TDMOIPBandwidth', 'TDMOIP Bandwidth Statistics', 1, 'idu4', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'TDMOIP Bandwidth Statistics', '', 600, 0],
            ['idu4PortStatistics', 'Port Statistics', 1, 'idu4', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Port Statistics', '', 600, 0],
            ['idu4outage', 'Device Reachability Statistics', 0, 'idu4', 2, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Reachability Statistics', '', 600, 0],
            ['idu4e1port', 'E1 Port Statistics', 0, 'idu4', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'E1 Port Statistics', '', 600, 0],
            ['idu4swPrimary', 'Primary Port Statistics', 0, 'idu4', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Primary Port Statistics', '', 600, 0],
            ['idu4swSecondary', 'Secondary Port Statistics', 1, 'idu4', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Secondary Port Statistics', '', 600, 0]]
        for default_temp in default_temp_list:
            ins_temp_query = "INSERT INTO  `graph_templet_table` \
            (`graph_display_id` ,`graph_display_name` ,`user_id` ,`is_disabled` ,`device_type_id` ,`graph_id` ,\
            `graph_tab_option` ,`refresh_button` , `next_pre_option` ,`start_value` ,`end_value` ,`graph_width` ,\
            `graph_height` ,`graph_cal_id` ,`show_type` ,`show_field` ,`show_cal_type` ,`show_tab_option`,\
            `graph_title`,`graph_subtitle`,`auto_refresh_time_second`,`is_deleted`)\
            VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s,'%s','%s' ,'%s',%s,%s)\
            " % (default_temp[0], default_temp[1], user_id, default_temp[2], default_temp[3], default_temp[4],
                 default_temp[5], default_temp[6], default_temp[
                7], default_temp[8], default_temp[9], default_temp[10],
                 default_temp[11], default_temp[
                12], default_temp[13], default_temp[14], default_temp[15],
                 default_temp[16], default_temp[17], default_temp[18], default_temp[19], default_temp[20])
            cursor.execute(ins_temp_query)
        global_db.commit()

        # Entry for calculation type
        calculation_field = {'idu4NWBandwidth': ['Total', 'delta'],
                             'idu4TDMOIPBandwidth': ['Total', 'Delta'],
                             'idu4PortStatistics': ['Total', 'Delta'],
                             'idu4outage': ['Total'],
                             'idu4e1port': ['Total', 'Delta'],
                             'idu4swPrimary': ['Total', 'Delta'],
                             'idu4swSecondary': ['Total', 'Delta']}
        for cal in calculation_field:
            i = 1
            for cal_val in calculation_field[cal]:
                ins_query = "insert into graph_calculation_table \
                (user_id,table_name,graph_cal_id,graph_cal_name) \
                values('%s','%s',%s,'%s')\
                " % (user_id, cal, i, cal_val)
                cursor.execute(ins_query)
                i += 1
        global_db.commit()

        # Entry for interface
        e1_port = ['port1', 'port2', 'port3', 'port4']
        idu4_port = ['odu', 'eth0', 'eth1']
        interface_field = {
            'idu4PortStatistics': idu4_port, 'idu4swPrimary': idu4_port,
            'idu4swSecondary': idu4_port, 'idu4e1port': e1_port}
        for table in interface_field:
            i = 0
            j = 0
            if table == 'idu4e1port':
                j = 1
            for interface in interface_field[table]:
                if i == 0:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)\
                    " % (user_id, table, j, interface, 1)
                else:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected)\
                    values ('%s','%s',%s,'%s',%s)\
                    " % (user_id, table, j, interface, 0)
                i += 1
                if table != 'idu4e1port' and i == 1:
                    j += 2
                else:
                    j += 1
                cursor.execute(ins_query)
        global_db.commit()

        #        get_coloum="SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE graph_name='%s' AND user_id='%s'"%('ap25_statisticsTable',user_id)
        #        cursor.execute(get_coloum)
        #        coloum_result=cursor.fetchall()
        #        table_field_dict=dict((field[0],field[1]) for field in coloum_result)

        # interface value
        graph_field = {'idu4NWBandwidth': ['rxPackets', 'txPackets', 'rxBytes', 'txBytes', 'rxErrors', 'txErrors'],
                       'idu4TDMOIPBandwidth': ['bytesTransmitted', 'bytesReceived'],
                       'idu4PortStatistics': ['framerx', 'frametx'],
                       'idu4outage': ['Reachable', 'Unreachable'],
                       'idu4e1port': ['bpv'],
                       'idu4swPrimary': ['framesRx', 'framesTx', 'inGoodOctets', 'inBadOctets'],
                       'idu4swSecondary': ['inUnicast', 'outUnicast', 'inBroadcast', 'outBroadcast', 'inMulticast',
                                           'outMulricast']}

        graph_display_name = {
        'idu4NWBandwidth': ['Rx Packets', 'Tx Packets', 'Rx Bytes', 'Tx Bytes', 'Rx Error', 'Tx Error'],
        'idu4TDMOIPBandwidth': ['Tx Bytes', 'Rx Bytes'],
        'idu4PortStatistics': ['Rx Frame', 'Tx Frame'],
        'idu4outage': ['Reachable', 'Unreachable'],
        'idu4e1port': ['BPV Error Count'],
        'idu4swPrimary': ['Rx Frames', 'Tx Frames', 'Good In Octets', 'Bad In Octets'],
        'idu4swSecondary': ['In Unicast', 'Out Unicast', 'In Broadcast', 'Out Broadcast', 'In Multicast',
                            'Out Mulricast']}

        tool_tip_name = {'idu4NWBandwidth': ['(pps)', '(pps)', '(bps)', '(bps)', '(error)', '(error)'],
                         'idu4TDMOIPBandwidth': ['(bps)', '(bps)'], 'idu4PortStatistics': ['(fps)', '(fps)'],
                         'idu4outage': ['(%)', '(%)'], 'idu4e1port': ['(bpv)'],
                         'idu4swPrimary': ['(frames)', '(frames)', '(octets)', '(octets)'],
                         'idu4swSecondary': ['(packets)', '(packets)', '(packets)', '(packets)', '(packets)',
                                             '(packets)']}

        for field in graph_field:
            i = 0
            for name in graph_field[field]:
                if i < 2:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                else:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')\
                    " % (user_id, field, name, graph_display_name[field][i], 0, tool_tip_name[field][i])
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        ajax_data = {'idu4NWBandwidth': ['idu4NWBandwidth', 'sp_common_graph_creation.py', 'post',
                                         'idu_iduNetworkStatisticsTable,timestamp,interfaceName,idu4NWBandwidth'],
                     'idu4TDMOIPBandwidth': ['idu4TDMOIPBandwidth', 'sp_common_graph_creation.py', 'post',
                                             'idu_tdmoipNetworkInterfaceStatisticsTable,timestamp,indexid,idu4TDMOIPBandwidth'],
                     'idu4PortStatistics': ['idu4PortStatistics', 'sp_common_graph_creation.py', 'post',
                                            'idu_portstatisticsTable,timestamp,softwarestatportnum,idu4PortStatistics'],
                     'idu4outage': ['idu4outage', 'sp_common_graph_creation.py', 'post',
                                    'outage,timestamp,noIndexName,idu4outage'],
                     'idu4e1port': ['idu4e1port', 'sp_common_graph_creation.py', 'post',
                                    'idu_e1PortStatusTable,timestamp,portNum,idu4e1port'],
                     'idu4swPrimary': ['idu4swPrimary', 'sp_common_graph_creation.py', 'post',
                                       'idu_swPrimaryPortStatisticsTable,timestamp,swportnumber,idu4swPrimary'],
                     'idu4swSecondary': ['idu4swSecondary', 'sp_common_graph_creation.py', 'post',
                                         'idu_portSecondaryStatisticsTable,timestamp,switchPortNum,idu4swSecondary']}
        for data in ajax_data:
            sql = "insert into graph_ajax_call_information \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, ajax_data[data][0], ajax_data[data][1], ajax_data[data][2], ajax_data[data][3])
            cursor.execute(sql)
        global_db.commit()

        # total_data={'apVAPUserConnect':['apVAPUserConnect','ap_total_data_count.py','post','ap25_vapClientStatisticsTable,addressMAC']}
        total_data = {}
        for count_data in total_data:
            sql = "insert into total_count_item \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, total_data[count_data][0], total_data[count_data][1], total_data[count_data][2],
                 total_data[count_data][3])
            cursor.execute(sql)
        global_db.commit()

    except Exception, e:
        output_dict = {'success': 1, 'result': str(e[-1])}
        return output_dict


def idu_status_info_new_user(user_id):
    """

    @param user_id:
    @return:
    """
    try:
        global global_db
        if global_db.open != 1:
            db_connect()

        cursor = global_db.cursor()

        #['idu4linkstatustable','Link Status',0,'idu4',1,1,1,0,0,5,180,-1,1,1,1,1,1,'E1 Port Status','Status',300,0,1]
        default_temp_list = [
            ['idu4e1portstatus', 'E1 Port Status', 0, 'idu4', 1, 1, 1, 0, 0, 5, 180, -1, 1, 1, 1, 1, 1,
             'E1 Port Status', 'Status', 300, 0, 1],
            ['idu4linkstatustable', 'Link Status', 0, 'idu4', 1, 1, 1, 0, 0, 5, 180, -1, 1, 1, 1, 1, 1, 'Link Status',
             'Status', 300, 0, 1]]
        for default_temp in default_temp_list:
            ins_temp_query = "INSERT INTO  `graph_templet_table` \
            (`graph_display_id` ,`graph_display_name` ,`user_id` ,`is_disabled` ,`device_type_id` ,\
            `graph_id` ,`graph_tab_option` ,`refresh_button` , `next_pre_option` ,`start_value` ,\
            `end_value` ,`graph_width` ,`graph_height` ,`graph_cal_id` ,`show_type` ,`show_field` ,\
            `show_cal_type` ,`show_tab_option`,`graph_title`,`graph_subtitle`,`auto_refresh_time_second`,`is_deleted`,`dashboard_type`)\
            VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s,'%s','%s' ,'%s',%s,%s,%s)\
            " % (default_temp[0], default_temp[1], user_id, default_temp[2], default_temp[3], default_temp[4],
                 default_temp[5], default_temp[6], default_temp[
                7], default_temp[8], default_temp[9], default_temp[10],
                 default_temp[11], default_temp[
                12], default_temp[13], default_temp[14], default_temp[15],
                 default_temp[16], default_temp[17], default_temp[18], default_temp[19], default_temp[20],
                 default_temp[21])
            cursor.execute(ins_temp_query)
        global_db.commit()

        # interface value

        # Entry for interface
        idu4_port = ['Port1', 'Port2', 'Port3', 'Port4']
        interface_field = {'idu4linkstatustable': idu4_port}
        for table in interface_field:
            i = 0
            for interface in interface_field[table]:
                if i == 0:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)\
                    " % (user_id, table, i + 1, interface, 1)
                else:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)" % (user_id, table, i + 1, interface, 0)
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        #,'idu4linkstatustable':['opStatus','los','lof','ais','rai','rxFrameSlip','txFrameSlip','bpv','adptClkState','holdOverStatus']
        graph_field = {'idu4e1portstatus': ['opStatus', 'lof', 'ais', 'rai', 'rxFrameSlip', 'txFrameSlip', 'bpv',
                                            'adptClkState', 'holdOverStatus'],
                       'idu4linkstatustable': ['operationalStatus', 'minJBLevel', 'maxJBLevel', 'underrunOccured',
                                               'overrunOccured']}

        graph_display_name = {'idu4e1portstatus': ['State', 'LOS', 'LOF', 'AIS', 'RAI', 'Rx Frame',
                                                   'Tx Frame', 'BPV', 'Adaptive State', 'Hold State'],
                              'idu4linkstatustable': ['State', 'Min JBLevel', 'Max JBLevel', 'Under-Run Occured',
                                                      'Over-Run Occured']}

        tool_tip_name = {'idu4e1portstatus': ['', '', '', '', '', '', '', '', '', ''],
                         'idu4linkstatustable': ['', '', '', '', '']}
        for field in graph_field:
            i = 0
            for name in graph_field[field]:
                if i < 2:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                else:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        ajax_data = {'idu4e1portstatus': ['idu4e1portstatus', 'sp_common_status_table_creation.py',
                                          'post', 'idu_e1PortStatusTable,timestamp,portNum,idu4e1portstatus'],
                     'idu4linkstatustable': ['idu4linkstatustable', 'sp_common_status_table_creation.py',
                                             'post', 'idu_linkStatusTable,timestamp,portNum,idu4linkstatustable']}
        for data in ajax_data:
            sql = "insert into graph_ajax_call_information \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, ajax_data[data][0], ajax_data[data][1], ajax_data[data][2], ajax_data[data][3])
            cursor.execute(sql)
        global_db.commit()

        total_data = {}
        for count_data in total_data:
            sql = "insert into total_count_item \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, total_data[count_data][0], total_data[count_data][1], total_data[count_data][2],
                 total_data[count_data][3])
            cursor.execute(sql)
        global_db.commit()
    except Exception, e:
        output_dict = {'success': 1, 'result': str(e[-1])}
        return output_dict


def odu100_add_status_info__for_new_user(user_id):
    """

    @param user_id:
    @return:
    """
    try:
        db_connect()
        global global_db
        cursor = global_db.cursor()

        default_temp_list = [
            ['odu100NWstatus', 'Network Bandwidth Status', 0, 'odu100', 1, 1, 1, 0, 0, 5, 180, -1, 1, 1, 1, 1, 1,
             'Network Bandwidth Status', 'Status', 300, 0, 1],
            ['odu100syncstatus', 'Sync Status', 0, 'odu100', 1, 1, 1, 0, 0, 5, 180,
             -1, 1, 1, 1, 1, 1, 'Sync Status', 'Status', 300, 0, 1],
            ['odu100Rastatus', 'Radio Status', 0, 'odu100', 1, 1, 1, 0, 0, 5, 180, -1, 1, 1, 1, 1, 1, 'Radio Status',
             'Status', 300, 0, 1]]
        for default_temp in default_temp_list:
            ins_temp_query = "INSERT INTO  `graph_templet_table` \
            (`graph_display_id` ,`graph_display_name` ,`user_id` ,`is_disabled` ,`device_type_id` ,`graph_id` ,`graph_tab_option` ,\
            `refresh_button` , `next_pre_option` ,`start_value` ,`end_value` ,`graph_width` ,`graph_height` ,`graph_cal_id` ,\
            `show_type` ,`show_field` ,`show_cal_type` ,`show_tab_option`,`graph_title`,`graph_subtitle`,\
            `auto_refresh_time_second`,`is_deleted`,`dashboard_type`)\
            VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s,'%s','%s' ,'%s',%s,%s,%s)\
            " % (default_temp[0], default_temp[1], user_id, default_temp[2], default_temp[3], default_temp[4],
                 default_temp[5], default_temp[
                6], default_temp[7], default_temp[8], default_temp[9],
                 default_temp[10], default_temp[
                11], default_temp[12], default_temp[13], default_temp[14],
                 default_temp[15], default_temp[
                16], default_temp[17], default_temp[18], default_temp[19],
                 default_temp[20], default_temp[21])
            cursor.execute(ins_temp_query)
        global_db.commit()

        # interface value
        graph_field = {'odu100NWstatus': ['nwInterfaceName', 'operationalState', 'macAddress'],
                       'odu100syncstatus': ['syncoperationalState', 'syncrasterTime', 'timerAdjust',
                                            'syncpercentageDownlinkTransmitTime'],
                       'odu100Rastatus': ['currentTimeSlot', 'raMacAddress', 'raoperationalState', 'unusedTxTimeUL',
                                          'unusedTxTimeDL']}

        graph_display_name = {'odu100NWstatus': ['Inteface Name', 'State', 'MAC Address'],
                              'odu100syncstatus': ['State', 'Raster Time', 'Adjust Timer', 'DW Link TX'],
                              'odu100Rastatus': ['Time Slot', 'RA MAC Address', 'State', 'Unused TX UL',
                                                 'Unused TX DL']}

        tool_tip_name = {'odu100NWstatus': ['', '', ''], 'odu100syncstatus': ['', '', '',
                                                                              '(%)'],
                         'odu100Rastatus': ['', '', '', '(usec)', '(usec)']}

        for field in graph_field:
            i = 0
            for name in graph_field[field]:
                if i < 2:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                else:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')" % (
                    user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        ajax_data = {'odu100NWstatus': ['odu100NWstatus', 'sp_common_status_table_creation.py', 'post',
                                        'odu100_nwInterfaceStatusTable,timestamp,nwStatusIndex,odu100NWstatus'],
                     'odu100syncstatus': ['odu100syncstatus', 'sp_common_status_table_creation.py', 'post',
                                          'odu100_synchStatusTable,timestamp,syncConfigIndex,odu100syncstatus'],
                     'odu100Rastatus': ['odu100Rastatus', 'sp_common_status_table_creation.py', 'post',
                                        'odu100_raStatusTable,timestamp,raIndex,odu100Rastatus']}
        for data in ajax_data:
            sql = "insert into graph_ajax_call_information \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, ajax_data[data][0], ajax_data[data][1], ajax_data[data][2], ajax_data[data][3])
            cursor.execute(sql)
        global_db.commit()

        total_data = {}
        for count_data in total_data:
            sql = "insert into total_count_item \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, total_data[count_data][0], total_data[count_data][1], total_data[count_data][2],
                 total_data[count_data][3])
            cursor.execute(sql)
        global_db.commit()
    except Exception, e:
        output_dict = {'success': 1, 'result': str(e[-1])}
        return output_dict


def ap_client_data_new_user(user_id):
    """

    @param user_id:
    """
    try:

        # first graph_id and second value is table name#
        global global_db
        if global_db.open != 1:
            db_connect()
        cursor = global_db.cursor()

        default_temp_list = [
            ['apClientBandwidth', 'Client Bandwidth Statistics', 0, 'ap25', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Client Bandwidth Statistics', 'Statistics', 600, 0, 2],
            ['apClientRssi', 'Client RSSI', 0, 'ap25', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1, 'Client RSSI', '',
             600, 0, 2]]
        for default_temp in default_temp_list:
            ins_temp_query = "INSERT INTO  `graph_templet_table` \
            (`graph_display_id` ,`graph_display_name` ,`user_id` ,`is_disabled` ,\
            `device_type_id` ,`graph_id` ,`graph_tab_option` ,`refresh_button` , \
            `next_pre_option` ,`start_value` ,`end_value` ,`graph_width` ,`graph_height` ,\
            `graph_cal_id` ,`show_type` ,`show_field` ,`show_cal_type` ,`show_tab_option`,\
            `graph_title`,`graph_subtitle`,`auto_refresh_time_second`,`is_deleted`,`dashboard_type`)\
    VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'%s','%s' ,\
    '%s',%s,%s,%s)" % (default_temp[0], default_temp[1], user_id, default_temp[2],
                       default_temp[3], default_temp[
                4], default_temp[5], default_temp[6],
                       default_temp[7], default_temp[
                8], default_temp[9], default_temp[10],
                       default_temp[11], default_temp[
                12], default_temp[13], default_temp[14],
                       default_temp[15], default_temp[
                16], default_temp[17], default_temp[18],
                       default_temp[19], default_temp[20], default_temp[21])
            cursor.execute(ins_temp_query)
        global_db.commit()

        # Entry for calculation type
        calculation_field = {'apClientBandwidth': ['Total'],
                             'apClientRssi': ['Total']}
        for cal in calculation_field:
            i = 1
            for cal_val in calculation_field[cal]:
                ins_query = "insert into graph_calculation_table \
                (user_id,table_name,graph_cal_id,graph_cal_name)\
                values('%s','%s',%s,'%s')\
                " % (user_id, cal, i, cal_val)
                cursor.execute(ins_query)
                i += 1
        global_db.commit()

        # Entry for interface
        interface_field = {}
        for table in interface_field:
            i = 0
            for interface in interface_field[table]:
                if i == 0:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)\
                    " % (user_id, table, i, interface, 1)
                else:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)" % (user_id, table, i, interface, 0)
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        # interface value
        graph_field = {'apClientBandwidth': ['txRate', 'rxRate'],
                       'apClientRssi': ['rssi']}
        graph_display_name = {'apClientBandwidth': ['Tx Rate',
                                                    'Rx Rate'], 'apClientRssi': ['RSSI']}
        tool_tip_name = {'apClientBandwidth': ['(Mbps)', '(Mbps)'],
                         'apClientRssi': ['(dBm)']}
        for field in graph_field:
            i = 0
            for name in graph_field[field]:
                if i < 2:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')\
                    " % (user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                else:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')\
                    " % (user_id, field, name, graph_display_name[field][i], 0, tool_tip_name[field][i])
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        ajax_data = {'apClientBandwidth': ['apClientBandwidth', 'client_graph_creation.py', 'post',
                                           'ap25_vapClientStatisticsTable,timestamp,addressMAC,apClientBandwidth'],
                     'apClientRssi': ['apClientRssi', 'client_graph_creation.py', 'post',
                                      'ap25_vapClientStatisticsTable,timestamp,addressMAC,apClientRssi']}
        for data in ajax_data:
            sql = "insert into graph_ajax_call_information \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, ajax_data[data][0], ajax_data[data][1], ajax_data[data][2], ajax_data[data][3])
            cursor.execute(sql)
        global_db.commit()

        total_data = {}
        for count_data in total_data:
            sql = "insert into total_count_item \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, total_data[count_data][0], total_data[count_data][1], total_data[count_data][2],
                 total_data[count_data][3])
            cursor.execute(sql)
        global_db.commit()

    except Exception, e:
        output_dict = {'success': 1, 'result': str(e[-1])}
        print output_dict


def ccu_add_graph_entry_for_new_user(user_id):
    """

    @param user_id:
    """
    try:
        global global_db
        if global_db.open != 1:
            db_connect()
        cursor = global_db.cursor()

        # Template Entry
        default_temp_list = [
            ['ccutemp', 'Temperature Statistics', 1, 'ccu', 1, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 1,
             'Temperature Statistics', 'Statistics', 600, 0],
            ['ccuvolt', 'Voltage Statistics', 1, 'ccu', 0, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'Voltage Statistics', '', 600, 0],
            ['ccucurrent', 'Current Statistics', 1, 'ccu', 0, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'Current Statistics', '', 600, 0],
            ['ccuoutage', 'Device Reachability Statistics', 0, 'ccu', 2, 1, 0, 0, 0, 5, 180, 250, 1, 1, 1, 1, 0,
             'Reachability Statistics', '', 600, 0]]
        for default_temp in default_temp_list:
            ins_temp_query = "INSERT INTO  `graph_templet_table` \
            (`graph_display_id` ,`graph_display_name` ,`user_id` ,`is_disabled` ,`device_type_id` ,`graph_id` ,\
            `graph_tab_option` ,`refresh_button` , `next_pre_option` ,`start_value` ,`end_value` ,\
            `graph_width` ,`graph_height` ,`graph_cal_id` ,`show_type` ,`show_field` ,\
            `show_cal_type` ,`show_tab_option`,`graph_title`,`graph_subtitle`,`auto_refresh_time_second`,`is_deleted`)\
            VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s,'%s','%s' ,'%s',%s,%s)\
            " % (default_temp[0], default_temp[1], user_id, default_temp[2],
                 default_temp[3], default_temp[
                4], default_temp[5], default_temp[6],
                 default_temp[7], default_temp[
                8], default_temp[9], default_temp[10],
                 default_temp[11], default_temp[
                12], default_temp[13], default_temp[14],
                 default_temp[15], default_temp[16], default_temp[17], default_temp[18], default_temp[19],
                 default_temp[20])
            cursor.execute(ins_temp_query)
        global_db.commit()

        # Calculation Entry
        calculation_field = {'ccutemp': ['Total'], 'ccuvolt': [
            'Total'], 'ccucurrent': ['Total'], 'ccuoutage': ['Total']}
        for cal in calculation_field:
            i = 1
            for cal_val in calculation_field[cal]:
                ins_query = "insert into graph_calculation_table \
                (user_id,table_name,graph_cal_id,graph_cal_name) \
                values('%s','%s',%s,'%s')\
                " % (user_id, cal, i, cal_val)
                cursor.execute(ins_query)
                i += 1
        global_db.commit()

        # Interface Entry
        interface_field = {}
        for table in interface_field:
            i = 0
            for interface in interface_field[table]:
                if i == 0:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)" % (user_id, table, i + 1, interface, 1)
                else:
                    ins_query = "insert into graph_interface_table \
                    (user_id,graph_name,interface_value,interface_display_name,is_selected) \
                    values ('%s','%s',%s,'%s',%s)\
                    " % (user_id, table, i + 1, interface, 0)
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        # Graph Field Entry
        graph_field = {
        'ccutemp': ['ccuRTSInternalTemperature', 'ccuRTSBatteryAmbientTemperature', 'ccuRTSSMPSTemperature'],
        'ccuvolt': ['ccuRTSSystemVoltage', 'ccuRTSACVoltageReading'],
        'ccucurrent': ['ccuRTSSolarCurrent', 'ccuRTSSMPSCurrent', 'ccuRTSBatteryCurrent', 'ccuRTSLoadCurrent',
                       'ccuRTSBatterySOC'],
        'ccuoutage': ['Reachable', 'Unreachable']}
        graph_display_name = {'ccutemp': ['Internal Temperature', 'Battery Temperature', 'SMPS Temperature'],
                              'ccuvolt': ['System Voltage', 'AC Voltage Reading'],
                              'ccucurrent': ['Solar Current', 'SMPS Current', 'Battery Current', 'Load Current',
                                             'Battery SOC'],
                              'ccuoutage': ['Reachable', 'Unreachable']}

        tool_tip_name = {'ccutemp': ['*C', '*C', '*C'],
                         'ccuvolt': ['mV', 'V'],
                         'ccucurrent': ['mA', 'mA', 'mA', 'mA', '%%'],
                         'ccuoutage': ['Reachable', 'Unreachable']}

        for field in graph_field:
            i = 0
            for name in graph_field[field]:
                if i < 2:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')\
                    " % (user_id, field, name, graph_display_name[field][i], 1, tool_tip_name[field][i])
                else:
                    ins_query = "insert into graph_field_table \
                    (user_id,graph_name,graph_field_value,graph_field_display_name,is_checked,tool_tip_title) \
                    values ('%s','%s','%s','%s',%s,'%s')\
                    " % (user_id, field, name, graph_display_name[field][i], 0, tool_tip_name[field][i])
                i += 1
                cursor.execute(ins_query)
        global_db.commit()

        # Ajax Call Entry
        ajax_data = {'ccutemp': ['ccutemp', 'sp_common_graph_creation.py', 'post',
                                 'ccu_ccuRealTimeStatusTable,timestamp,ccuRTSIndex,ccutemp'],
                     'ccuvolt': ['ccuvolt', 'sp_common_graph_creation.py', 'post',
                                 'ccu_ccuRealTimeStatusTable,timestamp,ccuRTSIndex,ccuvolt'],
                     'ccucurrent': ['ccucurrent', 'sp_common_graph_creation.py', 'post',
                                    'ccu_ccuRealTimeStatusTable,timestamp,ccuRTSIndex,ccucurrent'],
                     'ccuoutage': ['ccuoutage', 'sp_common_graph_creation.py', 'post',
                                   'outage,timestamp,noIndexName,ccuoutage']}
        for data in ajax_data:
            sql = "insert into graph_ajax_call_information \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, ajax_data[data][0], ajax_data[data][1], ajax_data[data][2], ajax_data[data][3])
            cursor.execute(sql)
        global_db.commit()

        total_data = {}
        for count_data in total_data:
            sql = "insert into total_count_item \
            (user_id,graph_id,url,method,other_data) \
            values('%s','%s','%s','%s','%s')\
            " % (user_id, total_data[count_data][0], total_data[count_data][1], total_data[count_data][2],
                 total_data[count_data][3])
            cursor.execute(sql)
        global_db.commit()

    except Exception, e:
        output_dict = {'success': 1, 'result': str(e[-1])}
        print output_dict


def count_user():
    """


    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return "db_not_connected"
        query = "SELECT count(*) from users"
        cursor = global_db.cursor()
        no_of_users = ()
        if cursor.execute(query) != 0:
            no_of_users = cursor.fetchall()
        cursor.close()
        db_close()
        if len(no_of_users) < 1:
            return " count is none "
        else:
            return int(no_of_users[0][0])
    except Exception as e:
        return " exception "
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def get_group_list():
    """


    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        query = "select `group_name`,`group_id` from groups where `is_deleted` <> 1"
        cursor = global_db.cursor()
        groupName_list = ()
        if cursor.execute(query) != 0:
            groupName_list = cursor.fetchall()
        cursor.close()
        db_close()
        if len(groupName_list) < 1:
            return 1
        else:
            return groupName_list

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def get_group_name(revieved_id, flag=0):
    """

    @param revieved_id:
    @param flag:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if flag:
            query = "SELECT group_name from groups where group_id = \"%s\" " % (
                revieved_id)
        else:
            query = "SELECT gp.group_name from groups as gp JOIN users_groups as ug ON gp.group_id = ug.group_id WHERE ug.user_id = \"%s\" " % (
            revieved_id)
        cursor = global_db.cursor()
        group_name = ""
        if cursor.execute(query) != 0:
            group_name = cursor.fetchall()
        cursor.close()
        db_close()
        if len(group_name) < 1:
            return ""
        else:
            return group_name[0][0]
    except Exception as e:
        return " exception "
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def get_group_users(groupID):
    """

    @param groupID:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        query = "SELECT ug.user_id, ul.user_name, u.first_name, u.last_name \
        FROM users_groups AS ug \
        INNER JOIN users AS u ON ug.user_id = u.user_id INNER JOIN user_login AS ul ON ug.user_id = ul.user_id \
        WHERE group_id = \"%s\"" % groupID
        gpUsers_tuple = ()
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            gpUsers_tuple = cursor.fetchall()
        cursor.close()
        db_close()
        if len(gpUsers_tuple) < 1:
            return 1
        else:
        # make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
        # gpUsers_list = []
        # for gpUser in gpUsers_tuple:
        #     gpUsers_list.append(make_list(gpUser))
            return gpUsers_tuple
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


# print "hi",get_group_users("a0564ece-f668-11e0-a835-f04da24c7c26")

def get_group_info(groupID):
    """

    @param groupID:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        query = "SELECT roles.role_name, groups.updated_by, groups.timestamp, groups.created_by, groups.creation_time \
        FROM groups \
        INNER JOIN roles ON roles.role_id = groups.role_id \
        WHERE groups.group_id = \"%s\"" % groupID
        gpDetail_tuple = ()
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            gpDetail_tuple = cursor.fetchone()
        cursor.close()
        db_close()
        if len(gpDetail_tuple) < 1:
            return 1
        else:
        #            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
        #            return make_list(gpDetail_tuple)
            return gpDetail_tuple
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def del_user_from_group(user_ids_list, flag=1):
    """

    @param user_ids_list:
    @param flag:
    @return:
    """
    db_connect()
    global global_db
    flag2 = 1
    try:
        delQuery = "delete from users_groups where "
        i = 0
        for user_id in user_ids_list:
            i += 1
            if len(user_ids_list) == i:
                delQuery += "`user_id` = \"%s\" " % user_id
            else:
                delQuery += "`user_id` = \"%s\" OR" % user_id

        if flag == 1:
            selQuery = "SELECT group_id FROM groups WHERE group_name = 'Default'"

            insQuery = "INSERT INTO `users_groups` (`user_group_id`, `user_id`, `group_id`) values"
            flag2 == 0

        cursor = global_db.cursor()
        if cursor.execute(delQuery) < 1:
            cursor.close()
            db_close()
            return 2

        if flag == 1 and flag2 == 1:
            if cursor.execute(selQuery) != 1:
                cursor.close()
                db_close()
                return 2
            else:
                default_id = cursor.fetchone()

            selectQuery = "SELECT user_id FROM `users_groups` WHERE \"%s\" " % default_id
            cursor.execute(selectQuery)

            ids_tuple = cursor.fetchall()

            f = lambda x: tuple(j[0] for j in x)

            ids_tuple = f(ids_tuple)

            i = 0
            for id in user_ids_list:
                i += 1
                try:
                    ids_tuple.index(id)
                except ValueError as e:
                    is_ins = 0
                    if i == len(user_ids_list):
                        insQuery += " (uuid(),\"%s\",\"%s\") " % (
                            id, default_id[0])
                    else:
                        insQuery += " (uuid(),\"%s\",\"%s\") ," % (
                            id, default_id[0])

            if is_ins == 0:
                cursor.execute(insQuery)
            else:
                pass  # print "insert NOT happening"

        else:
            pass
        global_db.commit()
        cursor.close()
        if flag == 1:
            db_close()
        elif flag == 0:
            pass
        else:
            db_close()

        return 0

    except Exception as e:
        return 111


def add_user_in_group(user_ids_list, newGroupID):
    """

    @param user_ids_list:
    @param newGroupID:
    @return:
    """
    global global_db
    try:
        insQuery = "insert into users_groups  (`user_group_id`, `user_id`, `group_id`) values"

        i = 0
        for uid in user_ids_list:
            i += 1
            if i == len(user_ids_list):
                insQuery += " (uuid(),\"%s\",\"%s\") " % (uid, newGroupID)
            else:
                insQuery += " (uuid(),\"%s\",\"%s\") ," % (uid, newGroupID)

        delResult = del_user_from_group(user_ids_list, 0)

        if delResult != 0:
            return 1

        if global_db.open != 1:
            return 1

        cursor = global_db.cursor()

        if cursor.execute(insQuery) < 1:
            cursor.close()
            db_close()
            return 3
        global_db.commit()
        cursor.close()
        db_close()
        return 0

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()

            # print
            # addUserInGroup('bb347a54-f668-11e0-a835-f04da24c7c26','4c83a918-f668-11e0-a835-f04da24c7c26')

            # Edit start :
            # Redmine Issue: Features
            # 687: "User Management Password Complexity"
            # 730: "Password Storage in Encrypted Form"
            # Description:
            # Password 2 num, 2 alpha, 2 special,
            # min 8 characters and Password SHA format
            # By: Grijesh Chauhan, Date: 7, Feb 2013


def add_user(u_dict, ul_dict, ug_dict):
    """

    @param u_dict:
    @param ul_dict:
    @param ug_dict:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        userID = uuid.uuid1()
        u_dict['user_id'] = userID
        ul_dict['user_id'] = userID
        ug_dict['user_id'] = userID

        insQuery1 = """INSERT INTO `users`(`user_id`,
                                            `first_name`,
                                            `last_name`,
                                            `designation`,
                                            `company_name`,
                                            `mobile_no`,
                                            `address`,
                                            `city_id`,
                                            `state_id`,
                                            `country_id`,
                                            `email_id`)
                                    VALUES (\"%(user_id)s\",
                                            \"%(first_name)s\", 
                                            \"%(last_name)s\", 
                                            \"%(designation)s\",
                                            \"%(company)s\", 
                                            \"%(mobile)s\", 
                                            \"%(address)s\", 
                                            NULL, 
                                            NULL, 
                                            NULL, 
                                            \"%(email_id)s\")
                    """ % u_dict

        ul_dict['password'] = global_db.escape_string(ul_dict['password'])
        insQuery2 = """INSERT INTO `user_login`(`user_login_id`, 
                                                `user_id`, 
                                                `user_name`, 
                                                `password`, 
                                                `timestamp`, 
                                                `created_by`, 
                                                `creation_time`, 
                                                `is_deleted`, 
                                                `updated_by`, 
                                                `nms_id`,
                                                `change_password_date`) 
                                        VALUES (UUID(), 
                                                \"%(user_id)s\", 
                                                \"%(user_name)s\", 
                                                SHA('%(password)s'), 
                                                '0000-00-00 00:00:00',
                                                \"%(created_by)s\",
                                                CURRENT_TIMESTAMP, 
                                                '0', 
                                                NULL, 
                                                NULL,
                                                NOW() )
                    """ % ul_dict

        insQuery3 = """INSERT INTO `users_groups` (`user_group_id`, 
                                                   `user_id`, 
                                                   `group_id`) 
                                        VALUES (UUID(), 
                                                \"%(user_id)s\", 
                                                \"%(groups)s\")
                    """ % ug_dict

        cursor = global_db.cursor()

        if cursor.execute(insQuery1) != 1:
            cursor.close()
            db_close()
            return 3
        if cursor.execute(insQuery2) != 1:
            cursor.close()
            db_close()
            return 3
        if cursor.execute(insQuery3) != 1:
            cursor.close()
            db_close()
            return 3
        global_db.commit()
        cursor.close()
        db_close()
        ap_add_default_data_new_user(userID)
        odu16_add_graph_info_new_user(userID)
        odu100_add_graph_info_new_user(userID)
        idu4_add_graph_info_new_user(userID)
        odu100_add_status_info__for_new_user(userID)
        ap_client_data_new_user(userID)
        idu_status_info_new_user(userID)
        ccu_add_graph_entry_for_new_user(userID)
        db_close()
        return 0
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()

# Edit end

def check_name(name, type):
    """

    @param name:
    @param type:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if type == "user":
            selectQuery = "SELECT user_name FROM `user_login` WHERE `user_name` = \"%s\"" % name.strip(
            )
        elif type == "group":
            selectQuery = "SELECT group_name FROM `groups` WHERE `group_name` = \"%s\"" % name.strip()
        else:
            db_close()
            return 1
        cursor = global_db.cursor()
        queryVal = cursor.execute(selectQuery)
        result = 1
        if queryVal == 0:
            result = 0
        elif queryVal == 1:
            result = 1
        else:
            result = 1
        cursor.close()
        db_close()
        return result

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def groupname_avail(gpname):
    """

    @param gpname:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        selectQuery = "SELECT group_name FROM `groups` WHERE `group_name` = \"%s\"" % gpname.strip(
        )
        cursor = global_db.cursor()
        queryVal = cursor.execute(selectQuery)
        result = 1
        if queryVal == 0:
            result = 0
        elif queryVal == 1:
            result = 11
        else:
            result = 11
        cursor.close()
        db_close()
        return result

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def is_loggedin_users(user_list):
    """

    @param user_list:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        selectQuery = "SELECT user_name FROM login_info WHERE user_name IN ( %s ) and is_logged_in = 1 " % (
            str(user_list)[1:-1])
        cursor = global_db.cursor()
        queryVal = cursor.execute(selectQuery)
        result = 1
        if queryVal == 0:
            result = 0
        else:
            query_result = cursor.fetchall()
            result = [i[0] for i in query_result]
        cursor.close()
        db_close()
        return result

    except Exception as e:
        return 1
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def del_user(user_ids_list, flag=1):
    """

    @param user_ids_list:
    @param flag:
    @return:
    """
    db_flag = 1
    if flag != 0:
        db_connect()
        db_flag = 0
    else:
        pass
    global global_db
    try:
        if global_db.open != 1:
            return 1

        delQuery = "delete from users where "
        #        del_query1 = "DELETE FROM total_count_item WHERE "
        #        del_query2 = "DELETE FROM graph_ajax_call_information WHERE "
        #        del_query3 = "DELETE FROM graph_calculation_table WHERE "
        #        del_query4 = "DELETE FROM graph_field_table WHERE "
        #        del_query5 = "DELETE FROM graph_interface_table WHERE "
        #        del_query6 = "DELETE FROM graph_templet_table WHERE "
        #
        i = 0
        for user_id in user_ids_list:
            i += 1
            if len(user_ids_list) == i:
                delQuery += "user_id = \"%s\" " % user_id
            #                del_query1 += "user_id = \"%s\" "%user_id
            #                del_query2 += "user_id = \"%s\" "%user_id
            #                del_query3 += "user_id = \"%s\" "%user_id
            #                del_query4 += "user_id = \"%s\" "%user_id
            #                del_query5 += "user_id = \"%s\" "%user_id
            #                del_query6 += "user_id = \"%s\" "%user_id
            else:
                delQuery += "user_id = \"%s\" OR " % user_id
            #                del_query1 += "user_id = \"%s\" OR "%user_id
            #                del_query2 += "user_id = \"%s\" OR "%user_id
            #                del_query3 += "user_id = \"%s\" OR "%user_id
            #                del_query4 += "user_id = \"%s\" OR "%user_id
            #                del_query5 += "user_id = \"%s\" OR "%user_id
            #                del_query6 += "user_id = \"%s\" OR "%user_id
            #
        cursor = global_db.cursor()
        if cursor.execute(delQuery) >= 1:
        #            cursor.execute(del_query1)
        #            cursor.execute(del_query2)
        #            cursor.execute(del_query3)
        #            cursor.execute(del_query4)
        #            cursor.execute(del_query5)
        #            cursor.execute(del_query6)
            pass
        elif cursor.execute(delQuery) == 0:
            pass
        else:
            cursor.close()
            db_close()
            return 4
        global_db.commit()
        cursor.close()
        if flag == 0 and db_flag == 1:
            pass
        else:
            db_close()

        return 0

    except Exception as e:
        return 111
    finally:
        if flag and isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def del_enable_user(userID, value):
    """

    @param userID:
    @param value:
    @return:
    """
    db_connect()
    global global_db
    if global_db.open != 1:
        return 1

    updateQuery = "UPDATE user_login set `is_deleted` = %s where `user_id` = \"%s\"" % (
        value, userID)

    if cursor.execute(updateQuery) != 1:
        cursor.close()
        db_close()
        return 4
    global_db.commit()
    cursor.close()
    db_close()
    pass

def getStatus(user_list):
    (login_attempts_enable, 
            max_login_attempts, 
            lock_duration, 
            failure_interval,
            notify_user_onlock,
            notify_admin_onlock) = \
                SystemConfig.get_login_attempts_details()

    fail_attempts = user_list[-2]
    last_failed_timediff= user_list[-1]
    status = {
        True: "Lock", 
        False: "Unlock"
        }.get(
            is_account_locked( 
                fail_attempts,
                max_login_attempts,
                last_failed_timediff,
                lock_duration
            ), "Lock")            
    user_list[-2:]  =  (status,)
    return user_list


def edit_user_view(userID):
    """

    @param userID:
    @return:
    """
    db_connect()
    global global_db
    result = 1
    try:
        if global_db.open != 1:
            result = 1
        selectQuery = "SELECT ul.user_id,ul.`user_name`,g.`group_name`,u.`first_name`,u.`last_name`,\
        u.`designation`,u.`company_name`,u.`mobile_no`,u.`address`,u.`email_id` \
        , `ul`.`failed_login_attempts`, \
        TIMESTAMPDIFF(MINUTE, `ul`.`failed_login_time`, '%s' )\
        FROM users as u \
        INNER JOIN user_login as ul ON ul.user_id = u.user_id \
        INNER JOIN users_groups as ug ON ug.user_id = ul.user_id \
        INNER JOIN groups as g ON g.group_id = ug.group_id  \
        WHERE ul.user_id = \"%s\"" % (datetime.now(), userID)

        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            user_details = cursor.fetchone()
        else:
            cursor.close()
            db_close()
            return 11
        cursor.close()
        db_close()

        make_list = lambda x: [" " if i == None or i == '' else i for i in x]
        user_list = getStatus(make_list(user_details))
        user_list.append("red" if user_list[-1] == 'Lock' else "green")

        user_tuple = (
            'user_id', 'user_name', 'group_name', 'first_name', 'last_name',
            'designation', 'company', 'mobile', 'address', 'email_id', 'status', 'status_color')

        user_dict = dict(zip(user_tuple, user_list))

        return user_dict

    except Exception as e:
        return 111  # str(e) 
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def lock_unlock_usr(user_id, status):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        (login_attempts_enable, 
        max_login_attempts, 
        lock_duration, 
        failure_interval,
        notify_user_onlock,
        notify_admin_onlock) = SystemConfig.get_login_attempts_details()

        query = """ UPDATE `user_login` 
                    SET `failed_login_attempts` = {1}, 
                    `failed_login_time` = '{2}'
                    WHERE `user_id` = '{0}' 
                """.format(user_id, 
                        0 if status == 'Lock' else (max_login_attempts + 1),
                        datetime.now())
        message = 'Operation NOT successful'
        cursor = global_db.cursor()
        if cursor.execute(query):
            global_db.commit()
            if status == 'Lock':
                message = 'User Unlocked successfully' 
            else:
                message = 'User Locked for %d hours' % lock_duration
            return (True, message)
        else:
            return (False, message)
        cursor.close()
        db_close()
    except Exception as e:
        return (False, message)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()    

def edit_user(u_dict, ug_dict, pwd_dict=None):
    """

    @param u_dict:
    @param ug_dict:
    @param pwd_dict:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        updateQuery1 = """UPDATE `users`
                        set `first_name`= \"%(first_name)s\",`last_name`=\"%(last_name)s\",`designation`=\"%(designation)s\",
        `company_name`=\"%(company)s\", `mobile_no`=\"%(mobile)s\", `address`=\"%(address)s\", `email_id`=\"%(email_id)s\"
        WHERE `user_id`=\"%(user_id)s\"""" % u_dict

        updateQuery2 = """  UPDATE `users_groups` 
                            SET `group_id` = \"%(groups)s\" 
                            WHERE `user_id`=\"%(user_id)s\"
                        """ % ug_dict
        if pwd_dict:
            pwd_dict['passwd'] = global_db.escape_string(pwd_dict['passwd'])
            updateQuery3 = """UPDATE `user_login` 
                              SET `old_password`= `password`, `password` =  SHA('%(passwd)s'), `change_password_date` = NOW() 
                              WHERE `user_id` = \"%(user_id)s\"
                           """ % pwd_dict
        cursor = global_db.cursor()

        cursor.execute(updateQuery1)
        cursor.execute(updateQuery2)
        if pwd_dict:
            cursor.execute(updateQuery3)
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111 #str(e)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def get_group_details(flag=1):
    """

    @param flag:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if flag:
            selectQuery = "SELECT  g.`group_id`, g.group_name \
            FROM groups AS g \
            WHERE g.is_deleted <> 1 and g.group_name <> 'Default' and g.group_name <> 'SuperAdmin'"
        else:  # is superadmin
            selectQuery = "SELECT  g.`group_id`, g.group_name \
            FROM groups AS g \
            WHERE g.is_deleted <> 1 and g.group_name <> 'Default' "

        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            group_details = cursor.fetchall()
        cursor.close()
        db_close()
        if len(group_details) < 1:
            return 1
        else:
        #            make_list = lambda x: [" - " if i == None or i == '' else i for i in x]
        #            group_details_list = []
        #            for group_detail in group_details:
        #                group_details_list.append(make_list(group_detail))
            return group_details
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()

# print get_group_details()


def add_group(var_dict):
    """

    @param var_dict:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        insQuery = "insert into groups \
        (`group_id`, `group_name`, `description`, `timestamp`, \
        `created_by`, `creation_time`, `is_deleted`, `updated_by`, `role_id`) \
        VALUES (UUID(), \"%(group_name)s\", \"%(description)s\", '0000-00-00 00:00:00', \
        'SuperAdmin', CURRENT_TIMESTAMP, '0', NULL, \"%(role)s\")" % var_dict
        cursor = global_db.cursor()
        if cursor.execute(insQuery) != 1:
            cursor.close()
            db_close()
            return 3
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def edit_group(var_dict):
    """

    @param var_dict:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
            # updateQuery = """UPDATE groups SET `description` = "%(description)s",
        # `updated_by` = "%(session_user)s", `role_id` = "%(role)s" WHERE
        # group_id = "%(group_id)s" """%var_dict
        updateQuery = """UPDATE groups
        SET `description` = "%(description)s", `updated_by` = "%(session_user)s"
        WHERE group_id = "%(group_id)s" """ % var_dict
        cursor = global_db.cursor()
        if cursor.execute(updateQuery) != 1:
            pass
            #        cursor.close()
            #        db_close()
            #        return 3
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def del_group(groupID, del_users=1):
    """

    @param groupID:
    @param del_users:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        result = 1
        delQuery = "DELETE from groups WHERE groups.group_id = \"%s\" " % groupID
        cursor = global_db.cursor()
        if del_users == 0:
            selQuery = "SELECT users_groups.user_id FROM users_groups WHERE users_groups.group_id = \"%s\" " % groupID
            cursor.execute(selQuery)
            user_ids = cursor.fetchall()
            if len(user_ids) > 0:
                f = lambda user_ids: [ids[0] for ids in user_ids]
                result = del_user(f(user_ids), 0)
            else:
                result = 0
        if del_users == 0 and result != 0:
            return 11

        if cursor.execute(delQuery) != 1:
            pass

        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111  # str(e)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def del_group_copy(groupID, del_users=1):
    """

    @param groupID:
    @param del_users:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        if del_users == 0 and gpValue == 1:
            delQuery = "UPDATE user_login \
            INNER JOIN users_groups ON user_login.user_id = users_groups.user_id \
            INNER JOIN groups ON users_groups.group_id = groups.group_id SET user_login.is_deleted = 1,groups.is_deleted=1 \
            WHERE users_groups.group_id = \"%s\"" % ()
        else:
            delQuery = "DELETE from groups WHERE groups.group_id = \"%s\" " % groupID

        delQuery1 = "DELETE from users_groups where group_id = \"%s\" " % groupID
        cursor = global_db.cursor()
        if cursor.execute(delQuery) < 1:
        #            pass
            cursor.close()
            db_close()
            return 2
        if cursor.execute(delQuery) < 1:
        #            pass
            cursor.close()
            db_close()
            return 2
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def get_user_details():
    """


    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
            # selectQuery = "SELECT  ul.`user_id`, ul.user_name,  u.`first_name` ,
        # u.`last_name` , u.`designation` , u.`mobile_no` , u.`email_id` FROM
        # user_login AS ul INNER JOIN users AS u WHERE u.user_id = ul.user_id
        # AND ul.is_deleted <> 1"
        selectQuery = "SELECT  ul.`user_id`, ul.user_name, g.group_name, u.`first_name` , \
        u.`last_name` , u.`designation` , u.`mobile_no` , u.`email_id` \
        FROM user_login AS ul \
        INNER JOIN users AS u ON u.user_id = ul.user_id \
        INNER JOIN users_groups as ug ON ug.user_id=ul.user_id \
        INNER JOIN groups as g ON  ug.group_id = g.group_id \
        where  ul.is_deleted <> 1"
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            user_details = cursor.fetchall()
        cursor.close()
        db_close()
        if len(user_details) < 1:
            return 1
        else:
            make_list = lambda x: [
                " - " if i == None or i == '' else i for i in x]
            user_details_list = []
            for user_detail in user_details:
                user_details_list.append(make_list(user_detail))
            return user_details_list
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()

# print get_user_details()


def edit_group_view(group_id):
    """

    @param group_id:
    @return:
    """
    db_connect()
    global global_db
    result = 1
    try:
        if global_db.open != 1:
            result = 1

        selectQuery = """SELECT g.group_id, g.group_name, g.description, g.role_id
        FROM groups as g
        WHERE g.group_id = \"%s\" AND g.is_deleted <> 1""" % group_id
        group_details = ()
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            group_details = cursor.fetchone()
        else:
            cursor.close()
            db_close()
            return 11
        cursor.close()
        db_close()

        make_list = lambda x: [" " if i == None or i == '' else i for i in x]

        group_list = make_list(group_details)

        group_tuple = ('group_id', 'group_name', 'description', 'role_id')

        group_dict = dict(zip(group_tuple, group_list))

        return group_dict

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()

# print edit_group_view("76929ad6-f666-11e0-a835-f04da24c7c26")


def get_role_list():
    """


    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        query = "select `role_name`,`role_id` from roles where `is_deleted` <> 1"
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            roleName_list = cursor.fetchall()
        cursor.close()
        db_close()
        if len(roleName_list) < 1:
            return 1
        else:
            return roleName_list

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def change_password(var_dict):
    """

    @param var_dict:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        selectQuery = "SELECT user_name FROM user_login WHERE `user_id` = \"%(user_id)s\" and `password`=\"%(old_password)s\" " % var_dict
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            if cursor.fetchone()[0] == var_dict['user_name']:
                updateQuery = "UPDATE user_login set `password`=\"%(password)s\ WHERE `user_id` = \"%(user_id)s\" " % var_dict
            else:
                cursor.close()
                db_close()
                return 100
        else:
            cursor.close()
            db_close()
            return 100

        cursor.execute(updateQuery)
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def get_hostgroup_info(hg_id):
    """

    @param hg_id:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        query = "SELECT `hostgroup_alias`,`updated_by`,`timestamp`,`created_by`,`creation_time` from hostgroups WHERE hostgroup_id = \"%s\"" % hg_id
        gpDetail_tuple = ()
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            gpDetail_tuple = cursor.fetchone()
        cursor.close()
        db_close()
        if len(gpDetail_tuple) < 1:
            return 1
        else:
            return gpDetail_tuple
    except Exception as e:
        return 111  # str(e)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def get_hostgroup_details():
    """


    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        query = "select `hostgroup_id`,`hostgroup_name` from hostgroups where `is_deleted` <> 1"
        cursor = global_db.cursor()
        groupName_list = ()
        if cursor.execute(query) != 0:
            groupName_list = cursor.fetchall()
        cursor.close()
        db_close()
        if len(groupName_list) < 1:
            return 1
        else:
            return groupName_list

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def show_hostgroups(group_id, all=1):
    """

    @param group_id:
    @param all:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if all == 0:
            query = "SELECT hg.`hostgroup_id` , hg.`hostgroup_name`, hg.`hostgroup_alias` \
            FROM hostgroups AS hg \
            WHERE hg.hostgroup_id NOT IN ( \
                        SELECT hg_grp.hostgroup_id FROM hostgroups_groups AS hg_grp WHERE hg_grp.`group_id` = '%s' )" % group_id
        elif group_id == "remain":
            query = "SELECT hg.`hostgroup_id`, hg.`hostgroup_name` , hg.`hostgroup_alias` \
            FROM hostgroups as hg \
            WHERE NOT EXISTS \
                        ( SELECT hg_grp.`hostgroup_id` FROM hostgroups_groups AS hg_grp WHERE hg.`hostgroup_id` = hg_grp.`hostgroup_id` )"
        else:
            query = "SELECT hostgroups.`hostgroup_id`, hostgroups.`hostgroup_name` , hostgroups.`hostgroup_alias` \
            FROM hostgroups_groups \
            INNER JOIN hostgroups ON hostgroups.hostgroup_id = hostgroups_groups.hostgroup_id \
            INNER JOIN groups ON hostgroups_groups.group_id = groups.group_id \
            WHERE groups.group_id = \"%s\"" % group_id
        gpHG_tuple = ()
        cursor = global_db.cursor()
        cursor.execute(query)
        gpHG_tuple = cursor.fetchall()
        cursor.close()
        db_close()
        return gpHG_tuple
    #        if len(gpHG_tuple) < 1 :
    #            return 1
    #        else:
    ##            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
    ##            gpHG_list = []
    ##            for gpHG in gpHG_tuple:
    ##                gpHG_list.append(make_list(gpHG))
    #            return gpHG_tuple

    except Exception as e:
        return 111  # str(e)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def show_groups(hostgroup_id, all_var=1, grp_value=0):
    """

    @param hostgroup_id:
    @param all_var:
    @param grp_value:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if all_var == 0 and grp_value == 1:  # superadmin grp_value = 1
            query = "SELECT gp.`group_id` , gp.`group_name` \
            FROM groups AS gp \
            WHERE gp.group_id NOT IN ( \
                        SELECT hg_grp.group_id FROM hostgroups_groups AS hg_grp \
                        WHERE hg_grp.`hostgroup_id` = '%s' ) \
                        and gp.`group_name`<> 'Default' " % hostgroup_id
        elif all_var == 0 and grp_value == 0:
            query = "SELECT gp.`group_id` , gp.`group_name` \
            FROM groups AS gp \
            WHERE gp.group_id NOT IN ( \
                        SELECT hg_grp.group_id FROM hostgroups_groups AS hg_grp \
                        WHERE hg_grp.`hostgroup_id` = '%s' ) \
                        and gp.`group_name`<> 'Default' \
                        and gp.`group_name`<> 'SuperAdmin' " % hostgroup_id
        elif hostgroup_id == "remain":
            query = "SELECT gp.`group_id` , gp.`group_name` \
            FROM groups AS gp WHERE gp.group_id WHERE NOT EXISTS \
                        ( SELECT hg_grp.`group_id` FROM hostgroups_groups AS hg_grp \
                        WHERE gp.group_id = hg_grp.`group_id` )"
        elif grp_value == 1:
            query = "SELECT groups.`group_id`, groups.`group_name` \
            FROM hostgroups_groups \
            INNER JOIN groups ON groups.group_id = hostgroups_groups.group_id \
            INNER JOIN hostgroups ON hostgroups_groups.hostgroup_id = hostgroups.hostgroup_id \
            WHERE hostgroups.hostgroup_id = \"%s\" " % hostgroup_id
        else:
            query = "SELECT groups.`group_id`, groups.`group_name` \
            FROM hostgroups_groups \
            INNER JOIN groups ON groups.group_id = hostgroups_groups.group_id \
            INNER JOIN hostgroups ON hostgroups_groups.hostgroup_id = hostgroups.hostgroup_id \
            WHERE hostgroups.hostgroup_id = \"%s\" and gp.`group_name`<> 'SuperAdmin' " % hostgroup_id
        gpHG_tuple = ()
        cursor = global_db.cursor()
        cursor.execute(query)
        gpHG_tuple = cursor.fetchall()
        cursor.close()
        db_close()
        return gpHG_tuple
    #        if len(gpHG_tuple) < 1 :
    #            return 1
    #        else:
    ##            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
    ##            gpHG_list = []
    ##            for gpHG in gpHG_tuple:
    ##                gpHG_list.append(make_list(gpHG))
    #            return gpHG_tuple

    except Exception as e:
        return 111  # str(e)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def add_hg_togroup(hg_ids_list, group_id):
    """

    @param hg_ids_list:
    @param group_id:
    @return:
    """
    db_connect()
    global global_db
    try:
        is_ins = 1
        if global_db.open != 1:
            return 1

        selQuery = "select `hostgroup_id` from hostgroups_groups where group_id = \"%s\" " % group_id
        cursor = global_db.cursor()

        cursor.execute(selQuery)

        hg_ids_tuple = cursor.fetchall()

        f = lambda x: tuple(str(j[0]) for j in x)

        hg_ids_tuple = f(hg_ids_tuple)

        insQuery = "insert into hostgroups_groups (`hostgroup_id`, `group_id`) values"

        i = 0
        for hgid in hg_ids_list:
            i += 1
            try:
                hg_ids_tuple.index(hgid)
            except ValueError as e:
                is_ins = 0
                if i == len(hg_ids_list):
                    insQuery += " (\"%s\",\"%s\") " % (hgid, group_id)
                else:
                    insQuery += " (\"%s\",\"%s\") ," % (hgid, group_id)

        if is_ins == 0:
            # print "insert is happening"
            cursor.execute(insQuery)
        else:
            pass  # print "insert NOT happening"
        global_db.commit()
        cursor.close()
        db_close()
        return 0

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def move_hg_togroup(hg_ids_list, group_id, old_group_id):
    """

    @param hg_ids_list:
    @param group_id:
    @param old_group_id:
    @return:
    """
    db_connect()
    global global_db
    try:
        insQuery = ""
        is_ins = 1
        if global_db.open != 1:
            return 1

        selQuery = "select `hostgroup_id` from hostgroups_groups where group_id = \"%s\" " % group_id
        cursor = global_db.cursor()

        cursor.execute(selQuery)

        hg_ids_tuples = cursor.fetchall()

        f = lambda x: tuple(str(j[0]) for j in x)

        hg_ids_tuple = f(hg_ids_tuples)
        #        hg_ids_tuple = sum(hg_ids_tuples,())
        insQuery = "insert into hostgroups_groups (`hostgroup_id`, `group_id`) values"

        i = 0
        comma_flag = 0
        for hgid in hg_ids_list:
            i += 1
            try:
                hg_ids_tuple.index(hgid)
            except ValueError as e:
                is_ins = 0
                if comma_flag == 0:
                    insQuery += " (\"%s\",\"%s\") " % (hgid, group_id)
                    comma_flag = 1
                else:
                    insQuery += " , (\"%s\",\"%s\") " % (hgid, group_id)

        if is_ins == 0:
            # print "insert is happening"
            cursor.execute(insQuery)
        else:
            pass  # print "insert NOT happening"
        global_db.commit()
        cursor.close()

        del_result = del_hg_fromgroup(hg_ids_list, old_group_id, 0)

        if del_result != 0:
            return "Not deleted but moved sucessfully"
        return 0

    except Exception as e:
        return 111  # str(e)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def move_group_tohg(hg_ids_list, group_id, old_group_id):
    """

    @param hg_ids_list:
    @param group_id:
    @param old_group_id:
    @return:
    """
    db_connect()
    global global_db
    try:
        is_ins = 1
        if global_db.open != 1:
            return 1

        selQuery = "select `group_id` from hostgroups_groups where hostgroup_id = \"%s\" " % group_id
        cursor = global_db.cursor()

        cursor.execute(selQuery)

        hg_tuple = cursor.fetchall()

        f = lambda x: tuple(str(j[0]) for j in x)

        hg_ids_tuple = f(hg_tuple)

        insQuery = "insert into hostgroups_groups (`group_id`, `hostgroup_id`) values"
        comma_flag = 0
        i = 0
        for hgid in hg_ids_list:
            i += 1
            try:
                hg_ids_tuple.index(hgid)
            except ValueError as e:
                is_ins = 0
                if comma_flag == 0:
                    insQuery += " (\"%s\",\"%s\") " % (hgid, group_id)
                    comma_flag = 1
                else:
                    insQuery += " , (\"%s\",\"%s\") " % (hgid, group_id)

        if is_ins == 0:
            # print "insert is happening"
            cursor.execute(insQuery)
        else:
            pass  # print "insert NOT happening"

        global_db.commit()
        cursor.close()

        del_result = del_gp_fromhostgroup(hg_ids_list, old_group_id, 0)

        if del_result != 0:
            return "Not deleted but moved sucessfully"
        return 0

    except Exception as e:
        return 111  # str(e)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def add_gp_tohostgroup(hg_ids_list, group_id):
    """

    @param hg_ids_list:
    @param group_id:
    @return:
    """
    db_connect()
    global global_db
    try:
        is_ins = 1
        if global_db.open != 1:
            return 1
        f = lambda x: tuple(j[0] for j in x)
        selQuery = "select `group_id` from hostgroups_groups where hostgroup_id = \"%s\" " % group_id
        cursor = global_db.cursor()

        cursor.execute(selQuery)

        hg_tuple = cursor.fetchall()

        f = lambda x: tuple(str(j[0]) for j in x)

        hg_ids_tuple = f(hg_tuple)

        insQuery = "insert into hostgroups_groups (`group_id`, `hostgroup_id`) values"

        i = 0
        comma_flag = 0
        for hgid in hg_ids_list:
            i += 1
            try:
                hg_ids_tuple.index(hgid)
            except ValueError as e:
                is_ins = 0
                if comma_flag == 0:
                    insQuery += " (\"%s\",\"%s\") " % (hgid, group_id)
                    comma_flag = 1
                else:
                    insQuery += " ,(\"%s\",\"%s\")" % (hgid, group_id)

        if is_ins == 0:
            # print "insert is happening"
            cursor.execute(insQuery)
        else:
            pass  # print "insert NOT happening"

        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111  # str(e)
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def del_gp_fromhostgroup(gp_ids_list, hostgroup_id, flag=1):
    """

    @param gp_ids_list:
    @param hostgroup_id:
    @param flag:
    @return:
    """
    if flag == 1:
        db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        delQuery = "delete from hostgroups_groups where "
        i = 0
        for gp_id in gp_ids_list:
            i += 1
            if len(gp_ids_list) == i:
                delQuery += "`hostgroup_id` = \"%s\" AND `group_id` = \"%s\" " % (
                    hostgroup_id, gp_id)
            else:
                delQuery += "`hostgroup_id` = \"%s\" AND `group_id` = \"%s\" OR " % (
                    hostgroup_id, gp_id)

        cursor = global_db.cursor()

        if cursor.execute(delQuery) < 1:
            cursor.close()
            db_close()
            return 3

        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111  # str(e)
    finally:
        if flag and isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def del_hg_fromgroup(hg_ids_list, group_id, flag=1):
    """

    @param hg_ids_list:
    @param group_id:
    @param flag:
    @return:
    """
    if flag == 1:
        db_connect()

    global global_db
    try:
        if global_db.open != 1:
            return 1

        delQuery = "delete from hostgroups_groups where "
        i = 0
        for hg_id in hg_ids_list:
            i += 1
            if len(hg_ids_list) == i:
                delQuery += "`hostgroup_id` = \"%s\" AND `group_id` = \"%s\" " % (
                    hg_id, group_id)
            else:
                delQuery += "`hostgroup_id` = \"%s\" AND `group_id` = \"%s\" OR " % (
                    hg_id, group_id)

        cursor = global_db.cursor()

        if cursor.execute(delQuery) < 1:
            cursor.close()
            db_close()
            return 3

        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 111  # str(e)
    finally:
        if flag and isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()


def get_hostgroup_list():
    """


    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        query = "select `hostgroup_name`,`hostgroup_id` from hostgroups where `is_deleted` <> 1"
        cursor = global_db.cursor()
        groupName_list = ()
        if cursor.execute(query) != 0:
            groupName_list = cursor.fetchall()
        cursor.close()
        db_close()
        if len(groupName_list) < 1:
            return 1
        else:
            return groupName_list

    except Exception as e:
        return 111
    finally:
        if isinstance(global_db, MySQLdb.connection):
            if global_db.open:
                db_close()
