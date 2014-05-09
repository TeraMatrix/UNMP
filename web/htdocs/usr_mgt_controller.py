#!/usr/bin/python2.6

"""
@author: Rahul Gautam
@note: user Management Controller
"""


import MySQLdb
import uuid
from unmp_config import SystemConfig

global global_db

def db_connect():
    """
    Used to connect to the database :: return database object ed in global_db variable
    """
    db = None
    global global_db
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        global_db = db
        print " $$$ $$$ Database Connect successful "
    except MySQLdb.Error as e:
        print "/*/*/* MYSQLdb Exception (db connect) : "+str(e)
    except Exception as e:
        print "/*/*/* Database Exception (db connect) : "+str(e)


def db_close():
    """
    closes connection with the database
    """
    global global_db
    try:
        global_db.close()
        print " db connection closed"
    except Exception as e:
        print "/*/*/* Database Exception ( db close ) : "+str(e)


def getGroupsData():
    db_connect()
    global global_db
    db_close()


def get_group_list():
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1        
        query = "select `group_name`,`group_id` from groups where `is_deleted` <> 1"
        cursor = global_db.cursor()
        groupName_list = ()
        if cursor.execute(query) != 0:
            groupName_list = cursor.fetchall()
        cursor.close()
        db_close()
        if len(groupName_list) < 1 :
            return 1
        else:
            return groupName_list
        
    except Exception as e:
        return 1
    


def get_group_users(groupID):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        
        query = "SELECT ug.user_id, ul.user_name, u.first_name, u.last_name FROM users_groups AS ug INNER JOIN users AS u ON ug.user_id = u.user_id INNER JOIN user_login AS ul ON ug.user_id = ul.user_id WHERE group_id = \"%s\""%groupID
        gpUsers_tuple = ()
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            gpUsers_tuple = cursor.fetchall()
        cursor.close()
        db_close()
        if len(gpUsers_tuple) < 1 :
            return 1
        else:
#            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
#            gpUsers_list = []
#            for gpUser in gpUsers_tuple:
#                gpUsers_list.append(make_list(gpUser))
            return gpUsers_tuple
    except Exception as e:
        return 1


#print "hi",get_group_users("a0564ece-f668-11e0-a835-f04da24c7c26")

def get_group_info(groupID):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        
        query = "SELECT roles.role_name, groups.updated_by, groups.timestamp, groups.created_by, groups.creation_time FROM groups INNER JOIN roles ON roles.role_id = groups.role_id WHERE groups.group_id = \"%s\""%groupID
        gpDetail_tuple = ()
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            gpDetail_tuple = cursor.fetchone()
        cursor.close()
        db_close()
        if len(gpDetail_tuple) < 1 :
            return 1
        else:
#            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
#            return make_list(gpDetail_tuple)
            return gpDetail_tuple
    except Exception as e:
        return 1
    


def del_user_from_group(user_ids_list,flag=1):
    db_connect()
    global global_db
    flag2 = 1
    try:
        delQuery = "delete from users_groups where "
        i = 0
        for user_id in user_ids_list:
            i +=1
            if len(user_ids_list) == i:
                delQuery += "`user_id` = \"%s\" "%user_id         
            else:
                delQuery += "`user_id` = \"%s\" OR"%user_id
        
        if flag == 1:
            
            selQuery = "SELECT group_id FROM groups WHERE group_name = 'Default'"
                                   
            insQuery = "INSERT INTO `users_groups` (`user_group_id`, `user_id`, `group_id`) values"
            flag2 == 0
        
        
        cursor = global_db.cursor()
        if cursor.execute(delQuery) < 1:
            cursor.close()
            db_close()
            return 2
                
        if flag == 1 and flag2 == 1:
            if cursor.execute(selQuery) != 1:
                cursor.close()
                db_close()
                return 2
            else:
                default_id = cursor.fetchone()
                
            selectQuery = "SELECT user_id FROM `users_groups` WHERE \"%s\" "%default_id
            cursor.execute(selectQuery)
            
            ids_tuple = cursor.fetchall()
        
            f = lambda x: tuple(j[0] for j in x)
        
            ids_tuple = f(ids_tuple)  
             
            i = 0   
            for id in user_ids_list:
                i += 1
                try:
                    ids_tuple.index(id)
                except ValueError as e:
                    is_ins = 0
                    if i == len(user_ids_list):
                        insQuery += " (uuid(),\"%s\",\"%s\") "%(id,default_id[0])
                    else:
                        insQuery += " (uuid(),\"%s\",\"%s\") ,"%(id,default_id[0])
            
              
                   
            if is_ins == 0:
                cursor.execute(insQuery) 
            else:
                print "insert NOT happening"
            
        else:
            pass
        global_db.commit()        
        cursor.close()
        if flag == 1:
            db_close()
        elif flag == 0:
            pass
        else:
            db_close()
            
        return 0
        
    except Exception as e:
        return 1

       
