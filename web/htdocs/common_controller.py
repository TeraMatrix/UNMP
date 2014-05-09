#!/usr/bin/python2.6
import MySQLdb

from unmp_model import *
import MySQLdb, xml.dom.minidom, sys, os
from sqlalchemy import create_engine
from sqlalchemy import *
from nagios_livestatus import Nagios
from common_bll import LocalSystemBll
from common import LocalSystem
from mysql_exception import mysql_connection
from json import JSONEncoder
from datetime import datetime
#session=session_db()
"""
Common Controller : All Common functions For NMS

Author : Anuj Samaria

(CodeScape Consultants Pvt. Ltd.) 
"""



##################################################
##                                              ##
##           Author- Anuj Samariya              ##
##                                              ##
##             Common Controller                ##
##                                              ##
##                                              ##
##          CodeScape Consultants Pvt. Ltd.     ##
##                                              ##
##################################################



class SqlAlchemyDBConnection(object):

    db = None
    db_connect = None
    #Session = None
    session = None
    error = 0
    def __init__(self):
        try:
            self.db = engine#create_engine("%s://%s:%s@%s/%s"%(sqlalchemy_driver,sqlalchemy_user_name,sqlalchemy_password,sqlalchemy_host,sqlalchemy_schema),pool_size=2,max_overflow=2,pool_timeout=300)
        except Exception as e:
            self.error = 1
    def sql_alchemy_db_connection_open(self):
        try:
            self.db_connect = self.db.connect()
            Session = sessionmaker(bind = self.db_connect)
            self.session = Session()
        except Exception as e:
            self.error = 1
    def get_sqlalchemy_credentials(self):
        sitename = __file__.split("/")[3]	# get site name
        #sitename='nms2'
        # set parameter and default values
        sqlalchemy_host = "localhost"
        sqlalchemy_user_name = "root"
        sqlalchemy_password = "root"
        sqlalchemy_schema = "nms_sample"
        sqlalchemy_driver="mysql"

        # config.xml file path
        xml_config_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/config.xml" % sitename
        #xml_config_file = "nms2"
        try:
            # check config.xml file exist or not
            if(os.path.isfile(xml_config_file)):
                dom = xml.dom.minidom.parse(xml_config_file)	# create xml dom object for config.xml file
                mysql_dom = dom.getElementsByTagName("sqlalchemy")
                for m in mysql_dom:
                    sqlalchemy_host = m.getAttribute("hostname")
                    sqlalchemy_user_name = m.getAttribute("username")
                    sqlalchemy_password = m.getAttribute("password")
                    sqlalchemy_schema = m.getAttribute("schema")
                    sqlalchemy_driver=m.getAttribute("driver")
            return sqlalchemy_host ,sqlalchemy_user_name ,sqlalchemy_password ,sqlalchemy_schema,sqlalchemy_driver
        except Exception as e:
            #print sys.exc_info()
            return sqlalchemy_host ,sqlalchemy_user_name ,sqlalchemy_password ,sqlalchemy_schema,sqlalchemy_driver
        
    def sql_alchemy_db_connection_close(self):
        try:
            self.session.close()
            #self.session.bind.dispose()
            self.session.close_all()
            self.db_connect.close()
            
        except Exception as e:
            self.error = 1
        

        
        
sqlalche_obj = SqlAlchemyDBConnection()
def chk_sqlalchemy_connection():
    global sqlalche_obj
    return  sqlalche_obj.error
# Author- Anuj Samariya
#
# This function is used for listing the Devices based on IPaddress,Macaddress,DeviceTy
# selected_device_type - This gives us the selected device type from drop down list e.g. "odu16"
# device_list_state - To make the select list enable or disable e.g for enable = "True" and for disable = "False"
# select_list_id - This is ID and Name of the Select List e.g "device_type" 
#
# return Page Header Search in string format (html) 



############################ Function for Paging##################################################

