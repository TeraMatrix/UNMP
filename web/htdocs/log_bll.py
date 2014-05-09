#!/usr/bin/python2.6

'''
@author: Mahipal Choudhary
@since: 07-Dec-2011
@version: 0.1
@note: All database related functions Related log management. 
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
import MySQLdb
from unmp_config import SystemConfig

class Log_bll(object):
# Required data for given user_id
    def get_log_data_bll(self,sEcho,iColumns,iDisplayLength,iDisplayStart,sColumns,sSearch,iSortCol_0,sSortDir_0):
    	try:
    	    db = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
    	    a_columns=["timestamp", "username" , "description"]
    	    s_table = "event_log"
    	    s_index_column = "timestamp"
    	    #query="Select timestamp, username , description from event_log order by timestamp desc"
    	    s_limit = ""
    	    #iDisplayLength,iDisplayStart
	    if (iDisplayStart != None and iDisplayLength != '-1'):
		s_limit = "LIMIT %s, %s" % (MySQLdb.escape_string(iDisplayStart),MySQLdb.escape_string(iDisplayLength))
	    # Ordering
	    #s_order = "ORDER BY timestamp desc,  "
	    s_order="ORDER BY  "
	    if iSortCol_0 != None and iSortCol_0!=-1:
	                s_order += "%s %s, " % (a_columns[int(iSortCol_0)],sSortDir_0)
	                s_order = s_order[:-2]
	
		# Filtering
	    s_where = "";
	    if sSearch != "":
			s_where = "WHERE ("
			for i in range(0,len(a_columns)):
				s_where += "%s LIKE '%%%s%%' OR " % (a_columns[i],MySQLdb.escape_string(sSearch))
			s_where = s_where[:-3]
			s_where += ")"
	
	    cursor = db.cursor()

	    # SQL queries
	    # Get data to display
	    sql_query = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s" % (", ".join(a_columns).replace(" , "," "),s_table,s_where,s_order,s_limit)
	    # create sql query - End
	    # execute sql query
	    cursor.execute(sql_query)
	    # fetch data from executed sql query
	    r_result = cursor.fetchall()
	    # close the cursor
	    cursor.close()
	    # prepare a cursor object using cursor() method
	    cursor = db.cursor()
	    # Data set length after filtering
	    sql_query = "SELECT FOUND_ROWS()"
	    # execute sql query
	    cursor.execute(sql_query)
	    # fetch data from executed sql query
	    i_filtered_total = cursor.fetchone()[0]
	    # close the cursor
	    cursor.close()
	    # prepare a cursor object using cursor() method
	    cursor = db.cursor()

	    # Total data set length
	    sql_query = "SELECT COUNT(%s) FROM %s" % (s_index_column,s_table)

	    # execute sql query
	    cursor.execute(sql_query)

	    # fetch data from executed sql query
	    i_total = cursor.fetchone()[0]

	    # close the cursor
	    cursor.close()

	    result_data = []
	    make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
	    for row in r_result:
                result_data.append(make_list(row))
	    # Output
	    output = {
			"sEcho": sEcho,
			"iTotalRecords": i_total,
			"iTotalDisplayRecords": i_filtered_total,
			"aaData":result_data
	    }

	    return output
    	except Exception,e:
	    output = {
			"sEcho": 0,
			"iTotalRecords": [],
			"iTotalDisplayRecords": [],
			"aaData":[],
			"exception":str(e)
	    }

	    # Encode Data into JSON
	    return output
    	finally:
    	    db.close() 
    	    
    def get_header_data(self):
    	try:
    	    conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
    	    cursor = conn.cursor ()
    	    query="Select timestamp, username , description from event_log order by timestamp desc limit 5"
            cursor.execute(query)
            log_tuple=cursor.fetchall()
            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            log_list=[]
            for row in log_tuple:
                log_list.append(make_list(row))
            return log_list
    	except Exception,e:
    	    return []
    	finally:
    	    conn.close() 
    	    
    	    
    	    
    def get_alarm_header_data(self,hostgroup_id_list):
    	try:
    	    conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
    	    cursor = conn.cursor ()
    	    query="SELECT t.serevity,STR_TO_DATE(t.trap_receive_date,'%a %b %e %H:%i:%s %Y'),t.trap_event_type,t.event_id,h.device_type_id,h.host_alias,t.agent_id,t.description FROM \
    	    			    trap_alarm_current as t \
    	    			INNER JOIN hosts as h ON t.agent_id=h.ip_address \
				INNER JOIN hosts_hostgroups ON hosts_hostgroups.host_id = h.host_id "
	    query+="    	INNER JOIN hostgroups ON hostgroups.hostgroup_id = hosts_hostgroups.hostgroup_id WHERE  hostgroups.hostgroup_id IN (%s) \
				 order by t.trap_receive_date desc limit 5 "%(','.join(hostgroup_id_list))
            cursor.execute(query)
            log_tuple=cursor.fetchall()
            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            log_list=[]
            for row in log_tuple:
                log_list.append(make_list(row))
            return log_list
    	except Exception,e:
    	    return str(e)
    	finally:
    	    conn.close()     	    
