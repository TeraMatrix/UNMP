#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@version: 0.1
@note: All Controller functions Related with Inventory. 
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


# Import modules that contain the function and libraries
from inventory_bll import HostgroupBll,VendorBll,BlackListMacBll,HostBll,DiscoveryBll,ServiceBll,NagioConfigurationBll,SystemSetting,all_firmware_detail

from inventory import Host
from inventory import Hostgroup
from inventory import Discovery
from inventory import Service
from inventory import NetworkMap
from inventory import Vendor
from inventory import BlackListMac

from utility import ErrorMessages,DeviceUtility,Validation,UNMPDeviceType
from datetime import datetime
from common import Common
from common_bll import Essential
from json import JSONEncoder
from license_bll import LicenseBll
from pysnmp_ap import pysnmp_get_table,pysnmp_get_node,pysnmp_get
from pysnmp_v1 import pysnmp_get_table as pysnmp_get_table_ccu
from py_module import pysnmp_geter
#
def server_time(h):
    global html
    html = h
    a = datetime.now()
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode({"date_time_server":[a.year,a.month,a.day,a.hour,a.minute,a.second]}))
#    html.write(JSONEncoder().encode([a.year,a.month,a.day,a.hour,a.minute,a.second]))

# Host
def manage_host(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/inventory_host.js"]
    header_btn = Host.header_buttons()
    html.new_header("Hosts","manage_host.py",header_btn,css_list,js_list)
    html.write(Host.manage_host())
    html.new_footer()

def grid_view_active_host(h):
    global html
    html = h
    i_display_start=str(html.var("iDisplayStart"))
    i_display_length=str(html.var("iDisplayLength"))
    s_search=str(html.var("sSearch"))
    sEcho=str(html.var("sEcho"))
    s_search=str(html.var("sSearch"))
    sSortDir_0=str(html.var("sSortDir_0"))
    iSortCol_0=str(html.var("iSortCol_0"))
    try:
        user_id =  html.req.session['user_id']  
        hst_bll = HostBll(user_id)                             # creating the HostBll object
        all_hosts_dict = hst_bll.grid_view_active_host(i_display_start,i_display_length,s_search,sEcho,sSortDir_0,iSortCol_0,html.req.vars)     # fetching all hosts data from database
        #html.write(str(all_hosts_dict))
        hosts_list = []                                 # creating empty list [we will use this in datatables]
        s_no = 0
        all_hosts=all_hosts_dict["aaData"]
        for hst in all_hosts:
            s_no += 1
            host_parent=hst[9]
            flag_parent=True
            if str(hst.is_localhost)=="1":
                host_parent="-"
                flag_parent=False
                for i in range(len(hst)):
                    if str(hst[i]).find(s_search)!=-1 and i!=9:
                        flag_parent=True
                        break
            if flag_parent:
                hosts_list.append([str(hst.host_id),\
                                   hst.is_localhost,\
                                   hst[3] != None and hst[3] or "-",\
                                   hst.ip_address != None and hst.ip_address or "-",\
                                   hst.device_name != None and hst.device_name or "-",\
                                   hst.hostgroup_name != None and hst.hostgroup_name or "-",\
                                   hst.mac_address != None and hst.mac_address or "-",\
                                   host_parent != None and host_parent or "-",\
                                   hst.priority_name != None and hst.priority_name or "-",\
                                   "<a href=\"device_details_example.py?host_id=%s\"><img class='host_opr' title='View Host Details' src='images/new/info.png' alt='view' style=\"width:16px;height:16px;\"/></a>&nbsp; <a href=\"javascript:editHost(%s,%s);\"><img class='host_opr' title='Edit Host Details' src='images/new/edit.png' alt='edit'/></a>" % (hst.host_id,hst.host_id,hst.is_localhost) ])       # creating 2D List of host details
    #    html.write(str(hosts_list))
        all_hosts_dict["aaData"]=hosts_list
        html.write(JSONEncoder().encode(all_hosts_dict))
        #html.write(str(all_hosts_dict))
    except Exception,e:
        output = {
            "sEcho": 0,
            "iTotalRecords":0,
            "iTotalDisplayRecords": 0,
            "aaData":[],
            "query":str(e),
            "dsd":all_hosts_dict
        }
        html.write(str(output))
        #html.write(JSONEncoder().encode(output))




def grid_view_disable_host(h):
    global html
    html = h
    i_display_start=str(html.var("iDisplayStart"))
    i_display_length=str(html.var("iDisplayLength"))
    s_search=str(html.var("sSearch"))
    sEcho=str(html.var("sEcho"))
    s_search=str(html.var("sSearch"))
    sSortDir_0=str(html.var("sSortDir_0"))
    iSortCol_0=str(html.var("iSortCol_0"))
    try:
        user_id =  html.req.session['user_id']  
        hst_bll = HostBll(user_id)                             # creating the HostBll object
        all_hosts_dict = hst_bll.grid_view_disable_host(i_display_start,i_display_length,s_search,sEcho,sSortDir_0,iSortCol_0,html.req.vars)     # fetching all hosts data from database
        hosts_list = []                                 # creating empty list [we will use this in datatables]
        s_no = 0
        all_hosts=all_hosts_dict["aaData"]
        for hst in all_hosts:
            s_no += 1
            hosts_list.append([str(hst.host_id),\
                               hst.is_localhost,\
                               hst[3] != None and hst[3] or "-",\
                               hst.ip_address != None and hst.ip_address or "-",\
                               hst.device_name != None and hst.device_name or "-",\
                               hst.hostgroup_name != None and hst.hostgroup_name or "-",\
                               hst.mac_address != None and hst.mac_address or "-",\
                               hst[9] != None and hst[9] or "-",\
                               hst.priority_name != None and hst.priority_name or "-",\
                               "<a href=\"device_details_example.py?host_id=%s\"><img class='host_opr' title='View Host Details' src='images/new/info.png' alt='view'/></a>&nbsp; <a href=\"javascript:editHost(%s,%s);\"><img class='host_opr' title='Edit Host Details' src='images/new/edit.png' alt='edit'/></a>" % (hst.host_id,hst.host_id,hst.is_localhost) ])       # creating 2D List of host details
        all_hosts_dict["aaData"]=hosts_list
        html.req.content_type = 'application/json'
        html.write(JSONEncoder().encode(all_hosts_dict))
    except Exception,e:	    
        output = {
            "sEcho": 0,
            "iTotalRecords":0,
            "iTotalDisplayRecords": 0,
            "aaData":[]
        }
        html.req.content_type = 'application/json'
        html.write(JSONEncoder().encode(output))


def grid_view_deleted_host(h):
    global html
    html = h
    user_id =  html.req.session['user_id']
    i_display_start=str(html.var("iDisplayStart"))
    i_display_length=str(html.var("iDisplayLength"))
    s_search=str(html.var("sSearch"))
    sEcho=str(html.var("sEcho"))
    s_search=str(html.var("sSearch"))
    sSortDir_0=str(html.var("sSortDir_0"))
    iSortCol_0=str(html.var("iSortCol_0"))
    try:  
        hst_bll = HostBll(user_id)                             # creating the HostBll object
        all_hosts_dict = hst_bll.grid_view_deleted_host(i_display_start,i_display_length,s_search,sEcho,sSortDir_0,iSortCol_0,html.req.vars)     # fetching all hosts data from database
        hosts_list = []                                 # creating empty list [we will use this in datatables]
        s_no = 0
        all_hosts=all_hosts_dict["aaData"]
        for hst in all_hosts:
            s_no += 1
            hosts_list.append([str(hst.host_id),\
                               hst.is_localhost,\
                               hst[1] != None and hst[1] or "-",\
                               hst.ip_address != None and hst.ip_address or "-",\
                               hst.device_name != None and hst.device_name or "-",\
                               hst.hostgroup_name != None and hst.hostgroup_name or "-",\
                               hst.mac_address != None and hst.mac_address or "-",\
                               hst[11] != None and hst[11] or "-",\
                               hst.priority_name != None and hst.priority_name or "-",\
                               hst.updated_by != None and hst.updated_by or "-",\
                               hst.timestamp != None and hst.timestamp.strftime("%d-%m-%Y %H:%M") or "-"])       # creating 2D List of host details
    #    html.write(str(hosts_list))
        all_hosts_dict["aaData"]=hosts_list
        html.write(JSONEncoder().encode(all_hosts_dict))
        JSONEncoder().encode(all_hosts_dict)
    except Exception,e:	    
        output = {
            "sEcho": 0,
            "iTotalRecords":0,
            "iTotalDisplayRecords": 0,
            "aaData":[],
            "query":str(e),
            "dsd":all_hosts_dict
        }
        #html.write(JSONEncoder().encode(output))
        html.write(str(output))



def grid_view_discovered_host(h):
    global html
    html = h
    i_display_start=str(html.var("iDisplayStart"))
    i_display_length=str(html.var("iDisplayLength"))
    s_search=str(html.var("sSearch"))
    sEcho=str(html.var("sEcho"))
    s_search=str(html.var("sSearch"))
    sSortDir_0=str(html.var("sSortDir_0"))
    iSortCol_0=str(html.var("iSortCol_0"))
    hst_bll = HostBll()                             # creating the HostBll object
    try:
        all_hosts_dict = hst_bll.grid_view_tcp_discovered_host(0,30000,s_search,sEcho,sSortDir_0,iSortCol_0,html.req.vars)     # fetching all hosts data from database
        hosts_list = []                                 # creating empty list [we will use this in datatables]
        temp_res=[]
        s_no = 0
        temp_list = []
        il=0
        fl=0
        all_hosts=all_hosts_dict["aaData"]
        di_product_id={6021:"RM/RM18 Master",
        6023:"RM/RM18 Master",
        6040:"CCU",
        6024:"RM/RM18 Slave",
        6022:"RM/RM18 Slave"}
        if all_hosts!=[]:
            for hst in all_hosts:
                if hst.ip_address in temp_list:
                    pass
                else:
                    s_no += 1
                    
                    hosts_list.append([str(hst.ne_id),\
                                       "TCP",\
                                       hst.ip_address != None and hst.ip_address or "",\
                                       hst.site_mac != None and hst.site_mac or "",\
                                       di_product_id.get(hst.product_id,"Unknown"),\
                                       hst.timestamp != "None" and hst.timestamp.strftime("%d-%m-%Y %H:%M") or ""])       # creating 2D List of host details
                    temp_list.append(hst.ip_address)
        all_hosts_dict2 = hst_bll.grid_view_discovered_host(0,30000,s_search,sEcho,sSortDir_0,iSortCol_0,html.req.vars)    
        temp_res=hosts_list
        all_hosts=all_hosts_dict2["aaData"]
        hosts_list=[]
        if all_hosts!=[]:
            for hst in all_hosts:
                if hst.ip_address in temp_list:
                    pass
                else:
                    s_no += 1
                    hosts_list.append([str(hst.discovered_host_id),\
                                       hst.discovery_type_id,\
                                       hst.ip_address != None and hst.ip_address or "",\
                                       hst.mac_address != None and hst.mac_address or "",\
                                       " - ",\
                                       hst.timestamp != None and hst.timestamp.strftime("%d-%m-%Y %H:%M") or ""])       # creating 2D List of host details
                    temp_list.append(hst.ip_address)
        temp_res+=hosts_list
        if(str(sSortDir_0)=="asc"):
            var = False
            temp_res=sorted(temp_res, key=lambda temp_res: temp_res[int(iSortCol_0)],reverse=False)
        else:
            var=True
            temp_res=sorted(temp_res, key=lambda temp_res: temp_res[int(iSortCol_0)],reverse=True)				     
        all_hosts_dict["aaData"]=temp_res[int(i_display_start):int(i_display_start)+int(i_display_length)]
        all_hosts_dict["iTotalRecords"]=len(temp_res)
        all_hosts_dict["iTotalDisplayRecords"]=len(temp_res)
        all_hosts_dict["value"]=iSortCol_0
        all_hosts_dict["var"]=var
        html.req.content_type = 'application/json'
        html.write(JSONEncoder().encode(all_hosts_dict))
    except Exception,e:	    
        output = {
            "sEcho": 0,
            "iTotalRecords":0,
            "iTotalDisplayRecords": 0,
            "aaData":[]
        }
        html.req.content_type = 'application/json'
        html.write(JSONEncoder().encode(output))


def get_mac_details(h):
	global html
	html = h
	ip_address = html.var("ip_address")
	if ip_address is not None:
		community = html.var("community") != None and html.var("community") or "public"
		port = html.var("port") != None and html.var("port") or 161
		port = Validation.is_number(port) and int(port) or 161
		device_type = html.var("device_type")
		#oid = "1.3.6.1.4.1.26149.10.4.1.3"
	
		#oid_dic={'mac_address':'1.3.6.1.4.1.26149.10.4.1.3.0','radio_mac_address':'1.3.6.1.4.1.26149.10.4.1.4.0'}
		oid_dic={'mac_address':'1.3.6.1.4.1.26149.10.4.1.3.0'}
		result=pysnmp_geter(oid_dic,ip_address,port,community)
		#result={"success":1,"result":"Devcie not provide the MAC Adress."}
		#html.req.content_type = 'application/json'
		#html.write(str(get_result))
		#html.write(JSONEncoder().encode(result))
		if result["success"]==0:
			pass
		else:
			result = {"success":1,"result":result['result'].values()[0]}
	else:
		result={"success":1,"result":"IP address not found"}
		
	html.req.content_type = 'application/json'
	html.write(JSONEncoder().encode(result))

def get_firmware_details(h):
    global html
    html = h
    ip_address = html.var("ip_address")
    if ip_address is not None:
        community = html.var("community") != None and html.var("community") or "public"
        port = html.var("port") != None and html.var("port") or 161
        port = Validation.is_number(port) and int(port) or 161
        device_type = html.var("device_type")
        oid_dic={'firmware_version':'1.3.6.1.4.1.26149.2.2.6.1.2.1'}
        pysnmp_result=pysnmp_geter(oid_dic,ip_address,port,community)
        if pysnmp_result["success"]==0:
            firmware_version = pysnmp_result['result'].values()[0]
            result = {"success":0,"result":firmware_version.split('_')[0]}
        else:
            result = {"success":1,"result":pysnmp_result['result'].values()[0]}
    else:
        result={"success":1,"result":"Firmware version not found"}
        
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))

