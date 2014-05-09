#!/usr/bin/python2.6

'''
@author		: Mahipal Choudhary
@since		: 07-Dec-2011
@version	: 0.1
@note		: All database related functions related to retrieving log data. 
@organization	: Codescape Consultants Pvt. Ltd.
@copyright	: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see		: http://www.codescape.in
'''

# Import modules that contain the function and libraries
import MySQLdb
from unmp_config import SystemConfig


class HostgroupMgmtBll(object):
    def get_hostgroup_data(self,hostgroup_ids_list = ['44','64']):
        '''
        @author			: Mahipal Choudhary
        @since			: 07-Dec-2011
        @requires		: nothing
        @var conn		: object of MySQLdb connection
        @var cursor		: object of cursor of connection 
        @var query		: the SQL Query which will be executed to get log data
        @var log_tuple		: the tuple which stores the data after we execute the query
        @var row		: variable for looping
        @var log_list		: list containing the log data	
        @note			: This is the function to get complete data for logs
        '''
        try:
            lis = []
            if len(hostgroup_ids_list) > 0:
                conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
                cursor = conn.cursor ()

                query="select hg.hostgroup_id,hg.hostgroup_name,g.group_name from hostgroups as hg \
			left join ( select hostgroup_id , group_id from hostgroups_groups) as hgg on hgg.hostgroup_id=hg.hostgroup_id \
			left join (select group_name , group_id from groups )  as g on g.group_id =hgg.group_id WHERE hgg.hostgroup_id in (%s) order by hg.hostgroup_name "%','.join(hostgroup_ids_list)
                cursor.execute(query)
        #       host_tuple=cursor.fetchall()
                tp=cursor.fetchall()
                di = {}
                li = []
                id=0
                make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
                for t in tp:
                    if di.has_key(int(t[0])):
                        li = di[int(t[0])]
                        grps = li.pop()
                        grps += "  , "+t[2]
                        li.append(grps)
                        di[int(t[0])] = li
                    else:
                        li = make_list(t)
                        di[int(t[0])] = li
                lis= di.values()
                for i in range(0,len(lis)):
                    id=lis[i].pop(0)
                    lis[i].append('<button class="yo-button" type="button" id="%s" name="%s" ><span class="edit">Manage</span></button>' %(id,lis[i][0]))

            return lis

        except Exception,e:
            return str(e)
        finally:
            conn.close() 

    def get_usergroup_data(self,host_id,flag_grp=0):
        '''
        @author			: Mahipal Choudhary
        @since			: 07-Dec-2011
        @requires		: nothing
        @var conn		: object of MySQLdb connection
        @var cursor		: object of cursor of connection 
        @var query		: the SQL Query which will be executed to get log data
        @var log_tuple		: the tuple which stores the data after we execute the query
        @var row		: variable for looping
        @var log_list		: list containing the log data	
        @note			: This is the function to get complete data for logs
        '''
        try:
            conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor ()
            if flag_grp == 1: # is superadmin
                query="select g.group_id,g.group_name,CONCAT( CONCAT(u.first_name ,' '),u.last_name) from users as u\
                    left join ( select hostgroup_id , group_id from hostgroups_groups) as hgg on hgg.hostgroup_id='%s' \
                    left join (select user_id , group_id from users_groups )  as ug on ug.group_id =hgg.group_id\
                    left join (select group_name , group_id from groups )  as g on ug.group_id =g.group_id \
                    where ug.user_id=u.user_id order by g.group_name" %(host_id)
            else:
                query="select g.group_id,g.group_name,CONCAT( CONCAT(u.first_name ,' '),u.last_name) from users as u\
                    left join ( select hostgroup_id , group_id from hostgroups_groups) as hgg on hgg.hostgroup_id='%s' \
                    left join (select user_id , group_id from users_groups )  as ug on ug.group_id =hgg.group_id\
                    left join (select group_name , group_id from groups )  as g on ug.group_id =g.group_id \
                    where ug.user_id=u.user_id and g.group_name<>'SuperAdmin' order by g.group_name" %(host_id)

            cursor.execute(query)
            tp=cursor.fetchall()
            di = {}
            li = []
            id=0
            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            for t in tp:
                if di.has_key(str(t[0])):
                    li = di[str(t[0])]
                    grps = li.pop()
                    grps += " ,  "+t[2]
                    li.append(grps)
                    di[str(t[0])] = li
                else:
                    li = make_list(t)
                    di[str(t[0])] = li
            lis= di.values()
            for i in range(0,len(lis)):
                pid=lis[i].pop(0)
                lis[i].insert(0,'<div id="ck_box"><input type="checkbox" name="group_check" value="%s" />' %(pid))
                lis[i].append('<img class=\"img-link\" src=\"images/new/info.png\" title=\"View User Details\" onclick=\"viewGroupDetails(\'%s\');\">' %(pid))
            #return lis
            #if(len(lis)==0):
            #    return []
            if flag_grp == 1:
                query2="select g.group_name,g.group_id  from hostgroups as h \
                left join ( select hostgroup_id , group_id from hostgroups_groups) as hgg on hgg.hostgroup_id=h.hostgroup_id \
                left join ( select group_name , group_id from groups ) as g on g.group_id=hgg.group_id \
                where h.hostgroup_id='%s' " %(host_id)
            else:
                query2="select g.group_name,g.group_id  from hostgroups as h \
                left join ( select hostgroup_id , group_id from hostgroups_groups) as hgg on hgg.hostgroup_id=h.hostgroup_id \
                left join ( select group_name , group_id from groups ) as g on g.group_id=hgg.group_id \
                where h.hostgroup_id='%s' and g.group_name<>'SuperAdmin' " %(host_id)
            cursor.execute(query2)
            tp2=cursor.fetchall()
            tr=[]
            lis_group=[]
            flag=0
            lism=[]
            for i in tp2:
                lism.append(i)
            lis_temp = sum(lis,[])
            for i in lism:
                flag=0
                if lis_temp.count(i[0])==0:
                    tr=[]
                    pid=i[1]
                    tr.append('<div id="ck_box"><input type="checkbox" name="group_check" value="%s" />' %(pid))
                    tr.append(i[0])
                    tr.append(" ")
                    tr.append('<img class=\"img-link\" src=\"images/new/info.png\" title=\"View User Details\" onclick=\"viewGroupDetails(\'%s\');\">' %(pid))
                    lis_group.append(tr)

            if (len(lis_group))==0:
                return lis
            else : 
                return lis+lis_group
        except Exception,e:
            return str(e)
        finally:
            conn.close()



    def get_usergroup_details(self,group_id):
        try:
            conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor ()
            query="SELECT CONCAT( CONCAT(u.first_name ,' '),u.last_name),u.mobile_no,u.email_id FROM `users`  as u \
                    LEFT JOIN (select group_id , user_id from users_groups) as ug on ug.user_id=u.user_id \
                    where ug.group_id='%s' order by u.first_name" %(group_id)
            cursor.execute(query)
            tp=cursor.fetchall()
            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            li=[]
            for t in tp:
                li.append(make_list(t))
            return li
        except Exception,e:
            return str(e)
        finally:
            conn.close()
