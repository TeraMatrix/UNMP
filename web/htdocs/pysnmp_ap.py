import socket
import sys
import time
# importing pysnmp library
import pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.api import v2c
# import traceback


def odubulk(oid, ip_address, port, community, max_value=10):
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
                    cmdgen.CommunityData('bulkodu-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                    first_value, max_value, make_tuple(oid))

                var_dict = {}

                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[553] = str(errorIndication)
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
                                if isinstance(val, v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = val.prettyPrint(
                                    )  # str(val) #str(val) #
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
                err_dict[551] = str(sock_err)
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


# print
# table_bulk("1.3.6.1.4.1.26149.2.2.13.5.1","172.22.0.120",161,"public",5)


def bulktable(oid, ip_address, port, community, max_value=5):
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
                    cmdgen.CommunityData('table-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                    first_value, max_value, make_tuple(oid))

                var_dict = {}

                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[553] = str(errorIndication)
                    return
                    # handle

                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = str(errorStatus)
                        success = 1
                        return
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        # print varBindTable
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
                                # print oid_values_list
                                if len(oid_values_list) > 0:
                                    oid_no = oid_values_list.pop(0)
                                else:
                                    success = 1
                                    return
                                if isinstance(val, v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = str(
                                        val)  # val.prettyPrint() val.prettyPrint() #str(val) #val.prettyPrint() #str(val)
                                    # if value.find('0x'):
                                    #    value = str(value[2:])

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
                                    # print oid_values_list
                                    if len(oid_values_list) == 1:
                                        if oid == '1.3.6.1.4.1.26149.10.4.4.1.1' or oid == '1.3.6.1.4.1.26149.10.4.5.1.1.1':
                                            pass
                                        else:
                                            if str(oid_values_list[0]) == '0':
                                                oid_values_list.pop(0)
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
                err_dict[551] = str(sock_err)
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err ' + str(err)
            except Exception as e:
                # print traceback.print_exc(e)
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

# print bulktable("1.3.6.1.4.1.26149.2.2.13.5.1","172.22.0.102",161,"public",5)


def bulkget(ip_address, port, community, oid, first_value, max_value, return_list=[]):
    """

    @param ip_address:
    @param port:
    @param community:
    @param oid:
    @param first_value:
    @param max_value:
    @param return_list:
    @return:
    """
    err_dict = {}
    success = 1
    try:
        print " RUN \n"
        make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
        # oid = oid.strip('.')

        errorIndication, errorStatus, errorIndex, \
        varBindTable = cmdgen.CommandGenerator().bulkCmd(
            cmdgen.CommunityData('table-agent', community), cmdgen.UdpTransportTarget((ip_address, port)), first_value,
            max_value, make_tuple(oid))

        if errorIndication and len(varBindTable) < 1:
            success = 1
            err_dict[553] = str(errorIndication)
            return
            # handle
        else:
            if errorStatus:
                # err_dict[int(errorStatus)] = str(errorStatus)
                err_dict[int(errorStatus)] = str(errorStatus)
                success = 1
                # print '%s at %s\n' % ( errorStatus.prettyPrint(),errorIndex
                # and varBindTable[-1][int(errorIndex)-1] or '?')
            else:
                success = 0

                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        # print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
                        # print name.prettyPrint()
                        temp_split = name.prettyPrint().split(oid)
                        if len(temp_split) > 1:
                            print temp_split
                            pass
                        else:
                            print " data :::: "
                            print " >>>>>>>>>>>>>>>>>>>> ", len(return_list)
                            success = 2
                            return

                        if isinstance(val, v2c.IpAddress):
                            value = str(val.prettyPrint())
                        else:
                            value = val.prettyPrint(
                            )  # str(val) #val.prettyPrint() #str(val)

                        return_list.append((name.prettyPrint(), value))

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
        success = 1
        err_dict[99] = 'pysnmp exception ' + str(e)
    finally:
        result_dict = {}
        if success == 0:
            result_dict['success'] = success
            result_dict['result'] = return_list
        elif success == 2:
            result_dict['success'] = success
            result_dict['result'] = return_list
        else:
            result_dict['success'] = success
            result_dict['result'] = err_dict
        return result_dict


def table_bulk(oid, ip_address, port, community):
    """

    @param oid:
    @param ip_address:
    @param port:
    @param community:
    @return:
    """
    err_dict = {}
    var_dict = {}
    success = 1
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                              int):
            try:
                oid = oid.strip('.')
                varBindTable = []
                first_value, max_value = 0, 7
                while 1:
                    print " *%%**%*%*%*%*%*%*  ", first_value
                    return_dict = bulkget(ip_address, port, community, oid,
                                          first_value, max_value, varBindTable)
                    if return_dict['success'] == 0:
                        varBindTable = return_dict['result']
                    elif return_dict['success'] == 2:
                        varBindTable = return_dict['result']
                        break
                    else:
                        success = 1
                        err_dict = return_dict['result']
                        return

                    first_value = first_value + max_value

                success = 0
                oid_li = []
                var_dict = {}
                print " ok "
                for name, value in varBindTable:
                    # print '%s = %s' % (name, value)
                    # print name.prettyPrint()
                    oid_values_list = name.split(oid)[1].strip('.').split('.')
                    # print oid_values_list
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
                        # oid_values_list.pop(0)
                        # print oid_values_list
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
                err_dict[551] = str(sock_err)
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err ' + str(err)
            except Exception as e:
                print " exx ", str(e)
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


###### NEW GENERIC TABLE FUNCTION
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
                oid = oid.strip('.')
                # print oid
                errorIndication, errorStatus, errorIndex, \
                varBindTable = cmdgen.CommandGenerator().nextCmd(
                    cmdgen.CommunityData('table-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                    make_tuple(oid))

                var_dict = {}

                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[553] = str(errorIndication)
                    # handle

                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = errorStatus.prettyPrint()
                        success = 1
                        # print '%s at %s\n' % (
                        # errorStatus.prettyPrint(),errorIndex and
                        # varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        # print varBindTable
                        print
                        print oid
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                # print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
                                # print name.prettyPrint()
                                oid_values_list = name.prettyPrint(
                                ).split(oid)[1].strip('.').split('.')
                                # print oid_values_list
                                if len(oid_values_list) > 0:
                                    oid_no = oid_values_list.pop(0)
                                else:
                                    success = 1
                                    return
                                if isinstance(val, v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = val.prettyPrint(
                                    )  # str(val) #val.prettyPrint() #str(val)
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
                                    # print oid_values_list
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
                err_dict[551] = str(sock_err)
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


def pysnmp_get_table_old(oid, ip_address, port, community):
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
                if errorIndication and len(varBindTable) < 1:
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
                        is_oid2 = 0
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                oid_values_list = name.prettyPrint(
                                ).split(oid)[1][1:].split('.')
                                if len(oid_values_list) == 3:
                                    oid_no, oid2, oid3 = oid_values_list
                                    is_oid2 = 1
                                elif len(oid_values_list) == 2:
                                    oid_no, oid3 = oid_values_list
                                else:
                                    success = 1
                                    return
                                if isinstance(val, v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = val.prettyPrint(
                                    )  # str(val) #val.prettyPrint() #str(val)
                                if oid_li.count(oid_no) == 0:
                                    oid_li.append(oid_no)
                                    count = 0
                                    flag = 1
                                    if len(oid_li) == 1:
                                        flag = 0

                                if flag == 0:
                                    count += 1
                                    li = []
                                    if is_oid2:
                                        li.append(oid2)
                                    li.append(oid3)
                                    li.append(value)
                                    var_dict[count] = li
                                else:
                                    count += 1
                                    li = var_dict[count]
                                    li.append(value)
                                    var_dict[count] = li

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
                ).nextCmd(cmdgen.CommunityData('table-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                          make_tuple(oid))
                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[553] = str(errorIndication)
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

                                if isinstance(val, v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = val.prettyPrint(
                                    )  # str(val) #val.prettyPrint() #str(val)

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
                err_dict[551] = str(sock_err)
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err ' + str(err)
            except Exception as e:
                success = 1
                err_dict[99] = 'pysnmp exception get ' + str(e)
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
            datatypes_dict = {
                'Integer32': v2c.Integer32, 'Unsigned32': v2c.Unsigned32, 'OctetString': v2c.OctetString,
                'DisplayString': v2c.OctetString, 'Gauge32': v2c.Gauge32,
                'IpAddress': v2c.IpAddress, 'Counter32': v2c.Counter32, 'Counter64': v2c.Counter64}

            response_dict = {}

            oid_str, datatype, value = received_list

            snmp_args = [cmdgen.CommunityData('single-set', community),
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
                    response_dict[553] = str(errorIndication)
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


# print single_set('172.22.0.101',161,'private',['1.3.6.1.4.1.26149.10.2.3.1.2.0','Integer32',2])
# print single_set('172.22.0.101',161,'private',['1.3.6.1.4.1.26149.10.2.3.2.1.0','OctetString','snuj1234'])
# print
# pysnmp_get_table('1.3.6.1.4.1.26149.10.2.3.4.2.1.1','172.22.0.101',161,'private')

# print single_set('172.22.0.101',
# 161,'private',['1.3.6.1.4.1.26149.10.2.3.4.1.1.0','Integer32',1])

def vapsetup_ap(ip_address, port=161):
    """

    @param ip_address:
    @param port:
    @return:
    """
    get_community = 'public'
    set_community = 'private'
    vap_dict = {}
    vap_data_list = []
    vapSelection_oid = '1.3.6.1.4.1.26149.10.2.3.1'
    selectVap_oid = '1.3.6.1.4.1.26149.10.2.3.1.2.0'
    basicVAPsetup_oid = '1.3.6.1.4.1.26149.10.2.3.2'
    basicVAPsecurity_oid = '1.3.6.1.4.1.26149.10.2.3.3.1'
    # vapWEPsecuritySetup_oid = '1.3.6.1.4.1.26149.10.2.3.3.2'
    vapWPAsecuritySetup_oid = '1.3.6.1.4.1.26149.10.2.3.3.3'
    basicACLsetup_oid = '1.3.6.1.4.1.26149.10.2.3.4.1'
    aclState_oid = '1.3.6.1.4.1.26149.10.2.3.4.1.1.0'
    aclMACsTable_oid = '1.3.6.1.4.1.26149.10.2.3.4.2.1.1'
    success = 0
    final_result_dict = {}
    try:
        vap_selc_dict = pysnmp_get_node(
            vapSelection_oid, ip_address, port, get_community)

        if vap_selc_dict['success'] == 0:
            vap_selc_list = vap_selc_dict['result'][1] if len(
                vap_selc_dict['result']) > 0 else []

            if len(vap_selc_list) > 1:
                total_vap = int(vap_selc_list[0])
                select_vap = vap_selc_list[1]

                for vap in range(1, total_vap + 1):
                    vap_data_list = []
                    # print " vap to set is ",vap
                    set_dict = single_set(ip_address, port, set_community,
                                          [selectVap_oid, 'Integer32', vap])
                    # print "set_dict",set_dict
                    if set_dict['success'] == 0:
                        result2_dict = pysnmp_get_node(basicVAPsetup_oid,
                                                       ip_address, port, get_community)  # basicVapSetup
                        # print "1",result2_dict
                        if result2_dict['success'] == 0:
                            list2 = result2_dict['result'][
                                1] if len(result2_dict['result']) > 0 else []
                            vap_data_list.append(list2)
                            result2_dict = pysnmp_get_node(
                                basicVAPsecurity_oid, ip_address, port, get_community)  # basicVapSecurity
                            # print "2",result2_dict
                            if result2_dict['success'] == 0:
                                list2 = result2_dict['result'][1] if len(
                                    result2_dict['result']) > 0 else []
                                vap_data_list.append(list2)

                                # result2_dict = pysnmp_get_node(vapWEPsecuritySetup_oid,ip_address, port, get_community) #vapWEP
                                # if result2_dict['success'] == 0:
                                #    list2 = result2_dict['result'][1] if len(result2_dict['result']) > 0 else []
                                #    vap_data_list.append(list2)
                                # else:
                                #    vap_data_list.append([])

                                result2_dict = pysnmp_get_node(
                                    vapWPAsecuritySetup_oid, ip_address, port, get_community)  # vapWAP
                                if result2_dict['success'] == 0:
                                    list2 = result2_dict['result'][1] if len(
                                        result2_dict['result']) > 0 else []
                                    vap_data_list.append(list2)
                                else:
                                    vap_data_list.append([])

                                result2_dict = pysnmp_get_node(
                                    basicACLsetup_oid, ip_address, port, get_community)  # basicACLmode
                                if result2_dict['success'] == 0:
                                    list2 = result2_dict['result'][1] if len(
                                        result2_dict['result']) > 0 else []
                                    list2 = list2[:2]
                                    list3 = []
                                    flag_acl_mode = 0
                                    if list2[0] == '0':
                                        acl_dict = single_set(
                                            ip_address, port, set_community, [aclState_oid, 'Integer32', 1])
                                        # print " @",acl_dict
                                        if acl_dict['success'] == 0:
                                            flag_acl_mode = 1
                                    time.sleep(1)
                                    result2_dict = pysnmp_get_table(
                                        aclMACsTable_oid, ip_address, port, get_community)  # ACLmacTable
                                    # print " >> ",result2_dict
                                    if result2_dict['success'] == 0:
                                        for i in range(1, len(result2_dict['result']) + 1):
                                            list3.append(result2_dict[
                                                'result'][i])
                                    if flag_acl_mode:
                                        acl_dict = single_set(
                                            ip_address, port, set_community, [aclState_oid, 'Integer32', 0])
                                        if acl_dict['success'] == 0:
                                            pass
                                        else:
                                            list2.pop(0)
                                            list2.insert(0, '1')

                                    vap_data_list.append(list2)
                                    vap_data_list.append(list3)
                                    vap_dict[vap] = vap_data_list

                            else:
                                return
                        else:
                            return
                    else:
                        return
            else:
                success = 1
                final_result_dict = " No vap Selection Found "
        else:
            success = 1
            final_result_dict = vap_selc_dict['result']
    except Exception, e:
        success = 1
        final_result_dict = str(e)
    finally:
        di = {}
        di['success'] = success
        if success == 0:
            final_result_dict['vap'] = vap_selc_list
            final_result_dict['data'] = vap_dict
        di['result'] = final_result_dict
        return di


# print vapsetup_ap('172.22.0.101')

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
                ).nextCmd(cmdgen.CommunityData('get-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                          make_tuple(oid))
                if errorIndication:
                    response_dict[553] = str(errorIndication)
                    success = 1
                    return
                else:
                    if errorStatus > 0 and errorIndex != None:
                        response_dict[int(
                            errorStatus)] = errorStatus.prettyPrint()
                        success = 1
                        return
                    elif errorStatus == 0:
                        # print varBindTable
                        if len(varBindTable) < 1:
                            success = 1
                            response_dict[
                                102] = 'NO VALUE ASSOCIATED WITH OID FOR SNMP GET'
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                if isinstance(val, v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = val.prettyPrint(
                                    )  # str(val) #val.prettyPrint() #str(val)
                                response_dict[oid] = value

            except socket.error as err:
                response_dict = {}
                success = 1
                response_dict[551] = str(err)
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
        datatypes_dict = {'Integer32': v2c.Integer32, 'Integer': v2c.Integer32, 'Unsigned32': v2c.Gauge32,
                          'OctetString': v2c.OctetString, 'DisplayString': v2c.OctetString, 'Gauge32': v2c.Gauge32,
                          'Gauge': v2c.Gauge32, 'IpAddress':
            v2c.IpAddress, 'Counter32': v2c.Counter32, 'Counter': v2c.Counter32, 'Counter64': v2c.Counter64}
        if is_recursive:
            print " **** recursive \n", port
            is_recursive = 0
            snmp_args = [cmdgen.CommunityData('ap-seter', community),
                         cmdgen.UdpTransportTarget(
                             (ip_address, int(port))),
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
                    response_dict[553] = str(errorIndication)
                    success = 1
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
                response_dict[551] = str(err)
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
                snmp_args = [cmdgen.CommunityData('ap25-seter', community),
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
                        response_dict[553] = str(errorIndication)
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
