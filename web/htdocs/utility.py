#!/usr/bin/python2.6

"""
@author: Yogesh Kumar
@since: 4-Oct-2011
@date: 4-Oct-2011
@version: 0.1
@note: This File Has Classes Validation: [to validate fileds], DeviceType: [to manage all devices], SystemSetting: [to manage settings of nms].
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""

# import all required modules
import re
import os
import time
import threading
import subprocess
import urllib2
import base64
# GET Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen
# for upnp discovery
from upnp_discovery import upnp_discover
# import inventory_bll
# from inventory_bll import DiscoveryBll


class Validation(object):
    """
    @author: Yogesh Kumar
    @since: 19-Oct-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to apply server side validation
    """

    @staticmethod
    def is_required(value):
        """

        @param value:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var value: value to check
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This Function validate the Required Filed.
        @summary: How To use:
                    is_required("value")                return: True
                    is_required(12)                     return: True
                    is_required(False)                  return: True
                    is_required(["a","b","c"])          return: True
                    is_required({"a":1,"b":2})          return: True
                    is_required(None)                   return: False
                    is_required("")                     return: False
        """
        try:
            if type(value) is int:          # check input value type is integer or not
                return True
            elif type(value) is dict:       # check input value type is dictionary or not
                if len(value) > 0:          # check dictionary length
                    return True
                else:
                    return False
            elif type(value) is list:       # check input value type is list or not
                if len(value) > 0:          # check list length
                    return True
                else:
                    return False
            elif type(value) is tuple:      # check input value type is tuple or not
                if len(value) > 0:          # check tuple length
                    return True
                else:
                    return False
            elif value != None and str(value).strip() != "":        # check input value not None and not an Empty String
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_number(number):
        """

        @param number:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var number: value to check {String(numeric value) or Integer or Float or Long}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: Validate Input Value is a Valid Number or Not (Empty String is Allow because this function doesn't check field is required).
        @summary: How To use:
                    is_number("12")                   return: True
                    is_number(12)                     return: True
                    is_number(0.12)                   return: True
                    is_number(1200000000000000000)    return: True
                    is_number(-12)                    return: True
                    is_number("-12")                  return: True
                    is_number("")                     return: True
                    is_number("string")               return: False
                    is_number(None)                   return: False
        """
        try:
            if str(number).strip() != "":                        # check input value is not an Empty String
                num = None
                if len(str(number).split(".")) > 0:
                    num = float(number)
                else:
                    num = int(number)
                    # convert input value into integer
                if type(num) is int or type(num) is long or type(
                        num) is float:       # check input value type is integer or long
                    return True
                else:
                    return False
            else:
                return True
        except Exception as e:
            return False

    @staticmethod
    def is_integer(number):
        """

        @param number:
        @author: Yogesh Kumar
        @since: 11-Jun-2012
        @version: 0.1
        @var number: value to check {String(numeric value only Integer or Long) or Integer or Long}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: Validate Input Value is a Valid Interger Number or Not (Empty String is Allow because this function doesn't check field is required).
        @summary: How To use:
                    is_integer("12")                   return: True
                    is_integer(12)                     return: True
                    is_integer(0.12)                   return: False
                    is_integer(1200000000000000000)    return: True
                    is_integer(-12)                    return: True
                    is_integer("-12")                  return: True
                    is_integer("")                     return: True
                    is_integer("string")               return: False
                    is_integer(None)                   return: False
        """
        try:
            if str(number).strip() != "":                        # check input value is not an Empty String
                num = None
                if str(number).find(".") >= 0:
                    return False
                else:
                    num = int(number)
                    # convert input value into integer
                if type(num) is int or type(num) is long:       # check input value type is integer or long
                    return True
                else:
                    return False
            else:
                return True
        except Exception as e:
            return False

    @staticmethod
    def is_string(value):
        """

        @param value:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var value: value to check { Only String}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function checks the input value is string or not.
        @summary: How To use:
                    is_string("12")                   return: True
                    is_string("CCPL")                 return: True
                    is_string("")                     return: True
                    is_string(None)                   return: False
                    is_string(12)                     return: False
                    is_string(object)                 return: False
        """
        try:
            if type(value) is str:            # check input value is String or not
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_positive_number(value):
        """

        @param value:
        @return:
        """
        try:
            if type(value) is str:
                if value != "":
                    pattern = re.compile(r"""^[0-9\n ]+$""")
                    # regular expression pattern for
                    # (Hexadecimal : A-F, a-f, 0-9 Ascii :
                    # A-Z, a-z, 0-9 Special : ! @ # are
                    # allowed
                    return pattern.match(value) is not None                    # Validate No Space
                else:
                    return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_hex_number(value):
        """

        @param value:
        @return:
        """
        try:
            if type(value) is str:
                if value != "":
                    pattern = re.compile(r"""^[a-z0-9A-Z\n ]+$""")
                    # regular expression pattern for
                    # (Hexadecimal : A-F, a-f, 0-9 Ascii :
                    # A-Z, a-z, 0-9 Special : ! @ # are
                    # allowed
                    return pattern.match(value) is not None                    # Validate No Space
                else:
                    return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_dictionary(value):
        """

        @param value:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var value: value to check {dictionary}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function checks the input value is a dictionary or not.
        @summary: How To use:
                    is_dictionary({})                 return: True
                    is_dictionary({"CCPL":1})         return: True
                    is_dictionary("")                 return: False
                    is_dictionary(None)               return: False
                    is_dictionary(12)                 return: False
                    is_dictionary(object)             return: False
        """
        try:
            if type(value) is dict:            # check input value is a Dictionary or not
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_list(value):
        """

        @param value:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var value: value to check {list}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function checks the input value is a list or not.
        @summary: How To use:
                    is_list([])                       return: True
                    is_list([1,2,3,4])                return: True
                    is_list("")                       return: False
                    is_list(None)                     return: False
                    is_list(12)                       return: False
                    is_list(object)                   return: False
        """
        try:
            if type(value) is list:            # check input value is a List or not
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_tuple(value):
        """

        @param value:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var value: value to check {tuple}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function checks the input value is a tuple or not.
        @summary: How To use:
                    is_tuple(())                      return: True
                    is_tuple((1,))                    return: True
                    is_tuple((1,2,3,4))               return: True
                    is_tuple("")                      return: False
                    is_tuple(None)                    return: False
                    is_tuple(12)                      return: False
                    is_tuple((12))                    return: False
                    is_tuple(object)                  return: False
        """
        try:
            if type(value) is tuple:            # check input value is a Tuple or not
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_boolean(value):
        """

        @param value:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var value: value to check {boolean}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function checks the input value is a tuple or not.
        @summary: How To use:
                    is_boolean(True)                  return: True
                    is_boolean(False)                 return: True
                    is_boolean(0)                     return: False
                    is_boolean(1)                     return: False
                    is_boolean("")                    return: False
                    is_boolean(None)                  return: False
                    is_boolean(12)                    return: False
                    is_boolean(object)                return: False
        """
        try:
            if type(value) is bool:            # check input value is a Boolean or not
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_valid_ipv4(ip):
        """

        @param ip:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var ip: ip to check {string}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function validate the ip address [IPv4].
        @summary: How To use:
                    is_valid_ipv4("192.168.1.1")      return: True
                    is_valid_ipv4("192.2.2")          return: False
                    is_valid_ipv4("192.42")           return: False
                    is_valid_ipv4(1)                  return: False
                    is_valid_ipv4("")                 return: False
                    is_valid_ipv4(None)               return: False
                    is_valid_ipv4(12)                 return: False
                    is_valid_ipv4(object)             return: False
        """
        try:
            ip = ip.strip()
            if ip != "":
                pattern = re.compile(
                    r"""^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$""")
                # regular expression pattern for IPv4 IP
                # Address validation
                return pattern.match(ip) is not None                    # Validate IPv4 IP Address
            else:
                return True
        except Exception as e:
            return False

    @staticmethod
    def is_valid_ipv6(ip):
        """

        @param ip:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var ip: ip to check {string}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function validate the ip address [IPv6].
        @summary: How To use:
                    is_valid_ipv6("3ffe:1900:4545:3:200:f8ff:fe21:67cf")      return: True
                    is_valid_ipv6("::0")                                      return: True
                    is_valid_ipv6("192.168.1.1")                              return: False
                    is_valid_ipv6("192.2.2")                                  return: False
                    is_valid_ipv6("192.42")                                   return: False
                    is_valid_ipv6(1)                                          return: False
                    is_valid_ipv6("")                                         return: False
                    is_valid_ipv6(None)                                       return: False
                    is_valid_ipv6(12)                                         return: False
                    is_valid_ipv6(object)                                     return: False
        """
        try:
            ip = ip.strip()
            if ip != "":
                pattern = re.compile(r"""
                                     ^
                                     \s*                         # Leading whitespace
                                     (?!.*::.*::)                # Only a single whildcard allowed
                                     (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
                                     (?:                         # Repeat 6 times:
                                     [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
                                     (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
                                     ){6}                        #
                                     (?:                         # Either
                                     [0-9a-f]{0,4}           #   Another group
                                     (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
                                     [0-9a-f]{0,4}           #   Last group
                                     (?: (?<=::)             #   Colon iff preceeded by exacly one colon
                                     |  (?<!:)              #
                                     |  (?<=:) (?<!::) :    #
                                     )                      # OR
                                     |                          #   A v4 address with NO leading zeros
                                     (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                                     (?: \.
                                     (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                                     ){3}
                                     )
                                     \s*                         # Trailing whitespace
                                     $
                                     """,
                                     re.VERBOSE | re.IGNORECASE | re.DOTALL)                        # regular expression pattern for IPv6 IP Address validation
                return pattern.match(ip) is not None                        # Validate IPv6 IP Address
            else:
                return True
        except Exception as e:
            return False

    @staticmethod
    def is_valid_ip(ip):
        """

        @param ip:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var ip: ip to check {string}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function validate the ip address [IPv6 and IPv4].
        @summary: How To use:
                    is_valid_ip("3ffe:1900:4545:3:200:f8ff:fe21:67cf")      return: True
                    is_valid_ip("::0")                                      return: True
                    is_valid_ip("192.168.1.1")                              return: True
                    is_valid_ip("192.2.2")                                  return: False
                    is_valid_ip("192.42")                                   return: False
                    is_valid_ip(1)                                          return: False
                    is_valid_ip("")                                         return: False
                    is_valid_ip(None)                                       return: False
                    is_valid_ip(12)                                         return: False
                    is_valid_ip(object)                                     return: False
        """
        return Validation.is_valid_ipv4(ip) or Validation.is_valid_ipv6(
            ip)   # call ip address [for IPv4 and IPv6] validation function which defined above.

    @staticmethod
    def is_valid_mac(mac):
        """

        @param mac:
        @author: Yogesh Kumar
        @since: 4-Oct-2011
        @version: 0.1
        @var mac: mac to check {string}
        @return: True/False [If validate/If not validate]
        @rtype: Boolean
        @note: This function validate the mac address.
        @summary: How To use:
                    is_valid_mac("11:22:33:44:55:66")     return: True
                    is_valid_mac("::0")                   return: False
                    is_valid_mac("192.168.1.1")           return: False
                    is_valid_mac("192.2.2")               return: False
                    is_valid_mac("192.42")                return: False
                    is_valid_mac(1)                       return: False
                    is_valid_mac("")                      return: False
                    is_valid_mac(None)                    return: False
                    is_valid_mac(12)                      return: False
                    is_valid_mac(object)                  return: False
        """
        try:
            mac = mac.strip()
            if mac != "":
            # pattern = re.compile(r"""^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$""")
            # # regular expression pattern for MAC Address validation
                pattern = re.compile(
                    r"""^([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}$|([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$|([0-9a-fA-F]{4}.){2}[0-9a-fA-F]{4}$""")  # updated by Rajendra Sharma
                return pattern.match(mac) is not None                                   # validate MAC Address
            else:
                return True
        except Exception as e:
            return False

    @staticmethod
    def is_valid_netmask(ip):
        """

        @param ip:
        @return:
        """
        try:
            return True
        except Exception as e:
            return False

    @staticmethod
    def no_space(value):
        """

        @param value:
        @return:
        """
        try:
            if type(value) is str:
                if value != "":
                    return value.find(" ") == -1                    # Validate No Space
                else:
                    return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_alpha(value):
        """

        @param value:
        @return:
        """
        try:
            if type(value) is str:
                if value != "":
                    pattern = re.compile(r"""^[a-zA-Z._\n ]+$""")
                    # regular expression pattern for space
                    # not allow
                    return pattern.match(value) is not None                    # Validate No Space
                else:
                    return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_alpha_numeric(value):
        """

        @param value:
        @return:
        """
        try:
            if type(value) is str:
                if value != "":
                    pattern = re.compile(r"""^[a-z0-9A-Z._\n ]+$""")
                    # regular expression pattern for space
                    # not allow
                    return pattern.match(value) is not None                    # Validate No Space
                else:
                    return True
            else:
                return False
        except Exception as e:
            return False


class ErrorMessages(object):
    """
    @author: Yogesh Kumar
    @since: 23-Oct-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to define Error Message
    """
    db_error = "dbError"
    validation_error = "validationError"
    sys_error = "sysError"
    unknown_error = "unknownError"
    duplicate_error = "duplicateError"
    duplicate_name_error = "duplicateNameError"
    duplicate_alias_error = "duplicateAliasError"
    no_record_error = "noRecordError"
    no_nms_instance_error = "noNmsInctanceError"
    nagios_config_error = "nagiosConfigError"
    change_ip_address_error = "changeIpAddressError"
    license_error = "licenseError"
    error_msg = None


class DiscoveryName(object):
    """
    @author: Yogesh Kumar
    @since: 16-Oct-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to define Discovery Name and Type
    """
    ping = "PING"
    snmp = "SNMP"
    upnp = "UPNP"
    tcp = "TCP"
    sdm = "SDM"


class HostState(object):
    """
    @author: Yogesh Kumar
    @since: 23-Oct-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to define States of Host
    """
    enable = "e"            # for Active Host
    disable = "d"            # for Disable Host


class UNMPDeviceType(object):
    """
    @author: Yogesh Kumar
    @since: 20-Oct-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to define device types
    """

    ap25 = "ap25"
    idu4 = "idu4"
    idu8 = "idu8"
    odu16 = "odu16"
    odu100 = "odu100"
    swt24 = "swt24"
    swt4 = "swt4"
    ccu = "ccu"
    generic = "unknown"


class SystemSetting(object):
    """
    @author: Yogesh Kumar
    @since: 20-Oct-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to define system settings and some of system operations & commands which are related with nagios and others.
    """

    @staticmethod
    def reload_nagios_config():
        """
        @author: Yogesh Kumar
        @since: 20-Oct-2011
        @version: 0.1
        @return: True/False {if Config Reload Successfully/Not Reload}
        @rtype: Boolean
        @note: This function reload the config file of nagios (this function works only for Linux Systems[red hat,ubuntu,cent os,other linux versions]).
        @summary: How To use:
                    reload_nagios_config()     return: True
                    reload_nagios_config()     return: False
        """
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        try:
            os.system('kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' %
                      nms_instance)      # execute os command which reloads nagios configuration
            time.sleep(3)
            return True
        except Exception, e:
            return e


class NagiosConfiguration(object):
    """
    @author: Yogesh Kumar
    @since: 12-Nov-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to create configuration of Nagios[host,hostgroup,service].
    """
    config_file = {
        "host": "hosts.cfg", "hostgroup": "hostgroups.cfg", "service": "services.cfg",
        "servicegroup": "servicegroups.cfg", "servicedependency": "servicedependency.cfg"}

    def hostgroup_config(self, hostgroup_name, hostgroup_alias):
        """

        @param hostgroup_name:
        @param hostgroup_alias:
        @return:
        """
        hostgroup_config_str = "" \
                               "\n\ndefine hostgroup {" \
                               "\n\thostgroup_name\t\t" + hostgroup_name + "" \
                                                                           "\n\talias\t\t\t" + hostgroup_name + "" \
                                                                                                                "\n}"
        return hostgroup_config_str

    def host_config(self, use_template, host_name, host_alias, ip_address, hostgroups, check_command, parents):
        """

        @param use_template:
        @param host_name:
        @param host_alias:
        @param ip_address:
        @param hostgroups:
        @param check_command:
        @param parents:
        @return:
        """
        host_config_str = "" \
                          "\n\ndefine host {" \
                          "\n\tuse\t\t\t" + use_template + "" \
                                                           "\n\thost_name\t\t" + host_name + "" \
                                                                                             "\n\talias\t\t\t" + host_alias + "" \
                                                                                                                              "\n\taddress\t\t" + ip_address + "" \
                                                                                                                                                               "" + (
                          hostgroups != None and ("\n\thostgroups\t\t" + hostgroups) or "") + "" \
                                                                                              "" + (
                          parents != None and ("\n\tparents\t\t" + parents) or "") + "" \
                                                                                     "" + (check_command != None and (
        "\n\tcheck_command\t\t" + check_command) or "\n\tcheck_command\t\techo \"No Check Command Applied\"") + "" \
                                                                                                                "\n}"
        return host_config_str

    def service_config(self, use_template, host_name, service_description, max_check_attempts, normal_check_interval,
                       retry_check_interval, check_command):
        """

        @param use_template:
        @param host_name:
        @param service_description:
        @param max_check_attempts:
        @param normal_check_interval:
        @param retry_check_interval:
        @param check_command:
        @return:
        """
        service_config_str = "" \
                             "\n\ndefine service {" \
                             "\n\tuse\t\t\t" + use_template + "" \
                                                              "\n\thost_name\t\t" + host_name + "" \
                                                                                                "\n\tservice_description\t\t\t" + service_description + "" \
                                                                                                                                                        "" + (
                             max_check_attempts != None and (
                             "\n\tmax_check_attempts\t\t" + max_check_attempts) or "") + "" \
                                                                                         "" + (
                             normal_check_interval != None and (
                             "\n\tnormal_check_interval\t\t" + normal_check_interval) or "") + "" \
                                                                                               "" + (
                             retry_check_interval != None and (
                             "\n\tretry_check_interval\t\t" + retry_check_interval) or "") + "" \
                                                                                             "" + (
                             check_command != None and (
                             "\n\tcheck_command\t\t" + check_command) or "\n\tcheck_command\t\techo \"No Check Command Applied\"") + "" \
                                                                                                                                     "\n}"
        return service_config_str

    def servicegroup_config(self, hostgroup_name, hostgroup_alias):
        """

        @param hostgroup_name:
        @param hostgroup_alias:
        @return:
        """
        servicegroup_config_str = "" \
                                  "\n\ndefine servicegroup {" \
                                  "\n\tservicegroup_name\t\t" + hostgroup_name + "" \
                                                                                 "\n\talias\t\t\t" + hostgroup_name + "" \
                                                                                                                      "\n}"
        return servicegroup_config_str

    def servicedependency_config(self, host_name, service_description, dependent_host_name,
                                 dependent_service_description):
        """

        @param host_name:
        @param service_description:
        @param dependent_host_name:
        @param dependent_service_description:
        @return:
        """
        execution_failure_criteria = "u,c"
        notification_failure_criteria = "w,u,c"
        servicedependency_config_str = "" \
                                       "\n\ndefine servicedependency{" \
                                       "\n\thost_name\t\t" + host_name + "" \
                                                                         "\n\tservice_description\t\t\t" + service_description + "" \
                                                                                                                                 "\n\tdependent_host_name\t\t" + dependent_host_name + "" \
                                                                                                                                                                                       "\n\tdependent_service_description\t\t" + dependent_service_description + "" \
                                                                                                                                                                                                                                                                 "\n\texecution_failure_criteria\t\t" + execution_failure_criteria + "" \
                                                                                                                                                                                                                                                                                                                                     "\n\tnotification_failure_criteria\t\t" + notification_failure_criteria + "" \
                                                                                                                                                                                                                                                                                                                                                                                                               "\n}"
        return servicedependency_config_str

    def write_host_config_file(self, nms_instance, file_content):
        """

        @param nms_instance:
        @param file_content:
        @return:
        """
        return self.write_config_file(nms_instance, self.config_file["host"], file_content)

    def write_hostgroup_config_file(self, nms_instance, file_content):
        """

        @param nms_instance:
        @param file_content:
        @return:
        """
        return self.write_config_file(nms_instance, self.config_file["hostgroup"], file_content)

    def write_service_config_file(self, nms_instance, file_content):
        """

        @param nms_instance:
        @param file_content:
        @return:
        """
        return self.write_config_file(nms_instance, self.config_file["service"], file_content)

    def write_servicegroup_config_file(self, nms_instance, file_content):
        """

        @param nms_instance:
        @param file_content:
        @return:
        """
        return self.write_config_file(nms_instance, self.config_file["servicegroup"], file_content)

    def write_servicedependency_config_file(self, nms_instance, file_content):
        """

        @param nms_instance:
        @param file_content:
        @return:
        """
        return self.write_config_file(nms_instance, self.config_file["servicedependency"], file_content)

    def write_config_file(self, nms_instance, file_name, file_content):
        """

        @param nms_instance:
        @param file_name:
        @param file_content:
        @return:
        """
        try:
            fw = open("/omd/sites/%s/etc/nagios/conf.d/%s" % (
                nms_instance, file_name), "w")
            fw.write(str(file_content))
            fw.close()
            return True
        except Exception, e:
            return e


class PingDiscovery(object):
    """
    Discover devices with PING
    """
    re_exp = re.compile(r"(\d) received")

    def ping_worker(self, dst_ip_str, discovery_id, DiscoveryBll_):
        """

        @param dst_ip_str:
        @param discovery_id:
        @param DiscoveryBll_:
        """
        obj_popen = subprocess.Popen(
            "ping -c2 " + dst_ip_str, shell=True, stdout=subprocess.PIPE)
        obj_popen.wait()
        bufData = obj_popen.stdout.read()
        if bufData != '':
            receive_value = int(re.findall(self.re_exp, bufData)[0])
            if receive_value == 2 or receive_value == 1:
                dic_bll = DiscoveryBll_()
                dic_bll.add_discovered_host(
                    discovery_id, dst_ip_str, dst_ip_str, UNMPDeviceType.generic, "")
        else:
            pass

    def check_ip(self, first, second):
        """

        @param first:
        @param second:
        @return:
        """
        for i in range(0, 4):
            if int(first[i]) <= int(second[i]):
                if int(first[i]) < int(second[i]):
                    return 1
            else:
                return 0
        return 1

    def ping_function(self, discovery_id, start_range, end_range, timeout, DiscoveryBll_):
        """

        @param discovery_id:
        @param start_range:
        @param end_range:
        @param timeout:
        @param DiscoveryBll_:
        """
        validate = 1
        first = start_range.split('.')
        second = end_range.split('.')
        if (len(first) == len(second) and len(first) == 4):
            for i in range(0, 4):
                if int(first[i]) <= int(second[i]):
                    if int(first[i]) < int(second[i]):
                        break
                else:
                    validate = 0
                    break
            if validate == 1:
                while self.check_ip(first, second) == 1:
                    if threading.active_count() > 60:
                        time.sleep(1)
                    if int(first[3]) != 255:
                        dst_ip_str = "%s.%s.%s.%s" % (
                            first[0], first[1], first[2], first[3])
                        t = threading.Thread(target=self.ping_worker, args=(
                            dst_ip_str, discovery_id, DiscoveryBll_,))
                        t.start()

                    first[3] = int(first[3]) + 1

                    if int(first[3]) > 255:
                        first[3] = 0
                        first[2] = int(first[2]) + 1
                        if int(first[2]) > 255:
                            first[2] = 0
                            first[1] = int(first[1]) + 1
                            if int(first[1]) > 255:
                                first[1] = 0
                                first[0] = int(first[0]) + 1
                                if int(first[0]) > 255:
                                    break
                time.sleep(15)
            else:
                pass  # return -1
        else:
            pass  # return -1


class SnmpDiscovery(object):
    """
    SNMP discovery
    """
    def snmp_ping_worker(self, ip_address_str, community, port, discovery_id, DiscoveryBll_):

        """

        @param ip_address_str:
        @param community:
        @param port:
        @param discovery_id:
        @param DiscoveryBll_:
        """
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
            # SNMP v1
            cmdgen.CommunityData('test-agent', community, 0),
            # SNMP v2
            # cmdgen.CommunityData('test-agent', community),
            # SNMP v3
            #    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
            cmdgen.UdpTransportTarget((ip_address_str, int(port))),
            # Plain OID
            (1, 3, 6, 1, 2, 1, 1, 1, 0),
        )
        if errorIndication:
            pass  # print errorIndication
        else:
            if errorStatus:
                pass
            else:
                dic_bll = DiscoveryBll_()
                dic_bll.add_discovered_host(discovery_id, ip_address_str,
                                            ip_address_str, UNMPDeviceType.generic, "")

    def check_ip(self, first, second):
        """

        @param first:
        @param second:
        @return:
        """
        for i in range(0, 4):
            if int(first[i]) <= int(second[i]):
                if int(first[i]) < int(second[i]):
                    return 1
            else:
                return 0
        return 1

    def snmp_function(self, discovery_id, start_range, end_range, timeout, community, port, version, DiscoveryBll_):
        """

        @param discovery_id:
        @param start_range:
        @param end_range:
        @param timeout:
        @param community:
        @param port:
        @param version:
        @param DiscoveryBll_:
        """
        validate = 1
        first = start_range.split('.')
        second = end_range.split('.')
        if (len(first) == len(second) and len(first) == 4):
            for i in range(0, 4):
                if int(first[i]) <= int(second[i]):
                    if int(first[i]) < int(second[i]):
                        break
                else:
                    validate = 0
                    break
            if validate == 1:
                while self.check_ip(first, second) == 1:
                    if threading.active_count() > 200:
                        time.sleep(1)
                    if int(first[3]) != 255:
                        dst_ip_str = "%s.%s.%s.%s" % (
                            first[0], first[1], first[2], first[3])
                        t = threading.Thread(target=self.snmp_ping_worker, args=(
                            dst_ip_str, community, port, discovery_id, DiscoveryBll_))
                        t.start()

                    first[3] = int(first[3]) + 1

                    if int(first[3]) > 255:
                        first[3] = 0
                        first[2] = int(first[2]) + 1
                        if int(first[2]) > 255:
                            first[2] = 0
                            first[1] = int(first[1]) + 1
                            if int(first[1]) > 255:
                                first[1] = 0
                                first[0] = int(first[0]) + 1
                                if int(first[0]) > 255:
                                    break
                time.sleep(15)
            else:
                pass  # return -1
        else:
            pass  # return -1


class UpnpDiscovery(object):
    """
    call UPNP discovery
    """
    def upnp_ping_worker(self, timeout):
        """

        @param timeout:
        @return:
        """
        upnp_dis_hosts = upnp_discover(3)  # better timeout is 5 or 10
        # output: {'172.22.0.10': ['Microsoft-Windows-NT/5.1'], '172.22.0.110':
        # ['Shyam/RU'], '172.22.0.1':
        # ['Linux/2.4.31-Amazon_SE-3.6.10.4.patch.3-R0416V36_BSP_SPI_FLASH_A4,'],
        # '172.22.0.101': ['Shyam/11nAP'], '172.22.0.17': ['Microsoft-Windows-
        # NT/5.1']}
        dis_hosts = []
        for udh in upnp_dis_hosts:
            dis_hosts.append(udh)
        return dis_hosts

    def upnp_function(self, discovery_id, timeout, DiscoveryBll_):
        """

        @param discovery_id:
        @param timeout:
        @param DiscoveryBll_:
        """
        dis_hosts = []
        dis_hosts = self.upnp_ping_worker(timeout)
        for dh_ip in dis_hosts:
            dic_bll = DiscoveryBll_()
            dic_bll.add_discovered_host(
                discovery_id, dh_ip, dh_ip, UNMPDeviceType.generic, "")
            # print 'ok %s = %s' % (ip_address_str, val.prettyPrint())
        time.sleep(10)


class DeviceUtility(object):
    """
    UNMP util file
    """
    def get_odu_node_type(self, ip_address_str, community='public', port_int=161, oid='1.3.6.1.4.1.26149.2.2.1.1.5.1'):
        """




        @param ip_address_str:
        @param community:
        @param port_int:
        @param oid:
        @requires: ip_address as String, Community as String, port as integer
        @return: 0,2 -> Master, 1,3 -> Slave, 4 -> SNMP_Response_timeout, 5 -> error_status_present_in_pysnmp_packet, 6 -> Function_Exception
        """
        try:
            make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('snmp-agent-100', community),
                cmdgen.UdpTransportTarget((ip_address_str, int(port_int))), make_tuple(oid), )

            if errorIndication:
                node_type = 4
            else:
                if errorStatus:
                    node_type = 5
                else:
                    val = varBinds[0][1]
                    node_type = int(val)

        except Exception as e:
            node_type = 6
        finally:
            return node_type

    def get_odu_ra_mac_cgi(self, url, username, password):
        """

        @param url:
        @param username:
        @param password:
        @return:
        """
        try:
            success = 1
            mac_str = ""
            err_str = ""
            if isinstance(url, str) and isinstance(username, str) and isinstance(password, str):
                req = urllib2.Request(url)
                auth_string = base64.encodestring(
                    "%s:%s" % (username, password))
                req.add_header("Authorization", "Basic %s" % auth_string)
                f = urllib2.urlopen(req)
                response = f.read()
                bx = response.find("Bridge MAC")
                response = response[:bx - 1]
                X = '([a-fA-F0-9]{2}[:|\-]?){6}'
                a = re.compile(X).search(response)
                if a:
                    success = 0
                    mac_str = response[a.start(): a.end()]
                else:
                    err_str = " mac not found "
            else:
                success = 1
                err_str = " arguments are not proper : (url , username, password) all arguments should be as String"

        except urllib2.URLError, e:
            success = 2
            err_str = " URL Error " + str(e)
        except Exception, e:
            success = 1
            err_str = "EXCEPTION : " + str(e)
        finally:
            response_dict = {}
            if success == 1:
                response_dict['success'] = success
                response_dict['result'] = err_str
            elif success == 0:
                response_dict['success'] = success
                response_dict['result'] = mac_str
            else:
                response_dict['success'] = success
                response_dict['result'] = err_str
            return response_dict

    def get_odu100_ra_mac(self, ip_address_str, community='public', port_int=161,
                          oid='1.3.6.1.4.1.26149.2.2.13.2.1.2.1'):
        """




        @param ip_address_str:
        @param community:
        @param port_int:
        @param oid:
        @requires: ip_address as String, Community as String, port as integer
        @return: {success:0,result:"result as str"} or {success:1,result:"exception"}
        """
        success = 1
        result = " Not found"
        try:
            make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('snmp-agent-100', community),
                cmdgen.UdpTransportTarget((ip_address_str, int(port_int))), make_tuple(oid), )

            if errorIndication:
                result = " No response recieved from device before snmp timeout"
            else:
                if errorStatus:
                    result = " Error Status found ", errorStatus
                else:
                    success = 0
                    val = varBinds[0][1]
                    result = str(val)

        except Exception as e:
            result = " Exception ", str(e)
        finally:
            result_dict = {}
            result_dict['success'] = success
            result_dict['result'] = result
            return result_dict

    def get_master_mac_from_slave(self, ip_address_str, community='public', port_int=161,
                                  oid='1.3.6.1.4.1.26149.2.2.13.9.2.1.5.1.1'):
        """




        @param ip_address_str:
        @param community:
        @param port_int:
        @param oid:
        @requires: ip_address as String, Community as String, port as integer
        @return: {success:0,result:"result as str"} or {success:1,result:"exception"}
        """
        success = 1
        result = " Not found"
        try:
            make_tuple = lambda x: tuple(int(i) for i in x.split('.'))

            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('snmp-agent-100', community),
                cmdgen.UdpTransportTarget((ip_address_str, int(port_int))), make_tuple(oid), )

            if errorIndication:
                result = " No response recieved from device before snmp timeout"
            else:
                if errorStatus:
                    result = " Error Status found ", errorStatus
                else:
                    success = 0
                    val = varBinds[0][1]
                    result = str(val)

        except Exception as e:
            result = " Exception ", str(e)
        finally:
            result_dict = {}
            result_dict['success'] = success
            result_dict['result'] = result
            return result_dict
