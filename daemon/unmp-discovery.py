#!/usr/bin/python2.6
"""
Description : VNL Unicast Discovery of different Devices for NMS(UNMP)

ServiceName: unmp-ds

Author : Rahul Gautam

Date: 22-Aug-2011

(CodeScape Consultants Pvt. Ltd.) 
"""
#
from daemon import Daemon		        # my custom Daemon class that daemonize my discovery server
#
from signal import signal, SIGTERM      # for handling kill signal
import socket
import thread
import threading
import time
import sys
import string
import binascii
import MySQLdb
from xml.dom.minidom import parse,Node
import os.path
from multiprocessing import Process,Event
from threading import Thread
from datetime import datetime, timedelta
import multiprocessing
import logging
logging.basicConfig(filename='/omd/daemon/log/unmp-discovery.log',format='%(levelname)s: %(asctime)s >> %(message)s', level=logging.DEBUG)



##################################################
##                                              ##    
##      Author- Rahul Gautam                    ##
##                                              ##    
##      VNL Unicast Discovery                   ##  
##      of different Devices                    ##
##                                              ##
##    CodeScape Consultants Pvt. Ltd.           ##
##                                              ##
##################################################



## PLEASE DON'T DELETE ANY COMMENT IN THIS FILE - Rahul Gautam

## loading configuration file in Discovery Server
config_location = '/omd/daemon/config.rg'         # config file's location

if(os.path.isfile(config_location)):              # getting variables from config file    
        execfile(config_location)
else:
    logging.critical(' !!!! Please check the Configuration file location : current location is > '+str(config_location)+' <  !!!!\n ****server is exiting****')
    sys.exit()
##

## global variables Description
db_status = 1
global_db = None
db_events_dict = {}
thread_count = 160                  # change this variable if you want to spawn more than 100 threads in this main process
status_dict = {}                    # used for event related continuous failure count for device error_no = 1 {device_ip : failure_count} 
thread_dict = {}                    # { DsThread object : client socket object}
process_list = []                   
sock_dict = {}                      # { client socket object : if set then 0 if not set then 1 }
nms_ip = '127.0.0.1'                     # comes from config file
#nms_ip = nms_ip                     # comes from config file
server_ip_addr = server_ip_addr    # getting your eth0 ip address OR you can set it manually here 
sock_list = []                      # socket list
process_dict = {}
process_event = {}
thread_list = []                    # thread list
device_toWatch = []
rule_variable = 0                   # this variable is specially used for checking purpose (its just like an alert for you that too many devices sending cmd_status == 1 so you have to check manually)
                                    # u can remove that rule_variable

sys_omc_tuple =   ('sys_omc_register_active_card_hwld','product_id','sys_omc_registerne_country','sys_omc_registerne_state','sys_omc_registerne_city','sys_omc_registerne_sitebldg','sys_omc_register_contact_person','sys_omc_register_contact_mobile','sys_omc_register_alternate_contact','sys_omc_register_contact_email','sys_omc_register_contact_addr','sys_omc_registerne_sitefloor','sys_omc_registerne_site_direction','sys_omc_registerne_site_landmark','site_mac','sys_omc_registerne_site_longitude','sys_omc_registerne_site_latitude','ip_address')


device_defaultInfo_dict = {'2051': '0000', '2053': 'India', '2052': '6021', '2055': 'Jaipur', '2054': 'Rajasthan', '2057': 'Peeyush', '2056': 'mayur apartment', '2059': '1234567890', '2058': '9876543210', '2060': 'praj@cscape.in', '2061': 'civil lines', '2062': 'floor', '2063': 'right', '2064': 'B1', '2065': '', '2066': '75.05', '2067': '26.06'}

##################


class State_exception(Exception):
    """
    used to raise an exception for if rule_variable's value is exceeding 200 
    """
    def __init__(self):
        pass
    def __str__(self):
        return " !!!!  this Exception is raise because more then 200 devices sending cmd_status UNSUCCESSFUL please CHECK SPECIFICS like entries in config.xml (if everything is ok then restart please and remove the rule_variable+1 entry from this file "

def get_xmlattribute(param_id):
    """ 
    used for retrieving information from rgconfig.xml file (not used because configuration file has custom .rg extention)
    """
    if(os.path.isfile(config_location)):
        f = parse(config_location)
        doc = f.documentElement.getElementsByTagName('param')
        for node in doc:
            if node.getAttribute('id') == param_id:
                param_value = node.getAttribute('value')
    return param_value    




def print_dumphex(s):
    """
    print hex data ::not used in program 
    """
    bytes = map(lambda x: '%.2x' % x, map(ord, s))
    for i in xrange(0,len(bytes)/16):
        print '    %s' % string.join(bytes[i*16:(i+1)*16],' ')
    print '    %s' % string.join(bytes[(i+1)*16:],' ')


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
    header=[bytes[i] for i in xrange(0,16)]
    return header

def get_payload(bytes):
    """
    Returns payload as a list :: required parameter is complete packet in the form of Hexadecimal list
    """
    payload=[bytes[i] for i in xrange(16,len(bytes))]
    return payload

def decode_header(header):
    """
    Returns Decoded the Header in the form of a dictionary{'param_name':'param_value'} :: required paramenter is Header as a Hexadecimal list 
    """
    bytes = header
    ne_id = [bytes[i] for i in xrange(0,4)]
    cmd_id = [bytes[i] for i in xrange(4,8)]
    cmd_status = [bytes[i] for i in xrange(8,12)]
    len_of_payload = [bytes[i] for i in xrange(12,14)]
    param_count = [bytes[i] for i in xrange(14,15)]
    tx_id = [bytes[i] for i in xrange(15,16)]

    decoded_header_list = {}
    
    decoded_header_list['tx_id']=int_decode(tx_id)
    decoded_header_list['param_count']=int_decode(param_count)
    decoded_header_list['len_of_payload']=int_decode(len_of_payload)
    decoded_header_list['cmd_status']=int_decode(cmd_status)
    decoded_header_list['cmd_id']=int_decode(cmd_id)
    decoded_header_list['ne_id']=int_decode(ne_id)

    return decoded_header_list
    

