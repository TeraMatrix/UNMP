#!/usr/bin/python2.6
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2010             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

import config

def page_index(html):
    html.req.headers_out.add("Cache-Control", "max-age=7200, public");
    html.write("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
 <title>Network Monitoring System</title>
 <link rel="shortcut icon" href="images/root.png" type="image/ico">
</head>
<frameset frameborder="0" framespacing="0" border="0">
    <frame src="%s" name="main" noresize>
</frameset>
</html>
""" % config.start_url)

def page_main(html):
    css_list = ["css/style.css","css/custom.css","calendrical/calendrical.css",'css/ccpl_jquery_combobox.css',"css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/highcharts.js","js/unmpDashboard.js","calendrical/calendrical.js"]
    html.new_header("Network Monitoring System","main.py","",css_list,javascript_list)
    rl = config.role

    if rl == "admin" or rl == "user":
        html.write("""
        <script type='text/javascript'>
        	$(function(){
        		$('#page_tip').hide();
			var w = $('#container_body').width();           //width of container _body
			if(w < 968){//alert(w);
			  $('#home-snapin-container').css({'width':'100%'});
			}
			else if(w < 1206 && w > 968)
			{
			 $('#home-snapin-container').width('968px'); 
			}
        	});
        </script>
<div id="home-snapin-container" style=\"display:none;\" >
<!-- General -->
<div class="shortcut-icon-div" onclick="javascript:parent.main.location='localhost_dashboard.py';">
<div><img src="images/gray_icon/64x64/chart_pie.png" width="44px" alt="dashboard"/></div><div style="width:60%;"><span class='head'>Dashboard</span><span class='sub-head'>View Core statistics of the UNMP system</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='log_user.py';">
<div><img src="images/gray_icon/64x64/user.png" width="44px" alt="user log"/></div><div style="width:60%;"><span class='head'>User Logs</span><span class='sub-head'>View activity logs of all users</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_events.py';">
<div><img src="images/gray_icon/64x64/device2.png" width="44px" alt="device and service logs"/></div><div style="width:60%;"><span class='head'>Device Logs</span><span class='sub-head'>View all system & device related activity logs</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='daemons_controller.py';">
<div><img src="images/gray_icon/64x64/puzzle.png" width="44px" alt="daemons"/></div><div style="width:60%;"><span class='head'>Daemons</span><span class='sub-head'>View and manage active services in UNMP System</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_host.py';">
<div><img src="images/gray_icon/64x64/games.png" width="44px" alt="inventory"/></div><div style="width:60%;"><span class='head'>Inventory</span><span class='sub-head'>View and manage devices in UNMP Eco-system</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_license.py';">
<div style="margin-left:-8px !important;"><img src="images/gray_icon/64x64/key.png" alt="license"/></div><div style="width:60%;"><span class='head'>License</span><span class='sub-head'>View License info and upgrade UNMP System License </span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_login.py';">
<div style="margin-left:-7px !important;"><img src="images/gray_icon/64x64/lock.png" alt="manage session"/></div><div style="width:60%;"><span class='head'>Sessions</span><span class='sub-head'>Manages login session of users</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_hostgroup.py';">
<div><img src="images/gray_icon/64x64/wired.png" width="44px" alt="manage hostgroup"/></div><div style="width:60%;"><span class='head'>Hostgroups</span><span class='sub-head'>Manage Hostgroups and mapping with Usergroups</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_group.py';">
<div><img src="images/gray_icon/64x64/users.png" width="44px" alt="manage usergroup"/></div><div style="width:60%;"><span class='head'>Usergroups</span><span class='sub-head'>Manage Usergroup and its users</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_user.py';">
<div><img src="images/gray_icon/64x64/users.png" width="44px" alt="users"/></div><div style="width:60%;"><span class='head'>Users</span><span class='sub-head'>Create,Edit and Delete users</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='discovery.py';">
<div><img src="images/gray_icon/64x64/search.png" width="44px" alt="auto discovery"/></div><div style="width:60%;"><span class='head'>Discovery</span><span class='sub-head'>Discover network element or host from the network </span></div>
</div>



<div class="shortcut-icon-div" onclick="javascript:parent.main.location='status_snmptt.py';">
<div><img src="images/gray_icon/64x64/warning.png" width="44px" alt="alerts"/></div><div style="width:60%;"><span class='head'>Alerts</span><span class='sub-head'>View and manage Alerts from the network element</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_service.py';">
<div><img src="images/gray_icon/64x64/add.png" width="44px" alt="service"/></div><div style="width:60%;"><span class='head'>Services</span><span class='sub-head'>View active  services on network element in UNMP System</span></div>
</div>

<div class="shortcut-icon-div">
<div><img src="images/gray_icon/64x64/map.png" width="44px" alt="maps"/></div><div style="width:60%;"><span class='head'>Maps</span><span class='sub-head'>View network element location and its releationships</span><ul class="button_group">
<li><a href="googlemap.py">Google</a></li>
<li><a href="circle_graph.py">Topology</a></li>
</ul></div>
</div>


<div class="shortcut-icon-div">
<div><img src="images/gray_icon/64x64/listing.png" width="44px" alt="listing"/></div><div style="width:60%;"><span class='head'>Listing</span><span class='sub-head'>Configure and monitor network elements</span><ul class="button_group">
<li><a href="mou_listing.py?device_type=mou,rou&device_list_state=enabled&selected_device_type=\'\'">Optical Repeater</a></li>
</ul></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='trapreport.py';">
<div><img src="images/gray_icon/64x64/notebook.png" width="44px" alt="reports"/></div><div style="width:60%;"><span class='head'>Report</span><span class='sub-head'>Generates device reports</span></div>
</div>



<div class="shortcut-icon-div" onclick="javascript:parent.main.location='status_snmptt.py';">
<div><img src="images/gray_icon/64x64/page.png" width="44px" alt="traps"/></div><div style="width:60%;"><span class='head'>Traps</span><span class='sub-head'>View traps generated by network elements</span></div>
</div>

<div style=\"clear:both;padding:10px;\"></div>
<!-- System Specific -->

<div class="shortcut-icon-div" style=\"display:none;\">
<div><img src="images/gray_icon/64x64/chart.png" width="44px" alt="comparison matrix"/></div><div style="width:60%;"><span class='head'>Comparison Matrix</span><span class='sub-head'>User can view all the devices performance information</span></div>
</div>
</div>

""")
    else:
        html.write("""
        <script type='text/javascript'>
        	$(function(){
        		$('#page_tip').hide();
        	});
        </script>
<div id="home-snapin-container">
<!-- General -->
<div class="shortcut-icon-div" onclick="javascript:parent.main.location='localhost_dashboard.py';">
<div><img src="images/gray_icon/64x64/chart_pie.png" width="44px" alt="dashboard"/></div><div style="width:60%;"><span class='head'>Dashboard</span><span class='sub-head'>View core statistics of the UNMP system</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='manage_events.py';">
<div><img src="images/gray_icon/64x64/device2.png" width="44px" alt="device and service logs"/></div><div style="width:60%;"><span class='head'>Device Logs</span><span class='sub-head'>View all system & device related activity logs</span></div>
</div>


<div class="shortcut-icon-div" onclick="javascript:parent.main.location='status_snmptt.py';">
<div><img src="images/gray_icon/64x64/warning.png" width="44px" alt="alerts"/></div><div style="width:60%;"><span class='head'>Alerts</span><span class='sub-head'>View and manage Alerts from the network element</span></div>
</div>

<div class="shortcut-icon-div">
<div><img src="images/gray_icon/64x64/map.png" width="44px" alt="maps"/></div><div style="width:60%;"><span class='head'>Maps</span><span class='sub-head'>View network element location and its releationships</span><ul class="button_group">
<li><a href="googlemap.py">Google</a></li>
<li><a href="circle_graph.py">Topology</a></li>
</ul></div>
</div>


<div class="shortcut-icon-div">
<div><img src="images/gray_icon/64x64/listing.png" width="44px" alt="listing"/></div><div style="width:60%;"><span class='head'>Listing</span><span class='sub-head'>User can configure and monitor network elements</span><ul class="button_group">
<li><a href="idu_listing.py?device_type=idu4,idu8&device_list_state=enabled&selected_device_type=\'\'">IDU</a></li>
<li><a href="odu_listing.py?device_type=ODU16,odu100,ODU16S&device_list_state=enabled&selected_device_type=\'\'">RM18/RM</a></li>
<li><a href="ap_listing.py?device_type=ap25&device_list_state=enabled&selected_device_type=\'\'">AP</a></li>
</ul></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='main_report.py';">
<div><img src="images/gray_icon/64x64/notebook.png" width="44px" alt="reports"/></div><div style="width:60%;"><span class='head'>Report</span><span class='sub-head'>Generates device reports</span></div>
</div>

<div class="shortcut-icon-div" onclick="javascript:parent.main.location='status_snmptt.py';">
<div><img src="images/gray_icon/64x64/page.png" width="44px" alt="traps"/></div><div style="width:60%;"><span class='head'>Traps</span><span class='sub-head'>View traps generated by network elements</span></div>
</div>

<div style="clear:both;padding:10px;"></div>
</div>

"""
)
    html.write("""<div id=\"home_button_div\" class=\"home-button\" >Snapins</div><div id=\"home_dashboard_id\" class=\"form-div\"  style=\"margin-bottom:0px;background-color:#FFF;\">\
        <table cellspacing="10px" cellpadding="0" width="100%%">\
        <colgroup>\
            <col style="width:50%;"/>\
            <col style="width:50%;"/>\
        </colgroup>\
        <tr>\
            <td><div id="dashboard1" class="db-box"></div></td>\
            <td><div id="dashboard2" class="db-box"></div></td>\
        </tr>\
        <tr>\
            <td><div id="dashboard3" class="db-box" style=\"overflow-x:hidden;overflow-y:auto;\"></div></td>\
            <td><div id="dashboard4" class="db-box" style=\"overflow-x:hidden;overflow-y:auto;\"></div></td>\
        </tr>\
		</table>\
    </div>""")
    html.new_footer()

# This function does nothing. The sites have already
# been reconfigured according to the variable _site_switch,
# because that variable is processed by connect_to_livestatus()
def ajax_switch_site(html):
    pass
