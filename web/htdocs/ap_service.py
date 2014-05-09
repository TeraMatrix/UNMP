#!/usr/bin/python2.6

#================================================================================================
#
# Author: Yogesh Kumar (ccpl)
#
# Purpose:
# Create and Delete Access point Graphs Services.
# 1) Access point Bandwidth
# 2) Access point Connected User
#
# functions:
# create_service_for_grapg()
# delete_service_for_graph()
#
# Requirement:
# Nagios
# Python 2.x or higher (with MySQLdb package)
# mySQL (with nms database schema and usefull tables)
#
# Output:
# edit serives.cfg file which is placed in conf.d folder
#
#=========================================================================


# import modules
from nms_config import *

# +---------------------------------------------------------------------------------------------+
# | Funtion to delete service for graphs                                                        |
# |                                                                                             |
# |  * host_name            : host name                                                         |
# |  * service_name         : service name                                                      |
# |                                                                                             |
# |  # return 0             : if service deleted successfully                                   |
# |  # return 1             : if service not deleted (function execution failed)                |
# |                                                                                             |
# +---------------------------------------------------------------------------------------------+


def delete_service_for_graph(host_name, service_name):
    site_name = __file__.split("/")[3]
    check_command = "%s!%s" % (service_name, site_name)
    service_file_path = "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % site_name
    temp_file_path = "/omd/sites/%s/tmp/temp.cfg" % site_name
    try:
        if (os.path.isfile(service_file_path)):
            startCheckLine = "#service-" + host_name + "-" + check_command
            endCheckLine = "#endservice-" + host_name + "-" + check_command
            checkfile = 0
            fr = open(service_file_path, "r")
            ftw = open(temp_file_path, "w")
            for line in fr:
                if (line.strip() != startCheckLine.strip() and checkfile == 0):
                    ftw.write(line)
                else:
                    checkfile = 1
            if (line.strip() == endCheckLine.strip() and checkfile == 1):
                checkfile = 0
            fr.close()
            ftw.close()
            ftr = open(temp_file_path, "r")
            fw = open(service_file_path, "w")
            for line in ftr:
                fw.write(line)
            ftr.close()
            fw.close()
            return 0
        else:
            return 1
    except:
        return 1

# +---------------------------------------------------------------------------------------------+
# | Funtion to create service for graphs                                                        |
# |                                                                                             |
# |  * host_name            : host name                                                         |
# |  * service_name         : service name                                                      |
# |                                                                                             |
# |  # return 0             : if service created successfully                                   |
# |  # return 1             : if service not created (function execution failed)                |
# |                                                                                             |
# +---------------------------------------------------------------------------------------------+


def create_service_for_graph(host_name, service_name):
    site_name = __file__.split("/")[3]
    refresh_time = get_refresh_time()
    check_command = "%s!%s" % (service_name, site_name)
    service_file_path = "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % site_name
    try:
        if (os.path.isfile(service_file_path)):
            fw = open(service_file_path, "a")
            fw.write("\n#service-" + host_name + "-" + check_command)
            fw.write("\ndefine service {")
            fw.write("\n\tuse\t\t\tgeneric-service")
            fw.write("\n\thost_name\t\t" + host_name)
            fw.write("\n\tservice_description\t\t\t" + service_name)
            fw.write("\n\tnormal_check_interval\t\t" + refresh_time)
            fw.write("\n\tcheck_command\t\t" + check_command)
            fw.write("\n}")
            fw.write("\n#endservice-" + host_name + "-" + check_command + "\n")
            fw.close()
            return 0
        else:
            return 1
    except:
        return 1