def data_table_data_sqlalchemy(ip_address,mac_address,device_type,i_display_start,i_display_length,s_search,sEcho,sSortDir_0,iSortCol_0,userid=None,html_var={}): #,

    # Easy set variables
    
    # columns that are shown in data table
    a_columns = []
    

    i_total=0
    i_filtered_total=0
    # table objects 
    table_classes = []
    if device_type=="":
        device_type="odu"
    # table object fields 
    if device_type=="odu100" or device_type=="odu16" or device_type=="odu":
        a_columns = ["host_id","host_alias","hostgroup_name","ip_address","mac_address","ra_mac","device_type_id","reconcile_health","config_profile_id"]
        table_classes = [Hosts,Hostgroups,Hosts,HostAssets,Hosts,HostsHostgroups,HostgroupsGroups,UsersGroups]
        table_columns = [["host_id","host_alias"],
                            ["hostgroup_name"],["ip_address","mac_address"],["ra_mac"],["device_type_id","reconcile_health","config_profile_id","is_deleted"]
                        ,["hostgroup_id","host_id"],["group_id","hostgroup_id"],["user_id","group_id"]]
                        
    elif device_type=='idu4':
        a_columns = ["host_id","host_alias","hostgroup_name","ip_address","mac_address","tdmoipInterfaceMac","hwType","device_type_id","reconcile_health","config_profile_id"]
        table_classes = [Hosts,Hostgroups,Hosts,IduIduInfoTable,Hosts,HostsHostgroups,HostgroupsGroups,UsersGroups]
        table_columns = [["host_id","host_alias"],
                            ["hostgroup_name"],["ip_address","mac_address"],["tdmoipInterfaceMac","hwType"],["device_type_id","reconcile_health","config_profile_id","is_deleted"]
                        ,["hostgroup_id","host_id"],["group_id","hostgroup_id"],["user_id","group_id"]]
    
    else:
        a_columns = ["host_id","host_alias","hostgroup_name","ip_address","mac_address","device_type_id","reconcile_health","config_profile_id","radioAPmode"]
        table_classes = [Hosts,Hostgroups,Hosts,HostsHostgroups,HostgroupsGroups,UsersGroups,Ap25RadioSetup]
        table_columns = [["host_id","host_alias"],
                            ["hostgroup_name"],["ip_address","mac_address","device_type_id","reconcile_health","config_profile_id","is_deleted"]
                        ,["hostgroup_id","host_id"],["group_id","hostgroup_id"],["user_id","group_id"],["radioAPmode"]]
    # if tables are two or more than 2 then define join type [join or outerjoin or user_defined_join or user_defined_outerjoin]
    table_join = [""]

    # other where conditions
    other_conditions = [
        {
            "type":"equal",
            "table_class":Hosts,
            "table_column":"is_deleted",
            "value":"0",
            "rel":"and"
        },
        {
            "type":"equal",
            "table_class":HostAssets,
            "table_column":"host_asset_id",
            "value":Hosts.host_asset_id,
            "rel":"and"
        },
        {
            "type":"equal",
            "table_class":UsersGroups,
            "table_column":"user_id",
            "value":userid,
            "rel":"and"
        },
        {
            "type":"equal",
            "table_class":UsersGroups,
            "table_column":"group_id",
            "value":HostgroupsGroups.group_id,
            "rel":"and"
        },
        {
            "type":"equal",
            "table_class":HostsHostgroups,
            "table_column":"hostgroup_id",
            "value":HostgroupsGroups.hostgroup_id,
            "rel":"and"
        },
        {
            "type":"equal",
            "table_class":Hosts,
            "table_column":"host_id",
            "value":HostsHostgroups.host_id,
            "rel":"and"
        },
        {
            "type":"like",
            "table_class":Hosts,
            "table_column":"ip_address",
            "value":"%%%s%%"%(ip_address),
            "rel":"and"
        },
        {
            "type":"like",
            "table_class":Hosts,
            "table_column":"mac_address",
            "value":"%%%s%%"%(mac_address),
            "rel":"and"
        },
        {
            "type":"like",
            "table_class":Hosts,
            "table_column":"device_type_id",
            "value":"%%%s%%"%(device_type),
            "rel":"and"
        },
        {
            "type":"equal",
            "table_class":Hostgroups,
            "table_column":"hostgroup_id",
            "value":HostgroupsGroups.hostgroup_id,
            "rel":"and"
        }]
        
    if device_type=="idu4":
        other_conditions.append(
        {
            "type":"equal",
            "table_class":IduIduInfoTable,
            "table_column":"host_id",
            "value":Hosts.host_id,
            "rel":"and"
        })
    if device_type=="ap25":
        other_conditions.append(
        {
            "type":"equal",
            "table_class":Ap25RadioSetup,
            "table_column":"config_profile_id",
            "value":Hosts.config_profile_id,
            "rel":"and"
        })
            
            

    
    ##	        device_tuple = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
    ##        filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
    ##        Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
    ##        UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
    ##        .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    # Create Session
    try:
        #Session = sessionmaker(bind=Engine)     # Making session of our current database
        #session = Session()			# Createing session object
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        query_column = []			# Query Column to store query fields
        query = None				# Query object default is null
        for class_i in range(0,len(table_classes)):
            if len(table_columns) > class_i:
                for column_i in range(0,len(table_columns[class_i])):
                    query_column.append(getattr(table_classes[class_i],table_columns[class_i][column_i]))	# append table fileds objects
                
        for class_i in range(0,len(table_classes)):
            if class_i == 0:
                query = sqlalche_obj.session.query(*tuple(query_column))		# creating query to pass the table fields
            elif class_i > 0:
                if len(table_join) > class_i-1:
                    if table_join[class_i-1] == "join":		# creating type of joins in tables
                        query = query.join(getattr(table_classes[class_i-1],table_classes[class_i].__tablename__))
                    elif table_join[class_i-1] == "outerjoin":
                        query = query.outerjoin(getattr(table_classes[class_i-1],table_classes[class_i].__tablename__))
                    elif table_join[class_i-1] == "user_defined_join":
                        if len(join_conditions) > class_i-1:
                            join_conditions_list = []
                            for join_condition in join_conditions[class_i-1]:
                                if isinstance(join_condition,dict):
                                    if isinstance(join_condition.get("join_with",None),str) or isinstance(join_condition.get("join_with",None),int) or isinstance(join_condition.get("join_with",None),long) or isinstance(join_condition.get("join_with",None),float):
                                        join_conditions_list.append(getattr(table_classes[class_i],join_condition["table_column"]) == join_condition["join_with"])
                                    elif isinstance(join_condition.get("join_with",None),dict):
                                        join_conditions_list.append(getattr(table_classes[class_i],join_condition["table_column"]) == getattr(join_condition["join_with"]["table_class"],join_condition["join_with"]["table_column"]))
                                        
                            if len(join_conditions_list) == 0:
                                query = query.join(table_classes[class_i])
                            elif len(join_conditions_list) == 1:
                                query = query.join(table_classes[class_i],join_conditions_list[0])
                            else:
                                query = query.join(table_classes[class_i],and_(*tuple(join_conditions_list)))
                    elif table_join[class_i-1] == "user_defined_outerjoin":
                        if len(join_conditions) > class_i-1:
                            join_conditions_list = []
                            for join_condition in join_conditions[class_i-1]:
                                if isinstance(join_condition,dict):
                                    if isinstance(join_condition.get("join_with",None),str) or isinstance(join_condition.get("join_with",None),int) or isinstance(join_condition.get("join_with",None),long) or isinstance(join_condition.get("join_with",None),float):
                                        join_conditions_list.append(getattr(table_classes[class_i],join_condition["table_column"]) == join_condition["join_with"])
                                    elif isinstance(join_condition.get("join_with",None),dict):
                                        join_conditions_list.append(getattr(table_classes[class_i],join_condition["table_column"]) == getattr(join_condition["join_with"]["table_class"],join_condition["join_with"]["table_column"]))
                                        
                            if len(join_conditions_list) == 0:
                                query = query.outerjoin(table_classes[class_i])
                            elif len(join_conditions_list) == 1:
                                query = query.outerjoin(table_classes[class_i],join_conditions_list[0])
                            else:
                                query = query.outerjoin(table_classes[class_i],and_(*tuple(join_conditions_list)))
                    else:
                        pass
                        #query = query.join(getattr(table_classes[class_i-1],table_classes[class_i].__tablename__))
                else:
                    pass
                    #query = query.join(getattr(table_classes[class_i-1],table_classes[class_i].__tablename__))
        
        
        # other conditions
        or_condition = []
        and_condition = []
        for other_condition in other_conditions:
            if isinstance(other_condition,dict):
                if other_condition.get("type",None) == "like":
                    if other_condition.get("table_class",None) != None and other_condition.get("table_column",None) != None:
                        if other_condition.get("rel",None) == "and":
                            and_condition.append(getattr(other_condition["table_class"],other_condition["table_column"]).like(other_condition.get("value","%%")))
                        else:
                            or_condition.append(getattr(other_condition["table_class"],other_condition["table_column"]).like(other_condition.get("value","%%")))
                    
                elif other_condition.get("type",None) == "equal":
                    if other_condition.get("table_class",None) != None and other_condition.get("table_column",None) != None:
                        if other_condition.get("rel",None) == "and":
                            and_condition.append(getattr(other_condition["table_class"],other_condition["table_column"]) == other_condition.get("value",None))
                        else:
                            or_condition.append(getattr(other_condition["table_class"],other_condition["table_column"]) == other_condition.get("value",None))

                elif other_condition.get("type",None) == "in":
                    if other_condition.get("table_class",None) != None and other_condition.get("table_column",None) != None:
                        if other_condition.get("rel",None) == "and":
                            and_condition.append(getattr(other_condition["table_class"],other_condition["table_column"]).in_(other_condition.get("value",[])))
                        else:
                            or_condition.append(getattr(other_condition["table_class"],other_condition["table_column"]).in_(other_condition.get("value",[])))
                            
                            
        
        if len(and_condition) == 0:
            if len(or_condition) == 0:
                pass
            elif len(or_condition) == 1:
                query = query.filter(or_condition[0])
            else:
                query = query.filter(or_(*tuple(or_condition)))
        elif len(and_condition) == 1:
            if len(or_condition) == 0:
                query = query.filter(and_condition[0])
            elif len(or_condition) == 1:
                query = query.filter(and_(and_condition[0],or_condition[0]))
            else:
                query = query.filter(and_(and_condition[0],or_(*tuple(or_condition))))
        else:
            if len(or_condition) == 0:
                query = query.filter(and_(*tuple(and_condition)))
            elif len(or_condition) == 1:
                query = query.filter(and_(and_(*tuple(and_condition)),or_condition[0]))
            else:
                query = query.filter(and_(and_(*tuple(and_condition)),*tuple(or_condition)))
        
        
        i_total = query.count()			# fetch total number of records
        
                    

        # Filtering
        is_individual_filter=False
        if is_individual_filter == False:
            s_search = s_search
            if s_search != "":
                filter_column = []
                for class_i in range(0,len(table_classes)):	# creating filtring in query
                    if len(table_columns) > class_i:
                        for column_i in range(0,len(table_columns[class_i])):
                            filter_column.append(getattr(table_classes[class_i],table_columns[class_i][column_i]).like("%" + s_search + "%"))
                if len(filter_column) > 0:
                    query = query.filter(or_(*tuple(filter_column)))

        # Ordering
        #i_sort_col_0 = req.vars.get("iSortCol_0",None)
