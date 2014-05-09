from datetime import datetime
import time

from sqlalchemy import and_, or_, desc, asc
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *

from common_bll import EventLog, Essential
from common_controller import *
from unmp_config import SystemConfig
from unmp_model import *
from pysnmp_module import pysnmp_set  # , pysnmp_get_table_ap
from pysnmp_v1 import pysnmp_get_table as ccu_bulk
from pysnmp_v1 import pysnmp_seter, snmp_ping
#from utility import ErrorMessages, Validation
#from py_module import pysnmp_geter, pysnmp_get_table, pysnmp_set1

essential_obj = Essential()

errorStatus = {0: 'noError',
               1: 'tooBig',
               2: 'noSuchName',
               3: 'badValue',
               4: 'readOnly',
               5: 'genErr',
               6: 'noAccess',
               7: 'wrongType',
               8: 'wrongLength',
               9: 'wrongEncoding',
               10: 'wrongValue',
               11: 'noCreation',
               12: 'inconsistentValue',
               13: 'resourceUnavailable',
               14: 'Commit is failed',
               15: 'undoFailed',
               16: 'authorizationError',
               17: 'The field is not writable',
               18: 'The name is not consistent',
               50: 'Unknown Error',
               551: 'Network is unreachable',
               52: 'typeError',
               553: 'No Response From Device.Please Try Again',
               54: 'Not able to lock the device.Please Retry Again',
               55: 'Not able to unlock the device',
               96: 'InternalError',
               97: 'ip-port-community_not_passed',
               98: 'otherException',
               99: 'pysnmpException'}

host_status_dic = {
    0: 'No operation', 1: 'Firmware download', 2: 'Firmware upgrade', 3: 'Restore default config', 4: 'Flash commit',
    5: 'Reboot', 6: 'Site survey', 7: 'Calculate BW', 8: 'Uptime service', 9: 'Statistics gathering',
    10: 'Reconciliation', 11: 'Table reconciliation', 12: 'Set operation', 13: 'Live monitoring',
    14: 'Status capturing'}

time_diff = 0


