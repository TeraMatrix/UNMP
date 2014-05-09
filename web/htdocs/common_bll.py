#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 03-Nov-2011
@version: 0.1
@note: All database and model's functions that are common. 
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
from unmp_model import *
from sqlalchemy.orm import sessionmaker
import subprocess, commands, MySQLdb, datetime
from unmp_config import SystemConfig
import time
import rrdtool
import psutil

class LocalSystemBll(object):
    def harddisk_details(self):
         harddisk = psutil.disk_usage('/')
         total = harddisk.total/(1024.0*1024.0*1024.0)
         free = harddisk.free/(1024.0*1024.0*1024.0)
         used = harddisk.used/(1024.0*1024.0*1024.0)
         unused = total-(free+used)
         return str('%.2f' %total) + "," + str('%.2f' %free) + "," + str('%.2f' %unused) + "," + str('%.2f' %used)
    
    def system_uptime(self):
         return datetime.datetime.fromtimestamp(psutil.BOOT_TIME).strftime('%d-%B-%Y %H:%M:%S')
    
    def ram_details(self):
         ram = psutil.phymem_usage()
         total = ram.total
         usePer = ram.percent;
         used = total*usePer/100
         free = total - used
         return "%.2f,%.2f" %(used/(1024.0*1024.0),free/(1024.0*1024.0))
         
    def convert_utc_to_ist(self,timestamp):
        offset_ist = 5.5
        return timestamp + ((offset_ist*60)*60000)
        
    def processor_details(self,total):
         total_sec = total*10 + 10
         cpu = rrdtool.fetch('/omd/daemon/rrd/cpu.rrd', 'AVERAGE', '-s','-%ssec' % total_sec)
	 data_series=[]
	 if len(cpu) == 3:
	      timestamp = cpu[0]
	      label = cpu[1]
	      data = cpu[2]
	      for i in range(len(label)):
	          data_series.append({"name":str(label[i]).replace("_"," "),"data":[]})
	          
	      for i in range(len(data)):
	          if total != 0:
	              for lbl_i in range(0,len(label)): 
	                  if data[i][lbl_i] != None:
	                      data_series[lbl_i]["data"].append({"x":self.convert_utc_to_ist((timestamp[0]+(timestamp[2]*(i)))*1000),"y":data[i][lbl_i]})
	                      if lbl_i == 0:
	                          total-=1
         return data_series
        
    def bandwidth_details(self,total):
         total_sec = total*10 + 10
         interface = rrdtool.fetch('/omd/daemon/rrd/interface.rrd', 'AVERAGE', '-s','-%ssec' % total_sec)
	 data_series=[]
	 if len(interface) == 3:
	      timestamp = interface[0]
	      label = interface[1]
	      data = interface[2]
	      for i in range(len(label)):
	          data_series.append({"name":str(label[i]).replace("_"," "),"data":[]})
	          
	      for i in range(len(data)):
	          if total!=0:
	              for lbl_i in range(0,len(label)): 
	                  if data[i][lbl_i] != None:
	                      data_series[lbl_i]["data"].append({"x":self.convert_utc_to_ist((timestamp[0]+(timestamp[2]*(i)))*1000),"y":data[i][lbl_i]/1024.0})
	                      if lbl_i == 0:
	                          total-=1
         return data_series
         
class EventLog(object):
    """
    @author: Rahul Gautam
    @since: 01-Dec-2011
    @version: 0.1
    @note: Logging Every Event and Action in Database   
    @organization: Codescape Consultants Pvt. Ltd.
    @copyright: 2011 Rahul Gautam for Codescape Consultants Pvt. Ltd.
    @see: http://www.codescape.in
        
    """
    global_db = None
    def db_connect(self):
        """
        Used to connect to the database :: return database object ed in global_db variable
        """
        db = None
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            self.global_db = db
        except MySQLdb.Error as e:
            print "/*/*/* MYSQLdb Exception (db connect) : "+str(e)
        except Exception as e:
            print "/*/*/* Database Exception (db connect) : "+str(e)
    
    
    def db_close(self):
        """
        closes connection with the database
        """
        try:
            self.global_db.close()
        except Exception as e:
            print "/*/*/* Database Exception ( db close ) : "+str(e)
            
    def log_event(self,description,user_name):
    	"""
    	@note: Used to log Event or Action in Database
    	"""
            
        try:
            self.db_connect()
            insert_query = "INSERT INTO `event_log` (`event_log_id`, `username`, `event_type_id`, `description`, `timestamp`) VALUES (NULL,\"%s\",NULL,\"%s\",\"%s\")"%(user_name,description,datetime.datetime.now())
            
            cursor = self.global_db.cursor()
            cursor.execute(insert_query)
            self.global_db.commit()
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()    
        except Exception as e:
            self.db_close()