def get_all_device_firmware_details(h):
    global html
    html = h
    result = all_firmware_detail()
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))




def odu_master_list(h):
    global html
    html = h
    device_type_id = html.var("device_type_id")
    hst_bll = HostBll()                             # creating the HostBll object
    master_list = hst_bll.odu_master(device_type_id)

    # get dns state select list
    value = []
    name = []


    if isinstance(master_list, Exception):
        pass
    else:
        for ml in master_list:
            if ml.host_id not in value:
                value.append(ml.host_id)
                name.append("%s (%s)" % (ml.mac_address,ml.ip_address))

    selected = ""
    list_id = "master_mac"
    list_name = "master_mac"
    title = "Choose or Fetch Root Node MAC Address"
    message = "-- Select Root Node --"
    master_list_select_list = Common.make_select_list(value, name, selected, list_id, list_name,title,message)
    html.write(master_list_select_list)

def form_host(h):
    global html
    html = h
    # get snmp version list
    value = ["1","2c","3"]
    name = ["v1","v2c","v3"]
    selected = "2c"
    list_id = "snmp_version"
    list_name = "snmp_version"
    title = "Choose SNMP Version"
    snmp_version_select_list = Common.make_select_list(value, name, selected, list_id, list_name,title)

    # get dns state select list
    value = ["Disable","Enable"]
    name = ["Disable","Enable"]
    selected = "Disable"
    list_id = "dns_state"
    list_name = "dns_state"
    title = "Choose DNS State"
    dns_state_select_list = Common.make_select_list(value, name, selected, list_id, list_name,title)


    hst_bll = HostBll()                             # creating the HostBll object

    # get host parent select list
    if html.req.session['group'].lower() == 'SuperAdmin'.lower():
        parents = hst_bll.host_parents()
    else:
        userid = html.req.session['user_id']
        parents = hst_bll.host_parents2(userid)
    parents_id = []
    parents_name = []

    selected = None
    list_id = "host_parent"
    list_name = "host_parent"
    title = "Choose Host Parent"

    #for pr in parents:
    #    parents_id.append(pr.host_id)
    #    parents_name.append(pr.host_name)

    for pr in parents:
        parents_id.append(pr[0])
        parents_name.append(pr[3])  

    host_parent_select_list =  Common.make_select_list(parents_id, parents_name, selected, list_id, list_name,title)

    # get host hostgroup select list
    if html.req.session['group'].lower() == 'SuperAdmin'.lower():
        hostgroups = hst_bll.host_hostgroups()
    else:
        userid = html.req.session['user_id']
        hostgroups = hst_bll.host_hostgroups2(userid)

    hostgroups_id = []
    hostgroups_name = []

    selected = None
    list_id = "hostgroup"
    list_name = "hostgroup"
    title = "Choose Hostgroup"

    for pr in hostgroups:
        hostgroups_id.append(pr.hostgroup_id)
        hostgroups_name.append(pr.hostgroup_alias)

    host_hostgroups_select_list =  Common.make_select_list(hostgroups_id, hostgroups_name, selected, list_id, list_name,title)


    # get host vendors select list
    vendors = hst_bll.host_vendors()
    vendors_id = []
    vendors_name = []

    selected = None
    list_id = "host_vendor"
    list_name = "host_vendor"
    title = "Choose Vendor Name"
    message = "-- Select Vendor --"
    for vd in vendors:
        vendors_id.append(vd.host_vendor_id)
        vendors_name.append(vd.vendor_name)

    host_vendor_select_list =  Common.make_select_list(vendors_id, vendors_name, selected, list_id, list_name,title,message)

    # get host OS select list
    os = hst_bll.host_os()
    os_id = []
    os_name = []

    selected = None
    list_id = "host_os"
    list_name = "host_os"
    title = "Choose Host OS Name"
    message = "-- Select OS --"
    for s in os:
        os_id.append(s.host_os_id)
        os_name.append(s.os_name)

    host_os_select_list =  Common.make_select_list(os_id, os_name, selected, list_id, list_name,title,message)

    # get host priority select list
    priority = hst_bll.host_priority()
    priority_id = []
    priority_name = []

    selected = None
    list_id = "host_priority"
    list_name = "host_priority"
    title = "Choose Host Priority"
    message = "-- Select Priority --"
    for pr in priority:
        priority_id.append(pr.priority_id)
        priority_name.append(pr.priority_name)

    host_priority_select_list =  Common.make_select_list(priority_id, priority_name, selected, list_id, list_name,title,message)

    # get host state select list
    state = hst_bll.host_state()
    state_id = []
    state_name = []

    selected = None
    list_id = "host_state"
    list_name = "host_state"
    title = "Choose Host State"
    message = "-- Select State --"
    for st in state:
        state_id.append(st.host_state_id)
        state_name.append(st.state_name)

    host_state_select_list =  Common.make_select_list(state_id, state_name, selected, list_id, list_name,title,message)

    # get device_type_select_list
    device = hst_bll.device_type()
    device_id = []
    device_name = []

    selected = None
    list_id = "device_type"
    list_name = "device_type"
    title = "Choose Device Type"
    message = "-- Select Device Type --"
    for dv in device:
        device_id.append(dv.device_type_id)
        device_name.append(dv.device_name)

    device_type_select_list =  Common.make_select_list(device_id, device_name, selected, list_id, list_name,title,message)

    master_value = []
    master_name = []
    selected = ""
    list_id = "master_mac"
    list_name = "master_mac"
    title = "Choose Root Node"
    message = "-- Select Root Node --"
    master_list_select_list = Common.make_select_list(master_value, master_name, selected, list_id, list_name, title, message)

    #Host.create_form(device_type_select_list,host_state_select_list,host_priority_select_list,host_vendor_select_list,host_parent_select_list,dns_state_select_list,snmp_version_select_list)
    html.write(Host.create_form(device_type_select_list,host_state_select_list,host_priority_select_list,host_vendor_select_list,host_os_select_list,host_parent_select_list,dns_state_select_list,snmp_version_select_list,host_hostgroups_select_list,master_list_select_list))