def add_user_in_group(user_ids_list,newGroupID):  
    global global_db
    try:
        insQuery = "insert into users_groups  (`user_group_id`, `user_id`, `group_id`) values"
        
        i = 0   
        for uid in user_ids_list:
            i += 1
            if i == len(user_ids_list):
                insQuery += " (uuid(),\"%s\",\"%s\") "%(uid,newGroupID)
            else:
                insQuery += " (uuid(),\"%s\",\"%s\") ,"%(uid,newGroupID)
        
        
        delResult = del_user_from_group(user_ids_list,0)
        
        if delResult != 0:
            return 1         
                                        
        if global_db.open != 1:
            return 1
                 
        cursor = global_db.cursor()
        
        if cursor.execute(insQuery) < 1:
            cursor.close()
            db_close()
            return 3
        global_db.commit()
        cursor.close()
        db_close()
        return 0
        
    except Exception as e:
        return 1

#print addUserInGroup('bb347a54-f668-11e0-a835-f04da24c7c26','4c83a918-f668-11e0-a835-f04da24c7c26')

def add_user(u_dict,ul_dict,ug_dict):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        userID = uuid.uuid1()
        u_dict['user_id'] = userID
        ul_dict['user_id'] = userID
        ug_dict['user_id'] = userID
        insQuery1 = """INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `designation`, `company_name`, `mobile_no`, `address`, `city_id`, `state_id`, `country_id`, `email_id`) VALUES (\"%(user_id)s\", \"%(first_name)s\", \"%(last_name)s\", \"%(designation)s\", \"%(company)s\", \"%(mobile)s\", \"%(address)s\", NULL, NULL, NULL, \"%(email_id)s\")"""%u_dict
        insQuery2 = """INSERT INTO `user_login` (`user_login_id`, `user_id`, `user_name`, `password`, `timestamp`, `created_by`, `creation_time`, `is_deleted`, `updated_by`, `nms_id`) VALUES (UUID(), \"%(user_id)s\", \"%(user_name)s\", \"%(password)s\", '0000-00-00 00:00:00', 'SuperAdmin', CURRENT_TIMESTAMP, '0', NULL, NULL)"""%ul_dict
        insQuery3 = """INSERT INTO `users_groups` (`user_group_id`, `user_id`, `group_id`) VALUES (UUID(), \"%(user_id)s\", \"%(groups)s\")"""%ug_dict
        cursor = global_db.cursor()
        
        if cursor.execute(insQuery1) != 1:
            cursor.close()
            db_close()
            return 3 
        if cursor.execute(insQuery2) != 1:
            cursor.close()
            db_close()
            return 3
        if cursor.execute(insQuery3) != 1:
            cursor.close()
            db_close()
            return 3
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 1


    


def check_name(name,type):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if type == "user":
            selectQuery = "SELECT user_name FROM `user_login` WHERE `user_name` = \"%s\""%name.strip()
        elif type == "group":
            selectQuery = "SELECT group_name FROM `groups` WHERE `group_name` = \"%s\""%name.strip()
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
    
def groupname_avail(gpname):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        selectQuery = "SELECT group_name FROM `groups` WHERE `group_name` = \"%s\""%gpname.strip()
        cursor = global_db.cursor()
        queryVal = cursor.execute(selectQuery)
        result = 1 
        if queryVal == 0:
            result = 0
        elif queryVal == 1:
            result = 11
        else:
            result = 11     
        cursor.close()
        db_close()
        return result
    
    except Exception as e:
        return 1