##        if(str(sSortDir_0)=="asc"):
##report_data_list2=sorted(report_data_list, key=lambda report_data_list: report_data_list[int(iSortCol_0)],reverse=False)
##else:
##report_data_list2=sorted(report_data_list, key=lambda report_data_list: report_data_list[int(iSortCol_0)],reverse=True)
#sSortDir_0,iSortCol_0
##        if iSortCol_0 != None and str(iSortCol_0) != "None":
##            if str(sSortDir_0) == "asc":
##                query = query.order_by(asc(getattr(Hosts,a_columns[int(iSortCol_0)])))
##            else:
##                query = query.order_by(desc(getattr(Hosts,a_columns[int(iSortCol_0)])))
            s_order = "ORDER BY  "
            for i in range(0,int(html_var.get("iSortingCols",0))):		# creating orderby in query
                i_sort_col_i = int(html_var.get("iSortCol_%s" % i,-1))+1
                b_sortable_ = html_var.get("bSortable_%s" % i_sort_col_i,None)
                if b_sortable_ == "true":
                    s_sort_dir_i = html_var.get("sSortDir_%s" % i,"asc")
                    for class_i in range(0,len(table_classes)):
                        if len(table_columns) > class_i:
                            for column_i in range(0,len(table_columns[class_i])):
                                if table_columns[class_i][column_i] == a_columns[i_sort_col_i]:
                                    if s_sort_dir_i == "asc":
                                        query = query.order_by(asc(getattr(table_classes[class_i],table_columns[class_i][column_i])))
                                    else:
                                        query = query.order_by(desc(getattr(table_classes[class_i],table_columns[class_i][column_i])))		
        #query = query.order_by(Hosts.host_alias).order_by(Hosts.ip_address)
        i_filtered_total = query.count()		# fetch record count after filtering applied in query
        
        # Paging
        s_limit = ""
        i_display_start = int(i_display_start)#req.vars.get("iDisplayStart",None)
        i_display_length = int(i_display_length)#req.vars.get("iDisplayLength",None)
        if (i_display_start != None and i_display_length != '-1'):	# creating paging in query
            query = query.limit(int(i_display_length)).offset(int(i_display_start))
        
        # ipSelectMacDeviceTypefetch records from database
        r_result = query.all()
        
        result_data = []
        for a_row in r_result:
            row = []
            for i in range(0,len(a_columns)):
                if a_columns[i] == "city":
                    # Special output formatting for 'city' column
                    row.append(a_row[i] == "Ajmer" and a_row[i] + "(H)" or a_row[i])
                    
                elif a_columns[i] == "subject_name":
                    # Special output formatting for 'subject_name' column
                    row.append(a_row[i] == None and "NA" or a_row[i])
                    
                elif a_columns[i] != " ":
                    row.append(a_row[i])
            result_data.append(row)

        # Output
        output = {
            "sEcho": int(sEcho),
            "iTotalRecords": i_total,
            "iTotalDisplayRecords": i_filtered_total,
            "aaData":result_data,
            "query":str(query),
            "i_display_start": i_display_start,
            "device_type":device_type
        }
        
        #sqlalche_obj.close()

        # Encode Data into JSON
        #req.write(JSONEncoder().encode(output))
        sqlalche_obj.sql_alchemy_db_connection_close()
        return output
                                        
    except Exception,e:
        output = {
            "sEcho": int(sEcho),
            "iTotalRecords": i_total,
            "iTotalDisplayRecords": i_filtered_total,
            "aaData":[],
            "i_display_start": i_display_start,
            "query":str(e)
        }
        return output
