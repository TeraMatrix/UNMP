#!/usr/bin/python2.6
# import the module
import MySQLdb
# import xml.dom.minidom
# import sys
# import os


def mysql_connection(database_name='nms'):
    """
    @return: this function return the cursor and database object.
    @rtype: Object.
    @requires: one argument(database name).
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 1 sept 2011
    @note: this function return the cursor and database object.
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    from unmp_config import SystemConfig

    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        #
        # sitename = __file__.split("/")[3]    # get site name of current nms.
        #
        # # set parameter and default values
        # mysql_host = "localhost"
        # mysql_user_name = "root"
        # mysql_password = "root"
        # mysql_db_schema = "nms_sample"
        #
        # try:
        #     # config.xml file path
        #     xml_config_file = "/omd/sites/%s/local/share/check_mk/web/htdocs/xml/config.xml" % sitename
        #
        #     if(os.path.isfile(xml_config_file)):
        #         dom = xml.dom.minidom.parse(
        #             xml_config_file)    # create xml dom object for config.xml file
        #         mysql_dom = dom.getElementsByTagName("mysql")
        #         for m in mysql_dom:
        #             mysql_host = m.getAttribute("hostname")
        #             mysql_user_name = m.getAttribute("username")
        #             mysql_password = m.getAttribute("password")
        #             mysql_db_schema = m.getAttribute("schema")
        #
        #     db = MySQLdb.connect(
        #         mysql_host, mysql_user_name, mysql_password, mysql_db_schema)

        cursor = db.cursor()
        return db, cursor
    except MySQLdb.Error as e:
        return 1, str(e[-1])
