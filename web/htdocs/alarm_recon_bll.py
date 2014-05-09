from datetime import datetime as dt
import datetime
import os
import socket
import time

import MySQLdb
import pysnmp
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.proto.api import v2c

from common_bll import db_connect, host_status_dict, Essential


class Bulk():
    """

    @param ip_address:
    @param port:
    @param community:
    @param timeout:
    @param varbinds:
    @param limit:
    """

    def __init__(self, ip_address, port=161, community='public', timeout=5, varbinds=20, limit=100):
        self.ip_address = ip_address
        self.port = port
        self.community = community
        self.bulk_result = {}
        self.var_binds = varbinds
        self.main_oid = ''
        self.agent = 'alarm-agent'
        self.timeout = timeout
        self.limit = limit
        self.make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

    def engine(self):
        """


        @return:
        """
        err_dict = {}
        try:
            success = 1
            port = int(self.port)
            self.snmpEngine = engine.SnmpEngine()
            config.addV1System(self.snmpEngine, self.agent, self.community)

            config.addTargetParams(
                self.snmpEngine, 'myParams', self.agent, 'noAuthNoPriv', 1)

            config.addTargetAddr(
                self.snmpEngine, 'myRouter', config.snmpUDPDomain,
                (self.ip_address, port), 'myParams'
            )
            config.addSocketTransport(
                self.snmpEngine,
                config.snmpUDPDomain,
                udp.UdpSocketTransport().openClientMode()
            )
            success = 0
        except pysnmp.proto.error.ProtocolError as err:
            success = 1
            err_dict[99] = 'pyproto err ' + str(err)
        except Exception, e:
            success = 1
            err_dict[99] = 'Exception : snmp Engine is not able to bind '
        finally:
            result = {}
            result['success'] = success
            result['result'] = err_dict
            return result

    def cbFun(
            self, sendRequesthandle, errorIndication, errorStatus, errorIndex,
            varBindTable, cbCtx):
        """

        @param sendRequesthandle:
        @param errorIndication:
        @param errorStatus:
        @param errorIndex:
        @param varBindTable:
        @param cbCtx:
        @return:
        """
        bulk_list = self.bulk_result['result']
        success = 3
        err_dict = {}
        try:
            if errorIndication:
                err_dict[553] = str(errorIndication)
                success = 1
                return
            if errorStatus:
                err_dict[int(errorStatus)] = errorStatus.prettyPrint()
                success = 1
                # print " ::
                # ",errorIndex,int(errorStatus),errorStatus.prettyPrint()
                return
            success = 0
            for varBindRow in varBindTable:
                for oid, val in varBindRow:
                    temp_split = oid.prettyPrint().split(self.main_oid)
                    if len(temp_split) > 1:
                        pass
                    else:
                        # print " table finished "
                        success = 2
                        return
                    if isinstance(val, v2c.IpAddress):
                        value = str(val.prettyPrint())
                    else:
                        value = str(val)  # val.prettyPrint() #str(val)
                    bulk_list.append((oid.prettyPrint(), value))

            for oid, val in varBindTable[-1]:
                if val is not None:
                    # print " break NONE "
                    break
            else:
                # print " else "
                return # stop on end-of-table
            if len(bulk_list) >= self.limit:
                return
            time.sleep(self.timeout)
            return 1  # continue walking
        finally:
            self.bulk_result = {}
            self.bulk_result['success'] = success
            if success == 1:
                if len(bulk_list) > 1:
                    self.bulk_result['result'] = bulk_list
                    self.bulk_result['error'] = err_dict
                    self.bulk_result['success'] = 4
                else:
                    self.bulk_result['result'] = err_dict
            else:
                self.bulk_result['result'] = bulk_list

    def bulkget(self, oid):
        """

        @param oid:
        @return:
        """
        err_dict = {}
        try:
            snmp_result = {}
            self.bulk_result = {}
            self.bulk_result['result'] = []
            self.bulk_result['success'] = 1
            success = 1
            self.main_oid = oid.strip(".")
            # print " running"
            cmdgen.BulkCommandGenerator().sendReq(
                self.snmpEngine, 'myRouter', 0, self.var_binds, (
                    (self.make_tuple(self.main_oid), None),), self.cbFun, None
            )

            self.snmpEngine.transportDispatcher.runDispatcher()

            # print " exit "

            if len(self.bulk_result) > 0:
                if self.bulk_result['success'] == 2 or self.bulk_result['success'] == 3 or self.bulk_result[
                    'success'] == 0 or self.bulk_result['success'] == 4:
                    success = 0
                    oid_li = []
                    var_dict = {}
                    oid_values_list = []
                    varBindTable = self.bulk_result['result']
                    for name, value in varBindTable:
                        # print '%s = %s' % (name, value)
                        oid_values_list = name.split(
                            self.main_oid)[1].strip('.').split('.')
                        if len(oid_values_list) > 0:
                            oid_no = oid_values_list.pop(0)
                        else:
                            success = 1
                            return

                        if oid_li.count(oid_no) == 0:
                            oid_li.append(oid_no)
                            count = 0
                            flag = 1
                            if len(oid_li) == 1:
                                flag = 0

                        if flag == 0:
                            count += 1
                            li = []
                            for i in oid_values_list:
                                li.append(i)
                            li.append(value)
                            var_dict[count] = li

                        else:
                            count += 1
                            li = var_dict[count]
                            li.append(value)
                            var_dict[count] = li
                    snmp_result['success'] = success
                    snmp_result['result'] = var_dict
                    if self.bulk_result['success'] == 4:
                        snmp_result[
                            'error'] = self.bulk_result.get('error', {})

                        # print snmp_result
                elif self.bulk_result['success'] == 1:
                    snmp_result = self.bulk_result
                self.bulk_result = {}

        except socket.error as sock_err:
            success = 1
            err_dict[551] = str(sock_err)
        except pysnmp.proto.error.ProtocolError as err:
            success = 1
            err_dict[99] = 'pyproto err ' + str(err)
        except TypeError as err:
            success = 1
            err_dict[99] = 'type err ' + str(err)
        except Exception as e:
            print " Exception BULK ", str(e)
            # print traceback.print_exc(e)
            success = 1
            err_dict[99] = 'pysnmp exception ' + str(e)
        finally:
            if len(err_dict) > 1:
                snmp_result['success'] = success
                snmp_result['result'] = err_dict
            if len(snmp_result) < 1:
                snmp_result['success'] = 1
                snmp_result['result'] = {224: 'Unable to get Error '}
            return snmp_result