class Essential(object):
    """
    @author: Rahul Gautam
    @since: 01-Dec-2011
    @version: 0.1
    @note: Logging Every Event and Action in Database   
    @organization: Codescape Consultants Pvt. Ltd.
    @copyright: 2011 Rahul Gautam for Codescape Consultants Pvt. Ltd.
    @see: http://www.codescape.in
        
    """
    global_db = None
    def db_connect(self):
        """
        Used to connect to the database :: return database object ed in global_db variable
        """
        db = None
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            self.global_db = db
        except MySQLdb.Error as e:
            print "/*/*/* MYSQLdb Exception (db connect) : "+str(e)
        except Exception as e:
            print "/*/*/* Database Exception (db connect) : "+str(e)
    
    
    def db_close(self):
        """
        closes connection with the database
        """
        try:
            self.global_db.close()
        except Exception as e:
            print "/*/*/* Database Exception ( db close ) : "+str(e)
            
    def get_hostgroup_ids(self,user_id):
        """
        @note: return hostgroup id as a list assigned to user
        """
        hostgroups_list = []
        try:
            self.db_connect()
            sel_query = """SELECT hostgroup_id FROM users_groups AS ug JOIN (SELECT hostgroup_id, group_id FROM hostgroups_groups) AS hg ON ug.group_id = hg.group_id WHERE ug.user_id =  '%s'"""%(user_id)
            
            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            hostgroups_list = [str(i[0]) for i in result]
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()    
        except Exception as e:
            self.db_close()
        finally:
            return hostgroups_list

    def get_host_id(self,value,what):
        """
        @note: return hostgroup id as a list assigned to user
        """
        host_id = None
        try:
            self.db_connect()
            sel_query = """SELECT host_id FROM hosts WHERE %s =  '%s'"""%(what,value)
            
            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                host_id = str(result[0][0])
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()    
        except Exception as e:
            self.db_close()
        finally:
            return host_id        
            
    def is_host_allow(self,user_id,hostid):
        """
        @note: Used Validate host and user mapping :: 1 is False
        """
        value = 1
        try:
            self.db_connect()
            sel_query = """SELECT hh.host_id FROM users_groups AS ug JOIN (SELECT hostgroup_id, group_id FROM hostgroups_groups) AS hg ON ug.group_id = hg.group_id
                            JOIN (SELECT host_id, hostgroup_id FROM hosts_hostgroups) AS hh ON hg.hostgroup_id = hh.hostgroup_id
                            WHERE ug.user_id =  '%s' and hh.host_id = '%s' """%(user_id,hostid)
            
            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) < 1:
                value = 1
            else:
                value = 0
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()    
        except Exception as e:
            self.db_close()
        finally:
            return value
    
    def host_status(self,hostid,status,host_ip=None,prev_status=0):
        """
        @host_status(1,0,None,10)
        @note: Used to update host operation status and varify it
        @dict: {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade', 3:'Restore default config', 4:'Flash commit', 5:'Reboot', 6:'Site survey', 7:'Calculate BW', 8:'Uptime service', 9:'Statistics gathering', 10:'Reconciliation', 11:'Table reconciliation', 12:'Set operation', 13:'Live monitoring', 14:'Status capturing'}
        """
        value = 0
        try:
            self.db_connect()
            if hostid:
                sel_query = """select status from host_status  where host_id = '%s'"""%(hostid)
            elif host_ip:
                sel_query = """select status from host_status  where host_ip = '%s'"""%(host_ip)
            else:
                value = 0 # error 100 
                return
            if status==None:
                value = 0 # error 100
                return 
            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                if int(result[0][0]) == prev_status or int(result[0][0]) == int(status):
                    if hostid:
                        up_query = """update host_status set status='%s' where host_id = '%s'"""%(status,str(hostid))
                    elif host_ip:
                        up_query = """update host_status set status='%s where host_ip = '%s'"""%(status,host_ip)
                    
                    cursor.execute(up_query)
                    self.global_db.commit()
                    value = 0
                else:
                    value = result[0][0]             
            else:
                value = 0 #value = 100 no row found
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()    
        except Exception as e:
            self.db_close()
        finally:
            return int(value)
        
    def get_hoststatus(self,hostid,host_ip=None):
        """
        @note: Used to update host operation status and varify it
        """
        value = 0
        try:
            self.db_connect()
            if hostid:
                sel_query = """select status from host_status  where host_id = '%s'"""%(hostid)
            elif host_ip:
                sel_query = """select status from host_status  where host_ip = '%s'"""%(host_ip)
            else:
                value = 0 # error 100 
                return
            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                value = result[0][0]
            else:
                value = 0 #value = 100 no row found
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()    
        except Exception as e:
            self.db_close()
        finally:
            return int(value)  
            
    def update_hoststatus(self,hostid,host_ip=None):
        """
        @note: Used to update host operation status
        """
        value = 0
        try:
            self.db_connect()
            if hostid:
                up_query = """update host_status set status='%s' where host_id = '%s'"""%(status,str(hostid))
            elif host_ip:
                up_query = """update host_status set status='%s where host_ip = '%s'"""%(status,host_ip)
            else:
                value = 0 # error 100 
                return
            cursor = self.global_db.cursor()
            cursor.execute(up_query)
            self.global_db.commit()
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()    
        except Exception as e:
            self.db_close()
        finally:
            return int(value)                     
