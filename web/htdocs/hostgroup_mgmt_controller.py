#!/usr/bin/python2.6

'''
@author		: Mahipal Choudhary
@since		: 07-Nov-2011
@version	: 0.1
@note		: All Controller functions Related with Reporting.
@organization	: Codescape Consultants Pvt. Ltd.
@copyright	: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see		: http://www.codescape.in
'''


# Import modules that contain the function and libraries
from hostgroup_mgmt import HostgroupMgmt
from hostgroup_mgmt_bll import HostgroupMgmtBll

# calling the view for reporting


def hostgroup_mgmt_view(h):
    '''
    @author			: Mahipal Choudhary
    @since			: 07-Nov-2011
    @requires			: html object h
    @param h			: html object from request
    @var html			: global object html
    @var css_list		: list storing name of css required
    @var js_list		: list storing name of javascript files required
    @note			: This is the controller function to create form for CRC PHY reports
    '''
    global html
    html = h
    css_list = ["css/demo_table_jui.css",
                "css/jquery-ui-1.8.4.custom.css", "css/style12.css", "css/divya.css"]
    js_list = ["js/lib/main/jquery.dataTables.min.js", "js/unmp/main/hostgroup_mgmt.js"]
    # header_btn = HostgroupMgmt.header_buttons()
    html.new_header("MAPPING BETWEEN HOSTGROUP AND USER GROUPS",
                    "hostgroup_mgmt_view.py", "", css_list, js_list)
    html.write(HostgroupMgmt.create_form())
    html.new_footer()


def get_hostgroup_data(h):
    '''
    @author			: Mahipal Choudhary
    @since			: 07-Nov-2011
    @requires			: html object h
    @param h			: html object from request
    @var html			: global object html
    @var no_of_devices		: number of devices for which report has to be generated
    @var date_start		: the starting date of report
    @var date_end		: the ending date of report
    @var all_host		: list of all hosts
    @var all_group		: list of all groups
    @var r			: the object of Report_bll class
    @var average_list		: list of average data for which report will be generated
    @note			: This function returns average data for CRC PHY reports
    '''
    global html
    html = h
    hostgroup_obj = HostgroupMgmtBll()
    hg = hostgroup_obj.get_hostgroup_data()
    html.write(str(hg))


def get_user_data_hostgroup(h):
    global html
    html = h
    sess_grp_name = html.req.session['group']
    host_id = html.var("hostgroup_id")
    hostgroup_obj = HostgroupMgmtBll()
    if sess_grp_name.lower() == 'superadmin':
        userdata = hostgroup_obj.get_usergroup_data(host_id, 1)

    else:
        userdata = hostgroup_obj.get_usergroup_data(host_id, 0)

    html.write(str(userdata))


def viewGroupDetails(h):
    global html
    html = h
    group_id = html.var("group_id")
    hostgroup_obj = HostgroupMgmtBll()
    res = hostgroup_obj.get_usergroup_details(group_id)
    # html.write(res)
    html.write(str(HostgroupMgmt.viewGroupDetails(res)))


# def view_page_tip_hostgroup(h):
#     global html
#     html = h
#     html.write(HostgroupMgmt.view_page_tip_hostgroup())