def host_parents(h):
    global html
    html  = h
    hst_bll = HostBll()                             # creating the HostBll object
    # get host parent select list
    parents = hst_bll.host_parents()
    parents_id = []
    parents_name = []

    selected = None
    list_id = "host_parent"
    list_name = "host_parent"
    title = "Choose Host Parent"

    for pr in parents:
        parents_id.append(pr.host_id)
        parents_name.append(pr.host_alias)

    host_parent_select_list =  Common.make_select_list(parents_id, parents_name, selected, list_id, list_name,title)
    html.write(host_parent_select_list)

def get_odu_ra_mac_and_node_type(h):
    global html
    html = h
    out = {"node_type_success":1,"ra_mac_success":1,"node_type":"SNMP agent gone away or device Unreachable","ra_mac":"SNMP agent gone away or device Unreachable"}  
    ip_address = html.var("ip_address")
    device_type = html.var("device_type")
    username = html.var("username")
    password = html.var("password")
    community = html.var("community") != None and html.var("community") or "public"
    port = html.var("port") != None and html.var("port") or 161
    port = Validation.is_number(port) and port or 161

    du = DeviceUtility()
    node_type = du.get_odu_node_type(ip_address.split(":")[0],community,port)   # @return: 0,2 -> Master, 1,3 -> Slave, 4 -> SNMP_Response_timeout, 5 -> error_status_present_in_pysnmp_packet, 6 -> Function_Exception
    ra_mac = None
    if device_type == UNMPDeviceType.odu16:
        ra_mac = du.get_odu_ra_mac_cgi("http://" + ip_address,username,password)         # #{'result': '00:80:48:71:85:B9', 'success': 0}
    elif device_type == UNMPDeviceType.odu100:
        ra_mac = du.get_odu100_ra_mac(ip_address.split(":")[0],community,port)         # #{'result': '00:80:48:71:85:B9', 'success': 0}
    if node_type == 0 or node_type == 1 or node_type == 2 or node_type == 3:
        out["node_type_success"] = 0
        out["node_type"] = node_type
    elif node_type == 6:
        out["node_type_success"] = 1
        out["node_type"] = "UNMP server is busy, please try again later."



    if isinstance(ra_mac,dict):
        if ra_mac["success"] == 0:
            out["ra_mac_success"] = 0
            out["ra_mac"] = ra_mac["result"]
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(out))

def get_master_mac_from_slave(h):
    global html
    html = h
    out = {"success":1,"result":"SNMP agent gone away or device Unreachable"}
    ip_address = html.var("ip_address")
    community = html.var("community") != None and html.var("community") or "public"
    port = html.var("port") != None and html.var("port") or 161
    port = Validation.is_number(port) and port or 161
    du = DeviceUtility()
    ra_mac_dict = du.get_master_mac_from_slave(str(ip_address).split(":")[0],community,port)
    hst_bll = HostBll()
    ra_mac = ""
    if ra_mac_dict["success"] == 0:
        ra_mac = str(ra_mac_dict["result"]).split(",")[0]
        if Validation.is_valid_mac(ra_mac) == True:
            master_id = hst_bll.get_master_id_by_ra_mac(ra_mac)
            if isinstance(master_id,long) or isinstance(master_id,int):
                out["success"] = 0
                out["result"] = master_id
            elif isinstance(master_id,str):
                out["result"] = "Device not exist for '%s' RA MAC" % ra_mac
            else:
                out["result"] = "UNMP server busy can't fetch host. RA MAC is '%s'" % ra_mac
        else:
            out["result"] = "Device Unreachable or RA MAC is incorrect"#"SNMP agent down or RA MAC is incorrect"
            21
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(out))

def get_network_details(h):
    global html
    html  = h
    out = {"success":1,"result":"SNMP agent gone away or device Unreachable"}
    ip_address = html.var("ip_address")
    community = html.var("community") != None and html.var("community") or "public"
    port = html.var("port") != None and html.var("port") or 161
    port = Validation.is_number(port) and int(port) or 161
    device_type = html.var("device_type")
    result = {"netmask":"","gateway":"","dns_state":"","primary_dns":"","secondary_dns":""}
    if UNMPDeviceType.ap25 == device_type:
        snmp_result1 = pysnmp_get_node("1.3.6.1.4.1.26149.10.1.2",ip_address,port,community)
        snmp_result2 = pysnmp_get("1.3.6.1.4.1.26149.10.1.3.1.1",ip_address,port,community)
        out["result1"] = snmp_result1
        out["result2"] = snmp_result2
        if snmp_result1["success"] == 0 and snmp_result2["success"] == 0 and len(snmp_result1["result"][1]) > 4:
            out["success"] = 0
            result["netmask"] = snmp_result1["result"][1][1]
            result["gateway"] = snmp_result1["result"][1][2]
            result["dns_state"] = snmp_result2["result"]["1.3.6.1.4.1.26149.10.1.3.1.1"]
            result["primary_dns"] = snmp_result1["result"][1][3]
            result["secondary_dns"] = snmp_result1["result"][1][4]
            result["odu100_management_mode"] = 0
            result["odu100_vlan_tag"] = 0
            result["idu4_management_mode"] = 0
            result["idu4_vlan_tag"] = 0
            result["idu4_tdm_ip"] = ""
            result["ccu_dhcp_netmask"] = ""
            out["result"] = result
    elif UNMPDeviceType.odu16 == device_type:
        snmp_result = pysnmp_get_table("1.3.6.1.4.1.26149.2.2.9.1",ip_address,port,community)
        if snmp_result["success"] == 0 and len(snmp_result["result"][1]) > 5:
            out["success"] = 0
            result["netmask"] = snmp_result["result"][1][3]
            result["gateway"] = snmp_result["result"][1][4]
            result["dns_state"] = snmp_result["result"][1][5]
            result["primary_dns"] = ""
            result["secondary_dns"] = ""
            result["odu100_management_mode"] = 0
            result["odu100_vlan_tag"] = 0
            result["idu4_management_mode"] = 0
            result["idu4_vlan_tag"] = 0
            result["idu4_tdm_ip"] = ""
            result["ccu_dhcp_netmask"] = ""
            out["result"] = result
    elif UNMPDeviceType.odu100 == device_type:#{'result': {1: ['1', '1', '172.22.0.102', '255.255.255.0', '172.22.0.1', '0', '0', '0']}, 'success': 0}
        snmp_result = pysnmp_get_table("1.3.6.1.4.1.26149.2.2.9.1",ip_address,port,community)
        if snmp_result["success"] == 0 and len(snmp_result["result"][1]) > 7:
            out["success"] = 0
            result["netmask"] = snmp_result["result"][1][3]
            result["gateway"] = snmp_result["result"][1][4]
            result["dns_state"] = snmp_result["result"][1][5]
            result["primary_dns"] = ""
            result["secondary_dns"] = ""
            result["odu100_management_mode"] = snmp_result["result"][1][6]
            result["odu100_vlan_tag"] = snmp_result["result"][1][7]
            result["idu4_management_mode"] = 0
            result["idu4_vlan_tag"] = 0
            result["idu4_tdm_ip"] = ""
            result["ccu_dhcp_netmask"] = ""
            out["result"] = result
    elif UNMPDeviceType.idu4 == device_type:#{'result': {1: ['0', '172.22.0.104', '255.255.255.0', '172.22.0.100', '0']}, 'success': 0}
        snmp_result = pysnmp_get_table("1.3.6.1.4.1.26149.2.1.2.4.1",ip_address,port,community)
        if snmp_result["success"] == 0 and len(snmp_result["result"][1]) > 4:
            out["success"] = 0
            result["netmask"] = snmp_result["result"][1][2]
            result["gateway"] = snmp_result["result"][1][3]
            result["dns_state"] = snmp_result["result"][1][4]
            result["primary_dns"] = ""
            result["secondary_dns"] = ""
            result["odu100_management_mode"] = 0
            result["odu100_vlan_tag"] = 0
            result["idu4_management_mode"] = 0
            result["idu4_vlan_tag"] = 0
            result["idu4_tdm_ip"] = ""
            result["ccu_dhcp_netmask"] = ""
            out["result"] = result
    elif UNMPDeviceType.idu8 == device_type:
        out["result"] = "SNMP oid is undefined or device Unreachable"
    elif UNMPDeviceType.ccu == device_type:
        snmp_result = pysnmp_get_table_ccu("1.3.6.1.4.1.26149.3.5.1",ip_address,port,community)
        if snmp_result["success"] == 0 and len(snmp_result["result"][1]) > 7:
            out["success"] = 0
            result["netmask"] = snmp_result["result"][1][3]
            result["gateway"] = snmp_result["result"][1][7]
            result["dns_state"] = 0
            result["primary_dns"] = ""
            result["secondary_dns"] = ""
            result["odu100_management_mode"] = 0
            result["odu100_vlan_tag"] = 0
            result["idu4_management_mode"] = 0
            result["idu4_vlan_tag"] = 0
            result["idu4_tdm_ip"] = ""
            result["ccu_dhcp_netmask"] = snmp_result["result"][1][6]
            out["result"] = result
    elif UNMPDeviceType.swt4 == device_type:
        out["result"] = "SNMP oid is undefined or device Unreachable"
    elif UNMPDeviceType.swt24 == device_type:
        out["result"] = "SNMP oid is undefined or device Unreachable"
    elif UNMPDeviceType.generic == device_type:
        out["result"] = "SNMP oid is undefined or device Unreachable"
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(out))

