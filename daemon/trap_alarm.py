#!/usr/bin/python2.6	

############################################################################################
#  AUTHOR : RAJENDRA SHARMA, RAHUL GAUATM
#  LAST DATE OF RELEASE : 	9 April 2012
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

global file_name, trap_executed, mask_file, maskfile_stat, mask_alarm_dict, mask_severity_dict

trap_executed = 0
mask_severity_dict = {}

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
        cursor = db.cursor()					#-- CURSOR CREATION ------#
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
	    cursor.execute("INSERT INTO id_info (index_id,deamon_name,time_stamp) values('%s','%s','%s')"%(0,'D1',datetime.now()) )  ## --- create first time entry forsnmptt.id_info  table ----####
	    db.commit()

    except MySQLdb as e:
        pass
		#print str(e)
		#logging.info(e)
    except SelfException:
        pass
    except Exception,e:
        logging.error(" Exception in trap daemon "+str(e))
        pass
		#logging.info(e)
		#print str(e)
    finally:
        if isinstance(db,MySQLdb.connection):
            if db.open:
                cursor.close()
                db.close()

#$#############################  CONNECTION FROM NEW DATABASE  ######################################
    try:
        if len(snmptt_trap_data) > 0:
            trap_executed = 1
            db=MySQLdb.connect(hostname,username,password,schema)  ## --- CREATE DATABASE CONNECTION  ---- ##
            cursor = db.cursor()					               # -- CREATE CURSOR-------# 
            for_str=[]
            for row in snmptt_trap_data:
                update_index_id=row[0]
                main_str=row[6]
                sub_str=re.split('[:]',row[6])
                if len(sub_str)>10:
                    replace_str=sub_str[0]+':'
                    main_str=main_str.replace(replace_str,'')
                    main_str=main_str.replace('\\','').replace('"','')
                for_str=main_str.split('|')
                # INSERT THE ENTRY IN TRAP_ALARMS TABLE IN THIS SQL QUERY #
                sql="INSERT INTO trap_alarms (event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description,timestamp) values('%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s',now())"% ( row[1],row[2],row[3],row[4],row[5],for_str[0],for_str[1],for_str[2],for_str[3],for_str[4],for_str[5],for_str[6],for_str[7])
                cursor.execute(sql)
                db.commit()
                
            cursor.execute("UPDATE id_info set index_id=%s,time_stamp='%s' WHERE deamon_name = 'D1'"% (update_index_id,datetime.now()))  ## ----  update index id  value in
            db.commit()
    except MySQLdb.Error as e:
        pass
		#logging.info(e)
		#print "MySQLdb Exception"+str(e)
    except SelfException:
        pass
		#logging.info(e)
    except Exception,e:
        logging.error(" Exception in trap daemon 2:  "+str(e))
        pass
		#logging.info(e)
		#print str(e)
    finally:
        if isinstance(db,MySQLdb.connection):
            if db.open:
                cursor.close()
                db.close()
		