##########################################################################
def page_header_search(ip_address,mac_address,device_types=None,selected_device_type=None,device_list_state="enabled",select_list_id="device_type",extra_tag_element_list=[]):
    """
    This function is used for listing the Devices based on IPaddress,Macaddress,DeviceTypes
    """
#   and extra_tag_element['click']==''\
#   and extra_tag_element['class']==''
    header_search_html = ""
    extra_tag_element_html=""
    if len(extra_tag_element_list)>0:
        for extra_tag_element in extra_tag_element_list:
            if extra_tag_element.get('id',None)!=None\
              and extra_tag_element.get('name',None)!=None\
              and extra_tag_element.get('value',None)!=None\
              and extra_tag_element.get('tag',None)!=None:
                extra_tag_element_html+="<input type='%(tag)s' id='%(id)s' name='%(name)s' value='%(value)s' class=\"yo-small yo-button\" style=\" margin-top: 2px;\">"% extra_tag_element

    header_search_html+="<div id=\"filterOptions\" style=\"position:relative;\">\
                            <div class=\"ipFilter\">IP : \
                                <input type=\"text\" name=\"filter_ip\" id=\"filter_ip\" style=\"width:140px;margin-left:10px;\" value=\"%s\"/>\
                            </div>\
                            <div  class=\"ipFilter\"> MAC:\
                                <input type=\"text\" name=\"filter_mac\" id=\"filter_mac\" style=\"width:140px;margin-left:10px;\" value=\"%s\"/>\
                            </div>\
                            <div  class=\"ipFilter\"  id=\"filterDeviceType\" > Device Type : \
                            %s\
                            </div>\
                            <div>\
                                <input type=\"button\"  id=\"btnSearch\" name=\"btnSearch\" value=\"Search\" class=\"yo-small yo-button\" style=\"margin-top: 2px;\"/>\
                                %s\
                            </div>\
                        </div>\
                        <div id=\"hide_search\" style=\"position: static; top: 1px; right: 1px; display: block; background-color: rgb(241, 241, 241); height: 20px; overflow: hidden; width: 100%%; z-index: 1000;\">\
                            <label class=\"lbl\" style=\"margin-left:10px;margin-top:5px;\"><b>Global Search</b></label>\
                            <span class=\"up\" style=\"height: 16px; width: 16px; display: block; float: right;margin:2px 10px;cursor:pointer;\"></span>\
                        </div>"%(ip_address,mac_address,device_type_select_list(device_types,selected_device_type,device_list_state,select_list_id),extra_tag_element_html)
                            
    
    return header_search_html