def decode_payload(payload,param_count):
    """
    Returns Decoded the Header in the form of a dictionary{'param_name':'param_value'} 
    :: required paramenters (Payload as a Hexadecimal list, param_count field from decoded header as int 
    """
    count = param_count    ### param_count comes from Header part
    payload = payload    
    decoded_payload = {}
    length_payload = len(payload)
    i = 0
    l = 0
    if  count != 0:    
        while count > 0:
            subtract = 0
            
            param_name = [payload[k] for k in xrange(i,i+2)]
            i=i+2            
            pn = int_decode(param_name)    # pn is decoded param name
            pn = str(pn)

            value_type = [payload[k] for k in xrange(i,i+1)]
            i=i+1
            
            value_size = [payload[k] for k in xrange(i,i+1)]
            j = int_decode(value_size)    # j is decoded Value_size
            i = i+1                        
            param_value = [payload[k] for k in xrange(i,i+j)]
            i= i+j
            
            subtract = i - l
            length_payload = length_payload - subtract
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
    li_str ='0x'+li_str
    decoded_data = long(li_str,16)
    return decoded_data

def int_decode(li_st):
    """
    decode int type of list value, return int value :: parameter (list)
    """
    li_str = ''.join(li_st)
    li_str ='0x'+li_str
    decoded_data = int(li_str,16)
    return decoded_data


def string_decode(li_st):
    """
    decode list value, return as a string value :: parameter (list)
    """
    li_st = li_st
    string_value = ''
    for li in li_st:
        string_value = string_value+chr(int(li,16)) 
    return string_value

def int_encode(int_value,bytes):
    """
    used for converting int value in hex, Returns string value (that contains Hex format) :: parametwrs (int value,and how many bytes that int value is to be hold) 
    """
    int_value = int(int_value)
    bytes = bytes*2
    hex_list = []
    hx_v = hex(int_value)           #contains hex_value
    st_v = str(hx_v)                #contains string value
    st_v = st_v[2:len(st_v)]
    net_length = bytes - len(st_v)
    str_v = ''                      #new Variable
    for i in xrange(0,net_length):
        str_v = str_v+'0'
    str_v = str_v+st_v              #it contains rectified hex value string
    hex_list = make_list(str_v)        
    hex_str = make_str(hex_list)
    return hex_str
    

def string_encode(str_v):
    """
    used for converting string in hex, Returns string (that contains Hex format) :: parameter (string value) 
    """
    str_v = str_v
    temp_list = [ord(i) for i in str_v]
    hex_list = []
    for i in temp_list:
        temp = hex(i)
        temp1 = temp[2:len(temp)]
        hex_list.append(temp1)
    hex_str = make_str(hex_list)
    return hex_str

def make_header(rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id):
    """
    used for making Header in hex format, Returns header in string (that contains hex format) :: all Header fields as parameter 
    """
    rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id = rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id
    str_header = ''
    str_header = str_header+int_encode(rne_id,4)
    str_header = str_header+int_encode(rcmd_id,4)
    str_header = str_header+int_encode(rcmd_status,4)
    str_header = str_header+int_encode(rlen_of_payload,2)
    str_header = str_header+int_encode(rparam_count,1)
    str_header = str_header+int_encode(rtx_id,1)
    return str_header

def make_param(rparam_name,rparam_size,rparam_value):
    """
    used for making payload misc_parameter, return as a String (that contains hex format) :: parameters (parameter_name as int, param_size as int, param_value as string)
    """
    rparam_name,rparam_size,rparam_value = rparam_name,rparam_size,rparam_value
    rparam_type = 1
    str_param = ''
    str_param = str_param+int_encode(rparam_name,2)
    str_param = str_param+int_encode(rparam_type,1)
    str_param = str_param+int_encode(rparam_size,1)
    str_param = str_param+string_encode(rparam_value)
    return str_param
    
    
def make_list(str_v):
    """
    returns list of a String Value :: parameter(string_value) 
    """
    str_v = str_v
    j = 0    
    li_st = []
    for i in xrange(0,len(str_v)/2):
        ele = str_v[j:j+2]
        j = j+2
        li_st.append(ele)
    return li_st


def make_str(hex_list):
    """ 
    returns string (that contains hex format) :: parameter(list)
    """ 
    hex_str = ''                    # hex_str is continuous string representation of hex output
    hex_list = hex_list
    for i in hex_list:
        hex_str = hex_str+i
    return hex_str


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
    global db_events_dict,global_db,db_status
    try:
        db = MySQLdb.connect(hostname,username,password,schema)
        global_db = db
        logging.info(" $$$ $$$ Database Connect successful ")
        db_status = 0
    except MySQLdb.Error as e:
        logging.error("/*/*/* MYSQLdb Exception (db connect) : "+str(e)) 
    except Exception as e:
        logging.error("/*/*/* Database Exception (db connect) : "+str(e)) 

def db_close():
    """
    closes connection with the database
    """
    global global_db
    try:
        global_db.close()
    except Exception as e:
        logging.error("/*/*/* Database Exception ( db close ) : "+str(e))
    
