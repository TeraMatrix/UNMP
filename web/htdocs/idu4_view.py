#!/usr/bin/python2.6
from datetime import datetime
class idu4View(object):

    @staticmethod
    def idu4_footer_tab(flag):
        if int(flag)==0:
            html_page='<div id=\"report_button_div\" class=\"form-div-footer\">\
            <table cellspacing="9px" cellpadding="0">\
            <tr>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"0\" name=\"option\" id=\"current_rept_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"current_rept_div\" width=\"25px\">Current Time</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"1\" name=\"option\" id=\"day1_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day1_rprt_div\" width=\"25px\">1 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"2\" name=\"option\" id=\"day2_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day2_rprt_div\" width=\"25px\">2 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"3\" name=\"option\" id=\"day3_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"day3_rprt_div\" width=\"25px\">3 Day</label></td>\
            <td style="vertical-align:middle;"><input type=\"radio\" value=\"4\" name=\"option\" id=\"week_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
            <td style="vertical-align:middle;"><label for=\"week_rprt_div\" width=\"25px\">1 Week</label></td>\
            <td style="text-align:right"><button type=\"submit\" class=\"yo-button\" id=\"odu_report_btn\" style=\"margin-top:5px;\" onclick="idu4PDFReportGeneration();"><span class=\"save\">Report</span></button></td>\
    	 <td style="text-align:left"><button type=\"submit\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="idu4ExcelReportGeneration();"><span class=\"report\">Report</span></button></td>\
            </tr></table>\
            </div></div>\
            '
        else:
    	   html_page='</div>'
        return html_page
    @staticmethod
    def idu4_table(ip_address,odu_start_date,odu_start_time,odu_end_date,odu_end_time,idu_refresh_time,total_count):
        dash_str = '\
        <input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\" />\
        <input type=\"hidden\" id=\"ip_address\" name=\"ip_address\" value=\"%s\" />\
        <input type=\"hidden\" id=\"total_count\" name=\"total_count\" value=\"%s\" />\
        <div style=\"float: right; font-size: 10px; color: rgb(85, 85, 85); font-weight: bold; padding: 10px 20px;\" >\
        <input type=\"textbox\" name=\"odu_start_date\" value=\"%s\" id=\"odu_start_date\" style=\"width:100px;\"/>\
        <input type=\"textbox\" name=\"odu_start_time\" value=\"%s\" id=\"odu_start_time\" style=\"width:80px;\"/>\
        <lable>--</lable>\
        <input type=\"textbox\" name=\"odu_end_date\" value=\"%s\" id=\"odu_end_date\" style=\"width:100px;\"/>\
        <input type=\"textbox\" name=\"odu_end_time\" value=\"%s\" id=\"odu_end_time\" style=\"width:80px;\"/>\
        <input type=\"button\" class=\"yo-small  yo-button\" name=\"odu_graph_show\" value=\"graph\" id=\"idu_graph_show\" style=\"width:50px;\"/>\
       </div>\
        </div>\
        <div id="idu4_host_info_div"></div>\
        <table id=\"idu4_device_graph\" cellspacing="10px" cellpadding="0" width="100%%">\
            <colgroup>\
                <col width="50%%" style="width:50%%;"/>\
                <col width="50%%" style="width:50%%;"/>\
            </colgroup>\
            <tr>\
                <td><div id="dashboard1" class="db-box"></div></td>\
                <td><div id="dashboard2" class="db-box"></div></td>\
            </tr>\
            <tr>\
                <td><div id="dashboard3" class="db-box"></div></td>\
                <td><div id="dashboard4" class="db-box"></div></td>\
            </tr>\
            <tr>\
                <td><div id="dashboard5" class="db-box"></div></td>\
                <td><div id="dashboard6" class="db-box"></div></td>\
            </tr>\
            <tr>\
                <td><div id="dashboard9" class="db-box"></div></td>\
                <td><div id="dashboard10" class="db-box"></div></td>\
            </tr>\
            <tr>\
                <td colspan="2"><div id="dashboard7" class="db-box"></div></td>\
            </tr>\
            <tr>\
                <td colspan="2"><div id="dashboard8" class="db-box"></div></td>\
            </tr>\
            <tr>\
                <td><div id="dashboard11" class="db-box"></div></td>\
            </tr>\
        </table>'% (idu_refresh_time,ip_address,total_count,odu_start_date,odu_start_time,odu_end_date,odu_end_time)
        return dash_str

    @staticmethod
    def device_information_view(result,ip_address):
        hour=0
        minute=0
        second=0
        device_detail=''
        if result is not None:
            if result[0][7] !="" or result!=None:
                hour=result[0][7]/3600
                minute=(result[0][7]/60)%60
                second=result[0][7]%60
            device_detail='<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
            device_detail+='<tbody>\
                        <tr>\
                        <th class="cell-title" colspan="4">\
                            '+str(ip_address)+'\
                        </th>\
                        </tr>\
                        <tr>\
                        <th class="cell-title" colspan="4">\
                            Host Details\
                        </th>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            H/W Serial Number\
                        </td>\
                        <td class="cell-info">'+str('--' if result[0][0]==None or result[0][0]==""  else result[0][0])+'</td>\
                        <td class="cell-label">\
                            System MAC\
                        </td>\
                        <td class="cell-info">'+str('--' if result[0][1]==None or result[0][1]==""  else result[0][1])+'</td>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            TDMOIP Interface MAC\
                        </td>\
                        <td class="cell-info">'+str('--' if result[0][2]==None or result[0][2]==""  else result[0][2])+'</td>\
                        <td class="cell-label">\
                            Active Version\
                        </td>\
                        <td class="cell-info">'+str('--' if result[0][3]==None or result[0][3]==""  else result[0][3])+'</td>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            Passive Version\
                        </td>\
                        <td class="cell-info">'+str('--' if result[0][4]==None or result[0][4]==""  else result[0][4])+'</td>\
                        <td class="cell-label">\
                            BootLoader Version\
                        </td>\
                        <td class="cell-info">'+str('--' if result[0][5]==None or result[0][5]==""  else result[0][5])+'</td>\
                        </tr>\
                        <tr>\
                        <td class="cell-label">\
                            Temperature(C)\
                        </td>\
                        <td class="cell-info">'+str('--' if result[0][6]==None or result[0][6]==""  else result[0][6])+'</td>\
                        <td class="cell-label">\
                            UpTime\
                        </td>\
                        <td class="cell-info">'+str(str(hour)+"Hr "+str(minute)+"Min "+str(second)+"Sec")+'</td>\
                        </tr>\
                        <tr>\
                        <th class="cell-title" colspan="4">\
                            Graphs\
                        </th>\
                        </tr>\
                    <tbody></table>'
        return device_detail

    @staticmethod
    def device_information_view_default():
        device_detail=''
        device_detail='<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
        device_detail+='<tbody>\
                    <tr>\
                    <th class="cell-title" colspan="4">\
                        Host Details\
                    </th>\
                    </tr>\
                    <tr>\
                    <td class="cell-label">\
                        H/W Serial Number\
                    </td>\
                    <td class="cell-info">--</td>\
                    <td class="cell-label">\
                        System MAC\
                    </td>\
                    <td class="cell-info">--</td>\
                    </tr>\
                    <tr>\
                    <td class="cell-label">\
                        TDMOIP Interface MAC\
                    </td>\
                    <td class="cell-info">--</td>\
                    <td class="cell-label">\
                        Active Version\
                    </td>\
                    <td class="cell-info">--</td>\
                    </tr>\
                    <tr>\
                    <td class="cell-label">\
                        Passive Version\
                    </td>\
                    <td class="cell-info">--</td>\
                    <td class="cell-label">\
                        BootLoader Version\
                    </td>\
                    <td class="cell-info">--</td>\
                    </tr>\
                    <tr>\
                    <td class="cell-label">\
                        Temperature(C)\
                    </td>\
                    <td class="cell-info">--</td>\
                    <td class="cell-label">\
                        UpTime\
                    </td>\
                    <td class="cell-info">--</td>\
                    </tr>\
                    <tr>\
                    <th class="cell-title" colspan="4">\
                        Graphs\
                    </th>\
                    </tr>\
                <tbody></table>'
        return device_detail

    @staticmethod
    def idu4_event_view(result,table_option,ip_address):
        image_title_name={0:"Normal",1:"Informational",2:"Normal",3:"Minor",4:"Major",5:"Critical"}
        image_dic={0:"images/status-0.png",1:"images/status-0.png",2:"images/status-0.png",3:"images/minor.png",4:"images/status-1.png",5:"images/critical.png"}
        length=5
        history_trap=''
        if table_option.strip() == "trap":
            if len(result) < 5:
                length=len(result)    
            history_trap='<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
            history_trap +='<tbody>\
            <tr class="yo-table-head" >\
                <th class=" vertline">&nbsp;</th>\
                <th>Event Id</th>\
                <th>Event Type</th>\
                <th>Receive Date</th>\
            </tr>'

            for i in range(length):
                if i<4:
                    history_trap+='<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>'% (image_dic[result[i][0]],image_title_name[result[i][0]],image_title_name[result[i][0]])
                    history_trap+='<td>%s</td>'%result[i][1]
                    history_trap+='<td>%s</td>'%result[i][2]
                    history_trap+='<td>%s</td></tr>'%result[i][3]
                else:
                    history_trap+='<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>'% (image_dic[result[i][0]],image_title_name[result[i][0]],image_title_name[result[i][0]])
                    history_trap+='<td>%s</td>'%result[i][1]
                    history_trap+='<td>%s</td>'%result[i][2]
                    history_trap+='<td>%s&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%s</td></tr>'%(result[i][3],(("<a href=\"status_snmptt.py?trap_status=history&ip_address="+ip_address+"\">more>></a>" if len(result) >5 else "" )))
            if len(result)<1:
                history_trap+='<tr ><td colspan="4"><b>Alarm does not exists.</b></td></tr>'

        else:
            # This query return the latest five entry of current alarm 
            length=5
            if len(result) < 5:
                length=len(result)    
            current_alarm_html='<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
            current_alarm_html +='<tbody>\
            <tr class="yo-table-head">\
                <th class=" vertline">&nbsp;</th>\
                <th>Event Id</th>\
                <th>Event Type</th>\
                <th>Receive Date</th>\
            </tr>'
            for i in range(length):
                if i<4:
                    current_alarm_html+='<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>'% (image_dic[result[i][0]],image_title_name[result[i][0]],image_title_name[result[i][0]])
                    current_alarm_html+='<td>%s</td>'%result[i][1]
                    current_alarm_html+='<td>%s</td>'%result[i][2]
                    current_alarm_html+='<td>%s</td></tr>'%result[i][3]
                else:
                    current_alarm_html+='<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>'% (image_dic[result[i][0]],image_title_name[result[i][0]],image_title_name[result[i][0]])
                    current_alarm_html+='<td>%s</td>'%result[i][1]
                    current_alarm_html+='<td>%s</td>'%result[i][2]
                    current_alarm_html+='<td>%s&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%s</td></tr>'%(result[i][3],(("<a href=\"status_snmptt.py?trap_status=history&ip_address="+ip_address+"\">more>></a>" if len(result) >5 else "" )))
            if len(result)<1:    
                current_alarm_html+='<tr ><td colspan="4"><b>Alarm does not exists.</b></td></tr>'
            # close database connection and cursor.
            history_trap=current_alarm_html
            history_trap+="</tbody></table>"
        history_trap_detail={'success':0,'output':history_trap}
        return history_trap_detail 

    @staticmethod
    def idu4_link_status_view(result,error_state):
        link_status='<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
        link_status +='<tbody>\
        <tr class="yo-table-head">\
            <th>Date Time</th>\
            <th>Port Number</th>\
            <th>Operatio State</th>\
            <th>Min JB Level</th>\
            <th>Max JB Level</th>\
            <th>Under Run Occured</th>\
            <th>Over Run Occured</th>\
        </tr>'
        if int(error_state)==1:
            link_status+='<tr ><td colspan="7" style=\"text-align:center;\"><b>Link status informations does not exists.</b></td></tr>'
        else:
            for i in range(len(result)):
                link_status+='<td>%s</td>'%'' if result[i][0]=='' or result[i][0]==None else result[i][0].strftime('%d-%m-%Y %H:%M')
                link_status+='<td>%s</td>'%'' if result[i][1]=='' or result[i][1]==None else result[i][1]
                link_status+='<td>%s</td>'%'' if result[i][2]=='' or result[i][2]==None else result[i][2]
                link_status+='<td>%s</td>'%'' if result[i][3]=='' or result[i][3]==None else result[i][3]
                link_status+='<td>%s</td>'%'' if result[i][4]=='' or result[i][4]==None else result[i][4]
                link_status+='<td>%s</td>'%'' if result[i][5]=='' or result[i][5]==None else result[i][5]
                link_status+='<td>%s</td>'%'' if result[i][6]=='' or result[i][6]==None else result[i][6]
        link_status+="</tbody></table>"
        link_result={'success':0,'output':link_status}
        return link_result

    @staticmethod
    def idu4_e1_port_statistics_view(result,error_state):
        state={0:'disabled',1:'enabled'}
        dic_1={0:'bitclear',1:'bitset'}
        dic_2={1:'bitclear',0:'bitset'}
        adpt_state={0:'state Idle' ,1:'State Self Test' ,2: 'State Acquistion',3:'State Tracking1',4:'State Tracking2',5:'State Recovered' ,6:'State Not Active'}
        hold_over={0:'In Hold Over Mode',1:'In Normal Mode'}
        link_status='<div style=\"overflow-x:auto;overflow-y:hidden; width:100%; height:100%;\"><table style=\"width:100%\" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
        link_status +='<tbody>\
        <tr class="yo-table-head">\
            <th>Date Time</th>\
            <th>Operatio State</th>\
            <th>LOS</th>\
            <th>LOF</th>\
            <th>Alarm  Indication Signal</th>\
            <th>Remote Alarm  Indication</th>\
            <th>Receive Frame Slip</th>\
            <th>Transmit Frame Slip</th>\
            <th>Recovery Clock State</th>\
            <th>Over Run Occured</th>\
        </tr>'
        if int(error_state)==1 or len(result)==0:
            link_status+='<tr ><td colspan="10" style=\"text-align:center;\"><b>E1 Port statistcis informations does not exists.</b></td></tr>'
        else:
            for i in range(len(result)):
                link_status+='<td>%s</td>'%('--' if result[i][0]=='' or result[i][0]==None else result[i][0].strftime('%d-%m-%Y %H:%M'))
                link_status+='<td>%s</td>'%('--' if result[i][1]=='' or result[i][1]==None else state[int(result[i][1])])
                link_status+='<td>%s</td>'%('--' if result[i][2]=='' or result[i][2]==None else dic_1[int(result[i][2])])
                link_status+='<td>%s</td>'%('--' if result[i][3]=='' or result[i][3]==None else dic_1[int(result[i][3])])
                link_status+='<td>%s</td>'%('--' if result[i][4]=='' or result[i][4]==None else dic_1[int(result[i][4])])
                link_status+='<td>%s</td>'%('--' if result[i][5]=='' or result[i][5]==None else dic_1[int(result[i][5])])
                link_status+='<td>%s</td>'%('--' if result[i][6]=='' or result[i][6]==None else dic_2[int(result[i][6])])
                link_status+='<td>%s</td>'%('--' if result[i][7]=='' or result[i][7]==None else dic_2[int(result[i][7])])
                link_status+='<td>%s</td>'%('--' if result[i][8]=='' or result[i][8]==None else adpt_state[int(result[i][8])])
                link_status+='<td>%s</td>'%('--' if result[i][9]=='' or result[i][9]==None else hold_over[int(result[i][9])])
        link_status+="</tbody></table></div>"
        link_result={'success':0,'link_table':link_status}
        return link_result

        
        
