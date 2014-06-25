#!/usr/bin/python2.6

############################################################################################
#  AUTHOR : RAJENDRA SHARMA, RAHUL GAUATM
#  LAST DATE OF RELEASE :     9 April 2012
#
#  REQUIRED : MYSQLdb,PYTHON,SNMPTT DATABASE, SNMPTT FILE
#  WORKING OF THIS DEAMON : THIS SELECT THE TRAP FROM SNMPTT DATABASE AND STORE IN TRAP_ALARMS TABLE ACCORDING TO REQUIRED FORMET.
#                           ALSO MASK TRAP AS ALARM ACCORDING USER DEFINATION
#
#############################################################################################

# import module
import os.path
import sys
from daemon import Daemon
import MySQLdb
import time
from datetime import datetime
import logging
logging.basicConfig(filename='/omd/daemon/log/trap_log.log',format='%(levelname)s: %(asctime)s >> %(message)s', level=logging.DEBUG)
import re
import traceback

global file_name, trap_executed, mask_file, maskfile_stat, mask_alarm_dict, temp_severity_dict, clear_alarm_dict, real_alarm_list

trap_executed = 0
mask_alarm_dict={}
temp_severity_dict={}
clear_alarm_dict={}
real_alarm_list=[]


global odu16_mask_alarm_dict, odu16_mask_severity_dict, odu16_clear_alarm_dict, odu16_real_alarm_list

odu16_mask_alarm_dict, odu16_mask_severity_dict, odu16_clear_alarm_dict, odu16_real_alarm_list = {}, {}, {}, []

file_name = "/omd/daemon/tmp/trap.time"

mask_file = "/omd/daemon/alarm_mask.rg"     # alarm mask file

mysql_file = '/omd/daemon/config.rg'

if os.path.isfile(mysql_file) and os.path.isfile(mask_file):    # getting variables from config file
    maskfile_stat = 0
    execfile(mysql_file)
else:
    sys.exit()

#Exception class for own created exception.
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
    def __init__(self,msg):
        pass
        #logging.info(msg)
        #print msg

def trap_daemon():
    global trap_executed
    trap_executed = 0
    update_index_id=0
    snmptt_trap_data=()
    try:
        db=MySQLdb.connect(hostname,username,password,"snmptt") ## --- DATABASE CONECTION CREATION  ---- ##
        cursor = db.cursor()                    #-- CURSOR CREATION ------#
        cursor.execute("SELECT index_id FROM id_info WHERE deamon_name = 'D1'")   ## ---- SELECT INDEX_ID FROM  SNMPTT.ID_INFO FOR IDENTIFIED LAST EXECUTION---#
        INDEX=cursor.fetchall()
        if len(INDEX) > 0: # -------THIS CHECK INDEX_ID EXIST OR NOT IN SNMPTT.ID_INFO  --------#
            #-- THIS SELECT NO OF  TRAP  ACCORDING TO CONDTION ------#
            sql = "SELECT id,eventname,eventid,agentip,uptime,traptime,formatline FROM snmptt WHERE id > %s" %INDEX[0]
            cursor.execute(sql)
            snmptt_trap_data=cursor.fetchall()
            # CALCULATE THE LENGTH THAT HOW MUCH ROW SELECTED #
            data_len = len(snmptt_trap_data)
            if data_len > 0:
                new_index_id= snmptt_trap_data[len(snmptt_trap_data)-1][0]
                cursor.execute("UPDATE id_info set index_id=%s,time_stamp='%s' WHERE deamon_name = 'D1'"% (new_index_id,datetime.now()))  ## ----  update index id  value in snmptt.id_info table ------##
                db.commit()  #---   SAVE THE ENTRY IN DATABASE -----#
        else:
            cursor.execute("INSERT INTO id_info (index_id, deamon_name, time_stamp) values('%s','%s','%s')"%(0,'D1',datetime.now()) )  ## --- create first time entry forsnmptt.id_info  table ----####
            db.commit()

    except MySQLdb as e:
        pass
        #print str(e)
        logging.info(str(e))
    except SelfException:
        pass
    except Exception,e:
        logging.error(" Exception in trap daemon "+str(traceback.format_exc()))
        pass
        #logging.info(e)
        #print str(e)
    finally:
        if isinstance(db,MySQLdb.connection):
            if db.open:
                cursor.close()
                db.close()

