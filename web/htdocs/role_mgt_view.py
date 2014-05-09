#!/usr/bin/python2.6

from htmllib import *
import role_bll

special_check = lambda x: 1 if set(
    "\"\`~!#$%^&*(){}[]+=|?<>:;").intersection(x) else 0
space_check = lambda x: 1 if set(" ").intersection(x) else 0


def validate_name(nm, type):
    """

    @param nm:
    @param type:
    @return:
    """
    if len(nm) < 5:
        return 1
    if special_check(nm) == 1:
        return 1
    if space_check(nm) == 0:
        if type == "role":  # role
            result = role_bll.check_rolename(nm, "role")
        else:
            result = 1
        if result == 0:
            return 0
        return 1
    return 1


def check_rolename(h):
    """

    @param h:
    """
    global html
    html = h
    name = html.var("name")
    type = html.var("type")
    result = 1
    __space = 1
    if space_check(name) == 0:
        __space = 0
    if __space == 0:
        if type == "role":  # role
            result = role_bll.check_rolename(name, "role")
        else:
            result = 1
    else:
        result = 1

    if result == 0:
        result = {'success': 0}
    else:
        result = {'success': 1}

    html.write(str(result))


def role_table(h):
    """

    @param h:
    """
    global html
    html = h
    role_str = ""
    table = role_bll.get_role_details("list")
    if table == 1:
        role_str += "<p style=\"border-bottom:1px solid #DDD;padding:5px 10px;height:18px;> Well ! its really embarasing But it seems there is No data availabe.</p>"
    elif table == 111 or table == 11:
        role_str += "<p style=\"border-bottom:1px solid #DDD;padding:5px 10px;height:18px;> Well ! its really embarasing : UnExpected Error.</p>"
    else:
        for tup in table:
            role_str += "<p class=\"role-name\" style=\"border-bottom:1px solid #DDD;padding:5px 10px;height:18px;\" id=\"%s\" >%s</p>" % tup
    html.write(role_str)


def role_info(h):
    """

    @param h:
    """
    global html
    html = h
    table = role_bll.get_role_details("details", html.var("role_id"))
    role_str = ""
    role_str += "<table cellspacing=\"0\" width=\"100%\" cellpadding=\"0\" class=\"tt-table\">\
                             <tbody><tr>\
                                        <td class=\"cell-label\" style=\"text-align:left;\">Updated By</td>\
                                        <td class=\"cell-label\" style=\"text-align:left;\">Update Time</td>\
                                        <td class=\"cell-label\" style=\"text-align:left;\">Created By</td>\
                                        <td class=\"cell-label\" style=\"text-align:left;\">Creation Time</td>\
                                     </tr>"
    if table == 1:
        role_str += "<tr> Well ! its really embarasing But it seems there is No data availabe. </tr>"
    else:
        role_str += "<tr>"
        for tup in table[0]:
            role_str += "<td class=\"cell-info1\">%s</td>" % str(tup)
        role_str += "</tr>"
    role_str += "</tbody></table> "
    html.write(role_str)


