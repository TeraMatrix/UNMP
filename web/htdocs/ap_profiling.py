#!/usr/bin/python2.6

from utility import UNMPDeviceType
from common_controller import MakeSelectListUsingDictionary
from ap_profiling_bll import APGetData
class APForms(object):
    
    @staticmethod
    def vap_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        vap_select_dic = {} 
        #{'name':['DISABLE','ENABLE'],'value':[0,1]}
        vap_select_dic = {"name":[1,2,3,4,5,6,7,8],"value":[1,2,3,4,5,6,7,8]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(vap_select_dic,selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg)
    
    @staticmethod
    def radio_channel_select_list(selected_field,selected_list_state,selected_list_id,is_readonly,select_list_initial_msg):
        channel_dic = {}
        j = 1
        i=2.412
        while(i<2.473):
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
                            <select name=\"radioSetup.radioCountryCode\" disabled=\"disabled\">\
                                <option value=\"NA\">DEFAULT </option>\
                                <option value=\"DB\">DEBUG</option>\
                                <option value=\"AL\">ALBANIA </option>\
                                <option value=\"DZ\">ALGERIA</option>\
                                <option value=\"AR\">ARGENTINA</option>\
                                <option value=\"AM\">ARMENIA</option>\
                                <option value=\"AU\">AUSTRALIA</option>\
                                <option value=\"AT\">AUSTRIA</option>\
                                <option value=\"AZ\">AZERBAIJAN</option>\
                                <option value=\"BH\">selected="">BAHRAIN</option>\
                                <option value=\"BY\">BELARUS </option>\
                                <option value=\"BE\">BELGIUM</option>\
                                <option value=\"BZ\">BELIZE</option>\
                                <option value=\"BO\">BOLIVIA</option>\
                                <option value=\"BA\">BOSNIA_HERZEGOWINA </option>\
                                <option value=\"BR\">BRAZIL</option>\
                                <option value=\"BN\">BRUNEI_DARUSSALAM</option>\
                                <option value=\"BG\">BULGARIA </option>\
                                <option value=\"CA\">CANADA</option>\
                                <option value=\"CL\">CHILE</option>\
                                <option value=\"CN\">CHINA</option>\
                                <option value=\"CO\">COLOMBIA</option>\
                                <option value=\"CR\">COSTA_RICA</option>\
                                <option value=\"HR\">CROATIA</option>\
                                <option value=\"CY\">CYPRUS</option>\
                                <option value=\"CZ\">CZECH</option>\
                                <option value=\"DK\">DENMARK</option>\
                                <option value=\"DO\">DOMINICAN REPUBLIC </option>\
                                <option value=\"EC\">ECUADOR</option>\
                                <option value=\"EG\">EGYPT</option>\
                                <option value=\"SV\">EL_SALVADOR</option>\
                                <option value=\"EE\">ESTONIA</option>\
                                <option value="">FAEROE_ISLANDS</option>\
                                <option value=\"FI\">FINLAND</option>\
                                <option value=\"FR\">FRANCE</option>\
                                <option value=\"GE\">GEORGIA</option>\
                                <option value=\"DE\">GERMANY</option>\
                                <option value=\"GR\">GREECE</option>\
                                <option value=\"GT\">GUATEMALA</option>\
                                <option value=\"HN\">HONDURAS</option>\
                                <option value=\"HK\">HONG KONG</option>\
                                <option value=\"HU\">HUNGARY</option>\
                                <option value=\"IS\">ICELAND</option>\
                                <option value=\"IN\">INDIA</option>\
                                <option value=\"ID\">INDONESIA</option>\
                                <option value=\"IR\">IRAN</option>\
                                <option value="">IRAQ</option>\
                                <option value=\"IE\">IRELAND</option>\
                                <option value=\"IL\">ISRAEL</option>\
                                <option value=\"IT\">ITALY</option>\
                                <option value="">JAMAICA</option>\
                                <option value=\"JP\">JAPAN</option>\
                                <option value=\"JO\">JORDAN</option>\
                                <option value=\"KZ\">KAZAKHSTAN</option>\
                                <option value=\"KE\">KENYA</option>\
                                <option value=\"KP\">KOREA NORTH</option>\
                                <option value=\"KW\">KUWAIT</option>\
                                <option value=\"LV\">LATVIA</option>\
                                <option value=\"LB\">LEBANON</option>\
                                <option value=\"LI\">LIECHTENSTEIN</option>\
                                <option value=\"LT\">LITHUANIA</option>\
                                <option value=\"LU\">LUXEMBOURG</option>\
                                <option value=\"MO\">MACAU</option>\
                                <option value=\"MK\">MACEDONIA</option>\
                                <option value=\"MY\">MALAYSIA</option>\
                                <option value="">MALTA</option>\
                                <option value=\"MX\">MEXICO</option>\
                                <option value=\"MC\">MONACO</option>\
                                <option value=\"MA\">MOROCCO</option>\
                                <option value=\"NL\">NETHERLANDS</option>\
                                <option value=\"NZ\">NEW ZEALAND</option>\
                                <option value="">NICARAGUA</option>\
                                <option value=\"NO\">NORWAY</option>\
                                <option value=\"OM\">OMAN</option>\
                                <option value=\"PK\">PAKISTAN</option>\
                                <option value=\"PA\">PANAMA</option>\
                                <option value="">PARAGUAY</option>\
                                <option value=\"PE\">PERU</option>\
                                <option value=\"PH\">PHILIPPINES</option>\
                                <option value=\"PL\">POLAND</option>\
                                <option value=\"PT\">PORTUGAL</option>\
                                <option value=\"PR\">PUERTO_RICO</option>\
                                <option value=\"QA\">QATAR</option>\
                                <option value=\"RO\">ROMANIA</option>\
                                <option value=\"RU\">RUSSIA</option>\
                                <option value=\"SA\">SAUDI ARABIA</option>\
                                <option value="">SERBIA MONTENEGRO</option>\
                                <option value=\"SG\">SINGAPORE</option>\
                                <option value=\"SK\">SLOVAKIA</option>\
                                <option value=\"SI\">SLOVENIA</option>\
                                <option value=\"ZA\">SOUTH AFRICA</option>\
                                <option value=\"ES\">SPAIN</option>\
                                <option value=\"LK\">SRI LANKA</option>\
                                <option value=\"SE\">SWEDEN</option>\
                                <option value=\"CH\">SWITZERLAND</option>\
                                <option value=\"SY\">SYRIA</option>\
                                <option value=\"TW\">TAIWAN</option>\
                                <option value=\"TH\">THAILAND</option>\
                                <option value=\"TT\">TRINIDAD Y TOBAGO</option>\
                                <option value=\"TN\">TUNISIA</option>\
                                <option value=\"TR\">TURKEY</option>\
                                <option value=\"AE\">UAE</option>\
                                <option value=\"UA\">UKRAINE</option>\
                                <option value=\"GB\">UNITED KINGDOM</option>\
                                <option value=\"US\">UNITED STATES</option>\
                                <option value=\"UY\">URUGUAY</option>\
                                <option value=\"UZ\">UZBEKISTAN</option>\
                                <option value=\"VE\">VENEZUELA</option>\
                                <option value=\"VN\">VIET NAM</option>\
                                <option value=\"YE\">YEMEN</option>\
                                <option value=\"ZW\">ZIMBABWE</option>\
                            </select>\
                            <input type=\"hidden\" name=\"countrycode\" id=\"countrycode\" value=\"\"/>\
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
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Gating Index</label>\
                            <input type=\"radio\" value=\"0\" name=\"radioSetup.radioGatingIndex\" />\
                            Half&nbsp;\
                            <input type=\"radio\" value=\"1\" name=\"radioSetup.radioGatingIndex\" />\
                            Full&nbsp;\
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
                            <input type=\"text\" value=\"%s\" id=\"radioSetup.radioAggFrames\" name=\"radioSetup.radioAggFrames\" maxlength=\"9\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Aggregation Size</label>\
                            <input type=\"text\" value=\"%s\" id=\"radioSetup.radioAggSize\" name=\"radioSetup.radioAggSize\" maxlength=\"9\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Aggregation Min Size</label>\
                            <input type=\"text\" value=\"%s\" id=\"radioSetup.radioAggMinSize\" name=\"radioSetup.radioAggMinSize\" maxlength=\"9\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"ap_common_submit\" value=\"Save\" id=\"id_save\" onClick=\"return commonFormSubmit('ap_radio_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name =\"ap_common_submit\"  id=\"id_retry\" value=\"Retry\"  onClick=\"return commonFormSubmit('ap_radio_form',this)\" class=\"yo-small yo-button\" style=\"display:none\"/>\
                            <input type=\"submit\" name =\"ap_common_submit\" id=\"id_cancel\" value=\"Cancel\"  onClick=\"return commonFormSubmit('ap_radio_form',this)\" class=\"yo-small yo-button\" style=\"display:none\"/>\
                            <input type=\"submit\" name =\"ap_common_submit\" id=\"id_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_radio_form',this)\" class=\"yo-small yo-button\" style=\"display:none\"/>\
                        </div>\
                    </form>"%(get_radio_data[0].radioState if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioAPmode if len(get_radio_data)>0 else "",\
                            get_radio_data[0].radioManagementVLANstate if len(get_radio_data)>0 else "",\
                            APForms.vap_select_list(get_radio_data[0].numberofVAPs if len(get_radio_data)>0 else "","enabled","radioSetup.numberOfVAPs",False,"Vap"),\
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
        basic_vap_setup = obj_bll_get_data.ap_get_data('Ap25BasicVAPsetup',host_id)
        basic_vap_security = obj_bll_get_data.ap_get_data('Ap25BasicVAPsecurity',host_id)
        wep_data = obj_bll_get_data.ap_get_data('Ap25VapWEPsecuritySetup',host_id)
        wpa_data = obj_bll_get_data.ap_get_data('Ap25VapWPAsecuritySetup',host_id)
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
                            <input id=\"basicVAPsetup.vapESSID\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"35\" name=\"basicVAPsetup.vapESSID\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Hide ESSID</label>\
                            <input id=\"basicVAPsetup.vapHiddenESSIDstate\" type=\"checkbox\" value=\"0\" name=\"basicVAPsetup.vapHiddenESSIDstate\" \"%s\">\
                        </div>\
                     <!--   <div class=\"row-elem\" id=\"vlan_id\">\
                            <label class=\"lbl\">VLAN ID</label>\
                            <input id=\"AP_VLAN\" type=\"text\" value=\"2\" maxlength=\"5\" size=\"8\" name=\"AP_VLAN\" disabled=\"disabled\">\
                        </div>\
                        <div class=\"row-elem\" id=\"vlan_priority\">\
                            <label class=\"lbl\">VLAN Priority</label>\
                            <input id=\"VLAN_PRI\" type=\"text\" value=\"0\" maxlength=\"1\" size=\"2\" name=\"VLAN_PRI\" disabled=\"disabled\">\
                        </div>\
                        <div class=\"row-elem\" id=\"vap_mode\">\
                            <label class=\"lbl\">VAP Mode</label>\
                            <input type=\"radio\" value=\"ap\" name=\"AP_MODE\" disabled=\"disabled\">\
                            Access Point&nbsp;\
                            <input type=\"radio\" value=\"ap-wds\" name=\"AP_MODE\" disabled=\"disabled\">\
                            WDS Access Point&nbsp;\
                        </div>\
                        <div class=\"row-elem\" id=\"root_mac_address\">\
                            <label class=\"lbl\">Root AP Mac Address</label>\
                            <input id=\"ROOTAP_MAC_2\" type=\"text\" value=\"\" maxlength=\"32\" size=\"35\" name=\"ROOTAP_MAC_2\" disabled=\"disabled\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Enable Dynamic VLan</label>\
                            <input id=\"chk_dyn_vlan\" type=\"checkbox\" disabled=\"disabled\">\
                            <span>(Dymamic VLAN can be Enabled in RootAP,Standard mode With Enterprise/Radius Support.)</span>\
                        </div>-->\
                        <div class=\"row-elem\" style=\"width:800px\">\
                            <label class=\"lbl\">RTS Threshold</label>\
                            %s\
                            <input id=\"basicVAPsetup.vapRTSthresholdValue\" name=\"basicVAPsetup.vapRTSthresholdValue\" type=\"text\" value=\"%s\" style=\"margin-left:10px\">\
                            </select>\
                        </div>\
                        <div class=\"row-elem\" style=\"width:800px\">\
                            <label class=\"lbl\">Fragmentation Threshold</label>\
                            %s\
                            <input id=\"basicVAPsetup.vapFragmentationThresholdValue\" type=\"text\" value=\"%s\" name=\"basicVAPsetup.vapFragmentationThresholdValue\" style=\"margin-left:10px\">\
                        </div>\
                        <div class=\"row-elem\" id=\"Beacon\">\
                            <label class=\"lbl\">Beacon Interval</label>\
                            <input id=\"basicVAPsetup.vapBeaconInterval\" type=\"text\" style=\"width: 65px;\" value=\"%s\" name=\"basicVAPsetup.vapBeaconInterval\">\
                        </div>\
                        \
                        <div class=\"row-elem\" style=\"width:1000px\">\
                            <div id=\"openradio\">\
                                <input id=\"sec_open\" type=\"radio\" name=\"basicVAPsecurity.vapSecurityMode\" onClick=\"Securitymode();\" \"%s\" value=\"0\">\
                                Open\
                            </div>\
                            <div id=\"opendiv\" style=\"margin-left:30px;\">\
                                <br/><p style=\"font-size:11px\"><b>No Security Applied</b></p>\
                            </div><br/><br/>\
                            <div id=\"wepradio\">\
                                <input id=\"sec_wep\" type=\"radio\" name=\"basicVAPsecurity.vapSecurityMode\" onClick=\"Securitymode();\" value=\"1\" \"%s\">\
                                WEP\
                            </div><br/>\
                            <div id=\"wepdiv\" style=\"margin-left:30px;\">\
                                <br/><p style=\"font-size:11px\"><b>Simple WEP Security (64 0r 128 bit hardware key)</b></p><br/>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Mode</label>\
                                    <input id=\"wepmode1\" type=\"radio\" value=\"0\" name=\"vapWEPsecuritySetup.vapWEPmode\" %s >\
                                    Open\
                                    <input id=\"wepmode2\" type=\"radio\" value=\"1\" name=\"vapWEPsecuritySetup.vapWEPmode\" %s >\
                                    Shared\
                                    <input id=\"wepmode4\" type=\"radio\" value=\"2\" name=\"vapWEPsecuritySetup.vapWEPmode\" %s>\
                                    Auto \
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Key1</label>\
                                    <input id=\"vapWEPsecuritySetup.vapWEPkey1\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"30\" name=\"vapWEPsecuritySetup.vapWEPkey1\">\
                                    <input id=\"Wepkey1_chk\" type=\"radio\" value=\"1\" name=\"vapWEPsecuritySetup.vapWEPprimaryKey\" maxlength=\"20\" %s>\
                                    Primary Key\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Key2</label>\
                                    <input id=\"vapWEPsecuritySetup.vapWEPkey2\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"30\" name=\"vapWEPsecuritySetup.vapWEPkey2\" maxlength=\"20\">\
                                    <input id=\"Wepkey2_chk\" type=\"radio\" value=\"2\" name=\"vapWEPsecuritySetup.vapWEPprimaryKey\" %s >\
                                    Primary Key\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Key3</label>\
                                    <input id=\"vapWEPsecuritySetup.vapWEPkey3\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"30\" name=\"vapWEPsecuritySetup.vapWEPkey3\" maxlength=\"20\">\
                                    <input id=\"Wepkey3_chk\" type=\"radio\" value=\"3\" name=\"vapWEPsecuritySetup.vapWEPprimaryKey\" %s >\
                                    Primary Key\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl\">Key4</label>\
                                    <input id=\"vapWEPsecuritySetup.vapWEPkey4\" type=\"text\" value=\"%s\" maxlength=\"32\" size=\"30\" name=\"vapWEPsecuritySetup.vapWEPkey4\" maxlength=\"20\">\
                                    <input id=\"Wepkey4_chk\" type=\"radio\" value=\"4\" name=\"vapWEPsecuritySetup.vapWEPprimaryKey\" %s >\
                                    Primary Key\
                                </div>\
                            </div><br/>\
                            <div id=\"wparadio\">\
                                <input id=\"sec_wpa\" type=\"radio\" name=\"basicVAPsecurity.vapSecurityMode\" onClick=\"Securitymode();\" value=\"2\" \"%s\">\
                                WPA\
                            </div><br/>\
                            <div id=\"wpadiv\" style=\"width:900px;margin-left:30px\">\
                                \
                                    <br/><p style=\"font-size:11px\"><b>Enhanced Security for Personal/Enterprise</b></p><br/><br/>\
                                    <div style=\"margin-left:30px\">\
                                    <input id=\"sec_802\" type=\"radio\" value=\"0\" name=\"vapWPAsecuritySetup.vapWPAmode\" onClick=\"WPAevents();\">\
                                    802.1x&nbsp;\
                                    <input id=\"secwpa\" type=\"radio\" value=\"1\" name=\"vapWPAsecuritySetup.vapWPAmode\" onClick=\"WPAevents();\">\
                                    WPA&nbsp;\
                                    <input id=\"secwpa2\" type=\"radio\" value=\"2\" name=\"vapWPAsecuritySetup.vapWPAmode\" onClick=\"WPAevents();\" checked=\"checked\">\
                                    WPA 2&nbsp;\
                                    <input id=\"secauto\" type=\"radio\" value=\"3\" name=\"vapWPAsecuritySetup.vapWPAmode\" onClick=\"WPAevents();\">\
                                    Auto&nbsp;\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">Cypher:</label>\
                                        <input id=\"cypher_CCMP\" type=\"radio\" value=\"0\" name=\"vapWPAsecuritySetup.vapWPAcypher\" checked=\"checked\">\
                                        CCMP\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">WPA Rekey Int:</label>\
                                        <input id=\"vapWPAsecuritySetup.vapWPArekeyInterval\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecuritySetup.vapWPArekeyInterval\">\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">WPA Master Rekey:</label>\
                                        <input id=\"vapWPAsecuritySetup.vapWPAmasterReKey\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecuritySetup.vapWPAmasterReKey\">\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">WEP Prekey Int:</label>\
                                        <input id=\"vapWPAsecuritySetup.vapWEPrekeyInt\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecuritySetup.vapWEPrekeyInt\">(802.1x mode only) \
                                    </div>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <input id=\"chk_PersonalKey\" type=\"radio\" name=\"vapWPAsecuritySetup.vapWPAkeyMode\" onClick=\"WPAevents();\" value=\"0\" %s />\
                                    <b style=\"font-size:11px;\">Personal Shared Key</b>\
                                </div>\
                                <div class=\"row-elem\" id=\"personalShared\" style=\"margin-left:30px;\">\
                                    <label class=\"lbl\">PSK KEY</label>\
                                    <input id=\"vapWPAsecuritySetup.vapWPAconfigPSKPassPhrase\" type=\"password\"  maxlength=\"64\" size=\"70\" name=\"vapWPAsecuritySetup.vapWPAconfigPSKPassPhrase\" value=\"%s\" />\
                                </div>\
                                <div class=\"row-elem\">\
                                   <input id=\"chk_EnterpriseKey\" type=\"radio\" name=\"vapWPAsecuritySetup.vapWPAkeyMode\" onClick=\"WPAevents();\" value=\"1\" %s>\
                                    <b style=\"font-size:11px;\">Enterprise/RADIUS support </b>\
                                </div>\
                                <div id=\"enterprise\" style=\"margin-left:30px;\">\
                                    <div class=\"row-elem\" style=\"width: 500px;\">\
                                        <label class=\"lbl\">RSN Preauth</label>\
                                        <input id=\"interface_dis\" type=\"radio\" value=\"0\" name=\"vapWPAsecuritySetup.vapWPArsnPreAuth\" %s >\
                                        Disable\
                                        <input id=\"interface_enb\" type=\"radio\" value=\"1\" name=\"vapWPAsecuritySetup.vapWPArsnPreAuth\" %s>\
                                        Enable &nbsp;&nbsp;Interface:\
                                        <input id=\"vapWPAsecuritySetup.vapWPArsnPreAuthInterface\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecuritySetup.vapWPArsnPreAuthInterface\">\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">EAP Reauth Period</label>\
                                        <input id=\"vapWPAsecuritySetup.vapWPAeapReAuthPeriod\" type=\"text\" value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecuritySetup.vapWPAeapReAuthPeriod\">\
                                        Seconds \
                                    </div>\
                                    <div class=\"row-elem\" style=\"width:900px\">\
                                        <label class=\"lbl\">Auth Server IP</label>\
                                        <input id=\"vapWPAsecuritySetup.vapWPAserverIP\" type=\"text\"  value=\"%s\" maxlength=\"16\" size=\"18\" name=\"vapWPAsecuritySetup.vapWPAserverIP\">\
                                        &nbsp;&nbsp;&nbsp;&nbsp; Port:\
                                        <input id=\"vapWPAsecuritySetup.vapWPAserverPort\" type=\"text\"  value=\"%s\" maxlength=\"6\" size=\"10\" name=\"vapWPAsecuritySetup.vapWPAserverPort\">\
                                    </div>\
                                    <div class=\"row-elem\">\
                                        <label class=\"lbl\">Shared Secret</label>\
                                        <input id=\"vapWPAsecuritySetup.vapWPAsharedSecret\" type=\"password\" value=\"%s\" maxlength=\"64\" size=\"66\" name=\"vapWPAsecuritySetup.vapWPAsharedSecret\">\
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
                        </div>\
                    </form>"%(APForms.vap_list(8,1,"enabled","vapselectionid",False,"VAP"),basic_vap_setup[0].vapESSID if len(basic_vap_setup)>0 else "",\
                    "checked=checked" if int(basic_vap_setup[0].vapHiddenESSIDstate)==0 else "" if len(basic_vap_setup)>0 else "",\
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
        get_basic_acl_data = obj_bll_get_data.ap_get_data('Ap25BasicACLsetup',host_id)
        get_acl_statistics = obj_bll_get_data.ap_get_data('Ap25AclStatisticsTable',host_id)
        get_mac_data = obj_bll_get_data.ap_get_data('Ap25AclMacTable',host_id)
        if len(get_radio_data)>0:
            select_vaps = get_radio_data[0].numberofVAPs
        form_view=""
        form_view += "<div id=\"acl_table_summary\">\
                        <fieldset><legend>ACL Summary</legend>\
                        <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"margin:10px\">"
        for i in range(0,select_vaps if select_vaps>0 else 8):
            form_view += "<th>VAP %s </th>"%(i+1)
        form_view+="<th>Total</th>"
        form_view+="<tr align=\"center\">"
        for i in range(0,select_vaps if select_vaps>0 else 8):
            form_view+="<td>%s</td>"%(0 if len(get_acl_statistics)==0 else get_acl_statistics[i].totalMACentries)
            total_mac_enteries +=0 if len(get_acl_statistics)==0 else get_acl_statistics[i].totalMACentries
        form_view+="<td>%s</td>"%(total_mac_enteries)
        form_view+="<tr/>"
        form_view +="</fieldset></table></div>"
        
        form_view +="<fieldset><legend>ACL Setting</legend>\
                        <form id=\"ap_acl_form\" name=\"ap_acl_form\" action=\"ap_acl_form_action.py\" method=\"get\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Select VAP</label>\
                                %s\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">ACL</label>\
                                <input id=\"acl_enabled\" type=\"radio\" value=\"1\" name=\"vapWPAsecuritySetup.aclState\" onClick=\"ACL();\">\
                                Enable\
                                <input id=\"acl_disabled\" type=\"radio\" value=\"0\" name=\"vapWPAsecuritySetup.aclState\" onClick=\"ACL();\" >\
                                Disable \
                                <input type=\"hidden\" name=\"aclState\" value=\"%s\"/>\
                            </div>\
                            <div id=\"acl_mac_type\">\
                                <div class=\"row-elem\" style=\"width: 500px;\">\
                                    <label class=\"lbl\">ACL Action</label>\
                                    <input id=\"acl_allow\" type=\"radio\" value=\"1\" name=\"vapWPAsecuritySetup.aclMode\"/>\
                                    Allow MAC Addresses in the ACL\
                                    <input id=\"acl_deny\" type=\"radio\" value=\"0\" name=\"vapWPAsecuritySetup.aclMode\"/>\
                                    Deny MAC Addresses in the ACL \
                                    <input type=\"hidden\" name=\"aclMode\" value=\"%s\"/>\
                                </div>\
                            </div>\
                            <div class=\"row-elem\">\
                                <input type=\"submit\" name =\"ap_common_submit\" value=\"Save\" id=\"id_save\" onClick=\"return commonFormSubmit('ap_acl_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"ap_common_submit\"  id=\"id_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_acl_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"ap_common_submit\" id=\"id_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_acl_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"ap_common_submit\" id=\"id_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('ap_acl_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"hidden\" value=\"%s\" name=\"vap_selection_id\" />\
                                <input type=\"hidden\" value=\"%s\" name=\"vap_selected\" />\
                            </div>\
                        </form>\
                        <div id=\"acl_mac_div\">\
                            <div>\
                                <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" style=\"margin-bottom: 0px;\">\
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
                        </div>\
                    </form>"%(get_radio_data[0].upnpServerStatus  if len(get_radio_data)>0 else "",
                            get_radio_data[0].systemLogStatus if len(get_radio_data)>0 else "",\
                            get_radio_data[0].systemLogIP if len(get_radio_data)>0 else "",\
                            get_radio_data[0].systemLogPort if len(get_radio_data)>0 else "",\
                            )
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

  
class APProfiling(object):
    
    @staticmethod
    def ap_listing():
        table_view = "<div>"
        table_view+= "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"device_data_table\" style=\"text-align:center\">\
                    <thead>\
                        <tr>\
                            <th>Device Status</th>\
                            <th>Host Alias</th>\
                            <th>Host Group</th>\
                            <th>IP Address</th>\
                            <th>Mac (eth)</th>\
                            <th>AP Mode</th>\
                            <th>Admin State</th>\
                            <th>Actions</th>\
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
    def ap_profiling_form(host_id,selected_device,device_list_parameter):
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
            tab_str += "<div class=\"yo-tabs\" id=\"config_tabs\" style=\"display:block\">\
                            <ul>\
                                <li><a class=\"active\" href=\"#content_1\">Radio Configuration</a></li>\
                                <li><a href=\"#content_2\">VAP Configuration</a></li>\
                                <li><a href=\"#content_3\">ACL Configuration</a></li>\
                                <li><a href=\"#content_4\">Services</a></li>\
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
                        </div>"%(APForms.radio_configuration(host_id,selected_device),APForms.vap_configuration(host_id,selected_device),APForms.acl_configuration(host_id,selected_device),APForms.services(host_id,selected_device))
            return tab_str

            
        
        
    @staticmethod
    def ap_div(ip_address,mac_address,host_id):
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
        profile_str = ""
        profile_str += "<div id=\"ap_form_div\" class=\"form-div\" style=\"margin-top: 56px;\"></div>"
        profile_str +="<div class=\"form-div-footer\">\
                            <div style=\"float: left;margin-left:15px\">\
                                <ul class=\"button_group\" style=\"margin:10px 0 0 10px !important;\"><li><a class=\"%s n-reconcile imgEditodu16\" state=\"%s\" onclick=\"radio_enable_disable(event,this,'%s','radioSetup.radioState');\"/>%s</a></li></ul>\
                            </div>\
                            <div style=\"float: right;margin-right:15px\">\
                                <input type=\"button\" id=\"ap25_commit\" name=\"ap25_commit\" value=\"Commit To Flash\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"ap25_reboot\" name=\"ap25_reboot\" value=\"Reboot\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"ap25_reconcile\" name=\"ap25_reconcile\" value=\"Reconciliation\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"ap25_scan\" name=\"ap25_scan\" value=\"AP SCAN\" class=\"yo-small yo-button\" onclick=\"apScan()\"/>\
                                <input type=\"hidden\" name=\"ip_address\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"mac_address\" value=\"%s\" />\
                                <input type=\"hidden\" name=\"host_id\" value=\"%s\" />\
                            </div>\
                        </div>" %(image_class,state,host_id,html_label,ip_address,mac_address,host_id)
        return profile_str
    
    @staticmethod
    def ap_profile_call(host_id,device_type,device_list_parameter):
        tab_str = ""
        if host_id == "" or host_id == "None":
            tab_str+="There is No Host Exist</div>"
        else:
            if device_type == UNMPDeviceType.ap25:
                tab_str += APProfiling.ap_profiling_form(host_id,device_type,device_list_parameter)# function call , it is used to make a form of selected profiling  
        return tab_str