#$#############################  CONNECTION FROM NEW DATABASE  ######################################
    device_date_format = '%a %b %d %H:%M:%S %Y'
    try:
        import trap_template
        from trap_template import *
        device_date_format = '%a %b %d %H:%M:%S %Y'
        if len(snmptt_trap_data) > 0:
            db=MySQLdb.connect(hostname,username,password,schema)   # --- CREATE DATABASE CONNECTION  ---- #
            cursor = db.cursor()                                    # -- CREATE CURSOR-------#
            for_str=[]
            for row in snmptt_trap_data:
                if row[1] in ["storageTrap", "otafTrap"]:
                    for_str = insert_values(row[1], row[6])
                    for_str = for_str.split("|")
                    sql="INSERT INTO trap_alarms (event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity, trap_event_id, \
                    trap_event_type, manage_obj_id, manage_obj_name, component_id, trap_ip, description, device_sent_date, timestamp) \
                    values('%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', now())\
                    "% (row[1],row[2],row[3],row[4],row[5],int(for_str[0]),for_str[1],for_str[2],for_str[3],for_str[4],for_str[5], \
                        for_str[6],for_str[7],str(datetime.now()))
                    cursor.execute(sql)
                    db.commit()
    except Exception as e:
        logging.error(" Exception in trap daemon 2 inner loop:  "+traceback.format_exc())
    try:
        if len(snmptt_trap_data) > 0:
            trap_executed = 1
            db=MySQLdb.connect(hostname,username,password,schema)  ## --- CREATE DATABASE CONNECTION  ---- ##
            cursor = db.cursor()                                   # -- CREATE CURSOR-------#
            for_str=[]
            for row in snmptt_trap_data:
                try:
                    update_index_id=row[0]
                    device_date = 'null'
                    if row[1] == 'ccuTrap':
                        for_str = row[6].split('|')
                        try:
                            if len(for_str[8]) > 20:
                                temp_str = for_str[8][:for_str[8].find(':')+6]
                            else:
                                temp_str = for_str[8]
                            device_date = datetime.strptime(temp_str,device_date_format)
                        except:
                            pass
                    else:
                        main_str=row[6]
                        sub_str=re.split('[:]',row[6])
                        if len(sub_str)>10:
                            replace_str=sub_str[0]+':'
                            main_str=main_str.replace(replace_str,'')
                            main_str=main_str.replace('\\','').replace('"','')
                        for_str=[i.strip() for i in main_str.split('|')]

                        try:
                            device_date = datetime.strptime(for_str[8],device_date_format)
                        except:
                            pass
                    # INSERT THE ENTRY IN TRAP_ALARMS TABLE IN THIS SQL QUERY #
                    sql="INSERT INTO trap_alarms (event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity, trap_event_id, \
                    trap_event_type, manage_obj_id, manage_obj_name, component_id, trap_ip, description, device_sent_date, timestamp) \
                    values('%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', now())\
                    "% (row[1],row[2],row[3],row[4],row[5],int(for_str[0]),for_str[1],for_str[2],for_str[3],for_str[4],for_str[5], \
                        for_str[6],for_str[7],device_date)
                    cursor.execute(sql)
                    db.commit()
                except Exception,e:
                    logging.error(" Exception in trap daemon 2 inner loop:  "+traceback.format_exc())
            #cursor.execute("UPDATE id_info set index_id=%s,time_stamp='%s' WHERE deamon_name = 'D1'"% (update_index_id,datetime.now()))  ## ----  update index id  value in
            #db.commit()
    except MySQLdb.Error as e:
        pass
        logging.info(str(e))
        #print "MySQLdb Exception"+str(e)
    except SelfException:
        pass
        #logging.info(e)
    except Exception,e:
        logging.error(" Exception in trap daemon 2:  "+traceback.format_exc())
        pass
        #print str(e)
    finally:
        if isinstance(db,MySQLdb.connection):
            if db.open:
                cursor.close()
                db.close()