def db_reconnect():
    """
    Used to Re-connect to the database if db is not connected :: return database object assigned in global_db variable
    """
    global db_events_dict,global_db
    db = None
    try:
        db = MySQLdb.connect(hostname,username,password,schema)
        global_db = db
        logging.info(" $$$ $$$ Database Re-Connect successful ")
        return 0
    except MySQLdb.Error as e:
        logging.error("/*/*/* MYSQLdb Exception (db Re-connect) : "+str(e)) 
        return 1
    except Exception as e:
        logging.error("/*/*/* Database Exception (db Re-connect) : "+str(e))    
        return 1
    


def db_get_neid(dip):
    """
    returns ne_id of device if device is previously registered
    """
    try:
        global global_db,db_status
        neid_value = None
        query = "select ne_id from tcp_discovery where ip_address = '%s' "%dip
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            neid_value = cursor.fetchone()[0]
        cursor.close()
        return neid_value            
    except MySQLdb.Error as e:
        logging.error("/*/*/* MYSQLdb Exception (get ne_id) : "+str(e))
        if str(e).find('2006') >= 0 or str(e).find('2014') >= 0:
            db_status = 1            
            return -1
    except Exception as e:
        logging.error("/*/*/* Database Exception (get ne_id) : "+str(e))
        
def db_registration(db_entries,dip):
    """
    this functions used for inserting all the details of device in the database received in registration(2001) step
    """
    try:
        global global_db,db_events_dict,sys_omc_tuple,db_status,device_defaultInfo_dict
        une_id = db_get_neid(dip)
        cursor = global_db.cursor()
        #val_tupl = tuple([db_entries[str(2051+i)] for i in xrange(len(db_entries))])
        #logging.info(" TEST  "+str(val_tupl))
        v_list = []
        for i in xrange(len(db_entries)):
            if str(db_entries[str(2051+i)]).find("populated") >= 0:
                v_list.append(device_defaultInfo_dict[str(2051+i)])
            else:
                v_list.append(db_entries[str(2051+i)])
        val_tuple = tuple(v_list)