def host_default_details(h):
    global html
    html  = h
    hst_bll = HostBll()                             # creating the HostBll object
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(hst_bll.host_default_details()))

def get_host_by_id(h):
    global html
    html  = h
    host_id = html.var("host_id")
    user_id =  html.req.session['user_id']
    es = Essential()

    if es.is_host_allow(user_id,host_id) == 0:    
        hst_bll = HostBll()                             # creating the HostBll object
        host = hst_bll.get_host_by_id(host_id)
        if isinstance(host, ErrorMessages):
            result = {"success":1,"msg":str(host.error_msg)}
        elif isinstance(host, Exception):
            result = {"success":1,"msg":"sysError","asdf":str(host)}
        else:
            result = {"success":0,"result":host}
    else:
        result = {"success":1,"msg":str("authError")}
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))

def is_duplicate_host_with_mac_address(h):
    global html
    html = h
    mac_address = html.var("mac_address")
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(HostBll().is_duplicate_host_with_mac_address(mac_address)))

def is_duplicate_host_with_ip_address(h):
    global html
    html = h
    ip_address = html.var("ip_address")
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(HostBll().is_duplicate_host_with_ip_address(ip_address)))

def is_duplicate_host_with_host_alias(h):
    global html
    html = h
    host_alias = html.var("host_alias")
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(HostBll().is_duplicate_host_with_host_alias(host_alias)))

def add_host(h):
    global html
    html = h
    try:
	    lb = LicenseBll()
	    device_type = html.var("device_type")
	    lb_result = lb.check_license_for_host(device_type)
	    if lb_result == True:
		nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
		host_name = html.var("host_name")
		host_alias = html.var("host_alias")
		ip_address = html.var("ip_address")
		mac_address = html.var("mac_address").upper() if html.var("mac_address") else html.var("mac_address")
		device_type_id = html.var("device_type")
		netmask = html.var("netmask")
		gateway = html.var("gateway")
		primary_dns = html.var("primary_dns")
		secondary_dns = html.var("secondary_dns")
		dns_state = html.var("dns_state")
		odu100_management_mode = html.var("odu100_management_mode")
		odu100_vlan_tag = html.var("odu100_vlan_tag")
		idu4_management_mode = html.var("idu4_management_mode") != None and html.var("idu4_management_mode") or 0
		idu4_vlan_tag = html.var("idu4_vlan_tag")
		idu4_tdm_ip = html.var("idu4_tdm_ip")
		ccu_dhcp_netmask = html.var("ccu_dhcp_netmask")
		timestamp = str(datetime.now())
		created_by = html.req.session["username"]
		creation_time = timestamp
		is_deleted = 0
		updated_by = created_by
		ne_id = None
		site_id = None
		host_state_id = html.var("host_state") 
		priority_id = html.var("host_priority")
		host_vendor_id = html.var("host_vendor")
		host_os_id = html.var("host_os")
		http_username = html.var("http_username")
		http_password = html.var("http_password")
		http_port = html.var("http_port")
		ssh_username = html.var("ssh_username")
		ssh_password = html.var("ssh_password")
		ssh_port = html.var("ssh_port")
		snmp_read_community = html.var("read_community")
		snmp_write_community = html.var("write_community")
		snmp_port = html.var("get_set_port")
		snmp_trap_port = html.var("trap_port")
		snmp_version_id = html.var("snmp_version")
		comment = html.var("host_comment")
		nms_instance = nms_instance
		parent_name = html.var("host_parent")
		lock_status = html.var("lock_position") and "t" or "f" 
		is_reconciliation = html.var("is_reconciliation") and True or False 
		is_localhost = 0
		longitude = html.var("longitude")
		latitude = html.var("latitude")
		serial_number = html.var("serial_number")
		hardware_version = html.var("hardware_version")
		hostgroup = html.var("hostgroup")
		ra_mac = html.var("ra_mac")
		node_type = html.var("node_type")
		master_id = html.var("master_mac")
		firmware_version = html.var("firmware_version")
		# check the version only for odu
		if firmware_version != None and firmware_version != "":#len(firmware_version)>1:
		    firmware_mapping_id = "7.2.20" if int(firmware_version.split(".")[-1]) < 25 and int(firmware_version.split(".")[-1]) >= 20 else "7.2.25"
		hst_bll = HostBll()                             # creating the HostBll object
		host = hst_bll.add(host_name,host_alias,ip_address,mac_address,device_type_id,netmask,gateway,primary_dns,secondary_dns,dns_state,odu100_management_mode,odu100_vlan_tag,idu4_management_mode,idu4_vlan_tag,idu4_tdm_ip,ccu_dhcp_netmask,timestamp,created_by,creation_time,is_deleted,updated_by,ne_id,site_id,host_state_id,priority_id,host_vendor_id,host_os_id,http_username,http_password,http_port,ssh_username,ssh_password,ssh_port,snmp_read_community,snmp_write_community,snmp_port,snmp_trap_port,snmp_version_id,comment,nms_instance,parent_name,lock_status,is_localhost,longitude,latitude,serial_number,hardware_version,hostgroup,ra_mac,node_type,master_id,firmware_version,is_reconciliation)
		if isinstance(host, ErrorMessages):
		    result = {"success":1,"msg":str(host.error_msg)}
		elif isinstance(host, Exception):
		    result = {"success":1,"msg":"sysError","h":str(host)}
		else:
		    result = {"success":0}
	    elif lb_result == "deviceTypeFalse":
		result = {"success":1,"msg":"licenseDeviceError"}        
	    else:
		result = {"success":1,"msg":"licenseError"}                
    except Exception,e:
        result = {}
        import traceback
        result["success"] = 1
        result["result"] = str(traceback.format_exc())
    finally:
        html.req.content_type = 'application/json'
        html.write(JSONEncoder().encode(result))