###### CURRENT CLEAR ALARM DAEMON FUNCTION
def current_clear_daemon():
    global mask_file, maskfile_stat, mask_alarm_dict, mask_severity_dict, clear_alarm_dict, \
           real_alarm_list, odu16_mask_alarm_dict, odu16_mask_severity_dict, odu16_clear_alarm_dict, odu16_real_alarm_list
    db = 1
    try:
        new_maskfile_stat = os.stat(mask_file).st_mtime
        if maskfile_stat != new_maskfile_stat:
            execfile(mask_file,globals())
            maskfile_stat = new_maskfile_stat
            logging.info(" current clear : New Mask file uploaded ")

        db=MySQLdb.connect(hostname,username,password,schema)
        #db=MySQLdb.connect("172.22.0.95",username,password,"nms_p")
        cursor = db.cursor()
        cursor.execute("SELECT timestamp FROM daemon_timestamp WHERE daemon_name='D2'")
        daemon_timestamp=cursor.fetchall()
        if len(daemon_timestamp) > 0:
            sql="SELECT * FROM trap_alarms WHERE timestamp between '%s' and now() order by event_id"%(daemon_timestamp[0][0])
            cursor.execute(sql)
            history_alarms=cursor.fetchall()
            cursor.execute("UPDATE daemon_timestamp SET timestamp=now() where daemon_name='D2'")
            db.commit()
            cursor.close()
            if len(history_alarms) < 1:
                return
        else:
            ins_query="INSERT INTO daemon_timestamp (daemon_name,timestamp) values('D2',now())"
            cursor.execute(ins_query)
            db.commit()
            cursor.close()
            history_alarms=()
            return

        cursor=db.cursor()
        #trap_alarms = {0: 'alarm_id', 1: 'event_id', 2: 'trap_id', 3: 'agent_id', 4: 'trap_date', 5: 'trap_received_date',\
                        # 6: 'severity', 7: 'trap_event_id', 8: 'trap_event_type', 9: 'manage_obj_id', 10: 'manage_obj_name',\
                        # 11: 'component_id', 12: 'trap_ip', 13: 'description', 14: 'device_sent_date', 15: 'timestamp'}
        prev_event = ''
        #logging.info(" mask_alarm_dict : "+str(mask_alarm_dict))
        #logging.info(" real_alarm_list : "+str(real_alarm_list))
        #logging.info("clear_alarm_dict  : "+str(clear_alarm_dict))
        #logging.info(" mask_severity_dict : "+str(mask_severity_dict))

        for row_alarm in history_alarms:
            try:
                if prev_event != row_alarm[1]:
                    #logging.info("  prev_event "+str(prev_event))
                    prev_event = row_alarm[1]
                    if row_alarm[1] == 'ruTrap16':
                        #logging.info("  in odu16 trap ")
                        temp_alarm_dict = odu16_mask_alarm_dict
                        temp_alarm_list = odu16_real_alarm_list
                        temp_severity_dict = odu16_mask_severity_dict
                        temp_clear_dict = odu16_clear_alarm_dict
                    else:
                        #logging.info("  in RU100 trap ")
                        temp_alarm_dict = mask_alarm_dict
                        temp_alarm_list = real_alarm_list
                        temp_severity_dict = mask_severity_dict
                        temp_clear_dict = clear_alarm_dict

                map_value = temp_alarm_dict.get(row_alarm[7])
                #print map_value,row_alarm[8]
                #logging.info("-----------------")
                #logging.info(" 1: "+str(row_alarm))

                # map_value means its a current alarm
                if map_value:
                    #logging.info(" 2: is a current alarm")
                    sql="SELECT * FROM  trap_alarm_current WHERE trap_event_type='%s' and manage_obj_id='%s' and manage_obj_name='%s' \
                    and agent_id='%s' and event_id='%s'"% (row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[3],row_alarm[1])
                    cursor.execute(sql)
                    current_info=cursor.fetchall()
                    # current alarm found
                    if len(current_info) > 0:
                        #logging.info(" 3: previous entry in current table found ")
                        #if real alarm
                        if temp_alarm_list.count(row_alarm[7]):
                            #logging.info("4: is a real alarm ")
                            # real alarm is below severity 2 then it will be treated as clear
                            if (row_alarm[6] < 2) and  (time.mktime(row_alarm[14].timetuple())  > time.mktime(current_info[0][14].timetuple())) \
                               and (row_alarm[7] != current_info[0][7]) and (current_info[0][8] == row_alarm[8]):   #future changeable
                                cursor.execute("INSERT INTO trap_alarm_clear (event_id, trap_id, agent_id, trap_date, trap_receive_date, \
                                serevity, trap_event_id, trap_event_type, manage_obj_id, manage_obj_name, component_id, trap_ip, description, \
                                device_sent_date, timestamp) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', now())\
                                "%(row_alarm[1],row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5], \
                                   temp_severity_dict.get(map_value,row_alarm[6]),row_alarm[7],temp_clear_dict.get(map_value,row_alarm[8]), \
                                   row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13],row_alarm[14]))
                                db.commit()
                                #logging.info('a')
                                sql="DELETE FROM trap_alarm_current WHERE trap_alarm_current_id='%s'"% current_info[0][0]
                                cursor.execute(sql)
                                db.commit()
                            else:
                                # if severity of real alarm is high then we will treat this as current alarm
                                if (row_alarm[6] == current_info[0][6])  \
                                   and  (time.mktime(time.strptime(row_alarm[5])))  > (time.mktime(time.strptime(current_info[0][5]))) \
                                   and  (row_alarm[7] == current_info[0][7]) and (current_info[0][8] == row_alarm[8]):
                                    #sql="INSERT INTO trap_alarm_clear\
                                          #event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity, trap_event_id, trap_event_type, \
                                          # manage_obj_id, manage_obj_name, component_id, trap_ip, description) \
                                          #values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')\
                                          #"%(row_alarm[1],row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],row_alarm[6],\
                                          #row_alarm[7],map_value,row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13])
                                    #cursor.execute(sql)
                                    #db.commit()
                                    # does timestamp needs to be updated
                                    sql="UPDATE trap_alarm_current set trap_id = '%s', agent_id = '%s', trap_date = '%s', trap_receive_date = '%s', \
                                    serevity = '%s', trap_event_id = '%s', trap_event_type = '%s', manage_obj_id = '%s', manage_obj_name = '%s', \
                                    component_id = '%s', trap_ip = '%s', description = '%s', device_sent_date = '%s' WHERE event_id = '%s' \
                                    "%(row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],temp_severity_dict.get(row_alarm[7],row_alarm[6]), \
                                       row_alarm[7],row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13], \
                                       current_info[0][0],row_alarm[14])
                                    cursor.execute(sql)
                                    db.commit()

                        # it not real alarm [ a normal trap masked by user]
                        else:
                            #logging.info(" 4: is NOT A real alarm ")
                            # Then we will update the existing current alarm's info [ current has come again ]
                            sql="UPDATE trap_alarm_current set trap_id = '%s',agent_id = '%s',trap_date = '%s',trap_receive_date = '%s',\
                            serevity = '%s',trap_event_id = '%s',trap_event_type = '%s',manage_obj_id = '%s',manage_obj_name = '%s',\
                            component_id = '%s',trap_ip = '%s',description = '%s', device_sent_date = '%s', timestamp = now() WHERE event_id = '%s' \
                            "%(row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],temp_severity_dict.get(row_alarm[7],row_alarm[6]), \
                               row_alarm[7],row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13], \
                               current_info[0][0],row_alarm[14])
                            cursor.execute(sql)
                            db.commit()

                    # alarm is current but not found in db so insert a fresh row
                    else:
                        #logging.info(" 3: New current entry should made for this current alarm ")
                        sql="INSERT INTO trap_alarm_current (event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,trap_event_id,\
                        trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description,device_sent_date, timestamp) \
                        values ('%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s', now())\
                        "%(row_alarm[1],row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],temp_severity_dict.get(row_alarm[7],row_alarm[6]), \
                           row_alarm[7],row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13],row_alarm[14])
                        cursor.execute(sql)
                        db.commit()

                # map_value not found so it should be clear alarm
                else:
                    #logging.info(" 2: Can be a clear alarm ")
                    key_li = [key for key, value in temp_alarm_dict.iteritems() if value == str(row_alarm[7])]

                    #logging.info(" 3: Can be a clear alarm : check key_li : ", str(key_li))
                    # with the help of key_li we will try to find that if this alarm is mapped with any current alarm
                    # if mapped then see if we have any current alarm in current table. only then we have to clear it.
                    if len(key_li) > 0:
                        sql="SELECT * FROM  trap_alarm_current WHERE trap_event_id='%s' and manage_obj_id='%s'and manage_obj_name='%s' \
                        and agent_id='%s' and event_id='%s'"% (key_li[0],row_alarm[9],row_alarm[10],row_alarm[3],row_alarm[1])
                        cursor.execute(sql)
                        current_info=cursor.fetchall()

                        # found a current in respect to this clear alarm so we have to clear it.
                        if len(current_info) > 0:
                            cursor.execute("INSERT INTO trap_alarm_clear (event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,\
                            trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description,device_sent_date, \
                            timestamp) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', now())\
                            "%(row_alarm[1],row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5], \
                               temp_severity_dict.get(row_alarm[7],row_alarm[6]),row_alarm[7],temp_clear_dict.get(row_alarm[7],row_alarm[8]), \
                               row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13],row_alarm[14]))
                            db.commit()
                            # delete all current alarm related to that id, becoz we have cleared it.
                            sql="DELETE FROM trap_alarm_current WHERE trap_alarm_current_id='%s'"% current_info[0][0]
                            cursor.execute(sql)
                            db.commit()
            except Exception,e:
                logging.error(" EXCEPTION in current clear inner loop : "+str(traceback.format_exc()))

    except MySQLdb.Error as e:
        pass
        logging.error(" MySQL EXCEPTION in current clear "+str(traceback.format_exc()))
        #print str(e)
    except SelfException as e:
        pass
        #print str(e)
    except Exception,e:
        logging.error(" EXCEPTION in current clear "+str(traceback.format_exc()))
    finally:
        if isinstance(db,MySQLdb.connection):
            if db.open:
                cursor.close()
                db.close()