def del_user(user_ids_list,flag = 1):
    db_flag = 1
    if flag != 0:
        db_connect()
        db_flag = 0
    else:
        pass 
    global global_db
    try:
        if global_db.open != 1:
            return 1
        
        delQuery = "delete from users where "
        i = 0
        for user_id in user_ids_list:
            i +=1
            if len(user_ids_list) == i:
                delQuery += "user_id = \"%s\" "%user_id         
            else:
                delQuery += "user_id = \"%s\" OR "%user_id
    
        cursor = global_db.cursor()
        if cursor.execute(delQuery) == 1:
            pass
        elif cursor.execute(delQuery) == 0:   
            pass
        else:        
            cursor.close()
            db_close()
            return 4
        global_db.commit() 
        cursor.close()
        if flag == 0 and db_flag == 1:
            pass
        else:
            db_close()
        return 0
    
    except Exception as e:
        return 1

def del_enable_user(userID,value):
    db_connect()
    global global_db
    if global_db.open != 1:
        return 1
    
    updateQuery = "UPDATE user_login set `is_deleted` = %s where `user_id` = \"%s\""%(value,userID)
    
    if cursor.execute(updateQuery) != 1:
        cursor.close()
        db_close()
        return 4
    global_db.commit() 
    cursor.close()
    db_close()
    pass

def edit_user_view(userID):
    db_connect()
    global global_db
    result = 1
    try:
        if global_db.open != 1:
            result = 1
        selectQuery = "SELECT ul.user_id,ul.`user_name`,g.`group_name`,u.`first_name`,u.`last_name`,u.`designation`,u.`company_name`,u.`mobile_no`,u.`address`,u.`email_id` FROM users as u INNER JOIN user_login as ul ON ul.user_id = u.user_id INNER JOIN users_groups as ug ON ug.user_id = ul.user_id INNER JOIN groups as g ON g.group_id = ug.group_id  WHERE ul.user_id = \"%s\""%userID
        
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            user_details = cursor.fetchone()
        else:
            cursor.close()
            db_close()
            return 11
        cursor.close()
        db_close()
        
        make_list = lambda x: [" " if i == None or i == '' else i for i in x]
        
        user_list = make_list(user_details)
            
        user_tuple = ('user_id','user_name','group_name','first_name','last_name','designation','company','mobile','address','email_id')
        
        user_dict = dict(zip(user_tuple,user_list))
        
        return user_dict
    
    except Exception as e:
        return str(e)
    
def edit_user(u_dict,ug_dict):   
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
            
        updateQuery1 = """UPDATE `users` set `first_name`= \"%(first_name)s\",`last_name`=\"%(last_name)s\",`designation`=\"%(designation)s\", `company_name`=\"%(company)s\", `mobile_no`=\"%(mobile)s\", `address`=\"%(address)s\", `email_id`=\"%(email_id)s\" where `user_id`=\"%(user_id)s\""""%u_dict
        updateQuery2 = """UPDATE `users_groups` set `group_id`=\"%(groups)s\" WHERE `user_id`=\"%(user_id)s\""""%ug_dict
        
        cursor = global_db.cursor()
        group_id = None
  
        cursor.execute(updateQuery1)        
        cursor.execute(updateQuery2)
        
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return str(e)

    
    
def get_group_details():
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        selectQuery = "SELECT  g.`group_id`, g.group_name FROM groups AS g WHERE g.is_deleted <> 1 and g.group_name <> 'Default' "
        
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            group_details = cursor.fetchall()
        cursor.close()
        db_close()
        if len(group_details) < 1 :
            return 1
        else:
#            make_list = lambda x: [" - " if i == None or i == '' else i for i in x]
#            group_details_list = []
#            for group_detail in group_details:
#                group_details_list.append(make_list(group_detail))
            return group_details    
    except Exception as e:
        return 1
    
#print get_group_details()

def add_group(var_dict):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        insQuery = "insert into groups (`group_id`, `group_name`, `description`, `timestamp`, `created_by`, `creation_time`, `is_deleted`, `updated_by`, `role_id`) VALUES (UUID(), \"%(group_name)s\", \"%(description)s\", '0000-00-00 00:00:00', 'SuperAdmin', CURRENT_TIMESTAMP, '0', NULL, \"%(role)s\")"%var_dict
        cursor = global_db.cursor()    
        if cursor.execute(insQuery) != 1:
            cursor.close()
            db_close()
            return 3
        global_db.commit() 
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 1
    