# Author- Anuj Samariya
#
# This function is used for creating the Select List Of Devices based on Devie Types,Selected Device Type,Device List State,Select List Id
#
# device_types - This is the list of device types which will show in drop down list e.g "odu16,odu100"
# selected_device_type - This gives us the selected device type from drop down list e.g. "odu16"
# device_list_state - To make the select list enable or disable e.g for enable = "True" and for disable = "False"
# select_list_id - This is ID and Name of the Select List e.g "device_type" 
#
# return SelectListHtml in string format (html)
def device_type_select_list(device_types=None,selected_device_type=None,device_list_state="enabled",select_list_id="device_type"):
    connection_chk = chk_sqlalchemy_connection()
    device_select=''
    if connection_chk == 0 or connection_chk == "0":
        global sqlalche_obj
        try:
        
            sqlalche_obj.sql_alchemy_db_connection_open()
            
            select_list_html = ""
            if device_list_state=="enabled":
                select_list_html+="<select id=\"%s\" name=\"select_device_list\">"%(select_list_id)
            else:
                select_list_html+="<select id=\"%s\" name=\"%s\" disabled=\"disabled\">"%(select_list_id,select_list_id)
            select_list_html+="<option value=\"\">-- Select Device --</option>"
            if device_types==None or device_types=="":
                device_list=sqlalche_obj.session.query(DeviceType.device_type_id,DeviceType.device_name).filter(DeviceType.is_deleted==0).order_by(DeviceType.sequence).all()
                for i in range(0,len(device_list)):
                    if device_list[i].device_type_id==selected_device_type:
                        device_select = device_list[i].device_type_id
                        select_list_html+="<option value=\"%s\" selected=\"selected\">%s</option>\
                        "%(device_list[i].device_type_id,device_list[i].device_name)
                    else:
                        select_list_html+="<option value=\"%s\" >%s</option>"%(device_list[i].device_type_id,device_list[i].device_name)
            
            else:
                selected_device_list=device_types.split(",")
                device_list=sqlalche_obj.session.query(DeviceType.device_type_id,DeviceType.device_name).filter(DeviceType.is_deleted==0).order_by(DeviceType.sequence).all()
                for i in range(0,len(device_list)):
                    if device_list[i].device_name in selected_device_list:
                        if device_list[i].device_type_id==selected_device_type:
                            device_select = device_list[i].device_type_id
                            select_list_html+="<option value=\"%s\" selected=\"selected\">%s</option>"%(device_list[i].device_type_id,device_list[i].device_name)
                        else:
                            select_list_html+="<option value=\"%s\">%s</option>"%(device_list[i].device_type_id,device_list[i].device_name)
                    else:
                        continue
            select_list_html+="</select>"
            select_list_html+="<input type=\"hidden\" value=\"%s\" name=\"device_select\"/>"%(device_select)
            sqlalche_obj.sql_alchemy_db_connection_close()
            return select_list_html
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
    else:
        select_list_html = ""
        select_list_html+="<select id=\"%s\" name=\"select_device_list\">"%(select_list_id)
        select_list_html+="<option value=\"\">-- Select Device --</option>"
        select_list_html+="</select>"
        return str("There is Some Problem with DataBase.Please Contact Your Administrator")


def make_select_list_using_dictionary(select_param_dic,selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg,attr={}):
    try:
        select_list_html=""
        attr_html = ""
        for attr_key in attr:
            attr_html+=attr_key+"='"+attr[attr_key]+"' "
        if select_list_state == "enabled":
            select_list_html+="<select id=\"%s\" name=\"%s\" %s>"%(select_list_id,select_list_id,attr_html)
        else:
            select_list_html+="<select id=\"%s\" name=\"%s\" disabled=\"disabled\" %s>"%(select_list_id,select_list_id,attr_html)
        
        select_list_html+="<option value=\"\">-- Select %s --</option>"%(select_list_initial_msg)
        for i in range(len(select_param_dic["value"])):
            if select_param_dic["value"][i]== selected_field:
                select_list_html+="<option value=\"%s\" selected=\"selected\">%s</option>"%(select_param_dic["value"][i],select_param_dic["name"][i])
            else:
                select_list_html+="<option value=\"%s\">%s</option>"%(select_param_dic["value"][i],select_param_dic["name"][i])
        select_list_html+="</select>"
        return str(select_list_html)
    except Exception as e:
        return str(e)