#-- CLASS DAEMON EXECUTION -----#
class MyDaemon(Daemon):
    """
    this Class is calling main() and Daemonizing my Discovery Server
    it extends Daemon class and provides start stop functionality for daemon
    """
    def run(self):
        global trap_executed
        try:
            while True:
                trap_daemon()
                if trap_executed:
                    current_clear_daemon()
                time.sleep(5)

        except Exception as e:
            print " Exception in trap_alarm daemon : ",+str(traceback.format_exc())



def write_time(action):        # if start then action = 0 / if stop then action = 1
    global file_name
    try:
        f = open(file_name,'r')
        flag = 0
        file_lines = f.readlines()
        if len(file_lines) < 1:
            flag = 1
            f.close()
            f = open(file_name,'w')
    except IOError, err:
        f = open(file_name,'w')
        flag = 1
    if flag == 0:
        if action == 0:
            try:
                stop_time = file_lines[1]
            except IndexError,err:
                stop_time = datetime.strftime(datetime.today(),'%c')
            f.close()
            start_time = datetime.strftime(datetime.today(),'%c')
            line_write = start_time+"\n"+stop_time
            f = open(file_name,'w')
            #print "start ",line_write
            f.writelines(line_write)
            f.flush()
            f.close()
        elif action == 1:
            start_time = file_lines[0]
            f.close()
            stop_time = datetime.strftime(datetime.today(),'%c')
            if start_time.find("\n") == -1:
                line_write = start_time+"\n"+stop_time
            else:
                line_write = start_time+stop_time
            f = open(file_name,'w')
            #print "stop ",line_write
            f.writelines(line_write)
            f.flush()
            f.close()
    elif flag == 1:
        if action == 0:
            start_time = datetime.strftime(datetime.today(),'%c')
            line_write = start_time
            #print line_write
            f.writelines(line_write)
            f.flush()
            f.close()
        elif action == 1:
            start_time = datetime.strftime(datetime.today(),'%c')
            stop_time = datetime.strftime(datetime.today(),'%c')
            line_write = start_time+"\n"+stop_time
            #print line_write
            f.writelines(line_write)
            f.flush()
            f.close()

########################
if __name__ == "__main__":
    daemon = MyDaemon('/omd/daemon/tmp/unmp-trap.pid', 'unmp-alarm')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            write_time(0)
            daemon.start()
        elif 'stop' == sys.argv[1]:
            write_time(1)
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print " Unknown command"
            print " Usage: unmp-alarm status | start | stop | restart | help | log \n     Please use help option if you are using it first time"
            sys.exit(2)
        sys.exit(0)
    else:
        print " Usage: unmp-alarm status | start | stop | restart | help | log  \n     Please use help option if you are using it first time"
        sys.exit(2)
#****************** PROGRAM END ***********************
