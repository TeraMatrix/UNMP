#!/usr/bin/python2.6
# import the packeges
import MySQLdb

from common_controller import *
from nms_config import *
from odu_controller import *
from datetime import datetime
from datetime import timedelta
from mysql_collection import mysql_connection
from unmp_dashboard_config import DashboardConfig
from operator import itemgetter
from utility import Validation


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
        return output_dict


class IDUDashboard(object):
    """
    IDU device related dashoard class
    """
    def idu4_dashboard(self, host_id):
        """

        @param host_id:
        @return: @raise:
        """
        try:
            db, cursor = mysql_connection('nms_sample')
            if db == 1:
                raise SelfException(cursor)
            ip_address = ""
            mac_address = ""
            selected_device = ""
            if Validation.is_valid_ip(host_id):
                ip_address = host_id
            else:
                if host_id == "" or host_id == None or str(host_id) == 'None':
                    ip_address = html.var("ip_address")
                    mac_address = html.var("mac_address")
                    selected_device = html.var("selected_device_type")
                    if cursor.execute(
                            "SELECT ip_address from hosts where mac_address = '%s' and device_type_id = '%s'") % (
                    mac_address, selected_device):
                        result = cursor.fetchall()
                    elif cursor.execute(
                            "SELECT ip_address from hosts where ip_address = '%s' and device_type_id = '%s'") % (
                    ip_address, selected_device):
                        result = cursor.fetchall()
                    else:
                        result = ()
                    if len(result) > 0:
                        ip_address = result[0][0]
                    else:
                        ip_address = ''
                else:
                    sql = "SELECT ip_address from hosts where host_id = '%s' " % (
                        host_id)
                    cursor.execute(sql)
                    ip_address = cursor.fetchall()
                    if ip_address is not None and len(ip_address) > 0:
                        ip_address = ip_address[0][0]
                    else:
                        ip_address = ''
                    #
                    #            if host_id == "" or host_id == None:
                    #                ip_address=html.var("ip_address")
                    #                mac_address=html.var("mac_address")
                    #                selected_device=html.var("selected_device_type")
                    #                if cursor.execute("SELECT ip_address from hosts where mac_address = '%s' and device_type_id = '%s'")%(mac_address,selected_device):
                    #                    result=cursor.fetchall()
                    #                elif cursor.execute("SELECT ip_address from hosts where ip_address = '%s' and device_type_id = '%s'")%(ip_address,selected_device):
                    #                    result=cursor.fetchall()
                    #                else:
                    #                    result=()
                    #                if len(result)>0:
                    #                    ip_address=result[0][0]
                    #                else:
                    #                    ip_address=''
                    #            else:
                    #                sql="SELECT ip_address from hosts where host_id = '%s' "%(host_id)
                    #                cursor.execute(sql)
                    #                ip_address=cursor.fetchall()
                    #                if ip_address is not None and len(ip_address)>0:
                    #                    ip_address=ip_address[0][0]
                    #                else:
                    #                    ip_address=''
            output_dict = {'success': 0, 'output': '%s' % ip_address}
            return output_dict
            # odu_network_interface_table_graph(h)
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def get_dashboard_data(self):
        """


        @return:
        """
        devcie_type_attr = ['id', 'refresh_time', 'time_diffrence']
        get_data = DashboardConfig.get_config_attributes(
            'idu4_dashboard', devcie_type_attr)
        odu_refresh_time = 10   # default time
        total_count = 10    # default count showing record
        if get_data is not None:
            if get_data[0][0] == 'idu4_D':
                odu_refresh_time = get_data[0][1]
                total_count = get_data[0][2]
        return str(odu_refresh_time), str(total_count)

    def idu4_interface(self, odu_start_date, odu_start_time, odu_end_date, odu_end_time, interface_value, ip_address,
                       limitFlag):
        """

        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param interface_value:
        @param ip_address:
        @param limitFlag:
        @return: @raise:
        """
        rx0 = []
        tx0 = []
        time_stamp0 = []
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query = "select (idu.rxBytes),(idu.txBytes),idu.timestamp from idu_iduNetworkStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where  h.ip_address='%s' AND  idu.timestamp >= '%s' AND idu.timestamp <='%s' and idu.interfaceName = %s order by idu.timestamp desc" % (
            ip_address, start_time, end_time, interface_value)
            sel_query += limit_data
            cursor.execute(sel_query)
            result = cursor.fetchall()
            for i in range(len(result) - 1):
                rx_byte = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                tx_byte = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                rx0.append(0 if rx_byte <= 0 else rx_byte)
                tx0.append(0 if tx_byte <= 0 else tx_byte)
                time_stamp0.append(result[i][2].strftime('%H:%M'))
            output_dict = {'success': 0, 'interface_rx': rx0,
                           'interface_tx': tx0, 'time_stamp0': time_stamp0}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_tdmoip(self, odu_start_date, odu_start_time, odu_end_date, odu_end_time, interface_value, ip_address,
                    limitFlag):
        """

        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param interface_value:
        @param ip_address:
        @param limitFlag:
        @return: @raise:
        """
        transmit = []
        receive = []
        time_stamp = []
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query = "select IFNULL((idu.bytesTransmitted),0),IFNULL((idu.bytesReceived),0),idu.timestamp from  idu_tdmoipNetworkInterfaceStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where h.ip_address='%s' AND idu.timestamp <='%s' AND idu.timestamp >= '%s' AND indexid=%s order by idu.timestamp desc " % (
                ip_address, end_time, start_time, interface_value)
            sel_query += limit_data
            cursor.execute(sel_query)
            result = cursor.fetchall()
            for i in range(len(result) - 1):
                rx_byte = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                tx_byte = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                receive.append(0 if rx_byte <= 0 else rx_byte)
                transmit.append(0 if tx_byte <= 0 else tx_byte)
                time_stamp.append(result[i][2].strftime('%H:%M'))
            output_dict = {'success': 0, 'transmit': transmit,
                           'receive': receive, 'time_stamp': time_stamp}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_link_status(self, odu_start_date, odu_start_time, odu_end_date, odu_end_time, interface_value, ip_address,
                         limitFlag):
        """

        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param interface_value:
        @param ip_address:
        @param limitFlag:
        @return: @raise:
        """
        transmit = []
        receive = []
        time_stamp = []
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query = "select  idu.timestamp,idu.operationalStatus,idu.minJBLevel,idu.maxJBLevel,idu.underrunOccured,idu.overrunOccured,idu.portNum from  idu_linkStatusTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where h.ip_address='%s' AND idu.timestamp <='%s' AND idu.timestamp >= '%s' and idu.bundleNum='%s' order by idu.timestamp desc " % (
                ip_address, end_time, start_time, interface_value)
            sel_query += limit_data
            cursor.execute(sel_query)
            result = cursor.fetchall()
            output_dict = {'success': 0, 'output': result}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_linkstatistcis(self, odu_start_date, odu_start_time, odu_end_date, odu_end_time, link_num, ip_address,
                            limitFlag):
        """

        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param link_num:
        @param ip_address:
        @param limitFlag:
        @return: @raise:
        """
        good_frm_eth0 = []
        good_frm_rx = []
        lost_pct_rx = []
        discard_pct = []
        record_pct = []
        event = []
        time_stamp = []
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query = "select  idu.timestamp,idu.goodFramesToEth,idu.goodFramesRx,idu.lostPacketsAtRx,idu.discardedPackets,idu.reorderedPackets,idu.underrunEvents from  idu_linkStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where h.ip_address='%s' AND idu.timestamp <='%s' AND idu.timestamp >= '%s' AND idu.bundlenumber='%s' order by idu.timestamp desc " % (
                ip_address, end_time, start_time, link_num)
            sel_query += limit_data
            cursor.execute(sel_query)
            result = cursor.fetchall()
            for i in range(len(result) - 1):
                res1 = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                res2 = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                res3 = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                res4 = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                res5 = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                res6 = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                good_frm_eth0.append(0 if res1 <= 0 else res1)
                good_frm_rx.append(0 if res2 <= 0 else res2)
                lost_pct_rx.append(0 if res3 <= 0 else res3)
                discard_pct.append(0 if res4 <= 0 else res4)
                record_pct.append(0 if res5 <= 0 else res5)
                event.append(0 if res6 <= 0 else res6)
                time_stamp.append(result[i][0].strftime('%H:%M'))
            linkstatistcis = {'success': 0, 'result': [good_frm_eth0, good_frm_rx,
                                                       lost_pct_rx, discard_pct, record_pct, event, time_stamp]}
            return linkstatistcis
        # Exception Handling
        except MySQLdb as e:
            linkstatistcis = {'success': 3, 'output': str(e[-1])}
            return linkstatistcis
        except SelfException:
            pass
        except Exception as e:
            linkstatistcis = {'success': 1, 'output': str(e[-1])}
            return linkstatistcis
        finally:
            db.close()

    def idu4_get_link_name(self):
        """


        @return: @raise:
        """
        link_value = []
        link_name = []
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            link_query = "SELECT distinct(idu.bundlenumber) FROM idu_linkStatisticsTable as idu"
            cursor.execute(link_query)
            link_result = cursor.fetchall()
            for link in link_result:
                link_value.append(
                    0 if link[0] == '' or link[0] == None else int(link[0]))
                link_name.append('Link ' + str(link[0]))
            output_dic = {'success': 0, 'link_name': link_name,
                          'link_value': link_value}
            return output_dic
        # Exception Handling
        except MySQLdb as e:
            output_dic = {'success': 3, 'output': str(e[-1])}
            return output_dic
        except SelfException:
            pass
        except Exception as e:
            output_dic = {'success': 1, 'output': str(e[-1])}
            return output_dic
        finally:
            db.close()

    def idu4_e1_port_status(self, odu_start_date, odu_start_time, odu_end_date, odu_end_time, port_num, ip_address,
                            limitFlag):
        """

        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param port_num:
        @param ip_address:
        @param limitFlag:
        @return: @raise:
        """
        bpv = []
        time_stamp = []
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query = "select  idu.timestamp,idu.opStatus,idu.los,idu.lof,idu.ais,idu.rai,idu.rxFrameSlip,idu.txFrameSlip,idu.adptClkState,idu.holdOverStatus,idu.bpv from  idu_e1PortStatusTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where h.ip_address='%s' AND idu.timestamp <='%s' AND idu.timestamp >= '%s' AND idu.portNum='%s' order by idu.timestamp desc " % (
                ip_address, end_time, start_time, port_num)
            sel_query += limit_data
            cursor.execute(sel_query)
            result = cursor.fetchall()
            for i in range(len(result) - 1):
                error_count = ((int(result[i][10]) - int(result[i + 1][10])))
                bpv.append(0 if error_count <= 0 else error_count)
                time_stamp.append(result[i][0].strftime('%H:%M'))
            output_dict = {'success': 0, 'output': result,
                           'bpv': bpv, 'timestamp': time_stamp}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_device_information(self, ip_address):
        """

        @param ip_address:
        @return: @raise:
        """
        last_reboot_time = ''
        try:
            db, cursor = mysql_connection()
            if db == 1 or db == '1':
                raise SelfException(cursor)
            sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,sw.passiveVersion,sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw INNER JOIN idu_iduInfoTable as info ON sw.host_id=sw.host_id INNER JOIN hosts ON hosts.host_id=sw.host_id WHERE hosts.ip_address='%s' limit 1" % ip_address
            cursor.execute(sql)
            result = cursor.fetchall()
            # sql="SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1"%ip_address
            # cursor.execute(sql)
            # reboot_resion=cursor.fetchall()
            # if len(reboot_resion)>0:
            #    last_reboot_time=reboot_resion[0][0]
            output_dict = {'success': 0, 'result': result,
                           'last_reboot_time': last_reboot_time}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_event(self, ip_address):
        """

        @param ip_address:
        @return: @raise:
        """
        normal = []
        inforamtional = []
        minor = []
        major = []
        critical = []
        time_stamp = []
        odu_trap_detail = {}
        try:
            db, cursor = mysql_connection()
            if db == 1 or db == '1':
                raise SelfException(cursor)
                # start_time=datetime.strptime(odu_start_date+' '+odu_start_time,"%d/%m/%Y %H:%M")
            # end_time=datetime.strptime(odu_end_date+'
            # '+odu_end_time,"%d/%m/%Y %H:%M")
            sql = "SELECT count(ta.trap_event_id),date(ta.timestamp) ,ta.serevity FROM trap_alarms as ta  where  date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s AND ta.agent_id='%s'  group by serevity,date(ta.timestamp) order by  timestamp desc" % (
                5, ip_address)
            cursor.execute(sql)
            trap_result = cursor.fetchall()
            if trap_result is not None:
                for i in range(0, 5):
                    normal1 = 0
                    inforamtional1 = 0
                    minor1 = 0
                    major1 = 0
                    critical1 = 0
                    for row in trap_result:
                        if datetime.date(datetime.now() + timedelta(days=-i)) == row[1]:
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
                    time_stamp.append(datetime.date(
                        datetime.now() + timedelta(days=-i)).strftime('%x'))
                    normal.append(normal1)
                    inforamtional.append(inforamtional1)
                    minor.append(minor1)
                    major.append(major1)
                    critical.append(critical1)
            time_stamp.reverse()
            normal.reverse()
            inforamtional.reverse()
            minor.reverse()
            major.reverse()
            critical.reverse()
            output_dict = {'success': 0, 'output': {'graph': [normal,
                                                              inforamtional, minor, major, critical],
                                                    'timestamp': time_stamp}}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_outage(self, ip_address):
        """

        @param ip_address:
        @return: @raise:
        """
        date_days = []  # this list store the days information with date.
        up_state = []
        # Its store the total up state of each day in percentage.
        down_state = []
        # Its store the total down state of each day in percentage.
        output_dict = {}  # its store the actual output for display in graph.
        last_status = ''
        down_flag = 0
        up_flag = 0
        current_date = datetime.date(datetime.now())
        # ed=str(current_date+timedelta(days=-14)) # Its used for testing.
        # cd=str(current_date+timedelta(days=-23)) # Its used for testing.
        current_datetime = datetime.strptime(str(current_date + timedelta(
            days=-5)) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        # last_datetime=datetime.strptime(str(current_date+timedelta(days=-1))+"
        # 23:59:59",'%Y-%m-%d %H:%M:%S') # convert the string in  datetime.
        last_datetime = datetime.strptime(
            str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        temp_date = last_datetime
        # this datetime last status calculation
        last_status_current_time = datetime.strptime(str(current_date + timedelta(
            days=-6)) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        last_status_end_time = datetime.strptime(str(current_date + timedelta(
            days=-5)) + " 23:59:59", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        try:
            # connection from mysql
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
                FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
               where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                order by nagios_statehistory.state_time " % (current_datetime, last_datetime, ip_address)
            # Execute the query.
            cursor.execute(sql)
            result = cursor.fetchall()

            # this query get last status of device
            sel_sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
                FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
               where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                order by nagios_statehistory.state_time  desc limit 1" % (
            last_status_current_time, last_status_end_time, ip_address)
            # Execute the query.
            cursor.execute(sel_sql)
            last_state = cursor.fetchall()
            if last_state is not None:
                if len(last_state) > 0:
                    last_status = last_state[0][2]

            if result is not None:
                if len(result) > 0:
                    for i in range(5):
                        flag = 0
                        total_down_time = 0
                        total_up_time = 0
                        temp_down_time = ''
                        temp_up_time = ''
                        temp_time = ''
                        j = 0
                        for row in result:
                            if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                                flag = 1
                                if row[2] == 0:
                                    if temp_up_time == '':
                                        temp_up_time = row[1]
                                        if last_status == '' and up_flag == 0:
                                            if temp_time is not '':
                                                if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                    total_up_time += abs((
                                                                             row[1] - temp_time).days * 1440 + (
                                                                         row[1] - temp_time).seconds / 60)
                                                    temp_up_time = row[1]
                                                else:
                                                    total_down_time += abs((
                                                                               row[1] - temp_time).days * 1440 + (
                                                                           row[1] - temp_time).seconds / 60)
                                                    temp_down_time = row[1]
                                            up_flag = 1
                                        elif last_status is not '' and up_flag == 0:
                                            up_flag = 1
                                            if last_status == 0:
                                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                            else:
                                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                    else:
                                        if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                            total_up_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_up_time = row[1]
                                        else:
                                            total_down_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_down_time = row[1]
                                else:
                                    if temp_down_time == '':
                                        temp_down_time = row[1]
                                        if last_status == '' and down_flag == 0:
                                            if temp_time is not '':
                                                if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                    total_up_time += abs((
                                                                             row[1] - temp_time).days * 1440 + (
                                                                         row[1] - temp_time).seconds / 60)
                                                    temp_up_time = row[1]
                                                else:
                                                    total_down_time += abs((
                                                                               row[1] - temp_time).days * 1440 + (
                                                                           row[1] - temp_time).seconds / 60)
                                                    temp_down_time = row[1]
                                            down_flag = 1
                                        elif last_status is not '' and down_flag == 0:
                                            down_flag = 1
                                            if last_status == 0:
                                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                            else:
                                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                    else:

                                        if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                            total_up_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_up_time = row[1]
                                        else:
                                            total_down_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_down_time = row[1]

                            if j < len(result):
                                temp_time = row[1]
                            j += 1
                        if flag == 1:
                            if result[j - 1][2] == 0:
                                total_up_time = abs((result[j - 1][1] - (
                                    temp_date + timedelta(days=-i))).days * 1440 + (
                                                    result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                            else:
                                total_down_time = abs((result[j - 1][1] - (
                                    temp_date + timedelta(days=-i))).days * 1440 + (
                                                      result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                        date_days.append((temp_date + timedelta(
                            days=-(i))).strftime("%d %b %Y"))
                        total = total_up_time + total_down_time
                        if flag == 1 and total > 0:
                            up_state.append(
                                round((total_up_time * 100) / float(total), 2))
                            down_state.append(
                                round((total_down_time * 100) / float(total), 2))
                        else:
                            up_state.append(0)
                            down_state.append(0)
                else:
                    sel_sql = "SELECT  nagios_hosts.address,nagios_hoststatus.status_update_time,nagios_hoststatus.current_state\
                        FROM nagios_hosts INNER JOIN nagios_hoststatus ON nagios_hoststatus.host_object_id = nagios_hosts.host_object_id\
                       where nagios_hoststatus.status_update_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                        order by nagios_hoststatus.status_update_time " % (current_datetime, last_datetime, ip_address)
                    cursor.execute(sel_sql)
                    result = cursor.fetchall()
                    for i in range(5):
                        flag = 0
                        total_down_time = 0
                        total_up_time = 0
                        for row in result:
                            if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                                flag = 1
                                if row[2] == 0:
                                    total_up_time = abs((row[1] - (temp_date + timedelta(
                                        days=-(i + 1)))).days * 1440 + (
                                                        row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:
                                    total_down_time = abs((row[1] - (temp_date + timedelta(
                                        days=-(i + 1)))).days * 1440 + (
                                                          row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                        date_days.append((temp_date + timedelta(
                            days=-(i))).strftime("%d %b %Y"))
                        total = total_up_time + total_down_time
                        if flag == 1 and total > 0:
                            up_state.append(
                                round((total_up_time * 100) / float(total), 2))
                            down_state.append(
                                round((total_down_time * 100) / float(total), 2))
                        else:
                            up_state.append(0)
                            down_state.append(0)
                # reverse the list according to date
            up_state.reverse()
            down_state.reverse()
            date_days.reverse()

            output_dict = {'success': 0, 'up_state': up_state,
                           'down_state': down_state, 'date_days': date_days}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_alarm_event(self, ip_address, table_option):
        """

        @param ip_address:
        @param table_option:
        @return: @raise:
        """
        history_trap_detail = {}
        try:
            db, cursor = mysql_connection('nms_sample')
            if db == 1:
                raise SelfException(cursor)
            if table_option.strip() == "trap":
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' order by ta.timestamp desc limit 7 " % ip_address
            else:
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' order by ta.timestamp desc limit 7 " % ip_address
            cursor.execute(sql)
            result = cursor.fetchall()
            output_dict = {'success': 0, 'output': result}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_port_statistics(self, odu_start_date, odu_start_time, odu_end_date, odu_end_time, port, ip_address,
                             limitFlag):
        """

        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param port:
        @param ip_address:
        @param limitFlag:
        @return: @raise:
        """
        rx0 = []
        tx0 = []
        time_stamp0 = []
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query = "select (idu.framerx),(idu.frametx),idu.timestamp from idu_portstatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where  h.ip_address='%s' AND  idu.timestamp >= '%s' AND idu.timestamp <='%s' and idu.softwarestatportnum = '%s' order by idu.timestamp desc" % (
            ip_address, start_time, end_time, port)
            sel_query += limit_data
            cursor.execute(sel_query)
            result = cursor.fetchall()
            for i in range(len(result) - 1):
                rx_byte = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                tx_byte = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                rx0.append(0 if rx_byte <= 0 else rx_byte)
                tx0.append(0 if tx_byte <= 0 else tx_byte)
                time_stamp0.append(result[i][2].strftime('%H:%M'))
            output_dict = {'success': 0, 'interface_rx': rx0,
                           'interface_tx': tx0, 'time_stamp0': time_stamp0}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_excel_report(self, ip_address, odu_start_date, odu_start_time, odu_end_date, odu_end_time, select_option,
                          limitFlag):
        """

        @param ip_address:
        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param select_option:
        @param limitFlag:
        @return: @raise:
        """
        if ip_address == '' or ip_address == None or ip_address == 'undefined' or str(
                ip_address) == 'None':    # if ip_address not received so excel not created
            raise SelfException(
                'This UBR devices not exists so excel report can not be generated.')  # Check msg
        try:
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system
            # create the start datetime and end datatime
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            # calculating the total days between start and end date.
            total_days = ((end_time - start_time).days)
            if total_days < 5:
                total_days = 5
                # Import the modules for excel generating.
            import xlwt
            from xlwt import Workbook, easyxf

            # create the excel file
            xls_book = Workbook(encoding='ascii')

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
            # create the connection with database
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)

            # we get the host inforamtion.
            sel_query = "SELECT device_type.device_name,hosts.host_alias FROM hosts INNER JOIN device_type ON hosts.device_type_id=device_type.device_type_id WHERE hosts.ip_address='%s'" % (
            ip_address)
            cursor.execute(sel_query)
            host_result = cursor.fetchall()
            device_type = ''
            device_name = ''
            if len(host_result) > 0:
                device_type = ('--' if host_result[0][0]
                                       == '' or host_result[0][0] == None else host_result[0][0])
                device_name = ('--' if host_result[0][1]
                                       == '' or host_result[0][1] == None else host_result[0][1])
                # end the host information fucntion
            # Device Inforamtion Excel Creation start here.
            sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,sw.passiveVersion,sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw INNER JOIN idu_iduInfoTable as info ON sw.host_id=sw.host_id INNER JOIN hosts ON hosts.host_id=sw.host_id WHERE hosts.ip_address='%s' limit 1" % ip_address
            cursor.execute(sql)
            device_detail = cursor.fetchall()

            table_output = []
            if len(device_detail) > 0:
                if device_detail[0][7] != "" or device_detail != None:
                    hour = device_detail[0][7] / 3600
                    minute = (device_detail[0][7] / 60) % 60
                    second = device_detail[0][7] % 60
            for value in device_detail:
                table_output.append(['H/W Serial Number', str('--' if device_detail[0][0]
                                                                      == None or device_detail[0][0] == "" else
                device_detail[0][0])])
                table_output.append(['System MAC', str('--' if device_detail[0][1]
                                                               == None or device_detail[0][1] == "" else
                device_detail[0][1])])
                table_output.append(['TDMOIP Interface MAC', str('--' if device_detail[0][2]
                                                                         == None or device_detail[0][2] == "" else
                device_detail[0][2])])
                table_output.append(['Active Version', str('--' if device_detail[0][3]
                                                                   == None or device_detail[0][3] == "" else
                device_detail[0][3])])
                table_output.append(['Passive Version', str('--' if device_detail[0][4]
                                                                    == None or device_detail[0][4] == "" else
                device_detail[0][4])])
                table_output.append(['BootLoader Version ', str('--' if device_detail[0][5]
                                                                        == None or device_detail[0][5] == "" else
                device_detail[0][5])])
                table_output.append(['Temperature(C)', str('--' if device_detail[0][6]
                                                                   == None or device_detail[0][6] == "" else
                device_detail[0][6])])
                table_output.append(['UpTime', str(
                    str(hour) + "Hr " + str(minute) + "Min " + str(second) + "Sec")])
            sql = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
            cursor.execute(sql)
            reboot_time = cursor.fetchall()
            if len(reboot_time) > 0:
                table_output.append(
                    ['Last Reboot Time', str(reboot_time[0][0])])
            else:
                table_output.append(['Last Reboot Time', '--'])

            xls_sheet = xls_book.add_sheet(
                'device_information', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, 2, "IDU Information", style)
            xls_sheet.write_merge(1, 1, 0, 2, str(device_type) + '       ' + str(
                device_name) + '         ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Element', 'Element Values']
            # heading=[table_output[0][1],table_output[0][2],table_output[0][3],table_output[0][4],table_output[0][5],table_output[0][6],table_output[0][7]]
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(table_output)):
                for j in range(len(table_output[k])):
                    width = 5000
                    xls_sheet.write(i, j, str(table_output[k][j]), style1)
                    xls_sheet.col(j).width = width
                i = i + 1

            # excel creatig for network bandwidth
            interface = ['eth0']
            for interface_value in range(len(interface)):
                if int(select_option) == 0:
                    if int(limitFlag) == 0:
                        limit_data = ''
                    else:
                        limit_data = ' limit 16'
                    sel_query = "select (idu.rxBytes),(idu.txBytes),idu.timestamp from idu_iduNetworkStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where  h.ip_address='%s' AND  idu.timestamp >= '%s' AND idu.timestamp <='%s' and idu.interfaceName = %s order by idu.timestamp desc" % (
                        ip_address, start_time, end_time, interface_value)
                    sel_query += limit_data
                else:
                    sel_query = "select (idu.rxBytes),(idu.txBytes),idu.timestamp from idu_iduNetworkStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where  h.ip_address='%s' AND  date(idu.timestamp) >= current_date()-%s AND date(idu.timestamp) <=current_date() and idu.interfaceName = %s order by idu.timestamp desc" % (
                    ip_address, total_days, interface_value)
                cursor.execute(sel_query)
                nw_result = cursor.fetchall()
                network_list = []
                for i in range(0, len(nw_result) - 1):
                    temp_list = []
                    temp_list = [nw_result[i][2].strftime('%d-%m-%Y %H:%M'), 0 if (int(nw_result[i][1]) - int(
                        nw_result[i + 1][0])) < 0 else (int(nw_result[i][0]) - int(nw_result[i + 1][0])),
                                 0 if (int(nw_result[i][1]) - int(nw_result[i + 1][1])) < 0 else (
                                 int(nw_result[i][1]) - int(nw_result[i + 1][1]))]
                    network_list.append(temp_list)
                network_list = sorted(network_list, key=itemgetter(0))
                xls_sheet = xls_book.add_sheet('network_bandwidth(%s)' % interface[
                    interface_value], cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(0, 0, 0, 2, "Network Bandwidth Information (%s)" %
                                                  interface[interface_value], style)
                xls_sheet.write(1, 0, device_type, style)
                xls_sheet.write(1, 1, device_name, style)
                xls_sheet.write(1, 2, ip_address, style)
                xls_sheet.write_merge(2, 2, 0, 2, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = ['DataTime', 'Receving Bytes', 'Transmitting Bytes']
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for k in range(len(network_list) - 1):
                    for j in range(len(network_list[k])):
                        width = 5000
                        xls_sheet.write(i, j, str(network_list[k][j]), style1)
                        xls_sheet.col(j).width = width
                    i = i + 1
                    # Network bandwith Excel ending here.

                    # TDMOIP Network bandwith Excel Starting here.
            interface = ['eth0']
            for interface_value in range(len(interface)):
                if int(select_option) == 0:
                    if int(limitFlag) == 0:
                        limit_data = ''
                    else:
                        limit_data = ' limit 16'
                    sel_query = "select IFNULL((idu.bytesTransmitted),0),IFNULL((idu.bytesReceived),0),idu.timestamp from  idu_tdmoipNetworkInterfaceStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where h.ip_address='%s' AND idu.timestamp <='%s' AND idu.timestamp >= '%s' AND indexid=%s order by idu.timestamp" % (
                        ip_address, end_time, start_time, interface_value)
                    sel_query += limit_data
                else:
                    sel_query = "select IFNULL((idu.bytesTransmitted),0),IFNULL((idu.bytesReceived),0),idu.timestamp from  idu_tdmoipNetworkInterfaceStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where  h.ip_address='%s' AND  date(idu.timestamp) >= current_date()-%s AND date(idu.timestamp) <=current_date() and idu.indexid = %s order by idu.timestamp desc" % (
                    ip_address, total_days, interface_value)
                cursor.execute(sel_query)
                nw_result = cursor.fetchall()
                network_list = []
                for i in range(0, len(nw_result) - 1):
                    temp_list = []
                    temp_list = [nw_result[i][2].strftime('%d-%m-%Y %H:%M'), 0 if (int(nw_result[i][1]) - int(
                        nw_result[i + 1][0])) < 0 else (int(nw_result[i][0]) - int(nw_result[i + 1][0])),
                                 0 if (int(nw_result[i][1]) - int(nw_result[i + 1][1])) < 0 else (
                                 int(nw_result[i][1]) - int(nw_result[i + 1][1]))]
                    network_list.append(temp_list)
                network_list = sorted(network_list, key=itemgetter(0))
                xls_sheet = xls_book.add_sheet('TDMOIP_network_bandwidth(%s)' % interface[
                    interface_value], cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, 2, "TDMOIP Network Bandwidth Information (%s)" % interface[interface_value], style)
                xls_sheet.write(1, 0, device_type, style)
                xls_sheet.write(1, 1, device_name, style)
                xls_sheet.write(1, 2, ip_address, style)
                xls_sheet.write_merge(2, 2, 0, 2, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                headings = ['DataTime', 'Transmitting Bytes', 'Receving Bytes']
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for k in range(len(network_list) - 1):
                    for j in range(len(network_list[k])):
                        width = 5000
                        xls_sheet.write(i, j, str(network_list[k][j]), style1)
                        xls_sheet.col(j).width = width
                    i = i + 1

                    # TDMOIP Network bandwith Excel ending here.

            # Trap Information Excel starting here.
            normal = []
            inforamtional = []
            minor = []
            major = []
            critical = []
            time_stamp = []
            sql = "SELECT count(ta.trap_event_id),date(ta.timestamp) ,ta.serevity FROM trap_alarms as ta  where  date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s AND ta.agent_id='%s'  group by serevity,date(ta.timestamp) order by  timestamp desc" % (
                total_days, ip_address)
            cursor.execute(sql)
            trap_result = cursor.fetchall()
            if trap_result is not None:
                # store the information in list.
                for i in range(0, int(total_days) + 1):
                    normal1 = 0
                    inforamtional1 = 0
                    minor1 = 0
                    major1 = 0
                    critical1 = 0
                    for row in trap_result:
                        if datetime.date(datetime.now() + timedelta(days=-i)) == row[1]:
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
                    time_stamp.append(datetime.date(datetime.now(
                    ) + timedelta(days=-i)).strftime('%d %b %Y'))
                    normal.append(normal1)
                    inforamtional.append(inforamtional1)
                    minor.append(minor1)
                    major.append(major1)
                    critical.append(critical1)

            event_list = []
            k = 0
            for time in time_stamp:
                event_list.append([int(inforamtional[k]), int(normal[k]), int(
                    minor[k]), int(major[k]), int(critical[k]), str(time_stamp[k])])
                k += 1

            event_list = sorted(event_list, key=itemgetter(5))
            xls_sheet = xls_book.add_sheet(
                'event_count_information', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 5, " %s Days Event Information" % total_days, style)
            xls_sheet.write_merge(1, 1, 0, 5, str(device_type) + '       ' + str(
                device_name) + '         ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 5, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Informational', 'Normal', 'Minor',
                        'Major', 'Critical', 'Time']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(event_list)):
                for j in range(len(event_list[k])):
                    width = 5000
                    xls_sheet.write(i, j, str(event_list[k][j]), style1)
                    xls_sheet.col(j).width = width
                i = i + 1

            # Trap Information Excel Ending here.

            # event Information excel start here.
            trap_days = ((end_time - start_time).days)
            if int(select_option) == 0:
            # sql="SELECT
            # ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date
            # FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND
            # date(ta.timestamp)=current_date()  order by ta.timestamp "%(ip_address)
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND ta.timestamp>='%s' AND ta.timestamp<='%s' order by ta.timestamp " % (
                ip_address, start_time, end_time)

            else:
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND date(ta.timestamp)=current_date() and  date(ta.timestamp)>current_date()-%s order by ta.timestamp " % (
                    ip_address, trap_days)
            cursor.execute(sql)
            trap_result = cursor.fetchall()
            severity_list = ['Informational', 'Normal',
                             'Informational', 'Minor', 'Major', 'Critical']

            xls_sheet = xls_book.add_sheet(
                'alarm_information', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 3, "%s Days Alarm Information" % (int(trap_days) + 1), style)
            xls_sheet.write_merge(1, 1, 0, 3, str(device_type) + '       ' + str(
                device_name) + '         ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 3, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Severity', 'Event ID', 'Event Type', 'Receive Date']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(trap_result)):
                for j in range(len(trap_result[k])):
                    if j == 0:
                        width = 5000
                        xls_sheet.write(
                            i, j, severity_list[trap_result[k][j]], style1)
                        xls_sheet.col(j).width = width
                    else:
                        width = 5000
                        xls_sheet.write(i, j, str(trap_result[k][j]), style1)
                        xls_sheet.col(j).width = width
                i = i + 1

            # event Information excel end here.

            # event Information excel start here.
            if int(select_option) == 0:
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' AND ta.timestamp>='%s' AND  ta.timestamp<='%s' order by ta.timestamp " % (
                ip_address, start_time, end_time)
            else:
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' AND date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s order by ta.timestamp " % (
                    ip_address, trap_days)
            cursor.execute(sql)
            trap_result = cursor.fetchall()
            severity_list = ['Informational', 'Normal',
                             'Informational', 'Minor', 'Major', 'Critical']

            xls_sheet = xls_book.add_sheet(
                'event_information', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 3, "%s Days Event Information" % (int(trap_days) + 1), style)
            xls_sheet.write_merge(1, 1, 0, 3, str(device_type) + '       ' + str(
                device_name) + '         ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 3, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Severity', 'Event ID', 'Event Type', 'Receive Date']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(trap_result)):
                for j in range(len(trap_result[k])):
                    if j == 0:
                        width = 5000
                        xls_sheet.write(
                            i, j, severity_list[trap_result[k][j]], style1)
                        xls_sheet.col(j).width = width
                    else:
                        width = 5000
                        xls_sheet.write(i, j, str(trap_result[k][j]), style1)
                        xls_sheet.col(j).width = width
                i = i + 1

            # event Information excel end here.

            # Outage excel start here.

            date_days = []  # this list store the days information with date.
            up_state = []
            # Its store the total up state of each day in percentage.
            down_state = []
            # Its store the total down state of each day in percentage.
            output_dict = {}
            # its store the actual output for display in graph.\
            last_status = ''
            down_flag = 0
            up_flag = 0
            current_date = datetime.date(datetime.now())
            current_datetime = datetime.strptime(str(current_date + timedelta(
                days=-(total_days))) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
            last_datetime = datetime.strptime(
                str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
            temp_date = last_datetime

            # this datetime last status calculation
            last_status_current_time = datetime.strptime(str(current_date + timedelta(
                days=-(total_days + 1))) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
            last_status_end_time = datetime.strptime(str(current_date + timedelta(
                days=-(total_days))) + " 23:59:59", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.

            sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
                FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
               where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                order by nagios_statehistory.state_time " % (current_datetime, last_datetime, ip_address)
            # Execute the query.
            cursor.execute(sql)
            result = cursor.fetchall()

            # this query get last status of device
            sel_sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
                FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
               where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                order by nagios_statehistory.state_time  desc limit 1" % (
            last_status_current_time, last_status_end_time, ip_address)
            # Execute the query.
            cursor.execute(sel_sql)
            last_state = cursor.fetchall()
            if last_state is not None:
                if len(last_state) > 0:
                    last_status = last_state[0][2]
            if result is not None:
                if len(result) > 0:
                    for i in range((total_days + 1)):
                        flag = 0
                        total_down_time = 0
                        total_up_time = 0
                        temp_down_time = ''
                        temp_up_time = ''
                        temp_time = ''
                        j = 0
                        for row in result:
                            if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                                flag = 1
                                if row[2] == 0:
                                    if temp_up_time == '':
                                        temp_up_time = row[1]
                                        if last_status == '' and up_flag == 0:
                                            if temp_time is not '':
                                                if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                    total_up_time += abs((
                                                                             row[1] - temp_time).days * 1440 + (
                                                                         row[1] - temp_time).seconds / 60)
                                                    temp_up_time = row[1]
                                                else:
                                                    total_down_time += abs((
                                                                               row[1] - temp_time).days * 1440 + (
                                                                           row[1] - temp_time).seconds / 60)
                                                    temp_down_time = row[1]
                                            up_flag = 1
                                        elif last_status is not '' and up_flag == 0:
                                            up_flag = 1
                                            if last_status == 0:
                                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                            else:
                                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                    else:
                                        if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                            total_up_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_up_time = row[1]
                                        else:
                                            total_down_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_down_time = row[1]
                                else:
                                    if temp_down_time == '':
                                        temp_down_time = row[1]
                                        if last_status == '' and down_flag == 0:
                                            if temp_time is not '':
                                                if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                    total_up_time += abs((
                                                                             row[1] - temp_time).days * 1440 + (
                                                                         row[1] - temp_time).seconds / 60)
                                                    temp_up_time = row[1]
                                                else:
                                                    total_down_time += abs((
                                                                               row[1] - temp_time).days * 1440 + (
                                                                           row[1] - temp_time).seconds / 60)
                                                    temp_down_time = row[1]
                                            down_flag = 1
                                        elif last_status is not '' and down_flag == 0:
                                            down_flag = 1
                                            if last_status == 0:
                                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                            else:
                                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                    else:

                                        if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                            total_up_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_up_time = row[1]
                                        else:
                                            total_down_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_down_time = row[1]

                            if j < len(result):
                                temp_time = row[1]
                            j += 1
                        if flag == 1:
                            if result[j - 1][2] == 0:
                                total_up_time = abs((result[j - 1][1] - (
                                    temp_date + timedelta(days=-i))).days * 1440 + (
                                                    result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                            else:
                                total_down_time = abs((result[j - 1][1] - (
                                    temp_date + timedelta(days=-i))).days * 1440 + (
                                                      result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                        date_days.append((temp_date + timedelta(
                            days=-(i))).strftime("%d %b %Y"))
                        total = total_up_time + total_down_time
                        if flag == 1 and total > 0:
                            up_state.append(
                                round((total_up_time * 100) / float(total), 2))
                            down_state.append(
                                round((total_down_time * 100) / float(total), 2))
                        else:
                            up_state.append(0)
                            down_state.append(0)
                else:
                    sel_sql = "SELECT  nagios_hosts.address,nagios_hoststatus.status_update_time,nagios_hoststatus.current_state\
                        FROM nagios_hosts INNER JOIN nagios_hoststatus ON nagios_hoststatus.host_object_id = nagios_hosts.host_object_id\
                       where nagios_hoststatus.status_update_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                        order by nagios_hoststatus.status_update_time " % (current_datetime, last_datetime, ip_address)
                    cursor.execute(sel_sql)
                    result = cursor.fetchall()
                    for i in range((total_days + 1)):
                        flag = 0
                        total_down_time = 0
                        total_up_time = 0
                        for row in result:
                            if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                                flag = 1
                                if row[2] == 0:
                                    total_up_time = abs((row[1] - (temp_date + timedelta(
                                        days=-(i + 1)))).days * 1440 + (
                                                        row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:
                                    total_down_time = abs((row[1] - (temp_date + timedelta(
                                        days=-(i + 1)))).days * 1440 + (
                                                          row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                        date_days.append((temp_date + timedelta(
                            days=-(i))).strftime("%d %b %Y"))
                        total = total_up_time + total_down_time
                        if flag == 1 and total > 0:
                            up_state.append(
                                round((total_up_time * 100) / float(total), 2))
                            down_state.append(
                                round((total_down_time * 100) / float(total), 2))
                        else:
                            up_state.append(0)
                            down_state.append(0)
                # close the database and cursor connection.
            # reverse the data
            outage_list = []
            k = 0
            for day in date_days:
                outage_list.append([day, up_state[k], down_state[k]])
                k += 1
            outage_list = sorted(outage_list, key=itemgetter(0))

            xls_sheet = xls_book.add_sheet(
                'outage_information', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 2, "%s Days Outage Information" % total_days, style)
            xls_sheet.write_merge(1, 1, 0, 2, str(device_type) + '       ' + str(
                device_name) + '         ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Date', 'Up State', 'Down State']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(outage_list)):
                for j in range(len(outage_list[k])):
                    width = 5000
                    xls_sheet.write(i, j, str(outage_list[k][j]), style1)
                    xls_sheet.col(j).width = width
                i = i + 1
                # Outage excel end here.

            # excel creatig end for network bandwidth
            xls_book.save(
                '/omd/sites/%s/share/check_mk/web/htdocs/download/IDU4_excel.xls' % nms_instance)
            output_dict = {'success': 0, 'output': str(sel_query)}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def idu4_pdf_report(self, ip_address, odu_start_date, odu_start_time, odu_end_date, odu_end_time, select_option,
                        limitFlag):
        """

        @param ip_address:
        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param select_option:
        @param limitFlag:
        @return: @raise:
        """
        if ip_address == '' or ip_address == None or ip_address == 'undefined' or str(
                ip_address) == 'None':    # if ip_address not received so excel not created
            raise SelfException(
                'This UBR devices not exists so excel report can not be generated.')  # Check msg
        try:
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system
            # create the start datetime and end datatime
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            # calculating the total days between start and end date.
            total_days = ((end_time - start_time).days)
            if total_days < 5:
                total_days = 5
            from reportlab.lib import colors
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import inch
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
            import reportlab
            from reportlab.platypus import Image
            from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle, Frame, BaseDocTemplate, Frame, PageTemplate
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch, cm, mm
            from reportlab.lib import colors
            from reportlab.platypus.paragraph import Paragraph
            from reportlab.lib.enums import TA_JUSTIFY
            import copy

            # create the database connection
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)

            # style of the pdf report
            styleSheet = getSampleStyleSheet()
            idu4_report = []
            MARGIN_SIZE = 14 * mm
            PAGE_SIZE = A4
            nms_instance = __file__.split("/")[3]
            # pdfdoc="/omd/sites/%s/share/check_mk/web/htdocs/download/IDU4_PDF_Report.pdf"%(nms_instance,start_time,end_time)
            pdfdoc = "/omd/sites/%s/share/check_mk/web/htdocs/download/IDU4_PDF_Report.pdf" % (
                nms_instance)

            pdf_doc = BaseDocTemplate(pdfdoc, pagesize=PAGE_SIZE,
                                      leftMargin=MARGIN_SIZE, rightMargin=MARGIN_SIZE,
                                      topMargin=MARGIN_SIZE, bottomMargin=MARGIN_SIZE)
            main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE,
                               PAGE_SIZE[0] - 2 *
                               MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,
                               leftPadding=0, rightPadding=0, bottomPadding=0,
                               topPadding=0, id='main_frame')
            main_template = PageTemplate(
                id='main_template', frames=[main_frame])
            pdf_doc.addPageTemplates([main_template])
            im = Image("/omd/sites/%s/share/check_mk/web/htdocs/images/new/logo.png" %
                       nms_instance, width=1.5 * inch, height=.5 * inch)
            im.hAlign = 'LEFT'
            idu4_report.append(im)
            idu4_report.append(Spacer(1, 1))

            data = []
            data.append(
                ['IDU4 ' + str(ip_address), str(start_time) + '--' + str(end_time)])
            t = Table(data, [3.5 * inch, 4 * inch])
            t.setStyle(TableStyle([
                ('LINEBELOW', (0, 0), (5, 1), 1, (0.7, 0.7, 0.7)),
                ('TEXTCOLOR', (0, 0), (0, 0), (0.11, 0.11, 0.11)),
                ('TEXTCOLOR', (1, 0), (1, 0), (0.65, 0.65, 0.65)),
                ('FONT', (0, 0), (1, 0), 'Helvetica', 14),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
            idu4_report.append(t)
            idu4_report.append(Spacer(11, 11))

            # PDF creation start here
            ########################################### ODU Device Information
            idu4_report.append(Spacer(21, 21))
            result1 = ''
            # create the cursor
            cursor = db.cursor()

            # we get the host inforamtion.
            sel_query = "SELECT device_type.device_name,hosts.host_alias FROM hosts INNER JOIN device_type ON hosts.device_type_id=device_type.device_type_id WHERE hosts.ip_address='%s'" % (
            ip_address)
            cursor.execute(sel_query)
            host_result = cursor.fetchall()
            device_type = ''
            device_name = ''
            if len(host_result) > 0:
                device_type = ('--' if host_result[0][0]
                                       == '' or host_result[0][0] == None else host_result[0][0])
                device_name = ('--' if host_result[0][1]
                                       == '' or host_result[0][1] == None else host_result[0][1])
                # end the host information fucntion
            # Device Inforamtion Excel Creation start here.
            sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,sw.passiveVersion,sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw INNER JOIN idu_iduInfoTable as info ON sw.host_id=sw.host_id INNER JOIN hosts ON hosts.host_id=sw.host_id WHERE hosts.ip_address='%s' limit 1" % ip_address
            cursor.execute(sql)
            device_detail = cursor.fetchall()
            table_output = []
            if len(device_detail) > 0:
                if device_detail[0][7] != "" or device_detail != None:
                    hour = device_detail[0][7] / 3600
                    minute = (device_detail[0][7] / 60) % 60
                    second = device_detail[0][7] % 60
                    table_output.append(['H/W Serial Number', str('--' if device_detail[0][0]
                                                                          == None or device_detail[0][0] == "" else
                    device_detail[0][0])])
                    table_output.append(['System MAC', str(
                        '--' if device_detail[0][1] == None or device_detail[0][1] == "" else device_detail[0][1])])
                    table_output.append(['TDMOIP Interface MAC', str('--' if device_detail[0][2]
                                                                             == None or device_detail[0][2] == "" else
                    device_detail[0][2])])
                    table_output.append(['Active Version', str(
                        '--' if device_detail[0][3] == None or device_detail[0][3] == "" else device_detail[0][3])])
                    table_output.append(['Passive Version', str(
                        '--' if device_detail[0][4] == None or device_detail[0][4] == "" else device_detail[0][4])])
                    table_output.append(['BootLoader Version ', str('--' if device_detail[0][5]
                                                                            == None or device_detail[0][5] == "" else
                    device_detail[0][5])])
                    table_output.append(['Temperature(C)', str(
                        '--' if device_detail[0][6] == None or device_detail[0][6] == "" else device_detail[0][6])])
                    table_output.append(['UpTime', str(str(
                        hour) + "Hr " + str(minute) + "Min " + str(second) + "Sec")])
            sql = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
            cursor.execute(sql)
            reboot_time = cursor.fetchall()
            if len(reboot_time) > 0:
                table_output.append(
                    ['Last Reboot Time', str(reboot_time[0][0])])
            else:
                table_output.append(['Last Reboot Time', '--'])

            data1 = []
            data1.append(['', 'IDU4 Device Information', '', ''])
            t = Table(
                data1, [.021 * inch, 1.8 * inch, 2.75 * inch, 2.4 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            idu4_report.append(t)

            data = table_output
            t = Table(data, [3.55 * inch, 3.55 * inch])
            t.setStyle(TableStyle([('FONT', (0, 0), (1, 0), 'Helvetica', 9),
                                   ('FONT', (0, 1), (1, int(
                                       len(
                                           table_output)) - 1), 'Helvetica', 9),
                                   ('ALIGN', (1,
                                              0), (
                                        1, int(
                                            len(table_output)) - 1), 'CENTER'),
                                   ('BACKGROUND',
                                    (0, 0), (5, 0), (0.9, 0.9, 0.9)),
                                   ('LINEABOVE',
                                    (0, 0), (5, 0), 1.21, (0.35, 0.35, 0.35)),
                                   ('GRID', (0, 0), (5, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                 'BACKGROUND', (1, i), (1, i), (0.95, 0.95, 0.95)),
                             ('BACKGROUND', (0, i - 1),
                              (0, i - 1), (0.98, 0.98, 0.98)),
                            ]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), (0.9, 0.9, 0.9))
                    ]))
            t.setStyle(
                TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
            idu4_report.append(t)
            data1 = []
            if len(table_output) > 1:
                data1.append(['1-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            else:
                data1.append(['0-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            t = Table(data1, [7.10 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
            idu4_report.append(t)
            ###################################################################

            ########################################### ODU Latest 5 Alams ####
            idu4_report.append(Spacer(31, 31))
            result1 = ''
            # create the cursor
            cursor = db.cursor()
            trap_days = ((end_time - start_time).days)
            if int(select_option) == 0:
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND ta.timestamp>='%s' AND ta.timestamp<='%s' order by ta.timestamp" % (
                    ip_address, start_time, end_time)
            else:
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s order by ta.timestamp" % (
                    ip_address, trap_days)
            cursor.execute(sql)
            result1 = cursor.fetchall()
            bll_obj = IDUDashboard()
            table_output = bll_obj.table_list_trap(result1, 'Lateat 5 Alarms')
            # close the database and cursor connection.
            cursor.close()
            data1 = []
            data1.append(['', 'Latest 5 Alarms', '', ''])
            t = Table(
                data1, [.021 * inch, 1.24 * inch, 3.14 * inch, 2.57 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            idu4_report.append(t)

            data = table_output
            t = Table(data, [inch, inch, 2.55 * inch, 2.55 * inch])
            t.setStyle(
                TableStyle([('FONT', (0, 0), (3, 0), 'Helvetica-Bold', 10),
                            ('FONT', (0, 1), (3,
                                              int(
                                                  len(
                                                      table_output)) - 1), 'Helvetica', 9),
                            ('ALIGN', (1,
                                       0), (
                                 3, int(
                                     len(table_output)) - 1), 'CENTER'),
                            ('BACKGROUND',
                             (0, 0), (3, 0), (0.9, 0.9, 0.9)),
                            ('LINEABOVE',
                             (0, 0), (3, 0), 1.21, (0.35, 0.35, 0.35)),
                            ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                 'BACKGROUND', (1, i), (3, i), (0.95, 0.95, 0.95)),
                             ('BACKGROUND', (0, i - 1),
                              (0, i - 1), (0.98, 0.98, 0.98)),
                            ]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (1, i), (3, i), (0.9, 0.9, 0.9))
                    ]))

            t.setStyle(
                TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
            idu4_report.append(t)
            data1 = []
            if len(table_output) > 1:
                data1.append(['1-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            else:
                data1.append(['0-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            t = Table(data1, [7.10 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
            idu4_report.append(t)
            ###################################################################

            ########################################### ODU Latest 5 Traps ####
            idu4_report.append(Spacer(31, 31))
            result1 = ''
            # create the cursor
            cursor = db.cursor()
            if int(select_option) == 0:
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' AND ta.timestamp>='%s' AND  ta.timestamp<='%s' order by ta.timestamp" % (
                    ip_address, start_time, end_time)
            else:
                sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' AND date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s order by ta.timestamp " % (
                    ip_address, trap_days)
            cursor.execute(sql)
            result1 = cursor.fetchall()
            table_output = bll_obj.table_list_trap(result1, 'Lateat 5 Traps')
            # close the database and cursor connection.
            cursor.close()
            data1 = []
            data1.append(['', 'Latest 5 Events', '', ''])
            t = Table(
                data1, [.021 * inch, 1.24 * inch, 3.14 * inch, 2.57 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            idu4_report.append(t)

            data = table_output
            t = Table(data, [inch, inch, 2.55 * inch, 2.55 * inch])
            t.setStyle(
                TableStyle([('FONT', (0, 0), (3, 0), 'Helvetica-Bold', 10),
                            ('FONT', (0, 1), (3,
                                              int(
                                                  len(
                                                      table_output)) - 1), 'Helvetica', 9),
                            ('ALIGN', (1,
                                       0), (
                                 3, int(
                                     len(table_output)) - 1), 'CENTER'),
                            ('BACKGROUND',
                             (0, 0), (3, 0), (0.9, 0.9, 0.9)),
                            ('LINEABOVE',
                             (0, 0), (3, 0), 1.21, (0.35, 0.35, 0.35)),
                            ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                 'BACKGROUND', (1, i), (3, i), (0.95, 0.95, 0.95)),
                             ('BACKGROUND', (0, i - 1),
                              (0, i - 1), (0.98, 0.98, 0.98)),
                            ]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (1, i), (3, i), (0.9, 0.9, 0.9))
                    ]))

            t.setStyle(
                TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
            idu4_report.append(t)
            data1 = []
            if len(table_output) > 1:
                data1.append(['1-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            else:
                data1.append(['0-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            t = Table(data1, [7.10 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
            idu4_report.append(t)
            ###################################################################

            ########################################### ODU Trap Information ##
            idu4_report.append(Spacer(31, 31))
            # create the cursor
            cursor = db.cursor()

            normal = []
            inforamtional = []
            minor = []
            major = []
            critical = []
            time_stamp = []

            sql = "SELECT count(ta.trap_event_id),date(ta.timestamp) ,ta.serevity FROM trap_alarms as ta  where  date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s AND ta.agent_id='%s'  group by serevity,date(ta.timestamp) order by  timestamp desc" % (
                total_days, ip_address)
            cursor.execute(sql)
            trap_result = cursor.fetchall()
            if trap_result is not None:
                # store the information in list.
                for i in range(0, int(total_days) + 1):
                    normal1 = 0
                    inforamtional1 = 0
                    minor1 = 0
                    major1 = 0
                    critical1 = 0
                    for row in trap_result:
                        if datetime.date(datetime.now() + timedelta(days=-i)) == row[1]:
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
                    time_stamp.append(datetime.date(datetime.now(
                    ) + timedelta(days=-i)).strftime('%d %b %Y'))
                    normal.append(normal1)
                    inforamtional.append(inforamtional1)
                    minor.append(minor1)
                    major.append(major1)
                    critical.append(critical1)

            table_output = []
            k = 0
            table_output.append(['DateTime', 'Informational',
                                 'Normal', 'Minor', 'Major', 'Critical'])
            for time in time_stamp:
                table_output.append([str(time_stamp[k]), int(inforamtional[k]),
                                     int(normal[k]), int(minor[k]), int(major[k]), int(critical[k])])
                k += 1

            # close the database and cursor connection.
            cursor.close()
            data1 = []
            if total_days == 0:
                data1.append(['', 'Current Day Events Information', '', ''])
                t = Table(
                    data1, [.021 * inch, 2.41 * inch, 2.44 * inch, 2.1 * inch])
            else:
                data1.append(['', 'Last ' + str(
                    total_days + 1) + ' Days Events Information', '', ''])
                t = Table(
                    data1, [.021 * inch, 2.21 * inch, 2.64 * inch, 2.1 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            idu4_report.append(t)
            data = table_output
            t = Table(data, [1.45 * 1.1 * inch, 1.1 * inch, 1.1 *
                                                            inch, 1.1 * inch, 1.1 * inch, 1.1 * inch])
            t.setStyle(
                TableStyle([('FONT', (0, 0), (5, 0), 'Helvetica-Bold', 10),
                            ('FONT', (0, 1), (5,
                                              int(
                                                  len(
                                                      table_output)) - 1), 'Helvetica', 9),
                            ('ALIGN', (1,
                                       0), (
                                 5, int(
                                     len(table_output)) - 1), 'CENTER'),
                            ('BACKGROUND',
                             (0, 0), (5, 0), (0.9, 0.9, 0.9)),
                            ('LINEABOVE',
                             (0, 0), (5, 0), 1.21, (0.35, 0.35, 0.35)),
                            ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                 'BACKGROUND', (1, i), (5, i), (0.95, 0.95, 0.95)),
                             ('BACKGROUND', (0, i - 1),
                              (0, i - 1), (0.98, 0.98, 0.98)),
                            ]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (1, i), (5, i), (0.9, 0.9, 0.9))
                    ]))

            t.setStyle(
                TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
            idu4_report.append(t)
            data1 = []
            if len(table_output) > 1:
                data1.append(['1-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            else:
                data1.append(['0-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            t = Table(data1, [7.10 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
            idu4_report.append(t)
            ###################################################################

            ########################################### ODU OUTAGE report gener
            idu4_report.append(Spacer(31, 31))
            # create the cursor
            cursor = db.cursor()

            date_days = []  # this list store the days information with date.
            up_state = []
            # Its store the total up state of each day in percentage.
            down_state = []
            # Its store the total down state of each day in percentage.
            output_dict = {}
            # its store the actual output for display in graph.\
            last_status = ''
            down_flag = 0
            up_flag = 0
            current_date = datetime.date(datetime.now())
            current_datetime = datetime.strptime(str(current_date + timedelta(
                days=-(total_days))) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
            last_datetime = datetime.strptime(
                str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
            temp_date = last_datetime

            # this datetime last status calculation
            last_status_current_time = datetime.strptime(str(current_date + timedelta(
                days=-(total_days + 1))) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
            last_status_end_time = datetime.strptime(str(current_date + timedelta(
                days=-(total_days))) + " 23:59:59", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.

            sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
                FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
               where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                order by nagios_statehistory.state_time " % (current_datetime, last_datetime, ip_address)
            # Execute the query.
            cursor.execute(sql)
            result = cursor.fetchall()

            # this query get last status of device
            sel_sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
                FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
               where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                order by nagios_statehistory.state_time  desc limit 1" % (
            last_status_current_time, last_status_end_time, ip_address)
            # Execute the query.
            cursor.execute(sel_sql)
            last_state = cursor.fetchall()
            if last_state is not None:
                if len(last_state) > 0:
                    last_status = last_state[0][2]
            if result is not None:
                if len(result) > 0:
                    for i in range((total_days + 1)):
                        flag = 0
                        total_down_time = 0
                        total_up_time = 0
                        temp_down_time = ''
                        temp_up_time = ''
                        temp_time = ''
                        j = 0
                        for row in result:
                            if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                                flag = 1
                                if row[2] == 0:
                                    if temp_up_time == '':
                                        temp_up_time = row[1]
                                        if last_status == '' and up_flag == 0:
                                            if temp_time is not '':
                                                if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                    total_up_time += abs((
                                                                             row[1] - temp_time).days * 1440 + (
                                                                         row[1] - temp_time).seconds / 60)
                                                    temp_up_time = row[1]
                                                else:
                                                    total_down_time += abs((
                                                                               row[1] - temp_time).days * 1440 + (
                                                                           row[1] - temp_time).seconds / 60)
                                                    temp_down_time = row[1]
                                            up_flag = 1
                                        elif last_status is not '' and up_flag == 0:
                                            up_flag = 1
                                            if last_status == 0:
                                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                            else:
                                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                    else:
                                        if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                            total_up_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_up_time = row[1]
                                        else:
                                            total_down_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_down_time = row[1]
                                else:
                                    if temp_down_time == '':
                                        temp_down_time = row[1]
                                        if last_status == '' and down_flag == 0:
                                            if temp_time is not '':
                                                if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                    total_up_time += abs((
                                                                             row[1] - temp_time).days * 1440 + (
                                                                         row[1] - temp_time).seconds / 60)
                                                    temp_up_time = row[1]
                                                else:
                                                    total_down_time += abs((
                                                                               row[1] - temp_time).days * 1440 + (
                                                                           row[1] - temp_time).seconds / 60)
                                                    temp_down_time = row[1]
                                            down_flag = 1
                                        elif last_status is not '' and down_flag == 0:
                                            down_flag = 1
                                            if last_status == 0:
                                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                            else:
                                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                                    days=-(i + 1)))).days * 1440 + (row[1] - (
                                                temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                    else:

                                        if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                            total_up_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_up_time = row[1]
                                        else:
                                            total_down_time += abs(
                                                (row[1] - temp_time).days * 1440 + (row[1] - temp_time).seconds / 60)
                                            temp_down_time = row[1]

                            if j < len(result):
                                temp_time = row[1]
                            j += 1
                        if flag == 1:
                            if result[j - 1][2] == 0:
                                total_up_time = abs((result[j - 1][1] - (
                                    temp_date + timedelta(days=-i))).days * 1440 + (
                                                    result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                            else:
                                total_down_time = abs((result[j - 1][1] - (
                                    temp_date + timedelta(days=-i))).days * 1440 + (
                                                      result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                        date_days.append((temp_date + timedelta(
                            days=-(i))).strftime("%d %b %Y"))
                        total = total_up_time + total_down_time
                        if flag == 1 and total > 0:
                            up_state.append(
                                round((total_up_time * 100) / float(total), 2))
                            down_state.append(
                                round((total_down_time * 100) / float(total), 2))
                        else:
                            up_state.append(0)
                            down_state.append(0)
                else:
                    sel_sql = "SELECT  nagios_hosts.address,nagios_hoststatus.status_update_time,nagios_hoststatus.current_state\
                        FROM nagios_hosts INNER JOIN nagios_hoststatus ON nagios_hoststatus.host_object_id = nagios_hosts.host_object_id\
                       where nagios_hoststatus.status_update_time between '%s'  and '%s' and nagios_hosts.address='%s'\
                        order by nagios_hoststatus.status_update_time " % (current_datetime, last_datetime, ip_address)
                    cursor.execute(sel_sql)
                    result = cursor.fetchall()
                    for i in range((total_days + 1)):
                        flag = 0
                        total_down_time = 0
                        total_up_time = 0
                        for row in result:
                            if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                                flag = 1
                                if row[2] == 0:
                                    total_up_time = abs((row[1] - (temp_date + timedelta(
                                        days=-(i + 1)))).days * 1440 + (
                                                        row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:
                                    total_down_time = abs((row[1] - (temp_date + timedelta(
                                        days=-(i + 1)))).days * 1440 + (
                                                          row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                        date_days.append((temp_date + timedelta(
                            days=-(i))).strftime("%d %b %Y"))
                        total = total_up_time + total_down_time
                        if flag == 1 and total > 0:
                            up_state.append(
                                round((total_up_time * 100) / float(total), 2))
                            down_state.append(
                                round((total_down_time * 100) / float(total), 2))
                        else:
                            up_state.append(0)
                            down_state.append(0)

            date_days.reverse()
            up_state.reverse()
            down_state.reverse()
            data1 = []
            data1.append(['', 'Outage Status', '', ''])
            t = Table(
                data1, [.021 * inch, 1.15 * inch, 2.94 * inch, 2.87 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            idu4_report.append(t)
            table_output = []
            table_output.append(['Date', 'up_state(%)', 'down_state(%)'])
            i = 0
            for date_time1 in date_days:
                table_output.append([date_time1, round(
                    up_state[i], 2), round(down_state[i], 2)])
                i += 1
            data = table_output
            t = Table(data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
            t.setStyle(
                TableStyle([('FONT', (0, 0), (2, 0), 'Helvetica-Bold', 10),
                            ('FONT', (0, 1), (2,
                                              int(
                                                  len(
                                                      table_output)) - 1), 'Helvetica', 9),
                            ('ALIGN', (1,
                                       0), (
                                 2, int(
                                     len(table_output)) - 1), 'CENTER'),
                            ('BACKGROUND',
                             (0, 0), (2, 0), (0.9, 0.9, 0.9)),
                            ('LINEABOVE',
                             (0, 0), (2, 0), 1.21, (0.35, 0.35, 0.35)),
                            ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                 'BACKGROUND', (1, i), (2, i), (0.95, 0.95, 0.95)),
                             ('BACKGROUND', (0, i - 1),
                              (0, i - 1), (0.98, 0.98, 0.98)),
                            ]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (1, i), (2, i), (0.9, 0.9, 0.9))
                    ]))

            t.setStyle(
                TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
            idu4_report.append(t)
            data1 = []
            if len(table_output) > 1:
                data1.append(['1-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            else:
                data1.append(['0-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            t = Table(data1, [7.10 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
            idu4_report.append(t)
            ###################################################################

            ########################################### IDU4 INTERFACE ########
            nw_interface = ['IDU4 NETWORK INTERFACE(eth0)']
            interface_index = 0
            for interface in nw_interface:
                idu4_report.append(Spacer(31, 31))
                cursor = db.cursor()
                result1 = ''
                # prepare SQL query to get total number of access points in this system
                # cursor.callproc("odu100_network_interface",(start_time,end_time,refresh_time,interface_index,ip_address))
                # result1=cursor.fetchall()
                if int(select_option) == 0:
                    sel_query = "select (idu.rxBytes),(idu.txBytes),idu.timestamp from idu_iduNetworkStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where  h.ip_address='%s' AND  idu.timestamp >= '%s' AND idu.timestamp <='%s' and idu.interfaceName = %s order by idu.timestamp desc" % (
                        ip_address, start_time, end_time, interface_index)
                    if int(limitFlag) == 0:
                        limit_data = ''
                    else:
                        limit_data = ' limit 16'
                    sel_query += limit_data

                else:
                    sel_query = "select (idu.rxBytes),(idu.txBytes),idu.timestamp from idu_iduNetworkStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where  h.ip_address='%s' AND date(idu.timestamp) <=current_date() AND date(idu.timestamp) >= current_date()-%s AND idu.interfaceName = %s order by idu.timestamp desc" % (
                        ip_address, total_days, interface_index)
                cursor.execute(sel_query)
                result1 = cursor.fetchall()
                table_output = bll_obj.nw_table_list_creation(
                    result1, interface, 'Receving(Kbps)', 'Transmitting(Kbps)', 'Time(HH:MM:SS)', )
                # close the database and cursor connection.
                cursor.close()
                data1 = []
                data1.append(['', interface, '', ''])
                t = Table(
                    data1, [.021 * inch, 2.62 * inch, 2.15 * inch, 2.22 * inch])
                t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                    'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
                idu4_report.append(t)

                data = table_output
                t = Table(data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
                t.setStyle(
                    TableStyle([('FONT', (0, 0), (2, 0), 'Helvetica-Bold', 10),
                                ('FONT', (0, 1), (2, int(len(
                                    table_output)) - 1), 'Helvetica', 9),
                                ('ALIGN', (1, 0), (2, int(
                                    len(table_output)) - 1), 'CENTER'),
                                ('BACKGROUND',
                                 (0, 0), (2, 0), (0.9, 0.9, 0.9)),
                                ('LINEABOVE', (0, 0),
                                 (2, 0), 1.21, (0.35, 0.35, 0.35)),
                                ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

                for i in range(1, len(table_output)):
                    if i % 2 == 1:
                        t.setStyle(
                            TableStyle(
                                [(
                                     'BACKGROUND', (1, i), (2, i), (0.95, 0.95, 0.95)),
                                 ('BACKGROUND', (0, i - 1), (0,
                                                             i - 1), (0.98, 0.98, 0.98)),
                                ]))
                    else:
                        t.setStyle(TableStyle([('BACKGROUND', (1, i), (2, i), (0.9, 0.9, 0.9))
                        ]))

                t.setStyle(TableStyle(
                    [('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
                idu4_report.append(t)
                data1 = []
                if len(table_output) > 1:
                    data1.append(['1-' + str(
                        len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
                else:
                    data1.append(['0-' + str(
                        len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
                t = Table(data1, [7.10 * inch])
                t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                    'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
                idu4_report.append(t)
                interface_index += 1
                ###############################################################

            ########################################### IDU4 INTERFACE ########
            nw_interface = ['IDU4 TDMOIP INTERFACE']
            interface_index = 0
            for interface in nw_interface:
                idu4_report.append(Spacer(31, 31))
                cursor = db.cursor()
                result1 = ''
                # prepare SQL query to get total number of access points in this system
                # cursor.callproc("odu100_network_interface",(start_time,end_time,refresh_time,interface_index,ip_address))
                # result1=cursor.fetchall()
                if int(select_option) == 0:
                    sel_query = "select IFNULL((idu.bytesTransmitted),0),IFNULL((idu.bytesReceived),0),idu.timestamp from  idu_tdmoipNetworkInterfaceStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where h.ip_address='%s' AND idu.timestamp <='%s' AND idu.timestamp >= '%s' AND indexid=%s order by idu.timestamp" % (
                        ip_address, end_time, start_time, interface_index)
                    if int(limitFlag) == 0:
                        limit_data = ''
                    else:
                        limit_data = ' limit 16'
                    sel_query += limit_data

                else:
                    sel_query = "select IFNULL((idu.bytesTransmitted),0),IFNULL((idu.bytesReceived),0),idu.timestamp from  idu_tdmoipNetworkInterfaceStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where h.ip_address='%s' AND date(idu.timestamp) <=current_date() AND date(idu.timestamp) >= current_date()-%s AND indexid=%s order by idu.timestamp" % (
                        ip_address, total_days, interface_index)
                cursor.execute(sel_query)
                result1 = cursor.fetchall()
                table_output = bll_obj.nw_table_list_creation(
                    result1, interface, 'Transmitting(Kbps)', 'Receving(Kbps)', 'Time(HH:MM:SS)')
                # close the database and cursor connection.
                cursor.close()
                data1 = []
                data1.append(['', interface, '', ''])
                t = Table(
                    data1, [.021 * inch, 2.62 * inch, 2.15 * inch, 2.22 * inch])
                t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                    'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
                idu4_report.append(t)

                data = table_output
                t = Table(data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
                t.setStyle(
                    TableStyle([('FONT', (0, 0), (2, 0), 'Helvetica-Bold', 10),
                                ('FONT', (0, 1), (2, int(len(
                                    table_output)) - 1), 'Helvetica', 9),
                                ('ALIGN', (1, 0), (2, int(
                                    len(table_output)) - 1), 'CENTER'),
                                ('BACKGROUND',
                                 (0, 0), (2, 0), (0.9, 0.9, 0.9)),
                                ('LINEABOVE', (0, 0),
                                 (2, 0), 1.21, (0.35, 0.35, 0.35)),
                                ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

                for i in range(1, len(table_output)):
                    if i % 2 == 1:
                        t.setStyle(
                            TableStyle(
                                [(
                                     'BACKGROUND', (1, i), (2, i), (0.95, 0.95, 0.95)),
                                 ('BACKGROUND', (0, i - 1), (0,
                                                             i - 1), (0.98, 0.98, 0.98)),
                                ]))
                    else:
                        t.setStyle(TableStyle([('BACKGROUND', (1, i), (2, i), (0.9, 0.9, 0.9))
                        ]))

                t.setStyle(TableStyle(
                    [('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
                idu4_report.append(t)
                data1 = []
                if len(table_output) > 1:
                    data1.append(['1-' + str(
                        len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
                else:
                    data1.append(['0-' + str(
                        len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
                t = Table(data1, [7.10 * inch])
                t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                    'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
                idu4_report.append(t)
                interface_index += 1
                #####################################################################################################
            # excel creatig end for network bandwidth
            pdf_doc.build(idu4_report)
            output_dict = {'success': 0, 'output': 'pdf downloaded'}
            return output_dict

        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def table_list_trap(self, result, table_name):
        """

        @param result:
        @param table_name:
        @return:
        """
        length = 5
        output = []
        first_h = ['Serevity', 'Event Id', 'Event State', 'Receive Date']
        output.append(first_h)
        if len(result) < 5:
            length = len(result)
        for i in range(0, length):
            temp_list = []
            temp_list = [result[i][0], result[i][1], result[i][2],
                         datetime.strptime(str(result[i][3]), '%a %b %d %H:%M:%S %Y').strftime('%x')]
            output.append(temp_list)
        return output

    def nw_table_list_creation(self, result, table_name, first_header, second_header, time):
        """

        @param result:
        @param table_name:
        @param first_header:
        @param second_header:
        @param time:
        @return:
        """
        output = []
        first_h = [time, first_header, second_header]
        output.append(first_h)
        if result is not None:
            for i in range(len(result) - 1):
                rx_byte = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                tx_byte = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                temp_list = []
                temp_list = [result[i][2].strftime('%d-%m-%Y %H:%M'), (
                    0 if rx_byte <= 0 else rx_byte), (0 if tx_byte <= 0 else tx_byte)]
                output.append(temp_list)
        return output