class CustomException(Exception):
    """

    @param args:
    """

    def __init__(self, *args):
        self.msg, self.code = 'Not Defined', 100
        if len(args) == 2:
            for arg in args:
                if isinstance(arg, str):
                    self.msg = arg
                elif isinstance(arg, int):
                    self.code = arg

    def __str__(self):
        return repr(self.msg)


class AlarmRecon():
    """

    @param host_id:
    @param alarms_limit:
    @param host_ip:
    """

    def __init__(self, host_id, alarms_limit=100, host_ip=None):
        self.host_id = str(host_id)
        self.alarms_limit = alarms_limit
        self.host_ip = host_ip
        self.oid = '.1.3.6.1.4.1.26149.2.2.15.1.1'
        self.db = ''
        self.alarm_status = 15

    def get_snmp_result(self, port, community):
        """

        @param port:
        @param community:
        @return:
        """
        err_dict = {}
        success = 0
        recon_dict = {}
        first_time = None
        last_time = None
        var_binds = 20
        is_es_set = 0
        success_dict = {}
        result = {}
        try:
            es = Essential()
            host_state = es.host_status(self.host_id, self.alarm_status)
            if host_state == 0:
                is_es_set = 1
                if self.alarms_limit <= 20:
                    var_binds = self.alarms_limit
                bulk_obj = Bulk(self.host_ip, port,
                                community, 2, var_binds, self.alarms_limit)
                recon_li = []
                recon_length = 0
                result = bulk_obj.engine()
                if result['success'] == 0:
                    result = bulk_obj.bulkget(self.oid)
                    es.host_status(self.host_id, 0, None, self.alarm_status)
                    is_es_set = 0
                    if result['success'] == 0:
                        result = result['result']
                        recon_length = len(result)
                        ##                        print " result ", result
                        recon_dict = {}
                        trapTimeStamp = 'timestamp'
                        perceivedSeverity = 'severity'
                        componentId = 'ip'
                        eventDesc = 'eventdesc'
                        format = '%d-%m-%Y %H:%M:%S'
                        severity_dict = {
                            'CLEAR ALARM': 0, 'INFORMATIONAL ALARM': 1, 'NORMAL ALARM': 2,
                            'MINOR ALARM': 3, 'MAJOR ALARM': 4, 'CRITICAL ALARM': 5}
                        for key in result:
                        ##                            print " key ", key
                            temp_di = eval(result[key][2].replace(
                                '\n', '').replace("},", "}"))
                            temp_di['severity'] = severity_dict.get(
                                temp_di['severity'], 2)
                            temp_di[
                                'event'] = temp_di['eventdesc'].split("::")[0]
                            temp_di['event_id'] = str(
                                odu100.get(temp_di['event']))
                            dt_value = dt.strptime(
                                temp_di['timestamp'].strip(), format)
                            if first_time:
                                pass
                            else:
                            ##                                print " dt_value ", dt_value
                                first_time = dt_value
                            last_time = dt_value
                            if dt_value in recon_dict:
                                li = recon_dict[dt_value] if isinstance(
                                    recon_dict[dt_value], list) else [recon_dict[dt_value]]
                                li.append(temp_di)
                                recon_dict[dt_value] = li
                            else:
                                recon_dict[dt_value] = temp_di
                            recon_li.append(dt_value)
                            temp_di = {}
                    else:
                        success = 1
                        err_dict = result['result']
                        return
                else:
                    success = 1
                    err_dict = result['result']
                    return
            else:
                success = 1
                err_dict = " Device is busy, Device %s is in progress." % host_status_dict.get(
                    int(host_state), "other operation")
        except Exception, e:
            success = 1
            ##            print " SELF GET SNMP RESULT ", str(e)
            err_dict = str(e)
        finally:
            if is_es_set:
                es.host_status(self.host_id, 0, None, self.alarm_status)
            success_dict['success'] = success
            if success == 0:
                success_dict['recon_length'] = recon_length
                success_dict['recon_dict'] = recon_dict
                success_dict['first_time'] = first_time
                success_dict['last_time'] = last_time
                if 'error' in result:
                    success_dict['error'] = result['error']
            else:
                success_dict['err_dict'] = err_dict
            return success_dict

    def recon(self):
        # select community, port
        # FIXME: this function has a remaining improvement in sql query
        #      in which we select `device_sent_date`
        #      `device_sent_date` should be selected more carefully
        #       because every thing else is depented on this
        # recheck and improve
        # there seems to be too many condition in this function
        # we could have separate function that would insert in current and clear
        # or revise the algorithm
        """


        @return: @raise:
        """
        try:
            how_many_rows = 0
            err_dict = {}
            success_dict = {}
            success = 1
            update_query = None
            if self.host_ip:
                snmp_details = "SELECT `ip_address`, `snmp_read_community`, `snmp_port`, `snmp_version_id` FROM `hosts` WHERE `ip_address` = '%s' and is_deleted = 0" % (
                    self.host_ip)
            elif self.host_id:
                snmp_details = "SELECT `ip_address`, `snmp_read_community`, `snmp_port`, `snmp_version_id` FROM `hosts` WHERE `host_id` = '%s' and is_deleted = 0" % (
                    self.host_id)
            else:
                raise CustomException(
                    " arguments are not proper:: Neither Host id nor IP is specified", 1)

            if self.alarms_limit <= 0:
                raise CustomException(
                    " arguments are not proper:: Request for 0 alarm reconciliation", 1)

            self.db = db_connect()
            if not isinstance(self.db, MySQLdb.connection):
                raise CustomException(
                    " error in db connection:: " + str(self.db), 11)

            try:
                cursor = self.db.cursor()
                cursor.execute(snmp_details)
                db_snmp_details = cursor.fetchall()
            except Exception, e:
                raise CustomException(
                    " error in query execution:: " + str(e), 12)
            else:
                cursor.close()
                self.db.close()  # can be a db_close() function
                self.db = ''
                if len(db_snmp_details) > 0 and len(db_snmp_details[0]) == 4:
                    self.host_ip = db_snmp_details[0][0]
                    community = db_snmp_details[0][1]
                    port = db_snmp_details[0][2]
                    version = db_snmp_details[0][3]
                else:
                    raise CustomException(
                        " snmp details not found for host ", 1)

            file1 = '/omd/daemon/alarm_mask.rg'
            file2 = '/omd/daemon/mapping_alarm.rg'

            if os.path.isfile(file1) and os.path.isfile(file2):
                execfile(file1, globals())
                execfile(file2, globals())
            else:
                raise CustomException(" alarm mask files not exists ", 1)

            if ('mask_alarm_dict' in vars() or 'mask_alarm_dict' in globals()) and (
                    'mask_severity_dict' in vars() or 'mask_severity_dict' in globals()) and (
                    'clear_alarm_dict' in vars() or 'clear_alarm_dict' in globals()) and (
                    'real_alarm_list' in vars() or 'real_alarm_list' in globals()) and (
                    'odu100' in vars() or 'odu100' in globals()):
                pass
            else:
                raise CustomException(" alarm mask files execution failed ", 1)

            snmp_result_dict = {}
            snmp_result_dict = self.get_snmp_result(port, community)
            ##            print snmp_result_dict
            if snmp_result_dict['success'] == 0:
                recon_dict = snmp_result_dict.get('recon_dict', {})
                first_time = snmp_result_dict.get('first_time')
                last_time = snmp_result_dict.get('last_time')
                recon_length = snmp_result_dict.get('recon_length', 0)
                if 'error' in snmp_result_dict:
                    success_dict['error'] = snmp_result_dict['error']
            else:
                success = 1
                err_dict = snmp_result_dict.get('err_dict', {})
                return

            ##            print " recon_dict ", recon_dict
            if len(recon_dict) > 0:
                update_query = "UPDATE trap_alarms INNER JOIN trap_alarm_clear ON trap_alarms.agent_id = trap_alarm_clear.agent_id \
                    INNER JOIN trap_alarm_current ON trap_alarms.agent_id = trap_alarm_current.agent_id \
                    SET trap_alarms.is_reconcile = '0', trap_alarm_clear.is_reconcile = '0', trap_alarm_current.is_reconcile = '0' \
                    WHERE trap_alarms.agent_id = '%s' and trap_alarms.is_reconcile = '1' " % (self.host_ip)

                device_sent_date = None
                first_sql = "SELECT `device_sent_date` FROM `trap_alarms` where `timestamp` = (select max(`timestamp`) from trap_alarms WHERE agent_id='%s')" % (
                self.host_ip)
                print " first_sql ", first_sql
                self.db = db_connect()
                if not isinstance(self.db, MySQLdb.connection):
                    raise CustomException(
                        " error in db connection:: " + str(self.db), 11)
                try:
                    cursor = self.db.cursor()
                    cursor.execute(first_sql)
                    result_sent_date = cursor.fetchall()
                except Exception, e:
                    raise CustomException(
                        " error in query execution:: " + str(e), 12)
                else:
                    cursor.close()
                    self.db.close()

                if len(result_sent_date) > 0 and len(result_sent_date[0]) > 0:
                    device_sent_date = result_sent_date[0][0]

                # print " device_sent_date, first_time >> ", device_sent_date, first_time

                if device_sent_date == None or device_sent_date > first_time:
                ##                    print " insert all of them"
                    # insert all of them
                    ins_query = "INSERT INTO trap_alarms (event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity, trap_event_id, trap_event_type, \
                                    manage_obj_id, manage_obj_name, component_id, trap_ip, description, device_sent_date, is_reconcile, timestamp) values"
                    flag = 0
                    prev_device_time = None
                    ins_timestamp = dt.now() - (first_time - last_time)
                    for i in sorted(recon_dict.keys()):
                    ##                        print " i ", i
                        if isinstance(recon_dict[i], list):
                            for ldi in recon_dict[i]:
                                if flag:
                                    ins_timestamp += (i - prev_device_time)
                                    ins_query += ", ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (
                                    self.host_ip, i.time(), ins_timestamp.ctime(), ldi['severity'], ldi['event_id'],
                                    ldi['event'],
                                    ldi['ip'], ldi['eventdesc'], i, ins_timestamp)
                                else:
                                    ins_query += "('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (
                                    self.host_ip, i.time(), ins_timestamp.ctime(), ldi['severity'], ldi['event_id'],
                                    ldi['event'],
                                    ldi['ip'], ldi['eventdesc'], i, ins_timestamp)
                                    flag = 1
                                prev_device_time = i
                        else:
                            if flag:
                                ins_timestamp += (i - prev_device_time)
                                ins_query += ", ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, i.time(), ins_timestamp.ctime(), recon_dict[i]['severity'],
                                             recon_dict[i]['event_id'], recon_dict[i]['event'],
                                             recon_dict[i]['ip'], recon_dict[i]['eventdesc'], i, ins_timestamp)
                            else:
                                flag = 1
                                ins_query += "('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, i.time(), ins_timestamp.ctime(), recon_dict[i]['severity'],
                                             recon_dict[i]['event_id'], recon_dict[i]['event'],
                                             recon_dict[i]['ip'], recon_dict[i]['eventdesc'], i, ins_timestamp)
                            prev_device_time = i

                    if flag:
                        self.db = db_connect()
                        if not isinstance(self.db, MySQLdb.connection):
                            raise CustomException(
                                " error in db connection:: " + str(self.db), 11)
                        try:
                            cursor = self.db.cursor()
                            if update_query:
                                cursor.execute(update_query)
                                self.db.commit()
                            how_many_rows = cursor.execute(
                                ins_query)  # a how many alarm reconcile value can be get
                            self.db.commit()
                        except Exception, e:
                            raise CustomException(
                                " error in query execution:: " + str(e), 12)
                        else:
                            cursor.close()
                            self.db.close()
                        ##                    print ins_query
                        ##                    print how_many_rows
                    success = 0
                    success_dict['msg'] = ' Alarm Reconciliation successful, %s new alarms found ' % (
                        how_many_rows) if how_many_rows else 'Alarm Reconciliation successful'
                    success_dict['time'] = dt.now()
                    return

                else:
                ##                    print " insert else"
                    sql = "SELECT `device_sent_date`,`trap_event_id`,`trap_event_type`,`serevity`,`timestamp` FROM \
                    (SELECT `device_sent_date`,`trap_event_id`,`trap_event_type`,`serevity`,`timestamp` FROM `trap_alarms` \
                    WHERE agent_id='%s' order by timestamp desc limit %s) as t \
                    where `device_sent_date` >= '%s' " % (self.host_ip, recon_length, last_time)
                    ##                    print " sql query ", sql
                    sql_result = ()
                    self.db = db_connect()
                    if not isinstance(self.db, MySQLdb.connection):
                        raise CustomException(
                            " error in db connection:: " + str(self.db), 11)
                    try:
                        cursor = self.db.cursor()
                        cursor.execute(sql)
                        sql_result = cursor.fetchall()
                    ##                        print "sql_result ", sql_result
                    except Exception, e:
                        raise CustomException(
                            " error in query execution:: " + str(e), 12)
                    else:
                        cursor.close()
                        self.db.close()
                    tup_di = {}
                    tup_li = []
                    timestamp_tobe = None  # define a real something
                    ##                    print
                    ##                    print " sql, length ", len(sql_result), recon_length
                    ##                    print " sql, first ", sql_result[0][0], first_time
                    ##                    print " sql, last ", sql_result[-1][0], last_time
                    ##                    print
                    if len(sql_result) == recon_length:
                        if sql_result[0][0] == first_time and sql_result[-1][0] == last_time:
                        # if sql_result[0][0] == first_time and
                        # sql_result[-1][0] == first_time:
                            success = 0
                            success_dict[
                                'msg'] = 'Alarm Reconciliation successful, Already upto date'
                            success_dict['time'] = dt.now()
                            return
                        elif sql_result[0][0] == first_time:
                            for i in sql_result:
                                tup_li.append(i[0])
                                if i[0] in tup_di:
                                    li = tup_di[i[0]] if isinstance(
                                        tup_di[i[0]], list) else [tup_di[i[0]]]
                                    li.append({'event_id': str(i[1]),
                                               'event': i[2], 'severity': int(i[3]), 'dbtime': i[4]})
                                    tup_di[i[0]] = li
                                else:
                                    tup_di[i[0]] = {'event_id': str(
                                        i[1]), 'event': i[2], 'severity': int(i[3]), 'dbtime': i[4]}
                                if i[0] >= last_time:
                                    pass
                                else:
                                    break
                        else:
                            for i in sql_result:
                                tup_li.append(i[0])
                                if i[0] in tup_di:
                                    li = tup_di[i[0]] if isinstance(
                                        tup_di[i[0]], list) else [tup_di[i[0]]]
                                    li.append({'event_id': str(i[1]),
                                               'event': i[2], 'severity': int(i[3]), 'dbtime': i[4]})
                                    tup_di[i[0]] = li
                                else:
                                    tup_di[i[0]] = {'event_id': str(
                                        i[1]), 'event': i[2], 'severity': int(i[3]), 'dbtime': i[4]}

                    else:
                        for i in sql_result:
                            tup_li.append(i[0])
                            if i[0] in tup_di:
                                li = tup_di[i[0]] if isinstance(
                                    tup_di[i[0]], list) else [tup_di[i[0]]]
                                li.append({'event_id': str(i[1]),
                                           'event': i[2], 'severity': int(i[3]), 'dbtime': i[4]})
                                tup_di[i[0]] = li
                            else:
                                tup_di[i[0]] = {'event_id': str(
                                    i[1]), 'event': i[2], 'severity': int(i[3]), 'dbtime': i[4]}
                            if i[0] >= last_time:
                                pass
                            else:
                                break

                            ##                    from copy import deepcopy
                            ##                    print "tup_li ", tup_li
                            ##                    print " tup_di ", tup_di
                    timestamp_tobe = tup_di[tup_li[-1]][0]['dbtime'] if isinstance(
                        tup_di[tup_li[-1]], list) else tup_di[tup_li[-1]][
                        'dbtime']  # datetime.datetime(2012, 7, 23, 19, 7, 55) # assign something real
                    timestamp = tup_li[-1]
                    current_di = {}
                    clear_di = {}
                    remain_di = {}
                    print " tup_li ", tup_li
                    for i in sorted(recon_dict.keys()):
                        temp_di = {}
                        temp_li = []
                        if i not in tup_di:
                            if i > timestamp:
                                timestamp_tobe += (i - timestamp)
                            else:
                                timestamp_tobe -= (timestamp - i)

                            print ">> i ", i, ' timestamp ', timestamp, ' timestamp_tobe ', timestamp_tobe
                            if isinstance(recon_dict[i], list):
                                temp_li = recon_dict[i]
                                for j in recon_dict[i]:
                                    temp_di[j['event_id']] = timestamp_tobe
                                if len(temp_di):
                                    remain_di[i] = temp_di
                            else:
                                remain_di[i] = timestamp_tobe

                        else:
                            try:
                                timestamp_tobe = tup_di[i]['dbtime']
                                if isinstance(recon_dict[i], list):
                                    # temp_li = deepcopy(recon_dict[i])
                                    temp_li = recon_dict[i]
                                    for k in temp_li:
                                        if k['event_id'] == tup_di[i]['event_id']:
                                            temp_li.remove(k)
                                    for j in temp_li:
                                        temp_di[j['event_id']] = timestamp_tobe
                                    if len(temp_di):
                                        remain_di[i] = temp_di

                            except TypeError:
                                if isinstance(recon_dict[i], list):
                                    for j in recon_dict[i]:
                                        found = 0
                                        for k in tup_di[i]:
                                            timestamp_tobe = k['dbtime']
                                            if k['event_id'] == j['event_id']:
                                                found = 1
                                                break
                                        if not found:
                                            temp_di[j[
                                                'event_id']] = timestamp_tobe
                                    if len(temp_di):
                                        remain_di[i] = temp_di

                                    # print ":::: i ", i, ' timestamp ', timestamp, ' timestamp_tobe ',
                                    # timestamp_tobe
                        timestamp = i
                        if (i in remain_di) > 0:
                            if isinstance(recon_dict[i], list):
                                for j in recon_dict[i]:
                                    print j['event_id']
                                    if j['event_id'] in mask_alarm_dict:
                                        current_di[j[
                                            'event_id']] = [i, timestamp_tobe]
                                        if j['event_id'] in clear_di:
                                            del clear_di[j['event_id']]

                                    elif j['event_id'] in mask_alarm_dict.values():
                                        clear_di[j[
                                            'event_id']] = [i, timestamp_tobe]
                                        if j['event_id'] in current_di:
                                            del current_di[j['event_id']]
                            else:
                                if recon_dict[i]['event_id'] in mask_alarm_dict:
                                    if recon_dict[i]['event_id'] in real_alarm_list:
                                        current_di[recon_dict[i][
                                            'event_id']] = [i, timestamp_tobe]
                                        if recon_dict[i]['event_id'] in clear_di:
                                            del clear_di[
                                                recon_dict[i]['event_id']]
                                    else:
                                        current_di[recon_dict[i][
                                            'event_id']] = [i, timestamp_tobe]
                                        if recon_dict[i]['event_id'] in clear_di:
                                            del clear_di[recon_dict[
                                                i]['event_id']]

                                elif recon_dict[i]['event_id'] in mask_alarm_dict.values():
                                    clear_di[
                                        recon_dict[i]['event_id']] = [i, timestamp_tobe]
                                    if recon_dict[i]['event_id'] in current_di:
                                        del current_di[
                                            recon_dict[i]['event_id']]

                    del_clear_li = []
                    # code for that > clear entry is liable to insert or not
                    for i in clear_di:
                        sure_replace = 0
                        is_break = 0
                        li = [key for key, value in mask_alarm_dict.iteritems(
                        ) if value == i]
                        ##                        print "      TESTING ", i, li
                        cl_dt = clear_di[i][0]
                        if li[0] in current_di:
                            if current_di[li[0]][0] > cl_dt:
                                cr_dt = current_di[li[0]][0]
                                sure_replace = 1
                        if sure_replace:
                            for k in sorted(tup_di.keys()):
                                try:
                                    if tup_di[k]['event_id'] == i:
                                        if cr_dt < k:
                                            clear_di[i] = [k,
                                                           clear_di[i][1] + (k - cl_dt)]
                                            is_break = 1
                                            break
                                except Exception, e:
                                    for ldi in tup_di[k]:
                                        if ldi['event_id'] == i:
                                            if cr_dt < k:
                                                clear_di[i] = [k, clear_di[
                                                                      i][1] + k - cl_dt]
                                                is_break = 1
                                                break
                        else:
                            cr_dt = None
                            for k in sorted(tup_di.keys()):
                                if k < cl_dt:
                                    try:
                                        if tup_di[k]['event_id'] == li[0]:
                                            cr_dt = k
                                    except Exception, e:
                                        print str(e)
                                        for ldi in tup_di[k]:
                                            if ldi['event_id'] == li[0]:
                                                cr_dt = k
                                elif k > cl_dt:
                                    if cr_dt:
                                        try:
                                            if tup_di[k]['event_id'] == i:
                                                break
                                        except Exception, e:
                                            for ldi in tup_di[k]:
                                                if ldi['event_id'] == li[0]:
                                                    break
                                    else:
                                        is_break = 1

                        if not is_break:
                            del_clear_li.append(i)

                    if len(del_clear_li) > 0:
                        for i in del_clear_li:
                            del clear_di[i]
                        # if real alarm behavior changed in trap alarm then change
                    # this too
                    if len(current_di) > 0:
                        for i in tup_di:
                            try:
                                cur_event_li = [key for key, value in mask_alarm_dict.iteritems(
                                ) if value == tup_di[i]['event_id']]
                                if len(cur_event_li) > 0:
                                    if cur_event_li[0] in current_di:
                                        if current_di[cur_event_li[0]][0] < i:
                                            del current_di[cur_event_li[0]]
                            except Exception as e:
                                for k in tup_di[i]:
                                    cur_event_li = [key for key,
                                                            value in mask_alarm_dict.iteritems() if
                                                    value == k['event_id']]
                                    if len(cur_event_li) > 0:
                                        if cur_event_li[0] in current_di:
                                            if current_di[cur_event_li[0]][0] < i:
                                                del current_di[cur_event_li[0]]

                    ins_query = "INSERT INTO trap_alarms (event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity, trap_event_id, trap_event_type, \
                                    manage_obj_id, manage_obj_name, component_id, trap_ip, description, device_sent_date, is_reconcile, timestamp) values"
                    flag = 0
                    ##                    print "\n   remain_di  ", remain_di
                    # print "  >>>>>>  clear ", clear_di, "       >>>>  current ", current_di
                    for i in sorted(remain_di.keys()):
                        if isinstance(recon_dict[i], list):
                            for ldi in recon_dict[i]:
                                if flag:
                                    ins_query += ", ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (
                                    self.host_ip, i.time(), remain_di[i].get(ldi['event_id']).ctime(), ldi['severity'],
                                    ldi['event_id'], ldi['event'],
                                    ldi['ip'], ldi['eventdesc'], i, remain_di[i].get(ldi['event_id']))
                                else:
                                    ins_query += "('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (
                                    self.host_ip, i.time(), remain_di[i].get(ldi['event_id']).ctime(), ldi['severity'],
                                    ldi['event_id'], ldi['event'],
                                    ldi['ip'], ldi['eventdesc'], i, remain_di[i].get(ldi['event_id']))
                                    flag = 1
                        else:
                            if flag:
                                ins_query += ", ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, i.time(), remain_di[i].ctime(), recon_dict[i]['severity'],
                                             recon_dict[i]['event_id'], recon_dict[i]['event'],
                                             recon_dict[i]['ip'], recon_dict[i]['eventdesc'], i, remain_di[i])
                            else:
                                flag = 1
                                ins_query += "('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, i.time(), remain_di[i].ctime(), recon_dict[i]['severity'],
                                             recon_dict[i]['event_id'], recon_dict[i]['event'],
                                             recon_dict[i]['ip'], recon_dict[i]['eventdesc'], i, remain_di[i])

                    if flag == 0:
                        ins_query = None
                    flag = 0
                    ins_clear = "INSERT INTO trap_alarm_clear \
                    (event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity, trap_event_id, trap_event_type, manage_obj_id, manage_obj_name, \
                    component_id, trap_ip, description, device_sent_date, is_reconcile, timestamp) values"
                    for i in sorted(clear_di.keys()):
                        if isinstance(recon_dict[clear_di[i][0]], list):
                            for ldi in recon_dict[clear_di[i][0]]:
                                if flag:
                                    ins_clear += ", ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, clear_di[i][0].time(), clear_di[i][1].ctime(),
                                             mask_severity_dict.get(ldi['event_id'], ldi['severity']), ldi['event_id'],
                                             clear_alarm_dict.get(ldi['event_id'], ldi['event']),
                                             ldi['ip'], ldi['eventdesc'], clear_di[i][0], clear_di[i][1])
                                else:
                                    ins_clear += " ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, clear_di[i][0].time(), clear_di[i][1].ctime(),
                                             mask_severity_dict.get(ldi['event_id'], ldi['severity']), ldi['event_id'],
                                             clear_alarm_dict.get(ldi['event_id'], ldi['event']),
                                             ldi['ip'], ldi['eventdesc'], clear_di[i][0], clear_di[i][1])
                                    flag = 1
                        else:
                            if flag:
                                ins_clear += ", ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, clear_di[i][0].time(), clear_di[i][1].ctime(),
                                             mask_severity_dict.get(recon_dict[clear_di[i][0]]['event_id'],
                                                                    recon_dict[clear_di[i][0]]['severity']),
                                             recon_dict[clear_di[i][0]]['event_id'],
                                             clear_alarm_dict.get(recon_dict[clear_di[i][0]]['event_id'],
                                                                  recon_dict[clear_di[i][0]]['event']),
                                             recon_dict[clear_di[i][0]]['ip'], recon_dict[clear_di[i][0]]['eventdesc'],
                                             clear_di[i][0], clear_di[i][1])
                            else:
                                flag = 1
                                ins_clear += "('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, clear_di[i][0].time(), clear_di[i][1].ctime(),
                                             mask_severity_dict.get(recon_dict[clear_di[i][0]]['event_id'],
                                                                    recon_dict[clear_di[i][0]]['severity']),
                                             recon_dict[clear_di[i][0]]['event_id'],
                                             clear_alarm_dict.get(recon_dict[clear_di[i][0]]['event_id'],
                                                                  recon_dict[clear_di[i][0]]['event']),
                                             recon_dict[clear_di[i][0]]['ip'], recon_dict[clear_di[i][0]]['eventdesc'],
                                             clear_di[i][0], clear_di[i][1])

                    if flag == 0:
                        ins_clear = None

                    flag = 0
                    ins_current = "INSERT INTO trap_alarm_current \
                    (event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity, trap_event_id, trap_event_type, manage_obj_id, manage_obj_name, \
                    component_id, trap_ip, description, device_sent_date, is_reconcile, timestamp) values"
                    for i in sorted(current_di.keys()):
                        if isinstance(recon_dict[current_di[i][0]], list):
                        ##                            print " in ", recon_dict[current_di[i][0]]
                            for ldi in recon_dict[current_di[i][0]]:
                                if flag:
                                    ins_current += ", ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, current_di[i][0].time(), current_di[i][1].ctime(),
                                             mask_severity_dict.get(ldi['event_id'], ldi['severity']), ldi['event_id'],
                                             ldi['event'],
                                             ldi['ip'], ldi['eventdesc'], current_di[i][0], current_di[i][1])
                                else:
                                    ins_current += " ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, current_di[i][0].time(), current_di[i][1].ctime(),
                                             mask_severity_dict.get(ldi['event_id'], ldi['severity']), ldi['event_id'],
                                             ldi['event'],
                                             ldi['ip'], ldi['eventdesc'], current_di[i][0], current_di[i][1])
                                    flag = 1
                        else:
                        ##                            print " out  ", recon_dict[current_di[i][0]]
                            if flag:
                                ins_current += ", ('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, current_di[i][0].time(), current_di[i][1].ctime(),
                                             mask_severity_dict.get(recon_dict[current_di[i][0]]['event_id'],
                                                                    recon_dict[current_di[i][0]]['severity']),
                                             recon_dict[current_di[i][0]]['event_id'],
                                             recon_dict[current_di[i][0]]['event'],
                                             recon_dict[current_di[i][0]]['ip'],
                                             recon_dict[current_di[i][0]]['eventdesc'], current_di[i][0],
                                             current_di[i][1])
                            else:
                                flag = 1
                                ins_current += "('ruTrap', '.1.3.6.1.4.1.26149.2.4.0.0.1', '%s', '%s', '%s', '%s', '%s', '%s', '500', 'RU', '504', '%s', '%s', '%s', '1', '%s')\
                                        " % (self.host_ip, current_di[i][0].time(), current_di[i][1].ctime(),
                                             mask_severity_dict.get(recon_dict[current_di[i][0]]['event_id'],
                                                                    recon_dict[current_di[i][0]]['severity']),
                                             recon_dict[current_di[i][0]]['event_id'],
                                             recon_dict[current_di[i][0]]['event'],
                                             recon_dict[current_di[i][0]]['ip'],
                                             recon_dict[current_di[i][0]]['eventdesc'], current_di[i][0],
                                             current_di[i][1])

                    if flag == 0:
                        ins_current = None

                    if len(remain_di) > 0:
                        self.db = db_connect()
                        if not isinstance(self.db, MySQLdb.connection):
                            raise CustomException(
                                " error in db connection:: " + str(self.db), 11)
                        try:
                            cursor = self.db.cursor()
                            if update_query:
                                cursor.execute(update_query)
                                self.db.commit()
                            how_many_rows = cursor.execute(
                                ins_query)  # a how many alarm reconcile value can be get
                            ##                            print
                            ##                            print "  INS ", ins_query
                            ##                            print
                            self.db.commit()
                            if ins_clear:
                                cursor.execute(
                                    ins_clear)  # a how many alarm reconcile value can be get
                                self.db.commit()
                            if ins_current:
                                cursor.execute(
                                    ins_current)  # a how many alarm reconcile value can be get
                                self.db.commit()
                            print " last ", remain_di
                        except Exception, e:
                            raise CustomException(
                                " error in query execution:: " + str(e), 13)
                        else:
                            cursor.close()
                            self.db.close()

                    success = 0
                    success_dict['msg'] = ' Alarm Reconciliation successful '
                    success_dict['time'] = dt.now()
                    return

        except Exception, e:
            import traceback

            print traceback.format_exc()
            success = 1
            err_dict = str(traceback.format_exc())
            print str(e)
        finally:
            final_result_dict = {}
            final_result_dict['success'] = success
            if success == 0 and len(success_dict) > 0:
                self.db = db_connect()
                if isinstance(self.db, MySQLdb.connection):
                    try:
                        cursor = self.db.cursor()
                        sql = "update alarm_recon set message = '%s', how_many = '%s', timestamp = '%s' where host_id = '%s'\
                        " % (success_dict['msg'], how_many_rows, success_dict['time'], self.host_id)
                        cursor.execute(sql)
                        self.db.commit()
                        cursor.close()
                        self.db.close()
                    except Exception, e:
                        pass
                final_result_dict['result'] = success_dict['msg']
                final_result_dict['time'] = success_dict['time'].ctime()
            else:
                final_result_dict['result'] = str(err_dict)
            print how_many_rows
            print err_dict
            print success_dict
            print " done "
            return final_result_dict

