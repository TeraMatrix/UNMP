#!/usr/bin/python2.6

from datetime import datetime
import time

from sqlalchemy import and_, or_, desc, asc
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *

from common_bll import EventLog
from common_controller import *
from py_module import snmp_ping, pysnmp_geter, pysnmp_set1  # ,pysnmp_get_table
from pysnmp_ap import pysnmp_seter, pysnmp_get, odubulk as bulktable
from pysnmp_module import pysnmp_set  # , pysnmp_get_table_ap
from unmp_config import SystemConfig
from unmp_model import *

errorStatus = {0: 'noError',
               1: 'Configuration failed.Please try again later',
               2: 'noSuchName',
               3: 'badValue',
               4: 'readOnly',
               5: 'Device is busy.Please try again later',
               6: 'noAccess',
               7: 'wrongType',
               8: 'wrongLength',
               9: 'wrongEncoding',
               10: 'Wrong value entered',
               11: 'noCreation',
               12: 'inconsistentValue',
               13: 'resourceUnavailable',
               14: 'commitFailed',
               15: 'undoFailed',
               16: 'authorizationError',
               17: 'notWritable',
               18: 'inconsistentName',
               50: 'unKnown',
               551: 'networkUnreachable',
               52: 'typeError',
               553: 'Request Timeout.Please Wait and Retry Again',
               54: 'Configuration Failed.Please try again later',
               55: 'Configuration Failed.Please try again later',
               91: 'Arguments are not proper',
               96: 'InternalError',
               97: 'ip-port-community_not_passed',
               98: 'otherException',
               99: 'pysnmpException',
               102: 'Unkown Error Occured'}


