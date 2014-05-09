#!/usr/bin/python2.6

'''
@author: Rajendra Sharma
@since: 12-Nov-2011
@date: 12-Nov-2011
@version: 0.1
@note: There is one Class that use to load Dashboard Configuration.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Rajendra Sharma for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# import packages
import MySQLdb
import xml.dom.minidom
import sys
import os


class DashboardConfig(object):
    '''
    @author: Rajendra Sharma
    @since: 12-Nov-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to fetch the data of configuration from xml file.
    '''

    @staticmethod
    def load_config_file():
        '''
        @author: Rajendra Sharma
        @since: 12-Nov-2011
        @version: 0.1
        @return: xml dom object
        @rtype: xml.dom.minidom
        @note: This function load the xml file and return xml dom object.
        @summary: How To use:
                    load_config_file()     return: [dom object]
                    load_config_file()     return: Exception object or None
        '''
        nms_instance = __file__.split(
            "/")[3]                           # it gives instance name of nagios system
        xml_config_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/dashboard_config.xml" % nms_instance                        # config.xml file path
        try:
            if (os.path.isfile(xml_config_file)):                        # check config.xml file exist or not
                dom = xml.dom.minidom.parse(
                    xml_config_file)            # create xml dom object of config.xml file
                return dom
            else:
                print xml_config_file
                return None
        except Exception, e:
            return None

    @staticmethod
    def get_config_attributes(tag_name, attribute_name, get_text=False):
        '''
        @author: Rajendra Sharma
        @since: 12-Nov-2011
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
        '''
        dom = DashboardConfig.load_config_file(
        )                        # create xml dom of config file
        dom_element = dom.getElementsByTagName(
            tag_name)            # get the element by tag name
        attribute_value = []
        # declare attribute value list    (2D)
        text_value = []
        # declare text value list        (1D)
        for elem in dom_element:                                    # iterate selected elements
            attr_value = []
            # declare attr_value list        (2D)
            for attr in attribute_name:                                # iterate attributes
                attr_value.append(elem.getAttribute(
                    attr))            # append attribute_value in attr_value
            attribute_value.append(attr_value)
            # append attr_value in attribute_value
            if get_text == True:
                text_value.append(DashboardConfig.get_tag_text(
                    elem.childNodes))    # append text value in text_value if get_text is True
        if get_text == True:
            return attribute_value, text_value
        else:
            return attribute_value
