#!/usr/bin/python2.6

"""
@author: Yogesh Kumar
@since: 21-Oct-2011
@date: 21-Oct-2011
@version: 0.1
@note: There is one Class that use to load System Configuration.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""

# import packages
import xml.dom.minidom
import os


def str2bool(v):
    """String to bool
      ----------------
    return bool for string object
    a helper function for get_pwd_expiry_details()
    @param v:
    """
    return v.lower() in ("yes", "true", "t", "1")


class SystemConfig(object):
    """
    @author: Yogesh Kumar
    @since: 21-Oct-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to fetch the data of configuration from xml file.
    """

    @staticmethod
    def load_config_file():
        """
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @return: xml dom object
        @rtype: xml.dom.minidom
        @note: This function load the xml file and return xml dom object.
        @summary: How To use:
        load_config_file()     return: [dom object]
        load_config_file()     return: Exception object or None
        """
        nms_instance = __file__.split(
            "/")[3]                           # it gives instance name of nagios system
        xml_config_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/config.xml" % nms_instance                        # config.xml file path
        try:
            if (os.path.isfile(xml_config_file)):                        # check config.xml file exist or not
                dom = xml.dom.minidom.parse(
                    xml_config_file)            # create xml dom object of config.xml file
                return dom
            else:
                print xml_config_file
                return None
        except Exception:
            return None

    @staticmethod
    def get_config_attributes(tag_name, attribute_name, get_text=False):
        """



        @param tag_name:
        @param attribute_name:
        @param get_text:
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @var tag_name: tag name that you want to get
        @var attribute_name: attribute list that you want to fetch
        @var get_text: True/False to fetch text value of passed tag_name
        @return: attribute values list and text values list
        @rtype: tuple
        @note: This function gives tag attribute's value and text.
        @summary: How To use:
        get_config_attributes("mysql",["username","password"],False)     return: ([["root","root"],],)
        get_config_attributes("mysql",["username","password"],True)     return: ([["root","root"],],"text")
        """
        dom = SystemConfig.load_config_file(
        )                        # create xml dom of config file
        dom_element = dom.getElementsByTagName(
            tag_name)            # get the element by tag name
        attribute_value = []                                        # declare attribute value list	(2D)
        text_value = []                                                # declare text value list		(1D)
        for elem in dom_element:                                    # iterate selected elements
            attr_value = []                                            # declare attr_value list		(2D)
            for attr in attribute_name:                                # iterate attributes
                attr_value.append(elem.getAttribute(
                    attr))            # append attribute_value in attr_value
            attribute_value.append(
                attr_value)                        # append attr_value in attribute_value
            if get_text is True:
                text_value.append(SystemConfig.get_tag_text(
                    elem.childNodes))  # append text value in text_value if get_text is True
        if get_text is True:
            return attribute_value, text_value
        else:
            return attribute_value

    @staticmethod
    def get_tag_text(node):
        """

        @param node:
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @para node: xml dom element's child node object
        @return: text of tag
        @rtype: string
        @note: This function gives text of tag [xml dom element's]
        @summary: How To use:
        get_tag_text(dom_element)     return: string
        """
        rc = []
        # rc list that store the text value and their child text
        for n in node:
            if n.nodeType == n.TEXT_NODE:                            # check the node type is TEXT_NODE or not
                rc.append(n.data)                                    # append text node to rc list
        return ''.join(rc)

    @staticmethod
    def get_mysql_credentials():
        """
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @return: tuple of mysql credentials [tuple (host-name,user-name,password,database-name)]
        @rtype: tuple
        @note: This function gives you the mysql credentails tuple
        @summary: How To use:
        get_mysql_credentials()     return: ("localhost","root","root","nms")
        """
        # return ("localhost","root","root","nms")
        credentials = SystemConfig.get_config_attributes(
            "mysql", ["hostname", "username", "password", "schema"], False)
        if len(credentials) > 0:
            return tuple(credentials[0])
        else:
            return ("localhost", "root", "root", "nms")        # Default Configuration

    @staticmethod
    def get_sqlalchemy_credentials():
        """
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @return: tuple of sqlalchemy credentials [tuple (sqlalchemy_driver,sqlalchemy_user_name,sqlalchemy_password,sqlalchemy_host,sqlalchemy_schema)]
        @rtype: tuple
        @note: This function gives you the sqlalchemy credentails tuple
        @summary: How To use:
        get_sqlalchemy_credentials()     return: (sqlalchemy_driver,sqlalchemy_user_name,sqlalchemy_password,sqlalchemy_host,sqlalchemy_schema)
        """
        # return ("mysql","root","root","localhost","nms")
        credentials = SystemConfig.get_config_attributes(
            "mysql", ["driver", "username", "password", "hostname", "schema"], False)
        if len(credentials) > 0:
            return tuple(credentials[0])
        else:
            return ("mysql", "root", "root", "localhost", "nms")        # Default Configuration

    @staticmethod
    def get_default_dashboard_refresh_time():
        """
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @return: refresh time in mins.
        @rtype: int
        @note: This function gives you the time in mins.
        @summary: How To use:
        get_default_dashboard_refresh_time()     return: 5
        """
        refresh_time = SystemConfig.get_config_attributes(
            "dashboard", ["refresh"], False)
        if len(refresh_time) > 0 and len(refresh_time[0]):
            return int(refresh_time[0][0])
        else:
            return 5        # Default mins.

    @staticmethod
    def get_page_credentials():
        """
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @return: get page credentials like start page,page title and refresh time.
        @rtype: dictionary
        @note: This function gives you the page credentials.
        @summary: How To use:
        get_page_credentials()     return: {start_page:"main.py",title:"Network Management System",refresh:1}
        """
        credentials = SystemConfig.get_config_attributes(
            "page", ["start", "title", "refresh"], False)
        if len(credentials) > 0 and len(credentials[0]) > 2:
            return {"start_page": credentials[0][0], "title": credentials[0][1], "refresh": int(credentials[0][2])}
        else:
            return {"start_page": "main.py", "title": "Network Management System",
                    "refresh": 5}        # Default Configuration

    @staticmethod
    def get_company_details():
        """
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @return: get company details like company name and website.
        @rtype: dictionary
        @note: This function gives you the company details.
        @summary: How To use:
        get_company_details()     return: {name:"CCPL","website":"http://www.codescape.in"}
        """
        credentials = SystemConfig.get_config_attributes(
            "company", ["name", "website"], False)
        if len(credentials) > 0 and len(credentials[0]) > 1:
            return {"name": credentials[0][0], "website": credentials[0][1]}
        else:
            return {"name": "CCPL", "website": "http://www.codescape.in"}        # Default Configuration

    @staticmethod
    def get_system_about_us():
        """
        @author: Yogesh Kumar
        @since: 21-Oct-2011
        @version: 0.1
        @return: get system details like version number.
        @rtype: dictionary
        @note: This function gives you the system details.
        @summary: How To use:
        get_system_about_us()     return: {version:"version 1.0"}
        """
        credentials = SystemConfig.get_config_attributes(
            "aboutus", ["version"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"version": credentials[0][0]}
        else:
            return {"version": "version 1.0"}        # Default Configuration

    @staticmethod
    def get_default_lat_long():
        """
        @author: Yogesh Kumar
        @since: 03-Nov-2011
        @version: 0.1
        @return: get default longitude and latitude of nms.
        @rtype: dictionary
        @note: This function gives you default longitude and latitude of nms.
        @summary: How To use:
        get_default_lat_long()     return: {latitude:"23.0",longitude:"27.0"}
        """
        credentials = SystemConfig.get_config_attributes(
            "googlemap", ["latitude", "longitude"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"latitude": credentials[0][0], "longitude": credentials[0][1]}
        else:
            return {"latitude": "23.0", "longitude": "27.0"}        # Default Configuration

    @staticmethod
    def get_host_http_details():
        """
        @author: Yogesh Kumar
        @since: 03-Nov-2011
        @version: 0.1
        @return: get default http username, password and port for hosts.
        @rtype: dictionary
        @note: This function gives you default http username, password and port for hosts.
        @summary: How To use:
        get_host_http_details()     return: {username:"admin",password:"password",port:""}
        """
        credentials = SystemConfig.get_config_attributes(
            "http", ["username", "password", "port"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"username": credentials[0][0], "password": credentials[0][1], "port": credentials[0][2]}
        else:
            return {"username": "admin", "password": "password", "port": ""}        # Default Configuration

    @staticmethod
    def get_host_snmp_details():
        """
        @author: Yogesh Kumar
        @since: 03-Nov-2011
        @version: 0.1
        @return: get default snmp read/write community,version and port for hosts.
        @rtype: dictionary
        @note: This function gives you default snmp read/write community,version and port for hosts.
        @summary: How To use:
        get_host_snmp_details()     return: {read_comm:"public",write_comm:"private",version:"2c",get_set_port:"161",trap_port:"162"}
        """
        credentials = SystemConfig.get_config_attributes(
            "snmp", ["readcomm", "writecomm", "version", "getsetport", "trapport"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"read_comm": credentials[0][0], "write_comm": credentials[0][1], "version": credentials[0][2],
                    "get_set_port": credentials[0][3], "trap_port": credentials[0][4]}
        else:
            return {"read_comm": "public", "write_comm": "private", "version": "2c", "get_set_port": "161",
                    "trap_port": "162"}        # Default Configuration

    @staticmethod
    def get_host_other_details():
        """
        @author: Yogesh Kumar
        @since: 04-Nov-2011
        @version: 0.1
        @return: get default state and priority for hosts.
        @rtype: dictionary
        @note: This function gives you default state and priority for hosts.
        @summary: How To use:
        get_host_other_details()     return: {host_state:"e",host_priority:"normal"}
        """
        credentials = SystemConfig.get_config_attributes(
            "host", ["state", "priority"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"host_state": credentials[0][0], "host_priority": credentials[0][1]}
        else:
            return {"host_state": "e", "host_priority": "normal"}        # Default Configuration

    @staticmethod
    def get_host_config_details():
        """
        @author: Yogesh Kumar
        @since: 04-Nov-2011
        @version: 0.1
        @return: get default state and priority for hosts.
        @rtype: dictionary
        @note: This function gives you default state and priority for hosts.
        @summary: How To use:
        get_host_other_details()     return: {host_state:"e",host_priority:"normal"}
        """
        credentials = SystemConfig.get_config_attributes(
            "hostconfig", ["use_template", "check_command"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"use_template": credentials[0][0], "check_command": credentials[0][1]}
        else:
            return {"use_template": "generic-host", "check_command": "check-host-alive"}        # Default Configuration

    @staticmethod
    def get_service_config_details():
        """
        @author: Yogesh Kumar
        @since: 04-Nov-2011
        @version: 0.1
        @return: get default state and priority for hosts.
        @rtype: dictionary
        @note: This function gives you default state and priority for hosts.
        @summary: How To use:
        get_host_other_details()     return: {host_state:"e",host_priority:"normal"}
        """
        credentials = SystemConfig.get_config_attributes(
            "serviceconfig", ["use_template", "max_check_attempts", "normal_check_interval", "retry_check_interval"],
            False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"use_template": credentials[0][0], "max_check_attempts": credentials[0][1],
                    "normal_check_interval": credentials[0][2], "retry_check_interval": credentials[0][3]}
        else:
            return {"use_template": "generic-service", "max_check_attempts": "1", "normal_check_interval": "5",
                    "retry_check_interval": "5"}        # Default Configuration

    @staticmethod
    def get_ping_details():
        """
        @author: Yogesh Kumar
        @since: 16-Nov-2011
        @version: 0.1
        @return: get default values of ping discovery.
        @rtype: dictionary
        @note: This function gives you default values of ping discovery.
        @summary: How To use:
        get_ping_details()     return: {"ping_ip_base":"192.168.0","ping_ip_base_start":"0","ping_ip_base_end":"50","ping_timeout":"5","ping_service_mng":"2"}
        """
        credentials = SystemConfig.get_config_attributes(
            "pingdiscovery", ["ip_base", "ip_base_start",
                              "ip_base_end", "timeout", "service"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"ping_ip_base": credentials[0][0], "ping_ip_base_start": credentials[0][1],
                    "ping_ip_base_end": credentials[0][2], "ping_timeout": credentials[0][3],
                    "ping_service_mng": credentials[0][4]}
        else:
            return {"ping_ip_base": "192.168.0", "ping_ip_base_start": "0", "ping_ip_base_end": "50",
                    "ping_timeout": "5", "ping_service_mng": "2"}        # Default Configuration

    @staticmethod
    def get_snmp_details():
        """
        @author: Yogesh Kumar
        @since: 16-Nov-2011
        @version: 0.1
        @return: get default values of snmp discovery.
        @rtype: dictionary
        @note: This function gives you default values of snmp discovery.
        @summary: How To use:
        get_snmp_details()     return: {"snmp_ip_base":"192.168.0","snmp_ip_base_start":"0","snmp_ip_base_end":"50","snmp_timeout":"5","snmp_service_mng":"2","snmp_community":"public","snmp_port":"22","snmp_version":"2c"}
        """
        credentials = SystemConfig.get_config_attributes(
            "snmpdiscovery",
            ["ip_base", "ip_base_start", "ip_base_end", "timeout", "service", "community", "port", "version"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"snmp_ip_base": credentials[0][0], "snmp_ip_base_start": credentials[0][1],
                    "snmp_ip_base_end": credentials[0][2], "snmp_timeout": credentials[0][3],
                    "snmp_service_mng": credentials[0][4], "snmp_community": credentials[0][5],
                    "snmp_port": credentials[0][6], "snmp_version": credentials[0][7]}
        else:
            return {"snmp_ip_base": "192.168.0", "snmp_ip_base_start": "0", "snmp_ip_base_end": "50",
                    "snmp_timeout": "5", "snmp_service_mng": "2", "snmp_community": "public", "snmp_port": "22",
                    "snmp_version": "2c"}        # Default Configuration

    @staticmethod
    def get_upnp_details():
        """
        @author: Yogesh Kumar
        @since: 16-Nov-2011
        @version: 0.1
        @return: get default values of upnp discovery.
        @rtype: dictionary
        @note: This function gives you default values of upnp discovery.
        @summary: How To use:
        get_upnp_details()     return: {"upnp_timeout":"5","upnp_service_mng":"2"}
        """
        credentials = SystemConfig.get_config_attributes(
            "upnpdiscovery", ["timeout", "service"], False)
        if len(credentials) > 0 and len(credentials[0]) > 0:
            return {"upnp_timeout": credentials[0][0], "upnp_service_mng": credentials[0][1]}
        else:
            return {"upnp_timeout": "5", "upnp_service_mng": "2"}        # Default Configuration

    @staticmethod
    def get_pwd_expiry_details():
        """
        @author: Grijesh Chauhan
        @since: 04-April-2013
        @version: 0.1
        @return: get default values of password expiry.
        @rtype: tuple
        @note: This function gives you default values of password expiry.
        @summary: How To use:
        get_pwd_expiry_details()  returns (True, 45, 5, False)
        """
        enable, expiry_age, warning_time, auto_password = \
            SystemConfig.get_config_attributes("password_expiry",
                                               ["enable", "expiry_age", "warning_time", "auto_password"],
                                               False)[0]
        enable = str2bool(enable)
        expiry_age = int(expiry_age)
        warning_time = int(warning_time)
        auto_password = str2bool(auto_password)

        return enable, expiry_age, warning_time, auto_password


    @staticmethod
    def get_login_attempts_details():
        '''
        @author: Grijesh Chauhan
        @since: 04-April-2013
        @version: 0.1
        @return: get default values of password expiry.
        @rtype: tuple
        @note: This function gives you default values of password expiry.
        @summary: How To use:
        get_login_attempts_details()  returns (True, 5, 12, 60)

        NOTE: `lockout_durationl`: will be interpreted in HOURs 
        ----- `failure_expiration_interval`: will be interpreted in MINUTEs
        '''
        (
        enable, 
        max_login_attempts, 
        lockout_duration, 
        failure_expiration_interval,
        notify_user, # for email notification
        notify_admin
        ) = SystemConfig.get_config_attributes( "login_attempts", [
                "enable", 
                "max_login_attempts", 
                "lockout_duration", 
                "failure_expiration_interval",
                "notify_user",
                "notify_admin"], False)[0]

        enable = str2bool(enable)
        max_login_attempts = int(max_login_attempts)
        lockout_duration = int(lockout_duration)
        failure_expiration_interval = int(failure_expiration_interval)
        notify_user = str2bool(notify_user)
        notify_admin = str2bool(notify_admin)
        
        return  (
            enable, 
            max_login_attempts, 
            lockout_duration, 
            failure_expiration_interval,
            notify_user,
            notify_admin
        )

    @staticmethod
    def get_unmp_login_password_details():
        '''
        @author: Grijesh Chauhan
        @since: 11-April-2013
        @version: 0.1
        @return: get default values of UNMP system email.
        @rtype: tuple
        @note: This function gives UNMP email credentials those can we 
               useful in devlopment purpose..
        @summary: How To use:
        get_unmp_login_password_details()  returns ("do.not.reply.to.unmp@gmail.com", 
                                                    "nms@123@")
        '''        
        ( unmp_email,
          unmp_password 
        ) = SystemConfig.get_config_attributes( "unmp_mail", [
                "username",
                "password"
                ], False)[0]

        return ( 
            unmp_email,
            unmp_password 
        )