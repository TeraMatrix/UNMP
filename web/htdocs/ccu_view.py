from utility import UNMPDeviceType
from common_controller import MakeSelectListUsingDictionary
from idu_profiling_bll import IduGetData

class CCUForms(object):    
    @staticmethod
    def enable_disable_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        select_list_name_value_dic = {}
        select_list_name_value_dic = {'name':['Disable','Enable'],'value':[0,1]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_list_name_value_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)

    @staticmethod
    def high_low_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        select_list_name_value_dic = {}
        select_list_name_value_dic = {'name':['Low To High','High To Low'],'value':[1,2]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_list_name_value_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)

    
    @staticmethod
    def battery_panel_form(host_id,selected_device):
        obj_bll = IduGetData()
        battery_panel = obj_bll.common_get_data("CcuBatteryPanelConfigTable",host_id)
        form_str = ""
        form_str = ""
        form_str += "<form id = \"battery_panel_form\" name = \"battery_panel_form\" action=\"battery_panel_action.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Battery Capacity</label>\
                            <input type = \"text\" maxlength=\"4\" id =\"ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity\" name = \"ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;100 to 1000</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Solar Panel</label>\
                            <input type = \"text\" maxlength=\"3\" id =\"ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP\" name = \"ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;0 to 999</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Solar Panel Count</label>\
                            <input type = \"text\" maxlength=\"3\"  id =\"ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount\" name = \"ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;0 to 255</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">New battery Installation Date</label>\
                            <input type = \"text\" maxlength=\"12\"  id =\"ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate\" name = \"ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;Upto 12 characters allowed</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ccu_common_submit\" value=\"Save\" id=\"ccu_save\" onClick=\"return commonFormSubmit('battery_panel_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\"  id=\"ccu_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('battery_panel_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('battery_panel_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('battery_panel_form',this)\" class=\"yo-small yo-button\" />\
                        </div>\
                    </form>\
                    "%("" if len(battery_panel)==0 else "" if battery_panel[0].ccuBPCSiteBatteryCapacity==None else battery_panel[0].ccuBPCSiteBatteryCapacity,\
                    "" if len(battery_panel)==0 else "" if battery_panel[0].ccuBPCSiteSolarPanelwP==None else battery_panel[0].ccuBPCSiteSolarPanelwP,\
                    "" if len(battery_panel)==0 else "" if battery_panel[0].ccuBPCSiteSolarPanelCount==None else battery_panel[0].ccuBPCSiteSolarPanelCount,\
                    "" if len(battery_panel)==0 else "" if battery_panel[0].ccuBPCNewBatteryInstallationDate==None else battery_panel[0].ccuBPCNewBatteryInstallationDate)
        return form_str
    
    @staticmethod
    def aux_io_form(host_id,selected_device):
        obj_bll = IduGetData()
        aux_data = obj_bll.common_get_data("CcuAuxIOTable",host_id)
        form_str = ""
        form_str = ""
        form_str += "<form id = \"aux_form\" name = \"aux_form\" action=\"aux_action.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">External Output 1</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">External Output 1</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">External Output 1</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">External Input 1 Alarm</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">External Input 2 Alarm</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">External Input 3 Alarm</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ccu_common_submit\" value=\"Save\" id=\"ccu_save\" onClick=\"return commonFormSubmit('aux_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\"  id=\"ccu_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('aux_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('aux_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('aux_form',this)\" class=\"yo-small yo-button\" />\
                        </div>\
                    </form>\
                    "%(CCUForms.enable_disable_select_list("" if len(aux_data)==0 else "" if aux_data[0].ccuAIExternalOutput1==None else aux_data[0].ccuAIExternalOutput1\
                    ,"enabled","ccuOAM.ccuAuxIOTable.ccuAIExternalOutput1",False,"External Output 1"),\
                    CCUForms.enable_disable_select_list("" if len(aux_data)==0 else "" if aux_data[0].ccuAIExternalOutput2==None else aux_data[0].ccuAIExternalOutput2,\
                    "enabled","ccuOAM.ccuAuxIOTable.ccuAIExternalOutput2",False,"External Output 2"),\
                    CCUForms.enable_disable_select_list("" if len(aux_data)==0 else "" if aux_data[0].ccuAIExternalOutput3==None else aux_data[0].ccuAIExternalOutput3,\
                    "enabled","ccuOAM.ccuAuxIOTable.ccuAIExternalOutput3",False,"External Output 3"),\
                    CCUForms.high_low_select_list("" if len(aux_data)==0 else "" if aux_data[0].ccuAIExternalInput1AlarmType==None else aux_data[0].ccuAIExternalInput1AlarmType,\
                    "enabled","ccuOAM.ccuAuxIOTable.ccuAIExternalInput1",False,"External Input 1 Alarm"),\
                    CCUForms.high_low_select_list("" if len(aux_data)==0 else "" if aux_data[0].ccuAIExternalInput2AlarmType==None else aux_data[0].ccuAIExternalInput2AlarmType,\
                    "enabled","ccuOAM.ccuAuxIOTable.ccuAIExternalInput2",False,"External Input 2 Alarm"),\
                    CCUForms.high_low_select_list("" if len(aux_data)==0 else "" if aux_data[0].ccuAIExternalInput3AlarmType==None else aux_data[0].ccuAIExternalInput3AlarmType,\
                    "enabled","ccuOAM.ccuAuxIOTable.ccuAIExternalInput3",False,"External Input 3 Alarm"))
        return form_str

    
    @staticmethod
    def alarm_threshold_form(host_id,selected_device):
        obj_bll = IduGetData()
        alarm_threshold_data = obj_bll.common_get_data("CcuAlarmAndThresholdTable",host_id)
        form_str = ""
        form_str = ""
        form_str += "<form id = \"alarm_threshold_form\" name = \"alarm_threshold_form\" action=\"alarm_threshold_action.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">High Temperature Alarm</label>\
                            <input type = \"text\" maxlength=\"3\"  id =\"ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm\" name = \"ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;0 to 100</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">PSM Request</label>\
                            <input type = \"text\" maxlength=\"2\"  id =\"ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest\" name = \"ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;0 to 80</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">SMPS Max Current Limit</label>\
                            <input type = \"text\" maxlength=\"5\"  id =\"ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit\" name = \"ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;0 to 60000</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Peak Load Current</label>\
                            <input type = \"text\" maxlength=\"3\"  id =\"ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent\" name = \"ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;0 to 100</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ccu_common_submit\" value=\"Save\" id=\"ccu_save\" onClick=\"return commonFormSubmit('alarm_threshold_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\"  id=\"ccu_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('alarm_threshold_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('alarm_threshold_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('alarm_threshold_form',this)\" class=\"yo-small yo-button\" />\
                        </div>\
                    </form>\
                    "%("" if len(alarm_threshold_data)==0 else "" if alarm_threshold_data[0].ccuATHighTemperatureAlarm==None else alarm_threshold_data[0].ccuATHighTemperatureAlarm,\
                      "" if len(alarm_threshold_data)==0 else "" if alarm_threshold_data[0].ccuATPSMRequest==None else alarm_threshold_data[0].ccuATPSMRequest,\
                      "" if len(alarm_threshold_data)==0 else "" if alarm_threshold_data[0].ccuATSMPSMaxCurrentLimit==None else alarm_threshold_data[0].ccuATSMPSMaxCurrentLimit,\
                      "" if len(alarm_threshold_data)==0 else "" if alarm_threshold_data[0].ccuATPeakLoadCurrent==None else alarm_threshold_data[0].ccuATPeakLoadCurrent)
        return form_str

    @staticmethod
    def unmp_ip_form(host_id,selected_device):
        obj_bll = IduGetData()
        site_info_data = obj_bll.common_get_data("CcuSiteInformationTable",host_id)
        form_str = ""
        form_str = ""
        form_str += "<form id = \"unmp_ip_form\" name = \"unmp_ip_form\" action=\"unmp_ip_action.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Site Name</label>\
                            <input type = \"text\" maxlength=\"64\"  id =\"ccuOAM.ccuSiteInformationTable.ccuSITSiteName\" name = \"ccuOAM.ccuSiteInformationTable.ccuSITSiteName\" value = \"%s\" maxsize = \"15\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;Upto 64 characters allowed</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ccu_common_submit\" value=\"Save\" id=\"ccu_save\" onClick=\"return commonFormSubmit('unmp_ip_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\"  id=\"ccu_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('unmp_ip_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('unmp_ip_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('unmp_ip_form',this)\" class=\"yo-small yo-button\" />\
                        </div>\
                    </form>\
                    "%("" if len(site_info_data)==0 else "" if site_info_data[0].ccuSITSiteName==None else site_info_data[0].ccuSITSiteName)
        return form_str

    @staticmethod
    def peer_form(host_id,selected_device):
        obj_bll = IduGetData()
        peer_data = obj_bll.common_get_data("CcuPeerInformationTable",host_id)
        form_str = ""
        form_str = ""
        form_str += "<form id = \"peer_form\" name = \"peer_form\" action=\"peer_action.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Peer 1 MAC</label>\
                            <input type = \"text\" maxlength=\"18\" id =\"ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID\" name = \"ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID\" value = \"%s\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Peer 2 MAC</label>\
                            <input type = \"text\" maxlength=\"18\" id =\"ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID\" name = \"ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID\" value = \"%s\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Peer 3 MAC</label>\
                            <input type = \"text\" maxlength=\"18\" id =\"ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID\" name = \"ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID\" value = \"%s\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Peer 4 MAC</label>\
                            <input type = \"text\" maxlength=\"18\" id =\"ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID\" name = \"ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID\" value = \"%s\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ccu_common_submit\" value=\"Save\" id=\"ccu_save\" onClick=\"return commonFormSubmit('peer_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\"  id=\"ccu_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('peer_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('peer_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('peer_form',this)\" class=\"yo-small yo-button\" />\
                        </div>\
                    </form>\
                    "%("" if len(peer_data)==0 else "" if peer_data[0].ccuPIPeer1MACID==None else peer_data[0].ccuPIPeer1MACID,\
                      "" if len(peer_data)==0 else "" if peer_data[0].ccuPIPeer2MACID==None else peer_data[0].ccuPIPeer2MACID,\
                      "" if len(peer_data)==0 else "" if peer_data[0].ccuPIPeer3MACID==None else peer_data[0].ccuPIPeer3MACID,\
                      "" if len(peer_data)==0 else "" if peer_data[0].ccuPIPeer4MACID==None else peer_data[0].ccuPIPeer4MACID)
        return form_str

    @staticmethod
    def control_form(host_id,selected_device):
        obj_bll = IduGetData()
        control_data = obj_bll.common_get_data("CcuControlTable",host_id)
        form_str = ""
        form_str = ""
        form_str += "<form id = \"ccu_control\" name = \"ccu_control\" action=\"ccu_control_form.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Load Turn Off</label>\
                            <input type = \"text\" maxlength=\"4\" id =\"ccuOAM.ccuControlTable.ccuCTLoadTurnOff\" name = \"ccuOAM.ccuControlTable.ccuCTLoadTurnOff\" value = \"%s\"/>\
                            <span style=\"font-size: 9px;\">&nbsp;&nbsp;0-9999</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">SMPS Charging</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ccu_common_submit\" value=\"Save\" id=\"ccu_save\" onClick=\"return commonFormSubmit('ccu_control',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\"  id=\"ccu_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('ccu_control',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('ccu_control',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ccu_common_submit\" id=\"ccu_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('ccu_control',this)\" class=\"yo-small yo-button\" />\
                        </div>\
                    </form>\
                    "%("" if len(control_data)==0 else "" if control_data[0].ccuCTLoadTurnOff==None else control_data[0].ccuCTLoadTurnOff,\
                      CCUForms.enable_disable_select_list("" if len(control_data)==0 else "" if control_data[0].ccuCTSMPSCharging==None else control_data[0].ccuCTSMPSCharging\
                    ,"enabled","ccuOAM.ccuControlTable.ccuCTSMPSCharging",False,"SMPS Charging"))
        return form_str
    
    