###### CURRENT CLEAR ALARM DAEMON FUNCTION
def current_clear_daemon():
    global mask_file, maskfile_stat, mask_alarm_dict, mask_severity_dict
    db = 1
    try:
        new_maskfile_stat = os.stat(mask_file).st_mtime
        if maskfile_stat != new_maskfile_stat:
            execfile(mask_file,globals())
            maskfile_stat = new_maskfile_stat
            
        logging.info(" current clear alarm Executing ")

        db=MySQLdb.connect(hostname,username,password,schema)
        #db=MySQLdb.connect("172.22.0.95",username,password,"nms_p")  
        cursor = db.cursor()                                   
        cursor.execute("SELECT timestamp FROM daemon_timestamp WHERE daemon_name='D2'")  
        daemon_timestamp=cursor.fetchall()
        if len(daemon_timestamp) > 0:  
            sql="SELECT * FROM trap_alarms WHERE timestamp between '%s' and now()"%(daemon_timestamp[0][0])
            cursor.execute(sql)
            history_alarms=cursor.fetchall()
            cursor.execute("UPDATE daemon_timestamp SET timestamp=now() where daemon_name='D2'")
            db.commit()
            cursor.close()
        else:
            ins_query="INSERT INTO daemon_timestamp (daemon_name,timestamp) values('D2',now())"
            cursor.execute(ins_query)
            db.commit()
            cursor.close() 
            history_alarms=()

        cursor=db.cursor()
        trap_alarms_tp = ('alarm_id', 'event_id', 'trap_id', 'agent_id', 'trap_date', 'trap_received_date', 'severity', 'trap_event_id', 'trap_event_type', 'manage_obj_id', 'manage_obj_name', 'component_id', 'trap_ip', 'description', 'timestamp')
        for row_alarm in history_alarms:

            map_value = mask_alarm_dict.get(row_alarm[8])
            
    #        print map_value,row_alarm[8]            
            
            if map_value:
                sql="SELECT * FROM  trap_alarm_current WHERE trap_event_type='%s' and manage_obj_id='%s'and manage_obj_name='%s' and agent_id='%s' "% (row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[3])
                cursor.execute(sql)
                current_info=cursor.fetchall()
                if len(current_info) > 0:
                    if real_alarm_list.count(row_alarm[8]): # if real alarm 
                        if (row_alarm[6] < 2) and  (time.mktime(row_alarm[14].timetuple())  > time.mktime(current_info[0][14].timetuple())) and ((row_alarm[7]) != (current_info[0][7])) and ((current_info[0][8]) == (row_alarm[8])):   # future changeable  
                            cursor.execute("INSERT INTO trap_alarm_clear (event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity, trap_event_id, trap_event_type, manage_obj_id, manage_obj_name, component_id, trap_ip, description) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(row_alarm[1],row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],mask_severity_dict.get(map_value,row_alarm[6]),row_alarm[7],map_value,row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13]))
                            db.commit()
                            sql="DELETE FROM trap_alarm_current WHERE trap_alarm_current_id='%s'"% current_info[0][0]
                            cursor.execute(sql)     
                            db.commit()
                        else:
                            if (row_alarm[6] == current_info[0][6])  and  (time.mktime(time.strptime(row_alarm[5])))  > (time.mktime(time.strptime(current_info[0][5]))) and  ((row_alarm[7]) == (current_info[0][7])) and ((current_info[0][8]) == (row_alarm[8])):
                                #sql="INSERT INTO trap_alarm_clear (event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(row_alarm[1],row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],row_alarm[6],row_alarm[7],map_value,row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13])
                                #cursor.execute(sql)
                                #db.commit()
                                sql="UPDATE trap_alarm_current set trap_id = '%s', agent_id = '%s', trap_date = '%s', trap_receive_date = '%s', serevity = '%s', trap_event_id = '%s', trap_event_type = '%s', manage_obj_id = '%s', manage_obj_name = '%s', component_id = '%s', trap_ip = '%s', description = '%s' WHERE event_id = '%s' "%(row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],mask_severity_dict.get(row_alarm[8],row_alarm[6]),row_alarm[7],row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13],current_info[0][0])
                                cursor.execute(sql)
                                db.commit()
                    else:
                        sql="UPDATE trap_alarm_current set trap_id = '%s',agent_id = '%s',trap_date = '%s',trap_receive_date = '%s',serevity = '%s',trap_event_id = '%s',trap_event_type = '%s',manage_obj_id = '%s',manage_obj_name = '%s',component_id = '%s',trap_ip = '%s',description = '%s' WHERE event_id = '%s' "%(row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],mask_severity_dict.get(row_alarm[8],row_alarm[6]),row_alarm[7],row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13],current_info[0][0])
                        cursor.execute(sql)
                        db.commit()
                else:
                    sql="INSERT INTO trap_alarm_current (event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description) values ('%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s')"%(row_alarm[1],row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],mask_severity_dict.get(row_alarm[8],row_alarm[6]),row_alarm[7],row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13])
                    cursor.execute(sql)
                    db.commit()
            else:
                key_li = [key for key, value in mask_alarm_dict.iteritems() if value == str(row_alarm[8])]
                if len(key_li) > 0:
                    sql="SELECT * FROM  trap_alarm_current WHERE trap_event_type='%s' and manage_obj_id='%s'and manage_obj_name='%s' and agent_id='%s'"% (key_li[0],row_alarm[9],row_alarm[10],row_alarm[3])
                    cursor.execute(sql)
                    current_info=cursor.fetchall()
                    if len(current_info) > 0:
                        cursor.execute("INSERT INTO trap_alarm_clear (event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(row_alarm[1],row_alarm[2],row_alarm[3],row_alarm[4],row_alarm[5],mask_severity_dict.get(row_alarm[8],row_alarm[6]),row_alarm[7],row_alarm[8],row_alarm[9],row_alarm[10],row_alarm[11],row_alarm[12],row_alarm[13]))
                        db.commit()
                        sql="DELETE FROM trap_alarm_current WHERE trap_alarm_current_id='%s'"% current_info[0][0]
                        cursor.execute(sql)    
                        db.commit()
 
    except MySQLdb.Error as e:
        print str(e)
    except SelfException as e:
        print str(e)
    except Exception,e:
        logging.error(" EXCEPTION in current clear "+str(e))
        print str(e)
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
            while 1:
                trap_daemon()
                if trap_executed:
                    current_clear_daemon()
                time.sleep(10)	

	except Exception as e:
		print " Exception in trap_alarm daemon : ",str(e[-1])



def write_time(action):		# if start then action = 0 / if stop then action = 1
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
    daemon = MyDaemon('/omd/daemon/tmp/unmp-trap.pid')
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