def role_view1(h):
    """

    @param h:
    """
    global html
    html = h
    # css_list =
    # ["css/role.css","css/demo_page.css","css/demo_table_jui.css","css
    # /jquery-ui-1.8.4.custom.css","css/divya.css"]
    css_list = ["css/role.css"]
    #,"css/demo_page.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css","css/divya.css"]
    javascript_list = ["js/unmp/main/manage_role.js"]
    add_btn = "<div class=\"header-icon\"><img onclick=\"addRole();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_role\" name=\"add_role\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" title=\"Add Role\"></div>" % theme
    edit_btn = "<div class=\"header-icon\"><img onclick=\"editRole();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_role\" name=\"edit_role\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" title=\"Edit Role\"></div>" % theme
    del_btn = "<div class=\"header-icon\"><img onclick=\"delRole();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_role\" name=\"del_role\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" title=\"Delete Role\"></div>" % theme
    all_btn = del_btn + edit_btn + add_btn
    html.new_header("Role Management", "manage_role.py", all_btn,
                    css_list, javascript_list)
    html.write("<table id=\"role_datatable\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\
        <colgroup>\
            <col width=\"150px\" style=\"width:150px;\"/>\
            <col width=\"auto\" style=\"width:auto;\"/>\
        </colgroup>\
        <tr>\
            <td rowspan=\"2\">\
                <div style=\"float:left;width:150px;height:100%;display:block;border-right:1px solid #CCCCCC;background-color:#F1F1F1;position:relative;font-size:10px;\">\
                                <div id=\"role_name_div\" style=\"display:bolck;width:100%;overflow-x:hidden;overflow-y:auto;\">\</div>\
                                </div>\
                            </div>\
            </td>\
            <td>\
                <div id=\"role_info\" style=\"display:block;\">\
                             </div>\
            </td>\
        </tr>\
        <tr>\
            <td>\
            <div id=\"role_groups\" class=\"role-links\" style=\"border-bottom:1px solid #CCCCCC;display:block;\">\
                             <div id=\"group_inrole_head\" class=\"user-group-th\" >\
                                <Strong>Groups in Role</Strong><span id=\"search_group\" style=\"float:right;\"> Search: <input type=\"text\" id=\"search_Group\" ></span> \
                            </div>\
                            <div id=\"groups_inrole\">\
                            </div>\
                            <div id=\"status-header\">\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" id=\"add_group_to_role\" type=\"button\" onclick=\"addGrpInRole();\" ><span class=\"add\">Add</span></button>\
                                </div>\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" type=\"button\" onclick=\"delGrpFrmRole();\" ><span class=\"delete\" >Delete</span></button>\
                                </div>\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" id=\"move_group_to_role\" type=\"button\" onclick=\"moveGrpToRole();\" ><span class=\"moveto\" >Move</span></button>\
                                </div>\
                            </div>\
                         </div>\
            </td>\
        </tr>\
    </table></div>\
    <div id=\"add_role\" style=\"display:none;\">\
                    \
                </div>\
                <div id=\"edit_role\" style=\"display:none;\">\
                \
                </div>")
    html.new_footer()


def dict_page(snapin, pages):
    """
    used in add_role_view
    @param snapin:
    @param pages:
    """
    dik = {}
    for i in snapin:
        li = []
        for j in pages:
            if i[0] == j[3]:
                li.append((j[0], j[1], j[2]))
        dik[i[0]] = li
    return dik


def dict_module(pageid_list, module):
    """
    used in add_role_view
    @param pageid_list:
    @param module:
    """
    dik = {}
    for i in pageid_list:
        li = []
        for j in module:
            if i == j[2]:
                li.append((j[0], j[1]))
        dik[i] = li
    return dik


def add_roleview(h):
    """

    @param h:
    """
    global html
    html = h
    type_tuple = type(())
    flag = -1
    html_str = ""

    html_str = "<div id=\"add_role_form\" name=\"add_role_form\">\
                    <div class=\"form-div\">\
                        <div class=\"form-body\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl lbl-big\" for=\"rolename\">Role Name</label>\
                                <input type=\"text\" id=\"role_name\" name=\"role_name\" title=\"Choose Unique Role Name. <br/>Must be at least 5 characters, No Space.\" onblur=\"name_chk();\" />\
                                <input type=\"button\" id=\"check_gname\" name=\"check_gname\" value=\"Check availability\" title=\"Check Role Name Availablity\" onclick=\"name_chk();\" />\
                                <span id=\"check_result\" name=\"check_result\" style=\"margin:20px\" ></span>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl lbl-big\" for=\"description\">Description</label>\
                                <textarea id=\"description\" name=\"description\" title=\"Role Description\"></textarea>\
                            </div>\
                            <div class=\"row-elem\">\
                               <label class=\"lbl lbl-big\" for=\"role\" title=\"Select Parent Role\" >Select Parent Role</label>" + roles_select_list(
        "", "") + "\
                            </div>"
    # form-body and form-div is not closed
    html_str += "\
                    </div>\
                    <div class=\"form-div-footer\">\
                        <button onclick=\"roleformSubmit();\" class=\"yo-small yo-button\"><span class=\"add\"></span><strong>Add</strong></button>\
                        <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_role\"><span class=\"cancel\">Cancel</span></button>\
                    </div>\
            </div>"
    html.write(html_str)

