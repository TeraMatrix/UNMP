#!/usr/bin/python2.6
from utility import UNMPDeviceType
from common_controller import MakeSelectListUsingDictionary
from ap_profiling_bll import APGetData
from common_bll import Essential

# create the global object
obj_essential = Essential ()
host_status_dic = {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade', 3:'Restore default config', 4:'Flash commit', 5:'Reboot', 6:'Site survey', 7:'Calculate BW', 8:'Uptime service', 9:'Statistics gathering', 10:'Reconciliation', 11:'Table reconciliation', 12:'Set operation', 13:'Live monitoring', 14:'Status capturing',15:'Refreshing Site Survey','16':'Refreshing RA Channel List'}
contory_code_val=0

class APForms(object):
   
    @staticmethod
    def country_code_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        global contory_code_val
        contory_code_val=selected_field
        vap_select_dic = {} 
        #{'name':['DISABLE','ENABLE'],'value':[0,1]}
        country_code_dic = {"name":['Default','Debug','Albania','Algeria','Argentina','Armenia','Australia','Austria','Azerbaijan','Bahrain','Belarus','Belgium','Belize','Bolvia','Bosnia-herzegovina','Brazil',\
                                    'Brunei-darussalam','Bulgaria','Canada','Chile','China','Colombia','Costa-rica','Croatia','Cyprus','Czech-republic','Denmark','Dominican-republic','Ecuador','Egypt',\
                                    'El-salvador','Estonia','Finland','France','Georgia','Germany','Greece','Guatemala','Honduras',\
                                    'Hong-kong','Hungary','Iceland','India','Indonesia','Iran','Ireland','Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya',\
                                    'North-korea','Kuwait','Latvia','Lebanon','Liechtenstein','Lithuania','Luxembourg','Macau','Macedonia','Malaysia','Malta','Mexico','Monaco','Morocco','Netherlands','New-zealand','Norway','Oman',\
                                    'Pakistan','Panama','Peru','Philippines','Poland','Portugal','Puerto-rico','Qatar','Romania','Russia','Saudi-arabia','Serbia-montenegro','Singapore','Slovak-republic','Slovenia','South-africa',\
                                    'Spain','Sri-lanka','Sweden','Switzerland','Syria','Taiwan','Thailand','Trinidad-and-tobago','Tunisia','Turkey','Ukraine','United-arab-emirates','United-kingdom','United-states','Uruguay',\
'Uzbekistan','Venezuela','Viet-nam','Yemen','Zimbawe'],\
                                "value":[0,511,8,12,32,51,36,40,31,48,112,56,84,68,70,76,96,100,124,152,156,170,188,191,196,203,208,214,218,818,222,\
                                        233,246,250,268,276,300,320,340,344,348,352,\
                                        356,360,364,372,376,380,388,392,400,398,404,408,414,428,422,438,440,442,446,807,458,470,484,492,504,528,554,\
                                        578,512,586,591,604,608,616,620,630,634,642,643,682,891,\
                                        702,703,705,710,724,144,752,756,760,158,764,780,788,792,804,784,826,840,858,860,862,704,887,716]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(country_code_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)
    @staticmethod
    def vap_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        vap_select_dic = {} 
        #{'name':['DISABLE','ENABLE'],'value':[0,1]}
        vap_select_dic = {"name":[1,2,3,4,5,6,7,8],"value":[1,2,3,4,5,6,7,8]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(vap_select_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)
    
    @staticmethod
    def radio_channel_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        channel_dic = {}
        global contory_code_val
        j = 1
        i=2.412
        last=2.479
        if contory_code_val==0:
            last=2.475
        while(i<last):
            channel_dic.setdefault('name',[]).append("Channel-%s"%(j)+":%s"%(i))
            channel_dic.setdefault('value',[]).append(j)
            i=i+0.005
            j=j+1
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(channel_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)
    
    @staticmethod
    def radio_mode_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        mode_dic = {}
        mode_dic={'name':['WiFi 11g','WiFi 11gn HT20','WiFi 11gn HT40+','WiFi 11gn HT40-'],'value':['0','1','2','3']}        
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(mode_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)

    @staticmethod
    def txpower_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        txpower_dic = {}
        txpower_dic.setdefault('name',[]).append("Default")
        txpower_dic.setdefault('value',[]).append(0)
        for i in range(1,31):
            txpower_dic.setdefault('name',[]).append(i)
            txpower_dic.setdefault('value',[]).append(i)
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(txpower_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)
    
    @staticmethod
    def vap_list(select_vaps,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        vap_dic = {}
        for i in range(0,select_vaps):
            vap_dic.setdefault('name',[]).append("VAP %s"%(i+1))
            vap_dic.setdefault('value',[]).append(i+1)
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(vap_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)
    
    @staticmethod
    def threshold_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        threshold_dic = {}
        threshold_dic={'name':['Off','Fixed'],'value':['0','1']}        
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(threshold_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)

    
    @staticmethod
    def radio_configuration(host_id,selected_device):
        obj_bll_get_data = APGetData()
        get_radio_data = obj_bll_get_data.ap_get_data('Ap25RadioSetup',host_id)
        form_view=""
        form_view+="<form id=\"ap_radio_form\" name=\"ap_radio_form\" action=\"ap_radio_form_action.py\" method=\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Radio</label>\
                            <input type=\"radio\" value=\"1\" name=\"radioSetup.radioState\" />\
                                Enable &nbsp;\
                            <input type=\"radio\" value=\"0\" name=\"radioSetup.radioState\" />\
                                Disable &nbsp;\
                            <input type=\"hidden\" name=\"radioState\" id=\"radioState\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\"  style=\"width:550px;\">\
                            <label class=\"lbl\">Startup Mode</label>\
                            <input id=\"startup_standard\" type=\"radio\" value=\"0\" name=\"radioSetup.radioAPmode\" onClick=\"Toggleradio();\"/>\
                            Standard&nbsp;\
                            <input id=\"startup_rootap\" type=\"radio\" value=\"1\" name=\"radioSetup.radioAPmode\" onClick=\"Toggleradio();\"/>\
                            RootAP&nbsp;\
                            <input id=\"startup_repeater\" type=\"radio\" value=\"2\" name=\"radioSetup.radioAPmode\" onClick=\"Toggleradio();\"/>\
                            Repeater&nbsp;\
                            <input id=\"startup_client\" type=\"radio\" value=\"3\" name=\"radioSetup.radioAPmode\" onClick=\"Toggleradio();\"/>\
                            Client&nbsp;\
                            <input id=\"startup_multi\" type=\"radio\" value=\"4\" name=\"radioSetup.radioAPmode\" onClick=\"Toggleradio();\"/>\
                            Multi AP&nbsp;\
                            <input id=\"startup_multivlan\" type=\"radio\" value=\"5\" name=\"radioSetup.radioAPmode\" onClick=\"Toggleradio();\"/>\
                            Multi VLAN\
                            <input type=\"hidden\" name=\"startupmode\" id=\"startupmode\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\" style=\"display:none\" id=\"manage_vlan_div\">\
                            <label class=\"lbl\">Management Vlan</label>\
                            <input id=\"Enbl_mngmtvlan\" type=\"radio\" name=\"radioSetup.radioManagementVLANstate\" value=\"1\" />\
                            Enable\
                            <input id=\"Dsbl_mngmtvlan\" type=\"radio\" name=\"radioSetup.radioManagementVLANstate\" value=\"0\" />\
                            Disable<br/><br/>\
                            <div style=\"margin-left: 140px;width:300px;font-size:9px\"><b>[Caution:If you Enable the Management VLAN You may lose the connectivity to Access Point throught ethernet.\
                            Verify that packet coming from ethernet has same managment tag for connectivity.]</b></div>\
                            <input type=\"hidden\" name=\"managevlan\" id=\"managevlan\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Country</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Number of VAPs</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Channel Frequency</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Wifi Mode</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Channel Width</label>\
                            <input type=\"radio\" value=\"0\" id=\"radioChannelWidth20\" name=\"radioSetup.radioChannelWidth\" />\
                            HT20&nbsp; \
                            <input type=\"radio\" value=\"1\" id=\"radioChannelWidth40\" name=\"radioSetup.radioChannelWidth\" />\
                            HT20/40&nbsp;\
                            <input type=\"hidden\" name=\"channelwidth\" id=\"channelwidth\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">TX Chain Mask</label>\
                            <input type=\"radio\" value=\"0\" id=\"txchain1\" name=\"radioSetup.radioTXChainMask\" />\
                            1 Chain &nbsp; \
                            <input type=\"radio\" value=\"1\" id=\"rxchain2\" name=\"radioSetup.radioTXChainMask\" />\
                            2 Chain &nbsp;\
                            <input type=\"radio\" value=\"2\" id=\"txeeprom\" name=\"radioSetup.radioTXChainMask\" />\
                            EEPROM &nbsp;\
                            <input type=\"hidden\" name=\"txchainmask\" id=\"txchainmask\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">RX Chain Mask</label>\
                            <input type=\"radio\" value=\"0\" id=\"rxchain1\" name=\"radioSetup.radioRXChainMask\" />\
                            1 Chain &nbsp; \
                            <input type=\"radio\" value=\"1\" id=\"rxchain2\" name=\"radioSetup.radioRXChainMask\" />\
                            2 Chain &nbsp;\
                            <input type=\"radio\" value=\"2\" id=\"rxeeprom\" name=\"radioSetup.radioRXChainMask\" />\
                            EEPROM &nbsp;\
                            <input type=\"hidden\" name=\"rxchainmask\" id=\"rxchainmask\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">TX Power</label>\
                            %s\
                             dBm\
                        </div>\
                        <div id=\"gradingIndex\" class=\"row-elem\" >\
                            <label class=\"lbl\">Guard Interval</label>\
                            <input type=\"radio\" value=\"0\" name=\"radioSetup.radioGatingIndex\" />\
                            Short&nbsp;\
                            <input type=\"radio\" value=\"1\" name=\"radioSetup.radioGatingIndex\" />\
                            Long&nbsp;\
                            <input type=\"hidden\" name=\"gatingindex\" id=\"gatingindex\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Aggregation</label>\
                            <input type=\"radio\" value=\"1\" id=\"chk_AMPDU_Enable\" name=\"radioSetup.radioAggregation\" />\
                            Enabled&nbsp; \
                            <input type=\"radio\" value=\"0\" id=\"chk_AMPDU_Disable\" name=\"radioSetup.radioAggregation\" />\
                            Disabled&nbsp;\
                            <input type=\"hidden\" name=\"aggregation\" id=\"aggregation\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Aggregation Frames</label>\
                            <input type=\"text\" value=\"%s\" id=\"radioSetup.radioAggFrames\" name=\"radioSetup.radioAggFrames\" maxlength=\"16\" /> 2- 64\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Aggregation Size</label>\
                            <input type=\"text\" value=\"%s\" id=\"radioSetup.radioAggSize\" name=\"radioSetup.radioAggSize\" maxlength=\"16\" /> 1024 - 65535 (Bytes)\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Aggregation Min Size</label>\
                            <input type=\"text\" value=\"%s\" id=\"radioSetup.radioAggMinSize\" name=\"radioSetup.radioAggMinSize\" maxlength=\"16\" /> 1024 - 65535 (Bytes)\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ap_common_submit\" value=\"Save\" id=\"id_save\" onClick=\"return commonFormSubmit('ap_radio_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name =\"ap_common_submit\"  id=\"id_retry\" value=\"Retry\"  onClick=\"return commonFormSubmit('ap_radio_form',this)\" class=\"yo-small yo-button\" style=\"display:none\"/>\
                            <input type=\"submit\" name =\"ap_common_submit\" id=\"id_cancel\" value=\"Cancel\"  onClick=\"return commonFormSubmit('ap_radio_form',this)\" class=\"yo-small yo-button\" style=\"display:none\"/>\
                            <input type=\"submit\" name =\"ap_common_submit\" id=\"id_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_radio_form',this)\" class=\"yo-small yo-button\" style=\"display:none\"/>\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"radio_configuration\" tablename=\"radioSetup\"/>\
                        </div>\
                    </form>"%(get_radio_data[0].radioState if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioAPmode if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioManagementVLANstate if len(get_radio_data)>0 else "",\
                            APForms.country_code_select_list(int(get_radio_data[0].radioCountryCode) if len(get_radio_data)>0 else "","enabled","radioSetup.radioCountryCode",False,"Country"),\
                            APForms.vap_select_list(get_radio_data[0].numberOfVAPs if len(get_radio_data)>0 else "","enabled","radioSetup.numberofVAPs",False,"Vap"),\
                            APForms.radio_channel_select_list(get_radio_data[0].radioChannel if len(get_radio_data)>0 else "","enabled","radioSetup.radioChannel",False,"Channel"),\
                            APForms.radio_mode_select_list(str(get_radio_data[0].wifiMode) if len(get_radio_data)>0 else "","enabled","radioSetup.wifiMode",False,"Mode"),\
                            get_radio_data[0].radioChannelWidth if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioTXChainMask if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioRXChainMask if len(get_radio_data)>0 else "",\
                            APForms.txpower_select_list(get_radio_data[0].radioTxPower if len(get_radio_data)>0 else "","enabled","radioSetup.radioTxPower",False,"TxPower"),\
                            get_radio_data[0].radioGatingIndex if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioAggregation if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioAggFrames if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioAggSize if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioAggMinSize if len(get_radio_data)>0 else ""
                            )    
        return str(form_view)

    @staticmethod
    def vap_configuration(host_id,selected_device):
        obj_bll_get_data = APGetData()
        basic_vap_setup = obj_bll_get_data.ap_get_data('Ap25BasicVAPconfigTable',host_id)
        basic_vap_security = obj_bll_get_data.ap_get_data('Ap25BasicVAPsecurity',host_id)
        wep_data = obj_bll_get_data.ap_get_data('Ap25VapWEPsecurityConfigTable',host_id)
        wpa_data = obj_bll_get_data.ap_get_data('Ap25VapWPAsecurityConfigTable',host_id)
        form_view=""
        form_view+="<form id=\"ap_vap_form\" name=\"ap_vap_form\" action=\"ap_vap_form_action.py\" method=\"get\">\
                        \
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Select VAP</label>\
                            %s\
                        </div>\
                        \
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">ESSID String</label>\
                            <input id=\"basicVAPconfigTable.vapESSID\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"35\" name=\"basicVAPconfigTable.vapESSID\">\
                        </div>\
                        <div class=\"row-elem\" id=\"hide_essid\">\
                            <label class=\"lbl\">Hide ESSID</label>\
                            <input id=\"basicVAPconfigTable.vapHiddenESSIDstate\" type=\"checkbox\" value=\"%s\" name=\"basicVAPconfigTable.vapHiddenESSIDstate\" %s>\
                        </div>\
                        <div class=\"row-elem\" id=\"vlan_id\">\
                            <label class=\"lbl\">VLAN ID</label>\
                            <input id=\"basicVAPconfigTable.vlanId\" type=\"text\" value=\"%s\" maxlength=\"4\" size=\"8\" name=\"basicVAPconfigTable.vlanId\"> 1 - 4095\
                        </div>\
                        <div class=\"row-elem\" id=\"vlan_priority\">\
                            <label class=\"lbl\">VLAN Priority</label>\
                            <input id=\"basicVAPconfigTable.vlanPriority\" type=\"text\" value=\"%s\" maxlength=\"1\" size=\"2\" name=\"basicVAPconfigTable.vlanPriority\"> 0 to 7\
                        </div>\
                        <div class=\"row-elem\" id=\"vap_mode\">\
                            <label class=\"lbl\">VAP Mode</label>\
                            <input type=\"radio\" value=\"0\" name=\"basicVAPconfigTable.vapMode\">\
                            Access Point&nbsp;\
                            <input type=\"radio\" value=\"1\" name=\"basicVAPconfigTable.vapMode\">\
                            WDS Access Point&nbsp;\
                        </div>\
                        <div class=\"row-elem\" id=\"root_mac_address\">\
                            <label class=\"lbl\">Root AP Mac Address</label>\
                            <input id=\"basicVAPconfigTable.vapRadioMac\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"35\" name=\"basicVAPconfigTable.vapRadioMac\">\
                        </div>\
                        <!--<div class=\"row-elem\">\
                            <label class=\"lbl\">Enable Dynamic VLan</label>\
                            <input id=\"chk_dyn_vlan\" type=\"checkbox\" disabled=\"disabled\">\
                            <span>(Dymamic VLAN can be Enabled in RootAP,Standard mode With Enterprise/Radius Support.)</span>\
                        </div>-->\
                        <div class=\"row-elem\" style=\"width:800px\">\
                            <label class=\"lbl\">RTS Threshold</label>\
                            %s\
                            <input id=\"basicVAPconfigTable.vapRTSthresholdValue\" name=\"basicVAPconfigTable.vapRTSthresholdValue\" type=\"text\" value=\"%s\" style=\"margin-left:10px\">\
                            </select> 256 - 2346 (Bytes)\
                        </div>\
                        <div class=\"row-elem\" style=\"width:800px\">\
                            <label class=\"lbl\">Fragmentation Threshold</label>\
                            %s\
                            <input id=\"basicVAPconfigTable.vapFragmentationThresholdValue\" type=\"text\" value=\"%s\" name=\"basicVAPconfigTable.vapFragmentationThresholdValue\" style=\"margin-left:10px\"> 256 - 2346 (Bytes)\
                        </div>\
                        <div class=\"row-elem\" id=\"Beacon\">\
                            <label class=\"lbl\">Beacon Interval</label>\
                            <input id=\"basicVAPconfigTable.vapBeaconInterval\" type=\"text\" style=\"width: 65px;\" value=\"%s\" name=\"basicVAPconfigTable.vapBeaconInterval\"> 40 - 1000 (Milliseconds)\
                        </div>\
                        \
                        <div class=\"row-elem\" style=\"width:1000px\">\
			    <h3>Security Settings</h3></br>\
                            <div id=\"openradio\">\
                                <input id=\"sec_open\" type=\"radio\" name=\"basicVAPconfigTable.vapSecurityMode\" onClick=\"Securitymode();\" \"%s\" value=\"0\">\
                                Open\
                            </div>\
                            <div id=\"opendiv\" style=\"margin-left:30px;\">\
                                <br/><p style=\"font-size:11px\"><b>No Security Applied</b></p>\
                            </div><br/><br/>\
                            <div id=\"wepradio\">\
                                <input id=\"sec_wep\" type=\"radio\" name=\"basicVAPconfigTable.vapSecurityMode\" onClick=\"Securitymode();\" value=\"1\" \"%s\">\
                                WEP\
                            </div><br/>\
                            <div id=\"wepdiv\" style=\"margin-left:30px;\">\
                                <br/><p style=\"font-size:11px\"><b>Simple WEP Security (64 0r 128 bit hardware key)</b></p><br/>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Mode</label>\
                                    <input id=\"wepmode1\" type=\"radio\" value=\"0\" name=\"vapWEPsecurityConfigTable.vapWEPmode\" %s >\
                                    Open\
                                    <input id=\"wepmode2\" type=\"radio\" value=\"1\" name=\"vapWEPsecurityConfigTable.vapWEPmode\" %s >\
                                    Shared\
                                    <input id=\"wepmode4\" type=\"radio\" value=\"2\" name=\"vapWEPsecurityConfigTable.vapWEPmode\" %s>\
                                    Auto \
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Key1</label>\
                                    <input id=\"vapWEPsecurityConfigTable.vapWEPkey1\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"30\" name=\"vapWEPsecurityConfigTable.vapWEPkey1\">\
                                    <input id=\"Wepkey1_chk\" type=\"radio\" value=\"1\" name=\"vapWEPsecurityConfigTable.vapWEPprimaryKey\" maxlength=\"20\" %s> Primary Key (Hexadecimal : A-F, a-f, 0-9 Ascii : A-Z, a-z, 0-9 Special : ! @ # are allowed)\
                                    Primary Key\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Key2</label>\
                                    <input id=\"vapWEPsecurityConfigTable.vapWEPkey2\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"30\" name=\"vapWEPsecurityConfigTable.vapWEPkey2\" maxlength=\"20\">\
                                    <input id=\"Wepkey2_chk\" type=\"radio\" value=\"2\" name=\"vapWEPsecurityConfigTable.vapWEPprimaryKey\" %s > Primary Key (Hexadecimal : A-F, a-f, 0-9 Ascii : A-Z, a-z, 0-9 Special : ! @ # are allowed)\
                                    Primary Key\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Key3</label>\
                                    <input id=\"vapWEPsecurityConfigTable.vapWEPkey3\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"30\" name=\"vapWEPsecurityConfigTable.vapWEPkey3\" maxlength=\"20\">\
                                    <input id=\"Wepkey3_chk\" type=\"radio\" value=\"3\" name=\"vapWEPsecurityConfigTable.vapWEPprimaryKey\" %s > Primary Key (Hexadecimal : A-F, a-f, 0-9 Ascii : A-Z, a-z, 0-9 Special : ! @ # are allowed)\
                                    Primary Key\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Key4</label>\
                                    <input id=\"vapWEPsecurityConfigTable.vapWEPkey4\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"30\" name=\"vapWEPsecurityConfigTable.vapWEPkey4\" maxlength=\"20\">\
                                    <input id=\"Wepkey4_chk\" type=\"radio\" value=\"4\" name=\"vapWEPsecurityConfigTable.vapWEPprimaryKey\" %s > Primary Key (Hexadecimal : A-F, a-f, 0-9 Ascii : A-Z, a-z, 0-9 Special : ! @ # are allowed)\
                                    Primary Key\
                                </div>\
                            </div><br/>\
                            <div id=\"wparadio\">\
                                <input id=\"sec_wpa\" type=\"radio\" name=\"basicVAPconfigTable.vapSecurityMode\" onClick=\"Securitymode();\" value=\"2\" \"%s\">\
                                WPA\
                            </div><br/>\
                            <div id=\"wpadiv\" style=\"width:900px;margin-left:30px\">\
                                \
                                    <br/><p style=\"font-size:11px\"><b>Enhanced Security for Personal/Enterprise</b></p><br/><br/>\
                                    <div style=\"margin-left:30px\">\
                                    <input id=\"sec_802\" type=\"radio\" value=\"0\" name=\"vapWPAsecurityConfigTable.vapWPAmode\" onClick=\"WPAevents();\">\
                                    802.1x&nbsp;\
                                    <input id=\"secwpa\" type=\"radio\" value=\"1\" name=\"vapWPAsecurityConfigTable.vapWPAmode\" onClick=\"WPAevents();\">\
                                    <span id=\"sec_wpa_name\">WPA</span>\
                                    <input id=\"secwpa2\" type=\"radio\" value=\"2\" name=\"vapWPAsecurityConfigTable.vapWPAmode\" onClick=\"WPAevents();\" checked=\"checked\">\
                                    WPA 2&nbsp;\
                                    <input id=\"secauto\" type=\"radio\" value=\"3\" name=\"vapWPAsecurityConfigTable.vapWPAmode\" onClick=\"WPAevents();\">\
                                    <span id=\"sec_auto_name\">Auto</span>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">Cipher:</label>\
                                        <input id=\"cypher_CCMP\" type=\"radio\" value=\"0\" name=\"vapWPAsecurityConfigTable.vapWPAcypher\" checked=\"checked\">\
                                        CCMP\
                                        <input id=\"cypher_TKIP\" type=\"radio\" value=\"1\" name=\"vapWPAsecurityConfigTable.vapWPAcypher\">\
                                        <span id=\"cypher_TKIP_Name\">TKIP</span>\
                                        <input id=\"cypher_AUTO\" type=\"radio\" value=\"2\" name=\"vapWPAsecurityConfigTable.vapWPAcypher\">\
                                        <span id=\"cypher_AUTO_Name\">AUTO</span>\
                                    </div>\
                                    <div class=\"row-elem\" style=\"display:none\">\
                                        <label class=\"lbl\">WPA Rekey Int:</label>\
                                        <input id=\"vapWPAsecurityConfigTable.vapWPArekeyInterval\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecurityConfigTable.vapWPArekeyInterval\">\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">WPA Master Rekey:</label>\
                                        <input id=\"vapWPAsecurityConfigTable.vapWPAmasterReKey\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecurityConfigTable.vapWPAmasterReKey\">  (Seconds)\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">WEP Rekey Int:</label>\
                                        <input id=\"vapWPAsecurityConfigTable.vapWEPrekeyInt\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecurityConfigTable.vapWEPrekeyInt\"> (802.1x mode only) \
                                    </div>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <input id=\"chk_PersonalKey\" type=\"radio\" name=\"vapWPAsecurityConfigTable.vapWPAkeyMode\" onClick=\"WPAevents();\" value=\"0\" %s />\
                                    <b style=\"font-size:11px;\">Personal Shared Key</b>\
                                </div>\
                                <div class=\"row-elem\" id=\"personalShared\" style=\"margin-left:30px;\">\
                                    <label class=\"lbl\">PSK KEY</label>\
                                    <input id=\"vapWPAsecurityConfigTable.vapWPAconfigPSKPassPhrase\" type=\"password\"  maxlength=\"64\" size=\"70\" name=\"vapWPAsecurityConfigTable.vapWPAconfigPSKPassPhrase\" value=\"%s\" />\
                                </div>\
                                <div class=\"row-elem\">\
                                   <input id=\"chk_EnterpriseKey\" type=\"radio\" name=\"vapWPAsecurityConfigTable.vapWPAkeyMode\" onClick=\"WPAevents();\" value=\"1\" %s>\
                                    <b style=\"font-size:11px;\">Enterprise/RADIUS support </b>\
                                </div>\
                                <div id=\"enterprise\" style=\"margin-left:30px;\">\
                                    <div class=\"row-elem\" style=\"width: 900px;\">\
                                        <label class=\"lbl\">RSN Preauth</label>\
                                        <input id=\"interface_dis\" type=\"radio\" value=\"0\" name=\"vapWPAsecurityConfigTable.vapWPArsnPreAuth\" %s >\
                                        Disable\
                                        <input id=\"interface_enb\" type=\"radio\" value=\"1\" name=\"vapWPAsecurityConfigTable.vapWPArsnPreAuth\" %s>\
                                        Enable &nbsp;&nbsp;Interface:\
                                        <input id=\"vapWPAsecurityConfigTable.vapWPArsnPreAuthInterface\"  type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecurityConfigTable.vapWPArsnPreAuthInterface\">\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">EAP Reauth Period</label>\
                                        <input id=\"vapWPAsecurityConfigTable.vapWPAeapReAuthPeriod\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecurityConfigTable.vapWPAeapReAuthPeriod\">\
                                        (Seconds) \
                                    </div>\
                                    <div class=\"row-elem\" style=\"width:900px\">\
                                        <label class=\"lbl\">Auth Server IP</label>\
                                        <input id=\"vapWPAsecurityConfigTable.vapWPAserverIP\" type=\"text\"  value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecurityConfigTable.vapWPAserverIP\">\
                                        &nbsp;&nbsp;&nbsp;&nbsp; Port:\
                                        <input id=\"vapWPAsecurityConfigTable.vapWPAserverPort\" type=\"text\"  value=\"%s\" maxlength=\"6\" size=\"10\" name=\"vapWPAsecurityConfigTable.vapWPAserverPort\">\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">Shared Secret</label>\
                                        <input id=\"vapWPAsecurityConfigTable.vapWPAsharedSecret\" type=\"password\" value=\"%s\" maxlength=\"64\" size=\"66\" name=\"vapWPAsecurityConfigTable.vapWPAsharedSecret\">\
                                    </div>\
                                </div>\
                            </div>\
                        </div> \
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ap_common_submit\" value=\"Save\" id=\"id_save\" onClick=\"return commonFormSubmit('ap_vap_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ap_common_submit\"  id=\"id_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_vap_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ap_common_submit\" id=\"id_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_vap_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ap_common_submit\" id=\"id_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_vap_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"selectionvap_id\" id=\"selectionvap_id\" value=\"%s\"/>\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"vap_configuration\" tablename=\"basicVAPconfigTable,vapWEPsecurityConfigTable,vapWPAsecurityConfigTable\"/>\
                        </div>\
                    </form>"%(APForms.vap_list(8,1,"enabled","vapselectionid",False,"VAP"),basic_vap_setup[0].vapESSID if len(basic_vap_setup)>0 else "",\
                                        int(basic_vap_setup[0].vapHiddenESSIDstate) if len(basic_vap_setup)>0 else 0,\
                    "checked=checked" if len(basic_vap_setup)>0 and int(basic_vap_setup[0].vapHiddenESSIDstate)==1 else "",\
                    basic_vap_setup[0].vlanId if len(basic_vap_setup)>0 else "",\
                    basic_vap_setup[0].vlanPriority if len(basic_vap_setup)>0 else "",\
                    basic_vap_setup[0].vapRadioMac if len(basic_vap_setup)>0 else "",\
                    APForms.threshold_select_list('0',"enabled","rts_mode",False,"Threshold"),basic_vap_setup[0].vapRTSthresholdValue if len(basic_vap_setup)>0 else "",\
                    APForms.threshold_select_list('0',"enabled","frag_mode",False,"Threshold"),basic_vap_setup[0].vapFragmentationThresholdValue if len(basic_vap_setup)>0 else "",\
                    basic_vap_setup[0].vapBeaconInterval if len(basic_vap_setup)>0 else "",\
                    "checked=checked" if basic_vap_security[0].vapSecurityMode==0 else "" if len(basic_vap_security)>0 else "",\
                    "checked=checked" if basic_vap_security[0].vapSecurityMode==1 else "" if len(basic_vap_security)>0 else "",\
                    "checked=checked" if wep_data[0].vapWEPmode==0 else "" if len(wep_data)>0 else "",\
                    "checked=checked" if wep_data[0].vapWEPmode==1 else "" if len(wep_data)>0 else "",\
                    "checked=checked" if wep_data[0].vapWEPmode==2 else "" if len(wep_data)>0 else "",\
                    wep_data[0].vapWEPkey1 if len(wep_data)>0 else "",\
                    "checked=checked" if wep_data[0].vapWEPprimaryKey==1 else "" if len(wep_data)>0 else "",\
                    wep_data[0].vapWEPkey2 if len(wep_data)>0 else "",\
                    "checked=checked" if wep_data[0].vapWEPprimaryKey==2 else "" if len(wep_data)>0 else "",\
                    wep_data[0].vapWEPkey3 if len(wep_data)>0 else "",\
                    "checked=checked" if wep_data[0].vapWEPprimaryKey==3 else "" if len(wep_data)>0 else "",\
                    wep_data[0].vapWEPkey4 if len(wep_data)>0 else "",\
                    "checked=checked" if wep_data[0].vapWEPprimaryKey==4 else "" if len(wep_data)>0 else "",\
                    "checked=checked" if basic_vap_security[0].vapSecurityMode==2 else "" if len(basic_vap_security)>0 else "",\
                    wpa_data[0].vapWPArekeyInterval if len(wpa_data)>0 else "",\
                    wpa_data[0].vapWPAmasterReKey if len(wpa_data)>0 else "",\
                    wpa_data[0].vapWEPrekeyInt if len(wpa_data)>0 else "",\
                    "checked=checked" if wpa_data[0].vapWPAkeyMode==0 else "" if len(wpa_data)>0 else "",\
                    wpa_data[0].vapWPAconfigPSKPassPhrase if len(wpa_data)>0 else "",\
                    "checked=checked" if wpa_data[0].vapWPAkeyMode==1 else "" if len(wpa_data)>0 else "",\
                    "checked=checked" if wpa_data[0].vapWPArsnPreAuth==0 else "" if len(wpa_data)>0 else "",\
                    "checked=checked" if wpa_data[0].vapWPArsnPreAuth==1 else "" if len(wpa_data)>0 else "",\
                    wpa_data[0].vapWPArsnPreAuthInterface if len(wpa_data)>0 else "",\
                    wpa_data[0].vapWPAeapReAuthPeriod if len(wpa_data)>0 else "",\
                    wpa_data[0].vapWPAserverIP if len(wpa_data)>0 else "",\
                    wpa_data[0].vapWPAserverPort if len(wpa_data)>0 else "",\
                    wpa_data[0].vapWPAsharedSecret if len(wpa_data)>0 else "",\
                    basic_vap_setup[0].vapselection_id if len(basic_vap_setup)>0 else "")
        return form_view
    
    @staticmethod
    def acl_configuration(host_id,selected_device):
        select_vaps = 0
        total_mac_enteries = 0
        obj_bll_get_data = APGetData()
        get_radio_data = obj_bll_get_data.ap_get_data('Ap25RadioSetup',host_id)
        get_basic_acl_data = obj_bll_get_data.ap_get_data('Ap25BasicACLconfigTable',host_id)
        get_acl_statistics = obj_bll_get_data.ap_get_data('Ap25AclStatisticsTable',host_id)
        get_mac_data = obj_bll_get_data.ap_get_data('Ap25AclMacTable',host_id)
        if len(get_radio_data)>0:
            select_vaps = get_radio_data[0].numberOfVAPs
        form_view=""
##        form_view += "<div id=\"acl_table_summary\">\
##                        <fieldset><legend>ACL Summary</legend>\
##                        <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"margin:10px\">"
##        for i in range(0,select_vaps if select_vaps>0 else 8):
##            form_view += "<th>VAP %s </th>"%(i+1)
##        form_view+="<th>Total</th>"
##        form_view+="<tr align=\"center\">"
##        for i in range(0,select_vaps if select_vaps>0 else 8):
##            form_view+="<td>%s</td>"%(0 if len(get_acl_statistics)==0 else get_acl_statistics[i].totalMACentries)
##            total_mac_enteries +=0 if len(get_acl_statistics)==0 else get_acl_statistics[i].totalMACentries
##        form_view+="<td>%s</td>"%(total_mac_enteries)
##        form_view+="<tr/>"
##        form_view +="</fieldset></table></div>"
        
        form_view +="<fieldset><legend>ACL Setting</legend>\
                        <form id=\"ap_acl_form\" name=\"ap_acl_form\" action=\"ap_acl_form_action.py\" method=\"get\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Select VAP</label>\
                                %s\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">ACL</label>\
                                <input id=\"acl_enabled\" type=\"radio\" value=\"1\" name=\"basicACLconfigTable.aclState\" onClick=\"ACL();\">\
                                Enable\
                                <input id=\"acl_disabled\" type=\"radio\" value=\"0\" name=\"basicACLconfigTable.aclState\" onClick=\"ACL();\" >\
                                Disable \
                                <input type=\"hidden\" name=\"aclState\" value=\"%s\"/>\
                            </div>\
                            <div id=\"acl_mac_type\">\
                                <div class=\"row-elem\" style=\"width: 500px;\">\
                                    <label class=\"lbl\">ACL Action</label>\
                                    <input id=\"acl_allow\" type=\"radio\" value=\"1\" name=\"basicACLconfigTable.aclMode\"/>\
                                    Allow MAC Addresses in the ACL\
                                    <input id=\"acl_deny\" type=\"radio\" value=\"0\" name=\"basicACLconfigTable.aclMode\"/>\
                                    Deny MAC Addresses in the ACL \
                                    <input type=\"hidden\" name=\"aclMode\" value=\"%s\"/>\
                                </div>\
                            </div>\
                            <div id=\"aclClientMsg\"></div>\
                            <div class=\"row-elem\">\
                                <input type=\"submit\" name =\"ap_common_submit\" value=\"Save\" id=\"id_save\" onClick=\"return commonFormSubmit('ap_acl_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"ap_common_submit\"  id=\"id_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_acl_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"ap_common_submit\" id=\"id_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_acl_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"ap_common_submit\" id=\"id_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_acl_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"hidden\" value=\"%s\" name=\"vap_selection_id\" />\
                                <input type=\"hidden\" value=\"%s\" name=\"vap_selected\" />\
                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"acl_configuration\" tablename=\"basicACLconfigTable,aclMacTable\"/>\
                            </div>\
                        </form>\
                        <div id=\"acl_mac_div\">\
                            <div>\
                                <table id=\"acl_table_id\" class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" style=\"margin-bottom: 0px;\">\
                                    <tr>\
                                        <th class=\"cell-title\">\
                                            MAC Operations\
                                            <img class=\"img-link\" src=\"images/new/file-delete.png\" title=\"Delete All Mac\" style=\"float: right; margin-right: 10px;height: 13px; width: 12px;\" onClick=\"aclChkAllDelete();\">\
                                            <img class=\"img-link\" src=\"images/new/delete.png\" title=\"Delete Mac\" style=\"float: right; margin-right: 10px; height: 13px; width: 12px;\" onClick=\"aclSingleDelete();\">\
                                            <img class=\"img-link\" src=\"images/new/add.png\" title=\"Add Mac\" style=\"float: right; margin-right: 10px;height: 14px; width: 12px;\" onClick=\"Macaddform();\">\
                                            <!--<img class=\"img-link\" src=\"images/new/update.png\" title=\"Upload MAC File\" style=\"float: right; margin-right: 10px;height: 14px; width: 12px;\" onClick=\"Uploadmacform();\" /> -->\
                                        </th>\
                                    </tr>\
                                </table>\
                            </div>\
                            <div id=\"macdiv\">\
                                <table id=\"showmac\" class=\"display\" style=\"width: 100%%;text-align:center\">\
                                    <thead>\
                                        <tr>\
                                            <th>Select</th>\
                                            <th>Serial No.</th>\
                                            <th>MAC Address</th>\
                                        </tr>\
                                    </thead><tbody>"%(APForms.vap_list(8,1,"enabled","vapSelection.selectVap",False,"VAP"),\
                                                   get_basic_acl_data[0].aclState if len(get_basic_acl_data)>0 else 0,\
                                                   get_basic_acl_data[0].aclMode if len(get_basic_acl_data)>0 else 0,\
                                                   get_basic_acl_data[0].vapselection_id if len(get_basic_acl_data)>0 else 1,select_vaps)
        if len(get_mac_data)>0:
            for i in range(0,len(get_mac_data)):
                form_view+="<tr>\
                                <td><input type=\"checkbox\" name=\"mac_chk\" id=\"mac_chk\" value=\"%s\"/>\
                                <td>%s</td>\
                                <td>%s</td>\
                            </tr>"%(get_mac_data[i].macaddress,i+1,get_mac_data[i].macaddress)                                        
        form_view+="</tbody></table></div></div>"
        form_view+="</fieldset>"
        return form_view
    
    @staticmethod
    def services(host_id,selected_device):
        obj_bll_get_data = APGetData()
        get_radio_data = obj_bll_get_data.ap_get_data('Ap25Services',host_id)
        form_view = ""
        form_view+="<form id=\"ap_service_form\" name=\"ap_service_form\" action=\"ap_service_form_action.py\" method=\"get\">\
                        <div class=\"row-elem\" style=\"position:relative\">\
                            <div style=\"position:relative\">\
                                <label class=\"lbl\">UPNP Server</label>\
                                <input type=\"radio\" value=\"1\" name=\"services.upnpServerStatus\" >\
                                Enable&nbsp;&nbsp;\
                                <input type=\"radio\" value=\"0\" name=\"services.upnpServerStatus\">\
                                Disable \
                                <input type=\"hidden\" name=\"upnpserver\" value=\"%s\" />\
                            </div>\
                            <div style=\"position:absolute\"></div>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">System Log</label>\
                            <input id=\"Syslog_enable\" type=\"radio\" value=\"1\" name=\"services.systemLogStatus\" onClick=\"Services();\">\
                            Enable&nbsp;&nbsp;\
                            <input id=\"Syslog_disable\" type=\"radio\" value=\"0\" name=\"services.systemLogStatus\" onClick=\"Services();\">\
                            Disable \
                            <input type=\"hidden\" name=\"systemlog\" value=\"%s\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Logging IP Address</label>\
                            <input id=\"services.systemLogIP\" type=\"text\"  style=\"width: 150px;\" name=\"services.systemLogIP\" value=\"%s\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Logging Port</label>\
                            <input id=\"services.systemLogPort\" type=\"text\" name=\"services.systemLogPort\" value=\"%s\" maxlength=\"5\" style=\"width: 50px;\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ap_common_submit\" value=\"Save\" id=\"id_save\" onClick=\"return commonFormSubmit('ap_service_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name =\"ap_common_submit\"  id=\"id_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_service_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name =\"ap_common_submit\" id=\"id_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_service_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name =\"ap_common_submit\" id=\"id_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_service_form',this)\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"services\" tablename=\"services\"/>\
                        </div>\
                    </form>"%(get_radio_data[0].upnpServerStatus  if len(get_radio_data)>0 else "",
                            get_radio_data[0].systemLogStatus if len(get_radio_data)>0 else "",\
                            get_radio_data[0].systemLogIP if len(get_radio_data)>0 else "",\
                            get_radio_data[0].systemLogPort if len(get_radio_data)>0 else "")
        return form_view
    
    @staticmethod
    def dhcpServer(host_id,selected_device):
        obj_bll_get_data = APGetData()
        get_radio_data = obj_bll_get_data.ap_get_data('Ap25DhcpServer',host_id)
        form_view = ""
        form_view+="<form id=\"ap_dhcp_form\" name=\"ap_dhcp_form\" action=\"ap_dhcp_form_action.py\" method=\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">DHCP Server</label>\
                            <input id=\"dhcp_enable\" type=\"radio\" value=\"1\" name=\"dhcpServer.dhcpServerStatus\" onClick=\"dhcpServices();\">\
                            Enable&nbsp;&nbsp;\
                            <input id=\"dhcp_disable\" type=\"radio\" value=\"0\" name=\"dhcpServer.dhcpServerStatus\" onClick=\"dhcpServices();\">\
                            Disable \
                            <input type=\"hidden\" name=\"dhcpStatus\" value=\"%s\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">DHCP Start IP Address</label>\
                            <input id=\"dhcpServer.dhcpStartIPaddress\" type=\"text\"  style=\"width: 150px;\" name=\"dhcpServer.dhcpStartIPaddress\" value=\"%s\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">DHCP End IP Address</label>\
                            <input id=\"dhcpServer.dhcpEndIPaddress\" type=\"text\"  style=\"width: 150px;\" name=\"dhcpServer.dhcpEndIPaddress\" value=\"%s\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Network Mask</label>\
                            <input id=\"dhcpServer.dhcpSubnetMask\" type=\"text\"  style=\"width: 150px;\" name=\"dhcpServer.dhcpSubnetMask\" value=\"%s\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Lease Time</label>\
                            <input id=\"dhcpServer.dhcpClientLeaseTime\" type=\"text\" name=\"dhcpServer.dhcpClientLeaseTime\" value=\"%s\" maxlength=\"5\" style=\"width: 50px;\"> (Minutes)\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">DHCP Client List</label>\
                            <input id=\"dhcp_client_info\" type=\"button\" name=\"dhcp_client_info\" value=\"Show Clients\" maxlength=\"5\" style=\"width: 100px;\" onClick=\"dhcpClientInformation();\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ap_common_submit\" value=\"Save\" id=\"id_save\" onClick=\"return commonFormSubmit('ap_dhcp_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name =\"ap_common_submit\"  id=\"id_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_dhcp_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name =\"ap_common_submit\" id=\"id_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_dhcp_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name =\"ap_common_submit\" id=\"id_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_dhcp_form',this)\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"dhcpServer\" tablename=\"dhcpServer\"/>\
                        </div>\
                    </form>"%(get_radio_data[0].dhcpServerStatus  if len(get_radio_data)>0 else "",
                            get_radio_data[0].dhcpStartIPaddress if len(get_radio_data)>0 else "",\
                            get_radio_data[0].dhcpEndIPaddress if len(get_radio_data)>0 else "",\
                            get_radio_data[0].dhcpSubnetMask if len(get_radio_data)>0 else "",\
                            get_radio_data[0].dhcpClientLeaseTime if len(get_radio_data)>0 else "")
        return form_view

    
    @staticmethod
    def acl_add_form():
        form_view = ""
        form_view+="<form id=\"acl_add_form\" name=\"acl_add_form\" action=\"acl_add_form_action.py\" method=\"get\">\
                        <div class=\"row-elem\">\
                            <input id=\"single_add\" type=\"radio\" value=\"1\" name=\"mac_add\" onClick=\"Macadd();\" checked=\"\">\
                            Single Add&nbsp;&nbsp;\
                            <input id=\"multiple_add\" type=\"radio\" value=\"0\" name=\"mac_add\" onClick=\"Macadd();\">\
                            Multiple Add\
                        </div>\
                        <div class=\"row-elem\" id=\"single_add_div\" style=\"display:none\">\
                            <label class=\"lbl\">MAC Address</label>\
                            <input id=\"mac_text\" type=\"text\" name=\"mac_text\" value=\"\" maxlength=\"17\">\
                        </div>\
                        <div class=\"row-elem\" id=\"multiple_add_div\" style=\"display:none\">\
                            <label class=\"lbl\">MAC Address</label>\
                            <textarea id=\"mac_text\" name=\"mac_text\" style=\"height:60px\" ></textarea>\
                            <span style=\"margin-left:142px;font-size:9px\">Add the macaddress seperated by comma</span>\
                        </div>\
                        <div class=\"row-elem\" id=\"add_mac\">\
                            <input type=\"submit\" name =\"ap_common_submit\" value=\"Add\" id=\"id_add\" class=\"yo-small yo-button\" onClick=\"return commonFormSubmit('acl_add_form',this);\" />\
                        </div>\
                    </form>"
        return form_view
    @staticmethod
    def acl_upload_form():
        form_view = ""
        form_view+="<form id=\"acl_update_form\" name=\"acl_update_form\" action=\"acl_update_form_action\" method=\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">MAC Address File</label>\
                            <input id=\"mac_file\" type=\"file\" name=\"mac_file\">\
                        </div>\
                        <div class=\"row-elem\" id=\"add_mac\">\
                            <input type=\"submit\" name =\"ap_common_submit\" value=\"Upload\" id=\"\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ap_common_submit\"  id=\"\" value=\"Retry\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ap_common_submit\" id=\"\" value=\"Cancel\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"ap_common_submit\" id=\"\" value=\"Ok\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                        </div>\
                    </form>"
        return form_view
    
    @staticmethod
    def edit_client_form(client_details,group_name):
    	status=""
    	if group_name.lower()=="guest":
    	    status="disabled=\"disabled\""
    	    
        form_view="\
        <form action=\"edit_ap_client_details.py\" method=\"get\" id=\"edit_client\">\
            <div class=\"row-elem\">\
                <label for=\"client_mac\" class=\"lbl lbl-big\">Client Mac</label>\
                <input type=\"text\" name=\"client_mac\" disabled=\"disabled\" id=\"client_mac\" value=\"%s\">\
                <input type=\"hidden\" id=\"client_id\" name=\"client_id\" value=\"%s\" />\
            </div>\
            <div class=\"row-elem\">\
                <label for=\"client_name\" class=\"lbl lbl-big\">Client Name</label>\
                <input type=\"text\" name=\"client_name\" id=\"client_name\" value=\"%s\" %s>\
            </div>\
            <div class=\"row-elem\">\
                <label for=\"client_ip\" class=\"lbl lbl-big\">Client IP</label>\
                <input type=\"text\" name=\"client_ip\" id=\"client_ip\" value=\"%s\" %s>\
            </div>\
            <div class=\"row-elem\">\
                <input class=\"yo-small yo-button\" type=\"submit\" value=\"Submit\"  %s/>\
            </div>\
        </form>\
        " % (client_details['client_mac'],client_details['client_id'],client_details['client_name'],status,client_details['client_ip'],status,status)
        return form_view

  
class APProfiling(object):
    
    @staticmethod
    def ap_listing():
        table_view = "<div id =\"ap_device_div\">"
        table_view+= "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"device_data_table\" style=\"text-align:center;width:100%\">\
                    <thead>\
                        <tr>\
                            <th>Device Status</th>\
                            <th>Host Alias</th>\
                            <th>Host Group</th>\
                            <th>IP Address</th>\
                            <th>Mac (eth)</th>\
                            <th>Connected Clients</th>\
                            <th>AP Mode</th>\
                            <th>Admin State</th>\
                            <th>Actions</th>\
                            <th>Process</th>\
                        </tr>\
                    </thead>\
                </table></div>\
                <div id=\"ap_client_div\" style=\"display:none\">\
                <table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"client_data_table\" style=\"text-align:center;width:100%\">\
                    <thead>\
                        <tr>\
                            <th>Connected</th>\
                            <th>Client Alias</th>\
                            <th>Client MAC</th>\
                            <th>Client IP</th>\
                            <th>Transferred Sequence</th>\
                            <th>Recieved Sequence</th>\
                            <th>Connected to AP </th>\
                            <th>RSSI</th>\
                            <th>SSID of AP</th>\
                            <th>Last Seen on</th>\
                            <th>Last AP connected</th>\
                            <th>Action</th>\
                        </tr>\
                    </thead>\
                </table></div>\
                <div id=\"status_div\" style=\"position:absolute;display:none\"/>\
                <div></div>\
                <div></div>\
                </div>"
        #eturn table_view
#<th>Transmitted Bytes</th>\
                            #<th>Recieved Bytes</th>\            
        return table_view#+table_view2
    
    @staticmethod
    def client_listing():
        table_view = "<div>"
        table_view+= "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"client_data_table\" style=\"text-align:center;width:100%\">\
                    <thead>\
                        <tr>\
                            <th>Current Connection State</th>\
                            <th>Client MAC</th>\
                            <th>Connected to AP </th>\
                            <th>RSSI</th>\
                            <th>Transmitted Bytes</th>\
                            <th>Recieved Bytes</th>\
                            <th>SSID of AP</th>\
                            <th>Last Seen on</th>\
                            <th>Last AP connected</th>\
                        </tr>\
                    </thead>\
                </table></div>\
                <div id=\"status_div\" style=\"position:absolute;display:none\"/>\
                <div></div>\
                <div></div>\
                </div>"
        return table_view
    
    @staticmethod
    def page_tip_ap_listing():
        try:
            """
            @param h : html Class Object
            @var html : this is html Class Object defined globally 
            @since : 12 December 2011
            @version :0.0 
            @date : 12 December 2011
            @note : This function is used for diplaying the help of odu Listing page.Every link help.Every button Help.What output display.Every Image description.
            @organisation : Codescape Consultants Pvt. Ltd.
            @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
            """
            html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>AP Listing</h1>"\
            "<div><strong>AP Listing</strong> has shown all AP Type Devices.On This Page You Can see Various Options</div>"\
            "<br/>"\
            "<div>On this page you can Edit Configuration, Update Firmware,See Graph and Events for Monitoring of Devices and also make Reconciliation of Devices.</div>"\
            "<br/>"\
            "<div><strong>Actions</strong></div>"\
            "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/edit.png\"/></div><div class=\"txt-div\">Edit Configuration</div></div>"\
            "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/graph.png\"/></div><div class=\"txt-div\">Device Monitoring</div></div>"\
            "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/alert.png\"/></div><div class=\"txt-div\">Device Events</div></div>"\
            "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/update.png\"/></div><div class=\"txt-div\">Firmware Upgrade</div></div>"\
            "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-green.png\"/></div><div class=\"txt-div\">Reconciliation done 100%</div></div>"\
            "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-black.png\"/></div><div class=\"txt-div\">Reconciliation done in between 36% and less than 90%</div></div>"\
            "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-red.png\"/></div><div class=\"txt-div\">Reconciliation done in between 0% and 35%</div></div>"\
            "<br/>"\
            "<div><strong>Note:</strong>After Reconciliation The Reconciliation Image changes according to Reconciliation Percentage.\
            The Reconiliation Images turns Red when Reconciliation done Between 0 to 35%\
            The Reconiliation Images turns Black when Reconciliation done Between 0 to less than 90%\
            The Reconiliation Images turns Green when Reconciliation Percentage Greater Than and Equal To 90%\
            </div>"\
            "</div>"
            return (str(html_view))
        except Exception,e:
            return str(e)

    
    @staticmethod
    def ap_profiling_form(group_name,host_id,selected_device,device_list_parameter):
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
        if device_list_parameter == "" or device_list_parameter ==[]:
            return "No Configuration Profile Exist"
        elif device_list_parameter[0].config_profile_id == None or device_list_parameter[0].config_profile_id=="":
            return "No Configuration Exist.Please Add Host Again"
        else:
            tab_str = ""
            tab_str += "<input type=\"hidden\" name=\"host_id\" id=\"host_id\" value=\"%s\"/><input type=\"hidden\" name=\"device_type\" id=\"device_type\" value=\"%s\"/>"%(host_id,selected_device)
            tab_str += "<input type=\"hidden\" name=\"group_name\" id=\"group_name\" value=\"%s\"/>"%(group_name)
            tab_str += "<div class=\"yo-tabs\" id=\"config_tabs\" style=\"display:block\">\
                            <ul>\
                                <li><a class=\"active\" href=\"#content_1\">Radio Configuration</a></li>\
                                <li><a href=\"#content_2\"id=\"vap_content\">VAP Configuration</a></li>\
                                <li><a href=\"#content_3\">ACL Configuration</a></li>\
                                <li><a href=\"#content_4\">Services</a></li>\
                                <li><a href=\"#content_5\">DHCP</a></li>\
                            </ul>\
                            <div id=\"content_1\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                                <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                                %s\
                                </div>\
                            </div>\
                            <div id=\"content_2\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                                <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                                %s\
                                </div>\
                            </div>\
                            <div id=\"content_3\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                                %s\
                            </div>\
                            <div id=\"content_4\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                                %s\
                            </div>\
                            <div id=\"content_5\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                                %s\
                            </div>\
                        </div>"%(APForms.radio_configuration(host_id,selected_device),APForms.vap_configuration(host_id,selected_device),APForms.acl_configuration(host_id,selected_device),APForms.services(host_id,selected_device),APForms.dhcpServer(host_id,selected_device))
            return tab_str

            
        
        
    @staticmethod
    def ap_div(ip_address,mac_address,host_id):
        global obj_essential
        obj_get_data = APGetData()
        ap_admin_state_data = obj_get_data.ap_get_data("Ap25RadioSetup",host_id)
        if len(ap_admin_state_data)>0:
            if ap_admin_state_data[0].radioState == 0:
                image_class = "red"
                state = 0
                html_label = "Radio Disabled"
            else:
                image_class = "green"
                state = 1
                html_label = "Radio Enabled"

            op_status = obj_essential.get_hoststatus(host_id)
            if op_status==None:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[0]
            elif op_status==0:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[op_status]
            else:
                op_img = "images/host_status1.png"
                op_title = host_status_dic[op_status]

        
        
        profile_str = ""
        profile_str += "<div id=\"ap_form_div\" class=\"form-div\" style=\"margin-top: 56px;\"></div>"
        profile_str +="<div class=\"form-div-footer\">\
                            <div style=\"float: left;margin-left:15px\">\
                                <ul class=\"button_group\" style=\"margin:10px 0 0 10px !important;\"><li><a id=\"admin_state\" class=\"%s n-reconcile imgEditodu16\" state=\"%s\" onclick=\"radio_enable_disable(event,this,'%s','radioSetup.radioState');\"/>%s</a></li></ul>\
                            </div>\
                            <div id=\"operation_status\" style=\"float: left; margin-top: 12px; margin-left: 15px;vertical-align: middle;\">\
                                <span>Process </span>&nbsp;&nbsp;&nbsp;<img class=\"n-reconcile\" id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:14px;height:14px;vertical-align: middle;\"class=\"imgbutton n-reconcile\"/></center>&nbsp;&nbsp;\
                            </div>\
                            <div id=\"footer_tab\" style=\"float: right;margin-right:15px\">\
                                <input type=\"button\" id=\"ap25_commit\" name=\"ap25_commit\" value=\"Apply Settings\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"ap25_reboot\" name=\"ap25_reboot\" value=\"Reboot\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"ap25_reconcile\" name=\"ap25_reconcile\" value=\"Reconciliation\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"ap25_scan\" name=\"ap25_scan\" value=\"AP Scan\" class=\"yo-small yo-button\" onclick=\"apScan()\"/>\
                                <input type=\"hidden\" name=\"ip_address\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"mac_address\" value=\"%s\" />\
                                <input type=\"hidden\" name=\"host_id\" value=\"%s\" />\
                            </div>\
                        </div>" %(image_class,state,host_id,html_label,op_img,op_title,ip_address,mac_address,host_id)
        return profile_str
    
    @staticmethod
    def ap_profile_call(group_name,host_id,device_type,device_list_parameter):
        tab_str = ""
        if host_id == "" or host_id == "None":
            tab_str+="There is No Host Exist</div>"
        else:
            if device_type == UNMPDeviceType.ap25:
                tab_str += APProfiling.ap_profiling_form(group_name,host_id,device_type,device_list_parameter)# function call , it is used to make a form of selected profiling  
        return tab_str