class CCUDeviceList(object):
    """
    Device CCU device listing class
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
            if device_list_param == None:
                device_list_param = []
            return device_list_param
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def ccu_device_list(self, ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search,
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

    def ccu_device_list_profiling(self, ip_address, mac_address, selected_device):
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
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()


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


class CcuCommonSetValidation(object):
    """
    Device CCU related validation
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
            o1 = aliased(CcuOids)
            table_name = "CcuOids"
            o2 = aliased(CcuOids)
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
                                    depend_oid_value.append(
                                        {keys: [
                                            query_result[0][0].oid +
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
                                    CcuOids.table_name, CcuOids.coloumn_name).filter(
                                    and_(CcuOids.oid_name == i, CcuOids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                else:

                                    if i in dic_result:
                                        table_name = "ccu_" + \
                                                     oid_list_table_field_value[0][0]
                                        table_name = rename_tablename(
                                            table_name)
                                        exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                            table_name, table_name, device_param_list[3])
                                        exec "table_result[0].%s = '%s'" % (
                                            oid_list_table_field_value[0][1], dic_result[i])
                                        if ("ccu_" + oid_list_table_field_value[0][0]) == "odu100_ipConfigTable":
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
                            # errorStatus.has_key(i)
                            success_result["result"] = errorStatus.get(
                                i, 'unknown SNMP Error')

            if len(dependent_oid) > 0:
                for i in range(0, len(dependent_oid)):
                    query_admin_result = sqlalche_obj.session.query(CcuOids.oid, CcuOids.oid_type,
                                                                    CcuOids.indexes).filter(
                        CcuOids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                    if 'ru.ruConfTable.adminstate-1' in dependent_oid[i]:
                        admin_state = "ru.ruConfTable.adminstate"
                        query_admin_result = sqlalche_obj.session.query(
                            CcuOids.oid, CcuOids.oid_type, CcuOids.indexes).filter(
                            CcuOids.oid_name == "ru.ruConfTable.adminstate").one()
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
                                            CcuOids.table_name, CcuOids.coloumn_name).filter(
                                            and_(CcuOids.oid_name == i, CcuOids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:
                                                table_name = "ccu_" + \
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
                                    # errorStatus.has_key(result["result"][i])
                                    success_result["result"] = errorStatus.get(
                                        result["result"][i], 'Unknown SNMP Error')

                    elif 'ru.ipConfigTable.adminState-1' in dependent_oid[i]:
                        query_admin_result = sqlalche_obj.session.query(
                            CcuOids.oid, CcuOids.oid_type, CcuOids.indexes).filter(
                            CcuOids.oid_name == "ru.ipConfigTable.adminState").one()
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
                                            CcuOids.table_name, CcuOids.coloumn_name).filter(
                                            and_(CcuOids.oid_name == i, CcuOids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:
                                                table_name = "_" + \
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
                                    # errorStatus.has_key(result["result"][i])
                                    success_result["result"] = errorStatus.get(
                                        result["result"][i], 'Unknown SNMP Error')
                    elif 'ru.ra.raConfTable.raAdminState-1' in dependent_oid[i]:
                        query_admin_result = sqlalche_obj.session.query(
                            CcuOids.oid, CcuOids.oid_type, CcuOids.indexes).filter(
                            CcuOids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                        dic_admin_value = {"ru.ra.raConfTable.raAdminState": [query_admin_result[0]
                                                                              + query_admin_result[2],
                                                                              query_admin_result[1], '1']}
                        if len(query_admin_result) > 0:
                            result = pysnmp_set(dic_admin_value, device_param_list[
                                0], device_param_list[1], device_param_list[2])
                            if result["success"] == 0 or result["success"] == '0':
                                success_result["success"] = result["success"]
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        result[
                                            "result"][i] = errorStatus[result["result"][i]]
                                    else:
                                        oid_list_table_field_value = sqlalche_obj.session.query(
                                            CcuOids.table_name, CcuOids.coloumn_name).filter(
                                            and_(CcuOids.oid_name == i, CcuOids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:
                                                table_name = "ccu_" + \
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
                                    # errorStatus.has_key(result["result"][i])
                                    success_result["result"] = errorStatus.get(
                                        result["result"][i], 'Unknown SNMP Error')
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
                        result = pysnmp_seter(
                            depend_oid_value[i], device_param_list[0],
                            device_param_list[1], device_param_list[2])
                        print result
                        if result["success"] == 0 or result["success"] == '0':
                            for i in result["result"]:
                                if result["result"][i] != 0:
                                    result["result"][
                                        i] = errorStatus[result["result"][i]]
                                else:
                                    oid_list_table_field_value = sqlalche_obj.session.query(
                                        CcuOids.table_name, CcuOids.coloumn_name).filter(
                                        and_(CcuOids.oid_name == i, CcuOids.device_type_id == device_type_id)).all()
                                    if len(oid_list_table_field_value) == 0:
                                        continue
                                    else:
                                        if i in dic_result:
                                            sql_table_name = "_" + \
                                                             oid_list_table_field_value[
                                                                 0][0]

                                            tableName = "ccu_" + \
                                                        sql_table_name + "_id"
                                            table_name = rename_tablename(
                                                sql_table_name)
                                            print table_name
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
            obj_set = CcuCommonSetValidation()
            flag = 0
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            if dic_result["success"] == '0' or dic_result["success"] == 0:
                for keys in dic_result.iterkeys():
                    if keys == "success":
                        continue
                    else:
                        oid_list_min_max_value = sqlalche_obj.session.query(
                            CcuOids.min_value, CcuOids.max_value).filter(
                            and_(CcuOids.oid_name == keys, CcuOids.device_type_id == device_type_id)).all()
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
                    print dic_result
                    return dic_result
            else:
                sqlalche_obj.sql_alchemy_db_connection_close()
                return dic_result
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            dic_result["success"] = 1
            dic_result["result"] = str(e)
            print "hello"
            return str(e)

# obj = CcuCommonSetValidation()
# print obj.common_validation(90,'ccu',{'ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID': '12:21:32:21:23:26', 'ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID': '12:21:32:21:23:27', 'ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID': '12:21:32:21:23:21', 'ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID': '12:21:32:21:23:24', 'success': 0})
#
############################################### CCU Reconciliation #######


class CCUReconcilation(object):
    """
    CCU device reconciliation
    """
    def default_reconciliation_controller(self, host_id, device_type_id, table_prefix, current_time, created_by,
                                          is_reconciliation):
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param current_time:
        @param created_by:
        @param is_reconciliation:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        new_profile = Odu16ConfigProfiles(device_type_id, "CCU", "Master", None, datetime.now(
        ), None, datetime.now(), None, 0)  # pass the parameter.
        sqlalche_obj.session.add(new_profile)
        sqlalche_obj.session.flush()
        sqlalche_obj.session.refresh(new_profile)
        new_profile_id = new_profile.config_profile_id
        default_profile_id = sqlalche_obj.session.query(Odu16ConfigProfiles.config_profile_id) \
            .filter(and_(Odu16ConfigProfiles.device_type_id == device_type_id,
                         Odu16ConfigProfiles.config_profile_type_id == "Default")).all()
        default_id = default_profile_id[0].config_profile_id
        print default_id
        panel_data = sqlalche_obj.session.query(CcuBatteryPanelConfigTable).filter(
            CcuBatteryPanelConfigTable.config_profile_id == default_id).all()
        if len(panel_data) > 0:
            for i in range(0, len(panel_data)):
                ccu_panel_data_add = CcuBatteryPanelConfigTable(new_profile_id, panel_data[i].ccuBPCIndex,
                                                                panel_data[i].ccuBPCSiteBatteryCapacity, panel_data[i]
                    .ccuBPCSiteSolarPanelwP, panel_data[i].ccuBPCSiteSolarPanelCount, datetime.now())
                sqlalche_obj.session.add(ccu_panel_data_add)

        ccu_threshold_data = sqlalche_obj.session.query(CcuAlarmAndThresholdTable).filter(
            CcuAlarmAndThresholdTable.config_profile_id == default_id).all()
        if len(ccu_threshold_data) > 0:
            for i in range(0, len(ccu_threshold_data)):
                ccu_threshold_data_add = CcuAlarmAndThresholdTable(new_profile_id, ccu_threshold_data[i].ccuATIndex,
                                                                   ccu_threshold_data[i].ccuATHighTemperatureAlarm,
                                                                   ccu_threshold_data[i].ccuATPSMRequest,
                                                                   ccu_threshold_data[i]
                                                                   .ccuATSMPSMaxCurrentLimit,
                                                                   ccu_threshold_data[i].ccuATPeakLoadCurrent,
                                                                   ccu_threshold_data[i].ccuATLowVoltageDisconnectLevel)
                sqlalche_obj.session.add(ccu_threshold_data_add)

        ccu_aux_data = sqlalche_obj.session.query(CcuAuxIOTable).filter(
            CcuAuxIOTable.config_profile_id == default_id).all()
        if len(ccu_aux_data) > 0:
            for i in range(0, len(ccu_aux_data)):
                ccu_aux_data_add = CcuAuxIOTable(
                    new_profile_id, ccu_aux_data[
                        i].ccuAIIndex, ccu_aux_data[i].ccuAIExternalOutput1,
                    ccu_aux_data[i].ccuAIExternalOutput2, ccu_aux_data[
                        i].ccuAIExternalOutput3, ccu_aux_data[
                        i].ccuAIExternalInput1,
                    ccu_aux_data[i].ccuAIExternalInput2, ccu_aux_data[
                        i].ccuAIExternalInput3, ccu_aux_data[
                        i].ccuAIExternalInput1AlarmType,
                    ccu_aux_data[i].ccuAIExternalInput2AlarmType, ccu_aux_data[i].ccuAIExternalInput3AlarmType)
                sqlalche_obj.session.add(ccu_aux_data_add)

        ccu_peer_data = sqlalche_obj.session.query(CcuPeerInformationTable).filter(
            CcuPeerInformationTable.config_profile_id == default_id).all()

        if len(ccu_peer_data) > 0:
            for i in range(0, len(ccu_peer_data)):
                ccu_peer_data_add = CcuPeerInformationTable(
                    new_profile_id, ccu_peer_data[
                        i].ccuPIIndex, ccu_peer_data[i].ccuPIPeer1MACID,
                    ccu_peer_data[i].ccuPIPeer2MACID, ccu_peer_data[
                        i].ccuPIPeer3MACID,
                    ccu_peer_data[i].ccuPIPeer4MACID)
                sqlalche_obj.session.add(ccu_peer_data_add)
        ccu_site_data = sqlalche_obj.session.query(CcuSiteInformationTable).filter(
            CcuSiteInformationTable.config_profile_id == default_id).all()

        if len(ccu_site_data) > 0:
            for i in range(0, len(ccu_site_data)):
                ccu_site_data_add = CcuSiteInformationTable(
                    new_profile_id, ccu_site_data[i].ccuSITIndex, ccu_site_data[i].ccuSITSiteName)
                sqlalche_obj.session.add(ccu_site_data_add)

        ccu_control_data = sqlalche_obj.session.query(CcuControlTable).filter(
            CcuControlTable.config_profile_id == default_id).all()
        if len(ccu_control_data) > 0:
            for i in range(0, len(ccu_site_data)):
                ccu_control_data_add = CcuControlTable(
                    new_profile_id, ccu_control_data[i].ccuCTIndex,
                    ccu_control_data[i].ccuCTLoadTurnOff, ccu_control_data[
                        i].ccuCTSMPSCharging, ccu_control_data[
                        i].ccuCTRestoreDefault,
                    ccu_control_data[i].ccuCTCCUReset)
                sqlalche_obj.session.add(ccu_control_data_add)

        ccu_information_data_add = CcuInformationTable(host_id, 0, 0,
                                                       "", "CCUVNL0123456789", "000.000.000")
        sqlalche_obj.session.add(ccu_information_data_add)

        ccu_network_data_add = CcuNetworkConfigurationTable(
            host_id, 0, "00:00:00:00:00:00", "192.168.1.2", "255.255.255.0", "0.0.0.0", "", "255.255.255.0", "")
        sqlalche_obj.session.add(ccu_network_data_add)

        ccu_software_data_add = CcuSoftwareInformationTable(
            host_id, 0, "000.000.000", "000.000.000", "000.000.000", "000.000.000")
        sqlalche_obj.session.add(ccu_software_data_add)

        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(new_profile_id), 0

    #######################  Device Reconciliation with isReconciliation recon
    def time_diff_rec_table(self, table_oid_dic, current_time):
        """

        @param table_oid_dic:
        @param current_time:
        @return:
        """
        table_dic = {}
        global time_diff
        time_diff = 30
        fmt = '%Y-%m-%d %H:%M:%S'
        a = str(current_time)
        global time_delay
        for i in table_oid_dic:
            if i == "raChannelListTable":
                continue
            table_rec_time = table_oid_dic[i][1]

            diff1 = datetime.strptime(str(table_rec_time), fmt)

            diff2 = datetime.strptime(a[:a.find('.') - 1], fmt)
            rec_time = (diff2 - diff1)
            rec_time = divmod(rec_time.days * 86400 + rec_time.seconds, 60)
            if rec_time[0] < time_diff:
                if table_oid_dic[i][0] == 0:
                    table_dic.update({i: table_oid_dic[i][2]})
            else:
                table_dic.update({i: table_oid_dic[i][2]})
        time_delay = diff1

        return table_dic

    def update_reconcilation_controller(self, host_id, device_type, table_prefix, current_time, user_name):
        """

        @param host_id:
        @param device_type:
        @param table_prefix:
        @param current_time:
        @param user_name:
        @return:
        """
        global essential_obj, sqlalche_obj, host_status_dic, errorStatus
        host_status = 0
        host_data = []
        table_oid_dic = {}
        table_var_bind = {}
        rec_not_done = []
        rec_done = []
        total_rec = 0
        rec = 0
        rec_per = 0
        table_result = []
        time_stamp = str(datetime.now())
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(Hosts). \
                filter(Hosts.host_id == host_id).all()

            result = {'success': 0, 'result': ""}
            if host_id != None or host_id != "":
                host_op_status = essential_obj.get_hoststatus(host_id)

                if host_op_status != None or host_op_status != "":

                    if int(host_op_status) == 0:
                        essential_obj.host_status(host_id, 10)

                        if len(host_data) > 0:

                            ping_chk = snmp_ping(host_data[0].ip_address, host_data[
                                0].snmp_read_community, int(host_data[0].snmp_port))
                            if int(ping_chk) == 0:
                                host_data[0].reconcile_status = 1
                                sqlalche_obj.session.commit()
                                if device_type == "ccu":
                                    table_result = sqlalche_obj.session.query(
                                        CcuOidTable).filter(CcuOidTable.is_recon == 1).all()
                                if len(table_result) > 0:
                                    for i in range(0, len(table_result)):
                                        table_oid_dic.update(
                                            {table_result[
                                                 i].table_name: [table_result[i].status,
                                                                 table_result[i].timestamp, table_result[i].table_oid]})
                                        table_var_bind.update({table_result[i].table_name:
                                                                   table_result[i].varbinds})

                                    rec_table_dic = self.time_diff_rec_table(
                                        table_oid_dic, current_time)
                                    # print "",rec_table_dic
                                    if len(rec_table_dic) > 0:
                                        total_rec = len(rec_table_dic)
                                        # print total_rec
                                        obj_system_config = SystemConfig()
                                        for j in rec_table_dic:
                                            print j, "#####################"
                                            column_list = []
                                            tablename = str(
                                                table_prefix) + str(j)
                                            # print tablename,"\n\n\n"
                                            sqlalche_tablename = rename_tablename(
                                                "_" + j)
                                            # print
                                            # sqlalche_tablename,"\n\n\n\n"
                                            database_name = obj_system_config.get_sqlalchemy_credentials(
                                            )
                                            # print
                                            # database_name,"%%%%%%%%%%%%%%%%%%%%%%"
                                            result_db = sqlalche_obj.db.execute(
                                                "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'" % (
                                                tablename, database_name[4]))
                                            for columns in result_db:
                                                column_list.append(
                                                    columns["column_name"])

                                            # time.sleep(5)
                                            result = ccu_bulk(str(rec_table_dic[j]) + str(".1"),
                                                              host_data[0].ip_address, int(
                                                    host_data[0].snmp_port), host_data[0].snmp_read_community,
                                                              int(table_var_bind.get(j)))
                                            if result['success'] == 1:
                                                for key in result['result']:
                                                    if int(key) == 53:
                                                        result['result'] = errorStatus.get(
                                                            key, "UNMP Server is busy.Please try after some time,2000")
                                                        result['success'] = 1

                                                    elif int(key) == 51:
                                                        result['result'] = errorStatus.get(
                                                            key, "UNMP Server is busy.Please try after some time,2002")
                                                        result['success'] = 1
                                                        return
                                                    elif int(key) == 97 or int(key) == 98 or int(key) == 99 or int(
                                                            key) == 102:
                                                        result['result'] = errorStatus.get(
                                                            key, "UNMP Server is busy.Please try after some time,2002")
                                                        result['success'] = 1
                                                        return
                                                    elif int(key) == 5:
                                                        result['result'] = errorStatus.get(
                                                            key, "Device is busy.Please try again later")
                                                        result['success'] = 1
                                                        return
                                                    elif int(key) == 24 or int(key) == 72:
                                                        result['result'] = errorStatus.get(
                                                            key, "Device is busy.Please try again later")
                                                        result['success'] = 1
                                                        return
                                                    else:
                                                        if key in errorStatus:
                                                            result['result'] = errorStatus.get(
                                                                key,
                                                                "UNMP Server is busy.Please try after some time,2003")
                                                rec_not_done.append(str(j))
                                            else:
                                                if len(result['result']) == 0:
                                                    rec_done.append(str(j))
                                                    rec = rec + 1
                                                ##                                                    if "config_profile_id" in column_list:
                                                ##                                                        sqlalche_obj.db.execute("delete from %s where config_profile_id = '%s' "%(tablename,host_data[0].config_profile_id))
                                                ##                                                    else:
                                                # sqlalche_obj.db.execute("delete from %s where host_id = '%s'
                                                # "%(tablename,host_data[0].host_id))
                                                else:
                                                    rec_done.append(str(j))
                                                    rec = rec + 1
                                                    if "config_profile_id" in column_list:
                                                        sqlalche_table_result = sqlalche_obj.session.query(
                                                            eval(sqlalche_tablename)).filter(
                                                            getattr(eval(sqlalche_tablename), "config_profile_id") ==
                                                            host_data[0].config_profile_id).all()

                                                    else:
                                                        sqlalche_table_result = sqlalche_obj.session.query(
                                                            eval(sqlalche_tablename)).filter(
                                                            getattr(eval(sqlalche_tablename),
                                                                    "host_id") == host_id).all()
                                                    primary_key_id = tablename + \
                                                                     "_id"

                                                    column_list.remove(
                                                        primary_key_id)
                                                    if "config_profile_id" in column_list:
                                                        column_list.remove(
                                                            "config_profile_id")
                                                        config_type = 1
                                                    else:
                                                        column_list.remove(
                                                            "host_id")
                                                        config_type = 0
                                                    if "timestamp" in column_list:
                                                        column_list.remove(
                                                            "timestamp")

                                                        timestamp = 1
                                                    else:
                                                        timestamp = 0
                                                    if j == "raAclConfigTable" or j == "peerConfigTable":
                                                        sqlalche_obj.db.execute(
                                                            "delete from %s where config_profile_id = '%s' " % (
                                                            tablename, host_data[0].config_profile_id))
                                                        time.sleep(1)
                                                        for row in result['result']:
                                                            sqlalche_obj.db.execute(
                                                                "Insert into %s values(NULL,%s,%s)" % (
                                                                    tablename, host_data[0].config_profile_id,
                                                                    str(result["result"][row])[1:-1]))
                                                    else:
                                                        if len(sqlalche_table_result) > 0:
                                                            for row in result['result']:
                                                                if len(sqlalche_table_result) >= row:
                                                                    for val in range(0, len(result['result'][row])):
                                                                        setattr(
                                                                            sqlalche_table_result[row - 1],
                                                                            column_list[val],
                                                                            str(result['result'][row][val]))
                                                                        if timestamp == 1:
                                                                            setattr(sqlalche_table_result[row - 1],
                                                                                    "timestamp", time_stamp[
                                                                                                 :time_stamp.find(
                                                                                                     '.') - 1])

                                                                else:
                                                                    if config_type == 1:
                                                                        sqlalche_obj.db.execute(
                                                                            "Insert into %s values(NULL,%s,%s)" % (
                                                                                tablename,
                                                                                host_data[0].config_profile_id,
                                                                                str(result["result"][row])[1:-1]))
                                                                    else:
                                                                        if timestamp == 0:
                                                                            sqlalche_obj.db.execute(
                                                                                "Insert into %s values(NULL,%s,%s)" % (
                                                                                    tablename, host_id,
                                                                                    str(result["result"][row])[1:-1]))
                                                                        else:
                                                                            sqlalche_obj.db.execute(
                                                                                "Insert into %s values(NULL,%s,%s,'%s')" % (
                                                                                    tablename, host_id,
                                                                                    str(result["result"][row])[1:-1],
                                                                                    time_stamp[
                                                                                    :time_stamp.find('.') - 1]))
                                                        else:
                                                            for row in result['result']:
                                                                if config_type == 1:
                                                                    sqlalche_obj.db.execute(
                                                                        "Insert into %s values(NULL,%s,%s)" % (
                                                                            tablename, host_data[0].config_profile_id,
                                                                            str(result["result"][row])[1:-1]))
                                                                else:
                                                                    if timestamp == 0:
                                                                        sqlalche_obj.db.execute(
                                                                            "Insert into %s values(NULL,%s,%s)" % (
                                                                                tablename, host_id,
                                                                                str(result["result"][row])[1:-1]))
                                                                    else:
                                                                        sqlalche_obj.db.execute(
                                                                            "Insert into %s values(NULL,%s,%s,'%s')" % (
                                                                            tablename, host_id, str(
                                                                                result["result"][row])[1:-1],
                                                                            time_stamp[:time_stamp.find('.') - 1]))

                                        sqlalche_obj.db.execute(
                                            "Update ccu_oid_table set status = 0 where table_name in ('%s')" % (
                                            "\',\'".join(rec_not_done)))
                                        a = str(current_time)
                                        sqlalche_obj.db.execute(
                                            "Update ccu_oid_table set status = 1,timestamp='%s' where table_name in ('%s')" %
                                            (a[:a.find('.') - 1], "\',\'".join(rec_done)))
                                        rec_per = (
                                            float(rec) / float(total_rec))
                                        # print rec_per
                                        rec_per = int(rec_per * 100)
                                        host_data[0].reconcile_health = rec_per
                                        host_data[0].reconcile_status = 2
                                        sqlalche_obj.session.commit()
                                        el = EventLog()
                                        el.log_event(
                                            "Device Reconcilation Done", "%s" % (user_name))
                                        result = {"success": 0, "result":
                                            {rec_per: [host_data[0].host_alias, host_data[0].ip_address]}}
                                        return
                                    else:
                                        result = {'success': 1,
                                                  'result': " Reconciliation of device configuration data has been completed successfully %s You can reinitiate the process after %s minutes" % (
                                                  str(time_delay), str(time_diff))}
                                        return
                                else:
                                    result = {'success': 1, 'result':
                                        "UNMP Server is busy.Please try after some time,1200"}
                                    return
                            else:
                                if int(ping_chk) == 2:
                                    result = {
                                        'success': 1, 'result': "Network is unreachable"}
                                else:
                                    result = {'success': 1,
                                              'result': "Reconciliation not done.No response from device " + str(
                                                  host_data[0]
                                                  .host_alias) + "(" + str(host_data[0].ip_address + ")")}
                                return
                        else:
                            result = {'success': 1, 'result':
                                "UNMP Server is busy.Please try after some time,1100"}
                            return
                    else:
                        result = {'success': 1, 'result': "Device is busy, Device " + host_status_dic[
                            int(host_op_status)] + " is in progress. please wait ..."}
                        return
                else:
                    result = {'success': 1, 'result':
                        "UNMP Server is busy.Please try after some time,1000"}
                    return
            else:
                result = {'success': 1, 'result': "Host Not Exist"}
                return
        except Exception as e:
            result = {"success": 1, "result":
                "UNMP Server is busy.Please try after some time" + str(e)}
            return
        finally:
            essential_obj.host_status(host_id, 0, None, 10)
            if len(host_data) > 0:
                host_data[0].reconcile_status = 0
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

            sqlalche_obj.sql_alchemy_db_connection_close()


obj = CCUReconcilation()
# print obj.default_reconciliation_controller(89,"ccu","ccu_",datetime.now(),"",True)
# print obj.update_reconcilation_controller(92,'ccu','ccu_',datetime.now(),"")
# ccu_obj=CcuCommonSetValidation()
# print
# ccu_obj.common_validation('7','ccu',{'ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP':
# '123', 'ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount':
# '187', 'ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity':
# '123', 'success': 0})