def edit_group(var_dict):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        updateQuery = """UPDATE groups SET `description` = "%(description)s", `updated_by` = 'SuperAdmin', `role_id` = "%(role)s" WHERE group_id = "%(group_id)s" """%var_dict
        cursor = global_db.cursor()
        if cursor.execute(updateQuery) != 1:
            pass
    #        cursor.close()
    #        db_close()
    #        return 3
        global_db.commit() 
        cursor.close()
        db_close()    
        return 0
    except Exception as e:
        return 1


def del_group(groupID,del_users=1):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        
        result = 1    
        delQuery = "DELETE from groups WHERE groups.group_id = \"%s\" "%groupID
        cursor = global_db.cursor()
        if del_users == 0:
            selQuery = "SELECT users_groups.user_id FROM users_groups WHERE users_groups.group_id = \"%s\" "%groupID
            cursor.execute(selQuery)
            user_ids = cursor.fetchall()        
            if len(user_ids) > 0:
                f = lambda user_ids: [ids[0] for ids in user_ids]
                result = del_user(f(user_ids),0)
            else:  
                result = 0
        if del_users == 0 and result != 0:
            return 11                   
                       
        if cursor.execute(delQuery) != 1 :
            pass

        global_db.commit() 
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return str(e)


def del_group_copy(groupID,del_users = 1):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
            
        if del_users == 0 and gpValue == 1:
            delQuery = "UPDATE user_login INNER JOIN users_groups ON user_login.user_id = users_groups.user_id INNER JOIN groups ON users_groups.group_id = groups.group_id SET user_login.is_deleted = 1,groups.is_deleted=1 WHERE users_groups.group_id = \"%s\""%()    
        else:
            delQuery = "DELETE from groups WHERE groups.group_id = \"%s\" "%groupID
        
        delQuery1 = "DELETE from users_groups where group_id = \"%s\" "%groupID
        cursor = global_db.cursor()
        if cursor.execute(delQuery) < 1 :
#            pass
            cursor.close()
            db_close()
            return 2
        if cursor.execute(delQuery) < 1:
#            pass
            cursor.close()
            db_close()
            return 2
        global_db.commit() 
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 1



def get_user_details():
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        selectQuery = "SELECT  ul.`user_id`, ul.user_name,  u.`first_name` , u.`last_name` , u.`designation` , u.`mobile_no` , u.`email_id` FROM user_login AS ul INNER JOIN users AS u WHERE u.user_id = ul.user_id AND ul.is_deleted <> 1"
        
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            user_details = cursor.fetchall()
        cursor.close()
        db_close()
        if len(user_details) < 1 :
            return 1
        else:
            make_list = lambda x: [" - " if i == None or i == '' else i for i in x]
            user_details_list = []
            for user_detail in user_details:
                user_details_list.append(make_list(user_detail))
            return user_details_list
    except Exception as e:
        return 1

#print get_user_details()

      
    
def edit_group_view(group_id):
    db_connect()
    global global_db
    result = 1
    try:
        if global_db.open != 1:
            result = 1
            
        selectQuery = """SELECT g.group_id, g.group_name, g.description, g.role_id FROM groups as g WHERE g.group_id = \"%s\" AND g.is_deleted <> 1"""%group_id
        group_details = ()
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            group_details = cursor.fetchone()
        else:
            cursor.close()
            db_close()
            return 11
        cursor.close()
        db_close()
        
        make_list = lambda x: [" " if i == None or i == '' else i for i in x]
        
        group_list = make_list(group_details)
            
        group_tuple = ('group_id','group_name','description','role_id')
        
        group_dict = dict(zip(group_tuple,group_list))
        
        return group_dict
           
    except Exception as e:
        return 1
#print edit_group_view("76929ad6-f666-11e0-a835-f04da24c7c26")
    
def get_role_list():
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1        
        query = "select `role_name`,`role_id` from roles where `is_deleted` <> 1"
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            roleName_list = cursor.fetchall()
        cursor.close()
        db_close()
        if len(roleName_list) < 1 :
            return 1
        else:
            return roleName_list  
        
    except Exception as e:
        return 1
    