#        val_tuple = tuple([db_entries[str(2051+i)] for i in xrange(len(db_entries))])
        #logging.info(" TEST TEST "+str(val_tuple))
        if une_id == None:  
            query = "insert into tcp_discovery (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%sys_omc_tuple+" values('%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"%val_tuple+"'%s')"%dip
            cursor.execute(query)
        else:
            u_list = []
            for i in range(0,len(sys_omc_tuple)):
                u_list.append(sys_omc_tuple[i])
                if i == len(sys_omc_tuple)-1:
                    u_list.append(dip)
                else:
                    u_list.append(val_tuple[i])
                           
            update = tuple(i for i in u_list)
            query = "update tcp_discovery %s = '%s',%s = %s,  %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s', %s = '%s',"%update
        global_db.commit()
        cursor.close()
        return une_id
    except MySQLdb.Error as e:
        logging.error("/*/*/* MYSQLdb Exception (Registration) : "+str(e))
        if str(e).find('2006') >= 0 or str(e).find('2014') >= 0:
            db_status = 1            
            return -1
    except Exception as e:
        logging.error("/*/*/* Database Exception (Registration) : "+str(e))
        


    
def db_set_device(dip,status):
    """
    when device is properly configured then this method set the is_set field to 0 in tcp_health_check table and also reset the health_check field
    """
    
    try:
        global global_db
        cursor = global_db.cursor()
        query = "UPDATE tcp_discovery SET is_set = 0 WHERE ip_address = '%s' "%(dip)
        cursor.execute(query)
        global_db.commit()
        query = "select timestamp from tcp_health_check where ip_address='%s' "%dip
        if cursor.execute(query) != 0:
            tstamp = cursor.fetchone()[0]
            query = "update tcp_health_check set health_check = 0, last_timestamp = '%s' where ip_address='%s' "%(tstamp,dip)
        else:
            neid = db_get_neid(dip)
            query = "insert into tcp_health_check (ne_id,ip_address) values(%s,'%s') "%(neid,dip)
       
        cursor.execute(query)
        global_db.commit()
        cursor.close()
    except MySQLdb.Error as e:
        logging.error("/*/*/* MYSQLdb Exception (set device) : "+str(e))     
    except Exception as e:
        logging.error("/*/*/* Database Exception (set device) : "+str(e))
       
    
    
def db_health_check(dip):
    """
    this function insert device health_check in tcp_health_check table
    """
    
    try:
        global global_db
        query = "select health_check from tcp_health_check where ip_address='%s' "%dip
        cursor = global_db.cursor()
        cursor.execute(query)
        health_check = cursor.fetchone()[0]
        health_check += 1
        query = "update tcp_health_check set health_check=%s where ip_address = '%s' "%(health_check,dip)
        cursor.execute(query)
        global_db.commit()
        cursor.close()
    except MySQLdb.Error as e:
        logging.error("/*/*/* MYSQLdb Exception (health_check) : "+str(e))
    except Exception as e:
        logging.error("/*/*/* Database Exception (health_check) : "+str(e))
        
        
def db_device_disconnet(dip):
    """
    used to enter the disconnect information of device
    """
    try:
        global global_db
        query = "select timestamp from tcp_health_check where ip_address='%s' "%dip
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            tstamp = cursor.fetchone()[0]
            if (datetime.now() - tstamp) > timedelta (seconds = 180):
                query = "update tcp_health_check set health_check = -1,  last_timestamp= '%s' where ip_address='%s' "%(tstamp,dip)
                cursor.execute(query)
                global_db.commit()
        cursor.close()
    except MySQLdb.Error as e:
        logging.error("/*/*/* MYSQLdb Exception (device disconnect) : "+str(e)) 
    except Exception as e:
        logging.error("/*/*/* Database Exception (device disconnect) : "+str(e)) 
    
def db_events():
    """
    this function used by EventThread to insert Event in daemon Event table
    """   
    pass



class DsThread(threading.Thread):
    """
    Thread that handles socket communication with device in main process
    """
    
    def __init__(self,csock,clip,clport):
        """ 
        init parameters for DsThread class is client socket object,client ip,client port,
        """ 
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self.clisock=csock          # client socket
        self.clip=clip              # client ip
        self.clport=clport          # client port
        
    
    def join(self,timeout=None):
        """
        Stop the thread
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        
    def recieve_send(self):
        """ 
        used for receive and sending data to the device 
        """
        global sock_list,rule_variable,sock_dict,thread_list,status_dict,config_responce,db_events_dict,ccu_responce
        ne_id,cmd_id,cmd_status,len_of_payload,param_count,tx_id = 0,0,1,0,0,0      # only initilization
        count = 0                                                                   # defining param_count
        
        device_response = config_responce
        
        cmd_set = 0
        
        try:    
            while not self._stopevent.isSet():            
                                        
                data,addrs=self.clisock.recvfrom(512)
                                
                if data:
                    if global_db.open != 1: db_connect()
                        
                    hex_data_list = dumphex(data)
                    #                    
                    # decoded Header
                    decoded_header = decode_header(get_header(hex_data_list))
                    #
                    # each field of decoded Header
                    ne_id = decoded_header['ne_id']
                    cmd_id = decoded_header['cmd_id']
                    cmd_status = decoded_header['cmd_status']
                    len_of_payload = decoded_header['len_of_payload']
                    param_count = decoded_header['param_count']
                    tx_id = decoded_header['tx_id']
                    #
                    # decoded Payload        
                    decoded_payload = decode_payload(get_payload(hex_data_list),param_count)
                    #logging.info(str(decoded_payload))
                    
                    ## REGISTRATION_RESPONCE
                    if cmd_id == 2001:    # confirming that this is REG_REQ
                        if cmd_status == 0:
                            # defining HEADER Variables
                            # preciding with r denotes that this is reply
                            db_entries = decoded_payload
                            
                            if str(decoded_payload['2052']) == '6040':  # modify it config_responce dict in 
                                device_response = ccu_responce                               
                            
                            rne_id = ne_id
                            rcmd_id = 2002    #or we can say cmd_id+1
                            rcmd_status = 0
                            rlen_of_payload = 0
                            rparam_count = 0
                            rtx_id = tx_id
                            #
                            encoded_header = make_header(rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id)
                            
                            reg_resp = asciirepr(encoded_header)    # Header in sendable format
                            
                            self.clisock.send(reg_resp)
                            
                            une_id = db_registration(db_entries,self.clip)
                            if une_id == None: une_id = db_get_neid(self.clip)
                            if une_id == -1 :
                                logging.error( " #@! #@! *** device connction is closing in DsThred beacuse DB is NOT connected "+str(self.clip)+':'+str(self.clport))
                                break                           

                                
                            
                        else:
                            logging.error( " #@! #@! *** device cmd_status is *1* on 2001 UNEXPECTED  **** "+str(self.clip)+':'+str(self.clport))
                            break
                        
                    ##

                    ## CONFIG RESPONCE                        
                    if cmd_id == 2003:    # confirming that this is CONFIG_REQ
                        if cmd_status == 0:
                            # defining PAYLOAD
                            # defining each_param_group then combining as a payload
                            # first param  = FTP_SERVER_IP
                            # second param = OMC_HOME
                            # third param  = SNMP_REQUEST_PORT
                            # four param   = SNMP_WRITE_COMMUNITY_PREFIX
                            # five param   = SNMP_READ_COMMUNITY_PREFIX
                            # six param    = SNMP_TRAP_PORT 
                            # seven param  = NE_ID
                            # eight param  = FTP_USER_NAME
                            # nine param   = FTP_USER_PASSWORD
                            param_list = ['2077','2075','2068','2071','2070','2069','2078','2072','2073']    # the order in which parameters have to be bound
                            payload = ''
                            count = 0
                            for i in param_list:                    
                                if count == 6:
                                    if une_id == 0:
                                        db_connect()
                                        une_id = db_get_neid(self.clip)
                                    rparam_value = str(une_id)
                                    rparam_size = len(str(rparam_value))
                                    rparam_name = param_list[6]
                                    payload = payload+make_param(rparam_name,rparam_size,rparam_value)
                                else:
                                    rparam_name = i
                                    rparam_value = device_response[rparam_name] 
                                    rparam_size = len(rparam_value)
                                    payload = payload+make_param(rparam_name,rparam_size,rparam_value)
                                count = count+1
                            #
                            # defining HEADER Variables
                            # preceding with r denotes that this is reply
                            rne_id = ne_id
                            rcmd_id = 2004    #or we can say cmd_id+1
                            rcmd_status = 0
                            rlen_of_payload = len(payload)/2
                            rparam_count = count
                            rtx_id = tx_id
                            encoded_header = make_header(rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id)
                            #
                            config_resp = asciirepr(encoded_header+payload)               
                            self.clisock.send(config_resp)
                            #
                        else:
                            logging.error( " #@! #@! *** device cmd_status is *1* UNEXPECTED  **** "+str(self.clip)+':'+str(self.clport))
                            break
                        
                    
                    ##
                
                    # FINAL RESPONCE
                    if cmd_id == 2005:                    
                        if cmd_status == 0:         # confirming that this is REG_REQ
                            
                            # defining HEADER Variables
                            # preceding with r denotes that this is reply
                            rne_id = ne_id
                            rcmd_id = 2006          #or can have cmd_id+1
                            rcmd_status = 0
                            rlen_of_payload = 0
                            rparam_count = 0
                            rtx_id = tx_id
                            #
                            encoded_header = make_header(rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id)
                            
                            reg_resp = asciirepr(encoded_header)    # Header in send_able format
                            
                            self.clisock.send(reg_resp)
                            logging.info("$$$ $$$   ***** Device "+str(self.clip)+':'+str(self.clport)+" added successfully with NE_ID : "+str(ne_id)+"*****  ##")
                            sock_dict[self.clisock] = 0
                            status_dict[self.clip] = 0
                            db_set_device(self.clip,cmd_status)
                            cmd_set = 1
                            
                            break                       
                                                 
                            
                        else:
                            logging.error( " #@! #@! ** still having some problem in 2005 ****(check ftp server settings in config.rg)**** "+str(self.clip)+':'+str(self.clport))
                            break
                        

                else:         
                    pass
            
        except socket.timeout:
            logging.error("%%%%%%%  Socket timeOUT Exception in Dsthread : "+self.clip+':'+str(self.clport))
            self.clisock.close()
            if global_db.open == 1:            
                db_device_disconnet(self.clip)
            else:
                db_connect()
            
        except Exception as e:
            logging.error("% % % % % % %  Exception in DsThread "+str(e))
            self.clisock.close()            
            if global_db.open == 1:
                db_device_disconnet(self.clip)
            else:
                db_connect()        
            

        finally:
            temp_status = status_dict[self.clip]
            if temp_status > 0:
                status_dict[self.clip] = temp_status + 1
            if cmd_set == 0:
                self.clisock.close()            
                db_device_disconnet(self.clip)
                        
                            
            

    def run(self):
        logging.info(" $$$ $$$ thread start for device > "+str(self.clip)+" : "+str(self.clport))
        self.recieve_send()
        logging.info(" $$$ $$$ ****DsThread Exiting for deivce "+str(self.clip)+" : "+str(self.clport)) 
        

## ************ class DsThread is End here ********************        


        


class PsThread(threading.Thread):
    """
    PsThread is a Monitoring thread that spawns a process when thread count in main process is reach to the value of thread_count global variable
    """
    def __init__(self):
        """
        init paramenter for PsThread 
        """
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        
    def join(self,timeout=None):
        """
        Stop the thread
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        
    def run(self):
        global process_dict,thread_count,global_db,process_event,thread_list
        psock_list = []                                             # list that holds sockets in it those we transfer to the process
        special_count = 0  
        try:
            logging.info(" $$$ $$$ PSThread is started ")
            while not self._stopevent.isSet():                      # if stop_event is set by main process then this PsThread exits from the loop
                time.sleep(30)                                      # PsThread sleeps for 30 secs
                
                if len(thread_list) > 0 or len(psock_list) > 0:          # check if thread count reach to that point when we have to spawn a process
                    global thread_dict,sock_dict
                    for dthread in thread_dict.keys():
                        
                        if dthread.isAlive() == True:
                            pass                            
                        else:
                            temp_sock = thread_dict[dthread]
                            if sock_dict[temp_sock] == 0:
                                thread_list.remove(dthread)     # write something #@!            #@!            
                                thread_dict.pop(dthread)
                                psock_list.append(temp_sock)    
                                sock_dict.pop(temp_sock)
                                if len(psock_list) > 70:
                                    special_count = 0
                                    break
                                else:
                                    special_count = special_count + 1
                    else:
                        special_count = special_count + 1                        
                    
                    if len(psock_list) > 0:
                        if len(psock_list) > 69 or special_count > 3:
                            special_count = 0
                            event = Event()
                            p = Process(target=process_function, args=(psock_list,event,global_db))                                
                            p.start()
                            process_dict[p] = len(psock_list)
                            process_event[p] = event 
                            for isock in psock_list:      
                                isock.close()                           #closing socket handlers from main process  
                            psock_list = []
                    else :
                        pass                                 
                else:
                    pass                                
        except Exception as e:
            logging.error(" % % % % % Exception in Psthread : "+str(e))
        finally:            
            logging.info(" //// Psthread is exiting  ")
  

############################################################################################################################################################


######### target function for child-process
 
def process_function(psock_list,event,global_db):
    """
    this is the target function for Process that spawns by PsThread it accepts sockets list and an Event object from main process 
    """
    try:
        
        count = 1
        sock_count = len(psock_list)
        logging.info(" $$$ $$$ spawned process is up having no of sockets : "+str(sock_count))
        if sock_count  > 50: 
            min_sock = 30
        elif sock_count  >= 35 and sock_count < 50:
            min_sock = 20
        elif sock_count  >= 25 and sock_count < 35:
            min_sock = 15
        elif sock_count  >= 19 and sock_count < 25:
            min_sock = 10
        elif sock_count  >=11 and sock_count < 19:
            min_sock = 5
        elif sock_count  >=5 and sock_count < 11:
            min_sock = 2
        elif sock_count  >2 and sock_count < 5:
            min_sock = 1
        elif sock_count >=1 and sock_count < 3:
            min_sock = 1
        #iptx_dict = {}                      # this dictionary keeps track of transaction id for a particular device {device_ip:tx_id}
        while not event.is_set():            # if event is set by main process then this process exits from the loop
            if len(psock_list) < min_sock:
                break
            try:
                if global_db.open == 0:
                    db_connect()                    
                for csock in psock_list:
                    ne_id,cmd_id,cmd_status,len_of_payload,param_count,tx_id = 0,0,1,0,0,0    # only initilization
        
                    cip,cport = csock.getpeername()
                    if event.is_set():
                        break                    
                    data,addrs=csock.recvfrom(2048)
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
                        
                        # decoded Payload        
                        decoded_payload = decode_payload(get_payload(hex_data_list),param_count)
                        
                        if cmd_id == 2011:          ## health check cmd_id
                            if cmd_status == 0: 
                                logging.info(" $$$ >> Health Check OK of device "+str(cip)+":"+str(cport))
                                try:
                                    query = "select health_check from tcp_health_check where ip_address='%s' "%cip
                                    cursor = global_db.cursor()
                                    cursor.execute(query)
                                    health_check = 1
                                    health_check = cursor.fetchone()[0]
                                    health_check += 1
                                    query = "update tcp_health_check set health_check=%s where ip_address = '%s' "%(health_check,cip)
                                    cursor.execute(query)
                                    global_db.commit()
                                    cursor.close()
                                    print health_check,'health'
                                except MySQLdb.Error as e:
                                    logging.error("/*/*/* MYSQLdb Exception in spawned process (health check ) : "+str(e))
                                except Exception as e:
                                    logging.error("/*/*/* Database Exception in spawned process : "+str(e)) 
                                
                            else:
                                logging.error( " #@! #@! #@! *** IN SPAWNED PROCESS > cmd_status is *1* at 2011 (HEALTH CHECK) UNEXPECTED  **** "+str(cip)+":"+str(cport))
                                break
                            #temp_txid = tx_id
                    else:
                        pass
                    

            
            except socket.timeout:
                logging.error("%%%%%%%  Socket timeOUT Exception in spawned process : "+cip+':'+str(cport))
                psock_list.remove(csock)
                csock.shutdown(socket.SHUT_RDWR)
                csock.close()
                if global_db.open == 1:
                    db_device_disconnet(cip)
                else:
                    db_connect()
            except Exception as e:
                logging.error("% % % % %  Exception in spwaned process INNER : "+str(e)+' >'+cip+':'+str(cport))
                psock_list.remove(csock)
                csock.close()
                if global_db.open == 1:
                    db_device_disconnet(cip)
                else:
                    db_connect()
            
    except Exception as e:
        logging.error("% % % % %  Exception in spawned process  : "+str(e)+' >'+cip+':'+str(cport))
        
    finally:
        logging.warning(" @@@@@ SPAWNED PROCESS EXITS having no. of socket objects :"+str(len(psock_list)))
        
############################################################################################################

class EventThread(threading.Thread):
    '''
    Event thread keep track of events, exceptions, errors generated in Discovery server and insert these events in database 
    '''
    def __init__(self):
        """
        init parameter for Event thread
        """
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        
    def join(self,timeout=None):
        """
        Stop the Thread
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        
    def run(self):
    
        err1 = 'device is NOT set, IP : >%s>'
        err2 = 'Monitoring thread is shutdown, Reason : >%s>'
        err3 = 'SubProcess is shutdown, Reason : >%s>'
        err4 = 'Not able to connect to DataBase'
        err5 = 'NMS DataBase is not responding'
        while not self._stopevent.isSet():                      # if stop_event is set by main process then this PsThread exits from the loop
            time.sleep(30)
            global status_dict,rule_variable,device_toWatch
            for eip in status_dict.keys():
                if status_dict[eip] > 6:
                    rule_variable = rule_variable + 1
                    device_toWatch.append(eip)
                    logging.critical(" !!!!!!!! Device is not set in last 5 rounds Please CHECK it ",+str(eip))
                                                           
                else:
                    pass
                if rule_variable > 200:
                    logging.critical(" !@!@!@!@!@!@!@!@ CRITICAL CRITICAL > More than 200 devices is not set in their last 5 rounds (rulevariable) even sigle device is not set then please check CONFIGURATION FILE config.rg")

            #####
            ## still have to complete it in future version as pasrt of event server
            #####
############################################################################################   



class nmsThread(threading.Thread):
    """ this class is used to handle nagios plugin request & sends information of Server health, no of spawned processes, no threas up, set devices, total no of devices"""
    
    def __init__(self, clisock, cip, cport):
        """ 
        init parameters for nmsThread class is client socket object,client ip,client port,
        """ 
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self.clisock=clisock          # client socket
        self.clip=cip                 # client ip
        self.clport=cport             # client port
        
    
    def join(self,timeout=None):
        """
        Stop the thread
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        
    def recieve_send(self):
        """ 
        used for receive and sending data to the device 
        """
        global sock_list,rule_variable,db_status
        ne_id,cmd_id,cmd_status,len_of_payload,param_count,tx_id = 0,0,1,0,0,0      # only initilization
        count = 0                                                                   # defining param_count
        try:    
            while not self._stopevent.isSet():            
                                        
                data,addrs=self.clisock.recvfrom(512)
                                
                if data:
                    # Hex_dump of Data Received in list
                    hex_data_list = dumphex(data)
                    #                    
                    # decoded Header
                    decoded_header = decode_header(get_header(hex_data_list))
                    #
                    # each field of decoded Header
                    ne_id = decoded_header['ne_id']
                    cmd_id = decoded_header['cmd_id']
                    cmd_status = decoded_header['cmd_status']
                    len_of_payload = decoded_header['len_of_payload']
                    param_count = decoded_header['param_count']
                    tx_id = decoded_header['tx_id']
                    #
                    # decoded Payload        
                    #
                                
                    ## REGISTRATION_RESPONCE
                    if cmd_id == 2001:    # confirming that this is REG_REQ
                        if cmd_status == 0:
                            # defining HEADER Variables
                            # preciding with r denotes that this is reply
                            rne_id = ne_id
                            rcmd_id = 2002    #or we can say cmd_id+1
                            rcmd_status = 0
                            rlen_of_payload = 0
                            rparam_count = 0
                            rtx_id = tx_id
                            #
                            encoded_header = make_header(rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id)
                            
                            reg_resp = asciirepr(encoded_header)    # Header in sendable format
                            
                            self.clisock.send(reg_resp)
                            print " nms ",reg_resp
                            
                        else:
                            #logwarning
                            break
                    ##

                    ## CONFIG RESPONCE                        
                    if cmd_id == 2003:    # confirming that this is CONFIG_REQ
                        if cmd_status == 0:
                            # defining PAYLOAD
                            # defining each_param_group then combining as a payload
                            # first param  = 3000 = Number of active processes
                            # second param = 3010 = Number of active threads
                            # third param  = 3020
                            # four param   = 3030
                            
                            param_list = ['3000','3010','3020']    # the order in which parameters have to be bound
                            resp_list = []
                            resp_list.append(threading.activeCount())
                            resp_list.append(len(multiprocessing.active_children()))
                            if db_status == 1 or db_status == 2:
                                resp_list.append(0)
                            elif db_status == 0:
                                resp_list.append(1)
                            else:
                                resp_list.append(0)
                                
                            
                            payload = ''
                            count = 0
                            for i in param_list:                    
                                rparam_name = i
                                #rparam_value = get_xmlattribute(rparam_name)
                                rparam_value = str(resp_list.pop())
                                rparam_size = len(rparam_value)
                                payload = payload+make_param(rparam_name,rparam_size,rparam_value)
                                count = count+1
                            #
                            print ' payload ',payload                                    
                            # defining HEADER Variables
                            # preceding with r denotes that this is reply
                            rne_id = ne_id
                            rcmd_id = 2004    #or we can say cmd_id+1
                            rcmd_status = 0
                            rlen_of_payload = len(payload)/2
                            rparam_count = count
                            rtx_id = tx_id
                            encoded_header = make_header(rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id)
                            #
                            
                            config_resp = asciirepr(encoded_header+payload)               
                            self.clisock.send(config_resp)
                            #
                        else:
                            #logwarning
                            break
                        
                    
                    ##
                
                    # FINAL RESPONCE
                    if cmd_id == 2005:                    
                        if cmd_status == 0:         # confirming that this is REG_REQ
                            
                            # defining HEADER Variables
                            # preceding with r denotes that this is reply
                            rne_id = ne_id
                            rcmd_id = 2006          #or can have cmd_id+1
                            rcmd_status = 0
                            rlen_of_payload = 0
                            rparam_count = 0
                            rtx_id = tx_id
                            #
                            encoded_header = make_header(rne_id,rcmd_id,rcmd_status,rlen_of_payload,rparam_count,rtx_id)
                            
                            reg_resp = asciirepr(encoded_header)    # Header in send_able format
                            
                            self.clisock.send(reg_resp)                  
                            break                       
                                                 
                            
                        else:
                            break


                else:         
                    pass
            
        except socket.timeout:
            #print " !!!!    in nmsThread socket timeout for device >"+self.clip+' : ',self.clport,' now closing socket connection'
            self.clisock.close()            
            
        except Exception as e:
            #print ' !!!!  Exception in nmsThread ',str(e)
            self.clisock.close()            
                   

        finally:
            #print " in nmsThread finally "                     
            pass
            

    def run(self):
        #print '\n*** nmsThread start for device > '+self.clip+' : ',self.clport
        self.recieve_send()
        #print ' ****nmsthread Exiting ******' 


##*********************************************
##
##     main program start here    
##
##*********************************************
def main():
    """
    This module is used to add new Devices in the network management system and configure them for snmp and ftp information 
    And asigning the device a unique network_ID for its life time.
    It also insert the received information from device in database.
    It creats a TCP server that listing for devices on port 6790 and accept their socket connection and start a new thread for that device communication.
    @Rahul Gautam ('Codescape Consultants Pvt. Ltd.') 
    """
    global thread_list,sock_list,server_ip_addr,rule_variable,process_dict,thread_dict,status_dict,thread_count,process_event,db_status
    db_connect()
    active_process = 49
    try:
        srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)       #creating server socket
        srvsock.bind( ("", 6790) )                             # binding to particular port
        #threading.stack_size(512*1024)
        sock_list.append(nms_ip)                                           # appending nms_ip in sock_list
        psThread_list = []
        #event = Event()
        psthread = PsThread()#event)                                       # this is a Monitoring thread that spawn a  process
        psthread.start()
        psThread_list.append(psthread)                
        
        logging.info('#######     hi! The VNL Unicast Discovery Server is running ......... on '+str(server_ip_addr)+':6790     ########       ... R. G. **')
        

        while 1:                                                          # always listening for devices (passive socket part)
            srvsock.listen(1)    
            clisock, (cip,cport) = srvsock.accept()                       # accepting client socket open an active socket for it

            if cip == nms_ip:
                #print '\n receive connection from Nagios ',cip
                clisock.settimeout(40)                                     # setting client socket timeout
                nmsthread = nmsThread(clisock,cip,cport)    
                nmsthread.start()                                          # new thread is start for that active socket
                print " nms thread start "
            
            elif threading.activeCount() < thread_count:
                if db_status == 1:
                    if db_reconnect() != 0:
                        db_status = 2
                    else:
                        db_status = 0
                if db_status == 2:
                    logging.error(" % % % Server is about to aclose beacuse UNABLE to connect to DataBase ") 
                    sys.exit(1)
                    
                clisock.settimeout(160)                                   # setting client socket timeout
                dthread = DsThread(clisock,cip,cport)   
                dthread.start()                                           # new thread is start for that active socket
                thread_list.append(dthread)
                thread_dict[dthread] = clisock
                sock_dict[clisock] = 1 
                if not status_dict.has_key(cip):
                    status_dict[cip] = 1
                print
                logging.info(" $$$ $$$ device accepted by server "+str(cip)+":"+str(cport)) 
                
            else:
                #clisock.shutdown(socket.SHUT_RDWR)
                #print 'closing socket for ',clisock.getpeername()
                clisock.close()

            if len(multiprocessing.active_children()) >= active_process:
                devices = process_dict.values()[0]
                for proces in process_dict.keys():
                    if devices >= process_dict[proces]:
                        devices = process_dict[proces]
                        to_beKilled = proces
                event = process_event[to_beKilled]
                event.set()
                logging.warning(" @@@ @@@ A spawned process is closing because active children is reached to max limit process is having "+str(devices)+" no of devices")
                process_dict.pop(to_beKilled)
                process_event.pop(to_beKilled)
                devices = 0
                if len(multiprocessing.active_children()) < 1:
                    break
                else:
                    pass
            else:
                pass
            if len(psThread_list) > 0:
                for pthread in psThread_list:
                    if pthread.isAlive() == False:
                        psthread = PsThread()#event)                                       # this is a Monitoring thread that spawn a  process
                        psthread.start()
                        psThread_list.append(psthread)
                        psThread_list.remove(pthread)
    
    except State_exception as s_e:
        print " State Exception Raised ",str(s_e)             
    except socket.error as (sock_errno, sock_errstr):
        logging.error(' /% /% /% Exception in socket ( in MAIN PROCESS ) : '+str(sock_errno)+' : '+str(sock_errstr))
        
    except KeyboardInterrupt as key:
        logging.error(" /% /% /%  Exception key board intruppt  IN MAIN PROCESS "+str(key))
        
    except Exception as e:
        logging.error(" !!!! Exception in main "+str(e))
        
    finally:
        
        logging.warning(' @@@@@ >>> Server is about to close Please Wait.........................*********')
        try:
            psthread.join()
        except Exception as e:
            pass
        finally :
            try:
                logging.info(' **** process_events '+str(len(process_event)))
                for proces in process_event.keys():
                    logging.info(' **** in for process events ')
                    event = process_event[proces]
                    event.set()
                    logging.debug(" ps event set "+str(proces))
                for dthread in thread_list:
                    if dthread.isAlive() == False:
                        thread_list.remove(dthread)
                    else:
                        dthread.join()
                        thread_list.remove(dthread)
               
            except  Exception as e:
                pass
            finally:
                time.sleep(20)
                db_close()
                srvsock.close()
                logging.critical(' !!!!! >>>>>>>>   Server is going to close  **if exception is not shown RECHECK EVERYTHING** <<<<<<<<<< ')
                sys.exit(0)




