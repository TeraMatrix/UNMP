#!/usr/bin/python2.6

#======================================================
# Author: Yogesh Kumar (ccpl)
# This file is used for get database connection.
#======================================================

# import packages
import MySQLdb, xml.dom.minidom, sys, os
from sqlalchemy import create_engine

# load mysql credentials from config.xml file
def get_mysql_credentials():
    sitename = __file__.split("/")[3]	# get site name

    # set parameter and default values
    mysql_host = "localhost"
    mysql_user_name = "root"
    mysql_password = "root"
    mysql_db_schema = "nms"

    # config.xml file path
    xml_config_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/config.xml" % sitename
    try:
        # check config.xml file exist or not
        if(os.path.isfile(xml_config_file)):
            dom = xml.dom.minidom.parse(xml_config_file)	# create xml dom object for config.xml file
            mysql_dom = dom.getElementsByTagName("mysql")
            for m in mysql_dom:
                mysql_host = m.getAttribute("hostname")
                mysql_user_name = m.getAttribute("username")
                mysql_password = m.getAttribute("password")
                mysql_db_schema = m.getAttribute("schema")
        return mysql_host,mysql_user_name,mysql_password,mysql_db_schema
    except:
        #print sys.exc_info()
        return mysql_host,mysql_user_name,mysql_password,mysql_db_schema


# Open database connection
def open_database_connection():
    try:
        mysql_host,mysql_user_name,mysql_password,mysql_db_schema = get_mysql_credentials()
        db = MySQLdb.connect(mysql_host,mysql_user_name,mysql_password,mysql_db_schema)
        return db
    except:
        return None

#close database connection
def close_connection(db_obj):
    db_obj.close()


# load sqlalchemy credentials from config.xml file
def get_sqlalchemy_credentials():
    sitename = __file__.split("/")[3]	# get site name
    #sitename='nms2'
    # set parameter and default values
    sqlalchemy_host = "localhost"
    sqlalchemy_user_name = "root"
    sqlalchemy_password = "root"
    sqlalchemy_schema = "nms_sample"
    sqlalchemy_driver="mysql"

    # config.xml file path
    xml_config_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/config.xml" % sitename
    #xml_config_file = "nms2"
    try:
        # check config.xml file exist or not
        if(os.path.isfile(xml_config_file)):
            dom = xml.dom.minidom.parse(xml_config_file)	# create xml dom object for config.xml file
            mysql_dom = dom.getElementsByTagName("sqlalchemy")
            for m in mysql_dom:
                sqlalchemy_host = m.getAttribute("hostname")
                sqlalchemy_user_name = m.getAttribute("username")
                sqlalchemy_password = m.getAttribute("password")
                sqlalchemy_schema = m.getAttribute("schema")
                sqlalchemy_driver=m.getAttribute("driver")
        return sqlalchemy_host ,sqlalchemy_user_name ,sqlalchemy_password ,sqlalchemy_schema,sqlalchemy_driver
    except:
        #print sys.exc_info()
        return sqlalchemy_host ,sqlalchemy_user_name ,sqlalchemy_password ,sqlalchemy_schema,sqlalchemy_driver

# Open database connection for sqlalchemy
def open_database_sqlalchemy_connection():
    try:
        sqlalchemy_host ,sqlalchemy_user_name ,sqlalchemy_password ,sqlalchemy_schema,sqlalchemy_driver = get_sqlalchemy_credentials()
        db=create_engine("%s://%s:%s@%s/%s"%(sqlalchemy_driver,sqlalchemy_user_name,sqlalchemy_password,sqlalchemy_host,sqlalchemy_schema))
        db_connect = db.connect()
        return db_connect
    except:
        return None

#Close database connection for sqlalchemy
def close_database_sqlalchemy_connection(db_obj_sqlalchemy):
    db_obj_sqlalchemy.close()

def get_refresh_time():
    sitename = __file__.split("/")[3]	# get site name
    refresh_time = 1			# default time

    # config.xml file path
    xml_config_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/config.xml" % sitename
    try:
        # check config.xml file exist or not
        if(os.path.isfile(xml_config_file)):
            dom = xml.dom.minidom.parse(xml_config_file)	# create xml dom object for config.xml file
            dashboard_dom = dom.getElementsByTagName("dashboard")
            for d in dashboard_dom:
                refresh_time = d.getAttribute("refresh")
        return refresh_time
    except:
        #print sys.exc_info()
        return refresh_time

def restart_nagios():
    sitename = __file__.split("/")[3]	# get site name
    try:
        os.system('kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
        return 0
    except:
        return 1

class SqlalchemyConnection:
    def open_database_sqlalchemy_connection():
        try:
            sqlalchemy_host ,sqlalchemy_user_name ,sqlalchemy_password ,sqlalchemy_schema,sqlalchemy_driver = get_sqlalchemy_credentials()
            db=create_engine("%s://%s:%s@%s/%s"%(sqlalchemy_driver,sqlalchemy_user_name,sqlalchemy_password,sqlalchemy_host,sqlalchemy_schema))
            db_connect = db.connect()
            return db_connect
        except:
            return None