#    snapin_tuple = role_bll.get_snapindata()
#    if type(snapin_tuple) == type_tuple:
#        flag = 0
#    elif snapin_tuple == 11:
#        flag = 1
#    if flag == 0:
#        page_tuple = role_bll.get_pagedata(snapin_tuple)
#        if type(page_tuple) == type_tuple:
#            page_list = []
#            for i in page_tuple:
#                page_list.append(i[2])
#        else:
#            flag = 1
#
#        if flag == 0 and len(page_list) > 0:
#            module_tuple = role_bll.get_moduledata(page_list)
#        else:
#            flag = 1 # 2
#
#    if flag == 0:
#        snapins = dict(snapin_tuple)
#        snapin_pages = dict_page(snapin_tuple,page_tuple)
#        page_modules = dict_module(page_list,module_tuple)
#        page_tuple = None
#        module_tuple = None
#	html_str += "<ul id=\"treeList\">"
#        for snap in snapins:
#            dik_s = {}
#            dik_s['snapin_name'] = snapins[snap]
#            html_str += "<li style=\"margin:15px; float:none; \"><div id=\"snapin\" class=\"snapin\" style=\"padding:1px; \">\
#                            <input type=\"checkbox\" style=\"margin:0px; float:none; padding:none; \" name=\"snapin_id\" >\
#                            <span id=\"snapin_name\" style=\"padding:1px; \">\
#                                    %(snapin_name)s\
#                            </span>"%dik_s
#
#            inner_list = snapin_pages[snap]
#            for page_tuple in inner_list:
#                page_id = page_tuple[2]
#                dik_p = {}
#                dik_p['plink_id'] = page_tuple[0]
#                dik_p['page_name'] = page_tuple[1]
#
#                html_str += "<ul><li style=\"margin-left:25px; float:none; \"><div id=\"page\" class=\"page\" style=\"padding:1px; \" >\
#                                        <input type=\"checkbox\" style=\"margin:0px; float:none; padding:none; \" name=\"plink_id\" value=\"%(plink_id)s\" >\
#                                        <span id=\"page_name\" style=\"padding:1px; \">\
#                                                %(page_name)s\
#                                        </span>"%dik_p
#
#
#                inner_list2 = page_modules[page_id]
#                if len(inner_list2) > 0:
#                    for module_tuple in inner_list2:
#                        dik_m = {}
#                        dik_m['module_name'] = module_tuple[0]
#                        dik_m['plink_id'] = module_tuple[1]
#
#                        html_str += "<ul><li style=\"margin-left:25px; float:none; \"> <div id=\"module\" class=\"module\" style=\"padding:1px; \">\
#                                        <input type=\"checkbox\" style=\"margin:0px; float:none; padding:none; \" name=\"plink_id\" value=\"%(plink_id)s\" >\
#                                        <span id=\"module_name\" style=\"padding:1px; \">\
#                                                %(module_name)s\
#                                        </span></div></li></ul>"%dik_m
#
#                    html_str += "</div></li></ul>" # page div close
#
#                else:
#                    html_str += "</div></li></ul>" # page div close
#
#            html_str += "</div></li></li>" # span div close
#
#    if flag == 0:
#        html_str += "</div>\
#                    </div>\
#                    <div class=\"form-div-footer\">\
#                        <button onclick=\"roleformSubmit();\" class=\"yo-small yo-button\"><span class=\"add\"></span><strong>Add</strong></button>\
#                        <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_role\"><span class=\"cancel\">Cancel</span></button>\
#                    </div>\
#            </div>"
#        html_str+= "</ul>"
#        html.write(html_str)
#    elif flag == 1:
#        html.write(" No data in DB ")
#    else:
#        html.write("Sorry for the inconvenience : Error occur ")