class IpMacSearch(object):
    global sqlalche_obj
    def ip_search(self,device_type,search_value,userid,ip_mac_search):
       #pass
        sqlalche_obj.sql_alchemy_db_connection_open()
        ip_mac_list = []
        ip_mac_list = sqlalche_obj.session.query(Hosts.ip_address if int(ip_mac_search)==1 else Hosts.mac_address).filter(and_(Hosts.is_deleted == 0,\
        Hosts.ip_address.like('%s%%'%(search_value)) if int(ip_mac_search)==1 else Hosts.mac_address.like('%s%%'%(search_value))\
            ,Hosts.device_type_id!='unknown',Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
            UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
            .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return ip_mac_list    
    
    def get_ip_mac_selected_device(self,selected_val,ip_mac_val):
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            ip_mac_list = []
            ip_mac_dic = {'ip_address': "",'mac_address':"",'error':"","success":0}
            
            ip_mac_list = sqlalche_obj.session.query(Hosts.mac_address if int(ip_mac_val)==1 else Hosts.ip_address,Hosts.device_type_id).\
                            filter(Hosts.ip_address==selected_val if int(ip_mac_val)==1 else Hosts.mac_address==selected_val).all()
            sqlalche_obj.sql_alchemy_db_connection_close()
            if len(ip_mac_list)!=[]:
                if int(ip_mac_val)==1:
                    ip_mac_dic['mac_address'] = ip_mac_list[0].mac_address
                else:
                    ip_mac_dic['ip_address'] = ip_mac_list[0].ip_address
                ip_mac_dic['selected_device'] = ip_mac_list[0].device_type_id
                    
            return ip_mac_dic    
        except Exception as e:
            ip_mac_dic['success']=1 
            ip_mac_dic['error'] = str(e)
            sqlalche_obj.sql_alchemy_db_connection_close()
            return ip_mac_dic
    
##obj = IpMacSearch()
#####print ip_search('odu','FF:FF:FF:FF:FF','613b6eba-53b3-11e1-87af-e069956899a4',0)
##print obj.get_ip_mac_selected_device('172.22.0.104',1)
class MakeSelectListUsingDictionary(object):
    @staticmethod
    def make_select_list_using_dictionary(select_param_dic,selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg):
        try:
            select_list_html=""
            if select_list_state == "enabled":
                select_list_html+="<select id=\"%s\" name=\"%s\">"%(select_list_id,select_list_id)
            else:
                select_list_html+="<select id=\"%s\" name=\"%s\" disabled=\"disabled\">"%(select_list_id,select_list_id)
            select_list_html+="<option value=\"\">-- Select %s --</option>"%(select_list_initial_msg)
            for i in range(len(select_param_dic["value"])):
                if select_param_dic["value"][i]== selected_field:
                    select_list_html+="<option value=\"%s\" selected=\"selected\">%s</option>"%(select_param_dic["value"][i],select_param_dic["name"][i])
                else:
                    select_list_html+="<option value=\"%s\">%s</option>"%(select_param_dic["value"][i],select_param_dic["name"][i])
            select_list_html+="</select>"
            return str(select_list_html)
        except Exception as e:
            return str(e)
            

# Author- Rajendra Sharma
#
# This function is used for creating the Select List Of any Table on Table Name value Field Name,Display Field Name,Selected Field ,Select List Id,Select List Initial Msg
#
#
# return SelectListHtml in string format (html)

#Exception class for own created exception.
class SelfException(Exception):
	"""
	@return: this class return the exception msg.
	@rtype: dictionary
	@requires: Exception class package(module)
	@author: Rajendra Sharma
	@since: 20 sept 2011
	@version: 0.1
	@date: 18 sept 2011
	@organisation: Code Scape Consultants Pvt. Ltd.
	@copyright: 2011 Code Scape Consultants Pvt. Ltd.
	"""
	def __init__(self,msg):
		return 1


def make_select_list(table_name="",value_field_name="",display_field_name="",selected_field="",select_list_state="enabled",select_list_id="",is_readonly="false",select_list_initial_msg=""):
    try:

        db,cursor=mysql_connection('nms_sample')
        if db ==1:
            raise SelfException(cursor)
            select_list_html=""
            if select_list_state == "enabled":
                select_list_html+="<select id=\"%s\" name=\"%s\">"%(select_list_id,select_list_id)
            else:
                select_list_html+="<select id=\"%s\" name=\"%s\" disabled=\"disabled\">"%(select_list_id,select_list_id)
            select_list_html+="<option value=\"\">-- Select %s --</option>"%(display_field_name)
        if table_name=="groups":
            sql="SELECT group_id,group_name FROM groups"
            cursor.execute(sql)
            result=cursor.fetchall()
            for row in result:
                if row[1] == selected_field:
                    select_list_html+="<option value=\"%s\" selected=\"selected\">%s</option>"%(row[1],row[1])
                else:
                    select_list_html+="<option value=\"%s\" >%s</option>"%(row[1],row[1])
        else:
            sql="SELECT "+value_field_name+","+display_field_name+" FROM "+table_name
            cursor.execute(sql)
            result=cursor.fetchall()
            for row in result:
                if row[0] == selected_field:
                    select_list_html+="<option value=\"%s\" selected=\"selected\">%s</option>"%(row[0],row[1])
                else:
                    select_list_html+="<option value=\"%s\" >%s</option>"%(row[0],row[1])
        # close the database and cursor connection
        cursor.close()
        db.close()
        select_list_html+="</select>"
        return select_list_html
    except MySQldb as e:
        return e
    except Exception as e:
        return e
    except SelfException as e:
        return e
            




def make_group_select_list(selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg):
	return make_select_list("groups","group_id","group_name",selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg)


def make_alarm_field_select_list(selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg):
	return make_select_list("trap_alarm_field_table","trap_alarm_field","field_name",selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg)	


def make_action_table_select_list(selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg):
    return make_select_list("actions","action_id","action_name",selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg)


def make_acknowledge_table_select_list(selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg):
	return make_select_list("acknowledge","acknowledge_id","acknowledge_name",selected_field,select_list_state,select_list_id,is_readonly,select_list_initial_msg)



# Import modules that contain the function and libraries
from nagios_livestatus import Nagios

def tactical_overview(h):
    '''
    @author: Yogesh Kumar
    @param h: html object [request object]
    @var html: global html object
    @note: this function call tactical overview function which gives status overview. 
    '''
    global html
    html = h
    html.write(str(Nagios.tactical_overview(html)))


def unmp_help(h):
    global html
    html = h
    css_list = []
    js_list = []
    header_btn = ""
    html.new_header("Help","help.py",header_btn,css_list,js_list)
    html.write("<p style=\"margin:10px;\">Contact Your Administrator.</p>")
    html.new_footer()
    

def localhost_dashboard(h):
    global html
    html = h
    css_list = []
    js_list = ["js/highcharts.js","js/pages/local_system_dashboard.js"]
    header_btn = ""
    html.new_header("UNMP System Dashboard","",header_btn,css_list,js_list)
    html.write(LocalSystem.localhost_dashboard_table())
    html.new_footer()

def system_uptime(h):
    global html
    html = h
    ls = LocalSystemBll()
    html.write(str(ls.system_uptime()))

def system_ram(h):
    global html
    html = h
    ls = LocalSystemBll()
    html.write(str(ls.ram_details()))
    
def system_harddisk_details(h):
    global html
    html = h
    ls = LocalSystemBll()
    html.write(str(ls.harddisk_details()))
    
def system_processor_details(h):
    global html
    html = h
    total = html.var("total")
    total = total != None and total or 1
    ls = LocalSystemBll()
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(ls.processor_details(int(total))))

def system_bandwidth_details(h):
    global html
    html = h
    total = html.var("total")
    total = total != None and total or 1
    ls = LocalSystemBll()
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(ls.bandwidth_details(int(total))))

