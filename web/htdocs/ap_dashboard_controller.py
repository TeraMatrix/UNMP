#!/usr/bin/python2.6
# import the packeges
import config, htmllib,time, cgi,MySQLdb,sys
from common_controller import *
from nms_config import *
from odu_controller import *
from datetime import datetime
from datetime import timedelta
import time
from mysql_exception import mysql_connection
from unmp_dashboard_config import DashboardConfig
from utility import Validation
from operator import itemgetter
from ap_dashboard_view import APView
from ap_dashboard_bll import APDashboard
import json
from json import JSONEncoder 
from encodings import undefined


def ap_dashboard_profiling(h):
    global html
    html=h
    flag=0
    css_list = ["css/style.css","css/custom.css","calendrical/calendrical.css"]
    javascript_list = ["js/highcharts.js","js/apDashboard.js","calendrical/calendrical.js"]
    html.new_header("AP Dashboard","","",css_list,javascript_list)
    html.write('<div class=\"form-div\" >')
    host_id = ""
    host_id = html.var("host_id")
    extr_button={'tag':'button','id':'adSrhAP','value':'Advance Graph','name':'adSrhAP'}
    #this is used for storing DeviceTypeList e.g "odu16,odu100"
    device_type = ""
    #this is used for storing DeviceListState e.g "enabled"
    device_list_state = ""
    device_list_param=[]
    if html.var("device_type") != None: #we get the variable of page through html.var
        device_type = html.var("device_type")
    if html.var("device_list_state") != None:
        device_list_state = html.var("device_list_state")    
    if host_id == None:
        host_id = ""
    device_list_param = get_device_param(host_id)
    html.header("AP Monitoring")
    if device_list_param == [] or device_list_param == None:
    	flag=1
        output,mac_address=get_device_field(host_id)
        if  int(output)==1:
            html.write(page_header_search("","","Access Point",None,"enabled","device_type",extr_button))
            #html.write(page_header_search("","","UBR,UBRe",device_type,"enabled","device_type",extr_button))
        else:
                html.write(page_header_search(host_id,mac_address,"Access Point",device_type,"enabled","device_type",extr_button))
    else:
        html.write(page_header_search(device_list_param[0][0],device_list_param[0][1],"Access Point",device_list_param[0][2],device_list_state,"device_type",extr_button))
    if host_id == "" or host_id == "None":
        val = ""
        flag=1
        html.write("<div id=\"ap_show_msg\"></div><div id=\"tab_yo\">There is no profile selected</div>")
    else:
        flag=0
        html.write("<div id=\"ap_show_msg\"></div><div id=\"tab_yo\" style=\"display:block;overflow:hidden\">")
        ap_dashboard(h)
        html.write("</div>")
    html.write(str(APView.ap_footer_tab(flag)))
    html.new_footer()


def get_device_field(ip_address):
    try:
        mac_address=''
        db,cursor=mysql_connection() # create the connection
        if db ==1:
            raise SelfException(cursor)
        if Validation.is_valid_ip(ip_address):
            sel_query="select mac_address from hosts where ip_address='%s'"%(ip_address)
            cursor.execute(sel_query)
            mac_result=cursor.fetchall()
            if len(mac_result)>0:
                mac_address=mac_result[0][0]
        else:
            sel_query="select mac_address from hosts where host_id='%s'"%(ip_address)
            cursor.execute(sel_query)
            mac_result=cursor.fetchall()
            if len(mac_result)>0:
                mac_address=mac_result[0][0]
        return 0,mac_address
    except SelfException:
        return 1,str(e[-1])
        pass
    except Exception as e:
        return 1,str(e[-1])
    finally:
        if db.open:
            db.close()



# listing function
def get_device_list_ap(h):
    global html
    html = h
    #this is the result which we show on the page
    result =  ""
    ip_address=""
    mac_address=""
    selected_device = "ap25"
    #take value of IPaddress from the page through html.var
    #check that value is None Then It takes the empty string
    if html.var("ip_address") == None:
        ip_address = ""
    else:
        ip_address = html.var("ip_address")
        
    #take value of MACAddress from the page through html.var
    #check that value is None Then It takes the empty string
    if html.var("mac_address") == None:
        mac_address = ""
    else:
        mac_address = html.var("mac_address")
        
    #take value of SelectedDevice from the page through html.var
    #check that value is None Then It takes the empty string
    if html.var("selected_device_type") == None:
        selected_device  = "odu16"
    else:
        selected_device = html.var("selected_device_type")
        
    #call the function get_odu_list of odu-controller which return us the list of devices in two dimensional list according to IPAddress,MACaddress,SelectedDevice
    result = get_device_list_odu_profiling(ip_address,mac_address,selected_device)
    if result==0 or result==1 or result==2:
        html.write(str(result))
    else:
        db,cursor=mysql_connection('nms_sample')
        if db ==1:
            raise SelfException(cursor)
        sel_query="select ip_address from hosts where host_id='%s'"%(result)
        cursor.execute(sel_query)
        ip_address=cursor.fetchall()
        if len(ip_address)>0:
            html.write(str(ip_address[0][0]))
        else:
            html.write('0')

