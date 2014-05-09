#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 04-Nov-2011
@version: 0.1
@note: All Views That are Common.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


class Common(object):
    @staticmethod
    def make_select_list(value=[], name=[], selected=None, list_id="list", list_name="list",
                         title="Please Choose Value", message=None):
        list_options = "%s" % (("<option value=\"\">%s</option>" %
                                message) if message != None else "")

        value_length = len(value)
        name_length = len(name)
        if value_length == name_length:
            for i in range(0, value_length):
                if selected == value[i]:
                    list_options += "<option value=\"%s\" selected=\"selected\">%s</option>" % (
                        value[i], name[i])
                else:
                    list_options += "<option value=\"%s\">%s</option>" % (
                        value[i], name[i])

        list_html = "" \
                    "<select id=\"" + str(list_id) + "\" name=\"" + str(list_name) + "\" title=\"" + str(title) + "\">" \
                                                                                                                  "" + str(
            list_options) + "" \
                            "</select>"
        return list_html


class LocalSystem(object):
    @staticmethod
    def localhost_dashboard_table():
        html_str = '\
        <table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
        <tbody>\
            <tr>\
            <th class="cell-title" colspan="4">\
                System Details\
            </th>\
            </tr>\
            <tr>\
            <td class="cell-label">\
                Last Reboot Time\
            </td>\
            <td class="cell-info" id="sys_uptime">\
            </td>\
            <td class="cell-label">\
                RAM\
            </td>\
            <td class="cell-info" id="sys_ram">\
            </td>\
            </tr>\
            <tr>\
            <td class="cell-label">\
                Memory\
            </td>\
            <td class="cell-info" id="sys_memory">\
            </td>\
            <td class="cell-label">\
                Bandwidth\
            </td>\
            <td class="cell-info" id="band_usage">\
                \
            </td>\
            <tr>\
            <td class="cell-label">\
                CPU\
            </td>\
            <td colspan="3" class="cell-info" id="cpu_usage">\
            </td>\
            </tr>\
        </tbody>\
        </table>\
        <table cellspacing="10px" cellpadding="0" width="100%%">\
        <colgroup>\
            <col width="50%%" style="width:50%%;"/>\
            <col width="50%%" style="width:50%%;"/>\
        </colgroup>\
        <tr>\
            <td><div id="dashboard1" class="db-box"></div></td>\
            <td><div id="dashboard2" class="db-box"></div></td>\
        </tr>\
            <td><div id="dashboard3" class="db-box"></div></td>\
            <td><div id="dashboard4" class="db-box"></div></td>\
        </tr>\
    </table>'
        return html_str