def add_role(h):
    """

    @param h:
    """
    global html
    html = h
    var_list = []
    var_dict = {}
    name_not = 0
    sel_page_link = 0
    prole = 0
    role_name = html.var("role_name")
    # plinks = html.var("plink_ids")
    description = html.var("descp")
    prole_id = html.var("prole_id")
    if description == None:
        description = ""
    if role_name == None:
        name_not = 1
    else:
        if validate_name(role_name, "role") == 0:
            pass
        else:
            name_not = 1

    if prole_id != None:
        if len(prole_id) < 6:
            prole = 1
    else:
        prole = 1
    #    if plinks != None:
    #        if len(plinks) < 6:
    #            sel_page_link = 1
    #    else:
    #        sel_page_link = 1

    result_json = {}
    if name_not == 1:
        result_json['success'] = 1
        result_json[
            'result'] = " Name Not valid, Choose Unique Name, No space, Min 5 character"
    elif prole == 1:
        result_json['success'] = 1
        result_json['result'] = " Please select Parent Role"
    #    elif sel_page_link == 1:
    #        result_json['success'] = 1
    #        result_json['result'] = " No page or module is selected "
    else:
        # plink_list = plinks.split(",")
        # result = role_bll.add_role(role_name,prole_id,description,plink_list)
        result = role_bll.add_role(role_name, prole_id, description)
        #        result_json['success'] = 1
        #        result_json['result'] = " Message :   "+str(result)+" : "+str(role_name)
        #        result = 1
        if result == 0:
            result_json['success'] = 0
        else:
            result_json['success'] = 1
            result_json['result'] = " Message :   " + str(result)

    html.write(str(result_json))


