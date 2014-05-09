#!/usr/bin/python2.6
'''
@author: Rahul Gautam

@since: 11-Sep-2011

@note: A complete set of SNMP functions (like set,walk,bulkGet,get,getNext) for UNMP using pysnmp library, with proper error handling

@organization: CodeScape Consultants Pvt. Ltd.

@copyright: 2011 Rahul Gautam for CodeScape Consultants Pvt. Ltd.
'''

import socket
import sys
# importing pysnmp library
import pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.api import v2c
#from common_controller import #logme

def pysnmp_get_table_ap(oid, ip_address, port, community):
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

# print pysnmp_get_table_ap('1.3.6.1.4.1.26149.2.1.2.2', '172.22.0.104',
# 8001, 'public')

# handel iiiii case

# errorStatus = {0:'noError',
#               1:'tooBig',
#               2:'noSuchName',
#               3:'badValue',
#               4:'readOnly',
#               5:'genErr',
#               6:'noAccess',
#               7:'wrongType',
#               8:'wrongLength',
#               9:'wrongEncoding',
#               10:'wrongValue',
#               11:'noCreation',
#               12:'inconsistentValue',
#               13:'resourceUnavailable',
#               14:'commitFailed',
#               15:'undoFailed',
#               16:'authorizationError',
#               17:'notWritable',
#               18:'inconsistentName',
#               50:'unKnown',
#               51:'networkUnreachable',
#               52:'typeError',
#               53:'requestTimeOut',
#               54:'0active_state_notAble_to_lock',
#               55:'1active_state_notAble_to_Unlock',
#               77:'Unknown',
#               96:'InternalError',
#               97:'ip-port-community_not_passed',
#               98:'otherException',
#               99:'pysnmpException'}


