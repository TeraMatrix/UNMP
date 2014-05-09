#!/usr/bin/python2.6

"""
@author: Yogesh Kumar
@since: 23-Oct-2011
@version: 0.1
@note: All Views Related with Inventory.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""
# flag for nagios
# if set to 1 means show advanced options for nagios
# if set to 0 means don't show advanced options
flag_nagios_call = 0


class Host(object):
    """
    Inventory Device related class
    """
    @staticmethod
    def header_buttons():
        """


        @return:
        """
        add_btn = "<div class=\"header-icon\"><img onclick=\"addHost();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Host\"></div>" % theme
        edit_btn = "<div class=\"header-icon\"><img onclick=\"editHost();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit Host Details\"></div>" % theme
        del_btn = "<div class=\"header-icon\"><img onclick=\"delHost();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Host\"></div>" % theme
        header_btn = del_btn + add_btn
        return header_btn

    @staticmethod
    def manage_host():
        """


        @return:
        """
        html_view = "" \
                    "<div id=\"grid_view_div\">" \
                    "<div class=\"yo-tabs\">" \
                    "<ul>" \
                    "<li>" \
                    "<a class=\"active\" href=\"#content_1\" id=\"active_host_tab\">Active Host</a>" \
                    "</li>" \
                    "<li>" \
                    "<a href=\"#content_2\" id=\"disable_host_tab\">Disabled Host</a>" \
                    "</li>" \
                    "<li>" \
                    "<a href=\"#content_3\" id=\"discovered_host_tab\">Discovered Host</a>" \
                    "</li>" \
                    "<li>" \
                    "<a href=\"#content_4\" id=\"deleted_host_tab\">Deleted Host</a>" \
                    "</li>" \
                    "</ul>" \
                    "<div id=\"content_1\" class=\"tab-content\" style=\"display:block;height:100%;\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_active_host\" style=\"text-align:center;display:none;\">\
                            <thead><tr><th></th><th></th>\
                            <th>Host Alias</th>\
                            <th>IP Address</th>\
                            <th>Device Type</th>\
                            <th>Hostgroup</th>\
                            <th>MAC Address</th>\
                            <th>Parent</th>\
                            <th>Priority</th>\
                            <th>Actions</th></tr></thead>\
                            </table>" \
                    "</div>" \
                    "<div id=\"content_2\" class=\"tab-content\" style=\"display:none;height:100%;\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_disable_host\" style=\"text-align:center;display:none;\">\
                            <thead><tr><th></th><th></th>\
                            <th>Host Alias</th>\
                            <th>IP Address</th>\
                            <th>Device Type</th>\
                            <th>Hostgroup</th>\
                            <th>MAC Address</th>\
                            <th>Parent</th>\
                            <th>Priority</th>\
                            <th>Actions</th></tr></thead>\
                            </table>" \
                    "</div>" \
                    "<div id=\"content_3\" class=\"tab-content\" style=\"display:none;height:100%;\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_discovered_host\" style=\"text-align:center;display:none;\">\
                            <thead><tr><th></th><th>Discovery Type</th>\
                            <th>IP Address</th>\
                            <th>MAC Address</th>\
                            <th>Device Type</th>\
                            <th>Discovered Date & Time</th>\
                            </tr></thead>\
                            </table>" \
                    "</div>" \
                    "<div id=\"content_4\" class=\"tab-content\" style=\"display:none;height:100%;\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_deleted_host\" style=\"text-align:center;display:none;\">\
                            <thead><tr><th></th><th></th>\
                            <th>Host Alias</th>\
                            <th>IP Address</th>\
                            <th>Device Type</th>\
                            <th>Hostgroup</th>\
                            <th>MAC Address</th>\
                             <th>Parent</th>\
                            <th>Priority</th>\
                            <th>Deleted by</th>\
                            <th>Deleted Date & Time</th>\
                            </tr></thead>\
                            </table>" \
                    "</div>" \
                    "</div>" \
                    "</div>" \
                    "<div id=\"form_div\" style=\"display:none;\"></div>"
        return html_view

    @staticmethod
    def create_form(device_type_select_list, host_state_select_list, host_priority_select_list, host_vendor_select_list,
                    host_os_select_list, host_parent_select_list, dns_state_select_list, snmp_version_select_list,
                    host_hostgroups_select_list, master_select_list):
        """

        @param device_type_select_list:
        @param host_state_select_list:
        @param host_priority_select_list:
        @param host_vendor_select_list:
        @param host_os_select_list:
        @param host_parent_select_list:
        @param dns_state_select_list:
        @param snmp_version_select_list:
        @param host_hostgroups_select_list:
        @param master_select_list:
        @return:
        """
        html_view = "" \
                    "<form action=\"#\" id=\"form_host\" method=\"get\"> " \
                    "<div class=\"form-div\">" \
                    "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                    "<tr>" \
                    "<th id=\"form_title\" class=\"cell-title\">Add New Host</th>" \
                    "</tr>" \
                    "</table>" \
                    "<div class=\"row-elem\" style=\"display:none;\">" \
                    "<label class=\"lbl lbl-big\" for=\"host_name\">Host Name</label>" \
                    "<input type=\"text\" value=\"host\" id=\"host_name\" name=\"host_name\" readonly=\"readonly\" title=\"Auto generated host name\" /> " \
                    "<input type=\"hidden\" id=\"host_id\" name=\"host_id\" /> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"host_alias\">Host Alias</label>" \
                    "<input type=\"text\" id=\"host_alias\" name=\"host_alias\" title=\"Enter a name to identify the host.\" /> " \
                    "<label for=\"host_alias\" generated=\"true\" class=\"error\"></label>" \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"ip_address\">IP Address</label>" \
                    "<input type=\"text\" id=\"ip_address\" name=\"ip_address\" title=\"Enter IP Address. e.g. 192.168.1.10\" /> " \
                    "<label for=\"ip_address\" generated=\"true\" class=\"error\"></label>" \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"device_type\">Device Type</label>" \
                    "" + device_type_select_list + "" \
                                                   "</div>" \
                                                   "<div class=\"row-elem odu100-only\" id=\"firmware_version_div\" style=\"display:none;\">" \
                                                   "<label class=\"lbl lbl-big\" for=\"firmware_version\">Firmware Version</label>" \
                                                   "<select id=\"firmware_version\" name=\"firmware_version\"></select>" \
                                                   "<img src=\"images/loading-small.gif\" alt=\"fetching...\" id=\"firmware_loading\" style=\"display:none;vertical-align:middle;margin-left:10px;\"/> " \
                                                   "<a id=\"a_firmware_version\"  href=\"javascript:getFirmwareVersion('odu100');\" style=\"margin:10px;\">Fetch</a>" \
                                                   "<label for=\"firmware_version\" generated=\"true\" class=\"error\"></label>" \
                                                   "</div>" \
                                                   "<div class=\"row-elem\">" \
                                                   "<label class=\"lbl lbl-big\" for=\"mac_address\">MAC Address</label>" \
                                                   "<input type=\"text\" id=\"mac_address\" name=\"mac_address\" title=\"Enter the host MAC Address or Hardware Address.\" /> " \
                                                   "<img src=\"images/loading-small.gif\" alt=\"fetching...\" id=\"mac_loading\" style=\"display:none;vertical-align:middle;margin-left:10px;\"/>" \
                                                   "<a id=\"a_fetch_mac\"  href=\"javascript:fetchMacAddress();\" style=\"margin:10px;\">Fetch</a>" \
                                                   "<label for=\"mac_address\" generated=\"true\" class=\"error\"></label>" \
                                                   "</div>" \
                                                   "<div class=\"row-elem\" id=\"radio_mac_div\" style=\"display:none;\">" \
                                                   "<label class=\"lbl lbl-big\" for=\"radio_mac_address\">Radio MAC Address</label>" \
                                                   "<input type=\"text\" id=\"radio_mac_address\" name=\"radio_mac_address\" title=\"Enter the Wifi MAC Address for Access Point.\" /> " \
                                                   "<img src=\"images/loading-small.gif\" alt=\"fetching...\" id=\"radio_mac_loading\" style=\"display:none;vertical-align:middle;margin-left:10px;\"/>" \
                                                   "<a id=\"a_fetch_radio_mac\"  href=\"javascript:fetchMacAddress();\" style=\"margin:10px;\">Fetch</a>" \
                                                   "<label for=\"radio_mac_address\" generated=\"true\" class=\"error\"></label>" \
                                                   "</div>" \
                                                   "<div class=\"row-elem\" id=\"ra_mac_div\" style=\"display:none;\">" \
                                                   "<label class=\"lbl lbl-big\" for=\"ra_mac\">RA MAC Address</label>" \
                                                   "<input type=\"text\" id=\"ra_mac\" name=\"ra_mac\" title=\"Enter or Fetch Host Radio Access MAC Address.\"/>" \
                                                   "<img src=\"images/loading-small.gif\" alt=\"fetching...\" id=\"ra_mac_loading\" style=\"display:none;vertical-align:middle;margin-left:10px;\"/>" \
                                                   "<a id=\"a_fetch_ra_mac\"  href=\"javascript:fetchRAMacAddress();\" style=\"margin:10px;\">Fetch</a>" \
                                                   "</div>" \
                                                   "<div class=\"row-elem\" id=\"node_type_div\" style=\"display:none;\">" \
                                                   "<label class=\"lbl lbl-big\" for=\"ra_mac\">Node Type</label>" \
                                                   "<select id=\"node_type\" name=\"node_type\" title=\"Choose node type\" >" \
                                                   "<option value=\"0\">rootRU</option>" \
                                                   "<option value=\"1\">t1TDN</option>" \
                                                   "<option value=\"2\">t2TDN</option>" \
                                                   "<option value=\"3\">t2TEN</option>" \
                                                   "</select>" \
                                                   "</div>" \
                                                   "<div class=\"row-elem\" id=\"master_slave_div\" style=\"display:none;\">" \
                                                   "<label class=\"lbl lbl-big\" for=\"master_mac\">Master MAC Address</label>" \
                                                   "" + master_select_list + "" \
                                                                             "<img src=\"images/loading-small.gif\" alt=\"fetching...\" id=\"master_mac_loading\" style=\"display:none;vertical-align:middle;margin-left:10px;\"/>" \
                                                                             "<a id=\"a_fetch_master_mac\" href=\"javascript:fetchMasterMacAddress();\" style=\"margin:10px;\">Fetch</a>" \
                                                                             "</div>" \
                                                                             "<div class=\"row-elem\">" \
                                                                             "<label class=\"lbl lbl-big\" for=\"host_state\">Host State</label>" \
                                                                             "" + host_state_select_list + "" \
                                                                                                           "</div>" \
                                                                                                           "<div class=\"row-elem\">" \
                                                                                                           "<label class=\"lbl lbl-big\" for=\"host_priority\">Priority</label>" \
                                                                                                           "" + host_priority_select_list + "" \
                                                                                                                                            "</div>" \
                                                                                                                                            "<div class=\"row-elem\">" \
                                                                                                                                            "<label class=\"lbl lbl-big\" for=\"host_parent\">Host Parent</label>" \
                                                                                                                                            "" + host_parent_select_list + "" \
                                                                                                                                                                           "</div>" \
                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"hostgroup\">Hostgroup</label>" \
                                                                                                                                                                           "" + host_hostgroups_select_list + "" \
                                                                                                                                                                                                              "</div>" \
                                                                                                                                                                                                              "<div class=\"row-elem\">" \
                                                                                                                                                                                                              "<label class=\"lbl lbl-big\" for=\"is_reconciliation\">Reconciliation</label>" \
                                                                                                                                                                                                              "<input type=\"checkbox\" id=\"is_reconciliation\" name=\"is_reconciliation\" title=\"Check if you want to fetch data from device\" />" \
                                                                                                                                                                                                              "</div>" \
                                                                                                                                                                                                              "<div class=\"row-elem\">" \
                                                                                                                                                                                                              "<label class=\"lbl lbl-big\" for=\"host_comment\">Comment</label>" \
                                                                                                                                                                                                              "<textarea id=\"host_comment\" name=\"host_comment\" title=\"Enter Host Comment\"></textarea>" \
                                                                                                                                                                                                              "</div>" \
                                                                                                                                                                                                              "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                                                                                                                                                                                                              "<tr>" \
                                                                                                                                                                                                              "<th id=\"network_details\" class=\"cell-title\">Network Details</th>" \
                                                                                                                                                                                                              "</tr>" \
                                                                                                                                                                                                              "</table>" \
                                                                                                                                                                                                              "<div class=\"row-elem\">" \
                                                                                                                                                                                                              "<label class=\"lbl lbl-big\" for=\"netmask\">Netmask</label>" \
                                                                                                                                                                                                              "<input type=\"text\" id=\"netmask\" name=\"netmask\" title=\"Enter Netmask\" /> " \
                                                                                                                                                                                                              "<img src=\"images/loading-small.gif\" alt=\"fetching...\" id=\"network_details_loading\" style=\"display:none;vertical-align:middle;margin-left:10px;\"/>" \
                                                                                                                                                                                                              "<a id=\"a_network_details_loading\"  href=\"javascript:fetchNetworkDetails();\" style=\"margin:10px;\">Fetch</a>" \
                                                                                                                                                                                                              "</div>" \
                                                                                                                                                                                                              "<div class=\"row-elem\">" \
                                                                                                                                                                                                              "<label class=\"lbl lbl-big\" for=\"gateway\">Gateway</label>" \
                                                                                                                                                                                                              "<input type=\"text\" id=\"gateway\" name=\"gateway\" title=\"Enter Gateway Address\" /> " \
                                                                                                                                                                                                              "</div>" \
                                                                                                                                                                                                              "<div class=\"row-elem\">" \
                                                                                                                                                                                                              "<label class=\"lbl lbl-big\" for=\"dns_state\">DHCP State</label>" \
                                                                                                                                                                                                              "" + dns_state_select_list + "" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem odu100-only\" style=\"display:none;\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"odu100_management_mode\">Management Mode</label>" \
                                                                                                                                                                                                                                           "<select id=\"odu100_management_mode\" name=\"odu100_management_mode\" title=\"Choose Management Mode\" >" \
                                                                                                                                                                                                                                           "<option value=\"0\">NORMAL(0)</option>" \
                                                                                                                                                                                                                                           "<option value=\"1\">VLAN(1)</option>" \
                                                                                                                                                                                                                                           "</select>" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem odu100-only\" style=\"display:none;\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"odu100_vlan_tag\">VLAN Tag</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"odu100_vlan_tag\" name=\"odu100_vlan_tag\" title=\"Enter VLAN tag\" /> (1-4094)" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem idu4-only\" style=\"display:none;\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"idu4_management_mode\">Management VLAN</label>" \
                                                                                                                                                                                                                                           "<input type=\"checkbox\" id=\"idu4_management_mode\" name=\"idu4_management_mode\" value=\"1\" title=\"Check Management VLAN Mode\" />" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem idu4-only\" style=\"display:none;\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"idu4_vlan_tag\">VLAN Tag</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"idu4_vlan_tag\" name=\"idu4_vlan_tag\" title=\"Enter VLAN tag\" /> (1-4094)" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem idu4-only\" style=\"display:none;\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"idu4_tdm_ip\">TDM IP Address</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"idu4_tdm_ip\" name=\"idu4_tdm_ip\" title=\"Enter TDM IP Address\" />" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem ap25-only\" style=\"display:none;\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"primary_dns\">Primary DNS</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"primary_dns\" name=\"primary_dns\" title=\"Enter Primary DNS\" /> " \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem ap25-only\" style=\"display:none;\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"secondary_dns\">Secondary DNS</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"secondary_dns\" name=\"secondary_dns\" title=\"Enter Secondary DNS\" /> " \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem ccu-only\" style=\"display:none;\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"ccu_dhcp_netmask\">DHCP Netmask</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"ccu_dhcp_netmask\" name=\"ccu_dhcp_netmask\" title=\"Enter DHCP Netmask\" /> " \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                                                                                                                                                                                                                                           "<tr>" \
                                                                                                                                                                                                                                           "<th id=\"http_details\" class=\"cell-title\">HTTP Details</th>" \
                                                                                                                                                                                                                                           "</tr>" \
                                                                                                                                                                                                                                           "</table>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"http_username\">Username</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"http_username\" name=\"http_username\" title=\"Enter HTTP Username\" value=\"\" />" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"http_password\">Password</label>" \
                                                                                                                                                                                                                                           "<input type=\"password\" id=\"http_password\" name=\"http_password\" title=\"Enter HTTP Password\" value=\"\" />" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"http_port\">Port</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"http_port\" name=\"http_port\" title=\"Enter HTTP Port\" value=\"\" /> " \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                                                                                                                                                                                                                                           "<tr>" \
                                                                                                                                                                                                                                           "<th id=\"snmp_details\" class=\"cell-title\">SNMP Details</th>" \
                                                                                                                                                                                                                                           "</tr>" \
                                                                                                                                                                                                                                           "</table>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"read_community\">Read Community</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"read_community\" name=\"read_community\" title=\"Enter SNMP Read Community\" value=\"\" />" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"write_community\">Write Community</label>" \
                                                                                                                                                                                                                                           "<input type=\"text\" id=\"write_community\" name=\"write_community\" title=\"Enter SNMP Write Community\" value=\"\" />" \
                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"snmp_version\">Version</label>" \
                                                                                                                                                                                                                                           "" + snmp_version_select_list + "" \
                                                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"get_set_port\">Get/Set Port</label>" \
                                                                                                                                                                                                                                                                           "<input type=\"text\" id=\"get_set_port\" name=\"get_set_port\" title=\"Enter SNMP Get/Set Port\" value=\"\" /> " \
                                                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"G_port\">Trap Port</label>" \
                                                                                                                                                                                                                                                                           "<input type=\"text\" id=\"trap_port\" name=\"trap_port\" title=\"Enter SNMP Trap Port\" value=\"\" />" \
                                                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                                                           "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                                                                                                                                                                                                                                                                           "<tr>" \
                                                                                                                                                                                                                                                                           "<th id=\"http_details\" class=\"cell-title\">SSH Details</th>" \
                                                                                                                                                                                                                                                                           "</tr>" \
                                                                                                                                                                                                                                                                           "</table>" \
                                                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"ssh_username\">Username</label>" \
                                                                                                                                                                                                                                                                           "<input type=\"text\" id=\"ssh_username\" name=\"ssh_username\" title=\"Enter SSH Username\" value=\"\" />" \
                                                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"ssh_password\">Password</label>" \
                                                                                                                                                                                                                                                                           "<input type=\"password\" id=\"ssh_password\" name=\"ssh_password\" title=\"Enter SSH Password\" value=\"\" />" \
                                                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                                                           "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"ssh_port\">Port</label>" \
                                                                                                                                                                                                                                                                           "<input type=\"text\" id=\"ssh_port\" name=\"ssh_port\" title=\"Enter SSH Port\" value=\"\" /> " \
                                                                                                                                                                                                                                                                           "</div>" \
                                                                                                                                                                                                                                                                           "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                                                                                                                                                                                                                                                                           "<tr>" \
                                                                                                                                                                                                                                                                           "<th id=\"snmp_details\" class=\"cell-title\">Host Asset</th>" \
                                                                                                                                                                                                                                                                           "</tr>" \
                                                                                                                                                                                                                                                                           "</table>" \
                                                                                                                                                                                                                                                                           "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                                                                                                                                                           "<label class=\"lbl lbl-big\" for=\"host_vendor\">Vendor</label>" \
                                                                                                                                                                                                                                                                           "" + host_vendor_select_list + "" \
                                                                                                                                                                                                                                                                                                          "</div>" \
                                                                                                                                                                                                                                                                                                          "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                                                                                                                                                                                          "<label class=\"lbl lbl-big\" for=\"host_os\">Host OS</label>" \
                                                                                                                                                                                                                                                                                                          "" + host_os_select_list + "" \
                                                                                                                                                                                                                                                                                                                                     "</div>" \
                                                                                                                                                                                                                                                                                                                                     "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"longitude\">Longitude</label>" \
                                                                                                                                                                                                                                                                                                                                     "<input type=\"text\" id=\"longitude\" name=\"longitude\" title=\"Enter Host Longitude\" value=\"\" />" \
                                                                                                                                                                                                                                                                                                                                     "</div>" \
                                                                                                                                                                                                                                                                                                                                     "<div class=\"row-elem\">" \
                                                                                                                                                                                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"latitude\">Latitude</label>" \
                                                                                                                                                                                                                                                                                                                                     "<input type=\"text\" id=\"latitude\" name=\"latitude\" title=\"Enter Host Latitude\" value=\"\" />" \
                                                                                                                                                                                                                                                                                                                                     "</div>" \
                                                                                                                                                                                                                                                                                                                                     "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                                                                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"lock_position\">Lock Position</label>" \
                                                                                                                                                                                                                                                                                                                                     "<input type=\"checkbox\" id=\"lock_position\" name=\"lock_position\" title=\"Is Latitude/Logitude Fixed\" value=\"t\" />" \
                                                                                                                                                                                                                                                                                                                                     "</div>" \
                                                                                                                                                                                                                                                                                                                                     "<div class=\"row-elem serial\">" \
                                                                                                                                                                                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"serial_number\">Serial Number</label>" \
                                                                                                                                                                                                                                                                                                                                     "<input type=\"text\" id=\"serial_number\" name=\"serial_number\" title=\"Enter Host Serial Number\" />" \
                                                                                                                                                                                                                                                                                                                                     "</div>" \
                                                                                                                                                                                                                                                                                                                                     "<div class=\"row-elem hardware\">" \
                                                                                                                                                                                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"hardware_version\">Hardware Version</label>" \
                                                                                                                                                                                                                                                                                                                                     "<input type=\"text\" id=\"hardware_version\" name=\"hardware_version\" title=\"Enter Host Hardware Version\"/>" \
                                                                                                                                                                                                                                                                                                                                     "</div>" \
                                                                                                                                                                                                                                                                                                                                     "</div>" \
                                                                                                                                                                                                                                                                                                                                     "<div class=\"form-div-footer\">" \
                                                                                                                                                                                                                                                                                                                                     "<button type=\"submit\" class=\"yo-small yo-button\" id=\"add_host\"><span class=\"add\">Add</span></button>" \
                                                                                                                                                                                                                                                                                                                                     "<button type=\"submit\" class=\"yo-small yo-button\" id=\"edit_host\"><span class=\"edit\">Edit</span></button>" \
                                                                                                                                                                                                                                                                                                                                     "<button type=\"button\" class=\"yo-small yo-button\" id=\"cancel_host\"><span class=\"cancel\">Cancel</span></button>"
        if flag_nagios_call:
            html_view += "<button type=\"button\" class=\"yo-small yo-button\" id=\"advanced_settings\" onclick=\"advance_settings_colorbox();\" ><span class=\"edit\">Advanced Settings</span></button>"
        html_view += "</div" \
                     "</form>"
        return html_view

        # @staticmethod
        # def page_tip_host():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_host.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)


class Hostgroup(object):
    """
    Hostgroup view
    """
    @staticmethod
    def header_buttons():
        """


        @return:
        """
        add_btn = "<div class=\"header-icon\"><img onclick=\"addHostgroup();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Hostgroup\"></div>" % theme
        edit_btn = "<div class=\"header-icon\"><img onclick=\"editHostgroup();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit Hostgroup\"></div>" % theme
        del_btn = "<div class=\"header-icon\"><img onclick=\"delHostgroup();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Hostgroup\"></div>" % theme
        header_btn = del_btn + add_btn
        return header_btn

    @staticmethod
    def manage_hostgroup():
        """


        @return:
        """
        html_view = "" \
                    "<div id=\"grid_view_div\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view\"></table>" \
                    "</div>" \
                    "<div id=\"form_div\" style=\"display:none;\"></div>" \
                    "<div id=\"manage_group_div\" style=\"display:none;\"></div>"
        return html_view

    @staticmethod
    def create_form():
        """


        @return:
        """
        html_view = "" \
                    "<form action=\"#\" id=\"form_hostgroup\" method=\"get\"> " \
                    "<div class=\"form-div\">" \
                    "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                    "<tr>" \
                    "<th id=\"form_title\" class=\"cell-title\">Add New Hostgroup</th>" \
                    "</tr>" \
                    "</table>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"hostgroup_name\">Hostgroup Name</label>" \
                    "<input type=\"text\" id=\"hostgroup_name\" name=\"hostgroup_name\" title=\"Enter Hostgroup Name\" /> " \
                    "<input type=\"hidden\" id=\"hostgroup_id\" name=\"hostgroup_id\" /> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"hostgroup_alias\">Hostgroup Alias</label>" \
                    "<input type=\"text\" id=\"hostgroup_alias\" name=\"hostgroup_alias\" title=\"Enter Hostgroup Alias\" /> " \
                    "</div>" \
                    "</div>" \
                    "<div class=\"form-div-footer\">" \
                    "<button type=\"submit\" class=\"yo-small yo-button\" id=\"add_hostgroup\"><span class=\"add\">Add</span></button>" \
                    "<button type=\"submit\" class=\"yo-small yo-button\" id=\"edit_hostgroup\"><span class=\"edit\">Edit</span></button>" \
                    "<button type=\"button\" class=\"yo-small yo-button\" id=\"cancel_hostgroup\"><span class=\"cancel\">Cancel</span></button>"
        if flag_nagios_call:
            html_view += "<button type=\"button\" class=\"yo-small yo-button\" id=\"advanced_settings\" onclick=\"advance_settings_colorbox();\" ><span class=\"edit\">Advanced Settings</span></button>"
        html_view += "</div" \
                     "</form>"
        return html_view

        # @staticmethod
        # def page_tip_hostgroup():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_hostgroup.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return html_view


class Discovery(object):
    """
    Discovery relate class
    """
    @staticmethod
    def header_buttons():
        """


        @return:
        """
        add_btn = "<div class=\"header-icon\"><img onclick=\"addHost();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Discovered Host\"></div>" % theme
        del_btn = "<div class=\"header-icon\"><img onclick=\"delHost();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Discovered Host\"></div>" % theme
        header_btn = del_btn + add_btn
        return header_btn

    @staticmethod
    def discovery():
        """


        @return:
        """
        html_view = "" \
                    "<div id=\"grid_view_div\">" \
                    "<div class=\"yo-tabs\">" \
                    "<ul>" \
                    "<li>" \
                    "<a class=\"active\" href=\"#content_1\" id=\"discovered_host_tab\">Discovered Host</a>" \
                    "</li>" \
                    "<li>" \
                    "<a href=\"#content_2\" id=\"ping_tab\">PING</a>" \
                    "</li>" \
                    "<li>" \
                    "<a href=\"#content_3\" id=\"snmp_tab\">SNMP</a>" \
                    "</li>" \
                    "<li>" \
                    "<a href=\"#content_4\" id=\"upnp_tab\">UPNP</a>" \
                    "</li>" \
                    "</ul>" \
                    "<div id=\"content_1\" class=\"tab-content\" style=\"display:block;height:100%;\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_discovered_host\" style=\"text-align:center;display:none;\">\
                            <thead><tr><th></th><th>Discovery Type</th>\
                            <th>IP Address</th>\
                            <th>MAC (Ethernet)</th>\
                            <th>Device Type</th>\
                            <th>Discovery Date & Time</th>\
                            </tr></thead>\
                            </table>" \
                    "</div>" \
                    "<div id=\"content_2\" class=\"tab-content\" style=\"display:none;\">" \
                    "</div>" \
                    "<div id=\"content_3\" class=\"tab-content\" style=\"display:none;\">" \
                    "</div>" \
                    "<div id=\"content_4\" class=\"tab-content\" style=\"display:none;\">" \
                    "</div>" \
                    "</div>" \
                    "</div>" \
                    "<div id=\"form_div\" style=\"display:none;\"></div>"
        return html_view

    @staticmethod
    def ping_form():
        """


        @return:
        """
        html_view = "" \
                    "<form action=\"ping_discovery.py\" id=\"form_ping\" method=\"get\" style=\"padding:0px;\"> " \
                    "<div class=\"form-div\" style=\"position:relative;\">" \
                    "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                    "<tr>" \
                    "<th class=\"cell-title\">PING Details</th>" \
                    "</tr>" \
                    "</table>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"ping_ip_base\">IP Base</label>" \
                    "<input type=\"text\" id=\"ping_ip_base\" name=\"ping_ip_base\" title=\"Enter a class C Network IP base. e.g. 192.168.0\" /> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"ping_ip_base_start\">IP Range Start</label>" \
                    "<input type=\"text\" id=\"ping_ip_base_start\" name=\"ping_ip_base_start\" title=\"Enter the IP octet of the Class C Network specified above from which NMS shall start discovering new devices.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"ping_ip_base_end\">IP Range End</label>" \
                    "<input type=\"text\" id=\"ping_ip_base_end\" name=\"ping_ip_base_end\" title=\"Enter the IP octet of the Class C Network specified above at which NMS shall stop discovering new devices.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"ping_timeout\">Timeout</label>" \
                    "<input type=\"text\" id=\"ping_timeout\" name=\"ping_timeout\" title=\"Enter a timeout in seconds for the PING request.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\" style=\"display:none;\">" \
                    "<label class=\"lbl lbl-big\">Service Management</label>" \
                    "<table><tr><td>" \
                    "<input type=\"radio\" id=\"ping_service_mng1\" name=\"ping_service_mng\" value=\"0\"/></td><td><label class=\"sub-lbl\" for=\"ping_service_mng1\">Automatic<label/>" \
                    "</td><td>" \
                    "<input type=\"radio\" checked=\"checked\" id=\"ping_service_mng2\" name=\"ping_service_mng\" value=\"1\"/></td><td><label class=\"sub-lbl\" for=\"ping_service_mng2\">Using Template<label/>" \
                    "</td><td>" \
                    "<input type=\"radio\" id=\"ping_service_mng3\" name=\"ping_service_mng\" value=\"2\"/></td><td><label class=\"sub-lbl\" for=\"ping_service_mng3\">Do not Create<label/>" \
                    "</td></tr></table>" \
                    "</div>" \
                    "</div>" \
                    "<div class=\"form-div-footer\">" \
                    "<button type=\"submit\" class=\"yo-small yo-button\" id=\"submit_ping\"><span class=\"ok\">Submit</span></button>" \
                    "<button type=\"button\" class=\"yo-small yo-button\" id=\"cancel_ping\"><span class=\"cancel\">Cancel</span></button>" \
                    "</div" \
                    "</form>"
        return html_view

    @staticmethod
    def snmp_form(snmp_version_list):
        """

        @param snmp_version_list:
        @return:
        """
        html_view = "" \
                    "<form action=\"snmp_discovery.py\" id=\"form_snmp\" method=\"get\" style=\"padding:0px;\"> " \
                    "<div class=\"form-div\" style=\"position:relative;\">" \
                    "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                    "<tr>" \
                    "<th class=\"cell-title\">SNMP Details</th>" \
                    "</tr>" \
                    "</table>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"snmp_ip_base\">IP Base</label>" \
                    "<input type=\"text\" id=\"snmp_ip_base\" name=\"snmp_ip_base\" title=\"Enter a class C Network IP base. e.g. 192.168.0\" /> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"snmp_ip_base_start\">IP Range Start</label>" \
                    "<input type=\"text\" id=\"snmp_ip_base_start\" name=\"snmp_ip_base_start\" title=\"Enter the IP octet of the Class C Network specified above from which NMS shall start discovering new devices.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"snmp_ip_base_end\">IP Range End</label>" \
                    "<input type=\"text\" id=\"snmp_ip_base_end\" name=\"snmp_ip_base_end\" title=\"Enter the IP octet of the Class C Network specified above at which NMS shall stop discovering new devices.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"snmp_timeout\">Timeout</label>" \
                    "<input type=\"text\" id=\"snmp_timeout\" name=\"snmp_timeout\" title=\"Enter a timeout in seconds for the SNMP request.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"snmp_community\">Community</label>" \
                    "<input type=\"text\" id=\"snmp_community\" name=\"snmp_community\" title=\"Enter community for the SNMP request.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"snmp_port\">Port</label>" \
                    "<input type=\"text\" id=\"snmp_port\" name=\"snmp_port\" title=\"Enter port number for the SNMP request.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"snmp_version\">Version</label>" \
                    "" + snmp_version_list + "" \
                                             "</div>" \
                                             "<div class=\"row-elem\" style=\"display:none;\">" \
                                             "<label class=\"lbl lbl-big\">Service Management</label>" \
                                             "<table><tr><td>" \
                                             "<input type=\"radio\" id=\"snmp_service_mng1\" name=\"snmp_service_mng\" value=\"0\"/></td><td><label class=\"sub-lbl\" for=\"snmp_service_mng1\">Automatic<label/>" \
                                             "</td><td>" \
                                             "<input type=\"radio\" checked=\"checked\" id=\"snmp_service_mng2\" name=\"snmp_service_mng\" value=\"1\"/></td><td><label class=\"sub-lbl\" for=\"snmp_service_mng2\">Using Template<label/>" \
                                             "</td><td>" \
                                             "<input type=\"radio\" id=\"snmp_service_mng3\" name=\"snmp_service_mng\" value=\"2\"/></td><td><label class=\"sub-lbl\" for=\"snmp_service_mng3\">Do not Create<label/>" \
                                             "</td></tr></table>" \
                                             "</div>" \
                                             "</div>" \
                                             "<div class=\"form-div-footer\">" \
                                             "<button type=\"submit\" class=\"yo-small yo-button\" id=\"submit_snmp\"><span class=\"ok\">Submit</span></button>" \
                                             "<button type=\"button\" class=\"yo-small yo-button\" id=\"cancel_snmp\"><span class=\"cancel\">Cancel</span></button>" \
                                             "</div" \
                                             "</form>"
        return html_view

    @staticmethod
    def upnp_form():
        """


        @return:
        """
        html_view = "" \
                    "<form action=\"upnp_discovery.py\" id=\"form_upnp\" method=\"get\" style=\"padding:0px;\"> " \
                    "<div class=\"form-div\" style=\"position:relative;\">" \
                    "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                    "<tr>" \
                    "<th class=\"cell-title\">UPNP Details</th>" \
                    "</tr>" \
                    "</table>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"upnp_timeout\">Timeout</label>" \
                    "<input type=\"text\" id=\"upnp_timeout\" name=\"upnp_timeout\" title=\"Enter a timeout in seconds for the UPNP request.\"/> " \
                    "</div>" \
                    "<div class=\"row-elem\" style=\"display:none;\">" \
                    "<label class=\"lbl lbl-big\">Service Management</label>" \
                    "<table><tr><td>" \
                    "<input type=\"radio\" id=\"upnp_service_mng1\" name=\"upnp_service_mng\" value=\"0\"/></td><td><label class=\"sub-lbl\" for=\"upnp_service_mng1\">Automatic<label/>" \
                    "</td><td>" \
                    "<input type=\"radio\" checked=\"checked\" id=\"upnp_service_mng2\" name=\"upnp_service_mng\" value=\"1\"/></td><td><label class=\"sub-lbl\" for=\"upnp_service_mng2\">Using Template<label/>" \
                    "</td><td>" \
                    "<input type=\"radio\" id=\"upnp_service_mng3\" name=\"upnp_service_mng\" value=\"2\"/></td><td><label class=\"sub-lbl\" for=\"upnp_service_mng3\">Do not Create<label/>" \
                    "</td></tr></table>" \
                    "</div>" \
                    "</div>" \
                    "<div class=\"form-div-footer\">" \
                    "<button type=\"submit\" class=\"yo-small yo-button\" id=\"submit_upnp\"><span class=\"ok\">Submit</span></button>" \
                    "<button type=\"button\" class=\"yo-small yo-button\" id=\"cancel_upnp\"><span class=\"cancel\">Cancel</span></button>" \
                    "</div" \
                    "</form>"
        return html_view

        # @staticmethod
        # def page_tip_discovery():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_discovery.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)


class Service(object):
    """
    UNMP device services for Nagios
    """
    @staticmethod
    def manage_service():
        """


        @return:
        """
        html_view = "" \
                    "<div id=\"form_div\" class=\"form-div\">" \
                    "<div id=\"grid_view_div\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view\" style=\"text-align:center;\">\
                                    <thead><tr><th></th><th></th><th>IP Address</th>\
                                    <th>Host Alias</th>\
                        <th>Hostgroup</th>\
                        <th>Device type</th>\
                        <th>Services</th>\
                        <th>Edit</th>\
                        </tr></thead>\
                     </table>" \
                    "</div>" \
                    "</div>" \
                    "<div class=\"form-div-footer\">\
                     <div class=\"user-header-icon\">\
                       <button class=\"yo-small yo-button\" id=\"apply_changes_services_button\" disabled=\"disabled\" type=\"button\" onclick=\"applyChanges();\">Apply Changes</button>\
                      </div>\
                </div>"
        return html_view

    @staticmethod
    def edit_service_details(host_alias, service_obj):
        """

        @param host_alias:
        @param service_obj:
        @return:
        """
        html_view = '<div style="display:block;overflow:hidden"><h2>%s</h2>' % str(
            host_alias)
        service_names = ""
        for service in service_obj:
            html_view += '<div class=\"row-elem\"><h3>%s%s:</h3></div>' % (
                service[0], "(Heartbeat Rate)" if service[0].lower().find("uptime") != -1 else "")
            html_view += '<div class=\"row-elem\">\
	   	<label class=\"lbl lbl-big\" style="width:100px;" >service check time:</label>\
	   	<select name="%s" id="%s" class="multiselect" title="Click to select an option">' % (
            service[0].replace(" ", "_"), service[0].replace(" ", "_"))
            # if service[0].lower().find("uptime")!=-1:
            #	html_view+='<option value=%s>%s</option></select></div>'%(str(service[1]),str(service[1]))
            # else:\
            timing = str(service[1]) + " mins"
            if str(service[1]) == "518400":
                timing = "Yearly"
            elif str(service[1]) == "43200":
                timing = "Monthly"
            elif str(service[1]) == "1440":
                timing = "Daily"
            elif str(service[1]) == "720":
                timing = "12 Hours"
            html_view += '\
	        <option value=%s>%s (current time)</option>\
		<option value=5>5 mins</option>\
		<option value=10>10 mins</option>\
		<option value=15>15 mins</option>\
		<option value=30>30 mins</option>\
		<option value=45>45 mins</option>\
		<option value=60>60 mins</option>\
		<option value=720>12 Hours</option>\
		<option value=1440>Daily</option>\
		<option value=43200>Monthly</option>\
		<option value=518400>Yearly</option>\
		</select>\
		</div>' % (str(service[1]), timing)
            service_names += str(service[0]) + ","
        html_view += '<input type="hidden" id="service_names" value="%s"/></div>' % (
            service_names)
        return html_view

        # @staticmethod
        # def page_tip_service():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_service.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)


class NetworkMap(object):
    """
    UNMP maps
    """
    @staticmethod
    def network_map():
        """


        @return:
        """
        html_view = "" \
                    "<p>Network Map </p>"
        return html_view

        # @staticmethod
        # def page_tip_network_map():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_network_map.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)


class Vendor(object):
    """
    Add delete Device vendor functionality
    """
    @staticmethod
    def header_buttons():
        """


        @return:
        """
        add_btn = "<div class=\"header-icon\"><img onclick=\"addVendor();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_vendor\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Vendor\"></div>" % theme
        edit_btn = "<div class=\"header-icon\"><img onclick=\"editVendor();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_vendor\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit Vendor\"></div>" % theme
        del_btn = "<div class=\"header-icon\"><img onclick=\"delVendor();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_vendor\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Vendor\"></div>" % theme
        header_btn = del_btn + edit_btn + add_btn
        return header_btn

    @staticmethod
    def manage_vendor():
        """


        @return:
        """
        html_view = "" \
                    "<div id=\"grid_view_div\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view\" ></table>" \
                    "</div>" \
                    "<div id=\"form_div\" style=\"display:none;\"></div>"
        return html_view

    @staticmethod
    def create_form():
        """


        @return:
        """
        html_view = "" \
                    "<form action=\"#\" id=\"form_vendor\" method=\"get\"> " \
                    "<div class=\"form-div\">" \
                    "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                    "<tr>" \
                    "<th id=\"form_title\" class=\"cell-title\">Add New Vendor</th>" \
                    "</tr>" \
                    "</table>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"vendor_name\">Vendor Name</label>" \
                    "<input type=\"text\" id=\"vendor_name\" name=\"vendor_name\" title=\"Enter Vendor Name\" /> " \
                    "<input type=\"hidden\" id=\"host_vendor_id\" name=\"host_vendor_id\" /> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"description\">Description</label>" \
                    "<textarea id=\"description\" name=\"description\" title=\"Enter Vendor Description\"></textarea> " \
                    "</div>" \
                    "</div>" \
                    "<div class=\"form-div-footer\">" \
                    "<button type=\"submit\" class=\"yo-small yo-button\" id=\"add_vendor\"><span class=\"add\">Add</span></button>" \
                    "<button type=\"submit\" class=\"yo-small yo-button\" id=\"edit_vendor\"><span class=\"edit\">Edit</span></button>" \
                    "<button type=\"button\" class=\"yo-small yo-button\" id=\"cancel_vendor\"><span class=\"cancel\">Cancel</span></button>" \
                    "</div" \
                    "</form>"
        return html_view

        # @staticmethod
        # def page_tip_vendor():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_vendor.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)


class BlackListMac(object):
    """
    Unused MAC blacklisting
    """
    @staticmethod
    def header_buttons():
        """


        @return:
        """
        add_btn = "<div class=\"header-icon\"><img onclick=\"addBlackListMac();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_black_list_mac\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Black List Mac\"></div>" % theme
        edit_btn = "<div class=\"header-icon\"><img onclick=\"editBlackListMac();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_black_list_mac\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit Black List Mac\"></div>" % theme
        del_btn = "<div class=\"header-icon\"><img onclick=\"delBlackListMac();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_black_list_mac\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Black List Mac\"></div>" % theme
        header_btn = del_btn + edit_btn + add_btn
        return header_btn

    @staticmethod
    def manage_black_list_mac():
        """


        @return:
        """
        html_view = "" \
                    "<div id=\"grid_view_div\">" \
                    "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view\"></table>" \
                    "</div>" \
                    "<div id=\"form_div\" style=\"display:none;\"></div>"
        return html_view

    @staticmethod
    def create_form():
        """


        @return:
        """
        html_view = "" \
                    "<form action=\"#\" id=\"form_black_list_mac\" method=\"get\"> " \
                    "<div class=\"form-div\">" \
                    "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                    "<tr>" \
                    "<th id=\"form_title\" class=\"cell-title\">Add New Black List Mac</th>" \
                    "</tr>" \
                    "</table>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"black_list_mac_name\">Black List Mac</label>" \
                    "<input type=\"text\" id=\"mac_address\" name=\"mac_address\" title=\"Enter Mac Address\" /> " \
                    "<input type=\"hidden\" id=\"black_list_mac_id\" name=\"black_list_mac_id\" /> " \
                    "</div>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"description\">Description</label>" \
                    "<textarea id=\"description\" name=\"description\" title=\"Enter Black List Mac Description\"></textarea> " \
                    "</div>" \
                    "</div>" \
                    "<div class=\"form-div-footer\">" \
                    "<button type=\"submit\" class=\"yo-small yo-button\" id=\"add_black_list_mac\"><span class=\"add\">Add</span></button>" \
                    "<button type=\"submit\" class=\"yo-small yo-button\" id=\"edit_black_list_mac\"><span class=\"edit\">Edit</span></button>" \
                    "<button type=\"button\" class=\"yo-small yo-button\" id=\"cancel_black_list_mac\"><span class=\"cancel\">Cancel</span></button>" \
                    "</div" \
                    "</form>"
        return html_view

        # @staticmethod
        # def page_tip_black_list_mac():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_black_list_mac.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)
