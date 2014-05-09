#!/usr/bin/python2.6

import MySQLdb
import uuid
# from unmp_config import SystemConfig
# from gi.overrides.keysyms import cursor

# select = 2
# delete = 3
# insert = 4
# update = 5


global global_db


def db_connect():
    """
    Used to connect to the database :: return database object ed in global_db variable
    """
    db = None
    global global_db
    try:
        db = MySQLdb.connect("localhost", "root", "root", "nms_copy")
        global_db = db
        print " $$$ $$$ Database Connect successful "
    except MySQLdb.Error as e:
        print "/*/*/* MYSQLdb Exception (db connect) : " + str(e)
    except Exception as e:
        print "/*/*/* Database Exception (db connect) : " + str(e)


def db_close():
    """
    closes connection with the database
    """
    global global_db
    try:
        global_db.close()
        print " db connection closed"
    except Exception as e:
        print "/*/*/* Database Exception ( db close ) : " + str(e)


def get_role_details(action, role_id=None):
    """

    @param action:
    @param role_id:
    @return:
    """
    db_connect()

    global global_db
    try:
        if global_db.open != 1:
            return 1
        role_tuple = ()
        if action == "list":
            selectQuery = "SELECT  r.`role_id`, r.role_name FROM roles AS r WHERE r.is_deleted <> 1 and r.is_default <> 0"
        elif action == "form" and role_id != None:
            selectQuery = "SELECT  r.`role_id`, r.role_name, r.parent_id, r.description  FROM roles AS r WHERE r.is_deleted <> 1 and r.is_default <> 0 and r.role_id = \"%s\" " % role_id
        elif action == "details" and role_id != None:
            selectQuery = "SELECT r.updated_by, r.timestamp, r.created_by, r.creation_time   FROM roles AS r WHERE r.is_deleted <> 1 and r.is_default <> 0 and r.role_id = \"%s\" " % role_id
        else:
            db_close()
            return "internal failure in role view"
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            role_tuple = cursor.fetchall()
        cursor.close()
        db_close()
        if len(role_tuple) < 1:
            return 11
        else:
        #            make_list = lambda x: [" - " if i == None or i == '' else i for i in x]
        #            role_list = []
        #            for role in role_tuple:
        #                role_list.append(make_list(role))
            return role_tuple
    except Exception as e:
        return 111


def copy_it():
    """


    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        cursor = global_db.cursor()
        if cursor.execute(sel_query) != 0:
            role_tuple = cursor.fetchall()
        cursor.close()
        db_close()

    except Exception as e:
        return str(e)


def get_snapindata():
    """


    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        snapin_tuple = 1

        sel_query = "SELECT snapin_id, snapin_name FROM snapins WHERE is_deleted <> 1"
        cursor = global_db.cursor()
        if cursor.execute(sel_query) != 0:
            snapin_tuple = cursor.fetchall()
        else:
            snapin_tuple = 11
        cursor.close()
        db_close()

        return snapin_tuple

    except Exception as e:
        return 1


def get_page_links(role_id):
    """

    @param role_id:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        link_tuple = 1

        sel_query = "select `pages_link_id` from `role_pages_link` where `role_id` = \"%s\" " % role_id
        cursor = global_db.cursor()
        if cursor.execute(sel_query) != 0:
            link_tuple = cursor.fetchall()
        else:
            link_tuple = 11
        cursor.close()
        db_close()

        return link_tuple

    except Exception as e:
        return 1


def get_pagedata(snapin_tuple):
    """

    @param snapin_tuple:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        pages_tuple = 1

        sel_query = "SELECT page_link_id, page_name, page_id, snapin_id FROM pages WHERE "
        cursor = global_db.cursor()
        or_flag = 0
        for snapin_id in snapin_tuple:
            if or_flag == 0:
                sel_query += "snapin_id =  '%s' " % (snapin_id[0])
                or_flag = 1
            else:
                sel_query += "OR snapin_id =  '%s' " % (snapin_id[0])

        sel_query += "AND is_deleted <> 1"

        if cursor.execute(sel_query) != 0:
            pages_tuple = cursor.fetchall()
        else:
            pages_tuple = 11
        cursor.close()
        db_close()

        return pages_tuple

    except Exception as e:
        return str(e)


def get_moduledata(page_list):
    """

    @param page_list:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        module_tuple = 1

        sel_query = "SELECT `module_name`,`page_link_id`,`page_id` FROM modules WHERE "
        cursor = global_db.cursor()
        or_flag = 0
        for page_id in page_list:
            if or_flag == 0:
                sel_query += "page_id =  '%s' " % (page_id)
                or_flag = 1
            else:
                sel_query += "OR page_id =  '%s' " % (page_id)

        sel_query += "AND is_deleted <> 1"

        if cursor.execute(sel_query) != 0:
            module_tuple = cursor.fetchall()
        else:
            module_tuple = 11
        cursor.close()
        db_close()

        return module_tuple

    except Exception as e:
        return str(e)


def check_rolename(name, type):
    """

    @param name:
    @param type:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if type == "role":
            selectQuery = "SELECT role_name FROM `roles` WHERE `role_name` = \"%s\"" % name.strip()
        else:
            db_close()
            return 1
        cursor = global_db.cursor()
        queryVal = cursor.execute(selectQuery)
        result = 1
        if queryVal == 0:
            result = 0
        elif queryVal == 1:
            result = 1
        else:
            result = 1
        cursor.close()
        db_close()
        return result

    except Exception as e:
        return 1