def pysnmp_set(received_dict={}, ip_address=None, port=None, community=None, admin_state={}, prev_str=None,
               response_dict={}, temp_dict={}, error_dict={}, state=0):
    """
    @requires: {'fullName_of_field':(oid_as_string,oid_datatype,oid_value_to_be_set)} , ip address, port, community, if admin_state dependency present then pass admin_state as dictionary 		{'admin_state':(oid_str)}

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
    print "\n %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n"
    #logme(str(received_dict)+','+str(ip_address)+','+str(port)+','+str(community)+','+str(admin_state))
    try:
        make_tuple = lambda x: tuple(int(i) for i in x.split(
            '.'))  # @note: this lambda function used to convert a oid string to oid tuple (in a format required by pysnmp)
        success = 0
        state_present = 0
        admin_name = None
        if ip_address == None and port == None and community == None:

            if prev_str != '':

                set_str = prev_str
                print "debug 1 RECURSIVE"

                if len(admin_state) > 0:
                    admin_name = admin_state.keys()[0]
                    if admin_name[len(admin_name) - 2:len(admin_name)] != '-1':
                        state_present = 1
                    else:
                        state_present = 0
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
                elif admin_name is not None:
                    temp_dict[aoid_tuple] = admin_name
                set_str = set_str + ')'
                print " >>>>  RECURSIVE CALL <<<< ", response_dict
                try:

                    exec set_str in locals(), globals()

                    if errorIndication:
                        response_dict = {}
                        response_dict[553] = str(errorIndication)
                        success = 1
                        return

                    else:

                        if errorStatus > 0 and errorIndex != None:

                            if state_present == 1 and int(errorIndex) == 1:
                                response_dict[
                                    54] = "NOT ABLE TO LOCK THE DEVICE"
                                success = 1
                                return
                            elif state == 0 and state_present == 1 and len(varBinds) == int(errorIndex):

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
                                print " ^^^^^^^^^^^^^^^^^^^^^^RECURSION AT ITS MAXIMUM LIMIT^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                                success = 1
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
                    response_dict[
                        99] = 'pysnmp exception in recursive : ' + str(e)

            else:
                response_dict = {}
                success = 1
                response_dict[96] = ' internal error prev_Str not passed'
        else:
            if ip_address != None and port != None and community != None:
                response_dict = {}
                temp_dict = {}
                prev_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('unmp_set_agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s), 15, 3)" % (
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

                    exec set_str in locals(), globals()

                    print " ok now "

                    if errorIndication:
                        response_dict[553] = str(errorIndication)
                        success = 1
                        return
                    else:

                        if errorStatus > 0 and errorIndex != None:

                            if state_present == 1 and int(errorIndex) == 1:
                                print "    ok ", response_dict
                                success = 1
                                response_dict[
                                    54] = "NOT ABLE TO LOCK THE DEVICE"
                                return
                            elif state_present == 1 and len(varBinds) == int(errorIndex):
                                print "    ok ", response_dict
                                response_dict[admin_name + '1'] = 55
                                state = 1
                                return pysnmp_set(received_dict, None, None, None, admin_state, prev_str, response_dict,
                                                  temp_dict, error_dict, state)

                            else:
                                print " >>>>>>>>>>>>>>>> YE LE RAHA HAI MERI JAN BHAI ", varBinds[int(errorIndex) - 1]
                                print "    ok ", response_dict
                                print " :::::::: ", errorStatus, " :::::: ", errorIndex
                                response_dict[temp_dict[
                                    varBinds[int(errorIndex) - 1][0]]] = int(errorStatus)
                                error_dict[
                                    varBinds[int(errorIndex) - 1][0]] = 1
                                if len(error_dict) >= len(received_dict):
                                    print " ^^^^^^^^^^^^^^^^^^^^^^ AT ITS MAXIMUM LIMIT^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                                    success = 1
                                    return
                                else:
                                    return pysnmp_set(received_dict, None, None, None, admin_state, prev_str,
                                                      response_dict, temp_dict, error_dict)

                            return

                        elif errorStatus == 0:
                            print " No error State ok every thing>>>>>>>>>"
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
        return final_responce_dict
        # sys.exit(1)


# print ' START llc form\n'
# print pysnmp_set({'ru.ra.llc.raLlcConfTable.frameLossThreshold': ['1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1', 'Gauge32', '429497295']},'172.22.0.120','161','private',{})
# print '\n END '


# print '\n START RA Status form\n'
# print pysnmp_set({'ru.ra.raConfTable.dfs': ['1.3.6.1.4.1.26149.2.2.13.1.1.10.1', 'Integer32', '0'],
#                     'ru.ra.raConfTable.dba': ['1.3.6.1.4.1.26149.2.2.13.1.1.7.1', 'Integer32', '0'],
#                     'ru.ra.tddMac.raTddMacConfigTable.passPhrase': ['1.3.6.1.4.1.26149.2.2.13.7.1.1.2.1', 'OctetString', ''],
#                     'ru.ra.tddMac.raTddMacConfigTable.encryptionType': ['1.3.6.1.4.1.26149.2.2.13.7.1.1.8.1', 'Integer32', '0'],
#                     'ru.ra.raConfTable.ssID': ['1.3.6.1.4.1.26149.2.2.13.1.1.5.1', 'OctetString', 'cscape'],
#                     'ru.ra.raConfTable.acm': ['1.3.6.1.4.1.26149.2.2.13.1.1.8.1', 'Integer32', '0'],
#                     'ru.ra.tddMac.raTddMacConfigTable.txPower': ['1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1', 'Gauge32', '0'],
#                     'ru.ra.raConfTable.acs': ['1.3.6.1.4.1.26149.2.2.13.1.1.9.1', 'Integer32', '0']},
#     '172.22.0.120','161','private',{'ru.ra.raConfTable.raAdminState-1': ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1']})
# print '\n END '


# print '\n START RA Status 2 form\n'
# print pysnmp_set({'ru.ra.raConfTable.anc': ['1.3.6.1.4.1.26149.2.2.13.1.1.14.1', 'Integer32', '0'],
#                     'ru.ra.raConfTable.linkDistance': ['1.3.6.1.4.1.26149.2.2.13.1.1.13.1', 'Integer32', '0'],
#                     'ru.ra.raConfTable.forceMimo': ['1.3.6.1.4.1.26149.2.2.13.1.1.15.1', 'Integer32', '0'],
#                     'ru.ra.raConfTable.numSlaves': ['1.3.6.1.4.1.26149.2.2.13.1.1.11.1', 'Integer32', '10'],
#                     'ru.ra.raConfTable.guaranteedBroadcastBW': ['1.3.6.1.4.1.26149.2.2.13.1.1.6.1', 'Integer32', '1'],
#                     'ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue': ['1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1', 'Gauge32', '1'],
#                     'ru.ra.raConfTable.antennaPort': ['1.3.6.1.4.1.26149.2.2.13.1.1.12.1', 'Integer32', '3'],
#                     'ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors': ['1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1', 'Gauge32', '0']},
#     '172.22.0.120','161','private',{'ru.syncClock.syncConfigTable.adminStatus': ['1.3.6.1.4.1.26149.2.2.11.1.1.2.1']})
# print '\n END '

# form_dict = {'ru.ra.raConfTable.dfs': ['1.3.6.1.4.1.26149.2.2.13.1.1.10.1', 'Integer32', '1'], 'ru.ra.raConfTable.acs': ['1.3.6.1.4.1.26149.2.2.13.1.1.9.1', 'Integer32', '0']}
# admin = {'ru.ra.raConfTable.raAdminState': ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1']}
# port='161'
# ip = '172.22.0.15'
# community = 'private'
# ans = pysnmp_set(form_dict,ip,port,community)
# print ans
# print
######
# form_dict = {'ru.omcConfTable.omcIpAddress': ['1.3.6.1.4.1.26149.2.2.7.1.2.1', 'IpAddress', '172.22.5550']}
##
# port='161'
# community = 'private'
# admin = {'ru.ruConfTable.adminstate-1': ['1.3.6.1.4.1.26149.2.2.11.1.1.2.1']}
##
# ans = pysnmp_set(form_dict,ip,port,community)
# print ans
# print
# form_dict = {'ru.ruConfTable.channelBandwidth': ['1.3.6.1.4.1.26149.2.2.1.1.7.1', 'Integer32', '3'], 'ru.omcConfTable.omcIpAddress': ['1.3.6.1.4.1.26149.2.2.7.1.2.1', 'IpAddress', '172.22.0.95'], 'ru.omcConfTable.periodicStatsTimer': ['1.3.6.1.4.1.26149.2.2.7.1.3.1', 'Unsigned32', '142']}
##
# ans = pysnmp_set(form_dict,ip,port,community,admin)
# print ans
##
##
# part = lambda x :x[x[0:x.rfind('.')-1].rfind('.')+1:len(x)] # A lambda function similar to get_oid_slice
# def get_oid_slice(str_,last_dot):
##    """
##    @author: Rahul Gautam
##
##    @requires: an oid string, and dot count from you want the silce of oid string
##
##    @return: oid_slice of oid string
##    """
##    pos = 0
##    s = str_
##    while last_dot != 0:
##        pos = s.rfind('.')
##        s = s[0:pos-1]
##        last_dot = last_dot-1
##    return str_[pos+1:len(str_)]
##
##
# def other_snmp_set(received_dict,priority_dict,row_status_dict={}):
##    """
##    @author: Rahul Gautam
##
##    @summary: this is a more complicated variant of pysnmp set function
##        currently not applicable
##        70% done
##        mostly useful in case of a row_status_dict creation and peer mac set
##        it adjust them automatically according their oid
##        recursive in nature
##    """
##    #prev_str = "errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', '%s'),cmdgen.UdpTransportTarget(('%s', %s))"%(community,ip_address,port)
##    make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
##    row_present = 0
##    set_str = ''
##    temp_dict = {}
##    if len(row_status_dict) > 0:
##        row_oid, oid_slice, rdatatype, rvalue = row_status_dict.values()[0]
##        row_present = 1
##    for i in xrange(1,len(priority_dict)+1):
##        oid_str,datatype,value = received_dict[priority_dict[i]]
##        if row_present == 1:
##            if int(get_oid_slice(oid_slice,1)) > int(get_oid_slice(oid_str,1)):
##                pass
##            else:
##                a_oid = get_oid_slice(oid_str,1)
##                print row_oid+'.1.'+a_oid
##                roid_tuple = make_tuple(row_oid+'.1.'+a_oid)
##                set_str = set_str+",(%s,v2c.%s(%s))"%(roid_tuple,rdatatype,rvalue)
##        oid_tuple = make_tuple(oid_str)
##        temp_dict[oid_tuple] = received_dict[priority_dict[i]]
##        set_str = set_str+",(%s,v2c.%s('%s'))"%(oid_tuple,datatype,value)
##    set_str = set_str+')'
##    print " first set packet",set_str


# print pysnmp_set({'iduConfiguration.e1PortConfigurationTable.lineType':
# ['1.3.6.1.4.1.26149.2.1.2.3.1.4.2', 'Integer32', 1],
# 'iduConfiguration.e1PortConfigurationTable.lineCode':
# ['1.3.6.1.4.1.26149.2.1.2.3.1.5.2', 'Integer32', 1],
# 'iduConfiguration.e1PortConfigurationTable.clockSource':
# ['1.3.6.1.4.1.26149.2.1.2.3.1.3.2', 'Integer32', 1]}, '172.22.0.104',
# '8001', 'private', {'adminState': ['1.3.6.1.4.1.26149.2.1.2.3.1.2.2',
# 'Integer32', 0]})