def change_password(var_dict):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
                
        selectQuery = "SELECT user_name FROM user_login WHERE `user_id` = \"%(user_id)s\" and `password`=\"%(old_password)s\" "%var_dict                
        cursor = global_db.cursor()
        if cursor.execute(selectQuery) != 0:
            if cursor.fetchone()[0] == var_dict['user_name']:
                updateQuery = "UPDATE user_login set `password`=\"%(password)s\ WHERE `user_id` = \"%(user_id)s\" "%var_dict
            else:
                cursor.close()
                db_close()
                return 100
        else:
            cursor.close()
            db_close()
            return 100
            
        cursor.execute(updateQuery)
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return 1


def get_hostgroup_info(hg_id):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        
        query = "SELECT `hostgroup_alias`,`updated_by`,`timestamp`,`created_by`,`creation_time` from hostgroups WHERE hostgroup_id = \"%s\""%hg_id
        gpDetail_tuple = ()
        cursor = global_db.cursor()
        if cursor.execute(query) != 0:
            gpDetail_tuple = cursor.fetchone()
        cursor.close()
        db_close()
        if len(gpDetail_tuple) < 1 :
            return 1
        else:
            return gpDetail_tuple
    except Exception as e:
        return str(e)



def get_hostgroup_details():
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1        
        query = "select `hostgroup_id`,`hostgroup_name` from hostgroups where `is_deleted` <> 1"
        cursor = global_db.cursor()
        groupName_list = ()
        if cursor.execute(query) != 0:
            groupName_list = cursor.fetchall()
        cursor.close()
        db_close()
        if len(groupName_list) < 1 :
            return 1
        else:
            return groupName_list
        
    except Exception as e:
        return 1

def show_hostgroups(group_id,all=1):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if all == 0:
            query = "SELECT hg.`hostgroup_id` , hg.`hostgroup_name`, hg.`hostgroup_alias` FROM hostgroups AS hg WHERE hg.hostgroup_id NOT IN ( \
                        SELECT hg_grp.hostgroup_id FROM hostgroups_groups AS hg_grp WHERE hg_grp.`group_id` = '%s' )"%group_id 
        elif group_id == "remain":
            query = "SELECT hg.`hostgroup_id`, hg.`hostgroup_name` , hg.`hostgroup_alias` FROM hostgroups as hg WHERE NOT EXISTS \
                        ( SELECT hg_grp.`hostgroup_id` FROM hostgroups_groups AS hg_grp WHERE hg.`hostgroup_id` = hg_grp.`hostgroup_id` )"
        else:
            query = "SELECT hostgroups.`hostgroup_id`, hostgroups.`hostgroup_name` , hostgroups.`hostgroup_alias` FROM hostgroups_groups INNER JOIN hostgroups ON hostgroups.hostgroup_id = hostgroups_groups.hostgroup_id INNER JOIN groups ON hostgroups_groups.group_id = groups.group_id WHERE groups.group_id = \"%s\""%group_id
        gpHG_tuple = ()
        cursor = global_db.cursor()
        cursor.execute(query)
        gpHG_tuple = cursor.fetchall()
        cursor.close()
        db_close()
        return gpHG_tuple
#        if len(gpHG_tuple) < 1 :
#            return 1
#        else:
##            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
##            gpHG_list = []
##            for gpHG in gpHG_tuple:
##                gpHG_list.append(make_list(gpHG))
#            return gpHG_tuple
    
    except Exception as e:
        return str(e)


def show_groups(hostgroup_id,all=1):
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1
        if all == 0:
            query = "SELECT gp.`group_id` , gp.`group_name` FROM groups AS gp WHERE gp.group_id NOT IN ( \
                        SELECT hg_grp.group_id FROM hostgroups_groups AS hg_grp WHERE hg_grp.`hostgroup_id` = '%s' ) and gp.`group_name`<> 'Default' "%hostgroup_id 
        elif hostgroup_id == "remain":
            query = "SELECT gp.`group_id` , gp.`group_name` FROM groups AS gp WHERE gp.group_id WHERE NOT EXISTS \
                        ( SELECT hg_grp.`group_id` FROM hostgroups_groups AS hg_grp WHERE gp.group_id = hg_grp.`group_id` )"
        else:
            query = "SELECT groups.`group_id`, groups.`group_name` FROM hostgroups_groups INNER JOIN groups ON groups.group_id = hostgroups_groups.group_id INNER JOIN hostgroups ON hostgroups_groups.hostgroup_id = hostgroups.hostgroup_id WHERE hostgroups.hostgroup_id = \"%s\""%hostgroup_id
        gpHG_tuple = ()
        cursor = global_db.cursor()
        cursor.execute(query)
        gpHG_tuple = cursor.fetchall()
        cursor.close()
        db_close()
        return gpHG_tuple
