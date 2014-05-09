#!/usr/bin/python2.6

from unmp_model import *
from utility import ErrorMessages,Validation,UNMPDeviceType
from unmp_config import SystemConfig
from sqlalchemy import and_,or_,desc,asc
from common_controller import *
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *
from pysnmp_ap import *
from py_module import snmp_ping
from common_bll import EventLog
from datetime import datetime
from unmp_config import SystemConfig
import time

errorStatus = {
               1:'tooBig',
               2:'No Such Name',
               3:'Bbad Value',
               4:'readOnly',
               5:'General Error',
               6:'noAccess',
               7:'Wrong Type',
               8:'wrongLength',
               9:'wrongEncoding',
               '10':'Wrong Value Entered',
               11:'No Oid Available',
               12:'inconsistentValue',
               13:'resourceUnavailable',
               14:'Commit Failed',
               15:'undoFailed',
               16:'Authorization Error',
               17:'notWritable',
               18:'Inconsistent Name',
               50:'System Error Occured',
               51:'Network is Unreachable',
               52:'typeError',
               53:'Request Timeout.Please Wait and Retry Again',
               54:'0active_state_notAble_to_lock',
               55:'1active_state_notAble_to_Unlock',
               96:'Arguments_are_not_proper',
               97:'ip port community not passes Correctly',
               98:'otherException',
               99:'pysnmpException'}


class DeviceParameters(object):
    
    def get_device_parameter(self,host_id):
        global sqlalche_obj
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            device_list_param=[]
            device_list_param = sqlalche_obj.session.query(Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.config_profile_id).filter(Hosts.host_id == host_id).all() 
            if device_list_param == None:
                device_list_param = []
            return device_list_param
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            
    

class APDeviceList(object):
    
    def ap_device_list(self,ip_address,mac_address,selected_device,i_display_start,i_display_length,s_search,sEcho,sSortDir_0,iSortCol_0,userid = None,html_req={}): 
        """
        Author- Anuj Samariya
        This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
        ip_address - This is the IP Address of device e.g 192.168.0.1
        mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
        selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
        return List of Devices in two dimensional list format 
        """
        device_dict = {}
        #try block starts
        try:
            device_dict = data_table_data_sqlalchemy(ip_address,mac_address,selected_device,i_display_start,i_display_length,s_search,sEcho,sSortDir_0,iSortCol_0,userid,html_req)
            #here we create the session of sqlalchemy 
            
            #this is the query which returns the multidimensional array of hosts table and store in device_list
##            device_list = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health).\
##            filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
##            Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(selected_device)),UsersGroups.user_id=='%s'%(userid),\
##            UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
##            .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
            return device_dict
        #try block ends
        
        #exception starts
        except Exception as e:
            output2 = {
            "sEcho": 1,
            "iTotalRecords": 10,
            "iTotalDisplayRecords": 10,
            "aaData":[],
            "query":str(e)
            }
            return output2
    
    def ap_device_list_profiling(self,ip_address,mac_address,selected_device):
        global sqlalche_obj
        device_list=[]
        device_type = selected_device
        device_list_state = "enabled"
        #try block starts
        try:
            #here we create the session of sqlalchemy 
            sqlalche_obj.sql_alchemy_db_connection_open()
            #this is the query which returns the multidimensional array of hosts table and store in device_tuple
            device_list = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address).filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
            Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id==device_type)).order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
            return device_list
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

class APCommitToFlash(object):

    def commit_to_flash(self,host_id):
        global sqlalche_obj
        result = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        oid_dict = {}
        i = 0
        oid_dict[1] = ['1.3.6.1.4.1.26149.10.5.1.0','Integer32',1]
        host_param = sqlalche_obj.session.query(Hosts.ip_address,Hosts.snmp_port,Hosts.snmp_write_community,Hosts.snmp_read_community).filter(Hosts.host_id==host_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(host_param)>0:
            result = single_set(host_param[0].ip_address,int(host_param[0].snmp_port),host_param[0].snmp_write_community,oid_dict[1])
            if result["success"]==0:
                oid_dict[2] =  ['1.3.6.1.4.1.26149.10.5.3.0','Integer32',1]
                result = single_set(host_param[0].ip_address,int(host_param[0].snmp_port),host_param[0].snmp_write_community,oid_dict[2])
                if result["success"]==0:
                    time.sleep(40)
                    while(i<5):
                        get_result = pysnmp_get('1.3.6.1.4.1.26149.10.5.3.0',host_param[0].ip_address,int(host_param[0].snmp_port),'public')
                        if get_result["success"]==0:
                            result = {"success":0,"result":"Configuration data saved permanently in the device"}
                            return result
                        else:
                            for k in get_result["result"]:
                                if k != 53 and k != '53':                                    
                                    if errorStatus.has_key(k):
                                        result = {"success":1,"result":errorStatus[k]}
                                        return result
                                elif k == 51 and k == '51':                                
                                    if errorStatus.has_key(k):
                                        result = {"success":1,"result":errorStatus[k]}
                                        return result
                                else:
                                    i = i+1
                                    time.sleep(10)
                    result = {'success':1,'result':'Device is Not Responding'}
                    return result
                else:
                    for k in result["result"]:
                        if errorStatus.has_key(k):
                            result = {"success":1,"result":errorStatus[k]}
                            return result
            else:
                for k in result["result"]:
                    if errorStatus.has_key(k):
                        result = {"success":1,"result":errorStatus[k]}
                        return result
        else:
            return {"success":1,"result":"Host Data Not Exist"}
    
    
        
        
def rename_tablename(tablename):
    try:
        ss=""
        idx = tablename.index("_")
        ss = tablename[0:idx] + tablename[idx+1].upper() + tablename[idx+1+1:]
        ss=ss[0].upper() + ss[1:]
        return ss
    except Exception as e:
        return e
    
class Reconciliation(object):
    
    def update_configuration(self,host_id,device_type_id):
        host_param = []
        global errorStatus
        global sqlalche_obj
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            obj_system_config = SystemConfig()
            table_prefix = "ap25_"
            total_table = 11
            rec = 1
            total_per = 0
            column_list = []
            host_param = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id == host_id).all()
            config_profile_id = host_param[0].config_profile_id
            if len(host_param)>0:
                snmp_ping_result = snmp_ping(host_param[0].ip_address,host_param[0].snmp_read_community,int(host_param[0].snmp_port))
                if int(snmp_ping_result)==0:
                    host_param[0].reconcile_status = 1
                    sqlalche_obj.session.commit()
                    database_name = obj_system_config.get_sqlalchemy_credentials()
                    result = vapsetup_ap(str(host_param[0].ip_address),int(host_param[0].snmp_port))
                    if result["success"]==0:
                        rec = rec + 1
                        vap_selection = sqlalche_obj.session.query(Ap25VapSelection).filter(Ap25VapSelection.config_profile_id == config_profile_id).all()
                        if len(result["result"]["vap"])==2:
                            for i in range(0,len(vap_selection)):
                                vap_selection[i].totalVAPsPresent = result["result"]["vap"][0]
                                vap_selection[i].selectVap = result["result"]["vap"][1]
                                sqlalche_obj.session.flush()
                        vap_tables = ['ap25_basicVAPsetup','ap25_basicVAPsecurity','ap25_vapWPAsecuritySetup','ap25_basicACLsetup','ap25_aclMacTable']
                        for i in result["result"]["data"]:
                            
                            for j in range(0,len(result["result"]["data"][i])):
                                
                                
                                column_list = []
                                result_db  = sqlalche_obj.db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'"%(vap_tables[j],database_name[4]))
                                for row in result_db:
                                    column_list.append(row["column_name"])
                                
                                primary_key = vap_tables[j]+"_id"
                                column_list.remove(primary_key)
                                column_list.remove('config_profile_id')
                                
                                if 'vapselection_id' in column_list:
                                    column_list.remove('vapselection_id')
                                sql_alche_table_name = rename_tablename(vap_tables[j])    
                                if vap_tables[j]=="ap25_aclMacTable":
                                    table_result = sqlalche_obj.session.query(eval('%s'%(sql_alche_table_name))).filter(and_(eval('%s'%(sql_alche_table_name)).\
                                                    config_profile_id=='%s'%(config_profile_id),(eval('%s'%(sql_alche_table_name)).vapselection_id=='%s'%(vap_selection[i].ap25_vapSelection_id)))).all()
                                    sqlalche_obj.db.execute("delete from %s where config_profile_id='%s' and vapselection_id='%s'"%(vap_tables[j],config_profile_id,vap_selection[i].ap25_vapSelection_id))
                                    sqlalche_obj.session.commit()
                                    table_result = sqlalche_obj.session.query(eval('%s'%(sql_alche_table_name))).filter(and_(eval('%s'%(sql_alche_table_name)).\
                                                    config_profile_id=='%s'%(config_profile_id),(eval('%s'%(sql_alche_table_name)).vapselection_id=='%s'%(vap_selection[i].ap25_vapSelection_id)))).all()
                                else:    
                                    table_result = sqlalche_obj.session.query(eval('%s'%(sql_alche_table_name))).filter(eval('%s'%(sql_alche_table_name)).config_profile_id=='%s'%(config_profile_id)).all()
                                    
                                if len(table_result)>0:
                                    
                                    
                                    if len(result["result"]["data"][i][j])>0:
                                        
                                        for k in range(0,len(result["result"]["data"][i][j])):
                                            exec "table_result[%s].%s = '%s'"%(i-1,column_list[k],result["result"]["data"][i][j][k])
                                else:
                                    if vap_tables[j] == "ap25_aclMacTable":
                                        if len(result["result"]["data"][i][j])>0:
                                            for k in range(0,len(result["result"]["data"][i][j])):
                                                sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s,%s)"%(vap_tables[j],config_profile_id,vap_selection[i].ap25_vapSelection_id,str(result["result"]["data"][i][j][k])[1:-1]))
                                time.sleep(2)
                    else:
                        if rec>0:
                            rec = rec - 1   
                    node_tables = sqlalche_obj.session.query(Ap25OidTable.table_name,Ap25OidTable.table_oid,Ap25OidTable.isNode).filter(Ap25OidTable.isVap==1).all()                
                    for i in range(0,len(node_tables)):