def edit_host(h):
    global html
    html = h
    nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
    lb = LicenseBll()
    host_id = html.var("host_id")
    device_type = html.var("device_type")
    lb_result = lb.check_license_for_host_edit(device_type,host_id)
    if lb_result == True:    
        host_name = html.var("host_name")
        host_alias = html.var("host_alias")
        ip_address = html.var("ip_address")
        mac_address = html.var("mac_address")
        device_type_id = html.var("device_type")
        netmask = html.var("netmask")
        gateway = html.var("gateway")
        primary_dns = html.var("primary_dns")
        secondary_dns = html.var("secondary_dns")
        dns_state = html.var("dns_state")
        odu100_management_mode = html.var("odu100_management_mode")
        odu100_vlan_tag = html.var("odu100_vlan_tag")
        idu4_management_mode = html.var("idu4_management_mode") != None and html.var("idu4_management_mode") or 0
        idu4_vlan_tag = html.var("idu4_vlan_tag")
        idu4_tdm_ip = html.var("idu4_tdm_ip")
        ccu_dhcp_netmask = html.var("ccu_dhcp_netmask")
        is_deleted = 0
        updated_by = html.req.session["username"]
        host_state_id = html.var("host_state") 
        priority_id = html.var("host_priority")
        host_vendor_id = html.var("host_vendor")
        host_os_id = html.var("host_os")
        http_username = html.var("http_username")
        http_password = html.var("http_password")
        http_port = html.var("http_port")
        ssh_username = html.var("ssh_username")
        ssh_password = html.var("ssh_password")
        ssh_port = html.var("ssh_port")
        snmp_read_community = html.var("read_community")
        snmp_write_community = html.var("write_community")
        snmp_port = html.var("get_set_port")
        snmp_trap_port = html.var("trap_port")
        snmp_version_id = html.var("snmp_version")
        comment = html.var("host_comment")
        parent_name = html.var("host_parent")
        hostgroup = html.var("hostgroup")
        lock_status = html.var("lock_position") and "t" or "f" 
        is_localhost = 0
        longitude = html.var("longitude")
        latitude = html.var("latitude")
        serial_number = html.var("serial_number")
        hardware_version = html.var("hardware_version")
        ra_mac = html.var("ra_mac")
        node_type = html.var("node_type")
        master_id = html.var("master_mac")
        ip_update = html.var("ip_update")
        firmware_version = html.var("firmware_version")
        hst_bll = HostBll()                             # creating the HostBll object
        host = None
        if str(ip_update) == "1":
            dhcp = dns_state == "Enable" and "1" or "0"
            device_dic = {"host_id":host_id, "device_type_id":device_type_id, "ip_address":ip_address, "ip_network_mask":netmask, "ip_gateway":gateway, "dhcp": dhcp, "primarydns":primary_dns,"secondarydns":secondary_dns,"odu100_vlan_tag":odu100_vlan_tag,"odu100_management_mode":odu100_management_mode,"idu4_management_mode":idu4_management_mode,"idu4_vlan_tag":idu4_vlan_tag,"idu4_tdm_ip":idu4_tdm_ip,"ccu_dhcp_netmask":ccu_dhcp_netmask}
            result_dic = hst_bll.change_device_network_details(device_dic)
            if isinstance(result_dic,dict) and result_dic.get("success") == 0:
                host = hst_bll.edit(host_id,host_name,host_alias,ip_address,mac_address,device_type_id,netmask,gateway,primary_dns,secondary_dns,dns_state,odu100_management_mode,odu100_vlan_tag,idu4_management_mode,idu4_vlan_tag,idu4_tdm_ip,ccu_dhcp_netmask,is_deleted,updated_by,host_state_id,priority_id,host_vendor_id,host_os_id,http_username,http_password,http_port,ssh_username,ssh_password,ssh_port,snmp_read_community,snmp_write_community,snmp_port,snmp_trap_port,snmp_version_id,comment,nms_instance,parent_name,lock_status,longitude,latitude,serial_number,hardware_version,hostgroup,ra_mac,node_type,master_id,firmware_version)
                if isinstance(host, ErrorMessages):
                    result = {"success":1,"msg":str(host.error_msg)}
                elif isinstance(host, Exception):
                    result = {"success":1,"msg":"sysError"}
                elif host == None:
                    result = {"success":1,"msg":"sysError"}
                else:
                    result = {"success":0,"h":str(host)}
            else:
                result = {"success":1,"msg":"changeIpAddressError"}
            html.req.content_type = 'application/json'
            html.write(JSONEncoder().encode(result))
        else:
            host = hst_bll.edit(host_id,host_name,host_alias,ip_address,mac_address,device_type_id,netmask,gateway,primary_dns,secondary_dns,dns_state,odu100_management_mode,odu100_vlan_tag,idu4_management_mode,idu4_vlan_tag,idu4_tdm_ip,ccu_dhcp_netmask,is_deleted,updated_by,host_state_id,priority_id,host_vendor_id,host_os_id,http_username,http_password,http_port,ssh_username,ssh_password,ssh_port,snmp_read_community,snmp_write_community,snmp_port,snmp_trap_port,snmp_version_id,comment,nms_instance,parent_name,lock_status,longitude,latitude,serial_number,hardware_version,hostgroup,ra_mac,node_type,master_id,firmware_version)
            if isinstance(host, ErrorMessages):
                result = {"success":1,"msg":str(host.error_msg)}
            elif isinstance(host, Exception):
                result = {"success":1,"msg":"sysError","h":str(host)}
            elif host == None:
                result = {"success":1,"msg":"sysError"}
            else:
                result = {"success":0,"h":str(host)}
            html.req.content_type = 'application/json'
            html.write(JSONEncoder().encode(result))

    else:
        result = {"success":1,"msg":"licenseDeviceError"}  
        html.req.content_type = 'application/json'
        html.write(JSONEncoder().encode(result))

def del_host(h):
    global html
    html = h
    nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
    host_ids = html.var("host_ids")
    host_ids = host_ids !=None and host_ids or ""
    updated_by = html.req.session["username"]
    hst_bll = HostBll()                             # creating the HostBll object
    host_count = hst_bll.delete(host_ids.split(","),nms_instance,updated_by)
    if isinstance(host_count, ErrorMessages):
        result = {"success":1,"msg":str(host_count.error_msg)}
    elif isinstance(host_count, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))

def del_deleted_host(h):
    global html
    html = h
    nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
    host_ids = html.var("host_ids")
    host_ids = host_ids !=None and host_ids or ""
    updated_by = html.req.session["username"]
    hst_bll = HostBll()                             # creating the HostBll object
    host_count = hst_bll.delete_deleted_host(host_ids.split(","),nms_instance,updated_by)
    if isinstance(host_count, ErrorMessages):
        result = {"success":1,"msg":str(host_count.error_msg)}
    elif isinstance(host_count, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))

def add_deleted_host(h):
    global html
    html = h
    nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
    host_ids = html.var("host_ids")
    host_ids = host_ids !=None and host_ids or ""
    updated_by = html.req.session["username"]
    hst_bll = HostBll()                             # creating the HostBll object
    host_count = hst_bll.add_deleted_host(host_ids.split(","),nms_instance,updated_by)
    if isinstance(host_count, ErrorMessages):
        result = {"success":1,"msg":str(host_count.error_msg)}
    elif isinstance(host_count, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))

def page_tip_inventory_host(h):
    global html
    html = h
    html.write(Host.page_tip_host())
# End-Host


