#!/usr/bin/python2.6

from utility import UNMPDeviceType
from common_controller import MakeSelectListUsingDictionary
from idu_profiling_bll import IduGetData


dict = {0: 'ODU', 2: 'LAN1', 3: 'LAN2', 4: 'CPU', 5: 'TDMOIP'}


class IduForms(object):

    ################# Select List Functions ##################################
    @staticmethod
    def select_list_ingress(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        ingress_name_value_dic = {}
        # call the function of common_controller
        # country_code_select_list_name_value_dic - This store the name and value of select list
        # This returns the select list string in html format
        for i in range(0, 64):
            j = 64 * i
            if i > 15:
                break
            else:
                ingress_name_value_dic.setdefault('name', []).append(str(j))
                ingress_name_value_dic.setdefault('value', []).append(j)
                continue
        for i in range(1, 11):
            j = i * 1000
            ingress_name_value_dic.setdefault('name', []).append(str(j))
            ingress_name_value_dic.setdefault('value', []).append(j)
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(ingress_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_list_egress(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        egress_name_value_dic = {}
        # call the function of common_controller
        # country_code_select_list_name_value_dic - This store the name and value of select list
        # This returns the select list string in html format
        for i in range(0, 64):
            j = 64 * i
            if i > 15:
                break
            else:
                egress_name_value_dic.setdefault('name', []).append(str(j))
                egress_name_value_dic.setdefault('value', []).append(j)
                continue
        for i in range(1, 11):
            j = i * 1000
            egress_name_value_dic.setdefault('name', []).append(str(j))
            egress_name_value_dic.setdefault('value', []).append(j)
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(egress_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def enable_disable_select_list(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_list_name_value_dic = {}
        select_list_name_value_dic = {'name': ['Disable',
                                               'Enable'], 'value': [0, 1]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def port_mirroring_select_list(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        port_mirroring_name_value_dic = {}
        port_mirroring_name_value_dic = {'name': ['ODU', 'LAN1',
                                                  'LAN2'], 'value': [0, 2, 3]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(port_mirroring_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_entry_type(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        entry_type_name_value_dic = {}
        entry_type_name_value_dic = {'name': ['Static', 'Mgmt',
                                              'Priority Override'], 'value': ['0', '1', '2']}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(entry_type_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_priority(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_priority_name_value_dic = {}
        select_priority_name_value_dic = {'name': ['0', '1', '2',
                                                   '3'], 'value': ['0', '1', '2', '3']}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_priority_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_clock_source(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_priority_name_value_dic = {}
        select_priority_name_value_dic = {'name': ['RCLK',
                                                   'Adaptive'], 'value': [0, 1]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_priority_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_line_type(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_priority_name_value_dic = {}
        select_priority_name_value_dic = {'name': ['Framed Without CRC',
                                                   'Framed With CRC', 'UnFramed'], 'value': [1, 2, 0]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_priority_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_line_code(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_priority_name_value_dic = {}
        select_priority_name_value_dic = {'name': ['HDB3'], 'value': [0]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_priority_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_admin_state(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_priority_name_value_dic = {}
        select_priority_name_value_dic = {'name': ['Locked',
                                                   'Unlocked'], 'value': [0, 1]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_priority_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_link_mode(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_link_mode_name_value_dic = {}
        select_link_mode_name_value_dic = {'name': ['Auto',
                                                    '100 Mbps', '10 Mbps'], 'value': [0, 2, 3]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_link_mode_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_mac_auth(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_mac_auth_name_value_dic = {}
        select_mac_auth_name_value_dic = {'name': ['Disable',
                                                   'Accept Specific MAC'], 'value': [0, 1]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_mac_auth_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_mirror_direction(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_mirror_name_value_dic = {}
        select_mirror_name_value_dic = {'name': ['Disable', 'Tx',
                                                 'Tx and Rx'], 'value': [0, 1, 2]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_mirror_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_dotq_mode(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_dotq_name_value_dic = {}
        select_dotq_name_value_dic = {'name': ['Disable',
                                               'Fallback', 'Check'], 'value': [0, 1, 2]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_dotq_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_mac_flow(selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        select_mac_flow_name_value_dic = {}
        select_mac_flow_name_value_dic = {'name': ['Disable',
                                                   'Enable'], 'value': [0, 1]}
        return MakeSelectListUsingDictionary.make_select_list_using_dictionary(select_mac_flow_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    @staticmethod
    def select_e1_port(port_num):
        select_list_html = ""
        for row in range(1, 5):
            if port_num != "":
                if row == int(port_num):
                    select_list_html += "<option value=\"%s\" selected=\"selected\"> %s </option>" % (row, row)
                else:
                    select_list_html += "<option value=\"%s\"> %s </option>" % (
                        row, row)
            else:
                select_list_html += "<option value=\"%s\"> %s </option>" % (
                    row, row)
        return select_list_html

    @staticmethod
    def select_timeslot(timeslots):
        select_list_html = ""
        pos = [0]
        if len(timeslots) > 0:
            for k in range(0, len(timeslots)):
                if int(timeslots[k]) == 1:
                    pos.append(k)
        for row in range(0, 32):
            if row == 0:
                select_list_html += "<option value=\"%s\" disabled=\"disabled\"> %s </option>" % (
                    row, row)
            else:
                if len(pos) > 0:
                    if row in pos:
                        select_list_html += "<option value=\"%s\" selected=\"selected\"> %s </option>" % (
                            row, row)
                    else:
                        select_list_html += "<option value=\"%s\"> %s </option>" % (
                            row, row)
                else:
                    select_list_html += "<option value=\"%s\"> %s </option>" % (
                        row, row)
        return select_list_html

    @staticmethod
    def select_disable_enable_list(value):
        select_list_html = ""
        if value == "":
            select_list_html += "<option value=\"1\">Enable</option>\
                            <option value=\"0\">Disable</option>"
        elif int(value) == 1:
            select_list_html += "<option value=\"1\" selected=\"selected\">Enable</option>\
                            <option value=\"0\">Disable</option>"

        else:
            select_list_html += "<option value=\"1\">Enable</option>\
                            <option value=\"0\" selected=\"selected\">Disable</option>"
        return select_list_html
################ Select List functions End ###############################

################################  ADVANCED CONFIGURATION #################
    @staticmethod
    def network_configuration():
        form_str = ""
        form_str += "<form id = \"\" name = \"\" action=\"\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">IP Address</label>\
                            <input type=\"text\" id=\"\" name = \"\" value = \"\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">IP Netmask</label>\
                            <input type = \"text\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">IP Default Gateway</label>\
                            <input type = \"text\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">DHCP state</label>\
                            <input type=\"checkbox\" name=\"\" value=\"\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Management VLAN</label>\
                            <input type=\"checkbox\" name=\"\" value=\"\"/>&nbsp\
                            <input type = \"text\" id =\"\" name = \"\" value = \"\" maxsize = \"15\" style=\"width:30px\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">TDM IP Address</label>\
                            <input type = \"text\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"\" value=\"Save\" id=\"\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\"  id=\"\" value=\"Retry\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Cancel\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Ok\"/ style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                        </div>\
                    </form>"
        return form_str

    @staticmethod
    def POE(host_id, selected_device):
        obj_bll = IduGetData()
        poe_data = obj_bll.common_get_data("IduPoeConfigurationTable", host_id)
        form_str = ""
        form_str += "<form id=\"poe_form\" name=\"poe_form\" action=\"poe_form_action.py\" method =\"get\">\
                        <table class=\"yo-table\" style=\"width:100%%\" cellspacing=\"0\" cellpadding=\"0\">\
                            <th>Port Number</th>\
                            <th>Admin State</th>\
                            <tr>\
                                <td>\
                                    odu1\
                                </td>\
                                <td>\
                                    %s\
                                </td>\
                            </tr>\
                        </table>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('poe_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('poe_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('poe_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('poe_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\" />\
                        </div>\
                    </form>" % (IduForms.enable_disable_select_list(poe_data[0].poeAdminStatus if isinstance(poe_data[0].poeAdminStatus, int) else int(poe_data[0].poeAdminStatus) if len(poe_data) > 0 else "", 'enabled', 'iduConfiguration.poeConfigurationTable.poeAdminStatus', 'false', 'Admin State'),
                                host_id, selected_device)
        return form_str

    @staticmethod
    def header_type():
        form_str = ""
        form_str += "<form id = \"\" name = \"\" action=\"\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Header</label>\
                            <select name=\"\" id=\"\">\
                                <option value\"0\">MEF</option>\
                                <option value\"1\">UDP</option>\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"\" value=\"Save\" id=\"\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\"  id=\"\" value=\"Retry\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Cancel\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Ok\"/ style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                        </div>\
                    </form>"
        return form_str

    @staticmethod
    def temperature(host_id, selected_device):
        obj_bll = IduGetData()
        temperature_data = obj_bll.common_get_data(
            "IduTemperatureSensorConfigurationTable", host_id)
        form_str = ""
        form_str += "<form id=\"temperature_form\" name=\"temperature_form\" action=\"temperature_form_action.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Lower Threshold</label>\
                            <input type=\"text\" id=\"iduConfiguration.temperatureSensorConfigurationTable.tempMin\" name=\"iduConfiguration.temperatureSensorConfigurationTable.tempMin\" value=\"%s\" maxsize=\"15\"/>\
                            (%s)&nbsp;<span style=\"font-size:9px\">-40 to 70</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Upper Threshold</label>\
                            <input type = \"text\" id =\"iduConfiguration.temperatureSensorConfigurationTable.tempMax\" name = \"iduConfiguration.temperatureSensorConfigurationTable.tempMax\" value = \"%s\" maxsize = \"15\"/>\
                            (%s)&nbsp;<span style=\"font-size:9px\">-40 to 70</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('temperature_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('temperature_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('temperature_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('temperature_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\" />\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"temperature\" tablename=\"temperatureSensorConfigurationTable\"/>\
                        </div>\
                    </form>" % (temperature_data[0].tempMin if len(temperature_data) > 0 else "", "\xc2\xb0C", temperature_data[0].tempMax if len(temperature_data) > 0 else "", "\xc2\xb0C", host_id, selected_device)
        return form_str

    @staticmethod
    def clock():
        form_str = ""
        form_str += "<form id = \"\" name = \"\" action=\"\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Clock Mode</label>\
                            <select name=\"\" id=\"\">\
                                <option value\"1\">One Clock</option>\
                                <option value\"2\">Two Clock</option>\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Clock Type</label>\
                            <select name=\"\" id=\"\">\
                                <option value=\"1\">STRATUM1</option>\
                                <option value=\"2\">STRATUM2</option>\
                                <option value=\"3\">STRATUM3</option>\
                                <option value=\"4\">STRATUM3E</option>\
                                <option value=\"5\">STRATUM4</option>\
                            </select>\
                        </div>\
                         <div class=\"row-elem\">\
                            <input type=\"submit\" name=\"temp_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"temp_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"temp_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"temp_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\" />\
                        </div>\
                    </form>"
        return form_str

    @staticmethod
    def datetime(host_id, selected_device):
        obj_bll = IduGetData()
        date_time_data = obj_bll.common_get_data(
            "IduRtcConfigurationTable", host_id)
        form_str = ""
        form_str += "<form id=\"date_time_form\" name=\"date_time_form\" action=\"date_time_action.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Year</label>\
                            <input type = \"text\" id =\"iduConfiguration.rtcConfigurationTable.year\" name=\"iduConfiguration.rtcConfigurationTable.year\" value = \"%s\" maxsize = \"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">1970 to 2037</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Month</label>\
                            <input type = \"text\" id =\"iduConfiguration.rtcConfigurationTable.month\" name=\"iduConfiguration.rtcConfigurationTable.month\" value = \"%s\" maxsize = \"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">1 to 12</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Day</label>\
                            <input type = \"text\" id =\"iduConfiguration.rtcConfigurationTable.day\" name=\"iduConfiguration.rtcConfigurationTable.day\" value = \"%s\" maxsize = \"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">1 to 31</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Hour</label>\
                            <input type = \"text\" id =\"iduConfiguration.rtcConfigurationTable.hour\" name=\"iduConfiguration.rtcConfigurationTable.hour\" value = \"%s\" maxsize = \"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">0 to 23</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Minute</label>\
                            <input type = \"text\" id =\"iduConfiguration.rtcConfigurationTable.min\" name=\"iduConfiguration.rtcConfigurationTable.min\" value = \"%s\" maxsize = \"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">0 to 59</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Seconds</label>\
                            <input type = \"text\" id =\"iduConfiguration.rtcConfigurationTable.sec\" name=\"iduConfiguration.rtcConfigurationTable.sec\" value = \"%s\" maxsize = \"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">0 to 50</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('date_time_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('date_time_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('date_time_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('date_time_form',this)\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"datetime\" tablename=\"rtcConfigurationTable\"/>\
                        </div>\
                    </form>" % (date_time_data[0].year if len(date_time_data) > 0 else "", date_time_data[0].month if len(date_time_data) > 0 else "",
                                date_time_data[0].day if len(
                                date_time_data) > 0 else "", date_time_data[0].hour if len(date_time_data) > 0 else "",
                                date_time_data[0].min if len(
                                date_time_data) > 0 else "", date_time_data[0].sec if len(date_time_data) > 0 else "",
                                host_id, selected_device)
        return form_str

    @staticmethod
    def table_alarm_port():
        alarm_table_str = ""
        alarm_table_str += " <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                                <th>\
                                    Alarm pin\
                                </th>\
                                <th>\
                                    Alarm String\
                                </th>\
                                <th>\
                                    Alarm level\
                                </th>\
                                <th>\
                                    Admin State\
                                </th>\
                                <th>\
                                    Port State\
                                </th>\
                                <th>\
                                   Action;\
                                </th>\
                                "
        for i in range(0, 4):
            alarm_table_str += " <tr>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td><img src='images/edit16.png' onclick=\"alarmPortFormEdit('%s')\" style=\"cursor:pointer\"  /></td>\
                                  </tr>" % (i + 1, i + 1, i + 1, i + 1, i + 1, i + 1)
        alarm_table_str += "</table>"
        return alarm_table_str

    @staticmethod
    def alarm_port_show_table():
        form_str = ""
        form_str += "\
                    <div class=\"row-elem\">\
                        %s\
                    </div>\
                    " % (IduForms.table_alarm_port)
        return form_str

    @staticmethod
    def alarm_port_form(alarm_port_list):
        form_str = ""
        form_str += "<form id = \"\" name = \"\" action=\"\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Alarm Pin</label>\
                            <input type = \"text\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Alarm String</label>\
                            <input type = \"text\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Alarm Level</label>\
                            <select name=\"\" id=\"\">\
                                <option value=\"0\">Critical</option>\
                                <option value=\"1\">Major</option>\
                                <option value=\"2\">Minor</option>\
                                <option value=\"3\">info</option>\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Admin State</label>\
                            <select name=\"\" id=\"\">\
                                <option value=\"0\">Locked</option>\
                                <option value=\"1\">unlocked</option>\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Port State</label>\
                            <select name=\"\" id=\"\">\
                                <option value=\"\">Not Applicable(N/A)</option>\
                                <option value=\"0\">Low</option>\
                                <option value=\"1\">High</option>\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"\" value=\"Save\" id=\"\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\"  id=\"\" value=\"Retry\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Cancel\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Ok\"/ style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                        </div>\
                    </form>\
                    "
        return form_str
################################ END ADVANCED CONFIGURATION FORMS ########

################################  PORT CONFIGURATION #####################

    @staticmethod
    def table_port_configuration(host_id, selected_device):
        global dict
        port_table_str = ""
        obj_bll = IduGetData()

        admin_dic = {0: "Locked", 1: "Unlocked"}
        link_mode_dic = {0: "Auto", 2: "100 Mbps", 3: "10 Mbps"}
        mac_auth_state_dic = {0: "Disable", 1: "Accept Specific Mac"}
        mirro_direction_dic = {0: "Disable", 1: "Tx", 2: "Tx abd Rx"}
        vlan_dotq_mode_dic = {0: "Disable", 1: "Fallback", 2: "Check"}
        mac_flow_control_dic = {0: "Disable", 1: "Enable"}

        port_configuration_data = obj_bll.common_get_data(
            "IduSwitchPortconfigTable", host_id)
        port_table_str += "<input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"table_port_configuration\" tablename=\"switchPortconfigTable\"/>"
        port_table_str += "<table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\">\
                                <th>\
                                    Port\
                                </th>\
                                <th>\
                                    Link Mode\
                                </th>\
                                <th>\
                                    Port VID\
                                </th>\
                                <th>\
                                    Auth State\
                                </th>\
                                <th>\
                                    Mirror Direction\
                                </th>\
                                <th>\
                                   VLAN Dotq Mode\
                                </th>\
                                <th>\
                                    MAC Flow Control\
                                </th>\
                                <!--<th>\
                                    Egress Mode\
                                </th>-->\
                                <th>\
                                    Admin State\
                                </th>\
                                <th>\
                                   Action\
                                </th>\
                                "
        if len(port_configuration_data) > 0:
            for i in range(0, len(port_configuration_data)):
                port_table_str += " <tr>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <!--<td>%s</td>-->\
                                        <td>%s</td>\
                                        <td><img src='images/edit16.png' title=\"Edit Port\" class=\"n-reconcile\" style=\"cursor:pointer\"  onclick=\"portConfigurationFormEdit('%s','%s','idu_switchPortconfigTable_id','IduSwitchPortconfigTable','%s')\" /></td>\
                                    </tr>" % (dict[port_configuration_data[i].switchportNum],
                                              link_mode_dic[port_configuration_data[i]
                                                            .swlinkMode], port_configuration_data[i].portvid,
                                              mac_auth_state_dic[port_configuration_data[
                                                                 i].macauthState],
                                              mirro_direction_dic[port_configuration_data[
                                                                  i].mirroringdirection],
                                              vlan_dotq_mode_dic[port_configuration_data[
                                                                 i].portdotqmode],
                                              mac_flow_control_dic[port_configuration_data[
                                                                   i].macflowcontrol], i + 1, admin_dic[port_configuration_data[i].swadminState],
                                              port_configuration_data[i].idu_switchPortconfigTable_id, host_id, selected_device)
        port_table_str += "</table>"
        return port_table_str

    @staticmethod
    def port_configuration_show_table(host_id, selected_device):
        form_str = ""
        form_str += "%s" % (
            IduForms.table_port_configuration(host_id, selected_device))
        return form_str

    @staticmethod
    def port_configuration_form(port_configuration_list, host_id, selected_device, index):
        form_str = ""
        form_str += "<form id=\"swt_port_config_form\" name=\"swt_port_config_form\" action=\"swt_port_config_action.py\" method =\"get\" style=\"overflow:hidden;\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Port</label>\
                            <input type = \"text\" id =\"port_config_id\" name = \"port_config_id\" value = \"%s\" maxsize = \"15\" readonly=\"readonly\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Admin State</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Link Mode</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Port VID</label>\
                            <input type = \"text\" id =\"switch.switchPortconfigTable.portvid\" name = \"switch.switchPortconfigTable.portvid\" value = \"%s\" maxsize = \"4\"/>\
                            &nbsp;<span style=\"font-size:9px\">0 to 4095</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Auth State</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Mirroring Direction</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">MAC Flow Control</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">VLAN Dotq Mode</label>\
                            %s\
                        </div>\
                        <!--<div class=\"row-elem\">\
                            <label class=\"lbl\">Egress Mode</label>\
                            <select name=\"\" id=\"\" disabled=\"disabled\">\
                                <option value=\"\">Select Egresss Mode</option>\
                                <option value=\"0\">Unmodified</option>\
                                <option value=\"1\">Untagged</option>\
                                <option value=\"2\">Tagged</option>\
                            </select>\
                        </div>-->\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('swt_port_config_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('swt_port_config_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('swt_port_config_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('swt_port_config_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"device_type\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"index_id\" value=\"%s\"/>\
                        </div>\
                    </form>\
                    " % (port_configuration_list[0].switchportNum,
                         IduForms.select_admin_state(port_configuration_list[0].swadminState if len(
                                                     port_configuration_list) > 0 else "", "enabled", "switch.switchPortconfigTable.swadminState", False, "Admin State"),
                         IduForms.select_link_mode(port_configuration_list[0].swlinkMode if len(
                                                   port_configuration_list) > 0 else "", "enabled", "switch.switchPortconfigTable.swlinkMode", False, "Link Mode"),
                         port_configuration_list[0].portvid if len(
                         port_configuration_list) > 0 else "",
                         IduForms.select_mac_auth(port_configuration_list[0].macauthState if len(
                                                  port_configuration_list) > 0 else "", "enabled", "switch.switchPortconfigTable.macauthState", False, "Mac Auth State"),
                         IduForms.select_mirror_direction(port_configuration_list[0].mirroringdirection if len(
                                                          port_configuration_list) > 0 else "", "enabled", "switch.switchPortconfigTable.mirroringdirection", False, "Mirror Direction"),
                         IduForms.select_mac_flow(port_configuration_list[0].macflowcontrol if len(
                                                  port_configuration_list) > 0 else "", "enabled", "switch.switchPortconfigTable.macflowcontrol", False, "Mac Flow Control"),
                         IduForms.select_dotq_mode(port_configuration_list[0].portdotqmode if len(
                                                   port_configuration_list) > 0 else "", "enabled", "switch.switchPortconfigTable.portdotqmode", False, "Dotq Mode"),
                         host_id, selected_device, index
                         )
        return form_str

    @staticmethod
    def table_port_bandwidth(host_id, selected_device):
        global dict
        obj_bll = IduGetData()
        port_bw_data = obj_bll.common_get_data("IduPortBwTable", host_id)
        port_bandwidth_str = ""
        port_bandwidth_str += "<input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"table_port_bandwidth\" tablename=\"portBwTable\"/>"
        port_bandwidth_str += " <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                                <th>\
                                    Port\
                                </th>\
                                <th>\
                                    Ingress (Kbps)\
                                </th>\
                                <th>\
                                    Egress (Kbps)\
                                </th>\
                                <th>\
                                    Action\
                                </th>\
                                "
        if len(port_bw_data) > 0:
            for i in range(0, len(port_bw_data)):
                port_bandwidth_str += " <tr>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td><img src='images/edit16.png'  title=\"Edit Port Bandwidth\" class=\"n-reconcile\" style=\"cursor:pointer\"  onclick=\"portBandwidthFormEdit('%s','%s','idu_portBwTable_id','IduPortBwTable','%s')\" /></td>\
                                      </tr>" % (dict[port_bw_data[i].switchportnum], port_bw_data[i].ingressbwvalue, port_bw_data[i].egressbwvalue,
                                                port_bw_data[i].idu_portBwTable_id, host_id, selected_device)
        port_bandwidth_str += "</table>"
        return port_bandwidth_str

    @staticmethod
    def port_bandwidth_show_table(host_id, selected_device):
        form_str = ""
        form_str += "%s" % (
            IduForms.table_port_bandwidth(host_id, selected_device))
        return form_str

    @staticmethod
    def port_bandwidth_form(port_bw_list, host_id, selected_device, index):
        if len(port_bw_list) > 0:
            form_str = ""
            form_str += "<form id=\"swt_port_bandwidth_form\" name=\"swt_port_bandwidth_form\" action=\"swt_bw_action.py\" method =\"get\" style=\"overflow:hidden;\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Port</label>\
                                <input type=\"text\" id=\"bw_id\" name=\"bw_id\" value=\"%s\" maxsize = \"15\" readonly=\"readonly\"/>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Ingress</label>\
                                %s\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Egress</label>\
                                %s\
                            </div>\
                            <div class=\"row-elem\">\
                                <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('swt_port_bandwidth_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('swt_port_bandwidth_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('swt_port_bandwidth_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('swt_port_bandwidth_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"device_type\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"index_id\" value=\"%s\"/>\
                        </div>\
                        </form>\
                        " % (port_bw_list[0].switchportnum, IduForms.select_list_ingress(port_bw_list[0].ingressbwvalue, 'enabled', 'switch.portBwTable.ingressbwvalue', 'false', 'Select Ingress'),
                             IduForms.select_list_egress(
                             port_bw_list[0].egressbwvalue, 'enabled',
                             'switch.portBwTable.egressbwvalue', 'false', 'Select Egress'), host_id, selected_device, index)
            return form_str

    @staticmethod
    def table_e1_port(host_id, selected_device):
        try:
            global dict
            obj_bll = IduGetData()
            admin_dic = {0: "Locked", 1: "Unlocked"}
            clock_source_dic = {0: "RCLK", 1: "Adaptive"}
            line_code_dic = {0: "HDB3", 1: "AMI"}
            line_type_dic = {1: "Framed Without CRC", 2:
                            "Framed With CRC", 0: "Unframed"}
            port_e1_data = obj_bll.common_get_data(
                "IduE1PortConfigurationTable", host_id)
            # dss=[]
            # dss=len(port_e1_data[0])
            port_e1_str = ""
            #
            port_e1_str += "<input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"table_e1_port\" tablename=\"e1PortConfigurationTable\"/>"
            port_e1_str += "<table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                                    <th>\
                                       E1 Port Number\
                                    </th>\
                                    <th>\
                                        Clock Source\
                                    </th>\
                                    <th>\
                                        Line Type\
                                    </th>\
                                    <!--<th>\
                                        Line Code\
                                    </th>-->\
                                    <th>\
                                        Admin State\
                                    </th>\
                                    <th>\
                                        Action\
                                    </th>\
                                    "
            if len(port_e1_data) > 0:
                for i in range(0, len(port_e1_data)):
                    port_e1_str += "<tr>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <!--<td>%s</td>-->\
                                            <td>%s</td>\
                                            <td><img title=\"Edit Port\" class=\"n-reconcile\" src='images/edit16.png' style=\"cursor:pointer\"  onclick=\"porte1FormEdit('%s','%s','idu_e1PortConfigurationTable_id','IduE1PortConfigurationTable','%s')\" /></td>\
                                    </tr>" % (port_e1_data[i].portNumber,
                                            clock_source_dic[port_e1_data[i]
                                                .clockSource], line_type_dic[
                                                    port_e1_data[i].lineType],
                                            line_code_dic[port_e1_data[i].lineCode], admin_dic[port_e1_data[i].adminState], port_e1_data[i].idu_e1PortConfigurationTable_id, host_id, selected_device)
            port_e1_str += "</table>"
            return str(port_e1_str)
        except Exception as e:
            return str(e)

    @staticmethod
    def form_e1_port(e1_port_list, host_id, selected_device, index):
        if len(e1_port_list) > 0:
            form_str = ""
            form_str += "<form id=\"e1_port_form\" name=\"e1_port_form\" action=\"e1_port_form_action.py\" method =\"get\" style=\"overflow:hidden;\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">E1 Port Number</label>\
                                <input type=\"text\" id=\"e1_port_id\" name=\"e1_port_id\" value=\"%s\" maxsize = \"15\" readonly=\"readonly\"/>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Clock Source</label>\
                                %s\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Line Type</label>\
                                %s\
                            </div>\
                            <!--<div class=\"row-elem\">\
                                <label class=\"lbl\">Line Code</label>\
                                %s\
                            </div>-->\
                            <!--<div class=\"row-elem\">\
                                <label class=\"lbl\" disabled=\"disabled\">Admin State</label>\
                                %s\
                            </div>-->\
                            <div class=\"row-elem\">\
                                <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('e1_port_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('e1_port_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('e1_port_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('e1_port_form',this)\" class=\"yo-small yo-button\" />\
                                <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"device_type\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"index_id\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"adminState\" value=\"%s\"/>\
                        </div>\
                        </form>\
                        " % (e1_port_list[0].portNumber, IduForms.select_clock_source(e1_port_list[0].clockSource, "enabled", "iduConfiguration.e1PortConfigurationTable.clockSource", "false", "Clock Source"),
                           IduForms.select_line_type(
                               e1_port_list[0].lineType, "enabled",
                                                     "iduConfiguration.e1PortConfigurationTable.lineType", "false", "Line Type"),
                           IduForms.select_line_code(
                               e1_port_list[0].lineCode, "enabled",
                                                     "iduConfiguration.e1PortConfigurationTable.lineCode", "false", "Line Code"),
                           IduForms.select_admin_state(
                               e1_port_list[0].adminState, "disabled",
                                                       "iduConfiguration.e1PortConfigurationTable.adminState", "false", "Admin State"),
                           host_id, selected_device, index, e1_port_list[0].adminState)
            return form_str

    @staticmethod
    def port_e1_port_show_table(host_id, selected_device):
        form_str = ""
        form_str += "%s" % (IduForms.table_e1_port(host_id, selected_device))
        return form_str

    @staticmethod
    def table_port_QinQ(host_id, selected_device):
        try:
            global dict
            obj_bll = IduGetData()
            port_qinq_data = obj_bll.common_get_data(
                "IduPortqinqTable", host_id)
            port_QinQ_str = ""
            port_QinQ_str += "<input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"table_port_QinQ\" tablename=\"portqinqTable\"/>"
            port_QinQ_str += "<table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                                    <th>\
                                        Port\
                                    </th>\
                                    <th>\
                                        QinQ State\
                                    </th>\
                                    <th>\
                                        Provider Tag\
                                    </th>\
                                    <th>\
                                        Action\
                                    </th>\
                                    "
            if len(port_qinq_data) > 0:
                for i in range(0, len(port_qinq_data)):
                    if port_qinq_data[i].switchportnumber in dict:
                        if dict[port_qinq_data[i].switchportnumber] == "LAN2":
                            continue
                        else:
                            num = port_qinq_data[i].providertag
                            temp = int(num / 4096)
                            num = num - temp * (4096)
                            res = 1000 * temp
                            # Step 2
                            temp = int(num / 256)
                            num = num - temp * (256)
                            res = res + 100 * temp
                            ## step 3
                            temp = int(num / 16)
                            num = num - temp * (16)
                            res = res + 10 * temp
                            # Step 4
                            temp = num
                            # result
                            res = res + temp

                            port_QinQ_str += "<tr>\
                                                    <td>%s</td>\
                                                    <td>%s</td>\
                                                    <td>%s</td>\
                                                    <td><img title=\"Edit Port QinQ\" class=\"n-reconcile\" src='images/edit16.png' style=\"cursor:pointer\"  onclick=\"portQinQFormEdit('%s','%s','idu_portqinqTable_id','IduPortqinqTable','%s')\" /></td>\
                                                  </tr>" % (port_qinq_data[i].switchportnumber in dict and dict[port_qinq_data[i].switchportnumber] or "",
                                                          "Disable" if port_qinq_data[
                                                              i].portqinqstate == 0 or port_qinq_data[i].portqinqstate == '0' else "Enable",
                                                          res, port_qinq_data[i].idu_portqinqTable_id, host_id, selected_device)
                port_QinQ_str += "</table>"
            return port_QinQ_str
        except Exception as e:
            return str(e)

    @staticmethod
    def port_QinQ_show_table(host_id, selected_device):
        form_str = ""
        form_str += "%s" % (IduForms.table_port_QinQ(host_id, selected_device))
        return form_str

    @staticmethod
    def port_QinQ_form(port_QinQ_list, host_id, selected_device, index):
        form_str = ""
        if len(port_QinQ_list) > 0:
            num = port_QinQ_list[0].providertag
            temp = int(num / 4096)
            num = num - temp * (4096)
            res = 1000 * temp
            # Step 2
            temp = int(num / 256)
            num = num - temp * (256)
            res = res + 100 * temp
            ## step 3
            temp = int(num / 16)
            num = num - temp * (16)
            res = res + 10 * temp
            # Step 4
            temp = num
            # result
            res = res + temp
        form_str += "<form id=\"qinq_form\" name=\"qinq_form\" action=\"qinq_form_action.py\" method =\"get\" style=\"overflow:hidden;\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Port</label>\
                            <input type=\"text\" id=\"qinq_id\" name=\"qinq_id\" value=\"%s\" maxsize=\"15\" readonly=\"readonly\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">QinQ State</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Provider Tag</label>\
                            <input type=\"text\" id=\"switch.portqinqTable.providertag\" name=\"switch.portqinqTable.providertag\" value=\"%s\" maxlength =4  />\
                            &nbsp;<span style=\"font-size:9px\">0 to 9999</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('qinq_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('qinq_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('qinq_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('qinq_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"index_id\" value=\"%s\"/>\
                        </div>\
                    </form>\
                    " % (port_QinQ_list[0].switchportnumber if len(port_QinQ_list) > 0 else "",
                       IduForms.enable_disable_select_list(port_QinQ_list[0].portqinqstate if len(
                           port_QinQ_list) > 0 else "", 'enabled', 'switch.portqinqTable.portqinqstate', 'false', 'Select QinQ State'),
                       res if len(port_QinQ_list) > 0 else "", host_id, selected_device, index)
        return form_str

    @staticmethod
    def port_mirroring(host_id, selected_device):
        obj_bll = IduGetData()
        mirroring_data = obj_bll.common_get_data(
            "IduMirroringportTable", host_id)
        form_str = ""
        form_str += "<form id=\"mirror_port_form\" name=\"mirror_port_form\" action=\"mirror_port_form_action.py\" method=\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Monitoring Port</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('mirror_port_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('mirror_port_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('mirror_port_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('mirror_port_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"special_case\" value=\"%s\"/>\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"port_mirroring\" tablename=\"mirroringportTable\"/>\
                        </div>\
                    </form>" % (IduForms.port_mirroring_select_list(mirroring_data[0].mirroringport if len(mirroring_data) > 0 else "", 'enabled', 'switch.mirroringportTable.mirroringport', 'false', 'Monitoring Port State'),
                              host_id, selected_device, 1)
        return form_str

    @staticmethod
    def table_port_ATU():
        port_ATU_str = ""
        port_ATU_str += " <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                                <th>\
                                    ATU ID\
                                </th>\
                                <th>\
                                    Entry Type\
                                </th>\
                                <th>\
                                    Priority\
                                </th>\
                                <th>\
                                    MAC Address\
                                </th>\
                                <th>\
                                    Member Port\
                                </th>\
                                <th>\
                                    Action\
                                </th>\
                                "
        for i in range(0, 16):
            port_ATU_str += " <tr>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td><img src='images/edit16.png' style=\"cursor:pointer\"  onclick=\"portATUFormEdit('%s')\" /></td>\
                                  </tr>" % (i + 1, i + 1, i + 1, i + 1, i + 1, i + 1)
        port_ATU_str += "</table>"
        return port_ATU_str

    @staticmethod
    def port_ATU_show_table():
        form_str = ""
        form_str += "%s" % (IduForms.table_port_ATU())
        return form_str

    @staticmethod
    def port_ATU_form(port_ATU_list):
        form_str = ""
        form_str += "<form id = \"\" name = \"\" action=\"\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Port</label>\
                            <input type = \"text\" id =\"\" name = \"\" value = \"\" maxsize = \"15\" disabled=\"disabled\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Entry Type</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Priority</label>\
                            %s\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">MAC Address</label>\
                            <input type = \"text\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Member Ports</label>\
                            <input type = \"checkbox\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>ODU\
                            <input type = \"checkbox\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>LAN1\
                            <input type = \"checkbox\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>LAN2\
                            <input type = \"checkbox\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>CPU\
                            <input type = \"checkbox\" id =\"\" name = \"\" value = \"\" maxsize = \"15\"/>Maxim\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"\" value=\"Save\" id=\"\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\"  id=\"\" value=\"Retry\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Cancel\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Ok\"/ style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" name = \"host_id\" value=\"\" style=\"Display:None\"/>\
                            <input type = \"hidden\" name = \"device_type\" value=\"\" />\
                        </div>\
                    </form>\
                    " % (IduForms.select_entry_type('', 'enabled', '', 'false', 'Select Entry Type'),
                       IduForms.select_priority('', 'enabled', '', 'false', 'Select Priority'))
        return form_str

    @staticmethod
    def table_port_Vlan(host_id, selected_device):
        obj_bll = IduGetData()
        port_vlan_data = obj_bll.common_get_data("IduVlanconfigTable", host_id)
        flag = 0
        vlan_dic = {}
        port_vlan_str = ""
        port_vlan_str += "<input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"table_port_Vlan\" tablename=\"vlanconfigTable\"/>"
        port_vlan_str += " <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                                <th>\
                                    VLAN ID\
                                </th>\
                                <th>\
                                    VLAN Name\
                                </th>\
                                <th>\
                                    Member Ports\
                                </th>\
                                <th>\
                                    VLAN Tag\
                                </th>\
                                <th style=\"text-align:left;\">\
                                    Action\
                                </th>\
                                "

        if len(port_vlan_data) > 0:
            for j in range(0, len(port_vlan_data)):
                member_ports = ""
                flag = 0
                number = int(port_vlan_data[j].memberports)
                port0 = number % 2
                if port0 > 0:
                    member_ports += "ODU"
                    flag = 1
                temp = int(number / 4)
                port2 = temp % 2
                if port2 > 0:
                    if flag == 1:
                        member_ports += ",LAN1"
                    else:
                        flag = 2
                        member_ports += "LAN1"
                temp = int(number / 8)
                port3 = temp % 2
                if port3 > 0:
                    if flag == 1:
                        member_ports += ",LAN2"
                    elif flag == 2:
                        member_ports += ",LAN2"
                    else:
                        flag = 3
                        member_ports += "LAN2"
                temp = int(number / 16)
                port4 = temp % 2
                if port4 > 0:
                    if flag == 1:
                        member_ports += ",CPU"
                    elif flag == 2:
                        member_ports += ",CPU"
                    elif flag == 3:
                        member_ports += ",CPU"
                    else:
                        flag = 4
                        member_ports += "CPU"
                temp = int(number / 32)
                port5 = temp % 2
                if port5 > 0:
                    if flag == 1:
                        member_ports += ",TDMOIP"
                    elif flag == 2:
                        member_ports += ",TDMOIP"
                    elif flag == 3:
                        member_ports += ",TDMOIP"
                    elif flag == 4:
                        member_ports += ",TDMOIP"
                    else:
                        member_ports += "TDMOIP"

                vlan_dic[
                    port_vlan_data[j].vlanid] = [port_vlan_data[j].vlanname, member_ports, port_vlan_data[j].vlantag,
                                                      port_vlan_data[j].idu_vlanconfigTable_id]

        for i in range(0, 16):
            if i + 1 in vlan_dic:
                port_vlan_str += " <tr>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td >%s</td>\
                                        <td style=\"text-align: left;\"><img title=\"Edit VLAN\" class=\"n-reconcile\" src='images/edit16.png' style=\"cursor:pointer\" onclick=\"portVlanFormAddEdit('%s','%s','idu_vlanconfigTable_id','IduVlanconfigTable','%s','%s','%s')\" />&nbsp;&nbsp;&nbsp;&nbsp;\
                                        <img title=\"Delete VLAN\" class=\"n-reconcile\" src='images/delete16.png' onclick=\"portVlanFormDelete('%s')\" style=\"cursor:pointer\"  /></td>\
                                      </tr>" % (i + 1, vlan_dic[i + 1][0], vlan_dic[i + 1][1], vlan_dic[i + 1][2],
                                              vlan_dic[i + 1][3], host_id, selected_device, 1, i + 1, i + 1)
            else:
                port_vlan_str += " <tr>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td style=\"text-align: left;\"><img title=\"ADD VLAN\" class=\"n-reconcile\" src='images/add16.png' style=\"cursor:pointer\" onclick=\"portVlanFormAddEdit('%s','%s','idu_vlanconfigTable_id','IduVlanconfigTable','%s','%s','%s')\" style=\"cursor:pointer\"  /></td>\
                                      </tr>" % (i + 1, "", "", "",
                                              "", host_id, selected_device, 0, i + 1)

        port_vlan_str += "</table>"
        return port_vlan_str

    @staticmethod
    def port_Vlan_show_table():
        form_str = ""
        form_str += "%s" % (IduForms.table_port_vlan())
        return form_str

    @staticmethod
    def port_vlan_form(port_vlan_list, host_id, selected_device, port_vlan_id, addEdit, vlanid):
        form_str = ""
        port0 = ""
        port2 = ""
        port3 = ""
        port4 = ""
        port5 = ""
        if int(addEdit) == 1:
            if len(port_vlan_list) > 0:
                number = int(port_vlan_list[0].memberports)
                port0 = number % 2
                if port0 > 0:
                    port0 = "checked=true"
                else:
                    port0 = ""
                temp = int(number / 4)
                port2 = temp % 2
                if port2 > 0:
                    port2 = "checked=true"
                else:
                    port2 = ""
                temp = int(number / 8)
                port3 = temp % 2
                if port3 > 0:
                    port3 = "checked=true"
                else:
                    port3 = ""
                temp = int(number / 16)
                port4 = temp % 2
                if port4 > 0:
                    port4 = "checked=true"
                else:
                    port4 = ""
                temp = int(number / 32)
                port5 = temp % 2
                if port5 > 0:
                    port5 = "checked=true"
                else:
                    port5 = ""

        form_str += "<form id=\"vlan_add_form\" name=\"vlan_add_form\" action=\"vlan_form_action.py\" method =\"get\" style=\"overflow:hidden;\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">VLAN ID</label>\
                            <input type = \"text\" id =\"vlan_id\" name = \"vlan_id\" value = \"%s\" maxsize = \"15\" readonly=\"readonly\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">VLAN Name</label>\
                            <input type = \"text\" id =\"switch.vlanconfigTable.vlanname\" name = \"switch.vlanconfigTable.vlanname\" value = \"%s\" maxsize = \"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Member Ports</label>\
                            <input type=\"checkbox\" id =\"port0\" name = \"switch.vlanconfigTable.memberports\" value = \"1\" maxsize = \"15\" \"%s\" />ODU\
                            <input type=\"checkbox\" id =\"port2\" name = \"switch.vlanconfigTable.memberports\" value = \"4\" maxsize = \"15\" \"%s\" />LAN1\
                            <input type=\"checkbox\" id =\"port3\" name = \"switch.vlanconfigTable.memberports\" value = \"8\" maxsize = \"15\" \"%s\" />LAN2\
                            <input type=\"checkbox\" id =\"port4\" name = \"switch.vlanconfigTable.memberports\" value = \"16\" maxsize = \"15\" \"%s\" />CPU\
                            <input type=\"checkbox\" id =\"port5\" name = \"switch.vlanconfigTable.memberports\" value = \"32\" maxsize = \"15\" \"%s\" />TDMOIP\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">VLAN Tag</label>\
                            <input type = \"text\" id =\"switch.vlanconfigTable.vlantag\" name = \"switch.vlanconfigTable.vlantag\" value = \"%s\" maxsize = \"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">1 to 4095</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('vlan_add_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('vlan_add_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('vlan_add_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('vlan_add_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"index_id\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"addEdit\" value=\"%s\"/>\
                            \
                        </div>\
                    </form>\
                    " % (vlanid, port_vlan_list[0].vlanname if len(port_vlan_list) > 0 else "" if int(addEdit) == 1 else "", port0, port2, port3, port4, port5,
                       port_vlan_list[0].vlantag if len(
                           port_vlan_list) > 0 else "" if int(addEdit) == 1 else "",
                       host_id, selected_device, port_vlan_id, addEdit)
        return form_str

    @staticmethod
    def e1_port_loopback():
        form_str = ""
        form_str += "<form id = \"\" name = \"\" action=\"\" method =\"get\">\
                        <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                            <th>\
                                Select\
                            </th>\
                            <th>\
                                Port No.\
                            </th>\
                            <th>\
                                Remote Loopback\
                            </th>\
                            <th>\
                                Local Loopback\
                            </th>\
                            <tr>\
                                <td><input type=\"radio\" name=\"\" value=\"\"/></td>\
                                <td><label class=\"lbl\">1</label></td>\
                                <td><input type=\"checkbox\" name=\"\" value=\"\"/></td>\
                                <td><input type=\"checkbox\" name=\"\" value=\"\"/></td>\
                            </tr>\
                            <tr>\
                                <td><input type=\"radio\" name=\"\" value=\"\"/></td>\
                                <td><label class=\"lbl\">2</label></td>\
                                <td><input type=\"checkbox\" name=\"\" value=\"\"/></td>\
                                <td><input type=\"checkbox\" name=\"\" value=\"\"/></td>\
                            </tr>\
                            <tr>\
                                <td><input type=\"radio\" name=\"\" value=\"\"/></td>\
                                <td><label class=\"lbl\">3</label></td>\
                                <td><input type=\"checkbox\" name=\"\" value=\"\"/></td>\
                                <td><input type=\"checkbox\" name=\"\" value=\"\"/></td>\
                            </tr>\
                            <tr>\
                                <td><input type=\"radio\" name=\"\" value=\"\"/></td>\
                                <td><label class=\"lbl\">4</label></td>\
                                <td><input type=\"checkbox\" name=\"\" value=\"\"/></td>\
                                <td><input type=\"checkbox\" name=\"\" value=\"\"/></td>\
                            </tr>\
                        </table>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name =\"\" value=\"Save\" id=\"\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\"  id=\"\" value=\"Retry\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Cancel\" style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"\" id=\"\" value=\"Ok\"/ style=\"Display:None\" onClick=\"\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" name = \"host_id\" value=\"\" style=\"Display:None\"/>\
                            <input type = \"hidden\" name = \"device_type\" value=\"\" />\
                        </div>\
                    </form>"

        return form_str

    @staticmethod
    def table_link_port(host_id, selected_device):
        obj_bll = IduGetData()
        port_link_data = obj_bll.common_get_data(
            "IduLinkConfigurationTable", host_id)
        flag = 0
        admin_dic = {0: "Locked", 1: "Unlocked"}
        link_dic = {}
        port_link_str = ""
        port_link_str += "<input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"table_link_port\" tablename=\"linkConfigurationTable\"/>"
        port_link_str += "<div><input type=\"button\" name=\"add_link\" value=\"Add New Link\" class=\"yo-small yo-button\" style=\"margin-left:5px\" onClick=\"portLinkFormEdit('','','','','',0)\"/>"
        port_link_str += " <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                                <th>\
                                    Link Number\
                                </th>\
                                <th>\
                                    Destination IP\
                                </th>\
                                <th>\
                                    Source Link ID\
                                </th>\
                                <th>\
                                    Destination Link ID\
                                </th>\
                                <th>\
                                    E1 Port Number\
                                </th>\
                                <th>\
                                    Time Slot\
                                </th>\
                                <th>\
                                    PayLoad Size\
                                </th>\
                                <th>\
                                    Jitter Buffer(usec)\
                                </th>\
                                <th>\
                                    Clock Recovery\
                                </th>\
                                <th>\
                                    Admin State\
                                </th>\
                                <th style=\"text-align:left;\">\
                                    Action\
                                </th>\
                            "
        if len(port_link_data) > 0:
            for i in range(0, len(port_link_data)):
                j = 0
                pos = ""
                timeslot = port_link_data[i].tsaAssign
                for k in range(0, len(timeslot)):
                    if j == 0:
                        if int(timeslot[k]) == 1:
                            pos += str(k)
                            j = 1
                    else:
                        if int(timeslot[k]) == 1:
                            pos += "," + str(k)
                port_link_str += "<tr>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td><ul class=\"button_group\" style=\"width:60px;\"><li><a class=\"%s\" id=\"admin_state_%s\" name=\"admin_state_%s\" state=\"%s\" bundle_num=\"%s\" onClick=\"idu_admin_state_change(event,this,'%s','%s','%s','iduConfiguration.linkConfigurationTable.adminStatus',1);\">%s</a></li></ul></td>\
                                    <td style=\"text-align: left;\"><img title=\"Edit Link\" class=\"n-reconcile\" src='images/edit16.png' style=\"cursor:pointer\"  onclick=\"portLinkFormEdit(%s,%s,'IduLinkConfigurationTable','idu_linkConfigurationTable_id',%s,'%s')\" />&nbsp;&nbsp;&nbsp;&nbsp;\
                                    <img title=\"Delete Link\" class=\"n-reconcile\" src='images/delete16.png' style=\"cursor:pointer\"  onclick=\"portlinkformdelete(%s,%s,%s)\" /></td>\
                                </tr>" % (port_link_data[i].bundleNumber, port_link_data[i].dstIPAddr,
                                        port_link_data[i].srcBundleID, port_link_data[
                                            i].dstBundleID, port_link_data[
                                                i].portNumber,
                                        pos, port_link_data[i].bundleSize, port_link_data[
                                            i].bufferSize, "Enable" if int(port_link_data[i].clockRecovery) == 1 else "Disable",
                                        "green" if int(port_link_data[i]
                                                       .adminStatus) == 1 else "red",
                                        port_link_data[i].portNumber, port_link_data[
                                            i].portNumber,
                                        1 if int(port_link_data[
                                                 i].adminStatus) == 1 else 0,
                                        port_link_data[i].bundleNumber,
                                        host_id, port_link_data[i].idu_linkConfigurationTable_id, port_link_data[
                                            i].portNumber, "Unlocked" if int(port_link_data[i].adminStatus) == 1 else "Locked", port_link_data[i].portNumber, port_link_data[i].bundleNumber, port_link_data[i].idu_linkConfigurationTable_id, 1, port_link_data[i].idu_linkConfigurationTable_id, port_link_data[i].portNumber, port_link_data[i].bundleNumber)
        else:
            port_link_str += "<tr>\
                                <td colspan=\"11\">No Data Available</td>\
                            </tr>"
        port_link_str += "</table></div>"
        return port_link_str

    @staticmethod
    def port_link_form(port_link_list, host_id, selected_device, port_link_id, port_num, link_num, addEdit):
        form_str = ""
        form_str += "<form id=\"link_form\" name=\"link_form\" method=\"get\" action=\"link_form_action.py\" style=\"overflow:hidden;\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Link Number</label>\
                            <input type=\"text\" id=\"bundle_id\" name=\"bundle_id\" value=\"%s\" maxsize=\"15\" %s/>\
                            &nbsp;<span style=\"font-size:9px\">0 to 63</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Destination IP Address</label>\
                            <input type=\"text\" id=\"iduConfiguration.linkConfigurationTable.dstIPAddr\" name=\"iduConfiguration.linkConfigurationTable.dstIPAddr\" value=\"%s\" maxsize=\"15\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Source Link ID</label>\
                            <input type=\"text\" id=\"iduConfiguration.linkConfigurationTable.srcBundleID\" name=\"iduConfiguration.linkConfigurationTable.srcBundleID\" value=\"%s\" maxsize=\"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">0 to 63</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Destination Link ID</label>\
                            <input type=\"text\" id=\"iduConfiguration.linkConfigurationTable.dstBundleID\" name=\"iduConfiguration.linkConfigurationTable.dstBundleID\" value=\"%s\" maxsize=\"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">0 to 63</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">E1 Port Number</label>\
                            <select id=\"port_number\" class=\"multiselect\" multiple=\"multiple\" name=\"port_number\" style=\"height:20px\" %s>\
                                %s\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Time Slot</label>\
                            <select id=\"iduConfiguration_linkConfigurationTable_tsaAssign\" class=\"multiselect\"  multiple=\"multiple\" name=\"iduConfiguration_linkConfigurationTable_tsaAssign\" style=\"height:20px\" %s>\
                                %s\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Payload Size</label>\
                            <input type=\"text\" id=\"iduConfiguration.linkConfigurationTable.bundleSize\" name=\"iduConfiguration.linkConfigurationTable.bundleSize\" value=\"%s\" maxsize=\"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">1 to 99</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Jitter Buffer(usec)</label>\
                            <input type=\"text\" id=\"iduConfiguration.linkConfigurationTable.bufferSize\" name=\"iduConfiguration.linkConfigurationTable.bufferSize\" value=\"%s\" maxsize=\"15\"/>\
                            &nbsp;<span style=\"font-size:9px\">1000 to 25000</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Clock Recovery</label>\
                            <select id=\"iduConfiguration_linkConfigurationTable_clockRecovery\" class=\"multiselect\"  multiple=\"multiple\" name=\"iduConfiguration_linkConfigurationTable_clockRecovery\" style=\"height:20px\">\
                                %s\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">VLAN</label>\
                            <select id=\"vlan\" class=\"multiselect\"  multiple=\"multiple\" name=\"vlan\" style=\"height:20px\" disabled=\"disabled\">\
                                %s\
                            </select>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">VLAN Tag</label>\
                            <input type=\"text\" id=\"vlan_tag\" name=\"vlan_tag\" value=\"\" maxsize=\"15\" disabled=\"disabled\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">VLAN Priority</label>\
                            <input type=\"text\" id=\"vlan_priority\" name=\"vlan_priority\" value=\"\" maxsize=\"15\" disabled=\"disabled\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('link_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('link_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('link_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('link_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"addEdit\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"e1_port_num\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"link_number\" value=\"%s\"/>\
                        </div>\
                    </form>" % (link_num if int(addEdit) == 1 else "", "disabled=disabled" if int(addEdit) == 1 else "",
                              port_link_list[
                                  0].dstIPAddr if int(addEdit) == 1 else "",
                              port_link_list[0].srcBundleID if int(
                                  addEdit) == 1 else "", port_link_list[0].dstBundleID if int(addEdit) == 1 else "",
                              "disabled=disabled" if int(
                                  addEdit) == 1 else "", IduForms.select_e1_port(port_num if int(addEdit) == 1 else ""),
                              "disabled=disabled" if int(addEdit) == 1 else "", IduForms.select_timeslot(
                                  port_link_list[0].tsaAssign if int(
                                      addEdit) == 1 else ""),
                              port_link_list[
                                  0].bundleSize if int(addEdit) == 1 else "",
                              port_link_list[
                                  0].bufferSize if int(
                                      addEdit) == 1 else "", IduForms.select_disable_enable_list(port_link_list[0].clockRecovery if int(addEdit) == 1 else ""),
                              IduForms.select_disable_enable_list(""),
                              host_id, selected_device, addEdit, port_num, link_num)

        return form_str

    @staticmethod
    def UNMP_ip_configuration(host_id, selected_device):
        obj_bll = IduGetData()
        omc_data = obj_bll.common_get_data("IduOmcConfigurationTable", host_id)
        form_str = ""
        form_str = "<form id=\"unmp_ip_form\" name = \"unmp_ip_form\" action=\"unmp_ip_action.py\" method =\"get\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">UNMP IP **</label>\
                            <input type=\"text\" id=\"iduConfiguration.omcConfigurationTable.omcIpAddress\" name=\"iduConfiguration.omcConfigurationTable.omcIpAddress\" value=\"%s\" maxsize=\"15\"/>\
                        </div>\
                        <div class=\"row-elem\" style=\"width: 600px;\">\
                            <input type=\"submit\" name=\"common_submit\" value=\"Save\" id=\"submit_save\" onClick=\"return commonFormSubmit('unmp_ip_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\"  id=\"submit_retry\" value=\"Retry\" style=\"Display:None\" onClick=\"return commonFormSubmit('unmp_ip_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return commonFormSubmit('unmp_ip_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"submit\" name=\"common_submit\" id=\"submit_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return commonFormSubmit('unmp_ip_form',this)\" class=\"yo-small yo-button\" />\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\"/><br/><br/>\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"UNMP_ip_configuration\" tablename=\"omcConfigurationTable\"/>\
                            <span  style=\"font-size: 11px;\">**UNMP IP - Configuring UNMP IP is important for capturing and monitoring the device alarms</span>\
                        </div>\
                    </form>" % (omc_data[0].omcIpAddress if len(omc_data) > 0 else "", host_id, selected_device)
        return form_str
################################ END PORT CONFIGURATION ENDS #############


class IduProfiling(object):

    @staticmethod
    def idu_listing():
        table_view = "<div>"
        table_view += "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"device_data_table\" style=\"text-align:center\">\
                    <thead>\
                        <tr>\
                            <th>Device Status</th>\
                            <th>Host Alias</th>\
                            <th>Host Group</th>\
                            <th>IP Address</th>\
                            <th>Mac (eth)</th>\
                            <th>TDMoIP MAC Address</th>\
                            <th>Device Type</th>\
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
    def page_tip_idu_listing():
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
                "<h1>IDU Listing</h1>"\
                "<div><strong>IDU Listing</strong> has shown all IDU Type Devices.On This Page You Can see Various Options</div>"\
                "<br/>"\
                "<div>On this page you can Edit Configuration, Update Firmware,See Graph and Events for Monitoring of Devices and also make Reconciliation of Devices.</div>"\
                "<br/>"\
                "<div><strong>Actions</strong></div>"\
                "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/edit.png\"/></div><div class=\"txt-div\">Edit Configuration</div></div>"\
                "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/graph.png\"/></div><div class=\"txt-div\">Device Monitoring</div></div>"\
                "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/alert.png\"/></div><div class=\"txt-div\">Device Events</div></div>"\
                "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/update.png\"/></div><div class=\"txt-div\">Firmware Upgrade</div></div>"\
                "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-green.png\"/></div><div class=\"txt-div\">Reconciliation done between 91% and 100%</div></div>"\
                "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-black.png\"/></div><div class=\"txt-div\">Reconciliation done in between 36% and less than 90%</div></div>"\
                "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-red.png\"/></div><div class=\"txt-div\">Reconciliation done in between 0% and 35%</div></div>"\
                "<br/>"\
                "<div><strong>Note:</strong>After Reconciliation The Reconciliation Image changes according to Reconciliation Percentage.\
            The Reconiliation Images turns Red when Reconciliation done Between 0 to 35%\
            The Reconiliation Images turns Black when Reconciliation done Between 36% to less than 90%\
            The Reconiliation Images turns Green when Reconciliation Percentage Greater Than and Equal To 90%\
            </div>"\
                "</div>"
            return (str(html_view))
        except Exception, e:
            return str(e)

    @staticmethod
    def page_tip_idu_profiling():
        """
        @param h : html Class Object
        @var html : this is html Class Object defined globally
        @var html_view : this is used to store the html content which is write on page
        @since : 12 December 2011
        @version :0.0
        @date : 12 December 2011
        @note : This function is used for diplaying the help of odu Profiling page.Every link help.Every Tab Help.What output display.Every Image description.How Forms works
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>IDU Profiling</h1>"\
            "<div><strong>IDU</strong> Profiling of (Device). You can edit the profiling of individual device.</div>"\
            "<br/>"\
            "<div><strong><u>Serach Profile</u></strong>At the top there is Ip Address,MAC Address,and Device Type.By All Of that you can select an individual profile.If more than one device is come in search result then you can move to UBR Listing page</div>"\
            "<br/>"\
            "<div><strong><u>E1 and Link Configruation</u></strong> On this tab you can manage the E1 Port and Link Configuration form individaully</div>"\
            "<br/>"\
            "<div><strong><u>E1 Port Configuration</u></strong> On this tab you can manage the E1 Ports and its functionality</div>"\
            "<br/>"\
            "<div><strong><u>Link Configuration</u></strong> On this tab You can manage the Link on particulat port and also add and edit or delete the link</div>"\
            "<br/>"\
            "<div><strong><u>Advance Configuration</u></strong> On this tab You can manage the Temperarure ,Date and Time and UNMP Form</div>"\
            "<br/>"\
            "<div><strong><u>Temperature</u></strong> On this tab you can manage the Lower and Higher Threshold</div>"\
            "<br/>"\
            "<div><strong><u>Date and Time</u></strong> On this tab you can manage time linke hour,minute,second etc</div>"\
            "<br/>"\
            "<div><strong><u>UNMP</u></strong> On this tab you should add the UNMP IP address for receiving traps through UNMP</div>"\
            "<br/>"\
            "<div><strong><u>Switch Configuration</u></strong>On this tab you can manage the Port ,Port Bandwidth,Port QinQ,Port Mirroring,Port VLAN forms configuration</div>"\
            "<br/>"\
            "<div><strong><u>Port Configuration</u></strong> On this tab you can manage the Port Details like Port Link Mode ,Port VID,Port Auth state etc</div>"\
            "<br/>"\
            "<div><strong><u>Port BandWidth Control</u></strong>On this tab you can manage the Port Ingress and Egress fields</div>"\
            "<br/>"\
            "<div><strong><u>Port QinQ</u></strong>On this tab you can manage the QinQ State and Proovider Tag</div>"\
            "<br/>"\
            "<div><strong><u>Port Mirroring</u></strong>On this tab you can manage the Mirroring Port</div>"\
            "<br/>"\
            "<div><strong><u>Port VLAN</u></strong>On this tab you can manage the VLAN Ports and also add and delete the VLAN</div>"\
            "<br/>"\
            "<div><strong><u>Admin States</u></strong> At the bottom left hand there are five admin states i.e. Four E1 Port Admin States and One Idu System Admin State.When Admin States locked color of the admin states are red but when they unlocked color are to green\
        </div>"\
            "<div><strong><u>Commit To Flash</u></strong> This is a button on the bottom of Page.It save all your page data on device permanently</div>"\
            "<br/>"\
            "<div><strong><u>Reconciliation</u></strong> This is a button on the bottom of Page.It save all device data on data storage and show on your page</div>"\
            "<br/>"\
            "<div><strong><u>Reboot</u></strong> This is a button on the bottom of Page.It Reboots the devive.When you press reboot there is a loading spin on you page and it stops spinning when device is reachable again after reboot.If device is not reachable after 100 sec then loading  automatically hides and show you the message</div>"\
            "<br/>"\
            "<div><strong><u>Form Working Description</u></strong> After Click On Save Button Of form.All The values given in form are going to set on the device.If All Values are set then \
        there is a <img src=\"images/done.png\"/> image is display after every Field.And OK button is display instead of save.After click on ok.the form is display with updated values.\
        If values are not set then the <img src=\"images/alert_restart.png\"/> image is display after fields which are not set.if No one field are set then it display after Every field on form .\
        By clicking on retry image after fields ,the value of that field is again going to retry.When retry image is displayed then there are two buttons are also\
        displayed Retry and Cancel button.When Click on retry button all fields are again going to set in which retry image is diplayed.On click on cancel button \
        the form is displayed with the updated values which are set and the retry values are discarded and the old values are displayed in that fileds\
        </div>"\
            "<br/>"\
            "</div>"
        return html_view

    @staticmethod
    def idu_profiling_form(host_id, selected_device, device_list_parameter):
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
        if device_list_parameter == "" or device_list_parameter == []:
            return "No Configuration Profile Exist"
        elif device_list_parameter[0].config_profile_id == None or device_list_parameter[0].config_profile_id == "":
            return "No Configuration Exist.Please Add Host Again"
        else:
            tab_str = ''
            tab_str += "<div class=\"yo-tabs\" id=\"config_tabs\" style=\"display:block\">\
                            <ul>\
                                <li><a  href=\"#content_1\">E1 and Link Configuration</a></li>\
                                <li><a href=\"#content_2\">Advanced Configuration</a></li>\
                                <li><a href=\"#content_3\">Switch Configuration</a></li>\
                                <li style=\"display:none;\"><a href=\"#content_4\">System Diagonistics</a></li>\
                                \
                                \
                            </ul>\
                            <div id=\"content_1\" class=\"tab-content\" style=\"display:block ;position: relative;margin-bottom:0px\" class=\"form-div\">\
                                <div class=\"yo-tabs\" style=\"margin:10px 0\">\
                                    <ul>\
                                        \
                                        <li><a href=\"#content1_2\">E1 Port Configuration</a></li>\
                                        <li><a href=\"#content1_3\">Link Configuration</a></li>\
                                        <li style=\"display:none\"><a class=\"active\" href=\"#content1_1\">Network</a></li>\
                                    </ul>\
                                    <div id=\"content1_1\" class=\"tab-content\">\
                                        <div>\
                                        \
                                        </div>\
                                    </div>\
                                    <div id=\"content1_2\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content1_3\" class=\"tab-content\">\
                                        <div>\
                                        \
                                        </div>\
                                        <div id=\"content1_3_1\">\
                                        %s\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                            <div id=\"content_2\" class=\"tab-content\" style=\"display:none;\">\
                                <div class=\"yo-tabs\" style=\"margin:10px 0\">\
                                    <ul>\
                                        <!--<li><a class=\"active\" href=\"#content2_1\">POE</a></li>-->\
                                        \
                                        <li><a href=\"#content2_4\">Temperature</a></li>\
                                        <li><a href=\"#content2_5\">Date and Time</a></li>\
                                        <li><a href=\"#content2_7\">UNMP</a></li>\
                                        <li style=\"display:none;><a href=\"#content2_6\">Alarm Port</a></li>\
                                        <li style=\"display:none;><a href=\"#content2_2\">Header Type</a></li>\
                                        <li style=\"display:none;><a href=\"#content2_3\">Clock</a></li>\
                                    </ul>\
                                    <div id=\"content2_1\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content2_2\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content2_3\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content2_4\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content2_5\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content2_6\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content2_7\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                            <div id=\"content_3\" class=\"tab-content\" style=\"display:none;\">\
                                <div class=\"yo-tabs\" style=\"margin:10px 0\">\
                                    <ul>\
                                        <li><a class=\"active\" href=\"#content3_1\">Port Configuration</a></li>\
                                        <li><a href=\"#content3_2\">Port Bandwidth Control</a></li>\
                                        <li><a href=\"#content3_3\">Port QinQ</a></li>\
                                        <li><a href=\"#content3_4\">Mirroring Port</a></li>\
                                        <li><a href=\"#content3_7\">Port VLAN</a></li>\
                                        <li style=\"display:none;><a href=\"#content3_5\">Port ACL</a></li>\
                                        <li style=\"display:none;><a href=\"#content3_6\">Port ATU</a></li>\
                                        \
                                        \
                                    </ul>\
                                    <div id=\"content3_1\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content3_2\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content3_3\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content3_4\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content3_5\" class=\"tab-content\">\
                                        <div>\
                                        \
                                        </div>\
                                    </div>\
                                    <div id=\"content3_6\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                    <div id=\"content3_7\" class=\"tab-content\">\
                                        <div>\
                                        %s\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                            <div id=\"content_4\" class=\"tab-content\" style=\"display:none;\">\
                                <div class=\"yo-tabs\" style=\"margin:10px 0\">\
                                    <ul>\
                                        <li><a class=\"active\" href=\"#content4_1\">E1 Port LoopBack</a></li>\
                                    </ul>\
                                </div>\
                                <div id=\"content4_1\" class=\"tab-content\">\
                                    <div>\
                                    %s\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                        <input type=\"hidden\" name=\"host_id\" id=\"host_id\" value=\"%s\"/>\
                        <input type=\"hidden\" name=\"ip_address\" value=\"%s\"/>\
                        <input type=\"hidden\" name=\"mac_address\" value=\"%s\"/>\
                        <input type=\"hidden\" name=\"device_type_id\" id=\"device_type_id\" value=\"%s\"/>" % (IduForms.table_e1_port(host_id, selected_device),
                                                                                                              IduForms.table_link_port(
                                                                                                                  host_id, selected_device),
                                                                                                              IduForms.POE(
                                                                                                                  host_id, selected_device), IduForms.header_type(),
                                                                                                              IduForms.clock(
                                                                                                                  ), IduForms.temperature(host_id, selected_device), IduForms.datetime(host_id, selected_device),
                                                                                                              IduForms.alarm_port_show_table(), IduForms.UNMP_ip_configuration(host_id, selected_device),
                                                                                                              IduForms.port_configuration_show_table(host_id, selected_device), IduForms.port_bandwidth_show_table(host_id, selected_device),
                                                                                                              IduForms.port_QinQ_show_table(
                                                                                                                  host_id, selected_device),
                                                                                                              #"",
                                                                                                              IduForms.port_mirroring(
                                                                                                                  host_id, selected_device), IduForms.port_ATU_show_table(), IduForms.table_port_Vlan(host_id, selected_device),
                                                                                                              IduForms.e1_port_loopback(),
                                                                                                              host_id, device_list_parameter[0].ip_address, device_list_parameter[0].mac_address, selected_device)
            return tab_str

    @staticmethod
    def idu_div(ip_address, mac_address, host_id):
        obj_get_data = IduGetData()
        html_str = ""
        op_data = []
        html_str += "<ul class=\"button_group\" style=\"margin:10px 0 0 10px !important;\">"
        e1_op_data = obj_get_data.get_e1_op_status(host_id)
        if len(e1_op_data) > 0:
            op_data = []
        else:
            op_data = [1, 1, 1, 1]
        e1_port_list = obj_get_data.common_get_data(
            'IduE1PortConfigurationTable', host_id)
        main_admin_state_list = obj_get_data.common_get_data(
            'IduIduAdminStateTable', host_id)
        if len(main_admin_state_list) > 0:
            if int(main_admin_state_list[0].adminstate) == 1:
                main_admin_image_class = "green"
                main_admin_html = "IDU Admin Unlocked"
            else:
                main_admin_image_class = "red"
                main_admin_html = "IDU Admin Locked"
        else:
            main_admin_image_path = "images/temp/red_dot.png"

        for k in range(0, len(e1_op_data)):
            op_data.append(e1_op_data[k].opStatus)

        for j in range(0, len(e1_port_list)):
            html_str += "<li><a class=\"%s\" id=\"e1_admin_state_%s\" name=\"admin_state_%s\" state=\"%s\" \
            onClick=\"idu_admin_state_change(event,this,'%s','%s','%s','iduConfiguration.e1PortConfigurationTable.adminState',0);\">%s</a></li>"\
                % (
                    "green" if int(e1_port_list[j].adminState) == 1 and int(op_data[j]) == 1 else "red" if int(
                        e1_port_list[j].adminState) == 1 and int(
                            op_data[j]) == 0 else "red",
                  e1_port_list[j].portNumber, e1_port_list[j].portNumber,
                  1 if int(e1_port_list[j].adminState) == 1 else 0,
                  host_id, e1_port_list[j].idu_e1PortConfigurationTable_id, e1_port_list[j].portNumber, "E1 Port%s Unlocked" % (e1_port_list[j].portNumber) if int(e1_port_list[j].adminState) == 1 else "E1 Port%s Locked" % (e1_port_list[j].portNumber))
        html_str += '<li><a class=\"%s\" onclick=\"main_admin_state_change(event,this,\'%s\',\'iduinfo.iduAdminStateTable.adminstate\'); \" />%s</a></li>'\
            % (main_admin_image_class, host_id, main_admin_html)
        html_str += "<ul>"
        profile_str = ""
        profile_str += "<div id=\"idu_form_div\" class=\"form-div\" style=\"margin-top: 56px;\"></div>"
        profile_str += "<div class=\"form-div-footer\">\
                            <div id=\"admin_div\" style=\"float: left;margin-left:15px\">\
                                %s\
                            </div>\
                            <div style=\"float:right;margin-right:10px\">\
                                <input type=\"button\" id=\"idu4_commit\" name=\"idu4_commit\" value=\"Commit To Flash\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"idu4_reboot\" name=\"idu4_reboot\" value=\"Reboot\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" id=\"idu4_reconcile\" name=\"idu4_reconcile\" value=\"Reconciliation\"  class=\"yo-small yo-button\"/>\
                                <input type=\"hidden\" name=\"ip_address\" value=\"%s\"/>\
                                <input type=\"hidden\" name=\"mac_address\" value=\"%s\" />\
                                <input type=\"hidden\" name=\"host_id\" value=\"%s\" />\
                                <!-- <input type=\"button\" id=\"idu4_adminState\" name=\"idu4_adminState\" value=\"System Admin State\"  class=\"yo-small yo-button\"/> -->\
                            </div>\
                        </div>" % (html_str, ip_address, mac_address, host_id)
        return profile_str

    @staticmethod
    def idu_profile_call(host_id, device_type, device_list_parameter):
        tab_str = ""
        if host_id == "" or host_id == "None":
            tab_str += "There is No Host Exist</div>"
        else:
            if device_type == UNMPDeviceType.idu4:
                tab_str += IduProfiling.idu_profiling_form(
                    host_id, device_type, device_list_parameter)  # function call , it is used to make a form of selected profiling
        return tab_str