def ap_dashboard(h):
    global html
    h=html
    ap_bll_obj=APDashboard()
    ap_refresh_time,total_count=ap_bll_obj.get_dashboard_data()
    host_id = html.var("host_id")
    now=datetime.now()
    odu_end_date=now.strftime("%d/%m/%Y")
    odu_end_time=now.strftime("%H:%M")
    now=now+timedelta(minutes=-int(total_count))
    odu_start_date=now.strftime("%d/%m/%Y")
    odu_start_time=now.strftime("%H:%M")
    result=ap_bll_obj.ap_dashboard(host_id)
    if int(result['success'])==0:
        html.write(APView.ap_table(result['output'],odu_start_date,odu_start_time,odu_end_date,odu_end_time,str(ap_refresh_time),str(total_count)))
    else:
        if int(result['success'])==2:
            html.write('Mysql Services is not running mode so please contact your administrator.')
        else:
            html.write ('No data exists')


def ap_device_details(h):
    global html
    html=h
    ip_address=html.var("ip_address")
    ap_bll_obj=APDashboard()
    output=ap_bll_obj.ap_device_information(ip_address)
    view_output=''
    if len(output['result'])>0:
        view_output=APView.device_information_view(output['result'],ip_address,output['no_of_uesr'])
    else:
        view_output=APView.device_information_view_default(ip_address,output['no_of_uesr'])
    html.write(str({'device_table':view_output,'success':0}))




def ap_network_interface_graph(h):
    global html
    html=h
    odu_start_date=html.var('start_date')
    odu_start_time=html.var('start_time')
    odu_end_date=html.var('end_date')
    odu_end_time=html.var('end_time')
    interface_value=html.var('interface_value')
    ip_address=html.var("ip_address")
    limitFlag=html.var("limitFlag")
    ap_bll_obj=APDashboard()
    output_result=ap_bll_obj.ap_interface(odu_start_date,odu_start_time,odu_end_date,odu_end_time,interface_value,ip_address,limitFlag)
    html.write(str(output_result))

def page_tip_ap_monitor_dashboard(h):
        global html
        html = h
        html_view = ""\
        "<div id=\"help_container\">"\
        "<h1>Dashboard</h1>"\
        "<div>This <strong>Dashboard</strong> show all device silver statistics information by graph.</div>"\
        "<br/>"\
        "<div>On this page you can see network bandwidth graph etc.</div>"\
        "<br/>"\
	"<div><input class=\"yo-button yo-small\" type=\"button\" style=\"width: 30px;\" value=\"Advaced Graph\" name=\"odu_graph_show\"> This button open a window on self click event and show more information according to data and time.</div>"\
	"<div><input class=\"yo-button yo-small\" type=\"button\" style=\"width: 30px;\" value=\"Search\" name=\"odu_graph_show\"> Search the devices.</div>"\
	"<div><button id=\"odu_report_btn\" class=\"yo-button\" style=\"margin-top: 5px;\" type=\"submit\"><span class=\"save\">Report</span></button>Download the PDF report.</div>"\
	"<br/>"\
	"<div><button id=\"odu_report_btn\" class=\"yo-button\" style=\"margin-top: 5px;\" type=\"submit\"><span class=\"report\">Report</span></button>Download the Excel report.</div>"\
	"<br/>\
	<br/>\
        <div><strong>Note:</strong>This page show real time information of device and it page refresh on 5 min time interval.\
	Search button search device by MAC address and IP address and show information by graph.\
	Graph button display the graph according to time interval show,this time interval also change by user.\
	report button provide PDF of all display information by graph \
        </div>"\
        "</div>"
        html.write(str(html_view))


