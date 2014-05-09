#!/usr/bin/python2.6
"""
@author		: Mahipal Choudhary
@date		: 07-Dec-2011
@version	: 0.1
@summary	: this is the View for the user to view logs.
@organisation	: Codescape Consultants Pvt ltd
"""


from datetime import datetime,timedelta
class ManageLogin(object):
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
            html_view="\
            		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" style=\"margin-bottom:0px;\">\
                        <tr>\
                            <th id=\"form_title\" class=\"cell-title\">Details of Logged in Users</th>\
                        </tr>\
            </table>\
			<table class=\"display\" name=\"login_user_table\" id=\"login_user_table\" width=\"100%%\" >\
			</table>"
            return html_view
        except Exception,e:
            return str(e)
            
            
    @staticmethod
    def view_page_tip_manage_login():
	html_view = ""\
	"<div id=\"help_container\">"\
	"<h1>MANAGE LOGIN-SESSION </h1>"\
	"<div>This page manages login-session of Users</div>"\
	"<br/>"\
	"<div>On this page user can end sessions with Inferior Roles.</div>"\
	"<br/>"\
	"<div><strong>Actions</strong></div>"\
	"<div class=\"action-tip\"><div class=\"txt-div\"><div class=\"user-header-icon\"><button class=\"destroy-button\" disabled=\"disabled\"  >Destroy</button>\
	Destroy the Session of the user.  </div></div></div>"
	return html_view 