class CCUProfiling(object):
    
    @staticmethod
    def ccu_listing():
        table_view = "<div>"
        table_view = "<div>"
        table_view+= "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"device_data_table\" style=\"text-align:center\">\
                        <thead>\
                            <tr>\
                                \
                                <th>Host Alias</th>\
                                <th>Host Group</th>\
                                <th>IP Address</th>\
                                <th>MAC Address</th>\
                                <th>System Voltage</th>\
                                <th>Solar Current</th>\
                                <th>Temperature</th>\
                                <th>Actions</th>\
                            </tr>\
                        </thead>\
                    </table></div>"
        return table_view
    
    @staticmethod
    def ccu_profiling_form(host_id,device_type,device_list_parameter):
        """
        @author : Anuj Samariya 
        @param h : html Class Object
        @var html : this is html Class Object defined globally 
        @var host_id : this is used to store the Host Id which is come from the page
        @device_list_param : this is used to store all the details of device 
        @tab_str : this is used to store the form string
        @var odu_configuration_object : this is used to store the object of class OduConfiguration  
        @since : 20 August 2011
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to write the forms of odu100 on the page
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
##        if device_list_parameter == "" or device_list_parameter ==[]:
##            return "No Configuration Profile Exist"
##        elif device_list_parameter[0].config_profile_id == None or device_list_parameter[0].config_profile_id=="":
##            return "No Configuration Exist.Please Add Host Again"
##        else:
        tab_str = ''
        tab_str += "<div class=\"yo-tabs\" id=\"config_tabs\" style=\"display:block\">\
                        <ul>\
                            <li><a class=\"active\" href=\"#content_1\">Battery Panel</a></li>\
                            <li><a href=\"#content_2\">AUX IO</a></li>\
                            <li><a href=\"#content_3\">Alarm Threshold</a></li>\
                            <li><a href=\"#content_4\">Peer Info</a></li>\
                            <li><a href=\"#content_5\">CCU Control</a></li>\
                            <li><a href=\"#content_6\">UNMP IP</a></li>\
                        </ul>\
                        <div id=\"content_1\" class=\"tab-content form-div\" style=\"display:block;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                        </div>\
                        <div id=\"content_2\" class=\"tab-content form-div\" style=\"display:block;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                        </div>\
                        <div id=\"content_3\" class=\"tab-content form-div\" style=\"display:block;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                        </div>\
                        <div id=\"content_4\" class=\"tab-content form-div\" style=\"display:block;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                        </div>\
                        <div id=\"content_5\" class=\"tab-content form-div\" style=\"display:block;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                        </div>\
                        <div id=\"content_6\" class=\"tab-content form-div\" style=\"display:block;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                        </div>\
                        <input type=\"hidden\" name=\"host_id\" id=\"host_id\" value=\"%s\"/>\
                        <input type=\"hidden\" name=\"device_type_id\" id=\"device_type_id\" value=\"%s\"/>"\
                        %(CCUForms.battery_panel_form(host_id,device_type),CCUForms.aux_io_form(host_id,device_type),\
                        CCUForms.alarm_threshold_form(host_id,device_type),CCUForms.peer_form(host_id,device_type),CCUForms.control_form(host_id,device_type),\
                        CCUForms.unmp_ip_form(host_id,device_type),host_id,device_type)
        return tab_str
    
    @staticmethod
    def ccu_div(ip_address,mac_address,host_id):
        profile_str = ""
        profile_str += "<div id=\"ccu_form_div\" class=\"form-div\" style=\"margin-top: 56px;\"></div>"
        profile_str +="<div class=\"form-div-footer\">\
                            <div style=\"float:right;margin-right:20px\">\
                                <!--<input type=\"button\" id=\"snmps_charging\" name=\"snmps_charging\" value=\"SMPS Charging\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"restore_default\" name=\"restore_default\" value=\"Restore Default\" class=\"yo-small yo-button\"/>-->\
                                <input type=\"button\" id=\"ccu_reconcile\" name=\"ccu_reconcile\" value=\"Reconciliation\"  class=\"yo-small yo-button\"/>\
                                <input type=\"hidden\" name=\"ip_address\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"mac_address\" value=\"%s\" />\
                                <input type=\"hidden\" name=\"host_id\" value=\"%s\" />\
                            </div>\
                        </div>"%(ip_address,mac_address,host_id)
        return profile_str
    
    @staticmethod
    def ccu_profile_call(host_id,device_type,device_list_parameter):
        tab_str = ""
        if host_id == "" or host_id == "None":
            tab_str+="There is No Host Exist</div>"
        else:
            if device_type == "ccu":
                tab_str += CCUProfiling.ccu_profiling_form(host_id,device_type,device_list_parameter)# function call , it is used to make a form of selected profiling  
        return tab_str