def ap_add_date_time_on_slide(h):
    global html
    html=h
    try:
        # calling the function
        ap_bll_obj=APDashboard()
        refresh_time,total_count=ap_bll_obj.get_dashboard_data()
        # start datetime and end datetime variable
        now=datetime.now()
        odu_end_date=now.strftime("%d/%m/%Y")
        odu_end_time=now.strftime("%H:%M")
        now=now+timedelta(minutes=-int(total_count))
        odu_start_date=now.strftime("%d/%m/%Y")
        odu_start_time=now.strftime("%H:%M")
        output_dict={'success':0,'end_date':odu_end_date,'end_time':odu_end_time,'start_date':odu_start_date,'start_time':odu_start_time}
        html.write(str(output_dict))
    except Exception as e:
        output_dict={'success':1,'output':str(e[-1])}
        html.write(str(output_dict))

def generic_json(h):
    global html
    html=h
    device_type=h.var('device_type_id')
    user_id=html.req.session["user_id"]    
    ap_bll_obj=APDashboard()
    result_dict=ap_bll_obj.all_graph_json('ap25',user_id)
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(result_dict)))
    
def common_graph_creation(h):
    global html
    html=h
    table_name=html.var('table_name')
    column_value=html.var('field')
    cal_type=html.var('calType')
    interface_value=html.var('tab')
    graph_type=html.var('type')
    start_date=html.var('start_date')
    start_time=html.var('start_time')
    end_date=html.var('end_date')
    end_time=html.var('end_time')
    flag=html.var('flag')
    ip_address=html.var('ip_address')
    update_field=html.var('update')
    start_date=datetime.strptime(start_date+' '+start_time,"%d/%m/%Y %H:%M")
    end_date=datetime.strptime(end_date+' '+end_time,"%d/%m/%Y %H:%M")
    column_name=column_value.split(",")
    table_name=table_name.split(",")
    user_id=html.req.session["user_id"]    
    if update_field=='' or update_field==None:
        update_field_name=''
    else:
        update_field_name=update_field
    ap_bll_obj=APDashboard()
    result_dict=ap_bll_obj.common_graph_json(user_id,table_name[0],table_name[1],flag,start_date,end_date,ip_address,graph_type,update_field_name,interface_value,cal_type,column_name)
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(result_dict)))
    
    
def ap_excel_report_genrating(h):
    global html
    html=h
    result1=''
    ip_address=html.var('ip_address')  # take ip_address from js side
    start_date=html.var('start_date')
    start_time=html.var('start_time')
    end_date=html.var('end_date')
    end_time=html.var('end_time')
    select_option=html.var('select_option')
    limitFlag=html.var("limitFlag")
    cal1=html.var('cal1')
    cal2=html.var('cal2')
    tab1=html.var('tab1')
    tab2=html.var('tab2')
    field1=html.var('field1')
    field2=html.var('field2')
    table_name1=html.var('table_name1')
    table_name2=html.var('table_name2')
    graph_name1=html.var('graph_name1')
    graph_name2=html.var('graph_name2')
    graph1=html.var('type1')
    graph2=html.var('type2')
    if int(select_option)>0:
        end_date=str(datetime.date(datetime.now())+timedelta(days=-1))
        start_time='00:00'
        end_time='23:59'
        if int(select_option)==1:
            start_date=str(datetime.date(datetime.now()))
        elif int(select_option)==2:
            start_date=str(datetime.date(datetime.now())+timedelta(days=-7))
        elif int(select_option)==3:
            start_date=str(datetime.date(datetime.now())+timedelta(days=-15))
        elif int(select_option)==4:
            start_date=str(datetime.date(datetime.now())+timedelta(days=-30))

        start_date=datetime.strptime(start_date+' '+start_time,"%Y-%m-%d %H:%M")
        end_date=datetime.strptime(end_date+' '+end_time,"%Y-%m-%d %H:%M")
    else:
        start_date=datetime.strptime(start_date+' '+start_time,"%d/%m/%Y %H:%M")
        end_date=datetime.strptime(end_date+' '+end_time,"%d/%m/%Y %H:%M")
    user_id=html.req.session["user_id"]    
    ap_bll_obj=APDashboard()
    result_dict=ap_bll_obj.ap_excel_report(user_id,ip_address,cal1,cal2,tab1,tab2,field1,field2,table_name1,table_name2,graph_name1,graph_name2,start_date,end_date,select_option,limitFlag,graph1,graph2)
    html.write(str(result_dict))
    