# al = AlarmRecon(94)

# al.recon()


class recon_bll():
    """

    @param host_id:
    @param host_ip:
    """

    def __init__(self, host_id=None, host_ip=None):
        self.db = None
        self.host_id = host_id
        self.host_ip = host_ip

    def get_host_details(self):
        """


        @return: @raise:
        """
        success = 1
        result = {}
        try:
            if self.db:
                pass
            else:
                self.db = db_connect()

            if isinstance(self.db, MySQLdb.connection):
                sql = "SELECT h.ip_address, h.host_alias, h.host_id, hs.status, ar.message, ar.how_many, ar.timestamp FROM hosts AS h \
                        JOIN host_status AS hs ON hs.host_id = h.host_id \
                        JOIN alarm_recon AS ar ON ar.host_id = h.host_id \
                        WHERE h.host_id =  '%s' AND h.is_deleted =  '0'" % (self.host_id)
                cursor = self.db.cursor()
                cursor.execute(sql)
                res = cursor.fetchall()
                if len(res) > 0 and len(res[0]) > 6:
                    self.host_ip = res[0][0]
                    result = {'ip': res[0][0], 'alias': res[0][1], 'id': res[0][2], 'status': int(res[0][3]),
                              'msg': 'Never executed before' if len(res[0][4]) < 2 else res[0][4],
                              'how_many': 0 if res[0][5] == -1 else res[0][5],
                              'timestamp': 'Never executed before' if res[0][5] == -1 else res[0][6].ctime()}
                    success = 0
                else:
                    raise Exception(" Host details not found ")
            else:
                result = str(self.db)
        except Exception, e:
            result = str(e)
        finally:
            result_dict = {}
            result_dict['success'] = success
            if success == 0:
                result_dict['result'] = result
            else:
                result_dict['result'] = result
            return result_dict

    def get_host_status(self):
        """


        @raise:
        """
        success = 1
        result = {}
        try:
            if self.db:
                pass
            else:
                self.db = db_connect()

            if isinstance(self.db, MySQLdb.connection):
                sql = "SELECT h.ip_address, hs.status FROM hosts AS h \
                        JOIN host_status AS hs ON hs.host_id = h.host_id \
                        WHERE h.host_id =  '%s' AND h.is_deleted =  '0'" % (self.host_id)
                cursor = self.db.cursor()
                cursor.execute(sql)
                res = cursor.fetchall()
                if len(res) > 0 and len(res[0]) > 6:
                    self.host_ip = res[0][0]
                    result = {'ip': res[0][0], 'status': res[0][3]}
                    success = 0
                else:
                    raise Exception(" Host details not found ")
            else:
                result = str(self.db)
        except Exception, e:
            result = str(e)
        finally:
            if isinstance(self.db, MySQLdb.connection):
                if self.db.open:
                    self.db.close()
            result_dict = {}
            result_dict['success'] = success
            if success == 0:
                result_dict['result'] = result
            else:
                result_dict['result'] = result

    def get_all_info(self):
        """


        @return:
        """
        try:
            self.db = db_connect()
            final_result = {}
            success = 1
            host_result = self.get_host_details()
            if host_result['success'] == 0:
                final_result['ip'] = host_result['result'].get('ip', '')
                final_result['id'] = host_result['result'].get('id', '')
                final_result['alias'] = host_result['result'].get('alias', '')
                final_result['status'] = 0 if host_result['result'].get(
                    'status') == 0 else 1  # introduce a yello light
                final_result['status_msg'] = host_status_dict.get(int(host_result['result'].get(
                    'status') if isinstance(host_result['result'].get('status'), int) else 50), 'other operation')
                final_result['msg'] = host_result['result'].get('msg', '')
                final_result['timestamp'] = host_result[
                    'result'].get('timestamp', '')
                success = 0
            else:
                final_result = host_result['result']

            self.db.close()

        except Exception, e:
            final_result = str(e)
        finally:
            if isinstance(self.db, MySQLdb.connection):
                if self.db.open:
                    self.db.close()
            result_dict = {}
            result_dict['success'] = success
            if success == 0:
                result_dict['result'] = final_result
            else:
                result_dict['result'] = final_result
            return result_dict
