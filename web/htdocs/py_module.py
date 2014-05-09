"""
@author: Rahul Gautam

@since: 11-Sep-2011

@note: A complete set of SNMP functions (like set,walk,bulkGet,get,getNext) for UNMP using pysnmp library, with proper error handling

@organization: CodeScape Consultants Pvt. Ltd.

@copyright: 2011 Rahul Gautam for CodeScape Consultants Pvt. Ltd.
"""

import socket
# importing pysnmp library
import pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.api import v2c


def pysnmp_get_acltable(oid, ip_address, port, community):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

                errorIndication, errorStatus, errorIndex, \
                varBindTable = cmdgen.CommandGenerator().nextCmd(
                    cmdgen.CommunityData('table-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                    make_tuple(oid))

                var_dict = {}

                if errorIndication:
                    success = 1
                    err_dict[553] = str(errorIndication)
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
                                oid_values_list = []
                                for i in range(1, 4):
                                    oid_values_list.append(
                                        name.prettyPrint().split('.')[-i])
                                oid3, oid2, oid_no = oid_values_list
                                if oid_li.count(oid_no) == 0:
                                    oid_li.append(oid_no)
                                    count = 0
                                    flag = 1
                                    if len(oid_li) == 1:
                                        flag = 0

                                if flag == 0:
                                    count += 1
                                    li = []
                                    value = str(
                                        val)  # val.prettyPrint() #str(val)
                                    li.append(oid2)
                                    li.append(oid3)
                                    li.append(value)
                                    var_dict[count] = li
                                else:
                                    count += 1
                                    li = var_dict[count]
                                    value = str(
                                        val)  # val.prettyPrint() #str(val)
                                    li.append(value)
                                    var_dict[count] = li

            except socket.error as (sock_errno, sock_errstr):
                success = 1
                err_dict[551] = sock_errstr
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


def pysnmp_peer_reconcile(oid, ip_address, port, community):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

                errorIndication, errorStatus, errorIndex, \
                varBindTable = cmdgen.CommandGenerator().nextCmd(
                    cmdgen.CommunityData('pysnmp-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                    make_tuple(oid))

                var_dict = {}

                if errorIndication:
                    success = 1
                    err_dict[553] = str(errorIndication)
                    # handle
                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = str(errorStatus)
                        success = 1
                        # print '%s at %s\n' % (
                        # errorStatus.prettyPrint(),errorIndex and
                        # varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        for varBindTableRow in varBindTable:
                            success = 0
                            for name, val in varBindTableRow:
                                oid_no = int(name.prettyPrint().split('.')[-1])
                                if oid_no in var_dict:
                                    li = var_dict[oid_no]
                                    li.append(str(val))
                                    var_dict[oid_no] = li
                                else:
                                    li = []
                                    li.append(str(val))
                                    var_dict[oid_no] = li
                                    # print '%s = %s' % (name.prettyPrint(),
                                    # val.prettyPrint())

            except socket.error as (sock_errno, sock_errstr):
                success = 1
                err_dict[551] = sock_errstr
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


# print pysnmp_peer_reconcile('1.3.6.1.4.1.26149.2.2.13.9.1',
# '172.22.0.102', 161, 'public')

# print
# pysnmp_peer_reconcile('1.3.6.1.4.1.26149.2.2.13.5','172.22.0.102',161,'public')


def pysnmp_get_table(oid, ip_address, port, community):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

                errorIndication, errorStatus, errorIndex, \
                varBindTable = cmdgen.CommandGenerator().nextCmd(
                    cmdgen.CommunityData('table-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                    make_tuple(oid))

                var_dict = {}

                if errorIndication:
                    success = 1
                    err_dict[553] = str(errorIndication)
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
                        for varBindTableRow in varBindTable:
                            success = 0
                            for name, val in varBindTableRow:
                                oid_no = int(name.prettyPrint().split('.')[-1])
                                # print oid_no
                                if oid_no in var_dict:
                                    li = var_dict[oid_no]
                                    if isinstance(val, v2c.IpAddress):
                                        value = str(val.prettyPrint())
                                    else:
                                        value = str(
                                            val)  # val.prettyPrint() #str(val)
                                    li.append(value)
                                    var_dict[oid_no] = li
                                else:
                                    li = []
                                    if isinstance(val, v2c.IpAddress):
                                        value = str(val.prettyPrint())
                                    else:
                                        value = str(
                                            val)  # val.prettyPrint() #str(val)
                                    li.append(value)
                                    var_dict[oid_no] = li
                                    # print '%s = %s' % (name.prettyPrint(),
                                    # val.prettyPrint())

            except socket.error as (sock_errno, sock_errstr):
                success = 1
                err_dict[551] = sock_errstr
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

# print pysnmp_get_table('1.3.6.1.4.1.26149.2.2.13.7.4', '172.22.0.102', 161, 'public')
#############


def pysnmp_demo_table(oid, ip_address, port, community):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

                errorIndication, errorStatus, errorIndex, \
                varBindTable = cmdgen.CommandGenerator().nextCmd(
                    cmdgen.CommunityData('table-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                    make_tuple(oid))

                var_dict = {}

                if errorIndication:
                    success = 1
                    err_dict[553] = str(errorIndication)
                    # handle
                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = str(errorStatus)
                        success = 1
                        # print '%s at %s\n' % (
                        # errorStatus.prettyPrint(),errorIndex and
                        # varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        num = 1
                        for varBindTableRow in varBindTable:
                            success = 0
                            for name, val in varBindTableRow:
                                oid_no = int(name.prettyPrint()[-1:])
                                if oid_no in var_dict:
                                    li = var_dict[oid_no]
                                    li.append(str(val))
                                    var_dict[oid_no] = li
                                else:
                                    li = []
                                    li.append(str(val))
                                    var_dict[oid_no] = li
                                    # print '%s = %s' % (name.prettyPrint(),
                                    # val.prettyPrint())

            except socket.error as (sock_errno, sock_errstr):
                success = 1
                err_dict[551] = sock_errstr
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

############

# print
# pysnmp_get_table('1.3.6.1.4.1.26149.2.1.6.3','172.22.0.104',8001,'public')


def pysnmp_acl_reconcile(oid, ip_address, port, community):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    err_dict = {}
    no_acl = 1
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

                errorIndication, errorStatus, errorIndex, \
                varBindTable = cmdgen.CommandGenerator().nextCmd(
                    cmdgen.CommunityData('pysnmp-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                    make_tuple(oid))

                row_dict = {}
                mac_dict = {}

                if errorIndication:
                    err_dict[553] = str(errorIndication)
                    # success = 1
                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = str(errorStatus)
                        print '%s at %s\n' % (
                            errorStatus.prettyPrint(),
                            errorIndex and varBindTable[
                                -1][int(errorIndex) - 1] or '?'
                        )
                    else:
                        flag = 0
                        no_acl = 0
                        for varBindTableRow in varBindTable:
                            no_acl = 0
                            for name, val in varBindTableRow:
                                if flag == 0:
                                    mac_oid = '.'.join(
                                        name.prettyPrint().split('.')[:-1])
                                    flag = 1
                                if name.prettyPrint().find(mac_oid) == -1:
                                    row_dict[int(name.prettyPrint(
                                    ).split('.')[-1])] = val.prettyPrint()
                                else:
                                    mac_dict[int(name.prettyPrint(
                                    ).split('.')[-1])] = str(val)
                                print '%s = %s' % (name.prettyPrint(), val.prettyPrint())

            except socket.error as (sock_errno, sock_errstr):
                success = 1
                err_dict[551] = sock_errstr
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
            err_dict[
                96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"
    except Exception, e:
        success = 1
        err_dict[98] = 'outer Exception ' + str(e)
    finally:
        result_dict = {}
        if len(err_dict) > 0:
            result_dict['err'] = err_dict
        elif len(mac_dict) > 0 and len(row_dict) > 0:
            result_dict['mac'] = mac_dict
            result_dict['row'] = row_dict
        elif no_acl == 0:
            result_dict['mac'] = mac_dict
            result_dict['row'] = row_dict
        else:
            result_dict['err'] = {102: 'Unknown'}
        return result_dict

# print
# pysnmp_acl_reconcile('1.3.6.1.4.1.26149.2.2.13.5','172.22.0.102',161,'public')


def pysnmp_reconcile(received_dict={}, ip_address=None, port=None, community=None):
    """

    @param received_dict:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    try:
        make_pystr = lambda x: ','.join(x.split('.'))
        make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
        success = 0
        ## outer if start
        if ip_address != None and port != None and community != None:
            response_dict = {}
            prev_str = None
            error_dict = {}
            state = 0
            temp_dict = {}
            prev_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('unmp-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s))" % (
                community, ip_address, port)
            state_present = 0
            get_str = prev_str
            for i in received_dict.keys():
                oid_str = received_dict[i]
                oid_pystr = make_pystr(oid_str)
                oid_tuple = make_tuple(oid_str)
                temp_dict[oid_tuple] = i
                get_str = get_str + ",(%s)" % oid_pystr
            get_str = get_str + ')'
            print " ###   PYSNMP GET PACKET   #### ", get_str
            try:

                exec get_str in locals(), globals()

                print " execution done "

                if errorIndication:
                    response_dict[553] = str(errorIndication)
                    success = 1
                    return

                else:
                    if errorStatus > 0 and errorIndex != None:

                        print " >>>>>>>>>>>>>>>> YE LE RAHA HAI MERI JAN BHAI ", varBinds[int(errorIndex) - 1]
                        error_dict[varBinds[int(errorIndex) - 1][0]] = 1

                        return

                    elif errorStatus == 0:
                        print " all  SET or GET  sucessful  >>>>>>>>>"

                        for name, val in varBinds:
                            # print ' ok %s = %s '%(name,val.prettyPrint())
                            if val != '' and val != None and val != ' ' and str(val).find(
                                    'populated') < 1:   # if needed put that and val != 'No Such Instance currently exists at this OID'
                                if isinstance(val, v2c.IpAddress):
                                    response_dict[
                                        temp_dict[name]] = str(val.prettyPrint())
                                else:
                                    response_dict[temp_dict[name]] = str(
                                        val)  # val.prettyPrint() #str(val)
                        return

            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[551] = sock_errstr
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

        # outer elif

        else:
            response_dict = {}
            success = 1
            response_dict[
                96] = 'arguments are missing'  # ' internal error prev_Str not passed'

    # outer exception
    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer ' + str(e)
    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success
        final_responce_dict['result'] = response_dict
        print " final_responce_dict ", final_responce_dict
        return final_responce_dict


def pysnmp_geter(received_dict={}, ip_address=None, port=None, community=None, prev_str=None, response_dict={},
                 temp_dict={}, error_dict={}, state=0):
    """

    @param received_dict:
    @param ip_address:
    @param port:
    @param community:
    @param prev_str:
    @param response_dict:
    @param temp_dict:
    @param error_dict:
    @param state:
    @return:
    """
    try:
        make_pystr = lambda x: ','.join(x.split('.'))
        make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
        success = 0
        ## outer if start
        if ip_address != None and port != None and community != None:
            response_dict = {}
            prev_str = None
            error_dict = {}
            state = 0
            temp_dict = {}
            prev_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('unmp-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s))" % (
                community, ip_address, port)
            state_present = 0
            get_str = prev_str
            for i in received_dict.keys():
                oid_str = received_dict[i]
                oid_pystr = make_pystr(oid_str)
                oid_tuple = make_tuple(oid_str)
                temp_dict[oid_tuple] = i
                get_str = get_str + ",(%s)" % oid_pystr
            get_str = get_str + ')'
            print " ###   PYSNMP GET PACKET   #### ", get_str
            try:

                exec get_str in locals(), globals()

                if errorIndication:
                    response_dict[553] = str(errorIndication)
                    success = 1
                    return

                else:
                    if errorStatus > 0 and errorIndex != None:

                        error_dict[varBinds[int(errorIndex) - 1][0]] = -1

                        return pysnmp_geter(received_dict, None, None, None, prev_str, response_dict, temp_dict,
                                            error_dict)

                    elif errorStatus == 0:
                        print " all  SET or GET  sucessful  >>>>>>>>>"

                        for name, val in varBinds:
                            # print ' ok %s = %s '%(name,val.prettyPrint())
                            if val != '' and val != None and val != ' ' and str(val).find(
                                    'populated') < 1:   # if needed put that and val != 'No Such Instance currently exists at this OID'
                                if isinstance(val, v2c.IpAddress):
                                    response_dict[
                                        temp_dict[name]] = str(val.prettyPrint())
                                else:
                                    response_dict[temp_dict[name]] = str(
                                        val)  # val.prettyPrint() #str(val)
                        return

            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[551] = sock_errstr
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

        # outer elif
        elif ip_address == None and port == None and community == None:

            if prev_str != '':
                print " recursive >>>>>>>>>>>>>>>> "
                get_str = prev_str
                # print "debug 1"

                for i in received_dict.keys():
                    oid_str = received_dict[i]
                    oid_pystr = make_pystr(oid_str)
                    oid_tuple = make_tuple(oid_str)
                    if oid_tuple in error_dict:
                        pass
                    else:
                        get_str = get_str + ",(%s)" % (oid_pystr)

                get_str = get_str + ')'
                print get_str

                try:

                    exec get_str in locals(), globals()
                    print " execution complete ", response_dict
                    if errorIndication:
                        response_dict[553] = str(errorIndication)
                        success = 1
                        return

                    else:
                        if errorStatus > 0 and errorIndex != None:
                            state = 0
                            error_dict[varBinds[int(errorIndex) - 1][0]] = -1
                            return pysnmp_geter(received_dict, None, None, None, prev_str, response_dict, temp_dict,
                                                error_dict, state)

                        elif errorStatus == 0:
                            for name, val in varBinds:
                                if val != '' and val != None and val != ' ' and str(val).find(
                                        'populated') < 1:   # if needed put that and val != 'No Such Instance currently exists at this OID'
                                    if isinstance(val, v2c.IpAddress):
                                        response_dict[temp_dict[
                                            name]] = str(val.prettyPrint())
                                    else:
                                        response_dict[temp_dict[name]] = str(
                                            val)  # val.prettyPrint() #str(val)
                            return

                except socket.error as (sock_errno, sock_errstr):
                    response_dict = {}
                    success = 1
                    response_dict[551] = sock_errstr
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
            response_dict[96] = ' internal error prev_Str not passed'

    # outer exception
    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer ' + str(e)
    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success
        final_responce_dict['result'] = response_dict
        return final_responce_dict


# print " finally its my tern "
# fd = {'upTime': '1.3.6.1.4.1.26149.2.2.3.1.4.1', 'ruoperationalState': '1.3.6.1.4.1.26149.2.2.3.1.7.1', 'poeStatus': '1.3.6.1.4.1.26149.2.2.3.1.5.1', 'cpuId': '1.3.6.1.4.1.26149.2.2.3.1.6.1', 'isConfigCommitedToFlash': '1.3.6.1.4.1.26149.2.2.3.1.3.1', 'lastRebootReason': '1.3.6.1.4.1.26149.2.2.3.1.2.1'}
# ip = '172.22.0.103'
# port = '161'
# c = 'public'
# print
# print pysnmp_geter(fd,ip,port,c)
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
            cmdgen.CommunityData('test-agent', community),
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
        print sock_errstr
        return 2
    except Exception as e:
        return 3

# print snmp_ping('172.22.0.120','public',161)


def pysnmp_get(ip_address, port, community, oid_str):
    """

    @param ip_address:
    @param port:
    @param community:
    @param oid_str:
    @return:
    """
    try:
        if ip_address != None and port != None and community != None and oid_str != None:
            make_pystr = lambda x: ','.join(x.split('.'))
            success = 0
            response_dict = {}
            oid_pystr = make_pystr(oid_str)
            get_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('unmp-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s)),(%s))" % (
            community, ip_address, port, oid_pystr)
            try:
                exec get_str in locals(), globals()

                if errorIndication:
                    response_dict[553] = str(errorIndication)
                    success = 1
                    return
                else:

                    if errorStatus > 0 and errorIndex != None:
                        response_dict[oid_str] = errorStatus
                        success = 1
                        return

                    elif errorStatus == 0:
                        for name, val in varBinds:

                            if val != '' and val != None:   # if needed put that and val != 'No Such Instance currently exists at this OID'
                                response_dict[oid_str] = str(val)
                                return
                            else:
                                response_dict[
                                    102] = 'No Such Instance or no Value present'
                                success = 1
                                return

            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[551] = sock_errstr
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
                response_dict[99] = 'pysnmp err ' + str(err)
        else:

            response_dict = {}
            success = 1
            response_dict[101] = 'parameters are not correct '

    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer ' + str(e)

    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success
        final_responce_dict['result'] = response_dict
        return final_responce_dict


# print pysnmp_get('172.22.0.101', 161 ,'public','1.3.6.1.4.1.26149.10.5.3.0')
def pysnmp_set1(ip_address, port, community, received_list):
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
        if ip_address != None and port != None and community != None:
            response_dict = {}
            set_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s))" % (
                community, ip_address, port)

            oid_str, datatype, value = received_list
            oid_tuple = make_tuple(oid_str)
            set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                oid_tuple, datatype, value)

            set_str = set_str + ')'
            print " ###   PYSNMP single value set only  *************** PACKET   #### ", set_str
            try:

                exec set_str in locals(), globals()

                if errorIndication:
                    success = 1
                    response_dict[553] = str(errorIndication)
                    return
                else:

                    if errorStatus > 0 and errorIndex != None:
                        response_dict[oid_str] = int(errorIndex)
                        return

                    elif errorStatus == 0:
                        print " no error >>>>>>>>>"
                        # response_dict[0] = 'all_field_set_sucessfully'
                        for name, val in varBinds:
                            response_dict[name.prettyPrint()] = 0
                        return

            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[551] = sock_errstr
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


def pysnmp_setAcl(ip_address, port, community, acl_dict={}, admin_dict={}, macAddr_dict={}, rowStatus_dict={},
                  prev_str=None, response_dict={}, temp_dict={}, error_dict={}, state=0, row=0):
    """













    @param ip_address:
    @param port:
    @param community:
    @param acl_dict:
    @param admin_dict:
    @param macAddr_dict:
    @param rowStatus_dict:
    @param prev_str:
    @param response_dict:
    @param temp_dict:
    @param error_dict:
    @param state:
    @param row:
    @requires:  ip address, port, community ,format for all dictionary objects {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)} up to rowStatus_dict

    @return: {'success': 0/1, result : {'fullName_of_field':('if successful then 0 if not then 1','error_number_if any otherwise 0')} }

    @rtype: Dictionary

    @author: Rahul Gautam

    @since: 21-sep-2011

    @date: 27-Sep-2011

    @version: 1.1

    @note: pysnmp_setAcl is a recursive function (it is a custom function designed specially for acl form in odu 100) that used to set the values for corresponding oids passed to
        it as a dictionary variable received dictionaries  {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)},
        and it return its response in another dictionary variable response_dict {'fullName_of_field':('if successful then 0 if not then 1','error_number_if any otherwise 0')}
        it handles all the errors related to snmp and some others like Neteork_Unreachable etc.

    @organization: CodeScape Consultants Pvt. Ltd.


    @copyright: 2011 Rahul Gautam for CodeScape Consultants Pvt. Ltd.

    @note: "in best case it sends only one packet of snmp set, if any of the value of that snmp set gives error, function removes that and resends the packet,
        so as the worst case when error occur in linear manner of each field of received _dict in snmp set then it send requests = length(received_dict)
        but thats the worst case In average case it is far more better than any linear or iterator function
        its recursive nature gives it a true optimisation in terms of network traffic."

    """
    try:
        make_pystr = lambda x: ','.join(x.split('.'))
        make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
        success = 0
        admin_name = None
        row_name = None
        mac_tuple = None
        mac_name = None
        if ip_address != None and port != None and community != None:

            response_dict = {}
            prev_str = None
            temp_dict = {}
            prev_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s))" % (
                community, ip_address, port)
            # print prev_str
            state_present = 0
            set_str = prev_str
            error_dict = {}
            state = 0
            row = 0
            row_present = 0
            set_str = prev_str
            if len(acl_dict) == 1 and len(admin_dict) == 1:
                state_present = 1
                admin_name = admin_dict.keys()[0]
                oid_str = admin_dict.values()[0][0]
                aoid_tuple = make_tuple(oid_str)
                temp_dict[aoid_tuple] = admin_name
                set_str = set_str + ",(%s,v2c.%s(%s))" % (
                    aoid_tuple, 'Integer32', '0')

                acl_name = acl_dict.keys()[0]
                # print acl_dict[acl_name]
                oid_str, datatype, value = acl_dict[acl_name]
                # print oid_str
                oid_tuple = make_tuple(oid_str)

                temp_dict[oid_tuple] = acl_name
                set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                    oid_tuple, datatype, value)

                admin_name = admin_dict.keys()[0]
                oid_str = admin_dict.values()[0][0]
                aoid_tuple = make_tuple(oid_str)
                set_str = set_str + ",(%s,v2c.%s(%s))" % (
                    aoid_tuple, 'Integer32', '1')

            if len(rowStatus_dict) == 1:
                row_name = rowStatus_dict.keys()[0]
                oid_str, datatype, row_value = rowStatus_dict[row_name]
                row_tuple = make_tuple(oid_str)
                temp_dict[row_tuple] = row_name
                row_present = 1
                set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                    row_tuple, datatype, row_value)

            if len(macAddr_dict) == 1:
                mac_name = macAddr_dict.keys()[0]
                oid_str, datatype, value = macAddr_dict[mac_name]
                mac_tuple = make_tuple(oid_str)
                temp_dict[mac_tuple] = mac_name
                set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                    mac_tuple, datatype, value)

            set_str = set_str + ')'

            try:
                print 'in ', macAddr_dict, rowStatus_dict
                exec set_str in locals(), globals()
                print " ~~~~~ PACEKET IS ", set_str
                print
                # print temp_dict
                if errorIndication:
                    response_dict = {}
                    response_dict[553] = str(errorIndication)
                    success = 1
                    return 'no'
                else:

                    if errorStatus > 0 and errorIndex != None:

                        if state_present == 1 and int(errorIndex) == 1:
                            print "    ok ", response_dict
                            # response_dict[admin_name] = 54
                            response_dict[temp_dict[
                                varBinds[int(errorIndex) - 1][0]]] = int(errorStatus)
                            error_dict[varBinds[int(errorIndex) - 1][0]] = 1

                            state = 2
                            response_dict[acl_name] = 100
                            error_dict[oid_tuple] = 1

                            # return pysnmp_setAcl(None, None,
                            # None,acl_dict,admin_dict,macAddr_dict,rowStatus_dict,prev_str,
                            # response_dict, temp_dict, error_dict,state)
                        elif temp_dict[varBinds[int(errorIndex) - 1][0]] == admin_name:
                            print "    ok ", response_dict
                            # response_dict[admin_name+'1'] = 55
                            response_dict[temp_dict[
                                              varBinds[int(errorIndex) - 1][0]] + '1'] = int(errorStatus)
                            error_dict[varBinds[int(errorIndex) - 1][0]] = 1
                            state = 1
                            # return pysnmp_set(None, None,
                            # None,acl_dict,admin_dict,macAddr_dict,rowStatus_dict,
                            # prev_str, response_dict, temp_dict,
                            # error_dict,state)

                        else:
                            print " >>>>>>>>>>>>>>>> YE LE RAHA HAI MERI JAN BHAI ", varBinds[int(errorIndex) - 1]
                            print "    ok responce dict is ", response_dict
                            print
                            response_dict[temp_dict[
                                varBinds[int(errorIndex) - 1][0]]] = int(errorStatus)
                            error_dict[varBinds[int(errorIndex) - 1][0]] = 1
                            if temp_dict[varBinds[int(errorIndex) - 1][0]] == row_name:
                                if str(row_value) == '4':
                                    print 'row '
                                    row = 1
                                    response_dict[temp_dict[mac_tuple]] = 100
                                    error_dict[mac_tuple] = 1
                                    # return pysnmp_setAcl(None, None,
                                    # None,acl_dict,admin_dict,macAddr_dict,rowStatus_dict,
                                    # prev_str, response_dict, temp_dict,
                                    # error_dict,state,row)
                                else:
                                    row = 2
                                    if (acl_dict) == 0 and (admin_dict) == 0 and (macAddr_dict) == 0:
                                        return
                                    else:
                                        pass

                        if len(error_dict) >= len(acl_dict) + len(admin_dict) + len(macAddr_dict) + len(rowStatus_dict):
                            return
                        else:

                            response_dict = pysnmp_setAcl(
                                None, None, None, acl_dict, admin_dict, macAddr_dict,
                                rowStatus_dict, prev_str, response_dict, temp_dict, error_dict, state, row)
                            return

                    elif errorStatus == 0:
                        print " all  SET or GET  sucessful  >>>>>>>>>"
                        # response_dict[0] = 'all_field_set_sucessfully'
                        for name, val in varBinds:
                            response_dict[temp_dict[name]] = 0
                        return

            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[551] = sock_errstr
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

        # outer
        else:

            if prev_str == None and ip_address == None and port == None and community == None:
                print " no ip"
            elif ip_address == None and port == None and community == None and prev_str != None:
                print " >>>>> RECURSIVE ", response_dict
                state_present = 0
                set_str = prev_str
                if len(acl_dict) == 1 and len(admin_dict) == 1 and state < 2:
                    state_present = 1
                    admin_name = admin_dict.keys()[0]
                    oid_str = admin_dict.values()[0][0]
                    aoid_tuple = make_tuple(oid_str)
                    temp_dict[aoid_tuple] = admin_name
                    set_str = set_str + \
                              ",(%s,v2c.%s(%s))" % (aoid_tuple, 'Integer32', '0')

                    acl_name = acl_dict.keys()[0]
                    # print acl_dict[acl_name]
                    oid_str, datatype, value = acl_dict[acl_name]
                    # print oid_str
                    oid_tuple = make_tuple(oid_str)
                    if oid_tuple in error_dict:
                        pass
                    else:
                        temp_dict[oid_tuple] = acl_name
                        set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                            oid_tuple, datatype, value)
                    if state != 1:
                        admin_name = admin_dict.keys()[0]
                        oid_str = admin_dict.values()[0][0]
                        aoid_tuple = make_tuple(oid_str)
                        set_str = set_str + ",(%s,v2c.%s(%s))" % (
                            aoid_tuple, 'Integer32', '1')

                if len(rowStatus_dict) == 1 and row == 0:
                    row_name = rowStatus_dict.keys()[0]
                    oid_str, datatype, row_value = rowStatus_dict[row_name]
                    oid_tuple = make_tuple(oid_str)
                    temp_dict[oid_tuple] = row_name
                    row_present = 1
                    set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                        oid_tuple, datatype, row_value)

                if len(macAddr_dict) == 1 and row != 1:
                    mac_name = macAddr_dict.keys()[0]
                    oid_str, datatype, value = macAddr_dict[mac_name]
                    mac_tuple = make_tuple(oid_str)
                    if mac_tuple in error_dict:
                        pass
                    else:
                        temp_dict[mac_tuple] = mac_name
                        set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                            mac_tuple, datatype, value)

                set_str = set_str + ')'

                print 'set_str   Packet ', set_str

                try:

                    exec set_str in locals(), globals()
                    print " execution secessful "
                    if errorIndication:
                        print 'time out hai'
                        response_dict = {}
                        response_dict[553] = str(errorIndication)
                        success = 1
                        return
                    else:

                        if errorStatus > 0 and errorIndex != None:
                            print " still error"

                            if state_present == 1 and int(errorIndex) == 1:

                                # response_dict[admin_name] = 54
                                response_dict[temp_dict[
                                    varBinds[int(errorIndex) - 1][0]]] = int(errorStatus)
                                error_dict[
                                    varBinds[int(errorIndex) - 1][0]] = 1
                                state = 1
                                # return pysnmp_setAcl(None, None,
                                # None,acl_dict,admin_dict,macAddr_dict,rowStatus_dict,prev_str,
                                # response_dict, temp_dict, error_dict,state)
                            elif len(varBinds) == int(errorIndex) and state_present == 1:

                                # response_dict[admin_name+'1'] = 55
                                response_dict[temp_dict[varBinds[int(
                                    errorIndex) - 1][0]] + '1'] = int(errorStatus)
                                error_dict[
                                    varBinds[int(errorIndex) - 1][0]] = 1
                                state = 2
                                # return pysnmp_setAcl(None, None,
                                # None,acl_dict,admin_dict,macAddr_dict,rowStatus_dict,
                                # prev_str, response_dict, temp_dict,
                                # error_dict,state)

                            else:
                                print " >>>>>>>>>>>>>>>> YE LE RAHA HAI MERI JAN BHAI ", varBinds[int(errorIndex) - 1]
                                print "    ok responce dict is ", response_dict
                                print

                                response_dict[temp_dict[
                                    varBinds[int(errorIndex) - 1][0]]] = int(errorStatus)
                                error_dict[
                                    varBinds[int(errorIndex) - 1][0]] = 1

                                if temp_dict[varBinds[int(errorIndex) - 1][0]] == row_name:
                                    if str(row_value) == '4':
                                        print 'row '
                                        row = 1
                                        response_dict[
                                            temp_dict[mac_tuple]] = 100
                                        error_dict[mac_tuple] = 1

                                        # return pysnmp_setAcl(None, None,
                                        # None,acl_dict,admin_dict,macAddr_dict,rowStatus_dict,
                                        # prev_str, response_dict, temp_dict,
                                        # error_dict,state,row)
                                    else:
                                        row = 2
                                        if (acl_dict) == 0 and (admin_dict) == 0 and (macAddr_dict) == 0:
                                            return
                                        else:
                                            pass
                                            # return pysnmp_setAcl( None, None,
                                            # None,
                                            # acl_dict,admin_dict,macAddr_dict,rowStatus_dict,prev_str,
                                            # response_dict, temp_dict,
                                            # error_dict,state,row)

                            if len(error_dict) >= len(acl_dict) + len(admin_dict) + len(macAddr_dict) + len(
                                    rowStatus_dict):
                                print " if me aa gaya h pysnmp NOW RETURNING RESULT"
                                return
                            else:
                                response_dict = pysnmp_setAcl(
                                    None, None, None, acl_dict, admin_dict, macAddr_dict,
                                    rowStatus_dict, prev_str, response_dict, temp_dict, error_dict, state, row)
                                return

                        elif errorStatus == 0:
                            print " all  SET or GET  sucessful  >>>>>>>>>"
                            # response_dict[0] = 'all_field_set_sucessfully'
                            for name, val in varBinds:
                                if name in temp_dict:
                                    print name
                                response_dict[temp_dict[name]] = 0
                            return

                except socket.error as (sock_errno, sock_errstr):
                    response_dict = {}
                    success = 1
                    response_dict[551] = sock_errstr
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
                print " no prev str internal error "
    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer err ' + str(e)
    finally:
        if 'success' in response_dict:
            return response_dict
        else:
            final_response_dict = {}
            final_response_dict['success'] = success
            final_response_dict['result'] = response_dict
            return final_response_dict


def pysnmp_seter(received_dict={}, ip_address=None, port=None, community=None, admin_state={}, prev_str=None,
                 response_dict={}, temp_dict={}, error_dict={}, state=0):
    """










    @param received_dict:
    @param ip_address:
    @param port:
    @param community:
    @param admin_state:
    @param prev_str:
    @param response_dict:
    @param temp_dict:
    @param error_dict:
    @param state:
    @requires: {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)} , ip address, port, community, if admin_state dependency present then pass admin_state as dictionary         {'admin_state':(oid_str)}

    @return: {'success': 0/1, result : {'fullName_of_field':('if successful then 0 if not then 1','error_number_if any otherwise 0')} }

    @rtype: Dictionary

    @author: Rahul Gautam

    @since: 11-sep-2011

    @date: 16-Sep-2011

    @version: 1.1

    @note: pysnmp_seter is a recursive function that used to set the values for corresponding oids passed to
        it as a dictionary variable received_dict  {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)},
        and it return its response in another dictionary variable response_dict {'fullName_of_field':('if successful then 0 if not then 1','error_number_if any otherwise 0')}
        it handles all the errors related to snmp and some others like Neteork_Unreachable etc.

    @organization: CodeScape Consultants Pvt. Ltd.


    @copyright: 2011 Rahul Gautam for CodeScape Consultants Pvt. Ltd.

    @note: "in best case it sends only one packet of snmp set, if any of the value of that snmp set gives error, function removes that and resends the packet,
        so as the worst case when error occur in linear manner of each field of received _dict in snmp set then it send requests = length(received_dict)
        but thats the worst case In average case it is far more better than any linear or iterator function
        its recursive nature gives it a true optimisation in terms of network traffic."

    """

    try:
        make_tuple = lambda x: tuple(int(i) for i in x.split(
            '.'))  # @note: this lambda function used to convert a oid string to oid tuple (in a format required by pysnmp)
        success = 0
        if ip_address == None and port == None and community == None:

            if prev_str != '':

                set_str = prev_str
                # print "debug 1"
                if len(admin_state) > 0:
                    admin_name = admin_state.keys()[0]
                    if admin_name[len(admin_name) - 2:len(admin_name)] != '-1':
                        state_present = 1
                    oid_str = admin_state.values()[0][0]
                    aoid_tuple = make_tuple(oid_str)
                    set_str = set_str + \
                              ",(%s,v2c.%s(%s))" % (aoid_tuple, 'Integer32', '0')

                for i in received_dict.keys():
                    oid_str, datatype, value = received_dict[i]
                    oid_tuple = make_tuple(oid_str)
                    if oid_tuple in error_dict:
                        pass
                    else:
                        set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                            oid_tuple, datatype, value)

                if state_present == 1 and state == 0:
                    set_str = set_str + \
                              ",(%s,v2c.%s(%s))" % (aoid_tuple, 'Integer32', '1')
                else:
                    temp_dict[aoid_tuple] = admin_name

                set_str = set_str + ')'
                print " >>>>  RECURSIVE CALL <<<< ", response_dict
                try:

                    exec set_str in locals(), globals()
                    print 'temp_dict ', temp_dict
                    print 'error_dict ', error_dict
                    if errorIndication:
                        response_dict[553] = str(errorIndication)
                        return

                    else:

                        if errorStatus > 0 and errorIndex != None:

                            if state_present == 1 and int(errorIndex) == 1:
                                response_dict[
                                    54] = "NOT ABLE TO LOCK THE DEVICE"
                                success = 1
                                return
                            elif state == 0 and len(varBinds) == int(errorIndex):
                                response_dict[admin_name + '1'] = 55
                                state = 1
                            else:
                                print " ^^^^^^^^^  something else >>>"
                                state = 0
                                response_dict[temp_dict[
                                    varBinds[int(errorIndex) - 1][0]]] = int(errorIndex)
                                error_dict[
                                    varBinds[int(errorIndex) - 1][0]] = 1

                            if len(error_dict) >= len(received_dict):
                                return
                            else:
                                return pysnmp_set(received_dict, None, None, None, admin_state, prev_str, response_dict,
                                                  temp_dict, error_dict, state)

                        elif errorStatus == 0:
                            for name, val in varBinds:
                                response_dict[temp_dict[name]] = 0
                            return

                except socket.error as (sock_errno, sock_errstr):
                    response_dict = {}
                    success = 1
                    response_dict[551] = sock_errstr
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
                response_dict[96] = ' internal error prev_Str not passed'
        else:
            if ip_address != None and port != None and community != None:
                response_dict = {}
                prev_str = None
                temp_dict = {}
                prev_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s))" % (
                community, ip_address, port)
                state_present = 0
                set_str = prev_str
                error_dict = {}
                state = 0

                if len(admin_state) > 0:
                    admin_name = admin_state.keys()[0]
                    if admin_name[len(admin_name) - 2:len(admin_name)] != '-1':
                        state_present = 1
                    oid_str = admin_state.values()[0][0]
                    aoid_tuple = make_tuple(oid_str)
                    temp_dict[aoid_tuple] = admin_name
                    set_str = set_str + \
                              ",(%s,v2c.%s(%s))" % (aoid_tuple, 'Integer32', '0')

                for i in received_dict.keys():
                    oid_str, datatype, value = received_dict[i]
                    oid_tuple = make_tuple(oid_str)
                    temp_dict[oid_tuple] = i
                    set_str = set_str + \
                              ",(%s,v2c.%s('%s'))" % (oid_tuple, datatype, value)
                if state_present == 1:
                    set_str = set_str + \
                              ",(%s,v2c.%s(%s))" % (aoid_tuple, 'Integer32', '1')
                    temp_dict[aoid_tuple] = admin_name + '1'
                set_str = set_str + ')'
                print " ###   PYSNMP SET PACKET   #### ", set_str
                try:
                    print 'temp_dict : >>>>>>>>>>>>>>>>>', temp_dict
                    exec set_str in locals(), globals()

                    if errorIndication:
                        response_dict[553] = str(errorIndication)
                        return
                    else:

                        if errorStatus > 0 and errorIndex != None:

                            if state_present == 1 and int(errorIndex) == 1:
                                print "    ok ", response_dict
                                success = 1
                                response_dict[
                                    54] = "NOT ABLE TO LOCK THE DEVICE"

                            elif len(varBinds) == int(errorIndex):
                                print "    ok ", response_dict
                                response_dict[admin_name + '1'] = 55
                                state = 1
                                response_dict = pysnmp_set(
                                    received_dict, None, None, None, admin_state, prev_str, response_dict, temp_dict,
                                    error_dict,
                                    state)

                            else:
                                print " >>>>>>>>>>>>>>>> YE LE RAHA HAI MERI JAN BHAI ", varBinds[int(errorIndex) - 1]
                                print "    ok ", response_dict
                                print
                                response_dict[temp_dict[
                                    varBinds[int(errorIndex) - 1][0]]] = int(errorStatus)
                                error_dict[
                                    varBinds[int(errorIndex) - 1][0]] = 1

                                response_dict = pysnmp_set(
                                    received_dict, None, None, None, admin_state,
                                    prev_str, response_dict, temp_dict, error_dict)

                            return

                        elif errorStatus == 0:
                            print " all  SET or GET  sucessful  >>>>>>>>>"

                            for name, val in varBinds:
                                if name in temp_dict:
                                    print name
                                response_dict[temp_dict[name]] = 0
                            return

                except socket.error as (sock_errno, sock_errstr):
                    response_dict = {}
                    success = 1
                    response_dict[551] = sock_errstr
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
        response_dict[98] = 'outer ' + str(e)
    finally:
        if 'success' in response_dict:
            return response_dict
        else:
            final_response_dict = {}
            final_response_dict['success'] = success
            final_response_dict['result'] = response_dict
            return final_response_dict
            # sys.exit(1)


##

def pysnmp_set(received_dict={}, ip_address=None, port=None, community=None, admin_state={}):
    """





    @param received_dict:
    @param ip_address:
    @param port:
    @param community:
    @param admin_state:
    @requires: {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)} , ip address, port, community, if admin_state dependency present then pass admin_state as dictionary         {'admin_state':(oid_str)}

    @return: {'success': 0/1, result : {'fullName_of_field':('if successful then 0 if not then 1','error_number_if any otherwise 0')} }

    @rtype: Dictionary

    @author: Rahul Gautam

    @since: 16-sep-2011

    @date: 21-Sep-2011

    @version: 1.1

    @note: pysnmp_set is a simple function that used to set the values for corresponding oids passed to
        it (means set multiple values at a single time in a single packet) as a dictionary variable received_dict  {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)},
        and it return its response in another dictionary variable response_dict {'fullName_of_field':('if successful then 0 if not then 1','error_number_if any otherwise 0')}
        it handles all the errors related to snmp and some others like Neteork_Unreachable etc.

    @organization: CodeScape Consultants Pvt. Ltd.


    @copyright: 2011 Rahul Gautam for CodeScape Consultants Pvt. Ltd.

    """
    try:
        make_tuple = lambda x: tuple(int(i) for i in x.split(
            '.'))  # @note: this lambda function used to convert a oid string to oid tuple (in a format required by pysnmp)
        success = 0
        if ip_address != None and port != None and community != None:
            response_dict = {}
            error_dict = {}
            temp_dict = {}
            prev_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s))" % (
                community, ip_address, port)
            state_present = 0
            set_str = prev_str

            if len(admin_state) > 0:
                admin_name = admin_state.keys()[0]
                if admin_name[len(admin_name) - 2:len(admin_name)] != '-1':
                    state_present = 1
                oid_str = admin_state.values()[0][0]
                aoid_tuple = make_tuple(oid_str)
                temp_dict[aoid_tuple] = admin_name
                set_str = set_str + ",(%s,v2c.%s(%s))" % (
                    aoid_tuple, 'Integer32', '0')

            for i in received_dict.keys():
                oid_str, datatype, value = received_dict[i]
                oid_tuple = make_tuple(oid_str)
                temp_dict[oid_tuple] = i
                set_str = set_str + ",(%s,v2c.%s('%s'))" % (
                    oid_tuple, datatype, value)
            if state_present == 1:
                set_str = set_str + ",(%s,v2c.%s(%s))" % (
                    aoid_tuple, 'Integer32', '1')
                temp_dict[aoid_tuple] = admin_name + '1'
            set_str = set_str + ')'
            print " ###   PYSNMP single *************** PACKET   #### ", set_str
            try:

                exec set_str in locals(), globals()

                if errorIndication:
                    success = 1
                    response_dict[553] = str(errorIndication)
                    return
                else:

                    if errorStatus > 0 and errorIndex != None:

                        if state_present == 1 and int(errorIndex) == 1:
                            print "    ok ", response_dict
                            success = 1
                            response_dict[54] = "NOT ABLE TO LOCK THE DEVICE"
                            return
                        elif len(varBinds) == int(errorIndex):
                            print "    ok ", response_dict
                            response_dict[admin_name + '1'] = 55
                            state = 1
                        else:
                            print " >>>>>>>>>>>>>>>> YE LE RAHA HAI MERI JAN BHAI ", varBinds[int(errorIndex) - 1]
                            print "    ok ", response_dict
                            print
                            response_dict[temp_dict[
                                varBinds[int(errorIndex) - 1][0]]] = int(errorStatus)
                            error_dict[varBinds[int(errorIndex) - 1][0]] = 1
                            for name, val in varBinds:
                                if temp_dict[name] in response_dict:
                                    pass
                                else:
                                    response_dict[temp_dict[name]] = 100
                        return

                    elif errorStatus == 0:
                        print " no error >>>>>>>>>"
                        # response_dict[0] = 'all_field_set_sucessfully'
                        for name, val in varBinds:
                            response_dict[temp_dict[name]] = 0
                        return

            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[551] = sock_errstr
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