def edit_roleview(h):
    """

    @param h:
    """
    global html
    html = h
    type_tuple = type(())
    flag = -1
    html_str = ""
    role_id = html.var("role_id")
    role_tuple = role_bll.get_role_details("form", role_id)
    if type(role_tuple) == type_tuple:
        flag = 0
    elif role_tuple == 11:
        flag = 1
    else:
        flag = 1
    if flag == 0:
        list_role = ['role_id', 'role_name', 'prole_id', 'description']
        dik_role = dict(zip(list_role, role_tuple[0]))
        html_str = "<div id=\"edit_role_form\" name=\"edit_role_form\">\
                        <div class=\"form-div\">\
                            <div class=\"form-body\">\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"rolename\">Role Name</label>\
                                    <input type=\"text\" id=\"role_name\" name=\"role_name\" disabled=\"disabled\" title=\"you can't edit Role Name\" value=\"%(role_name)s\"  />\
                                    <input type=\"hidden\" id=\"role_id\" name=\"role_id\" value=\"%(role_id)s\" />\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"description\">Description</label>\
                                    <textarea id=\"description\" name=\"description\" title=\"Role Description\">%(description)s</textarea>\
                                </div>\
                                " % dik_role
        prole_id = dik_role['prole_id']

        html_str += "<div class=\"row-elem\">\
                       <label class=\"lbl lbl-big\" for=\"role\" title=\"Select Parent Role\" >Select Parent Role</label>" + roles_select_list(
            prole_id, role_id) + "\
                    </div>"
        # form-body and form-div is not closed

        html_str += "\
                    </div>\
                    <div class=\"form-div-footer\">\
                        <button onclick=\"editformSubmit();\" class=\"yo-small yo-button\"><span class=\"edit\"></span><strong>Edit</strong></button>\
                        <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_role\"><span class=\"cancel\">Cancel</span></button>\
                    </div>\
            </div>"
        html.write(html_str)
    #    else:
    #        pass
    #
    #    pagelink_tuple = role_bll.get_page_links(role_id)
    #    #html.write(str(pagelink_tuple))
    #    html_str += "<ul id=\"treeList\">"
    #    if type(pagelink_tuple) == type_tuple:
    #        flag = 0
    #        pagelink_list = []
    #        for i in pagelink_tuple:
    #            pagelink_list.append(i[0])
    #    else:
    #        pagelink_list = []
    #    snapin_tuple = role_bll.get_snapindata()
    #    if type(snapin_tuple) == type_tuple:
    #        flag = 0
    #    elif snapin_tuple == 11:
    #        flag = 1
    #
    #    if flag == 0:
    #        page_tuple = role_bll.get_pagedata(snapin_tuple)
    #        if type(page_tuple) == type_tuple:
    #            page_list = []
    #            for i in page_tuple:
    #                page_list.append(i[2])
    #        else:
    #            flag = 1
    #
    #        if flag == 0 and len(page_list) > 0:
    #            module_tuple = role_bll.get_moduledata(page_list)
    #        else:
    #            flag = 1 # 2
    #
    #    if flag == 0:
    #        snapins = dict(snapin_tuple)
    #        snapin_pages = dict_page(snapin_tuple,page_tuple)
    #        page_modules = dict_module(page_list,module_tuple)
    #        page_tuple = None
    #        module_tuple = None
    #        for snap in snapins:
    #            dik_s = {}
    #            dik_s['snapin_name'] = snapins[snap]
    #
    #            inner_list = snapin_pages[snap]
    #            s_flag = 1
    #            pages_str = ""
    #            for page_tuple in inner_list:
    #                page_id = page_tuple[2]
    #                dik_p = {}
    #                dik_p['plink_id'] = page_tuple[0]
    #                dik_p['page_name'] = page_tuple[1]
    #                page_str = ""
    #
    #                if pagelink_list.count(page_tuple[0]) > 0:
    #                    s_flag = 0
    #                    #html.write(page_tuple[1])
    #                    page_str += "<ul><li style=\"margin-left:25px; float:none;\"><div id=\"page\" class=\"page\" >\
    #                                        <input type=\"checkbox\" name=\"plink_id\" style=\"margin:0px; float:none; padding:none; \" checked=\"checked\" value=\"%(plink_id)s\" >\
    #                                        <span id=\"page_name\" >\
    #                                                %(page_name)s\
    #                                        </span>"%dik_p
    #                else:
    #                    #html.write(page_tuple[1])
    #                    page_str += "<ul><li style=\"margin-left:25px; float:none;\"><div id=\"page\" class=\"page\" >\
    #                                        <input type=\"checkbox\" name=\"plink_id\" style=\"margin:0px; float:none; padding:none; \" value=\"%(plink_id)s\" >\
    #                                        <span id=\"page_name\" >\
    #                                                %(page_name)s\
    #                                        </span>"%dik_p
    #
    #
    #                inner_list2 = page_modules[page_id]
    #                if len(inner_list2) > 0:
    #                    for module_tuple in inner_list2:
    #                        dik_m = {}
    #                        dik_m['module_name'] = module_tuple[0]
    #                        dik_m['plink_id'] = module_tuple[1]
    #                        if pagelink_list.count(module_tuple[1]) > 0:
    #                            #html.write(module_tuple[0])
    #                            s_flag = 0
    #                            page_str += "<ul><li style=\"margin-left:25px; float:none;\"><div id=\"module\" class=\"module\" >\
    #                                            <input type=\"checkbox\" name=\"plink_id\" style=\"margin:0px; float:none; padding:none; \" checked=\"checked\" value=\"%(plink_id)s\" >\
    #                                            <span id=\"module_name\" >\
    #                                                    %(module_name)s\
    #                                            </span></div></li></ul>"%dik_m
    #                        else:
    #                            #html.write(module_tuple[0])
    #                            page_str += "<ul><li style=\"margin-left:25px; float:none;\"><div id=\"module\" class=\"module\" >\
    #                                            <input type=\"checkbox\" name=\"plink_id\" style=\"margin:0px; float:none; padding:none; \" value=\"%(plink_id)s\" >\
    #                                            <span id=\"module_name\" >\
    #                                                    %(module_name)s\
    #                                            </span></div></li></ul>"%dik_m
    #
    #
    #                    page_str += "</div></li></ul>" # page div close
    #                    pages_str += page_str
    #                else:
    #                    page_str += "</div></li></ul>" # page div close
    #                    pages_str += page_str
    #
    #            if s_flag == 0:
    #                html_str += "<li style=\"margin-left:25px; float:none;\"><div id=\"snapin\" class=\"snapin\" >\
    #                            <input type=\"checkbox\" checked=\"checked\" style=\"margin:0px; float:none; padding:none; \" name=\"snapin_id\">\
    #                            <span id=\"snapin_name\" >\
    #                                    %(snapin_name)s\
    #                            </span>"%dik_s
    #                html_str += pages_str
    #            elif s_flag == 1:
    #                html_str += "<li><div id=\"snapin\" class=\"snapin\" >\
    #                            <input type=\"checkbox\" name=\"snapin_id\" style=\"margin:0px; float:none; padding:none; \">\
    #                            <span id=\"snapin_name\" >\
    #                                    %(snapin_name)s\
    #                            </span>"%dik_s
    #                html_str += pages_str
    #            html_str += "</div>" # span div close
    #
    #    #html_str += "</ul>"
    #    if flag == 0:
    #        html_str += "</div>\
    #                    </div></ul>\
    #                    <div class=\"form-div-footer\">\
    #                        <button onclick=\"editformSubmit();\" class=\"yo-small yo-button\"><span class=\"edit\"></span><strong>Edit</strong></button>\
    #                        <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_role\"><span class=\"cancel\">Cancel</span></button>\
    #                    </div>\
    #            </div>"
    #
    #        html.write(html_str)
    elif flag == 1:
        html.write(" No data in DB ")
    else:
        html.write("Sorry for the inconvenience : UnExpected Error ")