#        if len(gpHG_tuple) < 1 :
#            return 1
#        else:
##            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
##            gpHG_list = []
##            for gpHG in gpHG_tuple:
##                gpHG_list.append(make_list(gpHG))
#            return gpHG_tuple
    
    except Exception as e:
        return str(e)



def add_hg_togroup(hg_ids_list,group_id):
    db_connect()
    global global_db
    try:
        is_ins = 1
        if global_db.open != 1:
            return 1
        f = lambda x: tuple(j[0] for j in x)
        selQuery = "select `hostgroup_id` from hostgroups_groups where group_id = \"%s\" "%group_id
        cursor = global_db.cursor()
        
        cursor.execute(selQuery)
        
        hg_ids_tuple = cursor.fetchall()
        
        f = lambda x: tuple(j[0] for j in x)
        
        hg_ids_tuple = f(hg_ids_tuple)  
             
        insQuery = "insert into hostgroups_groups (`hostgroup_group_id`, `hostgroup_id`, `group_id`) values"
        
        i = 0   
        for hgid in hg_ids_list:
            i += 1
            try:
                hg_ids_tuple.index(hgid)
            except ValueError as e:
                is_ins = 0
                if i == len(hg_ids_list):
                    insQuery += " (uuid(),\"%s\",\"%s\") "%(hgid,group_id)
                else:
                    insQuery += " (uuid(),\"%s\",\"%s\") ,"%(hgid,group_id)
                                                                
        
        if is_ins == 0:
            print "insert is happening"
            cursor.execute(insQuery) 
        else:
            print "insert NOT happening"
        global_db.commit()
        cursor.close()
        db_close()
        return 0
        
    except Exception as e:
        return 1


def move_hg_togroup(hg_ids_list,group_id,old_group_id):
    db_connect()
    global global_db
    try:
        insQuery = ""
        is_ins = 1
        if global_db.open != 1:
            return 1
        f = lambda x: tuple(j[0] for j in x)
        selQuery = "select `hostgroup_id` from hostgroups_groups where group_id = \"%s\" "%group_id
        cursor = global_db.cursor()
        
        cursor.execute(selQuery)
        
        hg_ids_tuple = cursor.fetchall()
        
        f = lambda x: tuple(j[0] for j in x)
        
        hg_ids_tuple = f(hg_ids_tuple)  
             
        insQuery = "insert into hostgroups_groups (`hostgroup_group_id`, `hostgroup_id`, `group_id`) values"
        
        i = 0   
        comma_flag = 0
        for hgid in hg_ids_list:
            i += 1
            try:
                hg_ids_tuple.index(hgid)
            except ValueError as e:
                is_ins = 0
                if comma_flag == 0:
                    insQuery += " (uuid(),\"%s\",\"%s\") "%(hgid,group_id)
                    comma_flag = 1
                else:
                    insQuery += " , (uuid(),\"%s\",\"%s\") "%(hgid,group_id)
                                                                
        if is_ins == 0:
            print "insert is happening"
            cursor.execute(insQuery) 
        else:
            print "insert NOT happening"
        global_db.commit()
        cursor.close()
        
        del_result = del_hg_fromgroup(hg_ids_list, old_group_id, 0)
        
        if del_result != 0:
            return "Not deleted but moved sucessfully"
        return 0
    
    except Exception as e:
        return str(e)+insQuery


