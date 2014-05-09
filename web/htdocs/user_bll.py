#!/usr/bin/python2.6

'''
@author: Mahipal Choudhary
@since: 14-Nov-2011
@version: 0.1
@note: All database related functions Related user management. 
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
import MySQLdb
from unmp_config import SystemConfig
from xlwt import Workbook, easyxf

class User_bll(object):
# Required data for given user_id
    def get_data_for_settings(self,user_id):
        try:
            conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor ()
            query="Select first_name,last_name,designation,company_name,mobile_no,address,email_id from users \
    		       where user_id='%s' " %(user_id)
            cursor.execute(query)
            user_tuple=cursor.fetchall()
            #user_data=[]
            #make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            #for row in user_tuple:
            #    user_data.append(make_list(row))
            return user_tuple[0]
        except Exception,e:
            return 1
        finally:
            conn.close() 

# Set data for given user_id
    def set_data_for_settings(self,user_id,first_name,last_name,company,designation,address,mobile,email_id):
        try:
            conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor ()
            query='update users set first_name="%s",last_name="%s",company_name="%s",designation="%s",address="%s",mobile_no="%s",email_id="%s"\
    		       where user_id="%s"' %(first_name,last_name,company,designation,address,mobile,email_id,user_id)
            cursor.execute(query)
            conn.commit()
            return 0  
        except Exception,e:
            return 1
        finally:
            conn.close() 

# Required password for given user_id
    def get_data_for_settings_password(self,user_id):
        try:
            conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor ()
            query='Select password from user_login where user_id="%s"' %(user_id)
            cursor.execute(query)
            user_tuple=cursor.fetchall()
            #user_data=[]
            #make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            #for row in user_tuple:
            #    user_data.append(make_list(row))
            return user_tuple[0]
        except Exception,e:
            return 1
        finally:
            conn.close() 

# Set data for given user_id
    def set_data_for_settings_password(self,user_id,password):
        try:
            conn = MySQLdb.connect (*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor ()
            query='update user_login set password="%s" where user_id="%s"' %(password,user_id)
            cursor.execute(query)
            conn.commit()
            return 0
        except Exception,e:
            return 1
        finally:
            conn.close() 