def edit_role(h):
    """

    @param h:
    """
    global html
    html = h
    var_list = []
    var_dict = {}
    name_not = 0
    prole = 0
    sel_page = 0
    role_id = html.var("role_id")
    description = html.var("descp")
    prole_id = html.var("prole_id")
    # plinks = html.var("plink_ids")
    # plink_list = plinks.split(",")

    if role_id == None:
        name_not = 1
    #    if len(plinks) < 6:
    #        sel_page = 1
    #
    if len(prole_id) < 6:
        prole = 1

    result_json = {}
    if name_not == 1:
        result_json['success'] = 1
        result_json['result'] = " No role exists pls refresh"
    elif prole == 1:
        result_json['success'] = 1
        result_json['result'] = " Please select Parent Role"
    elif sel_page == 1:
        result_json['success'] = 1
        result_json['result'] = " No page or module is selected "
    else:
        # result = role_bll.edit_role(role_id,description,prole_id,plink_list)
        result = role_bll.edit_role(role_id, description, prole_id)
        # result_json['success'] = 1
        # result_json['result'] = " Message :   "+str(result)
        # result = 1
        if result == 0:
            result_json['success'] = 0
        else:
            result_json['success'] = 1
            result_json['result'] = " Message :   " + str(result)

    html.write(str(result_json))


def del_role(h):
    """

    @param h:
    """
    global html
    html = h
    name_not = 0
    role_id = html.var("role_id")

    if role_id == None:
        name_not = 1

    result_json = {}
    if name_not == 1:
        result_json['success'] = 1
        result_json['result'] = " No Role exists pls refresh ctrl+5 "
    else:
        result = role_bll.del_role(role_id)

        if result == 0:
            result_json['success'] = 0
        else:
            result_json['success'] = 1
            result_json['result'] = " Message :   " + str(result)

    html.write(str(result_json))


