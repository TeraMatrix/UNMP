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


class ManageLoginBll(object):
    def get_login_data(self, user_id, username=None):
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
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            # query="SELECT lg.user_name , CONCAT(CONCAT(users.first_name,'
            # '),users.last_name) , lg.login_time ,lg.is_logged_in FROM
            # `login_info` as lg JOIN (select user_id ,user_name from
            # user_login) as ul on lg.user_name=ul.user_name join (select
            # first_name,last_name,user_id from users ) as users on
            # users.user_id=ul.user_id order by lg.login_time"
            query = "SELECT lg.user_name , CONCAT(CONCAT(users.first_name,' '),users.last_name) , \
                            groups.group_name, lg.login_time ,lg.is_logged_in, lg.last_accessed_time  \
                    FROM `login_info` as lg\
			 JOIN (select user_id ,user_name from user_login) as ul on lg.user_name=ul.user_name \
			 JOIN (select first_name,last_name,user_id from users ) as users  on users.user_id=ul.user_id \
			 JOIN (select user_id, group_id from users_groups) as ug on ug.user_id= users.user_id \
			 JOIN (select group_name , group_id,role_id from groups ) as groups on groups.group_id=ug.group_id \
			 join (select role_id,role_name from roles ) as roles  on roles.role_id=groups.role_id \
				order by lg.login_time desc"
            cursor.execute(query)
            log_tuple = cursor.fetchall()
            query = "select group_name from users_groups join (select group_name , group_id,role_id from groups ) as groups on groups.group_id=users_groups.group_id \
            	  join (select role_id,role_name from roles ) as roles  on roles.role_id=groups.role_id\
            	  where users_groups.user_id='%s'" % (user_id)
            cursor.execute(query)
            res2 = cursor.fetchall()
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            log_list = []
            for row in log_tuple:
                temp_list = make_list(row)
                if temp_list[4] == "1":
                    temp_list[4] = "Yes"
                    if (res2[0][0] == "SuperAdmin"):
                        if (temp_list[2] == "SuperAdmin"):
                            # temp_list.pop()
                            temp_list.append(
                                '<button class=\"destroy-button\" disabled="disabled" id="del_user_%s" >Destroy</button>' % (
                                temp_list[0]))
                        else:
                            # temp_list.pop()
                            temp_list.append(
                                '<button class=\"destroy-button\" id="del_user_%s" onclick="delUser(\'%s\');">Destroy</button>' % (
                                temp_list[0], temp_list[0]))
                    else:
                        if (temp_list[2] == "Admin" or temp_list[2] == "SuperAdmin"):
                            # temp_list.pop()
                            temp_list.append(
                                '<button class=\"destroy-button\" disabled="disabled"  id="del_user_%s" >Destroy</button>' % (
                                temp_list[0]))
                        else:
                            if username.lower() == temp_list[0].lower():
                                temp_list.append(
                                    '<button class=\"destroy-button\" disabled="disabled"  id="del_user_%s" >Destroy</button>' % (
                                    temp_list[0]))
                            else:
                            # temp_list.pop()
                            # temp_list.append('<img original-title="Delete
                            # User" style="width: 18px; height: 18px; margin:
                            # 6px 20px 6px 10px;"  id="del_user_%s"
                            # src="images/new_icons/logoutuser.png" class="n
                            # -tip-image" onclick="delUser(\'%s\');">'
                            # %(temp_list[0],temp_list[0]))
                                temp_list.append(
                                    '<button class=\"destroy-button\" id="del_user_%s" onclick="delUser(\'%s\');">Destroy</button>' % (
                                    temp_list[0], temp_list[0]))

                else:
                    temp_list[4] = "No"
                    # temp_list.pop() # on location 4 groupname is stored
                    temp_list.append(
                        '<button class=\"destroy-button\" disabled="disabled"  id="del_user_%s" >Destroy</button>' % (
                        temp_list[0]))
                log_list.append(temp_list)
            return log_list
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def set_session_delete(self, user_id):
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
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "update login_info set next_time_delete=1,is_logged_in=0 where user_name='%s'" % (
                user_id)
            cursor.execute(query)
            conn.commit()
            return 0
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def get_role_name(self, user_name):
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
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "select group_name from users_groups join (select group_name , group_id from groups ) as groups on groups.group_id=users_groups.group_id join \
 		   (select user_name,user_id from user_login ) as ul on ul.user_id=users_groups.user_id and ul.user_name='%s'" % (
            user_name)
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def update_login(self, user_id):
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
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "update login_info set is_logged_in='0' where user_name='%s'" % (
                user_id)
            cursor.execute(query)
            conn.commit()
            return []
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def get_role(self, user_id):
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
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "select group_name from users_groups join (select group_name , group_id from groups ) as groups on groups.group_id=users_groups.group_id \
            	  where users_groups.user_id='%s'" % (user_id)
            cursor.execute(query)
            res = cursor.fetchall()
            return res[0][0]
        except Exception, e:
            return str(e)
        finally:
            conn.close()
