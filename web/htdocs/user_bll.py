#!/usr/bin/python2.6

"""
@author: Mahipal Choudhary
@since: 14-Nov-2011
@version: 0.1
@note: All database related functions Related user management.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in

@second_author     : Grijesh Chauhan
@Project           : TCL UNMP
@Version           : 0.2
@Updation date     : 8-February-2013
@Purpose           : improvemented code:
                     added method: check_pwd
"""

# Import modules that contain the function and libraries
import MySQLdb
from unmp_config import SystemConfig
from xlwt import Workbook, easyxf


class User_bll(object):
    """
    User management related BLL class
    """
# Required data for given user_id
    def get_data_for_settings(self, user_id):
        """

        @param user_id:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "Select first_name,last_name,designation,company_name,mobile_no,address,email_id from users \
    		       where user_id='%s' " % (user_id)

            cursor.execute(query)
            user_tuple = cursor.fetchall()
            # user_data=[]
            # make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            # for row in user_tuple:
            #    user_data.append(make_list(row))
            return user_tuple[0]
        except Exception, e:
            return 1
        finally:
            conn.close()

        # Set data for given user_id

    def set_data_for_settings(self, user_id,
                              first_name,
                              last_name,
                              company,
                              designation,
                              address,
                              mobile,
                              email_id):
        """

        @param user_id:
        @param first_name:
        @param last_name:
        @param company:
        @param designation:
        @param address:
        @param mobile:
        @param email_id:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = 'UPDATE `users` \
                     SET `first_name` = "%s", \
                         `last_name` = "%s", \
                         `company_name` = "%s", \
                         `designation` = "%s", \
                         `address` = "%s", \
                         `mobile_no` ="%s", \
                         `email_id` ="%s" \
                     WHERE `user_id` = "%s"' % (
                first_name,
                last_name,
                company,
                designation,
                address,
                mobile,
                email_id,
                user_id)

            cursor.execute(query)
            conn.commit()
            return 0
        except Exception, e:
            return 1
        finally:
            conn.close()

        # Required password for given user_id

    def get_data_for_settings_password(self, user_id):
        """

        @param user_id:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = 'SELECT `password` \
                     FROM `user_login` \
                     WHERE `user_id` = "%s"' % ( user_id)
            cursor.execute(query)
            user_tuple = cursor.fetchall()

            return user_tuple[0]
        except Exception, e:
            return 1
        finally:
            conn.close()

        # Set data for given user_id

    def set_data_for_settings_password(self, user_id, password):
        """

        @param user_id:
        @param password:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            password = conn.escape_string(password)
            query = """UPDATE `user_login`
                       SET `old_password`= `password` , `password` = SHA('%s'), `change_password_date` = NOW()
                       WHERE `user_id` ="%s"
                    """ % (password, user_id)
            cursor.execute(query)
            conn.commit()
            return 0
        except Exception, e:
            return 1
        finally:
            cursor.close()
            conn.close()

    def verify_first_login(self, username):
        """

        @param username:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = """UPDATE `login_info`
                       SET  `is_first_login`= 0 
                       WHERE `user_name` = '%s' AND `is_logged_in` = %s
                    """ % (username, '1')
            cursor.execute(query)
            conn.commit()
            return 0
        except Exception, e:
            return 1
        finally:
            conn.close()

        # checks password

    @staticmethod
    def check_password(user_id, pwd):
        """

        @param user_id:
        @param pwd:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            pwd = conn.escape_string(pwd)
            cursor = conn.cursor()
            query = """SELECT user_name,user_id
                      FROM user_login 
                      WHERE user_id='%s' AND password=SHA('%s') 
                  """ % (user_id, pwd)
            if cursor.execute(query) == 1:
                return 0
            return query
        except Exception, e:
            return 1
        finally:
            cursor.close()
            conn.close()