##                        if node_tables[i][0]=='versions':
##                            continue
                        column_list=[]
                        
                        tablename = table_prefix + node_tables[i][0]
                        result_db  = sqlalche_obj.db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'"%(tablename,database_name[4]))
                        for row in result_db:
                            column_list.append(row["column_name"])
                        
                        if (node_tables[i][2]==0):
                            result = pysnmp_get_node(node_tables[i][1],host_param[0].ip_address,int(host_param[0].snmp_port),host_param[0].snmp_read_community)
                        else:
                            result = pysnmp_get_table(node_tables[i][1],host_param[0].ip_address,int(host_param[0].snmp_port),host_param[0].snmp_read_community)
                        
                        if result["success"]==0:
                            rec=rec+1
                            sqlalche_table_name = rename_tablename(tablename)
                            primary_key = tablename+"_id"
                            if 'config_profile_id' in column_list:
                                config_id = 0
                                table_result = sqlalche_obj.session.query(eval('%s'%(sqlalche_table_name))).filter(eval('%s'%(sqlalche_table_name)).config_profile_id=='%s'%(config_profile_id)).all()
                                
                            else:
                                config_id = 1
                                table_result = sqlalche_obj.session.query(eval('%s'%(sqlalche_table_name))).filter(eval('%s'%(sqlalche_table_name)).host_id=='%s'%(host_id)).all()                           
                            
                            if len(result["result"])>0:
                                if len(table_result)>0:
                                    column_list.remove(primary_key)
                                    if config_id == 0:
                                        column_list.remove('config_profile_id')
                                        for i in result["result"]:
                                            for k in range(0,len(column_list)):
                                                temp_result = str(result["result"][i][k])
                                                
                                                exec "table_result[%s].%s = '%s'"%(i-1,column_list[k],temp_result[:-1] if temp_result.count('\n') else temp_result)
                                                
                                    else:
                                        column_list.remove('host_id')
                                        for i in result["result"]:
                                            for k in range(0,len(column_list)):                                        
                                                temp_result = str(result["result"][i][k])
                                                
                                                exec "table_result[%s].%s = '%s'"%(i-1,column_list[k],temp_result[:-1] if temp_result.count('\n') else temp_result)
                                else:
                                    for i in range(0,len(result["result"])):
                                        if config_id == 0:
                                            sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%(tablename,config_profile_id,str(result["result"][i+1])[1:-1]))
                                        else:
                                            
                                            sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%(tablename,host_id,str(result["result"][i+1])[1:-1]))
                        else:
                            if rec>0:
                                rec = rec - 1
                        #sqlalche_obj.db.execute("insert into ap25_versions values(NULL,%s,'%s','%s','%s')"%(host_id,'Rev.b','','0.0.5'))
                        sqlalche_obj.session.commit()
                    total_per = float(rec)/float(total_table)
                    total_per = int(total_per*100)
                    host_param[0].reconcile_status = 2
                    host_param[0].reconcile_health = total_per
                    sqlalche_obj.session.commit()
                    time.sleep(1)
                    host_param[0].reconcile_status = 0
                    sqlalche_obj.session.commit()
                    result = {"success":0,"result":{total_per:[host_param[0].host_name,host_param[0].ip_address]}}
                    return result
                else:
                    if snmp_ping_result == 2:
                        result = {"success":1,"result":"Network is Unreachable"}
                    elif snmp_ping_result == 1:
                        result = {"success":1,"result":"%s(%s) Device may not be connected or may be reboot"%(host_param[0].host_name,host_param[0].ip_address)}
                    elif snmp_ping_result == 3:
                        result = {"success":1,"result":"%s(%s) Device is unresponsive"%(host_param[0].host_name,host_param[0].ip_address)}
                    host_param[0].reconcile_status = 0                    
                    sqlalche_obj.session.commit()
                    return result
            else:
                result = {"success":1,"result":"Host data not exist"}
                return result
        except Exception as e:
            host_param[0].reconcile_health = 0
            host_param[0].reconcile_status = 0
            sqlalche_obj.session.commit()            
            result = {"success":1,"result":"Error Occured %s"%str(e)}
            return result
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            
    ####################### Device Reconciliation with isReconciliation reconciliation #################################################        
    def default_configuration_added(self,host_id,device_type_id,reconcile_chk=True):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        new_profile = Odu16ConfigProfiles(device_type_id,"APConfiguration","Master",None,datetime.now(),None,datetime.now(),None,0)
        sqlalche_obj.session.add(new_profile)
        sqlalche_obj.session.flush()
        sqlalche_obj.session.refresh(new_profile)
        new_profile_id = new_profile.config_profile_id
        reconcile_per = 0
        default_profile_id = sqlalche_obj.session.query(Odu16ConfigProfiles.config_profile_id)\
                            .filter(and_(Odu16ConfigProfiles.device_type_id==device_type_id,Odu16ConfigProfiles.config_profile_type_id=="default")).all()
        
        
        if len(default_profile_id)==0:
            return new_profile_id,0
        else:
            ipdata = sqlalche_obj.session.query(Ap25AccesspointIPsettings).filter(Ap25AccesspointIPsettings.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(ipdata)>0:
                for i in range(0,len(ipdata)):
                    ip_add_row = Ap25AccesspointIPsettings(new_profile_id,"" if ipdata[i].lanIPaddress==None else ipdata[i].lanIPaddress,\
                                                           "" if ipdata[i].lanSubnetMask==None else ipdata[i].lanSubnetMask,\
                                                           "" if ipdata[i].lanGatewayIP==None else ipdata[i].lanGatewayIP,\
                                                           "" if ipdata[i].lanPrimaryDNS == None else ipdata[i].lanPrimaryDNS,\
                                                           "" if ipdata[i].lanSecondaryDNS==None else ipdata[i].lanSecondaryDNS)
                    sqlalche_obj.session.add(ip_add_row)
                    
            vapselection_data = sqlalche_obj.session.query(Ap25VapSelection).filter(Ap25VapSelection.config_profile_id == default_profile_id[0].config_profile_id).all()
            vap_selection_id = []
            if len(vapselection_data)>0:
                for i in range(0,len(vapselection_data)):
                    vapselection_add_row = Ap25VapSelection(new_profile_id,vapselection_data[i].totalVAPsPresent,vapselection_data[i].selectVap)
                    sqlalche_obj.session.add(vapselection_add_row)
                    sqlalche_obj.session.flush()
                    sqlalche_obj.session.refresh(vapselection_add_row)
                    vap_selection_id.append(vapselection_add_row.ap25_vapSelection_id)                                        
            
            vapsecurity_data = sqlalche_obj.session.query(Ap25BasicVAPsecurity).filter(Ap25BasicVAPsecurity.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(vapsecurity_data)>0:
                for i in range(0,len(vapsecurity_data)):
                    vapsecurity_add_row = Ap25BasicVAPsecurity(new_profile_id,vap_selection_id[i],vapsecurity_data[i].vapSecurityMode)
                    sqlalche_obj.session.add(vapsecurity_add_row)
                
            basicvapsetup_data = sqlalche_obj.session.query(Ap25BasicVAPsetup).filter(Ap25BasicVAPsetup.config_profile_id == default_profile_id[0].config_profile_id).all()   
            if len(basicvapsetup_data)>0:
                for i in range(0,len(basicvapsetup_data)):
                    basicvapsetup_add_row = Ap25BasicVAPsetup(new_profile_id,vap_selection_id[i],basicvapsetup_data[i].vapESSID,\
                                                              basicvapsetup_data[i].vapHiddenESSIDstate,basicvapsetup_data[i].vapRTSthresholdValue,\
                                                              basicvapsetup_data[i].vapFragmentationThresholdValue,\
                                                              basicvapsetup_data[i].vapBeaconInterval,basicvapsetup_data[i].vlanid,\
                                                                basicvapsetup_data[i].vlanpriority,\
                                                                basicvapsetup_data[i].vapmode)
                    sqlalche_obj.session.add(basicvapsetup_add_row)
                
            wepsecurity_data = sqlalche_obj.session.query(Ap25VapWEPsecuritySetup).filter(Ap25VapWEPsecuritySetup.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(wepsecurity_data)>0:
                for i in range(0,len(wepsecurity_data)):
                    wepsecurity_add_row = Ap25VapWEPsecuritySetup(new_profile_id,wepsecurity_data[i].vapWEPmode,\
                                                                  wepsecurity_data[i].vapWEPprimaryKey,wepsecurity_data[i].vapWEPkey1,\
                                                                  wepsecurity_data[i].vapWEPkey2,wepsecurity_data[i].vapWEPkey3,wepsecurity_data[i].vapWEPkey4)
                    sqlalche_obj.session.add(wepsecurity_add_row)
                
            acl_data = sqlalche_obj.session.query(Ap25AclMacTable).filter(Ap25AclMacTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(acl_data)>0:
                for i in range(0,len(acl_data)):
                    acl_add_row = Ap25AclMacTable(new_profile_id,vap_selection_id[i],acl_data[i].macaddress)
                    sqlalche_obj.session.query(acl_add_row)
                    
            basicacl_data = sqlalche_obj.session.query(Ap25BasicACLsetup).filter(Ap25BasicACLsetup.config_profile_id == default_profile_id[0].config_profile_id).all()  
            if len(basicacl_data)>0:
                for i in range(0,len(basicacl_data)):
                    basicacl_add_row = Ap25BasicACLsetup(new_profile_id,vap_selection_id[i],basicacl_data[i].aclState,basicacl_data[i].aclMode)
                    sqlalche_obj.session.add(basicacl_add_row)
                
            dhcp_data = sqlalche_obj.session.query(Ap25DhcpServer).filter(Ap25DhcpServer.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(dhcp_data)>0:
                for i in range(0,len(dhcp_data)):
                    dhcp_add_row = Ap25DhcpServer(new_profile_id,dhcp_data[i].dhcpServerStatus,dhcp_data[i].dhcpStartIPaddress,dhcp_data[i].dhcpEndIPaddress,\
                                    dhcp_data[i].dhcpSubnetMask,dhcp_data[i].dhcpClientLeaseTime)
                                    
                    sqlalche_obj.session.add(dhcp_add_row)
                
            radioselection_data = sqlalche_obj.session.query(Ap25RadioSelection).filter(Ap25RadioSelection.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(radioselection_data)>0:
                for i in range(0,len(radioselection_data)):
                    radioselection_row_add = Ap25RadioSelection(new_profile_id,radioselection_data[i].radio)
                    sqlalche_obj.session.add(radioselection_row_add)
                
            radiosetup_data = sqlalche_obj.session.query(Ap25RadioSetup).filter(Ap25RadioSetup.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(radiosetup_data)>0:
                for i in range(0,len(radiosetup_data)):
                    radiosetup_row_add = Ap25RadioSetup(new_profile_id,radiosetup_data[i].radioState,radiosetup_data[i].radioAPmode,\
                                                        radiosetup_data[i].radioManagementVLANstate,radiosetup_data[i].countrycode,radiosetup_data[i].numberofVAPs,\
                                                        radiosetup_data[i].radioChannel,radiosetup_data[i].wifiMode,radiosetup_data[i].radioTxPower,\
                                                        radiosetup_data[i].radioGatingIndex,radiosetup_data[i].radioAggregation,radiosetup_data[i].radioAggFrames,\
                                                        radiosetup_data[i].radioAggSize,\
                                                        radiosetup_data[i].radioAggMinSize,radiosetup_data[i].radioChannelWidth,\
                                                        radiosetup_data[i].radioTXChainMask,radiosetup_data[i].radioRXChainMask)
                    sqlalche_obj.session.add(radiosetup_row_add)
                
            service_data = sqlalche_obj.session.query(Ap25Services).filter(Ap25Services.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(service_data)>0:
                for i in range(0,len(service_data)):
                    service_data_add_row = Ap25Services(new_profile_id,service_data[i].upnpServerStatus,service_data[i].systemLogStatus,\
                                                        service_data[i].systemLogIP,service_data[i].systemLogPort,service_data[i].systemTime)
                                                        
                    sqlalche_obj.session.add(service_data_add_row)
            
            wpa_data = sqlalche_obj.session.query(Ap25VapWPAsecuritySetup).filter(Ap25VapWPAsecuritySetup.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(wpa_data)>0:
                for i in range(0,len(wpa_data)):
                    wpa_add_row = Ap25VapWPAsecuritySetup(new_profile_id,vap_selection_id[i],wpa_data[i].vapWPAmode,wpa_data[i].vapWPAcypher,\
                                                        wpa_data[i].vapWPArekeyInterval,wpa_data[i].vapWPAmasterReKey,wpa_data[i].vapWEPrekeyInt,\
                                                         wpa_data[i].vapWPAkeyMode,wpa_data[i].vapWPAconfigPSKPassPhrase,wpa_data[i].vapWPArsnPreAuth,\
                                                        wpa_data[i].vapWPArsnPreAuthInterface,wpa_data[i].vapWPAeapReAuthPeriod,\
                                                         wpa_data[i].vapWPAserverIP,wpa_data[i].vapWPAserverPort,wpa_data[i].vapWPAsharedSecret)
                    sqlalche_obj.session.add(wpa_add_row)
                    
            basicconfiguration_data = sqlalche_obj.session.query(Ap25BasicConfiguration).filter(Ap25BasicConfiguration.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(basicconfiguration_data)>0:
                for i in range(0,len(basicconfiguration_data)):
                    basicconfig_add_row = Ap25BasicConfiguration(new_profile_id,basicconfiguration_data[i].accesspointName)
                    sqlalche_obj.session.add(basicconfig_add_row)
            aclstats_data = sqlalche_obj.session.query(Ap25AclStatisticsTable).filter(Ap25AclStatisticsTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(aclstats_data)>0:
                for i in range(0,len(aclstats_data)):
                    aclstats_add_row = Ap25AclStatisticsTable(new_profile_id,aclstats_data[i].aclTotalsINDEX,aclstats_data[i].vapNumber,aclstats_data[i].totalMACentries)
                    sqlalche_obj.session.add(aclstats_add_row)
            
            version_data = sqlalche_obj.session.query(Ap25Versions).filter(Ap25Versions.host_id == host_id).all()
            if len(version_data)>0:
                for i in range(0,len(version_data)):
                    version_add_row = Ap25Versions(host_id,version_data[i].hardwareVersion,version_data[i].softwareVersion,version_data[i].bootLoaderVersion)
                    sqlalche_obj.session.add(version_add_row)
            host_param = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id == host_id).all()
            host_param[0].config_profile_id = new_profile_id
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            result = {}
            if reconcile_chk==True:
                result = self.update_configuration(host_id,device_type_id)
                if result['success']==0:
                    #result = {"success":0,"result":{total_per:[host_param[0].host_name,host_param[0].ip_address]}}
                    for i in result["result"]:
                        reconcile_per = i
                    return str(new_profile_id),reconcile_per
                else:
                    return str(new_profile_id),0
            else:
                return str(new_profile_id),0
        
    def reconciliation_status(self):
        global sqlalche_obj
        result = {}
        rec_dir = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        rec_list = sqlalche_obj.session.query(Hosts.host_id,Hosts.reconcile_status,Hosts.reconcile_health).filter(and_(Hosts.device_type_id.like(UNMPDeviceType.ap25+"%"))).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(rec_list)>0:
            for i in range(0,len(rec_list)):
                rec_dir[str(rec_list[i][0])] = [rec_list[i][1],rec_list[i][2]]
            result = {"result":rec_dir,"success":0}
            return result
        
    def reconciliation_chk_status(self,host_id):
        global sqlalche_obj
        result = {}
        if host_id!="" or host_id!=None:
            sqlalche_obj.sql_alchemy_db_connection_open()
            reconcile_status = sqlalche_obj.session.query(Hosts.reconcile_status,Hosts.reconcile_health).filter(Hosts.host_id==host_id).all()
            reconcile_update = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id==host_id).all()
            status = reconcile_status[0].reconcile_status
            if reconcile_status[0].reconcile_status == 2:
                reconcile_update[0].reconcile_status = 0
                sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            result = {"result":[status,reconcile_status[0].reconcile_health],"success":0}
            return result             
        else:
            sqlalche_obj.sql_alchemy_db_connection_close()
            result={"result":"Host No exist","success":1}
            return result
        
        
    def reboot(self,host_id):
        global sqlalche_obj
        result = {}
        i = 0
        global errorStatus
        oid_dict = {}
        get_result = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_param = sqlalche_obj.session.query(Hosts.ip_address,Hosts.snmp_port,Hosts.snmp_write_community,Hosts.snmp_read_community).filter(Hosts.host_id==host_id).all()
        oid_dict[1] =  ['1.3.6.1.4.1.26149.10.5.3.0','Integer32',1]
        if len(host_param)>0:
            result = single_set(host_param[0].ip_address,int(host_param[0].snmp_port),host_param[0].snmp_write_community,oid_dict[1])
            if result["success"]==0:
                time.sleep(40)
                while(i<10):
                    get_result = pysnmp_get('1.3.6.1.4.1.26149.10.5.3.0',host_param[0].ip_address,int(host_param[0].snmp_port),'public')
                    if get_result["success"]==0:
                        result = {"success":0,"result":"Device is rebooting successfully"}
                        return result                                    
                    else:
                        for k in get_result["result"]:
                            if k != 53 and k != '53':                                    
                                if errorStatus.has_key(k):
                                    result = {"success":1,"result":errorStatus[k]}
                                    return result
                            elif k == 51 and k == '51':                                
                                if errorStatus.has_key(k):
                                    result = {"success":1,"result":errorStatus[k]}
                                    return result
                            else:                                
                                i = i+1
                                time.sleep(10)
                result = {'success':1,'result':'Device is Not Responding'}
                return result
            else:
                for k in result["result"]:
                    if errorStatus.has_key(k):
                        result = {"success":1,"result":errorStatus[k]}
                        return result
        else:
            return {"success":1,"result":"Host Data Not Exist"}
        
class APScan(object):
    
    def ap_scan(self,host_id):
        global sqlalche_obj
        global errorStatus
        sqlalche_obj.sql_alchemy_db_connection_open()
        result = {}
        host_param = sqlalche_obj.session.query(Hosts.ip_address,Hosts.snmp_port,Hosts.snmp_write_community,Hosts.snmp_read_community).filter(Hosts.host_id==host_id).all()
        if len(host_param)>0:
            result = pysnmp_get_table('1.3.6.1.4.1.26149.10.4.5.1.1.1',host_param[0].ip_address,int(host_param[0].snmp_port),host_param[0].snmp_read_community)
            if result["success"]==0:
                return result
            else:
                #result = {'success':0,'result':0}
                for k in result["result"]:
                    if errorStatus.has_key(k):
                        result = {"success":1,"result":errorStatus[k]}
                        return result
        else:
            return "No Host Exist"

##obj = APScan()
##print obj.ap_scan(42)
class APGetData(object):
    
    def ap_get_data(self,class_name,host_id):
        try:
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_id == "" or host_id == None:
                return []
            config_id = sqlalche_obj.session.query(Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
            if len(config_id)>0:
                get_data = sqlalche_obj.session.query(eval('%s'%(class_name))).filter(eval('%s'%(class_name)).config_profile_id=='%s'%(config_id[0].config_profile_id)).all()
                if len(get_data)>0:
                    return get_data
                else:
                    return []
            else:
                return []
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()


class APCommonSetValidation(object):
    
    def common_set_config(self,host_id,device_type_id,dic_result,id=None,index=0,special_case=0):
    ##dic_result = {'success':0,'result':{'ru.omcConfTable.omcIpAddress':[1,'Not Done'],'ru.omcConfTable.periodicStatsTimer':[1,'Not Done']}}
    ##return dic_result
        try:  
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            success_result = {"success":'',"result":{}}
            global errorStatus 
            o1 = aliased(Ap25Oids)
            table_name = "Ap25Oids"
            o2 = aliased(Ap25Oids)
            rowSts = {'ru.ra.raAclConfigTable.rowSts':['1.3.6.1.4.1.26149.2.2.13.5.1.3','Integer32','']}
            query_result = []
            oid_admin_state = {"1":-1}
            independent_oid = []
            dependent_oid = []
            depend_oid_value = []
            result = {} 
            key = ""
            exist_data = 0
            for keys in dic_result.iterkeys():
                if keys == "success":
                    continue
                else:
                    query_result = sqlalche_obj.session.query(o2,o1.oid_name,o1.oid,o1.indexes).outerjoin(o1,o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys,o2.device_type_id == device_type_id)).all()
                    if len(query_result) > 0:
                        if query_result[0][0].dependent_id == "" or query_result[0][0].dependent_id == None:
                            independent_oid.append({keys:[query_result[0][0].oid + query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                        else:
                            if len(dependent_oid) > 0:
                                for i in range(0,len(dependent_oid)):
                                    if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                        admin_state = 'ru.ruConfTable.adminstate'
                                    elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                        admin_state = 'ru.ipConfigTable.adminState-1'
                                    elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                        admin_state = 'ru.ra.raConfTable.raAdminState-1'
                                    else:
                                        admin_state = query_result[0][1]
                                    if dependent_oid[i].has_key(admin_state):
                                        pos = i
                                        if len(depend_oid_value) > 0:
                                            depend_oid_value[pos][keys] = [query_result[0][0].oid + query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]
                                            break
                                        else:
                                            depend_oid_value.append({keys:[query_result[0][0].oid + query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                                            break
                                    else:
                                        if i == len(dependent_oid)-1:
                                            if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                                dependent_oid.append({query_result[0][1]+str(-1):[query_result[0][2]+query_result[0][3]]})
                                                depend_oid_value.append({keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                                            elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                                dependent_oid.append({query_result[0][1]+str(-1):[query_result[0][2]+query_result[0][3]]})
                                                depend_oid_value.append({keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                                            elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                                dependent_oid.append({query_result[0][1]+str(-1):[query_result[0][2]+query_result[0][3]]})
                                                depend_oid_value.append({keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                                            else:
                                                dependent_oid.append({query_result[0][1]:[query_result[0][2]+query_result[0][3]]})
                                                depend_oid_value.append({keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                                        else:
                                            continue
                            else:                           
                                if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                    dependent_oid.append({query_result[0][1]+str(-1):[query_result[0][2]+query_result[0][3]]})
                                    depend_oid_value.append({keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                                elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                    dependent_oid.append({query_result[0][1]+str(-1):[query_result[0][2]+query_result[0][3]]})
                                    depend_oid_value.append({keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                                elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':                                
                                    dependent_oid.append({query_result[0][1]+str(-1):[query_result[0][2]+query_result[0][3]]})
                                    depend_oid_value.append({keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})                               
                                else:
                                    dependent_oid.append({query_result[0][1]:[query_result[0][2]+query_result[0][3]]})
                                    depend_oid_value.append({keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})                                
                    else:
                        success_result["success"] = 1
                        success_result["result"] = "There is no row in database"       
                    
            pos = len(depend_oid_value)
            if pos!=0:
                for i in range(0,len(independent_oid)):
                    depend_oid_value[pos-1].update(independent_oid[i])
            else:
                for i in range(0,len(independent_oid)):
                    depend_oid_value.append(independent_oid[i])
            device_param_list = sqlalche_obj.session.query(Hosts.ip_address,Hosts.snmp_port,Hosts.snmp_write_community,Hosts.config_profile_id).\
                                filter(Hosts.host_id == host_id).one()         
            j = -1 
            if len(dependent_oid)>0:            
                for i in range(0,len(dependent_oid)):
                    j+=1                
                    if dependent_oid[i].has_key('ru.ruConfTable.adminstate-1'):
                        result = (pysnmp_seter(depend_oid_value[i],device_param_list[0],device_param_list[1],device_param_list[2],dependent_oid[i]))
                    elif dependent_oid[i].has_key('ru.ipConfigTable.adminState-1'):
                        result = (pysnmp_seter(depend_oid_value[i],device_param_list[0],device_param_list[1],device_param_list[2],dependent_oid[i]))
                    elif dependent_oid[i].has_key('ru.ra.raConfTable.raAdminState-1'):   
                        result = (pysnmp_seter(depend_oid_value[i],device_param_list[0],device_param_list[1],device_param_list[2],dependent_oid[i]))
                    else:
                        result = pysnmp_seter(depend_oid_value[i],device_param_list[0],device_param_list[1],device_param_list[2],dependent_oid[i])                    
                    if result["success"] == 0 or result["success"] == '0':                    
                        success_result["success"] = result["success"]
                        for i in result["result"]:
                            if result["result"][i] != 0:
                                result["result"][i] = errorStatus[result["result"][i]]
                            else:
                                oid_list_table_field_value = sqlalche_obj.session.query(Ap25Oids.table_name,Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i,Ap25Oids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                else:
                                    
                                    if i in dic_result:
                                        table_name = "ap25_" + oid_list_table_field_value[0][0]
                                        table_name = rename_tablename(table_name)
                                        exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()"%(table_name,table_name,device_param_list[3])
                                        exec "table_result[0].%s = '%s'"%(oid_list_table_field_value[0][1],dic_result[i])
                                        if ("ap25_" + oid_list_table_field_value[0][0]) == "odu100_ipConfigTable":
                                            host_data  = sqlalche_obj.session.query(Hosts).filter(Hosts.config_profile_id == device_param_list[3]).all()
                                            if i=="ru.ipConfigTable.ipAddress":
                                                host_data[0].ip_address = dic_result[i]
                                            if i=="ru.ipConfigTable.ipNetworkMask":
                                                host_data[0].netmask = dic_result[i]
                                            if i=="ru.ipConfigTable.ipDefaultGateway":
                                                host_data[0].gateway = dic_result[i]
                                        sqlalche_obj.session.commit()
                        success_result["result"].update(result["result"])
                    else:
                        success_result["success"] = 1
                        for i in result["result"]:
                            errorStatus.has_key(i)
                            success_result["result"] = errorStatus[i]
                            
            if len(dependent_oid)>0:  
                for i in range(0,len(dependent_oid)):               
                    query_admin_result = sqlalche_obj.session.query(Ap25Oids.oid,Ap25Oids.oid_type,Ap25Oids.indexes).filter(Ap25Oids.oid_name == "ru.ra.raConfTable.raAdminState").one()                            
                    if dependent_oid[i].has_key('ru.ruConfTable.adminstate-1'):                    
                        admin_state = "ru.ruConfTable.adminstate"
                        query_admin_result = sqlalche_obj.session.query(Ap25Oids.oid,Ap25Oids.oid_type,Ap25Oids.indexes).filter(Ap25Oids.oid_name == "ru.ruConfTable.adminstate").one()
                        dic_admin_value = {"ru.ruConfTable.adminstate":[query_admin_result[0]+query_admin_result[2],query_admin_result[1],'1']}                    
                        if len(query_admin_result) > 0:                       
                            result = pysnmp_seter(dic_admin_value,device_param_list[0],device_param_list[1],device_param_list[2])
                            if result["success"] == 0 or result["success"] == '0':
                                success_result["success"] = result["success"]
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        result["result"][i] = errorStatus[result["result"][i]]
                                    else:
                                        oid_list_table_field_value = sqlalche_obj.session.query(Ap25Oids.table_name,Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i,Ap25Oids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:
                                                table_name = "ap25_" + oid_list_table_field_value[0][0]
                                                table_name = rename_tablename(table_name)
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()"%(table_name,table_name,device_param_list[3])
                                               
                                                exec "table_result[0].%s = '%s'"%(oid_list_table_field_value[0][1],dic_result[i])
                                            sqlalche_obj.session.commit()
                                #success_result["result"].update(result["result"])
                            else:
                                #success_result["success"] = 1
                                for i in result["result"]:
                                    errorStatus.has_key(result["result"][i])
                                    #success_result["result"] = errorStatus[result["result"][i]]
                                    
                    elif dependent_oid[i].has_key('ru.ipConfigTable.adminState-1'):                  
                        query_admin_result = sqlalche_obj.session.query(Ap25Oids.oid,Ap25Oids.oid_type,Ap25Oids.indexes).filter(Ap25Oids.oid_name == "ru.ipConfigTable.adminState").one()
                        dic_admin_value = {"ru.ipConfigTable.adminState":[query_admin_result[0]+query_admin_result[2],query_admin_result[1],'1']}
                        if len(query_admin_result) > 0:                        
                            result = pysnmp_seter(dic_admin_value,device_param_list[0],device_param_list[1],device_param_list[2])                        
                            if result["success"] == 0 or result["success"] == '0':
                                success_result["success"] = result["success"]
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        result["result"][i] = errorStatus[result["result"][i]]
                                    else:
                                        oid_list_table_field_value = sqlalche_obj.session.query(Ap25Oids.table_name,Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i,Ap25Oids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:
                                                
                                                table_name = "ap25_" + oid_list_table_field_value[0][0]
                                                table_name = rename_tablename(table_name)
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()"%(table_name,table_name,device_param_list[3])
                                                exec "table_result[0].%s = '%s'"%(oid_list_table_field_value[0][1],dic_result[i])                                       
                                #success_result["result"] = errorStatus[result["result"][i]]
                            else:
                                #success_result["success"] = 1
                                for i in result["result"]:
                                    errorStatus.has_key(result["result"][i])
                                    #success_result["result"] = errorStatus[result["result"][i]]                                
                    elif dependent_oid[i].has_key('ru.ra.raConfTable.raAdminState-1'):                    
                        query_admin_result = sqlalche_obj.session.query(Ap25Oids.oid,Ap25Oids.oid_type,Ap25Oids.indexes).filter(Ap25Oids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                        dic_admin_value = {"ru.ra.raConfTable.raAdminState":[query_admin_result[0]+query_admin_result[2],query_admin_result[1],'1']}
                        if len(query_admin_result) > 0:                        
                            result = pysnmp_seter(dic_admin_value,device_param_list[0],device_param_list[1],device_param_list[2])  
                            if result["success"] == 0 or result["success"] == '0':
                                success_result["success"] = result["success"]
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        result["result"][i] = errorStatus[result["result"][i]]
                                    else:
                                        oid_list_table_field_value = sqlalche_obj.session.query(Ap25Oids.table_name,Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i,Ap25Oids.device_type_id == device_type_id)).all()
                                        if len(oid_list_table_field_value) == 0:
                                            continue
                                        else:
                                            if i in dic_result:                                           
                                                table_name = "ap25_" + oid_list_table_field_value[0][0]
                                                table_name = rename_tablename(table_name)
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()"%(table_name,table_name,device_param_list[3])
                                                exec "table_result[0].%s = '%s'"%(oid_list_table_field_value[0][1],dic_result[i])                                    
                                #success_result["result"].update(result["result"])
                            else:
                                for i in result["result"]:
                                    errorStatus.has_key(result["result"][i])
                                    #success_result["result"] = errorStatus[result["result"][i]]
                        break                
                    else:
                        continue
            if(j == -1): 
                if len(depend_oid_value)>0:  
                    dic_oid = {}
                    for i in range(0,len(depend_oid_value)):  
                        dic_oid.update(depend_oid_value[i])                  
                    if id!=None:
                        for key in depend_oid_value[i]:
                            oid = depend_oid_value[i][key][0][0:-1]
                            depend_oid_value[i][key][0] = str(oid)+str(id)
                    result = pysnmp_seter(dic_oid,device_param_list[0],device_param_list[1],device_param_list[2])                   
                    if result["success"] == 0 or result["success"] == '0':
                        success_result["success"] = result["success"]
                        for i in result["result"]:
                            if result["result"][i] != 0:
                                result["result"][i] = errorStatus[result["result"][i]]
                            else:
                                oid_list_table_field_value = sqlalche_obj.session.query(Ap25Oids.table_name,Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i,Ap25Oids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                else:
                                    if i in dic_result:
                                        sql_table_name = "ap25_" + oid_list_table_field_value[0][0]
                                        tableName= sql_table_name+"_id" 
                                        table_name = rename_tablename(sql_table_name)
                                        if index!=0:
                                            exec "table_result = sqlalche_obj.session.query(%s).filter(and_(%s.%s==%s,%s.config_profile_id == \"%s\")).all()"%(table_name,table_name,tableName,index,table_name,device_param_list[3])       
                                        else:
                                            exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()"%(table_name,table_name,device_param_list[3])
                                        if len(table_result)>0:
                                            if special_case!=0 and special_case!='0':
                                                exec "sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").update({'%s':%s})"%(table_name,table_name,device_param_list[3],oid_list_table_field_value[0][1],dic_result[i])
                                            else:
                                                exec "table_result[0].%s = '%s'"%(oid_list_table_field_value[0][1],dic_result[i])       
                                        else:
                                            exist_data = 1
                        if exist_data == 1:
                            success_result["success"]=1
                            success_result["result"]="Reconcilation process has exited. \n Please retry."
                        else:
                            success_result["result"].update(result["result"])
                    else:
                        if 53 in result["result"]:
                            return {"success":1,"result":"No Response From Device.Please Try Again"}
                        elif 51 in result["result"]:
                            return {"success":1,"result":"Network is unreachable"}
                        elif 99 in result["result"]:
                            return {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
                        else:
                            success_result["success"]=0
                            for i in result["result"]:
                                if result["result"][i] != 0:
                                    if errorStatus.has_key(result["result"][i]):
                                        result["result"][i] = errorStatus[result["result"][i]]
                            success_result["result"].update(result["result"])
                            
                        

            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close() 
            return success_result
             
            
        except ProgrammingError as e:
            return {"success":1,"result":"Some Programming Error Occurs","detail":""}
        except AttributeError as e:
            return {"success":1,"result":"Some Attribute Error Occurs","detail":str(e)}
        except OperationalError as e:
            return {"success":1,"result":"Some Operational Error Occurs","detail":str(e)}    
        except TimeoutError as e:
            return {"success":1,"result":"Timeout Error Occurs","detail":""}
        except NameError as e:
            return {"success":1,"result":"Some Name Error Occurs","detail":str(e[-1])}
        except UnboundExecutionError as e:
            return {"success":1,"result":"Unbound Execution Error Occurs","detail":""}
        except DatabaseError as e:
            return {"success":1,"result":"Database Error Occurs,Contact Your Administrator","detail":""}
        except DisconnectionError as e:
            return {"success":1,"result":"Database Disconnected","detail":""}
        except NoResultFound as e:
            return {"success":1,"result":"No result Found For this opeartion","detail":str(e)}
        except UnmappedInstanceError as e:
            return {"success":1,"result":"Some Unmapped instance error","detail":""}
        except NoReferenceError as e:
            return {"success":1,"result":"No reference Exists","detail":""}
        except SAWarning as e:
            return {"success":1,"result":"Warning Occurs","detail":""}
        except Exception as e:   
            return {"success":1,"result":"Operation Failed,contact Administrator","detail":str(e)}
        
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            
            
    def common_validation(self,host_id,device_type_id,dic_result,id=None,index=0,special_case=0):
        try:
            obj_set = APCommonSetValidation()
            flag = 0
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            if dic_result["success"] == '0' or dic_result["success"] == 0:
                for keys in dic_result.iterkeys():
                    if keys == "success":
                        continue
                    else:
                        oid_list_min_max_value = sqlalche_obj.session.query(Ap25Oids.min_value,Ap25Oids.max_value).filter(and_(Ap25Oids.oid_name == keys,Ap25Oids.device_type_id == device_type_id)).all()
                        if len(oid_list_min_max_value) == 0:
                            flag = 1
                            continue
                        else:
                            if (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value [0][0] == None) and (oid_list_min_max_value[0][1] != "" and oid_list_min_max_value[0][1] != None):
                                if int(dic_result[keys]) <= int(oid_list_min_max_value[0][1]) :
                                    dic_result["%s"%(keys)] = dic_result[keys]
                                else:
                                    dic_result={}
                                    flag = 1
                                    dic_result["result"] = "The value is large than %s"%(oid_list_min_max_value[1])
                                    break
                            elif (oid_list_min_max_value[0][0] != "" or oid_list_min_max_value[0][0] != None) and (oid_list_min_max_value[0][1] == "" and oid_list_min_max_value[0][1] == None):
                                if int(dic_result[keys]) >= int(oid_list_min_max_value[0][0]) :
                                    dic_result["%s"%(keys)] = dic_result[keys]
                                else:
                                    dic_result={}
                                    flag = 1
                                    dic_result["result"] = "The value is smaller than %s"%(oid_list_min_max_value[0][0])
                                    break
                            elif (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == None) and (oid_list_min_max_value[0][1] == "" or oid_list_min_max_value[0][1] == None):       
                                dic_result["%s"%(keys)] = dic_result[keys]
                            elif (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == 'NULL') and (oid_list_min_max_value[0][1] == "" or oid_list_min_max_value[0][1] == 'NULL'):       
                                dic_result["%s"%(keys)] = dic_result[keys]
                            else:
                                if (int(dic_result[keys]) >= int(oid_list_min_max_value[0][0])) and (int(dic_result[keys]) <= int(oid_list_min_max_value[0][1])):
                                    dic_result["%s"%(keys)] = dic_result[keys]
                                else:
                                    dic_result={}
                                    flag = 1
                                    dic_result["result"] = "%s Value must be in between %s and %s" %(keys.split(".")[-1],oid_list_min_max_value[0][0],oid_list_min_max_value[0][1])
                                    break
                if flag == 1:
                    dic_result["success"] = 1
                    sqlalche_obj.sql_alchemy_db_connection_close()   
                    return dic_result
                else:
                    sqlalche_obj.sql_alchemy_db_connection_close()   
                    dic_result = obj_set.common_set_config(host_id,device_type_id,dic_result,id,index,special_case=0)
                    return dic_result
            else:
                sqlalche_obj.sql_alchemy_db_connection_close()  
                return dic_result
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()  
            dic_result["success"] = 1
            dic_result["result"] = str(e)
            return str(e)
        
    def ap_cancel_form(self,host_id,device_type_id,dic_result):
        try:
            flag = 0
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            success_result = {}
            profile_id = sqlalche_obj.session.query(Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
            if dic_result["success"] == 0:
                for keys in dic_result:
                    if keys == "success":
                        continue
                    else:
                        oid_list_table_field_value = sqlalche_obj.session.query(Ap25Oids.table_name,Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == keys,Ap25Oids.device_type_id == device_type_id)).all()
                        
                        table_name = "ap25_" + oid_list_table_field_value[0][0]
                        table_name = rename_tablename(table_name)
                        str_table_obj = "table_result = sqlalche_obj.session.query(%s.%s).filter(%s.config_profile_id == \"%s\").all()"%(table_name,oid_list_table_field_value[0][1],table_name,profile_id[0])
                        exec str_table_obj
                        if len(table_result)>0:
                            for i in range(0,len(table_result)):
                                dic_result[keys] = str(table_result[i][0])
                        else:
                            dic_result ={}
                            dic_result["success"] = 1
                            dic_result["result"] = "Data Not Exixt"
                sqlalche_obj.sql_alchemy_db_connection_close()  
                return dic_result
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()  
            dic_result["success"] = 1
            dic_result["result"] = str(e[-1])
            return dic_result
        
    def basic_acl_set(self,host_id,device_type_id,dic_result):
        try:
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {}
            global errorStatus 
            o1 = aliased(Ap25Oids)
            table_name = "Ap25Oids"
            o2 = aliased(Ap25Oids)
            result = {} 
            independent_oid = []
            depend_oid_value = []
            set_vap_acl = {}
            basic_acl = {}
            host_data = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id==host_id).all()
            select_vpa_data = []
            for keys in dic_result.iterkeys():
                if keys == "success" or keys == "vap_selection_id":
                    continue
                else:
                    query_result = sqlalche_obj.session.query(o2,o1.oid_name,o1.oid,o1.indexes).outerjoin(o1,o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys,o2.device_type_id == device_type_id)).all()
                    if len(query_result)>0:
                        independent_oid.append({keys:[query_result[0][0].oid + query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]})
                    
            for i in independent_oid:
                for keys in i.iterkeys():
                    if keys == "vapSelection.selectVap":
                        set_vap_acl = i
                    else:
                        basic_acl.update(i)
            result = pysnmp_seter(basic_acl,host_data[0].ip_address,host_data[0].snmp_port,host_data[0].snmp_write_community,set_vap_acl)
            
            if result["success"] == 0 or result["success"] == '0':
                for i in result["result"]:
                    if result["result"][i] != 0:
                        result["result"][i] = errorStatus[result["result"][i]]
                    else:
                        if i in dic_result:
                            oid_list_table_field_value = sqlalche_obj.session.query(Ap25Oids.table_name,Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i,Ap25Oids.device_type_id == device_type_id)).all()
                            if len(oid_list_table_field_value)==0:
                                continue
                            if i == "vapSelection.selectVap":
                                select_vap_data = sqlalche_obj.session.query(Ap25VapSelection).filter(Ap25VapSelection.config_profile_id==host_data[0].config_profile_id).all()
                                if len(select_vap_data)>0:
                                    for j in range(0,len(select_vap_data)):
                                        select_vap_data[j].selectVap = dic_result[i]
                            else:
                                basic_acl_data = sqlalche_obj.session.query(Ap25BasicACLsetup).filter(Ap25BasicACLsetup.vapselection_id==dic_result['vap_selection_id']).all()
                                if len(basic_acl_data)>0:
                                    for k in range(0,len(basic_acl_data)):
                                        exec "basic_acl_data[%s].%s = '%s'"%(k,oid_list_table_field_value[0].coloumn_name,dic_result[i])
                sqlalche_obj.session.commit()
            else:
                if 53 in result["result"]:
                    result = {"success":1,"result":"No Response From Device.Please Try Again"}
                elif 51 in result["result"]:
                    result =  {"success":1,"result":"Network is unreachable"}
                elif 99 in result["result"]:
                    result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}                        
            return result    
        except ProgrammingError as e:
            return {"success":1,"result":"Some Programming Error Occurs","detail":""}
        except AttributeError as e:
            return {"success":1,"result":"Some Attribute Error Occurs","detail":str(e)}
        except OperationalError as e:
            return {"success":1,"result":"Some Operational Error Occurs","detail":str(e)}    
        except TimeoutError as e:
            return {"success":1,"result":"Timeout Error Occurs","detail":""}
        except NameError as e:
            return {"success":1,"result":"Some Name Error Occurs","detail":str(e[-1])}
        except UnboundExecutionError as e:
            return {"success":1,"result":"Unbound Execution Error Occurs","detail":""}
        except DatabaseError as e:
            return {"success":1,"result":"Database Error Occurs,Contact Your Administrator","detail":""}
        except DisconnectionError as e:
            return {"success":1,"result":"Database Disconnected","detail":""}
        except NoResultFound as e:
            return {"success":1,"result":"No result Found For this opeartion","detail":str(e)}
        except UnmappedInstanceError as e:
            return {"success":1,"result":"Some Unmapped instance error","detail":""}
        except NoReferenceError as e:
            return {"success":1,"result":"No reference Exists","detail":""}
        except SAWarning as e:
            return {"success":1,"result":"Warning Occurs","detail":""}
        except Exception as e:   
            return {"success":1,"result":"Operation Failed,contact Administrator","detail":str(e)}
        
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()


    def vap_set(self,host_id,device_type_id,dic_result,selectedvap,vap_id):
        try:
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {}
            global errorStatus 
            o1 = aliased(Ap25Oids)
            table_name = "Ap25Oids"
            o2 = aliased(Ap25Oids)
            result = {} 
            vap_data = {}
            independent_oid = []
            host_data = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id==host_id).all()
            for keys in dic_result.iterkeys():
                if keys == "success":
                    continue
                else:
                    query_result = sqlalche_obj.session.query(o2,o1.oid_name,o1.oid,o1.indexes).outerjoin(o1,o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys,o2.device_type_id == device_type_id)).all()
                    if len(query_result)>0:
                        try:
                            key = int(dic_result[keys])
                        except:
                            key = dic_result[keys]
                        independent_oid.append({keys:[query_result[0][0].oid + query_result[0][0].indexes,query_result[0][0].oid_type,key]})
                        
            for i in independent_oid:
                for keys in i.iterkeys():
                    vap_data.update(i)
            result = pysnmp_seter(vap_data,host_data[0].ip_address,host_data[0].snmp_port,host_data[0].snmp_write_community,{'selectedVap':['1.3.6.1.4.1.26149.10.2.3.1.2.0','Integer32',selectedvap]})
            print result,"\n\n\n"
            if result["success"] == 0 or result["success"] == '0':
                for i in result["result"]:
                    if result["result"][i] != 0:
                        result["result"][i] = errorStatus[result["result"][i]]
                    else:
                        if i in dic_result:
                            oid_list_table_field_value = sqlalche_obj.session.query(Ap25Oids.table_name,Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i,Ap25Oids.device_type_id == device_type_id)).all()
                            if len(oid_list_table_field_value)==0:
                                continue
                            if i == "selectedVap":
                                continue
                            tablename = "ap25_"+oid_list_table_field_value[0].table_name
                            sql_table_name = rename_tablename(tablename)
                            if i == "vapWEPsecuritySetup.vapWEPmode" or i=="vapWEPsecuritySetup.vapWEPkey1" or i=="vapWEPsecuritySetup.vapWEPkey2" or i=="vapWEPsecuritySetup.vapWEPkey3" or i=="vapWEPsecuritySetup.vapWEPkey4" or i=="vapWEPsecuritySetup.vapWEPprimaryKey":
                                
                                exec "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()"%(sql_table_name,sql_table_name,host_data[0].config_profile_id)
                                
                                exec "table_result[0].%s='%s'"%(oid_list_table_field_value[0].coloumn_name,dic_result[i])
                            else: 
                                
                                exec "table_result=sqlalche_obj.session.query(%s).filter(%s.vapselection_id=='%s').all()"%(sql_table_name,sql_table_name,vap_id)
                                exec "table_result[0].%s='%s'"%(oid_list_table_field_value[0].coloumn_name,dic_result[i])    
                            sqlalche_obj.session.commit()
            else:
                if 53 in result["result"]:
                    result = {"success":1,"result":"No Response From Device.Please Try Again"}
                elif 51 in result["result"]:
                    result =  {"success":1,"result":"Network is unreachable"}
                elif 99 in result["result"]:
                    result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}                        
            return result    
            
        except ProgrammingError as e:
            return {"success":1,"result":"Some Programming Error Occurs","detail":""}
        except AttributeError as e:
            return {"success":1,"result":"Some Attribute Error Occurs","detail":str(e)}
        except OperationalError as e:
            return {"success":1,"result":"Some Operational Error Occurs","detail":str(e)}    
        except TimeoutError as e:
            return {"success":1,"result":"Timeout Error Occurs","detail":""}
        except NameError as e:
            return {"success":1,"result":"Some Name Error Occurs","detail":str(e[-1])}
        except UnboundExecutionError as e:
            return {"success":1,"result":"Unbound Execution Error Occurs","detail":""}
        except DatabaseError as e:
            return {"success":1,"result":"Database Error Occurs,Contact Your Administrator","detail":""}
        except DisconnectionError as e:
            return {"success":1,"result":"Database Disconnected","detail":""}
        except NoResultFound as e:
            return {"success":1,"result":"No result Found For this opeartion","detail":str(e)}
        except UnmappedInstanceError as e:
            return {"success":1,"result":"Some Unmapped instance error","detail":""}
        except NoReferenceError as e:
            return {"success":1,"result":"No reference Exists","detail":""}
        except SAWarning as e:
            return {"success":1,"result":"Warning Occurs","detail":""}
        except Exception as e:   
            return {"success":1,"result":"Operation Failed,contact Administrator","detail":str(e)}
        
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            
class SelectVap(object):
    
    def select_vap_vap(self,host_id,device_type):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        final_result = []
        host_data = sqlalche_obj.session.query(Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
        result_data = sqlalche_obj.session.query(Ap25BasicACLsetup.aclState,Ap25BasicACLsetup.aclMode,Ap25BasicACLsetup.vapselection_id).filter(Ap25BasicACLsetup.config_profile_id==host_data[0].config_profile_id).all()
        
        for i in range(0,len(result_data)):
            sub_list=[int(i) for i in result_data[i]]
            final_result.append(sub_list)
        sqlalche_obj.sql_alchemy_db_connection_close()
        return final_result
    
    def select_vap_change(self,host_id,device_type):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        final_result = []
        sub_list_basic_vap = []
        sub_list_wep = []
        sub_list_wpa = []
        sub_list_basic_vap_security = []
        host_data = sqlalche_obj.session.query(Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
        result_basic_vap_data = sqlalche_obj.session.query(Ap25BasicVAPsetup.vapselection_id,Ap25BasicVAPsetup.vapESSID,Ap25BasicVAPsetup.vapHiddenESSIDstate,\
                                                            Ap25BasicVAPsetup.vapRTSthresholdValue,\
                                                            Ap25BasicVAPsetup.vapFragmentationThresholdValue,\
                                                            Ap25BasicVAPsetup.vapBeaconInterval).filter(Ap25BasicVAPsetup.config_profile_id==host_data[0].config_profile_id).all()        
        
        result_wep_security_data = sqlalche_obj.session.query(Ap25VapWEPsecuritySetup.vapWEPmode,\
                                                            Ap25VapWEPsecuritySetup.vapWEPprimaryKey,\
                                                            Ap25VapWEPsecuritySetup.vapWEPkey1,\
                                                            Ap25VapWEPsecuritySetup.vapWEPkey2,\
                                                            Ap25VapWEPsecuritySetup.vapWEPkey3,\
                                                            Ap25VapWEPsecuritySetup.vapWEPkey4).filter(Ap25VapWEPsecuritySetup.config_profile_id==host_data[0].config_profile_id).all()
        
        result_wpa_security_data = sqlalche_obj.session.query(Ap25VapWPAsecuritySetup.vapWPAmode,\
                                                            Ap25VapWPAsecuritySetup.vapWPAcypher,\
                                                            Ap25VapWPAsecuritySetup.vapWPArekeyInterval,\
                                                            Ap25VapWPAsecuritySetup.vapWPAmasterReKey,\
                                                            Ap25VapWPAsecuritySetup.vapWEPrekeyInt,\
                                                            Ap25VapWPAsecuritySetup.vapWPAkeyMode,\
                                                            Ap25VapWPAsecuritySetup.vapWPAconfigPSKPassPhrase,\
                                                            Ap25VapWPAsecuritySetup.vapWPArsnPreAuth,\
                                                            Ap25VapWPAsecuritySetup.vapWPArsnPreAuthInterface,\
                                                            Ap25VapWPAsecuritySetup.vapWPAeapReAuthPeriod,\
                                                            Ap25VapWPAsecuritySetup.vapWPAserverIP,\
                                                            Ap25VapWPAsecuritySetup.vapWPAserverPort,\
                                                            Ap25VapWPAsecuritySetup.vapWPAsharedSecret).filter(Ap25VapWPAsecuritySetup.config_profile_id==host_data[0].config_profile_id).all()
        result_basic_vap_security_mode = sqlalche_obj.session.query(Ap25BasicVAPsecurity.vapSecurityMode).filter(Ap25BasicVAPsecurity.config_profile_id==host_data[0].config_profile_id).all()
        for i in range(0,len(result_basic_vap_data)):
            for j in result_basic_vap_data[i]:
                if isinstance(j,str):
                    sub_list_basic_vap.append(j)
                else:
                    if j==None:
                        sub_list_basic_vap.append("")
                    else:
                        sub_list_basic_vap.append(int(j))
        for i in range(0,len(result_wep_security_data)):
            for j in result_wep_security_data[i]:
                if isinstance(j,str):
                    sub_list_wep.append(j)
                else:
                    if j==None:
                        sub_list_wep.append("")
                    else:
                        sub_list_wep.append(int(j))
        for i in range(0,len(result_wpa_security_data)):
            for j in result_wpa_security_data[i]:
                if isinstance(j,str):
                    sub_list_wpa.append(j)
                else:
                    if j==None:
                        sub_list_wpa.append("")
                    else:
                        sub_list_wpa.append(int(j))
                        
        for i in range(0,len(result_basic_vap_security_mode)):
            for j in result_basic_vap_security_mode[i]:
                if isinstance(j,str):
                    sub_list_basic_vap_security.append(j)
                else:
                    if j==None:
                        sub_list_basic_vap_security.append("")
                    else:
                        sub_list_basic_vap_security.append(int(j))

        v1,v2,v3 = 0,0,0
        li = []
        for i in range(0,8):
            temp_li = []
            temp_li+=sub_list_basic_vap[v1:v1+6]
            v1 = v1+6
            temp_li+=sub_list_wep
            temp_li+=sub_list_wpa[v2:v2+13]
            v2 = v2+13
            temp_li+=sub_list_basic_vap_security
            v3 = v3+1
            li.append(temp_li)
        sqlalche_obj.sql_alchemy_db_connection_close()
        return li
    
    def select_mac(self,vap_select_id):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        final_result = []
        result_data = sqlalche_obj.session.query(Ap25AclMacTable).filter(Ap25AclMacTable.vapselection_id==vap_select_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result_data

class MacOperations(object):
    
    def chk_mac_duplicate(self,macaddress,vap_selection_id):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        success = 0
        mac_list = sqlalche_obj.session.query(Ap25AclMacTable.macaddress).filter(Ap25AclMacTable.vapselection_id==vap_selection_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(mac_list)>0:
            for i in mac_list:
                
                if macaddress in i:
                    success = 1
                    break
                else:
                    success = 0
            return success
        else:
            return success
        
    def add_acl(self,host_id,device_type_id,dic_result,vap_selection_id,selected_vap):
        global sqlalche_obj
        m = 0
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_data = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id == host_id).all()
        acl_mac_data = sqlalche_obj.session.query(Ap25AclMacTable.macaddress).filter(Ap25AclMacTable.vapselection_id==vap_selection_id).all()
        vap_index = len(acl_mac_data)
        final_result = {}
        errorIndex = 0
        for i in dic_result:
            if i == "success":
                continue
            mac_length = len(dic_result[i])
            for j in range(0,len(dic_result[i])):
                result = pysnmp_seter({i:['1.3.6.1.4.1.26149.10.2.3.4.1.3.0','OctetString',dic_result[i][j]]},host_data[0].ip_address,host_data[0].snmp_port,host_data[0].snmp_write_community,{'vap_select':['1.3.6.1.4.1.26149.10.2.3.1.2.0','Integer32',selected_vap]})
                if result["success"] == 0 or result["success"] == '0':
                    for k in result["result"]:
                        if k=='vap_select':
                            continue
                        if result["result"][k] != 0:                            
                            if errorStatus.has_key(result["result"][i]):
                                errorIndex = 1
                                result["result"][i] = errorStatus[result["result"][i]]
                                if len(mac_length)>0:
                                    mac_length = mac_length - 1
                                
                        else:
                            sqlalche_obj.db.execute("Insert into %s values(NULL,'%s','%s','%s','%s')"%('ap25_aclMacTable',host_data[0].config_profile_id,vap_selection_id,vap_index,dic_result[i][j]))
                            vap_index = vap_index+1
                            m = m+1
                            final_result = {"success":0,"result":"%s Mac are added"%(m)}
                else:
                    if 53 in result["result"]:
                        if m>0:
                            final_result = {"success":1,"result":"%s Mac are added.No Response From Device.Please Try Again for remaining macaddresses"%(m)}
                        else:
                            final_result = {"success":1,"result":"No Response From Device.Please Try Again for remaining macaddresses"}
                    elif 51 in result["result"]:
                        if m>0:
                            final_result = {"success":1,"result":"%s Mac are added.But after that network is unreachable"%(m)}
                        else:
                            final_result =  {"success":1,"result":"Network is unreachable"}
                    elif 99 in result["result"]:
                        if m>0:
                            final_result = {"success":1,"result":"%s Mac are added.But after that UNMP has encountered an unexpected error"%(m)}
                        else:
                            final_result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
                    break
            sqlalche_obj.sql_alchemy_db_connection_close()   
            if errorIndex == 1:
                return result
            else: 
                return final_result
        
    def delete_acl(self,host_id,device_type_id,dic_result,selected_vap,vap_selection_id):
        global sqlalche_obj
        m = 0
        sqlalche_obj.sql_alchemy_db_connection_open()
        final_result = {}
        errorIndex = 0
        host_data = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id == host_id).all()
        for i in dic_result:
            if i == "success":
                continue
            mac_length = len(dic_result[i])
            for j in range(0,len(dic_result[i])):
                result = pysnmp_seter({i:['1.3.6.1.4.1.26149.10.2.3.4.1.4.0','OctetString',dic_result[i][j]]},host_data[0].ip_address,host_data[0].snmp_port,host_data[0].snmp_write_community,{'vap_select':['1.3.6.1.4.1.26149.10.2.3.1.2.0','Integer32',selected_vap]})
                if result["success"] == 0 or result["success"] == '0':
                    for k in result["result"]:
                        if k=='vap_select':
                            continue
                        if result["result"][k] != 0:
                            if errorStatus.has_key(result["result"][i]):
                                result["result"][i] = errorStatus[result["result"][i]]
                                errorIndex = 1
                                if len(mac_length)>0:
                                    mac_length = mac_length - 1

                        else:
                            sqlalche_obj.db.execute("delete from ap25_aclMacTable where macaddress='%s' and vapselection_id='%s'"%(dic_result[i][j],vap_selection_id))
                            m = m+1
                            final_result = {"success":0,"result":"%s Mac are Deleted"%(m)}
                else:
                    if 53 in result["result"]:
                        if m>0:
                            final_result = {"success":1,"result":"%s Mac are deleted.No Response From Device.Please Try Again for remaining macaddresses"%(m)}
                        else:
                            final_result = {"success":1,"result":"No Response From Device.Please Try Again for remaining macaddresses"}
                    elif 51 in result["result"]:
                        if m>0:
                            final_result = {"success":1,"result":"%s Mac are deleted.But after that network is unreachable"%(m)}
                        else:
                            final_result =  {"success":1,"result":"Network is unreachable"}
                    elif 99 in result["result"]:
                        if m>0:
                            final_result = {"success":1,"result":"%s Mac are deleted.But after that UNMP has encountered an unexpected error"%(m)}
                        else:
                            final_result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
                    break
            sqlalche_obj.sql_alchemy_db_connection_close()
            if errorIndex == 1:
                return result
            else: 
                return final_result
    
    def delete_all_mac(self,host_id,device_type_id,selected_vap,vap_selection_id):
        global sqlalche_obj
        global errorStatus
        sqlalche_obj.sql_alchemy_db_connection_open()
        result = {}
        fianl_result = {}
        errorIndex = 0
        host_data = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id == host_id).all()
        result = pysnmp_seter({'delete_mac':['1.3.6.1.4.1.26149.10.2.3.4.1.5.0','Integer32',1]},host_data[0].ip_address,host_data[0].snmp_port,host_data[0].snmp_write_community,{'vap_select':['1.3.6.1.4.1.26149.10.2.3.1.2.0','Integer32',selected_vap]})
        if result["success"] == 0 or result["success"] == '0':
            for k in result["result"]:
                if k=='vap_select':
                    continue
                if errorStatus.has_key(result["result"][k]):
                    result["result"][k] = errorStatus[result["result"][k]]
                    errorIndex = 1
                else:
                    sqlalche_obj.db.execute("delete from ap25_aclMacTable where vapselection_id='%s'"%(vap_selection_id))   
                    final_result = {'success':0,'result':'All Mac Deleted SuccessFully'} 

        else:
            if 53 in result["result"]:
                final_result = {"success":1,"result":"No Response From Device.Please Try Again for remaining macaddresses"}
            elif 51 in result["result"]:
                final_result =  {"success":1,"result":"Network is unreachable"}
            elif 99 in result["result"]:
                final_result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
        sqlalche_obj.sql_alchemy_db_connection_close()
        if errorIndex == 1:
            return result
        else: 
            return final_result

class APRadioState(object):
    def radio_enable_disable(self,host_id,admin_state,state):
        global sqlalche_obj
        global errorStatus
        try:
            snmp_result = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id==host_id).all()
            oid_data = sqlalche_obj.session.query(Ap25Oids.oid,Ap25Oids.indexes,Ap25Oids.oid_type).filter(Ap25Oids.oid_name==admin_state).all()            
            oid_dic = {admin_state:[str(oid_data[0].oid)+str(oid_data[0].indexes),oid_data[0].oid_type,state]}
            snmp_result = pysnmp_seter(oid_dic,host_data[0].ip_address,int(host_data[0].snmp_port),host_data[0].snmp_write_community)
            if snmp_result['success']==0:
                for i in snmp_result['result']:
                    if snmp_result['result'][i]==0:
                        main_admin_data = sqlalche_obj.session.query(Ap25RadioSetup).filter(Ap25RadioSetup.config_profile_id==host_data[0].config_profile_id).all()
                        main_admin_data[0].radioState = state
                    sqlalche_obj.session.commit()
            else:
                for i in snmp_result["result"]:
                    if snmp_result["result"][i] != 0:
                        if i in errorStatus:
                            snmp_result["result"] = errorStatus[i]
                    
        except:
            snmp_result['success']=1
            snmp_result['result']=str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_result

    def chk_radio_status(self,host_id):
        result = {'success':0,'result':""}
        try:
            global sqlalche_obj
            radio_status = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_id==None or host_id == "" or host_id=="undefined":
                result = {"success":1,"result":"No host exist"}
            else:
                host_id_list = host_id.split(",")
                for i in range(0,len(host_id_list)):
                    host_data_list = sqlalche_obj.session.query(Hosts.config_profile_id).filter(Hosts.host_id==host_id_list[i]).all() 
                    if len(host_data_list)>0:
                        radio_state = sqlalche_obj.session.query(Ap25RadioSetup.radioState).filter(Ap25RadioSetup.config_profile_id==host_data_list[0].config_profile_id).all()
                        radio_status.update({host_id_list[i]:radio_state[0].radioState if len(radio_state)>0 else ""})
                result = {'success':0,'result':radio_status}
        except Exception as e:
            result['success']=1
            result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result
#obj = APRadioState()

#print obj.radio_enable_disable(70,'radioSetup.radioState',1)
#print obj.chk_radio_status("70")
##obj = APCommonSetValidation()
####
##print obj.vap_set(42,'ap25', {'vapWEPsecuritySetup.vapWEPprimaryKey': '4', 'success': 0, 'basicVAPsetup.vapBeaconInterval': '100', 'vapWEPsecuritySetup.vapWEPmode': '1', 'basicVAPsetup.vapESSID': 'anuj', 'vapWEPsecuritySetup.vapWEPkey4': '12345', 'vapWEPsecuritySetup.vapWEPkey1': '', 'vapWEPsecuritySetup.vapWEPkey2': '12345', 'vapWEPsecuritySetup.vapWEPkey3': '12345'},\
##                1,17)

##obj = Reconciliation()
######
##print obj.update_configuration(46,'ap25')
