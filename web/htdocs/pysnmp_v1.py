import socket
import sys
# importing pysnmp library
import pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.api import v1
import time


def bulktable(oid, ip_address, port, community, max_value=10):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @param max_value:
    @return:
    """
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                oid = oid.strip('.')
                # print oid
                first_value = 0

                errorIndication, errorStatus, errorIndex, \
                varBindTable = cmdgen.CommandGenerator().bulkCmd(
                    cmdgen.CommunityData('bulk-agent', community, 0), cmdgen.UdpTransportTarget((ip_address, port)),
                    first_value, max_value, make_tuple(oid))

                var_dict = {}

                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[53] = str(errorIndication)
                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = errorStatus.prettyPrint()
                        print "int(errorIndex),str(errorStatus),int(errorStatus)", int(errorIndex), int(
                            errorStatus), str(errorStatus)
                        success = 1
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        print
                        print oid
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                # print '%s = %s' % (name.prettyPrint(),
                                # val.prettyPrint())
                                temp_split = name.prettyPrint().split(oid)
                                if len(temp_split) > 1:
                                    pass
                                else:
                                    return
                                    # print name.prettyPrint()
                                oid_values_list = name.prettyPrint(
                                ).split(oid)[1].strip('.').split('.')
                                print oid_values_list
                                if len(oid_values_list) > 0:
                                    oid_no = oid_values_list.pop(0)
                                else:
                                    success = 1
                                    return
                                if isinstance(val, v1.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = str(
                                        val)  # val.prettyPrint() #str(val)
                                if oid_li.count(oid_no) == 0:
                                    oid_li.append(oid_no)
                                    count = 0
                                    flag = 1
                                    if len(oid_li) == 1:
                                        flag = 0

                                if flag == 0:
                                    count += 1
                                    li = []
                                    # oid_values_list.pop(0)
                                    print oid_values_list
                                    for i in oid_values_list:
                                        li.append(i)
                                        # print " li ",li
                                    li.append(value)
                                    # print " li 2",li
                                    var_dict[count] = li
                                    # print var_dict
                                else:
                                    count += 1
                                    li = var_dict[count]
                                    li.append(value)
                                    var_dict[count] = li
                                    # print li,count
                                    # print "li,count",li,count,var_dict,oid_li

            except socket.error as sock_err:
                success = 1
                err_dict[51] = str(sock_err)
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err ' + str(err)
            except Exception as e:
                success = 1
                err_dict[99] = 'pysnmp exception ' + str(e)

        else:
            success = 1
            err_dict[
                96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"
    except Exception as e:
        success = 1
        err_dict[98] = 'outer Exception ' + str(e)
    finally:
        result_dict = {}
        if success == 0:
            result_dict['success'] = success
            result_dict['result'] = var_dict
        else:
            result_dict['success'] = success
            result_dict['result'] = err_dict
        return result_dict


def pysnmp_get_table(oid, ip_address, port, community, extra=0):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @param extra:
    @return:
    """
    err_dict = {}
    success = 1
    timeout = 5
    retries = 3
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                oid = oid.strip('.')
                errorIndication, errorStatus, errorIndex, \
                varBindTable = cmdgen.CommandGenerator().nextCmd(
                    cmdgen.CommunityData('table1-agent', community, 0),
                    cmdgen.UdpTransportTarget((ip_address, port), timeout, retries), make_tuple(oid))

                var_dict = {}

                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[53] = str(errorIndication)
                    return
                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = str(errorStatus)
                        success = 1
                        # print '%s at %s\n' % (
                        # errorStatus.prettyPrint(),errorIndex and
                        # varBindTable[-1][int(errorIndex)-1] or '?')
                        return
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        oid_values_list = []
                        # print varBindTable
                        # print
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                # print '%s = %s' % (name.prettyPrint(),
                                # val.prettyPrint())
                                oid_values_list = name.prettyPrint(
                                ).split(oid)[1].strip('.').split('.')
                                if len(oid_values_list) > 0:
                                    oid_no = oid_values_list.pop(0)
                                else:
                                    success = 1
                                    return
                                if isinstance(val, v1.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = str(
                                        val)  # val.prettyPrint() #str(val)
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

            except socket.error as sock_err:
                success = 1
                err_dict[51] = str(sock_err)
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err ' + str(err)
            except Exception as e:
                success = 1
                err_dict[99] = 'pysnmp exception ' + str(e)
        else:
            success = 1
            err_dict[
                96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"
    except Exception as e:
        success = 1
        err_dict[98] = 'outer Exception ' + str(e)
    finally:
        result_dict = {}
        if success == 0:
            result_dict['success'] = success
            result_dict['result'] = var_dict
        else:
            result_dict['success'] = success
            result_dict['result'] = err_dict
        return result_dict

# print pysnmp_get_table('1.3.6.1.4.1.26149.2.2.13.11.1', '172.22.0.102', 161, 'public')
# print pysnmp_get_table('1.3.6.1.4.1.26149.2.2.13.9.1.1', '172.22.0.102', 161, 'public')
# print pysnmp_get_table('1.3.6.1.4.1.26149.2.1.2.2.1', '172.22.0.104',
# 8001, 'public')


def pysnmp_get_node(oid, ip_address, port, community):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    err_dict = {}
    success = 1
    var_dict = {}
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

                errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator(
                ).nextCmd(cmdgen.CommunityData('table-v1-agent', community, 0),
                          cmdgen.UdpTransportTarget((ip_address, port)), make_tuple(oid))
                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[53] = str(errorIndication)
                    return
                    # handle

                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = str(errorStatus)
                        success = 1

                        # print '%s at %s\n' % (
                        # errorStatus.prettyPrint(),errorIndex and
                        # varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                # print '%s = %s' % (name.prettyPrint(),
                                # val.prettyPrint())
                                oid_no = name.prettyPrint(
                                ).split(oid)[1][1:].split('.')[0]

                                if oid_li.count(oid_no) == 0:
                                    oid_li.append(oid_no)
                                    count = 0
                                    flag = 1
                                    if len(oid_li) == 1:
                                        flag = 0

                                if isinstance(val, v1.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = str(
                                        val)  # val.prettyPrint() #str(val)

                                if flag == 0:
                                    count += 1
                                    li = []
                                    li.append(value)
                                    var_dict[count] = li
                                else:
                                    count += 1
                                    li = var_dict[count]
                                    li.append(value)
                                    var_dict[count] = li

            except socket.error as sock_err:
                success = 1
                err_dict[51] = str(sock_err)
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err ' + str(err)
            except Exception as e:
                success = 1
                err_dict[99] = 'pysnmp exception ' + str(e)
        else:
            success = 1
            err_dict[
                96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"
    except Exception as e:
        success = 1
        err_dict[98] = 'outer Exception ' + str(e)
    finally:
        result_dict = {}
        if success == 0:
            result_dict['success'] = success
            result_dict['result'] = var_dict
        else:
            result_dict['success'] = success
            result_dict['result'] = err_dict
        return result_dict

# print pysnmp_get_table('1.3.6.1.4.1.26149.10.2.3.4.2.1.1',
# '172.22.0.101', 161, 'public')

# print pysnmp_get_node('1.3.6.1.4.1.26149.2.2.13.11.1', '172.22.0.102',
# 161, 'public')

# print pysnmp_get_node('1.3.6.1.4.1.26149.10.2.2', '172.22.0.101', 161,
# 'public')


def single_set(ip_address, port, community, received_list):
    """

    @param ip_address:
    @param port:
    @param community:
    @param received_list:
    @return:
    """
    try:
        make_tuple = lambda x: tuple(int(i) for i in x.split(
            '.'))  # @note: this lambda function used to convert a oid string to oid tuple (in a format required by pysnmp)
        success = 0
        if isinstance(ip_address, str) and isinstance(community, str) and port != None and len(received_list) == 3:
            datatypes_dict = {'Integer': v1.Integer, 'OctetString': v1.OctetString, 'DisplayString': v1.OctetString,
                              'Gauge':
                                  v1.Gauge, 'IpAddress': v1.IpAddress, 'Counter': v1.Counter}

            response_dict = {}

            oid_str, datatype, value = received_list

            snmp_args = [cmdgen.CommunityData('single-v1-set', community, 0),
                         cmdgen.UdpTransportTarget((ip_address, int(port))),
            ]

            cmdClass = cmdgen.CommandGenerator().setCmd

            snmp_args.append(
                (make_tuple(oid_str), datatypes_dict[datatype](value)))
            # print snmp_args
            try:

                errorIndication, errorStatus, errorIndex, varBinds = cmdClass(
                    *snmp_args)

                if errorIndication:
                    success = 1
                    response_dict[53] = str(errorIndication)
                    return
                else:
                    if errorStatus > 0 and errorIndex != None:
                        success = 1
                        response_dict[str(
                            errorStatus)] = errorStatus.prettyPrint()
                        return

                    elif errorStatus == 0:
                        # print " no error >>>>>>>>>"
                        # response_dict[0] = 'all_field_set_sucessfully'
                        for name, val in varBinds:
                            response_dict[oid_str] = str(val)
                        return

            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[51] = sock_errstr
            except pysnmp.proto.error.ProtocolError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'type err ' + str(err)
            except Exception as e:
                response_dict = {}
                success = 1
                response_dict[99] = 'pysnmp exception ' + str(e)
        else:
            response_dict = {}
            success = 1
            response_dict[97] = 'IP or Port or community not present'
    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer err ' + str(e)
    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success
        final_responce_dict['result'] = response_dict
        return final_responce_dict


# print single_set('172.22.0.101',161,'private',['1.3.6.1.4.1.26149.10.2.3.1.2.0','Integer32',2])
# print single_set('172.22.0.101',161,'private',['1.3.6.1.4.1.26149.10.2.3.2.1.0','OctetString','snuj1234'])
# print
# pysnmp_get_table('1.3.6.1.4.1.26149.10.2.3.4.2.1.1','172.22.0.101',161,'private')

# print single_set('172.22.0.101',
# 161,'private',['1.3.6.1.4.1.26149.10.2.3.4.1.1.0','Integer32',1])

def pysnmp_get(oid, ip_address, port, community):
    # not to pass at the end .1 in oid
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    success = 0
    response_dict = {}
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

                errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator(
                ).nextCmd(cmdgen.CommunityData('getv1-agent', community, 0),
                          cmdgen.UdpTransportTarget((ip_address, port)), make_tuple(oid))
                if errorIndication:
                    response_dict[53] = str(errorIndication)
                    success = 1
                    return
                else:
                    if errorStatus > 0 and errorIndex != None:
                        response_dict[oid_str] = int(errorIndex)
                        return
                    elif errorStatus == 0:
                        # print varBindTable
                        if len(varBindTable) < 1:
                            success = 1
                            response_dict[
                                102] = 'NO VALUE ASSOCIATED WITH OID FOR SNMP GET'
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                if isinstance(val, v1.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = str(
                                        val)  # val.prettyPrint() #str(val)
                                response_dict[oid] = value

            except socket.error as err:
                response_dict = {}
                success = 1
                response_dict[51] = str(err)
            except pysnmp.proto.error.ProtocolError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'type err ' + str(err)
            except Exception as e:
                response_dict = {}
                success = 1
                response_dict[99] = 'pysnmp err ' + str(e)
        else:
            response_dict = {}
            success = 1
            response_dict[
                96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"

    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer ' + str(e)

    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success
        final_responce_dict['result'] = response_dict
        return final_responce_dict

# print pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.7', '172.22.0.102', 161,
# 'public')


def pysnmp_seter(received_dict={}, ip_address=None, port=None, community=None, admin_state={}, is_recursive=0,
                 response_dict={}, temp_dict={}, error_dict={}, state=0):
    """










    @param received_dict:
    @param ip_address:
    @param port:
    @param community:
    @param admin_state:
    @param is_recursive:
    @param response_dict:
    @param temp_dict:
    @param error_dict:
    @param state:
    @requires: {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)} , ip address, port, community, if admin_state dependency present then pass admin_state as dictionary         {'admin_state':(oid_str,datatype,value)}

    @return: {'success': 0/1, result : {'fullName_of_field':('if successful then 0 if not then 1','error_number_if any otherwise 0')} }

    @rtype: Dictionary

    @author: Rahul Gautam

    @since: 11-sep-2011

    @date: 16-Sep-2011

    @version: 1.1

    @note: pysnmp_set is a recursive function that used to set the values for corresponding oids passed to
        it as a dictionary variable received_dict  {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)},
        and it return its response in another dictionary variable response_dict {'fullName_of_field':('if successful then 0 if not then 1','error_number_if any otherwise 0')}
        it handles all the errors related to snmp and some others like Neteork_Unreachable etc.

    @organization: CodeScape Consultants Pvt. Ltd.

    @copyright: 2011 Rahul Gautam for CodeScape Consultants Pvt. Ltd.

    @note: "in best case it sends only one packet of snmp set, if any of the value of that snmp set gives error function removes that and resends the packet,
        so as the worst case when error occur in linear manner of each field of received _dict in snmp set then it send requests = length(received_dict)
        but thats the worst case In average case it is far more better than any linear or iterator function
        its recursive nature gives it a true optimisation in terms of network traffic."

    """
    try:
        make_tuple = lambda x: tuple(int(i) for i in x.split(
            '.'))  # @note: this lambda function used to convert a oid string to oid tuple (in a format required by pysnmp)
        success = 0
        state_present = 0
        aoid_tuple = None
        aoid_str = None
        snmp_args = None
        datatypes_dict = {
            'Integer': v1.Integer, 'Integer32': v1.Integer, 'OctetString': v1.OctetString,
            'DisplayString': v1.OctetString, 'Gauge': v1.Gauge, 'IpAddress': v1.IpAddress, 'Counter': v1.Counter}
        if is_recursive:
            print " **** recursive \n", port
            is_recursive = 0
            snmp_args = [cmdgen.CommunityData('v1-seter', community, 0),
                         cmdgen.UdpTransportTarget((ip_address, int(port))),
            ]
            cmdClass = cmdgen.CommandGenerator().setCmd

            if len(admin_state) > 0:
                state_present = 1
                admin_name = admin_state.keys()[0]
                oid_str, datatype, value = admin_state.values()[0]
                aoid_tuple = make_tuple(oid_str)
                # temp_dict[aoid_tuple] = admin_name
                snmp_args.append((aoid_tuple, datatypes_dict[datatype](value)))

            for i in received_dict.keys():
                oid_str, datatype, value = received_dict[i]
                oid_tuple = make_tuple(oid_str)
                if oid_tuple in error_dict:
                    pass
                else:
                    snmp_args.append(
                        (oid_tuple, datatypes_dict[datatype](value)))

            try:

                errorIndication, errorStatus, errorIndex, varBinds = cmdClass(
                    *snmp_args)

                if errorIndication:
                    response_dict[53] = str(errorIndication)
                    return

                else:
                    print "errorStatus ", errorStatus, " errorIndex ", errorIndex
                    if errorStatus > 0 and errorIndex != None:
                        first_varBind = varBinds[int(errorIndex) - 1][0]
                        if first_varBind == aoid_str:
                            success = 1
                            response_dict[
                                54] = "NOT ABLE TO SET FIRST DEFIND VALUE"
                            return
                        else:
                            state = 0
                            response_dict[
                                temp_dict[first_varBind]] = int(errorIndex)
                            print " >>> ", first_varBind, aoid_str, "\n"
                            error_dict[first_varBind] = 1

                        if len(error_dict) >= len(received_dict):
                            success = 1
                            return
                        else:
                            is_recursive = 1
                            # print " ***********
                            # ",error_dict,response_dict,temp_dict
                            return pysnmp_seter(received_dict, ip_address, port, community, admin_state, is_recursive,
                                                response_dict, temp_dict, error_dict, state)

                    elif errorStatus == 0:
                        for name, val in varBinds:
                            response_dict[temp_dict[name]] = 0
                        return

            except socket.error as err:
                response_dict = {}
                success = 1
                response_dict[51] = str(err)
            except pysnmp.proto.error.ProtocolError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'pyproto ' + str(err)
            except TypeError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'type err ' + str(err)
            except Exception as e:
                response_dict = {}
                success = 1
                response_dict[99] = 'pysnmp exception ' + str(e)

        else:
            if ip_address != None and port != None and community != None:

                response_dict = {}
                temp_dict = {}
                state_present = 0
                snmp_args = [cmdgen.CommunityData('v1-seter', community, 0),
                             cmdgen.UdpTransportTarget(
                                 (ip_address, int(port))),
                ]

                cmdClass = cmdgen.CommandGenerator().setCmd

                if len(admin_state) > 0:
                    state_present = 1
                    admin_name = admin_state.keys()[0]
                    aoid_str, datatype, value = admin_state.values()[0]
                    aoid_tuple = make_tuple(aoid_str)
                    temp_dict[aoid_tuple] = admin_name
                    snmp_args.append(
                        (aoid_tuple, datatypes_dict[datatype](value)))

                for i in received_dict.keys():
                    oid_str, datatype, value = received_dict[i]
                    oid_tuple = make_tuple(oid_str)
                    temp_dict[oid_tuple] = i
                    snmp_args.append(
                        (oid_tuple, datatypes_dict[datatype](value)))

                # print " snmp arguments ",snmp_args
                try:
                    errorIndication, errorStatus, errorIndex, varBinds = cmdClass(
                        *snmp_args)

                    if errorIndication:
                        response_dict[53] = str(errorIndication)
                        success = 1
                        return
                    else:
                        if errorStatus > 0 and errorIndex != None:
                            first_varBind = varBinds[int(errorIndex) - 1][0]
                            print first_varBind, " ::: ", aoid_tuple
                            if first_varBind == aoid_tuple:
                                success = 1
                                response_dict[
                                    54] = "NOT ABLE TO SET FIRST DEFIND VALUE"
                                return
                            else:
                                response_dict[
                                    temp_dict[first_varBind]] = int(errorStatus)
                                error_dict[first_varBind] = 1

                                if len(error_dict) >= len(received_dict):
                                    success = 1
                                    return
                                else:
                                    is_recursive = 1
                                    print "errorStatus ", errorStatus, " errorIndex ", errorIndex
                                    return pysnmp_seter(received_dict, ip_address, port, community, admin_state,
                                                        is_recursive, response_dict, temp_dict, error_dict)
                            return

                        elif errorStatus == 0:
                            # response_dict[0] = 'all_field_set_sucessfully'
                            for name, val in varBinds:
                                response_dict[temp_dict[name]] = 0
                            return

                except socket.error as (sock_errno, sock_errstr):
                    response_dict = {}
                    success = 1
                    response_dict[51] = sock_errstr
                except pysnmp.proto.error.ProtocolError as err:
                    response_dict = {}
                    success = 1
                    response_dict[99] = 'pyproto ' + str(err)
                except TypeError as err:
                    response_dict = {}
                    success = 1
                    response_dict[99] = 'type err ' + str(err)
                except Exception as e:
                    response_dict = {}
                    success = 1
                    response_dict[99] = 'pysnmp exception ' + str(e)

            else:
                response_dict = {}
                success = 1
                response_dict[97] = 'IP or Port or community not present'
    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer ' + str(e)
    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success
        final_responce_dict['result'] = response_dict
        print " response_dict ", response_dict
        return final_responce_dict
        # sys.exit(1)

# di = {'sv':['1.3.6.1.4.1.26149.10.2.3.1.2.0','Integer32','1']}
# d = {'vapssid':['1.3.6.1.4.1.26149.10.2.3.2.1.0','OctetString','ssidset'],
#     'vab':['1.3.6.1.4.1.26149.10.2.3.2.5.0','OctetString',180]}
# ss = {'radioSetup.radioAPmode': ['1.3.6.1.4.1.26149.10.2.2.2.0', 'Integer32', '5']}
# print pysnmp_seter(d, '172.22.0.101', 161, 'private')


def snmp_ping(ip_address_str, community, port):
    """

    @param ip_address_str:
    @param community:
    @param port:
    @return:
    """
    try:
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
            # SNMP v2
            cmdgen.CommunityData('test-agent', community, 0),
            cmdgen.UdpTransportTarget((ip_address_str, port)),
            # Plain OID
            (1, 3, 6, 1, 2, 1, 1, 1, 0),
        )
        if errorIndication:
            return 1
        else:
            if errorStatus:
                return 1
            else:
                return 0
    except socket.error as sock_errstr:
        return 2
    except Exception as e:
        return 3
