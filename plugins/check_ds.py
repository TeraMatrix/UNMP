#! /usr/bin/python2.6 -tt
import socket
import binascii
import time
import sys
import MySQLdb
import logging
import os
logging.basicConfig(filename='/omd/daemon/log/DS_nagiosPlugin.log',
                    format='%(levelname)s: %(asctime)s >> %(message)s', level=logging.DEBUG)


MySql_file = '/omd/daemon/config.rg'
if(os.path.isfile(MySql_file)):    # getting variables from config file
    execfile(MySql_file)
else:
    sys.exit()


def dumphex(s):
    """
    Returns Hexa decimal dump of received data from device into a list
    """
    bytes = map(lambda x: '%.2x' % x, map(ord, s))
    return bytes


def get_header(bytes):
    """
    Returns Header in the form of a list :: required parameter is complete packet in the form of Hexadecimal list
    """
    header = [bytes[i] for i in xrange(0, 16)]
    return header


def get_payload(bytes):
    """
    Returns payload as a list :: required parameter is complete packet in the form of Hexadecimal list
    """
    payload = [bytes[i] for i in xrange(16, len(bytes))]
    return payload


def decode_header(header):
    """
    Returns Decoded the Header in the form of a dictionary{'param_name':'param_value'} :: required paramenter is Header as a Hexadecimal list
    """
    bytes = header
    ne_id = [bytes[i] for i in xrange(0, 4)]
    cmd_id = [bytes[i] for i in xrange(4, 8)]
    cmd_status = [bytes[i] for i in xrange(8, 12)]
    len_of_payload = [bytes[i] for i in xrange(12, 14)]
    param_count = [bytes[i] for i in xrange(14, 15)]
    tx_id = [bytes[i] for i in xrange(15, 16)]

    decoded_header_list = {}

    decoded_header_list['tx_id'] = int_decode(tx_id)
    decoded_header_list['param_count'] = int_decode(param_count)
    decoded_header_list['len_of_payload'] = int_decode(len_of_payload)
    decoded_header_list['cmd_status'] = int_decode(cmd_status)
    decoded_header_list['cmd_id'] = int_decode(cmd_id)
    decoded_header_list['ne_id'] = int_decode(ne_id)

    return decoded_header_list


def decode_payload(payload, param_count):
    """
    Returns Decoded the Header in the form of a dictionary{'param_name':'param_value'}
    :: required paramenters (Payload as a Hexadecimal list, param_count field from decoded header as int
    """
    count = param_count  # param_count comes from Header part
    payload = payload
    decoded_payload = {}
    length_payload = len(payload)
    # print ' payload length ',length_payload
    i = 0
    l = 0
    if count != 0:
        while count > 0:
            subtract = 0

            param_name = [payload[k] for k in xrange(i, i + 2)]
            i = i + 2
            pn = int_decode(param_name)    # pn is decoded param name
            pn = str(pn)

            value_type = [payload[k] for k in xrange(i, i + 1)]
            i = i + 1

            value_size = [payload[k] for k in xrange(i, i + 1)]
            j = int_decode(value_size)    # j is decoded Value_size
            i = i + 1
            # print ' j value is ',value_size,' decoded ',j

            param_value = [payload[k] for k in xrange(i, i + j)]
            i = i + j

            # print ' i is now ',i
            subtract = i - l
            length_payload = length_payload - subtract
            # print 'pay load now is ',length_payload
            l = i

            decoded_payload[pn] = string_decode(param_value)
            count = count - 1
        pass

    return decoded_payload


def long_decode(li_st):
    """
    decode long type of list value, return long value:: parameter (list)
    """
    li_st = li_st
    li_str = ''.join(li_st)
    li_str = '0x' + li_str
    decoded_data = long(li_str, 16)
    return decoded_data


def int_decode(li_st):
    """
    decode int type of list value, return int value :: parameter (list)
    """
    li_str = ''.join(li_st)
    li_str = '0x' + li_str
    decoded_data = int(li_str, 16)
    return decoded_data


def string_decode(li_st):
    """
    decode list value, return as a string value :: parameter (list)
    """
    li_st = li_st
    string_value = ''
    for li in li_st:
        string_value = string_value + chr(int(li, 16))
    return string_value


def asciirepr(hexs):
    """
    replace the hexadecimal characters with ascii characters
    """
    data = hexs
    return binascii.unhexlify(data)


def hexrepr(hexs):
    """
    replace the ascii characters with hexadecimal characters (never used in that program)
    """
    data = hexs
    return binascii.hexlify(data)


def db_connect():
    """
    Used to connect to the database :: return database object assigned in global_db variable
    """
    db = None
    try:
        db = MySQLdb.connect(hostname, username, password, schema)
        # logging.info(" $$$ $$$ Database Connect successful ")
        # print 'db connect successful'
        return db
    except MySQLdb.Error as e:
        logging.error(
            "/*/*/* MYSQLdb Exception (db connect) : " + str(e))  # print str(e)
    except Exception as e:
        logging.error("/*/*/* Database Exception (db connect) : " + str(
            e))  # print "Exception in database connection "+str(e)


def db_close(db):
    """
    closes connection with the database
    """
    try:
        db.close()
        # logging.info(" $$$ $$$ Database Connection closed ")
    except Exception as e:
        logging.error("/*/*/* Database Exception ( db close ) : " + str(e))