def common_ip_mac_search(h):
    #pass
    global html
    html = h
    obj = IpMacSearch()
    ip_mac_list = []
    final_result = {}
    search_value  = html.var("s")
    total_records = html.var("totalRecord")
    #device_type = html.var("device_type")
##    if device_type == "None":
##        device_type == ""
    device_type = ""
    user_id =  html.req.session['user_id']
    ip_mac_search = html.var("ip_mac_search")
    result = obj.ip_search(device_type,search_value,user_id,ip_mac_search)
    if len(result)!=[]:
        for i in range(0,len(result)):
            ip_mac_list.append({'Name':result[i][0],'Hidden':""})
    final_result = {'items':ip_mac_list}
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(final_result)))

def get_ip_mac_selected_device(h):
    global html
    obj = IpMacSearch()
    html = h
    result = {}
    selected_val = html.var('selected_val')
    ip_mac_val = html.var('ip_mac_val')
    result = obj.get_ip_mac_selected_device(selected_val,ip_mac_val)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))

class TrapStatus(object):
    
    def trap_alarm_chk(self,host_id,device_type):
        trap_final_dic = {'success':0,'result':{}}
        try:
            global sqlalchemy
            sqlalche_obj.sql_alchemy_db_connection_open()
            trap_alarm_dic = {}
            severity = ""
            host_detail_list = sqlalche_obj.session.query(Hosts.ip_address).filter(Hosts.host_id==host_id).all()
            trap_alram_list = sqlalche_obj.session.query(TrapAlarms.trap_event_type,TrapAlarms.serevity,TrapAlarms.timestamp).filter(TrapAlarms.agent_id == host_detail_list[0].ip_address if len(host_detail_list)>0 else TrapAlarms.agent_id ==0 ).order_by(desc(TrapAlarms.timestamp)).limit(5).all()
            if len(trap_alram_list)>0:
                for i in range(0,len(trap_alram_list)):
                    if int(trap_alram_list[i].serevity) == 0 or int(trap_alram_list[i].serevity) == 2:
                        severity = "Normal"
                    elif int(trap_alram_list[i].serevity) == 1:
                        severity = "Informational"
                    elif int(trap_alram_list[i].serevity) == 3:
                        severity = "Minor"
                    elif int(trap_alram_list[i].serevity) == 4:
                        severity = "Major"
                    elif int(trap_alram_list[i].serevity) == 5:
                        severity = "Major"
                    trap_alarm_dic.update({'%s'%(i+1):{'event_type':trap_alram_list[i].trap_event_type,'Serevity':severity,'intime':datetime.strftime(trap_alram_list[i].timestamp,"%d-%b-%Y %A %I:%M:%S %p")}})
                trap_final_dic['result']=trap_alarm_dic
            else:
                trap_final_dic['success']=1
                trap_final_dic['result'] = "No Data Available"
            sqlalche_obj.sql_alchemy_db_connection_close()
        except Exception,e:
            trap_final_dic['success']=1
            trap_final_dic['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return trap_final_dic
        
def show_trap_alarms(h):
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    ip_address = html.var("ip_address")
    obj = TrapStatus()
    #{'result': {'1': {'intime': '05-Apr-2012 Thursday 02:36:08 PM', 'event_type': 'FLASH_COMMITED', 'Serevity': 'Informational'}, \
    #'3': {'intime': '03-Apr-2012 Tuesday 04:51:04 PM', 'event_type': 'LINK_UP', 'Serevity': 'Informational'}, 
    #'2': {'intime': '03-Apr-2012 Tuesday 04:57:51 PM', 'event_type': 'FLASH_COMMITED', 'Serevity': 'Informational'}, 
    #'5': {'intime': '03-Apr-2012 Tuesday 04:51:04 PM', 'event_type': 'SYNC_LOSS_THRESHOLD_EXCEEDED', 'Serevity': 'Normal'}, 
    #'4': {'intime': '03-Apr-2012 Tuesday 04:51:04 PM', 'event_type': 'SYNC_LOSS_THRESHOLD_EXCEEDED', 'Serevity': 'Normal'}}, 'success': 0}
    result_dic = obj.trap_alarm_chk(host_id,device_type)
    html_str = ""   
    html_str+="<table class=\"display yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"  
    html_str+="<th>Event Type</th><th>Serevity</th><th>Time</th>"
    if int(result_dic['success'])==0:
        for i in result_dic['result']:
            html_str+="<tr>"
            html_str+="<td>%s</td><td>%s</td><td>%s</td>"%("-" if result_dic['result'][i]['event_type']==None else result_dic['result'][i]['event_type'],\
                                                    "-" if result_dic['result'][i]['Serevity']==None else result_dic['result'][i]['Serevity'],\
                                                    "-" if result_dic['result'][i]['intime']==None else result_dic['result'][i]['intime'])
                                                    
            html_str+="</tr>"
        html_str+="<tr><td colspan=3><a id=\"more_trap\" href=\"status_snmptt.py?ip_address=%s-\">More</a></td></tr>"%(ip_address)
    else:
        html_str+="<tr><td colspan=3>%s</td></tr>"%(result_dic['result'])
    html_str+="</table>"
    html.write(html_str)
#make_alarm_field_select_list('agent_id',"enabled","trap_alarm_field",False,"trap field")


class DeviceStatus(object):
    def device_status(self,host_id):
        host_status_dic = {}
        host_data = []
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_id == "" or host_id == None or host_id == 'undefined':
                result = {"success":1,"result":"No Host Exist"}
            else:
                status_data = sqlalche_obj.db.execute("SELECT trap_event_id,host_id,timestamp FROM (SELECT * FROM  system_alarm_table WHERE host_id IN (%s)ORDER BY TIMESTAMP DESC) AS t GROUP BY host_id"%(host_id))
                host_ids = host_id.split(",")
                host_data_list = sorted(host_ids)
                host_status_dic = {}
                for row in status_data:
                    host_data = []
                    host_data.append(1) if int(row['trap_event_id'])==50001 else host_data.append(0)
                    host_data.append(str(datetime.strftime(row['timestamp'],"%d-%b-%Y %a %I:%M:%S %p")))
                    host_status_dic[row['host_id']] = host_data
                for i in range(0,len(host_data_list)):
                    host_data = []
                    if int(host_data_list[i]) in host_status_dic:
                        pass
                    else:
                        host_list_data = sqlalche_obj.session.query(Hosts.timestamp).filter(Hosts.host_id==host_data_list[i]).all()
                        host_data.append(0)
                        host_data.append(str(datetime.strftime(host_list_data[0].timestamp,"%d-%b-%Y %a %I:%M:%S %p")) if len(host_data)>0 else str(datetime.strftime(datetime.now(),"%d-%b-%Y %A %I:%M:%S %p")))
                        host_status_dic[host_data_list[i]] = host_data
                
                result = {'success':0,'result':host_status_dic}
        except Exception as e:
            result = {"success":1,"result":str(e)} 
            
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result
        #{"result": {"7": 1, "6": 0}, "success": 0}
    def common_list_device_status(self,host_id):
        try:
            global sqlalchemy
            
            sqlalche_obj.sql_alchemy_db_connection_open()
            snmp_up_down_time = ""
            timer_val = datetime.strftime(datetime.now(),"%d-%b-%Y %a %I:%M:%S %p")
            if host_id == "" or host_id == None or host_id == 'undefined':
                result = {"success":1,"result":{'device_status':["Device Unreachable since "+str(timer_val),"images/temp/red_dot.png"]}}
            else:
                snmp_up_time_data = sqlalche_obj.db.execute("select trap_event_id,timestamp from system_alarm_table where host_id='%s' order by timestamp desc limit 1"%(host_id))
                
                for row in snmp_up_time_data:
                    snmp_up_down_time = row['trap_event_id']
                    timer_val = datetime.strftime(row['timestamp'],"%d-%b-%Y %A %I:%M:%S %p")
                if snmp_up_down_time=="":
                    device_status = "Device Reachable"
                    device_status_image_path = "images/temp/green_dot.png"
                elif int(snmp_up_down_time) == 50001:
                    device_status = "Device Unreachable since"+str(timer_val)
                    device_status_image_path = "images/temp/red_dot.png"
                else:
                    device_status = "Device Reachable"
                    device_status_image_path = "images/temp/green_dot.png"
                result = {"success":1,"result":{'device_status':[device_status,device_status_image_path]}}
        except Exception as e:
            result = {"success":1,"result":{'device_status':[str(e),"images/temp/red_dot.png"]}}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result
    
##obj = DeviceStatus()
##print obj.common_list_device_status(79)
def device_status(h):
    global html
    html = h
    host_id = html.var("host_id")
    obj_device_status = DeviceStatus()
    result = obj_device_status.device_status(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))
          
##obj = TrapStatus()
##print obj.trap_alarm_chk(69,'odu100')
