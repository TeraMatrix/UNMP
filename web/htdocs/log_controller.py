#!/usr/bin/python2.6

'''
@author: Mahipal Choudhary
@since: 07-Dec-2011
@version: 0.1
@note: All Controller functions Related with Vieweing logs.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


# Import modules that contain the function and libraries
from log_bll import Log_bll
from log import Log
from json import JSONEncoder
from common_bll import Essential

def main_log(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/log.js"]
    html.new_header("LOG DETAILS","main_log.py","",css_list,js_list)
    html.write(Log.create_log_form())
    html.new_footer()

def get_data(h):
	global html
	html=h
	l=Log_bll()
	sEcho=str(html.var("sEcho"))
	iColumns=html.var("iColumns",0)
	iDisplayLength=str(html.var("iDisplayLength",10))
	iDisplayStart=str(html.var("iDisplayStart",0))
	sColumns=str(html.var("sColumns"))	
	sEcho	=str(html.var("sEcho"))
	sSearch	=str(html.var("sSearch"))
	iSortCol_0      =html.var("iSortCol_0",-1)
	sSortDir_0      =html.var("sSortDir_0","asc")
	result= l.get_log_data_bll(sEcho,iColumns,iDisplayLength,iDisplayStart,sColumns,sSearch,iSortCol_0,sSortDir_0)
	html.write(JSONEncoder().encode(result))

def get_current_data(h):
    global html
    html=h
    l=Log_bll()
    result= l.get_header_data()
    #html.write(str(result))
    html_str=Log.make_header_log(result)
    html.write(html_str)
    
    
    
def get_alarm_current_data(h):
    global html
    html=h
    l=Log_bll()
    user_id=html.req.session["user_id"]
    el=Essential()
    hostgroup_id_list=el.get_hostgroup_ids(user_id)
    result= l.get_alarm_header_data(hostgroup_id_list)
    html_str=Log.make_alarm_header_log(result)
    html.write(html_str)
    
    
  

def view_page_tip_log_user(h):
    global html
    html = h
    html.write(Log.view_page_tip_log_user())                          
