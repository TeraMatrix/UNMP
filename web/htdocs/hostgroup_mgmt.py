#!/usr/bin/python2.6
"""
@author		: Mahipal Choudhary
@date		: 07-Dec-2011
@version	: 0.1
@summary	: this is the View for the user to view logs.
@organisation	: Codescape Consultants Pvt ltd
"""


class HostgroupMgmt(object):
    @staticmethod
    def header_buttons():
        add_btn = "<div class=\"header-icon\"><img onclick=\"addHostgroup();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Hostgroup\"></div>" % theme
        edit_btn = "<div class=\"header-icon\"><img onclick=\"editHostgroup();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit Hostgroup\"></div>" % theme
        del_btn = "<div class=\"header-icon\"><img onclick=\"delHostgroup();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Hostgroup\"></div>" % theme
        header_btn = del_btn + edit_btn + add_btn
        return header_btn

    @staticmethod
    def create_form():
        '''
        @author		: Mahipal Choudhary
        @since		: 07-Dec-2011
        @requires	: Nothing
        @var html_view	: string containing code of View for logs
        @return		: the string of view.
        @note		: This function creates form for displaying all logs to the user.
        '''
        try:
            html_view = "\
            <div id=\"mahipal\">\
            <form name=\"get_hostgroup_data\" id=\"get_hostgroup_data\" action=\"get_hostgroup_data.py\" method=\"get\"> </form>\
            		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" style=\"margin-bottom:0px;\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\">Details of Mapping between Hostgroups and User Groups</th>\
                    </tr>\
            </table>\
			<table class=\"display\" name=\"hostgroup_table\" id=\"hostgroup_table\" width=\"100%%\" >\
			</table>\
			</div>\
			\
			<div id=\"rahul\" style=\"display:none;\"> \
			<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" style=\"margin-bottom:0px;\">\
                    <tr>\
                        <th id=\"form_title\" class=\"cell-title\"><div id=\"hg_details\" style=\"font-size:12px; display:inline;\"></div>Hostgroup Details</th>\
                    </tr>\
            </table>\
			<table id=\"hostgroup_table\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\
		<colgroup>\
			<col width=\"auto\" style=\"width:auto;\"/>\
		</colgroup>\
		<tr>\
			<td>\
				<div id=\"hostgroup_info\" style=\"display:block;\">\
                         </div>\
			</td>\
		</tr>\
		<tr>\
			<td>\
                <div id=\"hostgroup_groups\" style=\"border-bottom:1px solid #CCCCCC;display:block;\">\
                             <div id=\"grp_inhg_head\" class=\"user-group-th\" style=\"border-top:1px solid #AAA;\"  >\
                                    <Strong>Groups Assigned to This Hostgroup</Strong>  \
                                    <div align=\"right\" style=\"padding-right:15px; padding-top:5px;\"><button class=\"yo-button disabled\" id=\"add_group_to_hg\" type=\"button\" ><span class=\"add\">Add Group(s)</span></button> </div>\
                            </div>\
                            <div id=\"status-header\" style=\"height:30px;border-bottom:0.5px solid #DDD;\" >\
                                    <div align=\"right\" style=\"padding-right:15px;\" >\
                                          <button class=\"yo-button disabled\" type=\"button\" onclick=\"delGrpFrmHg();\"  ><span class=\"delete\" >Remove Group</span></button>\
                                          <button class=\"yo-button disabled\" id=\"move_group_to_hg\" type=\"button\" onclick=\"moveGrpToHg();\" ><span class=\"moveto\" >Move Group</span></button>\
                                    </div>\
                            </div>\
</td>\
		</tr>\
	</table>\
		<form name=\"get_user_data_hostgroup\" id=\"get_user_data_hostgroup\" action=\"get_user_data_hostgroup.py\" method=\"get\"> </form>\
			<table class=\"display\" name=\"user_details_table\" id=\"user_details_table\" width=\"100%%\" >\
			</table>\
			</div>\
			<div id=\"form_div\" style=\"display:none;\"></div>"
            return html_view
        except Exception, e:
            return str(e)

    @staticmethod
    def viewGroupDetails(res):
        html_str = '<div>\
    			<div id=\"viewGroupDetailsHead\" class=\"user-group-th\" >\
                      	  <Strong>USERS IN THIS GROUP</Strong>\
                        </div>\
                        <table class=\"yo-table\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" >\
                        	<colgroup width="30%"></colgroup>\
 	       			<colgroup width="30%"></colgroup>\
 	       			<colgroup width="30%"></colgroup>\
 	       			<tr class="yo-table-head">\
 	       				<th class=" vertline">User Name:</th>\
		    			<th>Mobile Number</th>\
		    			<th>Email ID</th>\
		    		</tr>'
        for i in range(0, len(res)):
            html_str += '<tr>\
		   <td class=" vertline">%s</td>\
		   <td class=" vertline">%s</td>\
		   <td class=" vertline">%s</td>\
		   </tr>' % (res[i][0], res[i][1], res[i][2])

        html_str += "</div>"
        return html_str

        # @staticmethod
        # def view_page_tip_hostgroup():
        #     import defaults
        #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_hostgroup.html", "r")
        #     html_view = f.read()
        #     f.close()
        #     return str(html_view)
