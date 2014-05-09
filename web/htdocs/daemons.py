#!/usr/bin/python2.6

"""
@author:   Mahipal Choudhary
@date:     03-11-2011
@version:  0.1
@summary:  this is the View for the user to view all daemons and their status 
@organisation:  Codescape Consultants Pvt ltd
"""
def index(dict_id,dict_name,dict_pid,dict_port,dict_details):
    try:
        s='<table class="yo-table" width="100%" cellpadding="0" cellspacing="0" style="text-align:left">\
 	       <colgroup width="10%"></colgroup>\
 	       <colgroup width="20%"></colgroup>\
 	       <colgroup width="6%"></colgroup>\
	       <colgroup width="6%"></colgroup>\
	       <colgroup width="6%"></colgroup>\
	       <colgroup width="8%"></colgroup>\
		 <tr class="yo-table-head">\
		    <th class=" vertline">Daemon Name</th>\
		    <th>Info</th>\
		    <th>Port</th>\
		    <th>Get Status</th>\
		    <th>State</th>\
		    <th>Actions</th>\
		  </tr>'
        for i in dict_id:
	    s +='\
<tr>\
		   <td class=" vertline" style="text-align:left"><label id="%s_name" style="text-align:left">%s</label></td>\
		   <td  style="text-align:left"><label id="%s_label">%s</label></td>\
		   <td style="text-align:left" ><label id="%s_port">%s</label></td>\
		   <input type="hidden" id="%s_pid" value="%s"/>\
								   <td style="text-align:left"><img src="images/new/refresh3.png" style=\"cursor:pointer;width:18px;\"  title="Refresh" id="%s_refresh" class="daemon-img refresh w-tip-image" /></td>\
								   <td style="text-align:left">\
								   			<img src="images/new/status-0.png" style=\"cursor:pointer;\"  title="ON" id="%s_on" class="daemon-img w-tip-image"/>\
								   			<img src="images/new/status-2.png" style=\"cursor:pointer;\"  title="OFF" id="%s_off" class="daemon-img w-tip-image"/>\
								   </td>\
								   <td style="text-align:left">\
								   				<img src="images/new/play.png" style=\"cursor:pointer;\"  title="Start" id="%s_start" class="daemon-img start w-tip-image"/>'%(dict_id[i],dict_name[i],dict_id[i],dict_details[i],dict_id[i],dict_port[i],dict_id[i],dict_id[i],dict_id[i],dict_id[i],dict_id[i],dict_id[i])
	    if(dict_id[i]=="unmp-ds"):
	        pass
	    else:
	        s+='<img src="images/new/restart.png"  style=\"cursor:pointer;\" title="Restart" id="%s_restart" class="daemon-img restart w-tip-image"/> &nbsp; &nbsp;'%(dict_id[i])
	    s+='<img src="images/new/stop.png"  style=\"cursor:pointer;\"title="Stop" id="%s_stop" class="daemon-img stop w-tip-image"/></td>\
							</tr>'%(dict_id[i])
        s=s+'			</table>'
	return s
        
    except Exception,e:
        return str(e)


def page_tip_daemons():
    html_view = ""\
    "<div id=\"help_container\">"\
    "<h1>DAEMONS MANAGEMENT</h1>"\
    "<div><strong></strong> This page manages Daemons .</div>"\
    "<br/>"\
    "<div>From this page you can start , stop or restart a daemon.</div>"\
    "<br/>"\
    "<div><strong>Actions</strong></div>"\
    "<div class=\"action-tip\"><div class=\"txt-div\"><img src=\"images/new/refresh3.png\" style=\"cursor:pointer;\"/> &nbsp; &nbsp; Refresh -Fetch the Current Running Status of Daemon</div></div>"\
    "<div class=\"action-tip\"><div class=\"txt-div\"><img src=\"images/new/status-0.png\" style=\"cursor:pointer;\"/> &nbsp; &nbsp; On -Last Captured Running State of the Daemon</div></div>"\
    "<div class=\"action-tip\"><div class=\"txt-div\"><img src=\"images/new/status-2.png\" style=\"cursor:pointer;\"/> &nbsp; &nbsp; Off -Last Captured Running State of the Daemon</div></div>"\
    "<div class=\"action-tip\"><div class=\"txt-div\"><img src=\"images/new/play.png\" style=\"cursor:pointer;\"/> &nbsp; &nbsp; Start - Displayed if the Daemon is in Shutdown State. Click to Start the daemon, if the action fails or executes successfully, the User would be duly notified on the same screen.</div></div>"\
    "<div class=\"action-tip\"><div class=\"txt-div\"><img src=\"images/new/restart.png\" style=\"cursor:pointer;\"/> &nbsp; &nbsp; Restart - Displayed if the Daemon is in Shutdown State. Click to Start the daemon, if the action fails or executes successfully, the User would be duly notified on the same screen.</div></div>"\
    "<div class=\"action-tip\"><div class=\"txt-div\"><img src=\"images/new/stop.png\" style=\"cursor:pointer;\"/> &nbsp; &nbsp; Click to stop the daemon</div></div>"\
    "</div>"
    return html_view