class DeviceParameters(object):
    """
    Sqlalchemy interface to get the device related parameters
    based on host_id of the device
    """
    def get_device_parameter(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            device_list_param = []
            device_list_param = sqlalche_obj.session.query(
                Hosts.ip_address, Hosts.mac_address, Hosts.device_type_id, Hosts.config_profile_id).filter(
                Hosts.host_id == host_id).all()
            if device_list_param is None:
                device_list_param = []
            return device_list_param
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()


class IduDeviceList(object):
    """
    This function is used to get the list of IDU Devices based
    on IPaddress,Macaddress,DeviceTypes
    """
    def idu_device_list(self, ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search,
                        sEcho, sSortDir_0, iSortCol_0, userid=None, html_req={}):
        """
        Author- Anuj Samariya
        This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
        ip_address - This is the IP Address of device e.g 192.168.0.1
        mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
        selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
        return List of Devices in two dimensional list format
        @param ip_address:
        @param mac_address:
        @param selected_device:
        @param i_display_start:
        @param i_display_length:
        @param s_search:
        @param sEcho:
        @param sSortDir_0:
        @param iSortCol_0:
        @param userid:
        @param html_req:
        """

        # try block starts
        try:
            # here we create the session of sqlalchemy
            device_dict = data_table_data_sqlalchemy(
                ip_address, mac_address, selected_device, i_display_start, i_display_length,
                s_search, sEcho, sSortDir_0, iSortCol_0, userid, html_req)
            # this is the query which returns the multidimensional array of hosts table and store in device_list
            ##            device_list = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health).\
            ##            filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
            ##            Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(selected_device)),UsersGroups.user_id=='%s'%(userid),\
            ##            UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
            ##            .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
            ##
            ##            sqlalche_obj.sql_alchemy_db_connection_close()
            return device_dict
        # try block ends

        # exception starts
        except Exception as e:
            output2 = {
                "sEcho": 1,
                "iTotalRecords": 10,
                "iTotalDisplayRecords": 10,
                "aaData": [],
                "query": str(e)
            }
            return output2
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def idu_device_list_profiling(self, ip_address, mac_address, selected_device):
        """

        @param ip_address:
        @param mac_address:
        @param selected_device:
        @return:
        """
        global sqlalche_obj
        device_list = []
        device_type = selected_device
        device_list_state = "enabled"
        # try block starts
        try:
            # here we create the session of sqlalchemy
            sqlalche_obj.sql_alchemy_db_connection_open()
            # this is the query which returns the multidimensional array of
            # hosts table and store in device_tuple
            device_list = sqlalche_obj.session.query(
                Hosts.host_id, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address).filter(
                and_(Hosts.is_deleted == 0, Hosts.ip_address.like('%s%%' % (ip_address)),
                     Hosts.mac_address.like('%s%%' % (mac_address)), Hosts.device_type_id == device_type)).order_by(
                Hosts.host_alias).order_by(Hosts.ip_address).all()
            return device_list
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

# idu_device_list_bll_obj = IduDeviceList()
# print
# idu_device_list_bll_obj.idu_device_list_profiling('172.22.0.105','11:22:11:22:44:11','idu4')


class IduGetDatabase(object):
    """
    get IDU related data from SQL
    """
    def common_get_data_by_id(self, id_value, host_id, id_name, class_name):
        """

        @param id_value:
        @param host_id:
        @param id_name:
        @param class_name:
        @return:
        """
        try:
            global sqlalche_obj
            get_data = []
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_id == "" or host_id is None:
                return []
            config_id = sqlalche_obj.session.query(
                Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
            if len(config_id) > 0:
                query = "get_data = sqlalche_obj.session.query(%s).filter(and_(%s.%s=='%s',%s.config_profile_id=='%s')).all()" % (
                class_name, class_name,
                id_name, id_value, class_name, config_id[0].config_profile_id)
                exec "get_data = sqlalche_obj.session.query(%s).filter(and_(%s.%s=='%s',%s.config_profile_id=='%s')).all()" % (
                class_name, class_name,
                id_name, id_value, class_name, config_id[0].config_profile_id)
                if len(get_data) > 0:
                    return get_data
                else:
                    return query
            else:
                return []
        except Exception as e:
            return 0
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

# idu_get_database_obj = IduGetDatabase()
# print idu_get_database_obj.common_get_data_by_id('301','67','idu_portBwTable_id','IduPortBwTable')
############################################### Reconciliation ###########


def rename_tablename(tablename):
    """

    @param tablename:
    @return:
    """
    try:
        ss = ""
        idx = tablename.index("_")
        ss = tablename[0:idx] + tablename[idx + 1].upper() + \
             tablename[
             idx + 1 + 1:]
        ss = ss[0].upper() + ss[1:]
        return ss
    except Exception as e:
        return e


class IduReconcilation(object):
    """
    Device IDU reconciliation
    """
    def default_reconciliation_controller(self, host_id, device_type_id, table_prefix, insert_update):
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param insert_update:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        new_profile = Odu16ConfigProfiles(
            device_type_id, "IduProfile", "Master",
            None, datetime.now(), None, datetime.now(), None, 0)
        sqlalche_obj.session.add(new_profile)
        sqlalche_obj.session.flush()
        sqlalche_obj.session.refresh(new_profile)
        new_profile_id = new_profile.config_profile_id
        default_profile_id = sqlalche_obj.session.query(Odu16ConfigProfiles.config_profile_id) \
            .filter(and_(Odu16ConfigProfiles.device_type_id == device_type_id,
                         Odu16ConfigProfiles.config_profile_type_id == "default")).all()
        default_id = default_profile_id[0].config_profile_id
        idu_poe_data = sqlalche_obj.session.query(IduPoeConfigurationTable).filter(
            IduPoeConfigurationTable.config_profile_id == default_id).all()
        if len(idu_poe_data) > 0:
            for i in range(0, len(idu_poe_data)):
                idu_poe_data_add = IduPoeConfigurationTable(
                    new_profile_id, idu_poe_data[i].indexId, idu_poe_data[i].poeAdminStatus)
                sqlalche_obj.session.add(idu_poe_data_add)

        idu_e1_port_data = sqlalche_obj.session.query(IduE1PortConfigurationTable).filter(
            IduE1PortConfigurationTable.config_profile_id == default_id).all()
        if len(idu_e1_port_data) > 0:
            for i in range(0, len(idu_e1_port_data)):
                idu_e1_port_data_add = IduE1PortConfigurationTable(new_profile_id, idu_e1_port_data[i].portNumber,
                                                                   idu_e1_port_data[i].adminState, idu_e1_port_data[
                        i].clockSource, idu_e1_port_data[i].lineType, idu_e1_port_data[i].lineCode)
                sqlalche_obj.session.add(idu_e1_port_data_add)

        idu_switch_port_data = sqlalche_obj.session.query(IduSwitchPortconfigTable).filter(
            IduSwitchPortconfigTable.config_profile_id == default_id).all()
        if len(idu_switch_port_data) > 0:
            for i in range(0, len(idu_switch_port_data)):
                idu_swtch_port_data_add = IduSwitchPortconfigTable(
                    new_profile_id, idu_switch_port_data[
                        i].switchportNum, idu_switch_port_data[i].swadminState,
                    idu_switch_port_data[
                        i].swlinkMode, idu_switch_port_data[
                        i].portvid, idu_switch_port_data[i].macauthState,
                    idu_switch_port_data[i].mirroringdirection, idu_switch_port_data[i].portdotqmode,
                    idu_switch_port_data[i].macflowcontrol)
                sqlalche_obj.session.add(idu_swtch_port_data_add)

        idu_temperature_data = sqlalche_obj.session.query(IduTemperatureSensorConfigurationTable).filter(
            IduTemperatureSensorConfigurationTable.config_profile_id == default_id).all()
        if len(idu_temperature_data) > 0:
            for i in range(0, len(idu_temperature_data)):
                idu_temperature_data_add = IduTemperatureSensorConfigurationTable(new_profile_id,
                                                                                  idu_temperature_data[i].tempIndex,
                                                                                  idu_temperature_data[i].tempMax,
                                                                                  idu_temperature_data[i].tempMin)
                sqlalche_obj.session.add(idu_temperature_data_add)

        idu_mirroring_data = sqlalche_obj.session.query(IduMirroringportTable).filter(
            IduMirroringportTable.config_profile_id == default_id).all()
        if len(idu_mirroring_data) > 0:
            for i in range(0, len(idu_mirroring_data)):
                idu_mirroring_data_add = IduMirroringportTable(
                    new_profile_id, idu_mirroring_data[i].mirroringindexid, idu_mirroring_data[i].mirroringport)
                sqlalche_obj.session.add(idu_mirroring_data_add)

        idu_qinq_data = sqlalche_obj.session.query(IduPortqinqTable).filter(
            IduPortqinqTable.config_profile_id == default_id).all()
        if len(idu_qinq_data) > 0:
            for i in range(0, len(idu_qinq_data)):
                idu_qinq_data_add = IduPortqinqTable(
                    new_profile_id, idu_qinq_data[i].switchportnumber, idu_qinq_data[i].portqinqstate,
                    idu_qinq_data[i].providertag)
                sqlalche_obj.session.add(idu_qinq_data_add)

        idu_bandwidth_data = sqlalche_obj.session.query(IduPortBwTable).filter(
            IduPortBwTable.config_profile_id == default_id).all()
        if len(idu_bandwidth_data) > 0:
            for i in range(0, len(idu_bandwidth_data)):
                idu_bandwidth_data_add = IduPortBwTable(
                    new_profile_id, idu_bandwidth_data[i].switchportnum, idu_bandwidth_data[i].egressbwvalue,
                    idu_bandwidth_data[i].ingressbwvalue)
                sqlalche_obj.session.add(idu_bandwidth_data_add)

        idu_rtc_data = sqlalche_obj.session.query(IduRtcConfigurationTable).filter(
            IduRtcConfigurationTable.config_profile_id == default_id).all()
        if len(idu_rtc_data) > 0:
            for i in range(0, len(idu_rtc_data)):
                idu_rtc_data_add = IduRtcConfigurationTable(
                    new_profile_id, idu_rtc_data[
                        i].rtcIndex, idu_rtc_data[
                        i].year, idu_rtc_data[i].month,
                    idu_rtc_data[
                        i].day, idu_rtc_data[i].hour,
                    idu_rtc_data[i].min, idu_rtc_data[i].sec)
                sqlalche_obj.session.add(idu_rtc_data_add)

        idu_omc_data = sqlalche_obj.session.query(IduOmcConfigurationTable).filter(
            IduOmcConfigurationTable.config_profile_id == default_id).all()
        if len(idu_omc_data) > 0:
            for i in range(0, len(idu_omc_data)):
                idu_omc_data_add = IduOmcConfigurationTable(
                    new_profile_id, idu_omc_data[i].omcIndex, idu_omc_data[i].omcIpAddress,
                    idu_omc_data[i].periodicStatsTimer)
                sqlalche_obj.session.add(idu_omc_data_add)

        idu_admin_data = sqlalche_obj.session.query(IduIduAdminStateTable).filter(
            IduIduAdminStateTable.config_profile_id == default_id).all()
        if len(idu_admin_data) > 0:
            for i in range(0, len(idu_admin_data)):
                idu_admin_data_add = IduIduAdminStateTable(
                    new_profile_id, idu_admin_data[i].stateId, idu_admin_data[i].adminstate)
                sqlalche_obj.session.add(idu_admin_data_add)

        idu_swstatus_data_add = IduSwStatusTable(host_id, None, None,
                                                 None, None, datetime.now())
        sqlalche_obj.session.add(idu_swstatus_data_add)

        idu_info_data_add = IduIduInfoTable(
            host_id, 1, None, None, None, None, None, None, None, None, None, datetime.now())
        sqlalche_obj.session.add(idu_info_data_add)

        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(new_profile_id), 0

    def update_device_reconcilation_controller(self, host_id, device_type_id, table_prefix, insert_update, user_name):
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param insert_update:
        @param user_name:
        @return:
        """
        try:
            global sqlalche_obj, errorStatus
            i = 0
            flag = 0
            tables_not_fill = []
            fill_not_table = []
            sqlalche_obj.sql_alchemy_db_connection_open()
            table_name = ""
            result = {}
            getvalue = {}
            rec = 1
            total_per = 21
            reconcile_per = 0
            config_profile_id = ""
            timestamp = 0
            host_data = []
            tablename = ""
            config_type = 0
            timestamp = 0
            primary_key_id = ""
            data_flag = 0
            link = ""
            time_stamp = str(datetime.now())
            obj_system_config = SystemConfig()
            if host_id == "" or host_id == None:
                result = {"success": 1, "result": "Host Not Exist"}
            else:
                try:

                    device_param_list = sqlalche_obj.session.query(Hosts). \
                        filter(Hosts.host_id == host_id).all()
                except:
                    return {"succes": 1, "result": "No host Exist"}
                if len(device_param_list) == 0:
                    if device_param_list[0].config_profile_id == None or device_param_list[0].config_profile_id == "":
                        result = {"success": 1,
                                  "result": "Configuration Not Exist For This Host"}
                        return result
                    else:
                        result = {"success": 1, "result": "Host Not Exist"}
                        return result
                else:
                    device_param_list[0].reconcile_status = 1
                    sqlalche_obj.session.commit()
                    tables_not_fill = sqlalche_obj.session.query(NmsGraphs.tablename).filter(
                        NmsGraphs.device_type_id == device_type_id).all()

                    if len(tables_not_fill) > 0:
                        for i in range(0, len(tables_not_fill)):
                            fill_not_table.append(tables_not_fill[i][0])

                    query_result = sqlalche_obj.session.query(
                        IduOidTable.table_name, IduOidTable.table_oid).distinct().filter(
                        not_(IduOidTable.table_name.in_((fill_not_table)))).all()
                    var_bind = sqlalche_obj.session.query(IduOidTable.table_name, IduOidTable.varbinds).distinct(
                    ).filter(not_(IduOidTable.table_name.in_((fill_not_table)))).all()
                    if snmp_ping(device_param_list[0].ip_address, device_param_list[0].snmp_read_community,
                                 int(device_param_list[0].snmp_port)) == 0:
                        if len(query_result) > 0:
                            oid_table_dict = {}
                            result = {}
                            oid_table_dict = dict(query_result)
                            var_bind_dic = dict(var_bind)
                            for i in oid_table_dict:
                                time.sleep(2)
                                if i == "aclportTable":
                                    continue
                                column_list = []
                                tablename = table_prefix + i
                                database_name = obj_system_config.get_sqlalchemy_credentials(
                                )
                                result_db = sqlalche_obj.db.execute(
                                    "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'" % (
                                    tablename, database_name[4]))
                                for row in result_db:
                                    column_list.append(row["column_name"])
                                    # if i=="linkConfigurationTable":
                                    #     result = bulktable(str(oid_table_dict[i])+".1",device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_read_community)
                                    #     print result,"%%%%%%%%%%%%%%%%%%%%%%%%%%%"
                                    # else:
                                time.sleep(1)
                                result = bulktable(str(oid_table_dict[i]) + ".1", device_param_list[0].ip_address, int(
                                    device_param_list[0].snmp_port), device_param_list[0].snmp_read_community,
                                                   var_bind_dic[i])
                                sql_table_name = rename_tablename(tablename)

                                if result["success"] == 1:
                                    if int(rec) > 0:
                                        rec = rec - 1
                                elif result["success"] == 0 and result["result"] == {}:
                                    rec = rec + 1
                                    exec "sqlalche_obj.session.query(%s).filter(%s.config_profile_id == %s).delete()" % (
                                        sql_table_name, sql_table_name, device_param_list[0].config_profile_id)
                                else:
                                    if i == "linkConfigurationTable" or i == "vlanconfigTable":
                                        exec "sqlalche_obj.session.query(%s).filter(%s.config_profile_id == %s).delete()" % (
                                            sql_table_name, sql_table_name, device_param_list[0].config_profile_id)
                                        sqlalche_obj.session.commit()
                                    rec = rec + 1
                                    if "config_profile_id" in column_list:
                                        exec "sqlalche_table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id==%s).all()" % (
                                            sql_table_name, sql_table_name, device_param_list[0].config_profile_id)
                                    else:
                                        exec "sqlalche_table_result = sqlalche_obj.session.query(%s).filter(%s.host_id==%s).all()" % (
                                            sql_table_name, sql_table_name, host_id)

                                    m = 0
                                    primary_key_id = tablename + "_id"
                                    column_list.remove(primary_key_id)
                                    if "config_profile_id" in column_list:
                                        column_list.remove("config_profile_id")
                                        config_type = 1
                                    else:
                                        column_list.remove("host_id")
                                        config_type = 0
                                    if "timestamp" in column_list:
                                        column_list.remove("timestamp")
                                        timestamp = 1
                                    else:
                                        timestamp = 0
                                    if len(sqlalche_table_result) > 0:
                                        for row in result['result']:
                                            for val in range(0, len(result['result'][row])):
                                                setattr(sqlalche_table_result[row -
                                                                              1], column_list[val],
                                                        str(result['result'][row][val]))
                                                if timestamp == 1:
                                                    setattr(sqlalche_table_result[
                                                                row - 1], "timestamp",
                                                            time_stamp[:time_stamp.find('.') - 1])
                                    else:
                                        for row in result['result']:
                                            if config_type == 1:
                                                sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" % (
                                                    tablename, device_param_list[0].config_profile_id,
                                                    str(result["result"][row])[1:-1]))
                                            else:
                                                if timestamp == 0:
                                                    sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" %
                                                                            (tablename, host_id,
                                                                             str(result["result"][row])[1:-1]))
                                                else:
                                                    sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s,'%s')" % (
                                                        tablename, host_id, str(result["result"][row])[1:-1],
                                                        time_stamp[:time_stamp.find('.') - 1]))
                                                    # if len(sqlalche_table_result)>0:
                                                    #     if i=="linkConfigurationTable":
                                                    #         if config_type == 1:
                                                    #             for i in result["result"]:
                                                    #                 for k in range(0,len(column_list)):
                                                    #                     exec "sqlalche_table_result[%s].%s = '%s'"%(i-1,column_list[k],str(result["result"][i][k]))
                                                    #     else:
                                                    #         for i in result["result"]:
                                                    #             for j in range(0,len(result["result"][i])):
                                                    #                 if config_type == 1:
                                                    #                     for k in range(0,len(column_list)):
                                                    #                         if k == 0:
                                                    #                             exec "sqlalche_table_result[m].%s='%s'"%(column_list[k],i)
                                                    #                         else:
                                                    #                             exec "sqlalche_table_result[%s].%s='%s'"%(m,column_list[k],result["result"][i][k-1])
                                                    #                         if timestamp == 1:
                                                    #                             exec "sqlalche_table_result[%s].timestamp='%s'"%(m,datetime.now())

                                                    #                 else:
                                                    #                     for k in range(0,len(column_list)):
                                                    #                         if k == 0:
                                                    #                             exec "sqlalche_table_result[m].%s='%s'"%(column_list[k],i)
                                                    #                         else:
                                                    #                             exec "sqlalche_table_result[%s].%s='%s'"%(m,column_list[k],result["result"][i][k-1])
                                                    #                         if timestamp == 1:
                                                    #                             exec "sqlalche_table_result[%s].timestamp='%s'"%(m,datetime.now())
                                                    #                 sqlalche_obj.session.commit()
                                                    #             m = m+1
                                                    # else:
                                                    #     if i=="linkConfigurationTable":
                                                    #         for i in range(0,len(result["result"])):
                                                    #             if config_type == 1:
                                                    #                 sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%(tablename,device_param_list[0].config_profile_id,str(result["result"][i+1])[1:-1]))
                                                    #             else:
                                                    #                 sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%(tablename,host_id,str(result["result"][i+1])[1:-1]))
                                                    #     else:
                                                    #         for i in result["result"]:
                                                    #             result["result"][i].insert(0,str(i))
                                                    #             if config_type ==1:
                                                    #                 sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)"%(tablename,device_param_list[0].config_profile_id,str(result["result"][i])[1:-1]))
                                                    #             else:
                                                    #                 if timestamp == 0:
                                                    #                     sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)"%(tablename,host_id,str(result["result"][i])[1:-1]))
                                                    #                 else:
                                                # sqlalche_obj.db.execute("Insert into %s
                                                # values(NULL,%s,%s,'%s')"%(tablename,host_id,str(result["result"][i])[1:-1],datetime.now()))

                            reconcile_per = (float(rec) / float(total_per))
                            reconcile_per = int(reconcile_per * 100)

                            device_param_list[
                                0].reconcile_health = reconcile_per
                            device_param_list[0].reconcile_status = 2
                            sqlalche_obj.session.commit()
                            device_param_list[0].reconcile_status = 0
                            el = EventLog()
                            el.log_event(
                                "Device Reconcilation Done", "%s" % (user_name))
                            sqlalche_obj.session.commit()
                            result = {"success": 0, "result": {reconcile_per: [
                                device_param_list[0].host_name, device_param_list[0].ip_address]}}
                            return result
                        else:
                            result = {"success": 1, "result":
                                "UNMP has shut down.Please contact UNMP vendor"}
                            device_param_list[0].reconcile_status = 0
                            sqlalche_obj.session.commit()
                            return result
                    else:
                        result = {"success": 1, "result": "%s(%s) Device may not be connected or may be Rebooting" % (
                            device_param_list[0].host_name, device_param_list[0].ip_address)}
                        device_param_list[0].reconcile_health = 0
                        device_param_list[0].reconcile_status = 0
                        sqlalche_obj.session.commit()
                        return result

        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occured", "detail": str(e)}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occured", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occured", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occured", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occured", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occured", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occured,Contact Your Administrator", "detail": ""}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occured", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    ####################### Device Reconciliation with isReconciliation reconc
    def new_device_reconcilation_controller(self, host_id, device_type_id, table_prefix, reconcile_chk=True,
                                            user_name=""):
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param reconcile_chk:
        @param user_name:
        @return:
        """
        try:
            global sqlalche_obj, errorStatus
            i = 0
            flag = 0
            tables_not_fill = []
            fill_not_table = []
            sqlalche_obj.sql_alchemy_db_connection_open()
            table_name = ""
            result = {}
            getvalue = {}
            rec = 1
            total_per = 21
            reconcile_per = 0
            config_profile_id = ""
            time_stamp = str(datetime.now())
            host_data = []
            if host_id == "" or host_id == None:
                result = {"success": 1, "result": "Host Not Exist"}
            else:
                if reconcile_chk == True:
                    try:
                        device_param_list = sqlalche_obj.session.query(Hosts). \
                            filter(Hosts.host_id == host_id).all()
                    except:
                        return {"succes": 1, "result": "No host Exist"}
                    if snmp_ping(device_param_list[0].ip_address, device_param_list[0].snmp_read_community,
                                 int(device_param_list[0].snmp_port)) == 0:
                        if len(device_param_list) == 0:
                            if device_param_list[0].config_profile_id == None or device_param_list[
                                0].config_profile_id == "":
                                result = {"success": 1,
                                          "result": "Configuration Not Exist For This Host"}
                                return result
                            else:
                                result = {
                                    "success": 1, "result": "Host Not Exist"}
                                return result
                        else:
                            device_param_list[0].reconcile_status = 1
                            sqlalche_obj.session.commit()
                            tables_not_fill = sqlalche_obj.session.query(NmsGraphs.tablename).filter(
                                NmsGraphs.device_type_id == device_type_id).all()
                            if len(tables_not_fill) > 0:
                                for i in range(0, len(tables_not_fill)):
                                    fill_not_table.append(
                                        tables_not_fill[i][0])

                            query_result = sqlalche_obj.session.query(
                                IduOidTable.table_name, IduOidTable.table_oid).distinct().filter(
                                not_(IduOidTable.table_name.in_((fill_not_table)))).all()
                            var_bind = sqlalche_obj.session.query(IduOidTable.table_name,
                                                                  IduOidTable.varbinds).distinct(
                            ).filter(not_(IduOidTable.table_name.in_((fill_not_table)))).all()
                            if len(query_result) > 0:
                                profile_id = Odu16ConfigProfiles(
                                    device_type_id, None, 'Master', None, datetime.now(), None, datetime.now(), None, 0)
                                sqlalche_obj.session.add(profile_id)
                                sqlalche_obj.session.flush()
                                config_profile_id = profile_id.config_profile_id
                                sqlalche_obj.session.commit()
                                oid_table_dict = {}
                                result = {}
                                oid_table_dict = dict(query_result)
                                var_bind_dic = dict(var_bind)
                                for i in oid_table_dict:
                                    if i == "aclportTable":
                                        continue
                                    column_list = []
                                    tablename = table_prefix + i
                                    result_db = sqlalche_obj.db.execute(
                                        "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s'" % (
                                        tablename))
                                    for row in result_db:
                                        column_list.append(row['column_name'])
                                    ##                                    if i=="linkConfigurationTable":
                                    ##                                        result = pysnmp_get_table_ap(oid_table_dict[i],device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_read_community)
                                    ##                                    else:
                                    # result =
                                    # pysnmp_get_table(oid_table_dict[i],device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_read_community)
                                    time.sleep(2)
                                    result = bulktable(str(oid_table_dict[i]) + ".1", device_param_list[0].ip_address,
                                                       int(
                                                           device_param_list[0].snmp_port),
                                                       device_param_list[0].snmp_read_community, var_bind_dic[i])
                                    if result["success"] == 1:
                                        if int(rec) > 0:
                                            rec = rec - 1
                                    elif result["success"] == 0 and result["result"] == {}:
                                        rec = rec + 1
                                    else:
                                        rec = rec + 1

                                    for row in result['result']:
                                        if "config_profile_id" in column_list:
                                            print "Insert into %s values(NULL,%s,%s)" % (
                                            tablename, config_profile_id, str(result["result"][row])[1:-1])
                                            sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" %
                                                                    (tablename, config_profile_id,
                                                                     str(result["result"][row])[1:-1]))
                                        else:
                                            if "timestamp" not in column_list:
                                                sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" %
                                                                        (tablename, host_id,
                                                                         str(result["result"][row])[1:-1]))
                                            else:
                                                sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s,'%s')" %
                                                                        (tablename, host_id,
                                                                         str(result["result"][row])[1:-1],
                                                                         time_stamp[:time_stamp.find('.') - 1]))
                                            ##                                        if i=="linkConfigurationTable":
                                            ##                                            for i in range(0,len(result["result"])):
                                            ##                                                if "config_profile_id" in column_list :
                                            ##                                                    sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%(tablename,config_profile_id,str(result["result"][i+1])[1:-1]))
                                            ##                                                else:
                                            ##                                                    sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%(tablename,host_id,str(result["result"][i+1])[1:-1]))
                                            ##                                        else:
                                            ##                                            for j in result["result"]:
                                            ##                                                result_db  = sqlalche_obj.db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s'"%(tablename))
                                            ##                                                for row in result_db:
                                            ##                                                    column_list.append(row['column_name'])
                                            ##                                                if "config_profile_id" in column_list :
                                            ##                                                    if "timestamp" in column_list:
                                            ##                                                        sqlalche_obj.db.execute("insert into %s values(NULL,%s,%s,%s,'%s')"%(tablename,config_profile_id,j,str(result["result"][j])[1:-1],datetime.now()))
                                            ##                                                    else:
                                            ##                                                        sqlalche_obj.db.execute("insert into %s values(NULL,%s,%s,%s)"%(tablename,config_profile_id,j,str(result["result"][j])[1:-1]))
                                            ##                                                else:
                                            ##                                                    if "timestamp" in column_list:
                                            ##                                                        sqlalche_obj.db.execute("insert into %s values(NULL,%s,%s,%s,'%s')"%(tablename,host_id,j,str(result["result"][j])[1:-1],datetime.now()))
                                            ##                                                    else:
                                            # sqlalche_obj.db.execute("insert into %s
                                            # values(NULL,%s,%s,%s)"%(tablename,host_id,j,str(result["result"][j])[1:-1]))

                                reconcile_per = (float(rec) / float(total_per))
                                reconcile_per = int(reconcile_per * 100)
                                device_param_list[
                                    0].reconcile_health = reconcile_per
                                device_param_list[0].reconcile_status = 2
                                sqlalche_obj.session.commit()
                                device_param_list[0].reconcile_status = 0
                                el = EventLog()
                                el.log_event(
                                    "Device Reconcilation Done", "%s" % (user_name))
                                sqlalche_obj.session.commit()
                                return str(config_profile_id), reconcile_per
                            else:
                                result = {"success": 1, "result":
                                    "UNMP has shut down.Please contact UNMP vendor"}
                                device_param_list[0].reconcile_status = 1
                                sqlalche_obj.session.commit()
                                return result
                    else:
                        device_param_list[0].reconcile_status = 0
                        sqlalche_obj.session.commit()
                        config_profile_id, reconcile_per = self.default_reconciliation_controller(
                            host_id, device_type_id, table_prefix, reconcile_chk)
                        return str(config_profile_id), reconcile_per
                else:
                    config_profile_id, reconcile_per = self.default_reconciliation_controller(
                        host_id, device_type_id, table_prefix, reconcile_chk)
                    return str(config_profile_id), reconcile_per
        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occured", "detail": str(e)}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occured", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occured", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occured", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occured", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occured", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occured,Contact Your Administrator", "detail": str(e)}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occured", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def reconciliation_status(self):
        """


        @return:
        """
        global sqlalche_obj
        result = {}
        rec_dir = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        rec_list = sqlalche_obj.session.query(
            Hosts.host_id, Hosts.reconcile_status, Hosts.reconcile_health).filter(
            and_(Hosts.device_type_id.like("idu4%"))).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(rec_list) > 0:
            for i in range(0, len(rec_list)):
                rec_dir[str(rec_list[i][0])] = [rec_list[i][1], rec_list[i][2]]
            result = {"result": rec_dir, "success": 0}
            return result

    def commit_to_flash(self, host_id, device_type_id):
        """

        @param host_id:
        @param device_type_id:
        @return:
        """
        global sqlalche_obj
        result = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        oid_dict = {}
        oid_dict[1] = ['1.3.6.1.4.1.26149.2.1.5.1.1.2.1', 'Integer32', 4]
        host_param = sqlalche_obj.session.query(
            Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community).filter(Hosts.host_id == host_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(host_param) > 0:
            result = pysnmp_set1(host_param[0].ip_address, int(
                host_param[0].snmp_port), host_param[0].snmp_write_community, oid_dict[1])
            return result
        else:
            return {"success": 1, "result": "Host Data Not Exist"}

    def reboot(self, host_id, device_type_id):
        """

        @param host_id:
        @param device_type_id:
        @return:
        """
        global sqlalche_obj
        result = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        oid_dict = {}
        oid_dict[1] = ['1.3.6.1.4.1.26149.2.1.5.1.1.2.1', 'Integer32', 5]
        host_param = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(host_param) > 0:
            snmp_get_result = pysnmp_get('1.3.6.1.4.1.26149.2.1.5.1.1.7', host_param[0].ip_address, int(host_param[0]
            .snmp_port), host_param[0].snmp_read_community)
            if snmp_get_result['success'] == 0:
                if int(snmp_get_result['result'].values()[0]) == 1:
                    snmp_get_om_operation = pysnmp_get('1.3.6.1.4.1.26149.2.1.5.1.1.2', host_param[0].ip_address, int(
                        host_param[0].snmp_port), host_param[0].snmp_read_community)
                    if snmp_get_om_operation['success'] == 0:
                        if int(snmp_get_om_operation['result'].values()[0]) == 1:
                            msg = "Software download operation is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 2:
                            msg = "Software  Activation is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 3:
                            msg = "Factory reset is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 4:
                            msg = "Commit to Flash is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 6:
                            msg = "Another Site Survey is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 7:
                            msg = "Bandwidth calculator is running.Please wait to complete that operation..."
                        else:
                            msg = "Some other operation is running.Please wait to complete that operation..."
                        result = {"success": 1, "result": msg, "flag": "1"}
                        return result
                    else:
                        if 53 in snmp_get_om_operation["result"]:
                            result = {"success": 1, "result":
                                "No Response From Device.Please Try Again", "flag": "1"}
                        elif 51 in snmp_get_om_operation["result"]:
                            result = {"success": 1,
                                      "result": "Network is unreachable", "flag": "1"}
                        elif 99 in snmp_get_om_operation["result"]:
                            result = {"success": 1, "result":
                                "UNMP Server is busy.Please Retry again", "flag": "1"}
                        else:
                            return snmp_get_om_operation
                        return result
                else:
                    result = pysnmp_set1(host_param[0].ip_address, int(
                        host_param[0].snmp_port), host_param[0].snmp_write_community, oid_dict[1])
                    time.sleep(5)
                    result['flag'] = 0
                    return result
            else:
                if 53 in snmp_get_result["result"]:
                    result = {"success": 1, "result":
                        "No Response From Device.Please Try Again", "flag": "1"}
                elif 51 in snmp_get_result["result"]:
                    result = {"success": 1, "result":
                        "Network is unreachable", "flag": "1"}
                elif 99 in snmp_get_result["result"]:
                    result = {"success": 1, "result":
                        "UNMP Server is busy.Please Retry again", "flag": "1"}
                else:
                    return snmp_get_result
                return result
        else:
            return {"success": 1, "result": "Host Data Not Exist"}

    def chk_ping(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        if host_id != "" or host_id != None:
            device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_read_community,
                                                           Hosts.config_profile_id). \
                filter(Hosts.host_id == host_id).one()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if snmp_ping(device_param_list[0], device_param_list[2], int(device_param_list[1])) == 0:
            return 0
        else:
            return 1

# obj = IduReconcilation()
# print obj.reboot(4,'idu4')
# print obj.default_reconciliation_controller(111,'idu4','idu_',True)


class IduGetData(object):
    """
    IDU device data fetch
    """
    def common_get_data(self, class_name, host_id, config=True):
        """

        @param class_name:
        @param host_id:
        @param config:
        @return:
        """
        try:
            global sqlalche_obj
            get_data = []
            sqlalche_obj.sql_alchemy_db_connection_open()
            exec_string = ''
            if host_id == "" or host_id == None:
                return []
            if config:
                config_id = sqlalche_obj.session.query(
                    Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
                if len(config_id) <= 0:
                    return []
                exec_string = "get_data = sqlalche_obj.session.query(%s).filter(%s.config_profile_id==%s).all()" % (
                    class_name, class_name, config_id[0].config_profile_id)
            else:
                exec_string = "get_data = sqlalche_obj.session.query(%s).filter(%s.host_id==%s).all()" % (
                    class_name, class_name, host_id)

            exec exec_string

            if len(get_data) > 0:
                return get_data
            else:
                return []
        except Exception as e:
            # sqlalche_obj.sql_alchemy_db_connection_close()
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def convert_time(self, value):
        """

        @param value:
        @return:
        """
        from datetime import datetime, timedelta

        try:
            sec = timedelta(seconds=int(int(value) / 100))
            d = datetime(1, 1, 1) + sec
            return "%d:%d:%d:%d" % (d.day - 1, d.hour, d.minute, d.second)
        except:
            return "0:0:0:0"

    def common_get_multivalue(self, device_type, oid_name, field_value):
        """

        @param device_type:
        @param oid_name:
        @param field_value:
        @return:
        """
        try:
            global sqlalche_obj
            get_data = []
            sqlalche_obj.sql_alchemy_db_connection_open()

            val_dict = {'device_type': device_type, 'oid_name':
                oid_name, 'field_value': field_value}

            get_data = sqlalche_obj.db.execute("SELECT %(device_type)s_oids_multivalues.value FROM  %(device_type)s_oids_multivalues join \
            %(device_type)s_oids on \
             %(device_type)s_oids.oid_id = %(device_type)s_oids_multivalues.oid_id and \
              %(device_type)s_oids.oid_name =  '%(oid_name)s' AND  %(device_type)s_oids_multivalues.name =  '%(field_value)s'" % (
            val_dict))

            for i in get_data:
                return str(i[0])

        except Exception as e:
            import traceback

            return traceback.format_exc()
            return ''
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def common_get_data_by_host(self, class_name, host_id):
        """

        @param class_name:
        @param host_id:
        @return:
        """
        try:
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_id == "" or host_id == None:
                return []

            exec "get_data = sqlalche_obj.session.query(%s).filter(%s.host_id==%s).all()" % (
                class_name, class_name, host_id)
            if len(get_data) > 0:
                return get_data
            else:
                return []
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def get_e1_op_status(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_id == "" or host_id == None:
                return []
            get_data = sqlalche_obj.session.query(IduE1PortStatusTable).filter(
                IduE1PortStatusTable.host_id == host_id).order_by(desc(IduE1PortStatusTable.timestamp)).order_by(
                asc(IduE1PortStatusTable.portNum)).limit(4).all()
            if len(get_data) > 0:
                return get_data
            else:
                return []
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()


# obj = IduGetData()
# print obj.common_get_data('Odu100RuConfTable',28)
# print obj.common_get_data_by_host("Odu100RaSiteSurveyResultTable",63)
class IduCommonSetValidation(object):
    """
    IDU device related validation fucntion
    """
    def common_set_config(self, host_id, device_type_id, dic_result, id=None, index=0, special_case=0):
    # dic_result = {'success':0,'result':{'ru.omcConfTable.omcIpAddress':[1,'Not Done'],'ru.omcConfTable.periodicStatsTimer':[1,'Not Done']}}
    # return dic_result
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param id:
        @param index:
        @param special_case:
        @return:
        """
        try:
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            success_result = {"success": '', "result": {}}
            global errorStatus
            o1 = aliased(IduOids)
            table_name = "IduOids"
            o2 = aliased(IduOids)
            rowSts = {'ru.ra.raAclConfigTable.rowSts': [
                '1.3.6.1.4.1.26149.2.2.13.5.1.3', 'Integer32', '']}
            query_result = []
            oid_admin_state = {"1": -1}
            independent_oid = []
            dependent_oid = []
            depend_oid_value = []
            result = {}
            key = ""
            exist_data = 0
            for keys in dic_result.iterkeys():
                if keys == "success":
                    continue
                else:
                    query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                        o1, o1.oid_id == o2.dependent_id).filter(
                        and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()
                    if len(query_result) > 0:
                        if query_result[0][0].dependent_id == "" or query_result[0][0].dependent_id == None:
                            independent_oid.append({keys: [query_result[0][0].oid + query_result[0][
                                0].indexes, query_result[0][0].oid_type, dic_result[keys]]})

                        else:
                            if len(dependent_oid) > 0:
                                for i in range(0, len(dependent_oid)):
                                    if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                        admin_state = 'ru.ruConfTable.adminstate'
                                    elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                        admin_state = 'ru.ipConfigTable.adminState-1'
                                    elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                        admin_state = 'ru.ra.raConfTable.raAdminState-1'
                                    else:
                                        admin_state = query_result[0][1]
                                    if admin_state in dependent_oid[i]:

                                        pos = i
                                        if len(depend_oid_value) > 0:
                                            depend_oid_value[pos][keys] = [
                                                query_result[0][0].oid + "." + str(id), query_result[0][0].oid_type,
                                                dic_result[keys]]
                                            break
                                        else:

                                            depend_oid_value.append(
                                                {keys: [query_result[0][0].oid + + "." + str(id),
                                                        query_result[0][0].oid_type, dic_result[keys]]})
                                            break
                                    else:

                                        if i == len(dependent_oid) - 1:
                                            if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                                dependent_oid.append({query_result[0][1] + str(
                                                    -1): [query_result[0][2] + query_result[0][3]]})
                                                depend_oid_value.append(
                                                    {keys: [query_result[0][0].oid + query_result[0][0]
                                                    .indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                            elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                                dependent_oid.append({query_result[0][1] + str(
                                                    -1): [query_result[0][2] + query_result[0][3]]})
                                                depend_oid_value.append(
                                                    {keys: [query_result[0][0].oid + query_result[0][0]
                                                    .indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                            elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                                dependent_oid.append({query_result[0][1] + str(
                                                    -1): [query_result[0][2] + query_result[0][3]]})
                                                depend_oid_value.append(
                                                    {keys: [query_result[0][0].oid + query_result[0][0]
                                                    .indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                            else:
                                                dependent_oid.append(
                                                    {query_result[0][1]: [query_result[0][2] + query_result[0][3]]})
                                                depend_oid_value.append({keys: [query_result[0][0].oid + "." + str(
                                                    id), query_result[0][0].oid_type, dic_result[keys]]})
                                        else:
                                            continue

                            else:
                                if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                    dependent_oid.append({query_result[0][1] + str(
                                        -1): [query_result[0][2] + query_result[0][3]]})
                                    depend_oid_value.append({keys: [query_result[0][0].oid +
                                                                    query_result[0][0].indexes,
                                                                    query_result[0][0].oid_type, dic_result[keys]]})
                                elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                    dependent_oid.append({query_result[0][1] + str(
                                        -1): [query_result[0][2] + query_result[0][3]]})
                                    depend_oid_value.append({keys: [query_result[0][0].oid +
                                                                    query_result[0][0].indexes,
                                                                    query_result[0][0].oid_type, dic_result[keys]]})
                                elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                    dependent_oid.append({query_result[0][1] + str(
                                        -1): [query_result[0][2] + query_result[0][3]]})
                                    depend_oid_value.append({keys: [query_result[0][0].oid +
                                                                    query_result[0][0].indexes,
                                                                    query_result[0][0].oid_type, dic_result[keys]]})
                                else:
                                    dependent_oid.append(
                                        {query_result[0][1]: [query_result[0][2] + "." + str(id)]})
                                    depend_oid_value.append({keys: [query_result[0][0].oid + "." + str(
                                        id), query_result[0][0].oid_type, dic_result[keys]]})
                    else:
                        success_result["success"] = 1
                        success_result[
                            "result"] = "There is no row in database"

            pos = len(depend_oid_value)
            if pos != 0:
                for i in range(0, len(independent_oid)):
                    depend_oid_value[pos - 1].update(independent_oid[i])
            else:
                for i in range(0, len(independent_oid)):
                    depend_oid_value.append(independent_oid[i])
            device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port,
                                                           Hosts.snmp_write_community, Hosts.config_profile_id). \
                filter(Hosts.host_id == host_id).one()
            j = -1
            if len(dependent_oid) > 0:
                for i in range(0, len(dependent_oid)):
                    j += 1
                    if 'ru.ruConfTable.adminstate-1' in dependent_oid[i]:
                        result = (
                            pysnmp_set(
                                depend_oid_value[i], device_param_list[0],
                                device_param_list[1], device_param_list[2], dependent_oid[i]))
                    elif 'ru.ipConfigTable.adminState-1' in dependent_oid[i]:
                        result = (
                            pysnmp_set(
                                depend_oid_value[i], device_param_list[0],
                                device_param_list[1], device_param_list[2], dependent_oid[i]))
                    elif 'ru.ra.raConfTable.raAdminState-1' in dependent_oid[i]:
                        result = (
                            pysnmp_set(
                                depend_oid_value[i], device_param_list[0],
                                device_param_list[1], device_param_list[2], dependent_oid[i]))
                    else:
                        result = pysnmp_set(
                            depend_oid_value[i], device_param_list[0],
                            device_param_list[1], device_param_list[2], dependent_oid[i])
                    if result["success"] == 0 or result["success"] == '0':
                        success_result["success"] = result["success"]
                        for i in result["result"]:
                            if result["result"][i] != 0:
                                result["result"][
                                    i] = errorStatus[result["result"][i]]
                            else:
                                oid_list_table_field_value = sqlalche_obj.session.query(
                                    IduOids.table_name, IduOids.coloumn_name).filter(
                                    and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                else:

                                    if i in dic_result:
                                        table_name = "idu_" + \
                                                     oid_list_table_field_value[0][0]
                                        table_name = rename_tablename(
                                            table_name)
                                        exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                            table_name, table_name, device_param_list[3])
                                        exec "table_result[0].%s = '%s'" % (
                                            oid_list_table_field_value[0][1], dic_result[i])
                                        if ("idu_" + oid_list_table_field_value[0][0]) == "odu100_ipConfigTable":
                                            host_data = sqlalche_obj.session.query(Hosts).filter(
                                                Hosts.config_profile_id == device_param_list[3]).all()
                                            if i == "ru.ipConfigTable.ipAddress":
                                                host_data[
                                                    0].ip_address = dic_result[i]
                                            if i == "ru.ipConfigTable.ipNetworkMask":
                                                host_data[
                                                    0].netmask = dic_result[i]
                                            if i == "ru.ipConfigTable.ipDefaultGateway":
                                                host_data[
                                                    0].gateway = dic_result[i]
                                        sqlalche_obj.session.commit()
                        success_result["result"].update(result["result"])
                    else:
                        success_result["success"] = 1
                        for i in result["result"]:
                            i in errorStatus
                            success_result["result"] = errorStatus[i]

            if len(dependent_oid) > 0:
                for i in range(0, len(dependent_oid)):
                    query_admin_result = sqlalche_obj.session.query(
                        IduOids.oid, IduOids.oid_type, IduOids.indexes).filter(
                        IduOids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                    if 'ru.ruConfTable.adminstate-1' in dependent_oid[i]:
                        admin_state = "ru.ruConfTable.adminstate"
                        query_admin_result = sqlalche_obj.session.query(
                            IduOids.oid, IduOids.oid_type, IduOids.indexes).filter(
                            IduOids.oid_name == "ru.ruConfTable.adminstate").one()
                        dic_admin_value = {"ru.ruConfTable.adminstate": [query_admin_result[0] +
                                                                         query_admin_result[2], query_admin_result[1],
                                                                         '1']}
                        if len(query_admin_result) > 0:
                            result = pysnmp_set(
                                dic_admin_value, device_param_list[0],
                                device_param_list[1], device_param_list[2])
                            if result["success"] == 0 or result["success"] == '0':
                                success_result["success"] = result["success"]
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        result[
                                            "result"][i] = errorStatus[result["result"][i]]
                                    else:
                                        oid_list_table_field_value = sqlalche_obj.session.query(
                                            IduOids.table_name, IduOids.coloumn_name).filter(
                                            and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:
                                                table_name = "idu_" + \
                                                             oid_list_table_field_value[
                                                                 0][0]
                                                table_name = rename_tablename(
                                                    table_name)
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                    table_name, table_name, device_param_list[3])

                                                exec "table_result[0].%s = '%s'" % (
                                                    oid_list_table_field_value[0][1], dic_result[i])
                                            sqlalche_obj.session.commit()
                                            # success_result["result"].update(result["result"])
                            else:
                                # success_result["success"] = 1
                                for i in result["result"]:
                                    result["result"][i] in errorStatus
                                    # success_result["result"] =
                                    # errorStatus[result["result"][i]]

                    elif 'ru.ipConfigTable.adminState-1' in dependent_oid[i]:
                        query_admin_result = sqlalche_obj.session.query(
                            IduOids.oid, IduOids.oid_type, IduOids.indexes).filter(
                            IduOids.oid_name == "ru.ipConfigTable.adminState").one()
                        dic_admin_value = {"ru.ipConfigTable.adminState": [query_admin_result[0] +
                                                                           query_admin_result[2], query_admin_result[1],
                                                                           '1']}
                        if len(query_admin_result) > 0:
                            result = pysnmp_set(
                                dic_admin_value, device_param_list[0],
                                device_param_list[1], device_param_list[2])
                            if result["success"] == 0 or result["success"] == '0':
                                success_result["success"] = result["success"]
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        result[
                                            "result"][i] = errorStatus[result["result"][i]]
                                    else:
                                        oid_list_table_field_value = sqlalche_obj.session.query(
                                            IduOids.table_name, IduOids.coloumn_name).filter(
                                            and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:
                                                table_name = "idu_" + \
                                                             oid_list_table_field_value[
                                                                 0][0]
                                                table_name = rename_tablename(
                                                    table_name)
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                    table_name, table_name, device_param_list[3])
                                                exec "table_result[0].%s = '%s'" % (
                                                    oid_list_table_field_value[0][1], dic_result[i])
                                                # success_result["result"] =
                                                # errorStatus[result["result"][i]]
                            else:
                                # success_result["success"] = 1
                                for i in result["result"]:
                                    result["result"][i] in errorStatus
                                    # success_result["result"] =
                                    # errorStatus[result["result"][i]]
                    elif 'ru.ra.raConfTable.raAdminState-1' in dependent_oid[i]:
                        query_admin_result = sqlalche_obj.session.query(
                            IduOids.oid, IduOids.oid_type, IduOids.indexes).filter(
                            IduOids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                        dic_admin_value = {"ru.ra.raConfTable.raAdminState": [query_admin_result[0]
                                                                              + query_admin_result[2],
                                                                              query_admin_result[1], '1']}
                        if len(query_admin_result) > 0:
                            result = pysnmp_set(
                                dic_admin_value, device_param_list[0],
                                device_param_list[1], device_param_list[2])
                            if result["success"] == 0 or result["success"] == '0':
                                success_result["success"] = result["success"]
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        result[
                                            "result"][i] = errorStatus[result["result"][i]]
                                    else:
                                        oid_list_table_field_value = sqlalche_obj.session.query(
                                            IduOids.table_name, IduOids.coloumn_name).filter(
                                            and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:
                                                table_name = "idu_" + \
                                                             oid_list_table_field_value[
                                                                 0][0]
                                                table_name = rename_tablename(
                                                    table_name)
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                    table_name, table_name, device_param_list[3])
                                                exec "table_result[0].%s = '%s'" % (
                                                    oid_list_table_field_value[0][1], dic_result[i])
                                                # success_result["result"].update(result["result"])
                            else:
                                for i in result["result"]:
                                    result["result"][i] in errorStatus
                                    # success_result["result"] =
                                    # errorStatus[result["result"][i]]
                        break
                    else:
                        continue
            if (j == -1):
                if len(depend_oid_value) > 0:
                    for i in range(0, len(depend_oid_value)):
                        if id != None:
                            for key in depend_oid_value[i]:
                                oid = depend_oid_value[i][key][0][0:-1]
                                depend_oid_value[
                                    i][key][0] = str(oid) + str(id)
                        result = pysnmp_set(depend_oid_value[i], device_param_list[
                            0], device_param_list[1], device_param_list[2])
                        if result["success"] == 0 or result["success"] == '0':
                            success_result["success"] = result["success"]
                            for i in result["result"]:
                                if result["result"][i] != 0:
                                    result["result"][
                                        i] = errorStatus[result["result"][i]]
                                else:
                                    oid_list_table_field_value = sqlalche_obj.session.query(
                                        IduOids.table_name, IduOids.coloumn_name).filter(
                                        and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                                    if len(oid_list_table_field_value) == 0:
                                        continue
                                    else:
                                        if i in dic_result:
                                            sql_table_name = "idu_" + \
                                                             oid_list_table_field_value[
                                                                 0][0]
                                            tableName = sql_table_name + "_id"
                                            table_name = rename_tablename(
                                                sql_table_name)
                                            if int(index) != 0:
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(and_(%s.%s==%s,%s.config_profile_id == \"%s\")).all()" % (
                                                    table_name, table_name, tableName, index, table_name,
                                                    device_param_list[3])
                                            else:
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                    table_name, table_name, device_param_list[3])
                                            if len(table_result) > 0:
                                                if int(special_case) != 0 and special_case != '0':
                                                    exec "sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").update({'%s':%s})" % (
                                                        table_name, table_name, device_param_list[3],
                                                        oid_list_table_field_value[0][1], dic_result[i])
                                                else:
                                                    exec "table_result[0].%s = '%s'" % (
                                                        oid_list_table_field_value[0][1], dic_result[i])
                                            else:
                                                print table_result
                                                exist_data = 1
                            if exist_data == 1:
                                success_result["success"] = 1
                                success_result[
                                    "result"] = "Reconcilation process has exited. \n Please retry."
                            else:
                                success_result[
                                    "result"].update(result["result"])
                        else:
                            if 53 in result["result"]:
                                return {"success": 1, "result": "No Response From Device.Please Try Again"}
                            elif 51 in result["result"]:
                                return {"success": 1, "result": "Network is unreachable"}
                            elif 99 in result["result"]:
                                return {"success": 1,
                                        "result": "UNMP has encountered an unexpected error. Please Retry"}
                            ##                            if i==len(depend_oid_value)-1:
                            ##                                success_result["success"] = 1
                            ##                                for i in result["result"]:
                            ##                                    errorStatus.has_key(i)
                            # success_result["result"] = errorStatus[result["result"][i]]
                            else:
                                success_result["success"] = 0
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        if result["result"][i] in errorStatus:
                                            result["result"][i] = errorStatus[
                                                result["result"][i]]
                                success_result[
                                    "result"].update(result["result"])
                                continue

            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            return success_result

        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occured", "detail": ""}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occured", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occured", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occured", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occured", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occured", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occured,Contact Your Administrator", "detail": ""}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occured", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def common_validation(self, host_id, device_type_id, dic_result, id=None, index=0, special_case=0):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param id:
        @param index:
        @param special_case:
        @return:
        """
        try:
            obj_set = IduCommonSetValidation()
            flag = 0
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            if dic_result["success"] == '0' or dic_result["success"] == 0:
                for keys in dic_result.iterkeys():
                    if keys == "success":
                        continue
                    else:
                        oid_list_min_max_value = sqlalche_obj.session.query(
                            IduOids.min_value, IduOids.max_value).filter(
                            and_(IduOids.oid_name == keys, IduOids.device_type_id == device_type_id)).all()
                        if len(oid_list_min_max_value) == 0:
                            flag = 1
                            continue
                        else:
                            if (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == None) and (
                                    oid_list_min_max_value[0][1] != "" and oid_list_min_max_value[0][1] != None):
                                if int(dic_result[keys]) <= int(oid_list_min_max_value[0][1]):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "The value is large than %s" % (
                                        oid_list_min_max_value[1])
                                    break
                            elif (oid_list_min_max_value[0][0] != "" or oid_list_min_max_value[0][0] != None) and (
                                    oid_list_min_max_value[0][1] == "" and oid_list_min_max_value[0][1] == None):
                                if int(dic_result[keys]) >= int(oid_list_min_max_value[0][0]):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "The value is smaller than %s" % (
                                        oid_list_min_max_value[0][0])
                                    break
                            elif (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == None) and (
                                    oid_list_min_max_value[0][1] == "" or oid_list_min_max_value[0][1] == None):
                                dic_result["%s" % (keys)] = dic_result[keys]
                            elif (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == 'NULL') and (
                                    oid_list_min_max_value[0][1] == "" or oid_list_min_max_value[0][1] == 'NULL'):
                                dic_result["%s" % (keys)] = dic_result[keys]
                            else:
                                if (int(dic_result[keys]) >= int(oid_list_min_max_value[0][0])) and (
                                    int(dic_result[keys]) <= int(oid_list_min_max_value[0][1])):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "%s value must be in between %s and %s" % (keys.split(
                                        ".")[-1], oid_list_min_max_value[0][0], oid_list_min_max_value[0][1])
                                    break
                if flag == 1:
                    dic_result["success"] = 1
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    return dic_result
                else:
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    dic_result = obj_set.common_set_config(
                        host_id, device_type_id, dic_result, id, index, special_case=0)
                    return dic_result
            else:
                sqlalche_obj.sql_alchemy_db_connection_close()
                return dic_result
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            dic_result["success"] = 1
            dic_result["result"] = str(e)
            return str(e)

    def idu_cancel_form(self, host_id, device_type_id, dic_result, id=None, primary_key_id=None):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param id:
        @param primary_key_id:
        @return:
        """
        try:
            flag = 0
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            success_result = {}
            profile_id = sqlalche_obj.session.query(
                Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
            if dic_result["success"] == 0:
                for keys in dic_result:
                    if keys == "success":
                        continue
                    else:
                        oid_list_table_field_value = sqlalche_obj.session.query(
                            IduOids.table_name, IduOids.coloumn_name).filter(
                            and_(IduOids.oid_name == keys, IduOids.device_type_id == device_type_id)).all()
                        print oid_list_table_field_value
                        table_name = "idu_" + oid_list_table_field_value[0][0]
                        table_name = rename_tablename(table_name)
                        if id == None:
                            str_table_obj = "table_result = sqlalche_obj.session.query(%s.%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                table_name, oid_list_table_field_value[0][1], table_name, profile_id[0])
                        else:
                            str_table_obj = "table_result = sqlalche_obj.session.query(%s.%s).filter(and_(%s.config_profile_id == \"%s\",%s.%s == \"%s\")).all()" % (
                                table_name, oid_list_table_field_value[0][1], table_name, profile_id[0], table_name,
                                primary_key_id, id)
                        exec str_table_obj
                        print table_result
                        if len(table_result) > 0:
                            for i in range(0, len(table_result)):
                                dic_result[keys] = str(table_result[i][0])
                        else:
                            dic_result = {}
                            dic_result["success"] = 1
                            dic_result["result"] = "Data Not Exixt"
                sqlalche_obj.sql_alchemy_db_connection_close()
                return dic_result
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            dic_result["success"] = 1
            dic_result["result"] = str(e[-1])
            return dic_result

    def vlan_set(self, host_id, device_type_id, dic_result, addEdit, id, index=None):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param addEdit:
        @param id:
        @param index:
        @return:
        """
        try:
            global errorStatus
            if int(addEdit) == 0:
                print "hai"
                row_status_val = 4
            else:
                row_status_val = 1
            dic_result.update({'switch.vlanconfigTable.vlantype': 1,
                               'switch.vlanconfigTable.vlanrowstatus': row_status_val})
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {}
            o1 = aliased(IduOids)
            table_name = "IduOids"
            o2 = aliased(IduOids)
            result = {}
            vlan_data = {}
            independent_oid = []
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            for keys in dic_result.iterkeys():
                if keys == "success":
                    continue
                else:
                    query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                        o1, o1.oid_id == o2.dependent_id).filter(
                        and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()
                    if len(query_result) > 0:
                        try:
                            key = int(dic_result[keys])
                        except:
                            key = dic_result[keys]
                        independent_oid.append({keys: [query_result[0][0].oid + "." +
                                                       str(id), query_result[0][0].oid_type, key]})

            for i in independent_oid:
                for keys in i.iterkeys():
                    vlan_data.update(i)
            result = pysnmp_set(vlan_data, host_data[0].ip_address, host_data[
                0].snmp_port, host_data[0].snmp_write_community)
            if result["success"] == 0 or result["success"] == '0':
                if int(addEdit) == 0:
                    vlan_add_data = IduVlanconfigTable(
                        host_data[0].config_profile_id, id, dic_result[
                            'switch.vlanconfigTable.vlanname'],
                        dic_result[
                            'switch.vlanconfigTable.vlantype'],
                        dic_result[
                            'switch.vlanconfigTable.vlantag'],
                        dic_result['switch.vlanconfigTable.memberports'],
                        dic_result['switch.vlanconfigTable.vlanrowstatus'])
                    sqlalche_obj.session.add(vlan_add_data)
                else:
                    for i in result["result"]:
                        if result["result"][i] != 0:
                            result["result"][
                                i] = errorStatus[result["result"][i]]
                        else:
                            if i in dic_result:
                                oid_list_table_field_value = sqlalche_obj.session.query(
                                    IduOids.table_name, IduOids.coloumn_name).filter(
                                    and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                tablename = "idu_" + \
                                            oid_list_table_field_value[0].table_name
                                sql_table_name = rename_tablename(tablename)
                                exec "table_result=sqlalche_obj.session.query(%s).filter(and_(%s.config_profile_id=='%s',%s.vlanid=='%s')).all()" % (
                                    sql_table_name, sql_table_name, host_data[0].config_profile_id, sql_table_name, id)
                                if len(table_result) > 0:
                                    exec "table_result[0].%s='%s'" % (
                                        oid_list_table_field_value[0].coloumn_name, dic_result[i])

                sqlalche_obj.session.commit()
            else:

                if 53 in result["result"]:
                    result = {"success": 1, "result":
                        "No Response From Device.Please Try Again"}
                elif 51 in result["result"]:
                    result = {"success": 1, "result":
                        "Network is unreachable"}
                elif 99 in result["result"]:
                    result = {"success": 1, "result":
                        "UNMP has encountered an unexpected error. Please Retry"}
                else:
                    result = {"success": 1, "result": result["result"]}
            return result

        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occurs", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def delete_vlan_port(self, host_id, id):
        """

        @param host_id:
        @param id:
        @return:
        """
        try:
            if host_id == None:
                result = {"success": 1, "result":
                    "No Host Exist.Please Reconcile or add the host properly"}
            else:
                global errorStatus
                global sqlalche_obj
                sqlalche_obj.sql_alchemy_db_connection_open()
                host_data = sqlalche_obj.session.query(
                    Hosts).filter(Hosts.host_id == host_id).all()
                result = pysnmp_set(
                    {'row_stats': ['1.3.6.1.4.1.26149.2.1.6.5.1.6.%s' % (
                        id), 'Integer32', 6]}, host_data[0].ip_address,
                    int(host_data[0].snmp_port), host_data[0].snmp_write_community)
                if result["success"] == 0 or result["success"] == '0':
                    vlan_delete = sqlalche_obj.session.query(IduVlanconfigTable).filter(
                        and_(IduVlanconfigTable.config_profile_id == host_data[0].config_profile_id,
                             IduVlanconfigTable.vlanid == id)).delete()
                    sqlalche_obj.session.commit()
                else:
                    if 53 in result["result"]:
                        result = {"success": 1, "result":
                            "No Response From Device.Please Try Again"}
                    elif 51 in result["result"]:
                        result = {"success": 1,
                                  "result": "Network is unreachable"}
                    elif 99 in result["result"]:
                        result = {"success": 1, "result":
                            "UNMP has encountered an unexpected error. Please Retry"}
                    else:
                        for i in result["result"]:
                            error_result = errorStatus[result["result"][i]]
                        result = {"success": 1, "result": error_result}
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result
        except Exception as e:
            return {"success": 1, "result": str(e)}

    def e1_port_set(self, host_id, device_type_id, dic_result, id, index):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param id:
        @param index:
        @return:
        """
        try:
            global errorStatus
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {}
            o1 = aliased(IduOids)
            table_name = "IduOids"
            o2 = aliased(IduOids)
            result = {}
            e1_port_data = {}
            independent_oid = []
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            for keys in dic_result.iterkeys():
                if keys == "success":
                    continue
                else:
                    query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                        o1, o1.oid_id == o2.dependent_id).filter(
                        and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()
                    if len(query_result) > 0:
                        try:
                            key = int(dic_result[keys])
                        except:
                            key = dic_result[keys]
                        independent_oid.append({keys: [query_result[0][0].oid + "." +
                                                       str(id), query_result[0][0].oid_type, key]})

            for i in independent_oid:
                for keys in i.iterkeys():
                    e1_port_data.update(i)
            result = pysnmp_set(e1_port_data, host_data[0].ip_address, host_data[0].snmp_port,
                                host_data[0].snmp_write_community, {'adminState': [
                    '1.3.6.1.4.1.26149.2.1.2.3.1.2.%s' % (id), 'Integer32', 0]})
            if result["success"] == 0 or result["success"] == '0':
                for i in result["result"]:
                    if result["result"][i] != 0:
                        result["result"][i] = errorStatus[result["result"][i]]
                    else:
                        if i == "adminState1":
                            i = "iduConfiguration.e1PortConfigurationTable.adminState"
                            oid_list_table_field_value = sqlalche_obj.session.query(
                                IduOids.table_name, IduOids.coloumn_name).filter(
                                and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                            if len(oid_list_table_field_value) == 0:
                                continue
                            tablename = "idu_" + \
                                        oid_list_table_field_value[0].table_name
                            sql_table_name = rename_tablename(tablename)
                            exec "table_result=sqlalche_obj.session.query(%s).filter(and_(%s.config_profile_id=='%s',%s.portNumber=='%s')).all()" % (
                                sql_table_name, sql_table_name, host_data[0].config_profile_id, sql_table_name, id)
                            if len(table_result) > 0:
                                exec "table_result[0].%s='%s'" % (
                                    oid_list_table_field_value[0].coloumn_name, 1)
                        elif i in dic_result:
                            oid_list_table_field_value = sqlalche_obj.session.query(
                                IduOids.table_name, IduOids.coloumn_name).filter(
                                and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                            if len(oid_list_table_field_value) == 0:
                                continue
                            tablename = "idu_" + \
                                        oid_list_table_field_value[0].table_name
                            sql_table_name = rename_tablename(tablename)
                            exec "table_result=sqlalche_obj.session.query(%s).filter(and_(%s.config_profile_id=='%s',%s.portNumber=='%s')).all()" % (
                                sql_table_name, sql_table_name, host_data[0].config_profile_id, sql_table_name, id)
                            if len(table_result) > 0:
                                exec "table_result[0].%s='%s'" % (
                                    oid_list_table_field_value[0].coloumn_name, dic_result[i])

                    sqlalche_obj.session.commit()
            else:

                if 53 in result["result"]:
                    result = {"success": 1, "result":
                        "No Response From Device.Please Try Again"}
                elif 51 in result["result"]:
                    result = {"success": 1, "result":
                        "Network is unreachable"}
                elif 99 in result["result"]:
                    result = {"success": 1, "result":
                        "UNMP has encountered an unexpected error. Please Retry"}
                else:
                    result = {"success": 1, "result": result["result"]}
            return result

        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occurs", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def check_vlan_tag(self, vlan_tag, host_id):
        """

        @param vlan_tag:
        @param host_id:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_data = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
        vlan_data = sqlalche_obj.session.query(IduVlanconfigTable.vlantag).filter(
            IduVlanconfigTable.config_profile_id == host_data[0].config_profile_id).all()
        flag = 0
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(vlan_data) > 0:
            for i in range(0, len(vlan_data)):
                if int(vlan_tag) in vlan_data[i]:
                    flag = 1
                    break
                else:
                    flag = 0
        else:
            flag = 0
        if flag == 1:
            return 1
        else:
            return 0

    def check_vlan_name(self, vlan_name, host_id):
        """

        @param vlan_name:
        @param host_id:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_data = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
        vlan_data = sqlalche_obj.session.query(IduVlanconfigTable.vlanname).filter(
            IduVlanconfigTable.config_profile_id == host_data[0].config_profile_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(vlan_data) > 0:
            for i in range(0, len(vlan_data)):
                if vlan_name in vlan_data[i]:
                    flag = 1
                    break
                else:
                    flag = 0
        else:
            flag = 0
        if flag == 1:
            return 1
        else:
            return 0

    def chk_link_e1_port(self, host_id, port_id):
        """

        @param host_id:
        @param port_id:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_data = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
        e1_port_data = sqlalche_obj.session.query(IduLinkConfigurationTable).filter(
            and_(IduLinkConfigurationTable.config_profile_id == host_data[0].config_profile_id,
                 IduLinkConfigurationTable.portNumber == port_id)).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(e1_port_data) > 0:
            return 1
        else:
            return 0

    def set_link_port(self, host_id, device_type_id, dic_result, id, index, addEdit):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param id:
        @param index:
        @param addEdit:
        @return:
        """
        try:
            global errorStatus
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {}
            o1 = aliased(IduOids)
            table_name = "IduOids"
            o2 = aliased(IduOids)
            result = {}
            link_port_data = {}
            independent_oid = []
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            for keys in dic_result.iterkeys():
                if keys == "success":
                    continue
                else:
                    query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                        o1, o1.oid_id == o2.dependent_id).filter(
                        and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()
                    if len(query_result) > 0:
                        if keys == "iduConfiguration_linkConfigurationTable_tsaAssign":
                            key = dic_result[keys]
                        else:
                            try:
                                key = int(dic_result[keys])
                            except:
                                key = dic_result[keys]
                        independent_oid.append({keys: [query_result[0][0].oid + "." + str(
                            index) + "." + str(id), query_result[0][0].oid_type, key]})

            for i in independent_oid:
                for keys in i.iterkeys():
                    link_port_data.update(i)
            if int(addEdit) == 1:
                result = pysnmp_set(link_port_data, host_data[0].ip_address, host_data[0].snmp_port,
                                    host_data[0].snmp_write_community, {'adminState': [
                        '1.3.6.1.4.1.26149.2.1.2.2.1.3.%s.%s' % (index, id), 'Integer32', 0]})
            else:
                result = pysnmp_seter(link_port_data, host_data[0].ip_address, host_data[0].snmp_port,
                                      host_data[0].snmp_write_community, {
                        'iduConfiguration.linkConfigurationTable.rowStatus': [
                            '1.3.6.1.4.1.26149.2.1.2.2.1.11.%s.%s' % (index, id), 'Integer32', 4]})
            if result["success"] == 0 or result["success"] == '0':
                if int(addEdit) == 1:
                    for i in result["result"]:
                        if result["result"][i] != 0:
                            result["result"][
                                i] = errorStatus[result["result"][i]]
                        else:
                            if i == "adminState1":
                                i = "iduConfiguration.linkConfigurationTable.adminStatus"
                                oid_list_table_field_value = sqlalche_obj.session.query(
                                    IduOids.table_name, IduOids.coloumn_name).filter(
                                    and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                tablename = "idu_" + \
                                            oid_list_table_field_value[0].table_name
                                sql_table_name = rename_tablename(tablename)
                                exec "table_result=sqlalche_obj.session.query(%s).filter(and_(%s.config_profile_id=='%s',%s.portNumber=='%s')).all()" % (
                                    sql_table_name, sql_table_name, host_data[0].config_profile_id, sql_table_name, id)
                                if len(table_result) > 0:
                                    exec "table_result[0].%s='%s'" % (
                                        oid_list_table_field_value[0].coloumn_name, 1)
                            elif i in dic_result:
                                oid_list_table_field_value = sqlalche_obj.session.query(
                                    IduOids.table_name, IduOids.coloumn_name).filter(
                                    and_(IduOids.oid_name == i, IduOids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                tablename = "idu_" + \
                                            oid_list_table_field_value[0].table_name
                                sql_table_name = rename_tablename(tablename)
                                exec "table_result=sqlalche_obj.session.query(%s).filter(and_(%s.config_profile_id=='%s',%s.portNumber=='%s')).all()" % (
                                    sql_table_name, sql_table_name, host_data[0].config_profile_id, sql_table_name, id)
                                if len(table_result) > 0:
                                    exec "table_result[0].%s='%s'" % (
                                        oid_list_table_field_value[0].coloumn_name, dic_result[i])
                else:
                    add_link_row = IduLinkConfigurationTable(
                        host_data[0].config_profile_id, index, id, 0,
                        dic_result[
                            'iduConfiguration.linkConfigurationTable.srcBundleID'],
                        dic_result[
                            'iduConfiguration.linkConfigurationTable.dstBundleID'],
                        dic_result[
                            'iduConfiguration.linkConfigurationTable.dstIPAddr'],
                        dic_result[
                            'iduConfiguration_linkConfigurationTable_tsaAssign'],
                        dic_result['iduConfiguration_linkConfigurationTable_clockRecovery'],
                        dic_result['iduConfiguration.linkConfigurationTable.bundleSize'],
                        dic_result['iduConfiguration.linkConfigurationTable.bufferSize'],
                        1)
                    sqlalche_obj.session.add(add_link_row)
            else:
                if 53 in result["result"]:
                    result = {"success": 1, "result":
                        "No Response From Device.Please Try Again"}
                elif 51 in result["result"]:
                    result = {"success": 1, "result":
                        "Network is unreachable"}
                elif 99 in result["result"]:
                    result = {"success": 1, "result":
                        "UNMP has encountered an unexpected error. Please Retry"}
                else:
                    result = {"success": 1, "result": result["result"]}

            sqlalche_obj.session.commit()

            return result

        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occurs", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()


class LinkConfiguration(object):
    """
    IDU link configuration related class
    """
    def delete_link_port(self, host_id, id, port_number, link_number):
        """

        @param host_id:
        @param id:
        @param port_number:
        @param link_number:
        @return:
        """
        try:
            if host_id == None:
                result = {"success": 1, "result":
                    "No Host Exist.Please Reconcile or add the host properly"}
            else:
                global errorStatus
                global sqlalche_obj
                sqlalche_obj.sql_alchemy_db_connection_open()
                host_data = sqlalche_obj.session.query(
                    Hosts).filter(Hosts.host_id == host_id).all()
                result = pysnmp_set({'row_stats': ['1.3.6.1.4.1.26149.2.1.2.2.1.11.%s.%s' % (port_number, link_number),
                                                   'Integer32', 6]}, host_data[0]
                                    .ip_address, int(host_data[0].snmp_port), host_data[0].snmp_write_community)
                if result["success"] == 0 or result["success"] == '0':
                    link_delete = sqlalche_obj.session.query(IduLinkConfigurationTable).filter(
                        IduLinkConfigurationTable.idu_linkConfigurationTable_id == id).delete()
                    sqlalche_obj.session.commit()
                else:
                    if 53 in result["result"]:
                        result = {"success": 1, "result":
                            "No Response From Device.Please Try Again"}
                    elif 51 in result["result"]:
                        result = {"success": 1,
                                  "result": "Network is unreachable"}
                    elif 99 in result["result"]:
                        result = {"success": 1, "result":
                            "UNMP has encountered an unexpected error. Please Retry"}
                    else:
                        for i in result["result"]:
                            error_result = errorStatus[result["result"][i]]
                        result = {"success": 1, "result": error_result}
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result
        except Exception as e:
            return {"success": 1, "result": str(e)}

    def selected_timeslot(self, host_id, port_num):
        """

        @param host_id:
        @param port_num:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_data = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        timeslot = sqlalche_obj.session.query(IduLinkConfigurationTable).filter(
            and_(IduLinkConfigurationTable.config_profile_id == host_data[0].config_profile_id,
                 IduLinkConfigurationTable.portNumber == port_num)).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(timeslot) > 0:
            return timeslot[0].tsaAssign
        else:
            return []

    def link_chk(self, host_id, link_num):
        """

        @param host_id:
        @param link_num:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        link_data = []
        host_data = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        link_data = sqlalche_obj.session.query(IduLinkConfigurationTable).filter(
            and_(IduLinkConfigurationTable.config_profile_id == host_data[0].config_profile_id,
                 IduLinkConfigurationTable.bundleNumber == link_num)).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if link_data == []:
            return 0
        else:
            return 1

    def src_bundle_chk(self, host_id, src_bundle_id, link, port):
        """

        @param host_id:
        @param src_bundle_id:
        @param link:
        @param port:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        flag = 0
        host_data = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        src_bundle_data = sqlalche_obj.session.query(IduLinkConfigurationTable.srcBundleID).filter(
            IduLinkConfigurationTable.config_profile_id == host_data[0].config_profile_id).all()
        src_bundle_set = sqlalche_obj.session.query(
            IduLinkConfigurationTable.srcBundleID).filter(
            and_(
                IduLinkConfigurationTable.config_profile_id == host_data[
                    0].config_profile_id,
                IduLinkConfigurationTable.bundleNumber == link, IduLinkConfigurationTable.portNumber == port)).all()
        if src_bundle_set != []:
            print src_bundle_set[0].srcBundleID
            if src_bundle_set[0].srcBundleID == src_bundle_id:
                flag = 0
            else:
                for i in range(0, len(src_bundle_data)):
                    if src_bundle_id in src_bundle_data[i]:
                        flag = 1
                        break
                    else:
                        flag = 0

        else:
            for i in range(0, len(src_bundle_data)):
                if src_bundle_id in src_bundle_data[i]:
                    flag = 1
                    break
                else:
                    flag = 0

        if flag == 0:
            return 0
        else:
            return 1
        sqlalche_obj.sql_alchemy_db_connection_close()

    def destination_bundle_chk(self, host_id, dst_bundle_id, link, port):
        """

        @param host_id:
        @param dst_bundle_id:
        @param link:
        @param port:
        @return:
        """
        global sqlalche_obj
        flag = 0
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_data = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        dst_bundle_data = sqlalche_obj.session.query(IduLinkConfigurationTable.dstBundleID).filter(
            IduLinkConfigurationTable.config_profile_id == host_data[0].config_profile_id).all()
        dst_bundle_set = sqlalche_obj.session.query(
            IduLinkConfigurationTable.dstBundleID).filter(
            and_(
                IduLinkConfigurationTable.config_profile_id == host_data[
                    0].config_profile_id,
                IduLinkConfigurationTable.bundleNumber == link, IduLinkConfigurationTable.portNumber == port)).all()

        if dst_bundle_set != []:
            if dst_bundle_set[0].dstBundleID == dst_bundle_id:
                flag = 0
            else:
                for i in range(0, len(src_bundle_data)):
                    if dst_bundle_id in dst_bundle_data[i]:
                        flag = 1
                        break
                    else:
                        flag = 0

        else:
            for i in range(0, len(dst_bundle_data)):
                if dst_bundle_id in dst_bundle_data[i]:
                    flag = 1
                    break
                else:
                    flag = 0

        if flag == 0:
            return 0
        else:
            return 1
        sqlalche_obj.sql_alchemy_db_connection_close()


class IduLinkCount(object):
    """
    IDU link related class
    """
    def link_count(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            global sqlalchemy
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(
                Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
            all_link_count = sqlalche_obj.session.query(IduLinkConfigurationTable). \
                filter(IduLinkConfigurationTable.config_profile_id == host_data[0]
            .config_profile_id).count()
            if all_link_count > 0:
                link_data_count = sqlalche_obj.session.query(IduLinkConfigurationTable). \
                    filter(and_
                    (IduLinkConfigurationTable.config_profile_id == host_data[0].config_profile_id,
                     IduLinkConfigurationTable.adminStatus == 1)).count()

                total_link_unlocked = float(
                    link_data_count) / float(all_link_count)
                total_link_unlocked = int(total_link_unlocked * 100)
                result = {"success": 0, "result": total_link_unlocked}
            else:
                result = {"success": 1, "result": 0}

        except Exception as e:
            result = {"success": 1, "result": str(e)}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

    def global_admin_change(self, host_ids):
        """

        @param host_ids:
        @return:
        """
        try:
            global sqlalchemy
            admin_data_dic = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_ids == "" or host_ids == None or host_ids == 'undefined':
                result = {"success": 1, "result": "No Host Exist"}
            else:
                host_ids_list = host_ids.split(",")
                for i in range(0, len(host_ids_list)):
                    host_data_list = sqlalche_obj.session.query(
                        Hosts.config_profile_id).filter(Hosts.host_id == host_ids_list[i]).all()
                    if len(host_data_list) > 0:
                        e1_admin_data_list = sqlalche_obj.session.query(
                            IduE1PortConfigurationTable.adminState).filter(
                            IduE1PortConfigurationTable.config_profile_id == host_data_list[0][0]).all()
                        main_admin_data_list = sqlalche_obj.session.query(
                            IduIduAdminStateTable.adminstate).filter(
                            IduIduAdminStateTable.config_profile_id == host_data_list[0][0]).all()
                        total_link_unlocked = self.link_count(host_ids_list[i])
                        if total_link_unlocked['success'] == 0:
                            link_title = total_link_unlocked['result']
                        else:
                            link_title = "No Link Exists"
                        sqlalche_obj.sql_alchemy_db_connection_open()
                        if len(e1_admin_data_list) > 0:
                            temp_list = []
                            for j in range(0, len(e1_admin_data_list)):
                                temp_list.append(
                                    int(e1_admin_data_list[j].adminState))
                            admin_data_dic.update({host_ids_list[i]: [temp_list, main_admin_data_list[0]
                            .adminstate if len(main_admin_data_list) > 0 else 0, link_title]})

                    else:
                        admin_data_dic.update(
                            {host_ids_list[i]: "No Host Exist"})
                sqlalche_obj.sql_alchemy_db_connection_close()
                result = {'success': 0, 'result': admin_data_dic}

        except Exception as e:
            result = {"success": 1, "result": str(e)}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

    def global_admin_request(self, host_ids):
        """

        @param host_ids:
        @return:
        """
        try:
            global sqlalchemy
            admin_data_dic = {}
            obj_get_data = IduGetData()
            sqlalche_obj.sql_alchemy_db_connection_open()
            link_data_list = []
            e1_op_list = []
            if host_ids == "" or host_ids == None or host_ids == 'undefined':
                result = {"success": 1, "result": "No Host Exist"}
            else:
                host_ids_list = host_ids.split(",")
                for i in range(0, len(host_ids_list)):
                    host_data_list = sqlalche_obj.session.query(
                        Hosts.config_profile_id).filter(Hosts.host_id == host_ids_list[i]).all()
                    if len(host_data_list) > 0:
                        e1_status_data = sqlalche_obj.session.query(IduE1PortStatusTable).filter(
                            IduE1PortStatusTable.host_id == host_ids_list[i]).order_by(
                            desc(IduE1PortStatusTable.timestamp)).order_by(asc(IduE1PortStatusTable.portNum)).limit(
                            4).all()
                        e1_admin_data_list = sqlalche_obj.session.query(
                            IduE1PortConfigurationTable.adminState).filter(
                            IduE1PortConfigurationTable.config_profile_id == host_data_list[0][0]).all()
                        main_admin_data_list = sqlalche_obj.session.query(
                            IduIduAdminStateTable.adminstate).filter(
                            IduIduAdminStateTable.config_profile_id == host_data_list[0][0]).all()
                        total_link_data = obj_get_data.common_get_data(
                            "IduLinkConfigurationTable", host_ids_list[i])
                        if len(total_link_data) > 0:
                            for k in range(0, len(total_link_data)):
                                link_data_list.append(
                                    int(total_link_data[k].adminStatus))
                        if len(e1_admin_data_list) > 0:
                            temp_list = []
                            for j in range(0, len(e1_admin_data_list)):
                                temp_list.append(
                                    int(e1_admin_data_list[j].adminState))
                        if len(e1_status_data) > 0:
                            for k in range(0, len(e1_status_data)):
                                e1_op_list.append(
                                    int(e1_status_data[k].opStatus))
                        admin_data_dic.update({host_ids_list[i]: [temp_list, main_admin_data_list[0].adminstate if len(
                            main_admin_data_list) > 0 else 0, e1_op_list, link_data_list]})

                    else:
                        admin_data_dic.update(
                            {host_ids_list[i]: "No Host Exist"})
                sqlalche_obj.sql_alchemy_db_connection_close()
                result = {'success': 0, 'result': admin_data_dic}

        except Exception as e:
            result = {"success": 1, "result": str(e)}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

# obj = IduLinkCount()
# print obj.link_count(80)
# print obj.global_admin_request("35")


class IduAdminStateChange(object):
    """
    Fetch the IDU admin states for ports and links
    """
    #{"result": {"iduConfiguration.e1PortConfigurationTable.adminState": 14}, "success": 1}

    def get_admin_op_state(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj
        global errorStatus
        snmp_get = {}
        try:
            # sqlalche_obj.sql_alchemy_db_connection_open()
            get_dic_operation = {
                'e1': '1.3.6.1.4.1.26149.2.1.2.3.1.2.1', 'e2': '1.3.6.1.4.1.26149.2.1.2.3.1.2.2',
                'e3': '1.3.6.1.4.1.26149.2.1.2.3.1.2.3', 'e4': '1.3.6.1.4.1.26149.2.1.2.3.1.2.4',
                'admin': '1.3.6.1.4.1.26149.2.1.1.1.1.2.1', 'e1op': '1.3.6.1.4.1.26149.2.1.3.2.1.2.1',
                'e2op': '1.3.6.1.4.1.26149.2.1.3.2.1.2.2',
                'e3op': '1.3.6.1.4.1.26149.2.1.3.2.1.2.3', 'e4op': '1.3.6.1.4.1.26149.2.1.3.2.1.2.4'}
            obj_get_data = IduGetData()
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            e1_data = sqlalche_obj.session.query(IduE1PortConfigurationTable).filter(
                IduE1PortConfigurationTable.config_profile_id == host_data[0].config_profile_id).all()
            admin_data = sqlalche_obj.session.query(IduIduAdminStateTable).filter(
                IduIduAdminStateTable.config_profile_id == host_data[0].config_profile_id).all()
            e1_status_data = sqlalche_obj.session.query(IduE1PortStatusTable).filter(
                IduE1PortStatusTable.host_id == host_id).order_by(desc(IduE1PortStatusTable.timestamp)).order_by(
                asc(IduE1PortStatusTable.portNum)).limit(4).all()

            k = 0
            snmp_get = pysnmp_geter(get_dic_operation, host_data[0].ip_address, int(
                host_data[0].snmp_port), host_data[0].snmp_read_community)
            if snmp_get['success'] == 0:
                print "hello"
                for i in snmp_get['result']:
                    if int(snmp_get['result'][i]) != -1:
                        if i == 'e1':
                            if len(e1_data) > 0:
                                e1_data[0].adminState = snmp_get['result'][i]
                        elif i == 'e2':
                            if len(e1_data) > 0:
                                e1_data[1].adminState = snmp_get['result'][i]
                        elif i == 'e3':
                            if len(e1_data) > 0:
                                e1_data[2].adminState = snmp_get['result'][i]
                        elif i == 'e4':
                            if len(e1_data) > 0:
                                e1_data[3].adminState = snmp_get['result'][i]
                        elif i == 'admin':
                            if len(admin_data) > 0:
                                admin_data[
                                    0].adminstate = snmp_get['result'][i]
                        elif i == 'e1op':
                            if len(e1_status_data) > 0:
                                e1_status_data[
                                    0].opStatus = snmp_get['result'][i]
                        elif i == 'e2op':
                            if len(e1_status_data) > 0:
                                e1_status_data[
                                    1].opStatus = snmp_get['result'][i]
                        elif i == 'e3op':
                            if len(e1_status_data) > 0:
                                e1_status_data[
                                    2].opStatus = snmp_get['result'][i]
                        elif i == 'e4op':
                            if len(e1_status_data) > 0:
                                e1_status_data[
                                    3].opStatus = snmp_get['result'][i]
                sqlalche_obj.session.commit()
            else:
                for i in snmp_get["result"]:
                    if i == 553:
                        snmp_get["result"] = str(host_data[0].host_alias) + " (" + str(host_data[0]
                        .ip_address) + ") " + str(errorStatus.get(i, "Device is not resposive"))
                    elif i == 551:
                        snmp_get["result"] = str(host_data[0].host_alias) + " (" + str(host_data[0]
                        .ip_address) + ") " + str(errorStatus.get(i, "Device is not resposive"))
                    elif snmp_result["result"][i] != 0:
                        snmp_get["result"] = str(host_data[0].host_alias) + " (" + str(
                            host_data[0].ip_address) + ") " + str(
                            errorStatus.get(snmp_get["result"][i], "Device is not resposive"))
        except Exception as e:
            snmp_get['success'] = 1
            snmp_get['result'] = str(e)
        finally:

            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_get

    def e1_port_admin_change(self, host_id, primary_id, port_number, admin_state_name, state):
        """

        @param host_id:
        @param primary_id:
        @param port_number:
        @param admin_state_name:
        @param state:
        @return:
        """
        global sqlalche_obj
        global errorStatus
        try:
            snmp_result = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            oid_data = sqlalche_obj.session.query(IduOids.oid, IduOids.oid_type).filter(
                IduOids.oid_name == admin_state_name).all()
            oid_dic = {admin_state_name: [str(oid_data[0].oid) + "." + str(
                port_number), oid_data[0].oid_type, state]}
            snmp_result = pysnmp_seter(oid_dic, host_data[0].ip_address, int(
                host_data[0].snmp_port), host_data[0].snmp_write_community)

            if snmp_result['success'] == 0:
                for i in snmp_result['result']:
                    if snmp_result['result'][i] == 0:
                        self.get_admin_op_state(host_id)
                        # e1_port_data = sqlalche_obj.session.query(IduE1PortConfigurationTable).filter(IduE1PortConfigurationTable.idu_e1PortConfigurationTable_id==primary_id).all()
                        # e1_port_data[0].adminState = state
                        # sqlalche_obj.session.commit()
            else:
                if 53 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                elif 51 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                else:
                    for i in snmp_result["result"]:
                        if int(snmp_result["result"].values()[0]) != 0:
                            snmp_result["result"] = errorStatus.get(int(
                                snmp_result["result"].values()[0]), "SNMP agent not respond")

        except:
            snmp_result['success'] = 1
            snmp_result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_result

    def link_port_admin_change(self, host_id, primary_id, port_number, bundle_number, admin_state_name, state):
        """

        @param host_id:
        @param primary_id:
        @param port_number:
        @param bundle_number:
        @param admin_state_name:
        @param state:
        @return:
        """
        global sqlalche_obj
        global errorStatus
        try:
            snmp_result = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            oid_data = sqlalche_obj.session.query(IduOids.oid, IduOids.oid_type).filter(
                IduOids.oid_name == admin_state_name).all()
            oid_dic = {admin_state_name: [str(oid_data[0].oid) + "." + str(
                port_number) + "." + str(bundle_number), oid_data[0].oid_type, state]}
            snmp_result = pysnmp_seter(oid_dic, host_data[0].ip_address, int(
                host_data[0].snmp_port), host_data[0].snmp_write_community)
            if snmp_result['success'] == 0:
                for i in snmp_result['result']:
                    if snmp_result['result'][i] == 0:
                        link_port_data = sqlalche_obj.session.query(IduLinkConfigurationTable).filter(
                            IduLinkConfigurationTable.idu_linkConfigurationTable_id == primary_id).all()
                        link_port_data[0].adminStatus = state
                    sqlalche_obj.session.commit()
            else:
                if 53 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                elif 51 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                else:
                    for i in snmp_result["result"]:
                        if snmp_result["result"][i] != 0:
                            if snmp_result["result"].get(i) in errorStatus:
                                if snmp_result["result"].get(i) == 12:
                                    snmp_result[
                                        "result"] = "The link is not on device.So please reconcile the device"
                                else:
                                    snmp_result[
                                        "result"] = errorStatus[snmp_result["result"][i]]

        except:
            snmp_result['success'] = 1
            snmp_result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_result

    def main_admin_change(self, host_id, admin_state_name, state):
        """

        @param host_id:
        @param admin_state_name:
        @param state:
        @return:
        """
        global sqlalche_obj
        global errorStatus
        try:
            snmp_result = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            oid_data = sqlalche_obj.session.query(
                IduOids.oid, IduOids.indexes, IduOids.oid_type).filter(IduOids.oid_name == admin_state_name).all()
            oid_dic = {admin_state_name: [str(oid_data[0].oid) + str(
                oid_data[0].indexes), oid_data[0].oid_type, state]}
            snmp_result = pysnmp_seter(oid_dic, host_data[0].ip_address, int(
                host_data[0].snmp_port), host_data[0].snmp_write_community)
            if snmp_result['success'] == 0:
                for i in snmp_result['result']:
                    if snmp_result['result'][i] == 0:
                        self.get_admin_op_state(host_id)
                    ##                        main_admin_data = sqlalche_obj.session.query(IduIduAdminStateTable).filter(IduIduAdminStateTable.config_profile_id==host_data[0].config_profile_id).all()
                    ##                        main_admin_data[0].adminstate = state
                    ##                    sqlalche_obj.session.commit()
            else:
                if 53 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                elif 51 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                else:
                    for i in snmp_result["result"]:
                        if snmp_result["result"][i] != 0:
                            if i in errorStatus:
                                snmp_result["result"] = errorStatus[i]

        except:
            snmp_result['success'] = 1
            snmp_result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_result

    def locked_unlocked_all(self, host_id, port_num, primary_ids, admin_state_name, state):
        """

        @param host_id:
        @param port_num:
        @param primary_ids:
        @param admin_state_name:
        @param state:
        @return:
        """
        global sqlalche_obj
        global errorStatus
        try:
            snmp_result = {}
            oid_dic = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            oid_data = sqlalche_obj.session.query(
                IduOids.oid, IduOids.indexes, IduOids.oid_type).filter(IduOids.oid_name == admin_state_name).all()
            port_num_list = port_num.split(",")
            primary_id_list = primary_ids.split(",")
            primary_id_dic = {}
            if len(port_num_list) > 0:
                for i in range(0, len(port_num_list)):
                    temp_dic = {'admin_state_%s' % (port_num_list[i]): [str(
                        oid_data[0].oid) + "." + str(port_num_list[i]), oid_data[0].oid_type, state]}
                    oid_dic.update(temp_dic)
                    primary_id_dic.update({'admin_state_%s' % (
                        port_num_list[i]): primary_id_list[i]})
            snmp_result = pysnmp_seter(oid_dic, host_data[0].ip_address, int(
                host_data[0].snmp_port), host_data[0].snmp_write_community)
            if snmp_result['success'] == 0:
                for i in snmp_result['result']:
                    if snmp_result['result'][i] == 0:
                        e1_port_data = sqlalche_obj.session.query(IduE1PortConfigurationTable).filter(
                            IduE1PortConfigurationTable.idu_e1PortConfigurationTable_id == primary_id_dic[i]).all()
                        e1_port_data[0].adminState = state
                    else:
                        if snmp_result["result"].get(i) in errorStatus:
                            snmp_result["result"][
                                i] = errorStatus[snmp_result["result"][i]]
                sqlalche_obj.session.commit()
            else:
                if 53 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                elif 51 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                else:
                    for i in snmp_result["result"]:
                        if snmp_result["result"][i] != 0:
                            if snmp_result["result"].get(i) in errorStatus:
                                snmp_result[
                                    "result"] = errorStatus[snmp_result["result"][i]]
        except:
            snmp_result['success'] = 1
            snmp_result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_result

    def link_locked_unlocked_all(self, host_id, port_num, primary_ids, bundle_num, admin_state_name, state):
        """

        @param host_id:
        @param port_num:
        @param primary_ids:
        @param bundle_num:
        @param admin_state_name:
        @param state:
        @return:
        """
        global sqlalche_obj
        global errorStatus
        try:
            snmp_result = {}
            oid_dic = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            oid_data = sqlalche_obj.session.query(
                IduOids.oid, IduOids.indexes, IduOids.oid_type).filter(IduOids.oid_name == admin_state_name).all()
            port_num_list = port_num.split(",")
            primary_id_list = primary_ids.split(",")
            bundle_num_list = bundle_num.split(",")
            primary_id_dic = {}
            if len(port_num_list) > 0:
                for i in range(0, len(port_num_list)):
                    temp_dic = {'admin_state_%s' % (port_num_list[i]): [str(oid_data[0].oid) + "." + str(
                        port_num_list[i]) + "." + str(bundle_num_list[i]), oid_data[0].oid_type, state]}
                    oid_dic.update(temp_dic)
                    primary_id_dic.update({'admin_state_%s' % (
                        port_num_list[i]): primary_id_list[i]})
            snmp_result = pysnmp_seter(oid_dic, host_data[0].ip_address, int(
                host_data[0].snmp_port), host_data[0].snmp_write_community)
            if snmp_result['success'] == 0:
                for i in snmp_result['result']:
                    if snmp_result['result'][i] == 0:
                        link_port_data = sqlalche_obj.session.query(IduLinkConfigurationTable).filter(
                            IduLinkConfigurationTable.idu_linkConfigurationTable_id == primary_id_dic[i]).all()
                        link_port_data[0].adminStatus = state
                    else:
                        if snmp_result["result"].get(i) in errorStatus:
                            snmp_result["result"][
                                i] = errorStatus[snmp_result["result"][i]]
                sqlalche_obj.session.commit()
            else:
                if 53 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                elif 51 in snmp_result["result"]:
                    snmp_result["result"] = errorStatus[53]
                else:
                    for i in snmp_result["result"]:
                        if snmp_result["result"][i] != 0:
                            if snmp_result["result"].get(i) in errorStatus:
                                if snmp_result["result"].get(i) == 12:
                                    snmp_result[
                                        "result"] = "The link is not on device.So please reconcile the device"
                                else:
                                    snmp_result[
                                        "result"] = errorStatus[snmp_result["result"][i]]
        except:
            snmp_result['success'] = 1
            snmp_result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_result


# obj = IduAdminStateChange()
# print obj.get_admin_op_state(35)
# print obj.main_admin_change(65,'iduinfo.iduAdminStateTable.adminstate',1)
# print obj.link_locked_unlocked_all(65,"1,2,3","16,17,18","1,2,3","iduConfiguration.linkConfigurationTable.adminStatus",0)
# print obj.link_port_admin_change(65,18,3,3,'iduConfiguration.linkConfigurationTable.adminStatus',1)
# print
# obj.e1_port_admin_change(80,49,1,'iduConfiguration.e1PortConfigurationTable.adminState',1)