####  calling main() and Daemonizing my Discovery Server


class MyDaemon(Daemon):
    """
    this Class is calling main() and Daemonizing my Discovery Server
    it extends Daemon class and provides start stop functioality for daemon
    """
    def run(self):
        print " Discovery Server daemon starting ...... check its status with status option \n"
        if server_ip_addr:
            if(os.path.isfile(config_location)):
                signal(SIGTERM, lambda signum, stack_frame: exit(1))
                #time.sleep(5)
                main()
            else:
                logging.critical(' !!!! Please check the Config file location !!!! current location is '+str(config_location)+'\n ****server is exiting****')
        else:
            logging.critical('!!!!! unable to Get Server IP Address !!!!')

########################
if __name__ == "__main__":
	daemon = MyDaemon('/omd/daemon/tmp/unmp-ds.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'status' == sys.argv[1]:
			daemon.status()
		else:
			print " Unknown command"
			print " Usage: unmp-ds status | start | stop | restart | help | log \n     Please use help option if you are using it first time" 
			sys.exit(2)
		sys.exit(0)
	else:
		print " Usage: unmp-ds status | start | stop | restart | help | log  \n     Please use help option if you are using it first time"
		sys.exit(2)
#****************** PROGRAM END ***********************


##########################################################################
#BASE_PARAMID_OAM_OMC = 2050


#Param Name                            Param Value

#ACTIVE_CARD_HW_ID                 BASE_PARAMID_OAM_OMC +1
#PRODUCT_ID                        BASE_PARAMID_OAM_OMC +2
#NE_COUNTRY                        BASE_PARAMID_OAM_OMC +3
#NE_STATE                          BASE_PARAMID_OAM_OMC +4
#NE_CITY                           BASE_PARAMID_OAM_OMC +5
#NE_SITE_BLDG                      BASE_PARAMID_OAM_OMC +6
#CONTACT_PERSON                    BASE_PARAMID_OAM_OMC +7
#CONTACT_MOBILE                    BASE_PARAMID_OAM_OMC +8
#ALTERNATE_CONTACT_NO              BASE_PARAMID_OAM_OMC +9
#CONTACT_EMAIL                     BASE_PARAMID_OAM_OMC +10
#CONTACT_ADDRESS                   BASE_PARAMID_OAM_OMC +11
#NE_SITE_FLOOR                     BASE_PARAMID_OAM_OMC +12
#NE_SITE_DIRECTION                 BASE_PARAMID_OAM_OMC +13
#NE_SITE_LANDMARK                  BASE_PARAMID_OAM_OMC +14
#NE_SITE_NICKNAME                  BASE_PARAMID_OAM_OMC +15
#NE_SITE_LONGITUDE                 BASE_PARAMID_OAM_OMC +16
#NE_SITE_LATITUDE                  BASE_PARAMID_OAM_OMC +17
#SNMP_REQUEST_PORT                 BASE_PARAMID_OAM_OMC +18
#SNMP_TRAP_PORT                    BASE_PARAMID_OAM_OMC +19
#SNMP_READ_COMMUNITY_PREFIX        BASE_PARAMID_OAM_OMC +20
#SNMP_WRITE_COMMUNITY_PREFIX       BASE_PARAMID_OAM_OMC +21
#FTP_USER_NAME                     BASE_PARAMID_OAM_OMC +22
#FTP_USER_PASSWORD                 BASE_PARAMID_OAM_OMC +23
#OMC_HOME                          BASE_PARAMID_OAM_OMC +25
#FTP_SERVER_IP                     BASE_PARAMID_OAM_OMC +27
