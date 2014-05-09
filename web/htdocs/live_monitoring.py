#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@version: 0.1
@note: All Views Related with Inventory. 
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

class LiveMonitoring(object):
    @staticmethod
    def header_buttons():
        add_btn = "<div class=\"header-icon\"><img onclick=\"addHost();\" class=\"n-tip-image\" src=\"images/new_icons/round_plus.png\" id=\"add_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Host\"></div>"
        header_btn = ""
        return header_btn
    
    @staticmethod
    def live_monitring(host_id):
        return "<input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"><div id=\"host_details\"></div><div id=\"live_monitoring\"></div>" % host_id