# def add_role(role_name,prole_id,description,plink_list):
#    db_connect()
#    global global_db
#    try:
#        if global_db.open != 1:
#            return 1
#        role_id = uuid.uuid1()
#        ins_query = "INSERT INTO `roles` (`role_id`, `role_name`, `description`, `parent_id`, `timestamp`, `created_by`, `creation_time`, `updated_by`)\
#        VALUES (\"%s\", \"%s\", \"%s\", \"%s\", CURRENT_TIMESTAMP, 'cscape', CURRENT_TIMESTAMP, 'cscape')"%(role_id,role_name,description,prole_id)
#
#        ins_query2 = "INSERT INTO `role_pages_link` (`role_pages_link_id`, `role_id`, `pages_link_id`) VALUES"
#        i = 0
#        for plinkid in plink_list:
#            i += 1
#            if i == len(plink_list):
#                ins_query2 += " (uuid(),\"%s\",\"%s\") "%(role_id,plinkid)
#            else:
#                ins_query2 += " (uuid(),\"%s\",\"%s\") ,"%(role_id,plinkid)
#
#        cursor = global_db.cursor()
#        if cursor.execute(ins_query) > 0:
#            if cursor.execute(ins_query2) > 0:
#                global_db.commit()
#                result = 0
#            else:
#                result = 11
#        else:
#            result = 111
#
#        cursor.close()
#        db_close()
#        return result
#
#    except Exception as e:
#        return str(e)
def add_role(role_name, prole_id, description):
    """

    @param role_name:
    @param prole_id:
    @param description:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        role_id = uuid.uuid1()
        ins_query = "INSERT INTO `roles` (`role_id`, `role_name`, `description`, `parent_id`, `timestamp`, `created_by`, `creation_time`, `updated_by`)\
        VALUES (\"%s\", \"%s\", \"%s\", \"%s\", CURRENT_TIMESTAMP, 'cscape', CURRENT_TIMESTAMP, 'cscape')" % (
        role_id, role_name, description, prole_id)

        cursor = global_db.cursor()
        if cursor.execute(ins_query) > 0:
            global_db.commit()
            result = 0
        else:
            result = 111

        cursor.close()
        db_close()
        return result

    except Exception as e:
        return str(e)


def edit_role(role_id, description, p_role_id, plink_list=None):
    """

    @param role_id:
    @param description:
    @param p_role_id:
    @param plink_list:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        st_r = ""

        update_query = "update `roles` set `description` = \"%s\", `parent_id` = \"%s\" , `timestamp` = CURRENT_TIMESTAMP, `updated_by` = 'cscape' where role_id=\"%s\" " % (
            description, p_role_id, role_id)
        if plink_list != None:

            del_query = "DELETE from `role_pages_link` where `role_id` = \"%s\" " % (
                role_id)

            ins_query = "INSERT INTO `role_pages_link` (`role_pages_link_id`, `role_id`, `pages_link_id`) VALUES"
            i = 0
            for plinkid in plink_list:
                i += 1
                if i == len(plink_list):
                    ins_query += " (uuid(),\"%s\",\"%s\") " % (
                        role_id, plinkid)
                else:
                    ins_query += " (uuid(),\"%s\",\"%s\") ," % (
                        role_id, plinkid)

            # st_r += " up "+update_query+"  del "+del_query+"  ins "+ins_query
            # return st_r
            cursor = global_db.cursor()
            cursor.execute(update_query)
            cursor.execute(del_query)
            global_db.commit()
            cursor.execute(ins_query)
        else:
            cursor = global_db.cursor()
            cursor.execute(update_query)
        global_db.commit()
        result = 0
        #    else:
        #        result = 11
        # else:
        #    result = 111

        cursor.close()
        db_close()
        return result

    except Exception as e:
        return str(e)


def del_role(role_id):
    """

    @param role_id:
    @return:
    """
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        sel_query = "select group_id from groups where role_id = \"%s\" " % role_id

        sel_def_id = "select role_id from roles where is_default = 0 "

        del_query = "delete from roles where role_id = \"%s\" " % role_id

        cursor = global_db.cursor()

        result = 0

        if cursor.execute(sel_def_id) > 0:
            default_id_tup = cursor.fetchall()
            default_id = default_id_tup[0][0]
            up_query = "update groups set role_id = \"%s\" " % default_id
        else:
            result = 2

        if result == 0:
            if cursor.execute(sel_query) > 0:
                groupids_tuple = cursor.fetchall()
                comma = 0
                for group_id in groupids_tuple:
                    if comma == 0:
                        up_query += " Where group_id = \"%s\" " % group_id[0]
                        comma = 1
                    else:
                        up_query += " OR group_id = \"%s\" " % group_id[0]

                if cursor.execute(up_query) > 0:
                    result = 0
                else:
                    result = 5
        else:
            result = 2

        if result == 0:
            if cursor.execute(del_query) > 0:
                result = 0
                global_db.commit()
            else:
                result = 3

        cursor.close()
        db_close()
        return result

    except Exception as e:
        return str(e)


def update_grp_inrole(role_id, groupid_list):
    """

    @param role_id:
    @param groupid_list:
    """
    pass
