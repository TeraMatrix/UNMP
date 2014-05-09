#!/usr/bin/python2.6
# Extract site from our own absolute filename :-)
# __file__ should be
# /omd/sites/###SITE###/share/check_mk/web/htdocs/defaults.py

site = __file__.split("/")[3]
execfile('/omd/sites/%s/etc/check_mk/defaults' % site)

# site starting from a local path instead of global path
# local path is defined by the */local/share/*
# golbal path is defined by the */share/*
startaslocal = True
# if the startaslocal is true UNMP will be loaded from the
#   */local/share/* path

#dictionary to maintain the configuration file paths
confpaths = {
    "isfolder": "",
    "config": "config.xml",
    "shyam" : "shyamdevices.xml",
    "svc" : "service.xml",
    "service" : "service_template.xml",
    "dashboard_config": "dashboard_config.xml",
    "configurationTemplate": "configurationTemplate.xml",
    "configurationTemplateDefault" : "configurationTemplateDefault.xml",
    "license": "license",
    "mysql_backup": "mysql_backup.sh",
    "mysql_restore": "mysql_restore.sh",
    "backup_log": "backup_log.log",
    "ping" : "pingDiscovery.xml",
    "snmp" : "snmpDiscovery.xml",
    "upnp" : "upnpDiscovery.xml",
    "sdmc" : "sdmcDiscovery.xml",
    "nmsScheduling" : "nmsScheduling.xml"
             }

configpath = "/omd/sites/" + site

if (startaslocal):
    configpath = configpath + "/local/"

configpath = configpath + "/share/check_mk/web/htdocs/"

def get_config_path(configname = "isfolder", folder = "xml"):
    configxml = configpath + folder + "/" + confpaths[configname]
    return str(configxml)