def roles_select_list(selectedRole, notRole):
    """

    @param selectedRole:
    @param notRole:
    @return:
    """
    selectString = "<select id=\"role\" name=\"role\" title=\"Select Parent Role\"><option value=\"\" class='required' >-- Select Parent Role --</option>"
    role_tuple = role_bll.get_role_details("list")
    # role_list = ['Admin','Operator','Guest']
    if role_tuple == 1:
        pass
    else:
        for roleName in role_tuple:
            if notRole == str(roleName[0]):
                pass
            elif selectedRole == str(roleName[0]):
                selectString += "<option value=\"" + str(
                    roleName[0]) + "\" selected=\"selected\">" + str(roleName[1]) + "</option>"
            else:
                selectString += "<option value=\"" + str(
                    roleName[0]) + "\">" + str(roleName[1]) + "</option>"
    selectString += "</select>"
    return selectString


# addrole form
#<form action=\"add_role.py\" method=\"get\" id=\"add_role_form\" name=\"add_role_form\">\
#                        <div class=\"form-div\">\
#                            <div class=\"form-body\">\
#                                <div class=\"row-elem\">\
#                                    <label class=\"lbl lbl-big\" for=\"rolename\">Role Name</label>\
#                                    <input type=\"text\" id=\"role_name\" name=\"role_name\" title=\"Choose Unique Role Name. <br/>Must be at least 4 characters, No Space.\" onblur=\"name_chk();\" />\
#                                    <input type=\"button\" id=\"check_gname\" name=\"check_gname\" value=\"Check availability\" title=\"Check Role Name Availablity\" onclick=\"name_chk();\" />\
#                                    <span id=\"check_result\" name=\"check_result\" style=\"margin:20px\" ></span>\
#                                </div>\
#                                <div class=\"row-elem\">\
#                                    <label class=\"lbl lbl-big\" for=\"description\">Description</label>\
#                                    <textarea id=\"description\" name=\"description\" title=\"Role Description\"></textarea>\
#                                </div>\
#                            </div>\
#                        </div>\
#                        <div class=\"form-div-footer\">\
#                            <button type=\"submit\" class=\"yo-small yo-button\"><span class=\"add\"></span><strong>Add</strong></button>\
#                            <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_add_role\"><span class=\"cancel\">Cancel</span></button>\
#                        </div>\
#</form>\



#
# for snap in snapin:
#    dik_s = {}
#    dik_s['snapin_name'] = snapin[snap]
#    html_str += "<div id=\"snapin\" class=\"snapin\" >\
#                    <input type=\"checkbox\" name=\"snapin_id\">\
#                    <span id=\"snapin_name\" >\
#                            \"%(snapin_name)s\"\
#                    </span>"%dik_s
#
#    inner_list = snapin_pages[snap]
#    for page_tuple in inner_list:
#        page_id = page_tuple[2]
#        dik_p = {}
#        dik_p['plink_id'] = page_tuple[0]
#        dik_p['page_name'] = page_tuple[1]
#
#        html_str += "<div id=\"page\" class=\"page\" >\
#                                <input type=\"checkbox\" name=\"plink_id\" value=\"%(plink_id)s\" >\
#                                <span id=\"page_name\" >\
#                                        \"%(page_name)s\"\
#                                </span>"%dik_p
#
#
#        inner_list2 = page_module[page_id]
#        if len(inner_list2) > 0:
#            for module_tuple in inner_list2:
#                dik_m = {}
#                dik_m['module_name'] = module_tuple[0]
#                dik_m['plink_id'] = module_tuple[1]
#
#                html_str += "<div id=\"module\" class=\"module\" >\
#                                <input type=\"checkbox\" name=\"plink_id\" value=\"%(plink_id)s\" >\
#                                <span id=\"module_name\" >\
#                                        \"%(module_name)s\"\
#                                </span></div>"%dik_m
#
#            html_str += "</div>" # page div close
#
#        else:
#            html_str += "</div>" # page div close
#
#    html_str += "</div>" # span div close
#