def move_group_tohg(hg_ids_list,group_id,old_group_id):
    db_connect()
    global global_db
    try:
        is_ins = 1
        if global_db.open != 1:
            return 1
        f = lambda x: tuple(j[0] for j in x)
        selQuery = "select `group_id` from hostgroups_groups where hostgroup_id = \"%s\" "%group_id
        cursor = global_db.cursor()
        
        cursor.execute(selQuery)
        
        hg_tuple = cursor.fetchall()
        
        f = lambda x: tuple(j[0] for j in x)
        
        hg_ids_tuple = f(hg_tuple)  
             
        insQuery = "insert into hostgroups_groups (`hostgroup_group_id`, `group_id`, `hostgroup_id`) values"
        comma_flag = 0
        i = 0   
        for hgid in hg_ids_list:
            i += 1
            try:
                hg_ids_tuple.index(hgid)
            except ValueError as e:
                is_ins = 0
                if comma_flag == 0:
                    insQuery += " (uuid(),\"%s\",\"%s\") "%(hgid,group_id)
                    comma_flag = 1
                else:
                    insQuery += " , (uuid(),\"%s\",\"%s\") "%(hgid,group_id)
                                                                
        
        if is_ins == 0:
            print "insert is happening"
            cursor.execute(insQuery) 
        else:
            print "insert NOT happening"
            
        global_db.commit()
        cursor.close()
        
        del_result = del_gp_fromhostgroup(hg_ids_list, old_group_id, 0)
        
        if del_result != 0:
            return "Not deleted but moved sucessfully"
        return 0
    
    except Exception as e:
        return str(e)
    
   
def add_gp_tohostgroup(hg_ids_list,group_id):
    db_connect()
    global global_db
    try:
        is_ins = 1
        if global_db.open != 1:
            return 1
        f = lambda x: tuple(j[0] for j in x)
        selQuery = "select `group_id` from hostgroups_groups where hostgroup_id = \"%s\" "%group_id
        cursor = global_db.cursor()
        
        cursor.execute(selQuery)
        
        hg_tuple = cursor.fetchall()
        
        f = lambda x: tuple(j[0] for j in x)
        
        hg_ids_tuple = f(hg_tuple)  
             
        insQuery = "insert into hostgroups_groups (`hostgroup_group_id`, `group_id`, `hostgroup_id`) values"
        
        i = 0   
        for hgid in hg_ids_list:
            i += 1
            try:
                hg_ids_tuple.index(hgid)
            except ValueError as e:
                is_ins = 0
                if i == len(hg_ids_list):
                    insQuery += " (uuid(),\"%s\",\"%s\") "%(hgid,group_id)
                else:
                    insQuery += " (uuid(),\"%s\",\"%s\") ,"%(hgid,group_id)
                                                                
        
        if is_ins == 0:
            print "insert is happening"
            cursor.execute(insQuery) 
        else:
            print "insert NOT happening"
            
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return str(e)
    
    
    
def del_gp_fromhostgroup(gp_ids_list,hostgroup_id,flag=1):
    if flag == 1:
        db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1

        delQuery = "delete from hostgroups_groups where "
        i = 0
        for gp_id in gp_ids_list:
            i +=1
            if len(gp_ids_list) == i:
                delQuery += "`hostgroup_id` = \"%s\" AND `group_id` = \"%s\" "%(hostgroup_id,gp_id)         
            else:
                delQuery += "`hostgroup_id` = \"%s\" AND `group_id` = \"%s\" OR "%(hostgroup_id,gp_id)
                                                                
        cursor = global_db.cursor()
        
        if cursor.execute(delQuery) < 1:
            cursor.close()
            db_close()
            return 3
    
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return str(e)

    
def del_hg_fromgroup(hg_ids_list,group_id,flag=1):
    if flag == 1:
        db_connect()
        
    global global_db
    try:
        if global_db.open != 1:
            return 1

        delQuery = "delete from hostgroups_groups where "
        i = 0
        for hg_id in hg_ids_list:
            i +=1
            if len(hg_ids_list) == i:
                delQuery += "`hostgroup_id` = \"%s\" AND `group_id` = \"%s\" "%(hg_id,group_id)         
            else:
                delQuery += "`hostgroup_id` = \"%s\" AND `group_id` = \"%s\" OR "%(hg_id,group_id)
                                                                
        cursor = global_db.cursor()
        
        if cursor.execute(delQuery) < 1:
            cursor.close()
            db_close()
            return 3
    
        global_db.commit()
        cursor.close()
        db_close()
        return 0
    except Exception as e:
        return str(e)
  
def get_hostgroup_list():       
    db_connect()
    global global_db
    try:
        if global_db.open != 1:
            return 1        
        query = "select `hostgroup_name`,`hostgroup_id` from hostgroups where `is_deleted` <> 1"
        cursor = global_db.cursor()
        groupName_list = ()
        if cursor.execute(query) != 0:
            groupName_list = cursor.fetchall()
        cursor.close()
        db_close()
        if len(groupName_list) < 1 :
            return 1
        else:
            return groupName_list
        
    except Exception as e:
        return 1  
