#!/usr/bin/python2.6
"""
@author		: Mahipal Choudhary
@date		: 07-Dec-2011
@version	: 0.1
@summary	: this is the View for the user to view logs.
@organisation	: Codescape Consultants Pvt ltd
"""


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
            html_view = "\
            		<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" style=\"margin-bottom:0px;\">\
                        <tr>\
                            <th id=\"form_title\" class=\"cell-title\">Details of Logged in Users</th>\
                        </tr>\
            </table>\
			<table class=\"display\" name=\"login_user_table\" id=\"login_user_table\" width=\"100%%\" >\
			</table>"
            return html_view
        except Exception, e:
            return str(e)

            # @staticmethod
            # def view_page_tip_manage_login():
            #     import defaults
            #     f = open(defaults.web_dir + "/htdocs/locale/view_page_tip_manage_login.html", "r")
            #     html_view = f.read()
            #     f.close()
            #     return str(html_view)