# Hostgroup
def manage_hostgroup(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/inventory_hostgroup.js"]
    header_btn = Hostgroup.header_buttons()
    html.new_header("Hostgroups","manage_hostgroup.py",header_btn,css_list,js_list)
    html.write(Hostgroup.manage_hostgroup())
    html.new_footer()


def grid_view_hostgroup(h):
    global html
    html = h
    flag_value = 1    
    hostgroup_id_list = []

    if html.req.session['group'].lower() == 'SuperAdmin'.lower():
        flag_value = 0
    #html.write(str(flag_value))
    if flag_value:
        user_id =  html.req.session['user_id']
        es = Essential()
        hostgroup_id_list = es.get_hostgroup_ids(user_id)
    hostgroups_list = []                                # creating empty list [we will use this in datatables]
    #html.write(str(flag_value))
    if len(hostgroup_id_list) > 0 or flag_value == 0:
        hg_bll = HostgroupBll()                             # creating the HostgorupBll object
        all_hostgroups = hg_bll.grid_view(hostgroup_id_list,flag_value)                 # fetching all hostgroups data from database
        number_of_hosts= hg_bll.grid_view_number_of_hosts(hostgroup_id_list,flag_value)
        #html.write(str(number_of_hosts))
        #html.write(str(all_hostgroups))
        #html.write(str(hostgroup_id_list))
        s_no = 0
        temp_list = []
        di_hg={}
        for row in number_of_hosts:
            key=str(row[0])
            if di_hg.has_key(key):
                j=di_hg[key]
                j.append(row[4]+" ("+str(row[3])+") ")
                di_hg[key]=j
            else:
                j=[row[4]+" ("+str(row[3])+") "]
                di_hg[key]=j
        #html.write(str(all_hostgroups)+" &&&&&&  "+str(hostgroup_id_list)+str(flag_value)+" ;; ")
        #html.write(str(di_hg))
        for hg in all_hostgroups:
            s_no += 1
            if hg.hostgroup_id in temp_list:
                indx = temp_list.index(hg.hostgroup_id)
                hostgroups_list[indx][5] += ", "
                hostgroups_list[indx][5] += hg.group_name != None and hg.group_name or ""

            else:
                hostgroups_list.append([str(hg.hostgroup_id),\
                                        hg.is_default,\
                                        s_no,\
                                        hg.hostgroup_name != None and hg.hostgroup_name or "-",\
                                        hg.hostgroup_alias != None and hg.hostgroup_alias or "-",\
                                        hg.group_name != None and hg.group_name or "",\
                                        ", ".join(di_hg[str(hg.hostgroup_id)]) if di_hg.has_key(str(hg.hostgroup_id)) else "" ,\
                                        "<img id=\"%s\" src=\"images/new/group.png\" title=\"Manage Assigned Usergroups\" alt=\"manage\" class=\"img-link\" />&nbsp\
                                    <a href=\"javascript:editHostgroup(%s,%s);\"><img class=\"host_opr\" title=\"Edit Hostgroup\" src=\"images/new/edit.png\" alt=\"edit\"/></a>" % (hg.hostgroup_id,hg.hostgroup_id,hg.is_default) ] )       # creating 2D List of hostgroup details
                temp_list.append(hg.hostgroup_id)

    html.write(str(hostgroups_list))




def form_hostgroup(h):
    global html
    html = h
    html.write(Hostgroup.create_form())

def add_hostgroup(h):
    global html
    html = h
    nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
    hostgroup_name = html.var("hostgroup_name")
    hostgroup_alias = html.var("hostgroup_alias")
    timestamp = str(datetime.now())
    created_by = html.req.session["username"]
    group_name = html.req.session["group"]
    creation_time = timestamp
    is_deleted = 0
    updated_by = created_by
    is_default = 0
    hg_bll = HostgroupBll()                             # creating the HostgorupBll object
    hostgroup_id = hg_bll.add(hostgroup_name,hostgroup_alias,timestamp,created_by,creation_time,is_deleted,updated_by,is_default,nms_instance,group_name)
    if isinstance(hostgroup_id, ErrorMessages):
        result = {"success":1,"msg":str(hostgroup_id.error_msg)}
    elif isinstance(hostgroup_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def get_hostgroup_by_id(h):
    global html
    html = h
    hostgroup_id = html.var("hostgroup_id")
    hg_bll = HostgroupBll()                             # creating the HostgorupBll object
    hostgroup = hg_bll.get_hostgroup_by_id(hostgroup_id)
    if isinstance(hostgroup, ErrorMessages):
        result = {"success":1,"msg":str(hostgroup.error_msg)}
    elif isinstance(hostgroup, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0,"result":[str(hostgroup.hostgroup_id),hostgroup.hostgroup_name != None and hostgroup.hostgroup_name or "",hostgroup.hostgroup_alias != None and hostgroup.hostgroup_alias or "",hostgroup.timestamp != None and hostgroup.timestamp.strftime("%d-%m-%Y %H:%M") or "",hostgroup.created_by != None and hostgroup.created_by or "",hostgroup.creation_time != None and hostgroup.creation_time.strftime("%d-%m-%Y %H:%M") or "",hostgroup.updated_by != None and hostgroup.updated_by or ""]}
    html.write(str(result))

def edit_hostgroup(h):
    global html
    html = h
    nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
    hostgroup_id = html.var("hostgroup_id")
    hostgroup_name = html.var("hostgroup_name")
    hostgroup_alias = html.var("hostgroup_alias")
    timestamp = str(datetime.now())
    is_deleted = 0
    updated_by = html.req.session["username"]
    is_default = 0
    hg_bll = HostgroupBll()                             # creating the HostgorupBll object
    hostgroup_id = hg_bll.edit(hostgroup_id,hostgroup_name,hostgroup_alias,timestamp,is_deleted,updated_by,is_default,nms_instance)
    if isinstance(hostgroup_id, ErrorMessages):
        result = {"success":1,"msg":str(hostgroup_id.error_msg)}
    elif isinstance(hostgroup_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def del_hostgroup(h):
    global html
    html = h
    nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
    hostgroup_ids = html.var("hostgroup_ids")
    hostgroup_ids = hostgroup_ids !=None and hostgroup_ids or ""
    updated_by = html.req.session["username"]
    hg_bll = HostgroupBll()                             # creating the HostgorupBll object
    hostgroup_count = hg_bll.delete(hostgroup_ids.split(","),nms_instance,updated_by)
    if isinstance(hostgroup_count, ErrorMessages):
        result = {"success":1,"msg":str(hostgroup_count.error_msg)}
    elif isinstance(hostgroup_count, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def page_tip_inventory_hostgroup(h):
    global html
    html = h
    html.write(Hostgroup.page_tip_hostgroup())    
# End-Hostgroup

# Discovery
def discovery(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/inventory_discovery.js"]
    header_btn = Discovery.header_buttons()
    html.new_header("Discovery","discovery.py",header_btn,css_list,js_list)
    html.write(Discovery.discovery())
    html.new_footer()

def ping_discovery_form(h):
    global html
    html = h
    html.write(Discovery.ping_form())

def ping_discovery(h):
    global html
    html = h
    ping_ip_base = html.var("ping_ip_base")
    ping_ip_base_start = html.var("ping_ip_base_start")
    ping_ip_base_end = html.var("ping_ip_base_end")
    ping_timeout = html.var("ping_timeout")
    ping_service_mng  = html.var("ping_service_mng")
    timestamp = str(datetime.now())
    created_by = html.req.session["username"]
    creation_time = timestamp
    is_deleted = 0
    updated_by = created_by
    dis_bll = DiscoveryBll()                             # creating the HostgorupBll object
    ping_dis_id = dis_bll.ping_discovery(ping_ip_base,ping_ip_base_start,ping_ip_base_end,ping_timeout,ping_service_mng,timestamp,created_by,creation_time,updated_by,is_deleted)
    if isinstance(ping_dis_id, ErrorMessages):
        result = {"success":1,"msg":str(ping_dis_id.error_msg)}
    elif isinstance(ping_dis_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0,"discovery_id":str(ping_dis_id)}
    html.write(str(result))

def run_ping_discovery(h):
    global html
    html = h
    discovery_id = html.var("discovery_id")
    dis_bll = DiscoveryBll()
    rd = dis_bll.run_ping_discovery(discovery_id)
    if isinstance(rd, ErrorMessages):
        result = {"success":1,"msg":str(rd.error_msg)}
    elif isinstance(rd, Exception):
        result = {"success":1,"msg":"sysError","a":str(rd)}
    else:
        result = {"success":0}
    html.write(str(result))


def run_snmp_discovery(h):
    global html
    html = h
    discovery_id = html.var("discovery_id")
    dis_bll = DiscoveryBll()
    rd = dis_bll.run_snmp_discovery(discovery_id)
    if isinstance(rd, ErrorMessages):
        result = {"success":1,"msg":str(rd.error_msg)}
    elif isinstance(rd, Exception):
        result = {"success":1,"msg":"sysError","a":str(rd)}
    else:
        result = {"success":0}
    html.write(str(result))

def run_upnp_discovery(h):
    global html
    html = h
    discovery_id = html.var("discovery_id")
    dis_bll = DiscoveryBll()
    rd = dis_bll.run_upnp_discovery(discovery_id)
    if isinstance(rd, ErrorMessages):
        result = {"success":1,"msg":str(rd.error_msg)}
    elif isinstance(rd, Exception):
        result = {"success":1,"msg":"sysError","a":str(rd)}
    else:
        result = {"success":0}
    html.write(str(result))


def snmp_discovery_form(h):
    global html
    html = h

    # get snmp version list
    value = ["1","2c","3"]
    name = ["v1","v2c","v3"]
    selected = "2c"
    list_id = "snmp_version"
    list_name = "snmp_version"
    title = "Choose SNMP Version"
    snmp_version_select_list = Common.make_select_list(value, name, selected, list_id, list_name,title)

    html.write(Discovery.snmp_form(snmp_version_select_list))

def snmp_discovery(h):
    global html
    html = h
    snmp_ip_base = html.var("snmp_ip_base")
    snmp_ip_base_start = html.var("snmp_ip_base_start")
    snmp_ip_base_end = html.var("snmp_ip_base_end")
    snmp_timeout = html.var("snmp_timeout")
    snmp_community = html.var("snmp_community")
    snmp_version = html.var("snmp_version")
    snmp_port = html.var("snmp_port")
    snmp_service_mng  = html.var("snmp_service_mng")
    timestamp = str(datetime.now())
    created_by = html.req.session["username"]
    creation_time = timestamp
    is_deleted = 0
    updated_by = created_by
    dis_bll = DiscoveryBll()                             # creating the HostgorupBll object
    snmp_dis_id = dis_bll.snmp_discovery(snmp_ip_base,snmp_ip_base_start,snmp_ip_base_end,snmp_timeout,snmp_community,snmp_port,snmp_version,snmp_service_mng,timestamp,created_by,creation_time,updated_by,is_deleted)
    if isinstance(snmp_dis_id, ErrorMessages):
        result = {"success":1,"msg":str(snmp_dis_id.error_msg)}
    elif isinstance(snmp_dis_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0,"discovery_id":str(snmp_dis_id)}
    html.write(str(result))

def upnp_discovery_form(h):
    global html
    html = h
    html.write(Discovery.upnp_form())

def upnp_discovery(h):
    global html
    html = h
    upnp_timeout = html.var("upnp_timeout")
    upnp_service_mng  = html.var("upnp_service_mng")
    timestamp = str(datetime.now())
    created_by = html.req.session["username"]
    creation_time = timestamp
    is_deleted = 0
    updated_by = created_by
    dis_bll = DiscoveryBll()                             # creating the HostgorupBll object
    upnp_dis_id = dis_bll.upnp_discovery(upnp_timeout,upnp_service_mng,timestamp,created_by,creation_time,updated_by,is_deleted)
    if isinstance(upnp_dis_id, ErrorMessages):
        result = {"success":1,"msg":str(upnp_dis_id.error_msg)}
    elif isinstance(upnp_dis_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0,"discovery_id":str(upnp_dis_id)}
    html.write(str(result))

def page_tip_inventory_discovery(h):
    global html
    html = h
    html.write(Discovery.page_tip_discovery())

def delete_discovered_host(h):   
    global html
    html = h
    discovery_type = html.var("discovery_type")
    host_id = html.var("host_id")

    host_id = host_id !=None and host_id or ""
    discovery_type = discovery_type != None and discovery_type or ""
    updated_by = html.req.session["username"]
    dis_bll = DiscoveryBll()                             # creating the HostgorupBll object
    host_count = dis_bll.delete_discovered_host(discovery_type.split(","),host_id.split(","),updated_by)
    if isinstance(host_count, ErrorMessages):
        result = {"success":1,"msg":str(host_count.error_msg)}
    elif isinstance(host_count, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))

def ping_default_details(h):
    global html
    html = h
    dis_bll = DiscoveryBll()                             # creating the HostBll object
    html.write(str(dis_bll.ping_default_details()))

def snmp_default_details(h):
    global html
    html = h
    dis_bll = DiscoveryBll()                             # creating the HostBll object
    html.write(str(dis_bll.snmp_default_details()))

def upnp_default_details(h):
    global html
    html = h
    dis_bll = DiscoveryBll()                             # creating the HostBll object
    html.write(str(dis_bll.upnp_default_details()))
# End-Discovery

# Service
def manage_service(h):
    global html
    html = h
    #css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css","css/jquery.multiselect.css"]
    css_list=["css/demo_table_jui.css","css/style12.css","css/jquery.multiselect.css","css/jquery.multiselect.filter.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery-ui-1.8.6.custom.min.js","js/pages/jquery.multiselect.min.js","js/pages/jquery.multiselect.filter.js","js/jquery.dataTables.min.js","js/pages/inventory_service.js"]
    #   js_list = ["js/jquery.dataTables.min.js","js/jquery-ui-1.8.6.custom.min.js","js/pages/jquery.multiselect.min.js","js/pages/inventory_service.js"]
    add_btn = "<div class=\"header-icon\"><img onclick=\"addService();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_service\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Service\"></div>" % theme
    edit_btn = "<div class=\"header-icon\"><img onclick=\"editService();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_service\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit Service\"></div>" % theme
    del_btn = "<div class=\"header-icon\"><img onclick=\"delService();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_service\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Service\"></div>" % theme
    header_btn = ""
    html.new_header("Services","manage_service.py",header_btn,css_list,js_list)
    html.write(Service.manage_service())
    html.new_footer()

def page_tip_inventory_service(h):
    global html
    html = h
    html.write(Service.page_tip_service())

def grid_view_service(h):
    global html
    html = h
    i_display_start=str(html.var("iDisplayStart"))
    i_display_length=str(html.var("iDisplayLength"))
    s_search=str(html.var("sSearch"))
    sEcho=str(html.var("sEcho"))
    s_search=str(html.var("sSearch"))
    sSortDir_0=str(html.var("sSortDir_0"))
    iSortCol_0=str(html.var("iSortCol_0"))
    user_id =  html.req.session['user_id']  
    srv_bll = ServiceBll(user_id)
    #srv_bll = ServiceBll()
    try:                             # creating the ServiceBll object
        all_hosts_dict = srv_bll.grid_view(i_display_start,i_display_length,s_search,sEcho,sSortDir_0,iSortCol_0,html.req.vars)                     # fetching all hostgroups data from database
        host_list = []                                # creating empty list [we will use this in datatables]
        all_hosts=all_hosts_dict["aaData"]
        s_no = 0
        for hst in all_hosts:
            s_no += 1
            ip_address=hst.ip_address
            query_service = "GET services\nColumns: service_state service_description service_last_check service_next_check \nFilter: host_address = " + ip_address
            html.live.set_prepend_site(True)
            serv= html.live.query(query_service)
            #serv.sort()
            html.live.set_prepend_site(False)
            host_list.append([str(hst.host_id),\
                              int(hst.is_localhost),\
                              "<a href=\"#\"onclick=\"viewServiceDetails(%s,'%s')\">"%(str(hst.host_id),hst.host_alias) + (hst.ip_address != None and hst.ip_address or "-") + "</a>",\
                              hst.host_alias != None and hst.host_alias or "-",\
                              hst.hostgroup_name != None and hst.hostgroup_name or "-",\
                              hst.device_name != None and hst.device_name or "-",\
                              #str(serv),
                              #str(srv_bll.grid_view_service(hst.host_id)),\
                              make_service_box(srv_bll.grid_view_service(hst.host_id),serv),\
                              "<a href=\"javascript:editService(%s,%s);\"><img class='host_opr' title='Edit Service Details' src='images/new/edit.png' alt='edit'/></a>" % (hst.host_id,hst.is_localhost)])
        #html.write(str(host_list))
        all_hosts_dict["aaData"]=host_list
        html.write(JSONEncoder().encode(all_hosts_dict))
        #html.write(str(all_hosts_dict))
    except Exception,e:
        output = {
            "sEcho": 1,
            "iTotalRecords":1,
            "iTotalDisplayRecords": 1,
            "aaData":[],
            "query":str(e)
        }
        html.write(str(output))
        #html.write(JSONEncoder().encode(output))

def get_time_tick(timetick,flag=0):
    import datetime
    last_check=""
    if datetime.datetime.now()>datetime.datetime.fromtimestamp(timetick):
        delta=datetime.datetime.now()-datetime.datetime.fromtimestamp(timetick)
        if flag:
            return " Service check is in progress"
    else:
        delta=datetime.datetime.fromtimestamp(timetick)-datetime.datetime.now()
    second=delta.seconds
    if second<60:
        last_check=str(second)+" sec"
    elif second<3600:
        minute=int(second/60)
        second=second%60
        last_check=str(minute)+" min "+str(second)+" sec"
    elif second<86400 and delta.days==0:
        hour=int(second/3600)
        minute=int((second-hour*3600)/60)
        last_check=str(hour)+" hour,"+str(minute)+" min"	    
    else:
        hour=int(second/3600)
        minute=int((second-hour*3600)/60)
        last_check=str(delta.days)+" days,"+str(hour)+" hour,"+str(minute)+" min"
    return last_check

def make_service_box(services,live_status):
    try:
        global html
        html_str=""
        for service_tuple in services:
            mins=service_tuple[1] or "-"
            if str(mins)=="518400":
                mins="Y"
            elif str(mins)=="43200":
                mins="M"
            elif str(mins)=="1440":
                mins="D"
            #elif str(mins)=="720":
            #    mins="12 Hours"

            service_name=service_tuple[0]
            host_id=service_tuple[2]
            index=[ i for i,x in enumerate(live_status) if x.count(service_name) ]
            if index==[]:
                continue
            time_tick=live_status[index[0]][3]
            last_check=get_time_tick(time_tick)
            time_tick=live_status[index[0]][4]
            next_check=get_time_tick(time_tick,1)
            service_status=live_status[index[0]][1]
            if service_status in [0,1,2,3]:
                html_str+= "<div class=\"service-box n-tip-image\" id=\"service_big_box_%s_%s\" \
                title=\"Service check &lt;br/&gt;&lt;br/&gt;Time since last check:%s.&lt;br/&gt;Time of next scheduled check:%s.\"> \
                <img id=\"service_big_box_%s_%s_img\" style=\"z-index:3;float:left;height:15px;width:15px;vertical-align:middle;margin-top:3px;\" src=\"images/new/status-%s.png\"/> \
                <span style=\"padding:5px;float:left;\">%s</span> \
                <div id=\"service_box_%s_%s\" class=\"service-boxwhite\" style=\"height:12px;float:right;padding:2px 5px 5px 5px;\" >%s</div></div> \
                " % (str(host_id),str(service_name.replace(" ","_")),last_check,next_check,str(host_id),str(service_name.replace(" ","_")),service_status,service_name,str(host_id),str(service_name.replace(" ","_")),str(mins))
            else:
                html_str+= " <div class=\"service-box n-tip-image\" id=\"service_big_box_%s_%s\" \
                title=\"Service check <br/><br/>Time since last check:%s.<br/>Time of next scheduled check:%s.\"> \
                <img id=\"service_big_box_%s_%s_img\" style=\"z-index:3;float:left;height:15px;width:15px;vertical-align:middle;margin-top:3px;\" src=\"images/new/status-3.png\"/> \
                <span style=\"padding:5px;float:left;\">%s</span> \
                <div id=\"service_box_%s_%s\" class=\"service-boxwhite\" style=\"height:12px;float:right;padding:2px 5px 5px 5px \" >%s</div></div> \
                " % (str(host_id),str(service_name.replace(" ","_")),last_check,next_check,str(host_id),str(service_name.replace(" ","_")),service_name,str(host_id),str(service_name.replace(" ","_")),str(mins))
        return html_str
    except Exception,e:
        return str(e)


def edit_service_details(h): 
    global html
    html = h
    host_id=html.var("host_id")
    user_id =  html.req.session['user_id']  
    srv_bll = ServiceBll(user_id)
    host_details=srv_bll.get_host_details(host_id)[0]
    html_str=Service.edit_service_details(host_details.host_alias,srv_bll.grid_view_service(host_id))
    html.write(html_str)

def apply_service_changes(h):
    global html
    html = h   
    hosts_list=str(html.var("service_hosts")).split(",")
    service_time=str(html.var("service_time")).split(",")
    service_name=str(html.var("service_name")).split(",")
    user_id =  html.req.session['user_id']  
    user_name=  html.req.session['username']  
    srv_bll = ServiceBll(user_id)
    result=srv_bll.set_service_time(hosts_list,service_name,service_time,user_name)
    html.write(JSONEncoder().encode(result))

def update_service_table(h):    
    global html
    html = h   
    hosts_list=str(html.var("hosts_list")).split(",")
    if hosts_list==[""]:
        html.write("[]")
    else:
        user_id=html.req.session["user_id"]
        srv_bll = ServiceBll(user_id)
        all_host=[]
        all_hosts=[]
        for host in hosts_list:
            host_id=host.split('_')[3]
            all_host.append(host_id)
            if host_id not in all_hosts:
                all_hosts.append(host_id)
        host_result=[]
        #srv_bll = ServiceBll()
        title_str_list=[]
        html_str_list=[]
        service_str_list=[]
        try: 
            for host_id in all_hosts:
                result_obj=srv_bll.get_host_details(host_id)
                query_service = "GET services\nColumns: service_state service_description service_last_check service_next_check \nFilter: host_address = " + result_obj[0][3]
                html.live.set_prepend_site(True)
                serv= html.live.query(query_service)
                html.live.set_prepend_site(False)
                result=update_service_box(srv_bll.grid_view_service(host_id),serv)
                for j in result["html_str"]:
                    html_str_list.append(j)
                for j in result["title_str"]:
                    title_str_list.append(j)
                for j in result["service_str"]:
                    service_str_list.append(j)		    		    

            #html.write(str({"html_str":html_str_list,"title_str":title_str_list,"id_array":all_host,"service_str":service_str_list}))
            html.write(JSONEncoder().encode({"html_str":html_str_list,"title_str":title_str_list,"id_array":all_host,"service_str":service_str_list,"success":0}))
        except Exception,e:
            html.write(JSONEncoder().encode({"success":1,"except":str(e)}))

def update_service_box(services,live_status):
    try:
        global html
        html_str=[]
        title_str=[]
        service_str=[]
        for service_tuple in services:
            mins=service_tuple[1] or "-"
            service_name=service_tuple[0]
            service_str.append(service_name.replace(" ","_"))
            host_id=service_tuple[2]
            index=[ i for i,x in enumerate(live_status) if x.count(service_name) ]
            if index==[]:
                continue
            time_tick=live_status[index[0]][3]
            last_check=get_time_tick(time_tick)
            time_tick=live_status[index[0]][4]
            next_check=get_time_tick(time_tick,1)
            service_status=live_status[index[0]][1]
            title_str.append("Service check <br/><br/>Time since last check:%s.<br/>Time of next scheduled check:%s."%(last_check,next_check))
            if service_status in [0,1,2,3]:
                html_str.append(service_status)
            else:
                html_str.append(3)
        return {"html_str":html_str,"title_str":title_str,"service_str":service_str}
    except Exception,e:
        return {"html_str":str(e),"title_str":str(e)}
# End-Service
# Network-Map
def network_map(h):
    global html
    html = h
    css_list = []
    js_list = ["js/pages/inventory_network_map.js"]
    header_btn = ""
    html.new_header("Network Map","network_map.py",header_btn,css_list,js_list)
    html.write(NetworkMap.network_map())
    html.new_footer()

def page_tip_inventory_network_map(h):
    global html
    html = h
    html.write(NetworkMap.page_tip_network_map())

# End-Network-Map


# Vendor
def manage_vendor(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/inventory_vendor.js"]
    header_btn = Vendor.header_buttons()
    html.new_header("Vendor","#inventory",header_btn,css_list,js_list)
    html.write(Vendor.manage_vendor())
    html.new_footer()

def grid_view_vendor(h):
    global html
    html = h
    vd_bll = VendorBll()                             # creating the VendorBll object
    all_vendors = vd_bll.grid_view()                 # fetching all vendors data from database
    vendors_list = []                                # creating empty list [we will use this in datatables]
    s_no = 0
    for vd in all_vendors:
        s_no += 1
        vendors_list.append([str(vd.host_vendor_id),\
                             s_no,\
                             vd.vendor_name != None and vd.vendor_name or "-",\
                             vd.description != None and vd.description or "-"])       # creating 2D List of vendor details
    html.write(str(vendors_list))

def form_vendor(h):
    global html
    html = h
    html.write(Vendor.create_form())

def add_vendor(h):
    global html
    html = h
    vendor_name = html.var("vendor_name")
    description = html.var("description")
    timestamp = str(datetime.now())
    created_by = html.req.session["username"]
    creation_time = timestamp
    is_deleted = 0
    updated_by = created_by
    vd_bll = VendorBll()                             # creating the VendorBll object
    host_vendor_id = vd_bll.add(vendor_name,description,timestamp,created_by,creation_time,is_deleted,updated_by)
    if isinstance(host_vendor_id, ErrorMessages):
        result = {"success":1,"msg":str(host_vendor_id.error_msg)}
    elif isinstance(host_vendor_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def get_vendor_by_id(h):
    global html
    html = h
    host_vendor_id = html.var("host_vendor_id")
    vd_bll = VendorBll()                             # creating the VendorBll object
    vendor = vd_bll.get_vendor_by_id(host_vendor_id)
    if isinstance(vendor, ErrorMessages):
        result = {"success":1,"msg":str(vendor.error_msg)}
    elif isinstance(vendor, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0,"result":[str(vendor.host_vendor_id),vendor.vendor_name != None and vendor.vendor_name or "",vendor.description != None and vendor.description or ""]}
    html.write(str(result))

def edit_vendor(h):
    global html
    html = h
    host_vendor_id = html.var("host_vendor_id")
    vendor_name = html.var("vendor_name")
    description = html.var("description")
    timestamp = str(datetime.now())
    is_deleted = 0
    updated_by = html.req.session["username"]
    vd_bll = VendorBll()                             # creating the VendorBll object
    host_vendor_id = vd_bll.edit(host_vendor_id,vendor_name,description,timestamp,is_deleted,updated_by)
    if isinstance(host_vendor_id, ErrorMessages):
        result = {"success":1,"msg":str(host_vendor_id.error_msg)}
    elif isinstance(host_vendor_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def del_vendor(h):
    global html
    html = h
    host_vendor_ids = html.var("host_vendor_ids")
    host_vendor_ids = host_vendor_ids !=None and host_vendor_ids or ""
    updated_by = html.req.session["username"]
    vd_bll = VendorBll()                             # creating the HostgorupBll object
    vendor_count = vd_bll.delete(host_vendor_ids.split(","),updated_by)
    if isinstance(vendor_count, ErrorMessages):
        result = {"success":1,"msg":str(vendor_count.error_msg)}
    elif isinstance(vendor_count, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def page_tip_inventory_vendor(h):
    global html
    html = h
    html.write(Vendor.page_tip_vendor())

# End-Vendor

# BlackListMac
def manage_black_list_mac(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/inventory_black_list_mac.js"]
    header_btn = BlackListMac.header_buttons()
    html.new_header("Black List Mac","#inventory",header_btn,css_list,js_list)
    html.write(BlackListMac.manage_black_list_mac())
    html.new_footer()

def grid_view_black_list_mac(h):
    global html
    html = h
    blm_bll = BlackListMacBll()                             # creating the BlackListMacBll object
    all_black_list_macs = blm_bll.grid_view()                 # fetching all black_list_macs data from database
    black_list_macs_list = []                                # creating empty list [we will use this in datatables]
    s_no = 0
    for blm in all_black_list_macs:
        s_no += 1
        black_list_macs_list.append([str(blm.black_list_mac_id),\
                                     s_no,\
                                     blm.mac_address != None and blm.mac_address or "-",\
                                     blm.description != None and blm.description or "-"])       # creating 2D List of black_list_mac details
    html.write(str(black_list_macs_list))

def form_black_list_mac(h):
    global html
    html = h
    html.write(BlackListMac.create_form())

def add_black_list_mac(h):
    global html
    html = h
    mac_address = html.var("mac_address")
    description = html.var("description")
    timestamp = str(datetime.now())
    created_by = html.req.session["username"]
    creation_time = timestamp
    is_deleted = 0
    updated_by = created_by
    blm_bll = BlackListMacBll()                             # creating the BlackListMacBll object
    black_list_mac_id = blm_bll.add(mac_address,description,timestamp,created_by,creation_time,is_deleted,updated_by)
    if isinstance(black_list_mac_id, ErrorMessages):
        result = {"success":1,"msg":str(black_list_mac_id.error_msg)}
    elif isinstance(black_list_mac_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def get_black_list_mac_by_id(h):
    global html
    html = h
    black_list_mac_id = html.var("black_list_mac_id")
    blm_bll = BlackListMacBll()                             # creating the BlackListMacBll object
    black_list_mac = blm_bll.get_black_list_mac_by_id(black_list_mac_id)
    if isinstance(black_list_mac, ErrorMessages):
        result = {"success":1,"msg":str(black_list_mac.error_msg)}
    elif isinstance(black_list_mac, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0,"result":[str(black_list_mac.black_list_mac_id),black_list_mac.mac_address != None and black_list_mac.mac_address or "",black_list_mac.description != None and black_list_mac.description or ""]}
    html.write(str(result))

def edit_black_list_mac(h):
    global html
    html = h
    black_list_mac_id = html.var("black_list_mac_id")
    mac_address = html.var("mac_address")
    description = html.var("description")
    timestamp = str(datetime.now())
    is_deleted = 0
    updated_by = html.req.session["username"]
    blm_bll = BlackListMacBll()                             # creating the BlackListMacBll object
    black_list_mac_id = blm_bll.edit(black_list_mac_id,mac_address,description,timestamp,is_deleted,updated_by)
    if isinstance(black_list_mac_id, ErrorMessages):
        result = {"success":1,"msg":str(black_list_mac_id.error_msg)}
    elif isinstance(black_list_mac_id, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def del_black_list_mac(h):
    global html
    html = h
    black_list_mac_ids = html.var("black_list_mac_ids")
    black_list_mac_ids = black_list_mac_ids !=None and black_list_mac_ids or ""
    updated_by = html.req.session["username"]
    blm_bll = BlackListMacBll()                             # creating the HostgorupBll object
    black_list_mac_count = blm_bll.delete(black_list_mac_ids.split(","),updated_by)
    if isinstance(black_list_mac_count, ErrorMessages):
        result = {"success":1,"msg":str(black_list_mac_count.error_msg)}
    elif isinstance(black_list_mac_count, Exception):
        result = {"success":1,"msg":"sysError"}
    else:
        result = {"success":0}
    html.write(str(result))

def page_tip_inventory_black_list_mac(h):
    global html
    html = h
    html.write(BlackListMac.page_tip_black_list_mac())

# End-BlackListMac


# Misc
def write_nagios_config(h):
    nms_name = __file__.split("/")[3]       # it gives instance name of nagios system
    global html
    html = h
    hst_bll = NagioConfigurationBll()
    wng = hst_bll.write_nagios_config(nms_name)

    result = {"success":1,"msg":"unknownError"} 
    if isinstance(wng, bool):
        if wng == True:
            result = {"success":0}
        else:
            result = {"success":1,"msg":"nagiosConfigError"}
    elif isinstance(wng, Exception):
        result = {"success":1,"msg":"sysError","sda":wng}
    html.write(str(result))

def reload_nagios_config(h):
    global html
    html = h
    rslt = SystemSetting.reload_nagios_config()
    html.write(str(rslt))
# End-Misc