def main():
    db = None
    try:
        dict_for_nagios = {}
        NOT_UP = 1
        some_problem = 1  # shows criticalness
        set_devices = 0
        total_devices = 0
        server_ip = nms_ip         # discovery server ip
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(40)
        s.connect((server_ip, 6790))
        first = asciirepr('00000000000007d10000000000000001')
        second = asciirepr('00000000000007d30000000000000002')
        third = asciirepr('00000000000007d50000000000000003')
        sending_data = []
        sending_data.append(third)
        sending_data.append(second)
        sending_data.append(first)

        # print " up "
        while 1:
            if len(sending_data) == 0:
                # print " hi"
                break
            s.send(sending_data.pop())
            data = s.recv(1024)
            # print " ok "
            if data:
                hex_data_list = dumphex(data)
                decoded_header = decode_header(get_header(hex_data_list))
                #
                # each field of decoded Header
                ne_id = decoded_header['ne_id']
                cmd_id = decoded_header['cmd_id']
                cmd_status = decoded_header['cmd_status']
                len_of_payload = decoded_header['len_of_payload']
                param_count = decoded_header['param_count']
                tx_id = decoded_header['tx_id']
                # print param_count
                # print get_payload(hex_data_list)
                # decoded Payload
                decoded_payload = decode_payload(
                    get_payload(hex_data_list), param_count)
                # print decoded_payload
                #
                # print ' >>>>>>>>>>>>> cmd_id is ',cmd_id,' and cmd_status is
                # ',cmd_status,' & Transaction id is ',tx_id,' ne_id is ',ne_id
                if cmd_id == 2002:
                    if cmd_status == 0:
                        NOT_UP = 0
                        some_problem = 0
                    else:
                        NOT_UP = 1
                if cmd_id == 2004:
                    if cmd_status == 0:
                        NOT_UP = 0
                        some_problem = 0
                        dict_for_nagios = decoded_payload  # 3000 is no of processes running 3010 is no of threads
                    else:
                        some_problem = 1
                if cmd_id == 2006:
                    if cmd_status == 0:
                        NOT_UP = 0
                        some_problem = 0
                        try:
                            db = db_connect()
                            cursor = db.cursor()
                            query = 'select count(ne_id) from tcp_discovery'
                            if cursor.execute(query) != 0:
                                total_devices = cursor.fetchone()[0]
                            query = 'select count(ne_id) from tcp_discovery where is_set = 0'
                            if cursor.execute(query) != 0:
                                set_devices = cursor.fetchone()[0]
                            cursor.close()
                            db_close(db)
                        except MySQLdb.Error as e:
                            logging.error(
                                "/*/*/* MYSQLdb Exception (db connect) : " + str(e))  # print str(e)
                        except Exception as e:
                            logging.error("/*/*/* Database Exception (db connect) : " +
                                          str(e))  # print "Exception in database connection "+str(e)

                    else:
                        some_problem = 1

    except socket.timeout:
        NOT_UP = 1
        # print " exception timout "
        # s.shutdown(SHUT_RDWR)
        s.close()
    except socket.error as (sock_errno, sock_errstr):
        NOT_UP = 1
        # error = " S"
        # print " exception ",str(sock_errno),"  : ",str(sock_errstr)
        # s.shutdown(SHUT_RDWR)
        s.close()
    finally:
        s.close()
        # print dict_for_nagios
        if '3020' in dict_for_nagios:
            threads_no = dict_for_nagios['3020']
        else:
            NOT_UP = 1
            some_problem = 1
            threads_no = 'not recieved'
        if '3010' in dict_for_nagios:
            some_problem = 0
            process_no = dict_for_nagios['3010']
        else:
            process_no = 'not recieved'
        if '3000' in dict_for_nagios:
            if dict_for_nagios['3000'] == '1':
                some_problem = 0
                ds_state = " DataBase connection is OK "
            else:
                some_problem = 1
                ds_state = " DataBase is NOT connected "
        else:
            ds_state = 'not recieved'
        if NOT_UP == 0 and some_problem == 0:
            print " UNMP - Discovery Server is Running 	Health state : OK"
            print " Number of open Threads   : %s " % str(threads_no)
            print " Number of open Process   : %s " % str(process_no)
            print " Number of Total Devices  : %s " % str(total_devices)
            print " Number of SET Devices    : %s " % str(set_devices)
            print ds_state
            sys.exit(0)
        if NOT_UP == 0 and some_problem == 1:
            print " UNMP - Discovery Server is Running 	Health state : Warning"
            print " Number of Total Devices  : %s " % str(total_devices)
            print " Number of SET Devices    : %s " % str(set_devices)
            print " Number of open Threads   : %s " % str(threads_no)
            print " Number of open Process   : %s " % str(process_no)
            print ds_state
            sys.exit(1)
        if NOT_UP == 1 and some_problem == 1:
            print " UNMP - Discovery Server is NOT running 	   Health state : Critical"
            print " Number of Total Devices  : %s " % str(total_devices)
            print " Number of SET Devices    : %s " % str(set_devices)
            sys.exit(2)
        else:
            print " UNMP - Discovery Server is NOT running      Health state : UnKnown"
            print " Number of open Threads   : %s " % str(threads_no)
            print " Number of open Process   : %s " % str(process_no)
            print " Number of Total Devices  : %s " % str(total_devices)
            print " Number of SET Devices    : %s " % str(set_devices)
            print ds_state
            sys.exit(3)

        # print " OUTPUT : NOT_UP : ",NOT_UP," || dict_for_nagios :
        # ",dict_for_nagios," || total devices : ",total_devices," ||
        # set_devices : ",set_devices," || "

if __name__ == '__main__':
    main()
