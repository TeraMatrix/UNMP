#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@version: 0.1
@note: All database and model's functions Related with Inventory.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
from unmp_model import *
from utility import ErrorMessages, Validation, HostState, NagiosConfiguration, SystemSetting, DiscoveryName, PingDiscovery, SnmpDiscovery, UpnpDiscovery, UNMPDeviceType
from unmp_config import SystemConfig
from sqlalchemy import and_, or_, desc, asc
from odu_controller import OduReconcilation
from swt4_controller import create_default_configprofile_for_swt4
from idu_profiling_bll import IduReconcilation
from ccu_profiling_bll import CCUReconcilation
from common_bll import EventLog
from pysnmp_module import pysnmp_set
from pysnmp_v1 import pysnmp_seter
from pysnmp_v1 import snmp_ping as snmp_ping_ccu
from py_module import snmp_ping
from license_bll import LicenseBll
from ap_profiling_bll import Reconciliation
import MySQLdb
import random
from json import JSONEncoder
import time
from datetime import datetime
from sqlalchemy.orm import aliased
# search by wnc for new nagios code
from nagios_bll import NagiosBll
# flag for nagios
# if set to 1 means call NagiosBll
# if set to 0 means call old nagios functions
flag_nagios_call = 0

import defaults
nms_instance = defaults.site

class HostgroupBll(object):
    def get_data_table_sqlalchemy(self, a_columns, table_columns, table_classes, table_join, other_conditions, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, req_vars, join_conditions=[], group_by=False, diff_count=3):
        i_total = 0
        i_filtered_total = 0
        Session = sessionmaker(bind=engine)
        try:
            session = Session()
            query_column = []			# Query Column to store query fields
            query = None				# Query object default is null
            for class_i in range(0, len(table_classes)):
                if len(table_columns) > class_i:
                    for column_i in range(0, len(table_columns[class_i])):
                        query_column.append(getattr(table_classes[class_i], table_columns[
                                            class_i][column_i]))  # append table fileds objects

            for class_i in range(0, len(table_classes)):
                if class_i == 0:
                    query = session.query(*tuple(
                        query_column))		# creating query to pass the table fields
                elif class_i > 0:
                    if len(table_join) > class_i - 1:
                        if table_join[class_i - 1] == "join":		# creating type of joins in tables
                            query = query.join(getattr(table_classes[
                                               class_i - 1], table_classes[class_i].__tablename__))
                        elif table_join[class_i - 1] == "outerjoin":
                            query = query.outerjoin(getattr(table_classes[
                                                    class_i - 1], table_classes[class_i].__tablename__))
                        elif table_join[class_i - 1] == "user_defined_join":
                            if len(join_conditions) > class_i - 1:
                                join_conditions_list = []
                                for join_condition in join_conditions[class_i - 1]:
                                    if isinstance(join_condition, dict):
                                        if isinstance(join_condition.get("join_with", None), str) or isinstance(join_condition.get("join_with", None), int) or isinstance(join_condition.get("join_with", None), long) or isinstance(join_condition.get("join_with", None), float):
                                            join_conditions_list.append(getattr(
                                                table_classes[class_i], join_condition["table_column"]) == join_condition["join_with"])
                                        elif isinstance(join_condition.get("join_with", None), dict):
                                            join_conditions_list.append(getattr(table_classes[class_i], join_condition["table_column"])
                                                                        == getattr(join_condition["join_with"]["table_class"], join_condition["join_with"]["table_column"]))

                                if len(join_conditions_list) == 0:
                                    query = query.join(table_classes[class_i])
                                elif len(join_conditions_list) == 1:
                                    query = query.join(
                                        table_classes[class_i], join_conditions_list[0])
                                else:
                                    query = query.join(
                                        table_classes[class_i], and_(*tuple(join_conditions_list)))
                        elif table_join[class_i - 1] == "user_defined_outerjoin":
                            if len(join_conditions) > class_i - 1:
                                join_conditions_list = []
                                for join_condition in join_conditions[class_i - 1]:
                                    if isinstance(join_condition, dict):
                                        if isinstance(join_condition.get("join_with", None), str) or isinstance(join_condition.get("join_with", None), int) or isinstance(join_condition.get("join_with", None), long) or isinstance(join_condition.get("join_with", None), float):
                                            join_conditions_list.append(getattr(
                                                table_classes[class_i], join_condition["table_column"]) == join_condition["join_with"])
                                        elif isinstance(join_condition.get("join_with", None), dict):
                                            join_conditions_list.append(getattr(table_classes[class_i], join_condition["table_column"])
                                                                        == getattr(join_condition["join_with"]["table_class"], join_condition["join_with"]["table_column"]))

                                if len(join_conditions_list) == 0:
                                    query = query.outerjoin(
                                        table_classes[class_i])
                                elif len(join_conditions_list) == 1:
                                    query = query.outerjoin(
                                        table_classes[class_i], join_conditions_list[0])
                                else:
                                    query = query.outerjoin(table_classes[class_i], and_(
                                        *tuple(join_conditions_list)))
                        else:
                            pass
                            # query =
                            # query.join(getattr(table_classes[class_i-1],table_classes[class_i].__tablename__))
                    else:
                        pass
                        # query =
                        # query.join(getattr(table_classes[class_i-1],table_classes[class_i].__tablename__))

            # other conditions
            or_condition = []
            and_condition = []
            for other_condition in other_conditions:
                if isinstance(other_condition, dict):
                    if other_condition.get("type", None) == "like":
                        if other_condition.get("table_class", None) != None and other_condition.get("table_column", None) != None:
                            if other_condition.get("rel", None) == "and":
                                and_condition.append(
                                    getattr(other_condition["table_class"],
                                            other_condition["table_column"]).like(other_condition.get("value", "%%")))
                            else:
                                or_condition.append(
                                    getattr(other_condition["table_class"],
                                            other_condition["table_column"]).like(other_condition.get("value", "%%")))

                    elif other_condition.get("type", None) == "equal":
                        if other_condition.get("table_class", None) != None and other_condition.get("table_column", None) != None:
                            if other_condition.get("rel", None) == "and":
                                and_condition.append(
                                    getattr(other_condition["table_class"],
                                            other_condition["table_column"]) == other_condition.get("value", None))
                            else:
                                or_condition.append(
                                    getattr(other_condition["table_class"],
                                            other_condition["table_column"]) == other_condition.get("value", None))

                    elif other_condition.get("type", None) == "in":
                        if other_condition.get("table_class", None) != None and other_condition.get("table_column", None) != None:
                            if other_condition.get("rel", None) == "and":
                                and_condition.append(
                                    getattr(other_condition["table_class"],
                                            other_condition["table_column"]).in_(other_condition.get("value", [])))
                            else:
                                or_condition.append(
                                    getattr(other_condition["table_class"],
                                            other_condition["table_column"]).in_(other_condition.get("value", [])))
                    elif other_condition.get("type", None) == "not in":
                        if other_condition.get("table_class", None) != None and other_condition.get("table_column", None) != None:
                            if other_condition.get("rel", None) == "and":
                                and_condition.append(
                                    ~getattr(other_condition["table_class"],
                                             other_condition["table_column"]).in_(other_condition.get("value", [])))
                            else:
                                or_condition.append(~getattr(other_condition["table_class"], other_condition[
                                                    "table_column"]).in_(other_condition.get("value", [])))

            if len(and_condition) == 0:
                if len(or_condition) == 0:
                    pass
                elif len(or_condition) == 1:
                    query = query.filter(or_condition[0])
                else:
                    query = query.filter(or_(*tuple(or_condition)))
            elif len(and_condition) == 1:
                if len(or_condition) == 0:
                    query = query.filter(and_condition[0])
                elif len(or_condition) == 1:
                    query = query.filter(
                        and_(and_condition[0], or_condition[0]))
                else:
                    query = query.filter(
                        and_(and_condition[0], or_(*tuple(or_condition))))
            else:
                if len(or_condition) == 0:
                    query = query.filter(and_(*tuple(and_condition)))
                elif len(or_condition) == 1:
                    query = query.filter(
                        and_(or_(or_condition[0]), *tuple(and_condition)))
                else:
                    query = query.filter(and_(
                        or_(*tuple(or_condition)), *tuple(and_condition)))

            if group_by:
                query = query.group_by(group_by)
            i_total = query.count()			# fetch total number of records

            # Filtering
            is_individual_filter = False
            if is_individual_filter == False:
                s_search = s_search
                if s_search != "":
                    filter_column = []
                    for class_i in range(0, len(table_classes)):  # creating filtring in query
                        if len(table_columns) > class_i:
                            for column_i in range(0, len(table_columns[class_i])):
                                filter_column.append(
                                    getattr(table_classes[class_i],
                                            table_columns[class_i][column_i]).like("%" + s_search + "%"))
                    if len(filter_column) > 0:
                        query = query.filter(or_(*tuple(filter_column)))

            # ordering
            s_order = "ORDER BY  "
            # order_dict={}
            col_number = 1
            temp_li = []
            for i in range(0, int(req_vars.get("iSortingCols", 0))):		# creating orderby in query
                i_sort_col_i = int(req_vars.get("iSortCol_%s" % i, -1))
                b_sortable_ = req_vars.get(
                    "bSortable_%s" % i_sort_col_i, "true")
                temp_li.append([i_sort_col_i, b_sortable_])
                if b_sortable_ == "true":
                    s_sort_dir_i = req_vars.get("sSortDir_%s" % i, "asc")
                    for class_i in range(0, len(table_classes)):
                        temp_li.append(class_i)
                        if len(table_columns) > class_i:
                            for column_i in range(0, len(table_columns[class_i])):
                                temp_li.append([a_columns[i_sort_col_i],
                                               col_number, i_sort_col_i, table_columns[class_i][column_i]])
                                if table_columns[class_i][column_i] == a_columns[i_sort_col_i] and abs(i_sort_col_i - col_number) <= diff_count:
                                    if s_sort_dir_i == "asc":
                                        # order_dict["table_name"]=getattr(table_classes[class_i],table_columns[class_i][column_i])
                                        # order_dict["direction"]="asc"
                                        query = query.order_by(asc(
                                            getattr(table_classes[class_i], table_columns[class_i][column_i])))
                                    else:
                                        # order_dict["table_name"]=getattr(table_classes[class_i],table_columns[class_i][column_i])
                                        # order_dict["direction"]="desc"
                                        query = query.order_by(
                                            desc(getattr(table_classes[class_i], table_columns[class_i][column_i])))
                                col_number += 1
#	                    if order_dict["direction"]=="asc":
#	                        query = query.order_by(asc(order_dict["table_name"]))
#	                    else:
#	                        query = query.order_by(desc(order_dict["table_name"]))
                                        # query = query.order_by(desc(getattr(table_classes[class_i],table_columns[class_i][column_i])))
            # query =
            # query.order_by(Hosts.host_alias).order_by(Hosts.ip_address)
            i_filtered_total = query.count(
            )		# fetch record count after filtering applied in query

            # Paging
            s_limit = ""
            i_display_start = int(
                i_display_start)  # req.vars.get("iDisplayStart",None)
            i_display_length = int(
                i_display_length)  # req.vars.get("iDisplayLength",None)
            if (i_display_start != None and i_display_length != '-1'):  # creating paging in query
                query = query.limit(
                    int(i_display_length)).offset(int(i_display_start))

            # fetch records from database
            r_result = query.all()

            result_data = []
            for a_row in r_result:
                row = []
                for i in range(0, len(a_columns)):
                    row.append(a_row[i])
                    # if a_columns[i] == "city":
                        # Special output formatting for 'city' column
                    # row.append(a_row[i] == "Ajmer" and a_row[i] + "(H)" or
                    # a_row[i])

                    # elif a_columns[i] == "subject_name":
                        # Special output formatting for 'subject_name' column
                    #    row.append(a_row[i] == None and "NA" or a_row[i])

                    # elif a_columns[i] != " ":
                    #    row.append(a_row[i])
                result_data.append(row)

            # Output
            output = {
                "sEcho": int(sEcho),
                "iTotalRecords": i_total,
                "iTotalDisplayRecords": i_filtered_total,
                "aaData": r_result,
                "query": "",  # str(query),#str(temp_li),#str(query),
                "i_display_start": i_display_start
            }
            # sqlalche_obj.close()
            session.close()
            return output

        except Exception, e:
            output = {
                "sEcho": 0,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "i_display_start": 0,
                "query": str(e),
                "sds": ""  # str(query)
            }
            return output

    def grid_view(self, hostgroup_id_list, flag=1):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if flag:
                hostgroup = session.query(Hostgroups.hostgroup_id, Hostgroups.hostgroup_name, Hostgroups.hostgroup_alias, Hostgroups.is_default, Groups.group_name).outerjoin(
                    HostgroupsGroups, Hostgroups.hostgroup_id == HostgroupsGroups.hostgroup_id).outerjoin(Groups, HostgroupsGroups.group_id == Groups.group_id).filter(and_(Hostgroups.is_deleted == 0, Hostgroups.hostgroup_id.in_(hostgroup_id_list))).order_by(Hostgroups.hostgroup_name).all()          # execute query and fetch data
            else:
                hostgroup = session.query(Hostgroups.hostgroup_id, Hostgroups.hostgroup_name, Hostgroups.hostgroup_alias, Hostgroups.is_default, Groups.group_name).outerjoin(
                    HostgroupsGroups, Hostgroups.hostgroup_id == HostgroupsGroups.hostgroup_id).outerjoin(Groups, HostgroupsGroups.group_id == Groups.group_id).filter(Hostgroups.is_deleted == 0).order_by(Hostgroups.hostgroup_name).all()          # execute query and fetch data
            return hostgroup
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def grid_view_number_of_hosts(self, hostgroup_id_list, flag=1):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if flag:
                hostgroup = session.query(Hostgroups.hostgroup_id, Hostgroups.hostgroup_name, Hostgroups.hostgroup_alias, func.count(Hosts.device_type_id), DeviceType.device_name).outerjoin(HostsHostgroups, Hostgroups.hostgroup_id == HostsHostgroups.hostgroup_id).outerjoin(
                    Hosts, HostsHostgroups.host_id == Hosts.host_id).outerjoin(DeviceType, Hosts.device_type_id == DeviceType.device_type_id).filter(and_(Hostgroups.is_deleted == 0, Hosts.is_deleted == 0, Hosts.host_state_id == 'e', Hostgroups.hostgroup_id.in_(hostgroup_id_list))).group_by(Hosts.device_type_id, Hostgroups.hostgroup_id).order_by(Hostgroups.hostgroup_name).all()          # execute query and fetch data
            else:
                hostgroup = session.query(Hostgroups.hostgroup_id, Hostgroups.hostgroup_name, Hostgroups.hostgroup_alias, func.count(Hosts.device_type_id), DeviceType.device_name).outerjoin(
                    HostsHostgroups, Hostgroups.hostgroup_id == HostsHostgroups.hostgroup_id).outerjoin(Hosts, HostsHostgroups.host_id == Hosts.host_id).outerjoin(DeviceType, Hosts.device_type_id == DeviceType.device_type_id).filter(and_(Hostgroups.is_deleted == 0, Hosts.is_deleted == 0, Hosts.host_state_id == 'e')).group_by(Hosts.device_type_id, Hostgroups.hostgroup_id).order_by(Hostgroups.hostgroup_name).all()

            return hostgroup
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def get_hostgroup_by_id(self, hostgroup_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hostgroups = session.query(
                Hostgroups.hostgroup_id, Hostgroups.hostgroup_name, Hostgroups.hostgroup_alias, Hostgroups.is_default, Hostgroups.timestamp, Hostgroups.created_by, Hostgroups.creation_time,
                Hostgroups.updated_by).filter(Hostgroups.hostgroup_id == hostgroup_id).all()          # execute query and fetch data
            if len(hostgroups) == 1:
                return hostgroups[0]
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def add(self, hostgroup_name, hostgroup_alias, timestamp, created_by, creation_time, is_deleted, updated_by, is_default, nms_instance, group_name):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            lic = LicenseBll()
            if lic.check_license_for_hostgroup() == True:
                if self.validate(hostgroup_name, hostgroup_alias):
                    if self.is_duplicate_hostgroup_for_add(hostgroup_name, hostgroup_alias):
                        hostgroup = Hostgroups(
                            hostgroup_name, hostgroup_alias, timestamp,
                            created_by, creation_time, is_deleted, updated_by, is_default)
                        session.add(hostgroup)
                        session.flush()
                        session.refresh(hostgroup)
                        hg_id = hostgroup.hostgroup_id
                        session.commit()

                        db = MySQLdb.connect(
                            *SystemConfig.get_mysql_credentials())
                        cursor = db.cursor()
                        if group_name.lower() == "superadmin":
                            sel_query = "select group_id from groups where group_name = 'SuperAdmin'"
                        else:
                            sel_query = "select group_id from groups where group_name = 'SuperAdmin' or group_name = '%s'" % group_name
                        cursor.execute(sel_query)
                        result_tuple = cursor.fetchall()
                        if len(result_tuple) > 0:
                            if len(result_tuple) == 2:
                                insert_query = "insert into hostgroups_groups (`hostgroup_id`, `group_id`) values ('%s','%s'),('%s','%s')" % (
                                    str(hg_id), result_tuple[0][0], str(hg_id), result_tuple[1][0])
                            else:
                                insert_query = "insert into hostgroups_groups (`hostgroup_id`, `group_id`) values ('%s','%s')" % (
                                    str(hg_id), result_tuple[0][0])
                            cursor.execute(insert_query)
                            db.commit()
                        cursor.close()
                        db.close()
                        if(flag_nagios_call == 0):
                            ncbll = NagioConfigurationBll()
                            wnc = ncbll.write_nagios_config(nms_instance)
                            condition_nagios = isinstance(wnc, bool)
                        else:
                            n_bll = NagiosBll()
                            wnc = n_bll.add_new_hostgroup(
                                hostgroup_name, hostgroup_alias)
                            condition_nagios = wnc["success"] == 0
                        if (condition_nagios):
                            if flag_nagios_call:
                                SystemSetting.reload_nagios_config()
                            el = EventLog()
                            el.log_event("New Hostgroup named " +
                                         hostgroup_name + " added in unmp system", created_by)
                            return hostgroup.hostgroup_id
                        else:
                            err = ErrorMessages()
                            err.error_msg = err.nagios_config_error
                            return err
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.duplicate_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.validation_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.license_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def edit(self, hostgroup_id, hostgroup_name, hostgroup_alias, timestamp, is_deleted, updated_by, is_default, nms_instance):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if self.validate(hostgroup_name, hostgroup_alias):
                if self.is_duplicate_hostgroup_for_edit(hostgroup_id, hostgroup_name, hostgroup_alias):
                    hostgroups = session.query(Hostgroups).filter(
                        Hostgroups.hostgroup_id == hostgroup_id).all()
                    if len(hostgroups) == 1:
                        hostgroup = hostgroups[0]
                        hostgroup.hostgroup_name = hostgroup_name
                        hostgroup.hostgroup_alias = hostgroup_alias
                        hostgroup.timestamp = timestamp
                        hostgroup.is_deleted = is_deleted
                        hostgroup.updated_by = updated_by
                        hostgroup.is_default = is_default
                        session.commit()
                        if(flag_nagios_call == 0):
                            ncbll = NagioConfigurationBll()
                            wnc = ncbll.write_nagios_config(nms_instance)
                            condition_nagios = isinstance(wnc, bool)
                        else:
                            ncbll = NagiosBll()
                            wnc = n_bll.edit_old_hostgroup(
                                old_hostgroup_name, hostgroup_name, hostgroup_alias)
                            condition_nagios = wnc["success"] == 0
                        # ncbll = NagioConfigurationBll()
                        # wnc = ncbll.write_nagios_config(nms_instance)
                        if condition_nagios:
                            if flag_nagios_call:
                                SystemSetting.reload_nagios_config()
                            el = EventLog()
                            el.log_event(
                                "Hostgroup %s updated successfully " % (hostgroup_name), updated_by)
                            return hostgroup.hostgroup_id
                        else:
                            err = ErrorMessages()
                            err.error_msg = err.nagios_config_error
                            return err
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.no_record_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.duplicate_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def delete(self, hostgroup_ids, nms_instance, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            default_hostgroup_id = None
            default_hostgroup_ids = session.query(Hostgroups.hostgroup_id).filter(
                Hostgroups.is_default == 1).all()          # execute query and fetch data
            for hg_id in default_hostgroup_ids:
                default_hostgroup_id = hg_id[0]
            hosts = session.query(HostsHostgroups.host_id).filter(
                HostsHostgroups.hostgroup_id.in_(hostgroup_ids)).all()

            hostgroups = session.query(Hostgroups).filter(Hostgroups.hostgroup_id.in_(
                hostgroup_ids)).all()          # execute query and fetch data
            hostgroup_count = len(hostgroups)
            if hostgroup_count > 0:
                el = EventLog()
                wnc = {}
                for hg in hostgroups:
                    el.log_event("Hostgroup %s Deleted." %
                                 (hg.hostgroup_alias), updated_by)
                    if(flag_nagios_call == 1):
                        n_bll = NagiosBll()
                        wnc = n_bll.delete_old_hostgroup(hg.hostgroup_name)
                        condition_nagios = wnc["success"] == 0
                    session.delete(hg)
                session.commit()
                if default_hostgroup_id != None:
                    for host in hosts:
                        hostgroup_obj = HostsHostgroups(
                            host[0], default_hostgroup_id)
                        session.add(hostgroup_obj)
                    session.commit()
#                ncbll = NagioConfigurationBll()
#                wnc = ncbll.write_nagios_config(nms_instance)
                if(flag_nagios_call == 0):
                    ncbll = NagioConfigurationBll()
                    wnc = ncbll.write_nagios_config(nms_instance)
                    condition_nagios = isinstance(wnc, bool)
                if (condition_nagios):
                    if flag_nagios_call:
                        SystemSetting.reload_nagios_config()
                    return hostgroup_count
                else:
                    err = ErrorMessages()
                    err.error_msg = err.nagios_config_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def validate(self, hostgroup_name, hostgroup_alias):
        if Validation.no_space(hostgroup_name) and Validation.is_alpha_numeric(hostgroup_name) and Validation.is_required(hostgroup_name) and Validation.is_required(hostgroup_alias) and Validation.is_alpha_numeric(hostgroup_alias):
            return True
        else:
            return False

    def is_duplicate_hostgroup_for_add(self, hostgroup_name, hostgroup_alias):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hostgroup_count = session.query(Hostgroups).filter(
                or_(Hostgroups.hostgroup_name == hostgroup_name, Hostgroups.hostgroup_alias == hostgroup_alias)).count()
            if hostgroup_count == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()                     # close the session object

    def is_duplicate_hostgroup_for_edit(self, hostgroup_id, hostgroup_name, hostgroup_alias):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hostgroup_count = session.query(Hostgroups).filter(and_(Hostgroups.hostgroup_id != hostgroup_id, or_(
                Hostgroups.hostgroup_name == hostgroup_name, Hostgroups.hostgroup_alias == hostgroup_alias))).count()
            if hostgroup_count == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()                     # close the session object


class DiscoveryBll(object):
    def delete_discovered_host(self, discovery_type, host_id, updated_by):
        tcp_ne_id = []
        discovered_host_id = []
        if len(discovery_type) == len(host_id):
            for i in range(0, len(discovery_type)):
                if discovery_type[i] == "TCP":
                    tcp_ne_id.append(int(host_id[i]))
                else:
                    discovered_host_id.append(host_id[i])
            Session = sessionmaker(
                bind=engine)     # making session of our current database
            try:
                session = Session(
                )                 # creating new session object
                tcp_host = session.query(TcpDiscovery).filter(TcpDiscovery.ne_id.in_(
                    tcp_ne_id)).all()          # execute query and fetch data
                discovered_host = session.query(DiscoveredHosts).filter(DiscoveredHosts.discovered_host_id.in_(
                    discovered_host_id)).all()          # execute query and fetch data
                tcp_host_count = len(tcp_host) + len(discovered_host)
                if tcp_host_count > 0:
                    el = EventLog()
                    for th in tcp_host:
                        el.log_event(
                            "TCP Discovered Host '%s' Deleted." % (th.ip_address), updated_by)
                        session.delete(th)
                    for dh in discovered_host:
                        el.log_event(
                            "Discovered Host '%s' Deleted." % (dh.ip_address), updated_by)
                        session.delete(dh)
                    session.commit()
                else:
                    err = ErrorMessages()
                    err.error_msg = err.no_record_error
                    return err

            except Exception, e:
                err = ErrorMessages()
                err.error_msg = err.db_error
                return err
            finally:
                session.close()                     # close the session object
        else:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err

    def ping_default_details(self):
        ping_details = SystemConfig.get_ping_details()
        ping_details_dic = {
            "ping_ip_base": str(ping_details["ping_ip_base"]),
            "ping_ip_base_start": str(ping_details["ping_ip_base_start"]),
            "ping_ip_base_end": str(ping_details["ping_ip_base_end"]),
            "ping_timeout": str(ping_details["ping_timeout"]),
            "ping_service_mng": str(ping_details["ping_service_mng"])
        }
        return {"success": 0, "result": ping_details_dic}

    def ping_discovery(self, base_ip, base_ip_start, base_ip_end, timeout, service_mngt, timestamp, created_by, creation_time, updated_by, is_deleted):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if self.ping_validate(base_ip, base_ip_start, base_ip_end, timeout, service_mngt):
                discovery = Discovery(DiscoveryName.ping, (base_ip + "." + base_ip_start), (
                    base_ip + "." + base_ip_end), timeout, None, None, None, None, None, service_mngt, 0, timestamp, created_by, creation_time, updated_by, is_deleted)
                session.add(discovery)
                session.commit()
                el = EventLog()
                el.log_event("Ping Discovery Initiated.", updated_by)
                return discovery.discovery_id
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def ping_validate(self, base_ip, base_ip_start, base_ip_end, timeout, service_mngt):
        if Validation.is_valid_ip(base_ip + "." + base_ip_start) and Validation.is_valid_ip(base_ip + "." + base_ip_end) and Validation.is_required(base_ip) and Validation.is_required(base_ip_end) and Validation.is_required(base_ip_start) and Validation.is_required(timeout) and Validation.is_required(service_mngt) and Validation.is_number(base_ip_start) and Validation.is_number(base_ip_end) and Validation.is_number(timeout):
            return True
        else:
            return False

    def snmp_default_details(self):
        snmp_details = SystemConfig.get_snmp_details()
        snmp_details_dic = {
            "snmp_ip_base": str(snmp_details["snmp_ip_base"]),
            "snmp_ip_base_start": str(snmp_details["snmp_ip_base_start"]),
            "snmp_ip_base_end": str(snmp_details["snmp_ip_base_end"]),
            "snmp_timeout": str(snmp_details["snmp_timeout"]),
            "snmp_service_mng": str(snmp_details["snmp_service_mng"]),
            "snmp_community": str(snmp_details["snmp_community"]),
            "snmp_port": str(snmp_details["snmp_port"]),
            "snmp_version": str(snmp_details["snmp_version"])
        }
        return {"success": 0, "result": snmp_details_dic}

    def snmp_discovery(self, base_ip, base_ip_start, base_ip_end, timeout, snmp_community, snmp_port, snmp_version, service_mngt, timestamp, created_by, creation_time, updated_by, is_deleted):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if self.snmp_validate(base_ip, base_ip_start, base_ip_end, timeout, snmp_community, snmp_port, snmp_version, service_mngt):
                # discovery_type_id,ip_start_range,ip_end_range,timeout,snmp_community,snmp_port,snmp_version,sdm_device_list,scheduling_id,service_management,done_percent,timestamp,created_by,creation_time,updated_by,is_deleted
                discovery = Discovery(DiscoveryName.snmp, (base_ip + "." + base_ip_start), (
                    base_ip + "." + base_ip_end), timeout, snmp_community, snmp_port, snmp_version, None, None, service_mngt, 0, timestamp, created_by, creation_time, updated_by, is_deleted)
                session.add(discovery)
                session.commit()
                el = EventLog()
                el.log_event("SNMP Discovery Initiated.", updated_by)
                return discovery.discovery_id
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def snmp_validate(self, base_ip, base_ip_start, base_ip_end, timeout, snmp_community, snmp_port, snmp_version, service_mngt):
        if Validation.is_valid_ip(base_ip + "." + base_ip_start) and Validation.is_valid_ip(base_ip + "." + base_ip_end) and Validation.is_required(base_ip) and Validation.is_required(base_ip_end) and Validation.is_required(base_ip_start) and Validation.is_required(timeout) and Validation.is_required(service_mngt) and Validation.is_number(base_ip_start) and Validation.is_number(base_ip_end) and Validation.is_number(timeout) and Validation.is_required(snmp_port) and Validation.is_number(snmp_port) and Validation.is_required(snmp_community) and Validation.is_required(snmp_version) and Validation.is_alpha_numeric(snmp_community) and Validation.is_alpha_numeric(snmp_version):
            return True
        else:
            return False

    def upnp_default_details(self):
        upnp_details = SystemConfig.get_upnp_details()
        upnp_details_dic = {
            "upnp_timeout": str(upnp_details["upnp_timeout"]),
            "upnp_service_mng": str(upnp_details["upnp_service_mng"])
        }
        return {"success": 0, "result": upnp_details_dic}

    def upnp_discovery(self, timeout, service_mngt, timestamp, created_by, creation_time, updated_by, is_deleted):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if self.upnp_validate(timeout, service_mngt):
                # discovery_type_id,ip_start_range,ip_end_range,timeout,snmp_community,snmp_port,snmp_version,sdm_device_list,scheduling_id,service_management,done_percent,timestamp,created_by,creation_time,updated_by,is_deleted
                discovery = Discovery(
                    DiscoveryName.upnp, None, None, timeout, None, None, None, None, None, service_mngt, 0,
                    timestamp, created_by, creation_time, updated_by, is_deleted)
                session.add(discovery)
                session.commit()
                el = EventLog()
                el.log_event("UNMP Discovery Initiated.", updated_by)
                return discovery.discovery_id
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def upnp_validate(self, timeout, service_mngt):
        if Validation.is_required(timeout) and Validation.is_required(service_mngt) and Validation.is_number(timeout):
            return True
        else:
            return False

    def add_discovered_host(self, discovery_id, host_alias, ip_address, device_type_id, mac_address):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            discovered_host = DiscoveredHosts(
                discovery_id, host_alias, ip_address, device_type_id, mac_address)
            session.add(discovered_host)
            session.commit()
            return discovered_host.discovered_host_id
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def run_ping_discovery(self, discovery_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            discovery = session.query(Discovery.ip_start_range, Discovery.ip_end_range, Discovery.timeout).filter(
                Discovery.discovery_id == discovery_id).all()          # execute query and fetch data
            if len(discovery) == 1:
                dis = discovery[0]
                start_range = dis.ip_start_range
                end_range = dis.ip_end_range
                timeout = dis.timeout
                pd = PingDiscovery()
                pd.ping_function(discovery_id, start_range,
                                 end_range, timeout, DiscoveryBll)
                discovery = session.query(Discovery).filter(
                    Discovery.discovery_id == discovery_id).all()          # execute query and fetch data
                if len(discovery) > 0:
                    discovery[0].is_deleted = 1
                    discovery[0].done_percent = 100
                    session.commit()
                return True
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object

    def run_snmp_discovery(self, discovery_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            discovery = session.query(Discovery.ip_start_range, Discovery.ip_end_range, Discovery.timeout, Discovery.snmp_community, Discovery.snmp_port, Discovery.snmp_version).filter(
                Discovery.discovery_id == discovery_id).all()          # execute query and fetch data
            if len(discovery) == 1:
                dis = discovery[0]
                start_range = dis.ip_start_range
                end_range = dis.ip_end_range
                timeout = dis.timeout
                community = dis.snmp_community
                port = dis.snmp_port
                version = dis.snmp_version

                pd = SnmpDiscovery()
                pd.snmp_function(discovery_id, start_range, end_range,
                                 timeout, community, port, version, DiscoveryBll)
                discovery = session.query(Discovery).filter(
                    Discovery.discovery_id == discovery_id).all()          # execute query and fetch data
                if len(discovery) > 0:
                    discovery[0].is_deleted = 1
                    discovery[0].done_percent = 100
                    session.commit()
                return True
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object

    def run_upnp_discovery(self, discovery_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            discovery = session.query(Discovery.timeout).filter(
                Discovery.discovery_id == discovery_id).all()          # execute query and fetch data
            if len(discovery) == 1:
                dis = discovery[0]
                timeout = dis.timeout
                ud = UpnpDiscovery()
                ud.upnp_function(discovery_id, timeout, DiscoveryBll)
                discovery = session.query(Discovery).filter(
                    Discovery.discovery_id == discovery_id).all()          # execute query and fetch data
                if len(discovery) > 0:
                    discovery[0].is_deleted = 1
                    discovery[0].done_percent = 100
                    session.commit()
                return True
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object


class HostBll(object):
    def __init__(self, userid=None):
        self.userid = userid

    def grid_view_active_host(self, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, req_vars):
        # Session = sessionmaker(bind=engine)     # making session of our
        # current database
        try:
            # session = Session()                 # creating new session object
            Host_child = aliased(Hosts)
            Host_parent = aliased(Hosts)
            a_columns = [
                "host_id", "is_localhost", "host_name", "host_alias", "ip_address",
                "device_name", "hostgroup_name", "mac_address", "host_alias", "priority_name", "host_state_id"]
            table_columns = [
                ["host_id", "is_localhost", "host_name", "host_alias",
                    "ip_address", "mac_address", "host_state_id"],
                ["device_name"],
                ["hostgroup_name"],
                [],
                [],
                [],
                ["host_alias"],
                ["priority_name"]
            ]
            table_classes = [Host_child, DeviceType, Hostgroups, UsersGroups,
                             HostgroupsGroups, HostsHostgroups, Host_parent, Priority]
            table_join = [
                "user_defined_outerjoin", "", "user_defined_outerjoin",
                "user_defined_outerjoin", "user_defined_outerjoin", "", "user_defined_outerjoin"]
            hgbll_obj = HostgroupBll()
            type_grid = "active_host"
            join_conditions = [
                [
                    {
                        "table_column": "device_type_id",
                        "join_with": {
                            "table_class": Host_child,
                            "table_column": "device_type_id"
                        }
                    }
                ],
                [],
                [
                    {"table_column": "user_id",
                     "join_with": '%s' % (self.userid)
                     }
                ],
                [
                    {
                        "table_column": "group_id",
                        "join_with": {
                            "table_class": UsersGroups,
                            "table_column": "group_id"
                        }
                    }
                ],
                [
                    {
                        "table_column": "hostgroup_id",
                        "join_with": {
                            "table_class": HostgroupsGroups,
                            "table_column": "hostgroup_id"
                        }
                    }
                ],
                [],
                [
                    {
                        "table_column": "priority_id",
                        "join_with": {
                            "table_class": Host_child,
                            "table_column": "priority_id"
                        }
                    }
                ]
            ]
            other_conditions = [
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "is_deleted",
                    "value": 0,
                    "rel": "and"
                },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "host_state_id",
                    "value": HostState.enable,
                    "rel": "and"
                },
                {
                    "type": "equal",
                    "table_class": HostgroupsGroups,
                    "table_column": "group_id",
                    "value": UsersGroups.group_id,
                    "rel": "and"
                },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "host_id",
                    "value": HostsHostgroups.host_id,
                    "rel": "and"
                },
                {
                    "type": "equal",
                    "table_class": Hostgroups,
                    "table_column": "hostgroup_id",
                    "value": HostsHostgroups.hostgroup_id,
                    "rel": "and"
                },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "parent_name",
                    "value": Host_parent.host_id,
                    "rel": "or"
                },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "is_localhost",
                    "value": 1,
                    "rel": "or"
                }
            ]
            group_by = Host_child.host_id
            req_vars["iSortCol_0"] = int(req_vars["iSortCol_0"]) + 1
            diff_count = 3
            hosts = hgbll_obj.get_data_table_sqlalchemy(
                a_columns, table_columns, table_classes, table_join, other_conditions, i_display_start, i_display_length, s_search,
                                                        sEcho, sSortDir_0, iSortCol_0, req_vars, join_conditions, group_by, diff_count)
            # hosts = session.query(Hosts.host_id, Hosts.is_localhost, Hosts.host_name, Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.host_state_id,DeviceType.device_name).filter(and_(Hosts.is_deleted == 0,Hosts.host_state_id == HostState.enable,Hosts.device_type_id == DeviceType.device_type_id,\
            # UsersGroups.user_id=='%s'%(self.userid),UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id)).order_by(Hosts.host_name).all()
            # # execute query and fetch data
            return hosts
        except Exception, e:
            return str(e)
        # finally:
        #    session.close()                     # close the session object

    def grid_view_disable_host(self, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, req_vars):
        # Session = sessionmaker(bind=engine)     # making session of our
        # current database
        try:
            # session = Session()                 # creating new session object
            Host_child = aliased(Hosts)
            Host_parent = aliased(Hosts)
            a_columns = [
                "host_id", "is_localhost", "host_name", "host_alias", "ip_address",
                "device_name", "hostgroup_name", "mac_address", "host_alias", "priority_name", "host_state_id"]
            table_columns = [
                ["host_id", "is_localhost", "host_name", "host_alias",
                    "ip_address", "mac_address", "host_state_id"],
                             ["device_name"],
                             ["hostgroup_name"],
                             [],
                             [],
                             [],
                             ["host_alias"],
                             ["priority_name"]
                             ]
            table_classes = [Host_child, DeviceType, Hostgroups, UsersGroups,
                HostgroupsGroups, HostsHostgroups, Host_parent, Priority]
            table_join = [
                "user_defined_outerjoin", "", "user_defined_outerjoin",
                "user_defined_outerjoin", "user_defined_outerjoin", "", "user_defined_outerjoin"]
            hgbll_obj = HostgroupBll()
            type_grid = "active_host"
            join_conditions = [
                [
                    {
                        "table_column": "device_type_id",
                        "join_with": {
                            "table_class": Host_child,
                            "table_column": "device_type_id"
                        }
                    }
                    ],
                [],
                [
                    {"table_column": "user_id",
                     "join_with": '%s' % (self.userid)
                     }
                    ],
                [
                    {
                        "table_column": "group_id",
                        "join_with": {
                            "table_class": UsersGroups,
                            "table_column": "group_id"
                        }
                    }
                    ],
                [
                    {
                        "table_column": "hostgroup_id",
                        "join_with": {
                            "table_class": HostgroupsGroups,
                            "table_column": "hostgroup_id"
                        }
                    }
                    ],
                [],
                [
                    {
                        "table_column": "priority_id",
                        "join_with": {
                            "table_class": Host_child,
                            "table_column": "priority_id"
                        }
                    }
                ]
            ]
            other_conditions = [
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "is_deleted",
                    "value": 0,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "host_state_id",
                    "value": HostState.disable,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": DeviceType,
                    "table_column": "device_type_id",
                    "value": Hosts.device_type_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": UsersGroups,
                    "table_column": "user_id",
                    "value": '%s' % (self.userid),
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": HostgroupsGroups,
                    "table_column": "group_id",
                    "value": UsersGroups.group_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": HostgroupsGroups,
                    "table_column": "hostgroup_id",
                    "value": HostsHostgroups.hostgroup_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "host_id",
                    "value": HostsHostgroups.host_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Hostgroups,
                    "table_column": "hostgroup_id",
                    "value": HostsHostgroups.hostgroup_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "parent_name",
                    "value": Host_parent.host_id,
                    "rel": "and"
                }
            ]
            group_by = Host_child.host_id
            diff_count = 3
            req_vars["iSortCol_0"] = int(req_vars["iSortCol_0"]) + 1
            hosts = hgbll_obj.get_data_table_sqlalchemy(
                a_columns, table_columns, table_classes, table_join, other_conditions, i_display_start, i_display_length, s_search,
                                                        sEcho, sSortDir_0, iSortCol_0, req_vars, join_conditions, group_by, diff_count)
            # hosts = session.query(Hosts.host_id, Hosts.is_localhost,
            # Hosts.host_name,
            # Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.host_state_id,DeviceType.device_name).filter(and_(Hosts.is_deleted
            # == 0,Hosts.host_state_id ==
            # HostState.disable,Hosts.device_type_id ==
            # DeviceType.device_type_id,UsersGroups.user_id=='%s'%(self.userid),UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id)).order_by(Hosts.host_name).all()
            # # execute query and fetch data
            return hosts
        except Exception, e:
            return str(e)
        # finally:
        #    session.close()                     # close the session object

    def grid_view_deleted_host(self, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, req_vars):
        # Session = sessionmaker(bind=engine)     # making session of our
        # current database
        try:
            # session = Session()                 # creating new session object
            # hosts = session.query(Hosts.host_id, Hosts.is_localhost,
            # Hosts.host_name,
            # Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.host_state_id,DeviceType.device_name,Hosts.timestamp,Users.first_name,
            # Users.last_name).filter(and_(Hosts.is_deleted ==
            # 1,Hosts.device_type_id ==
            # DeviceType.device_type_id,Hosts.updated_by ==
            # Users.user_id)).order_by(Hosts.host_name).all()          #
            # execute query and fetch data
            Host_child = aliased(Hosts)
            Host_parent = aliased(Hosts)
            a_columns = [
                "host_id", "host_alias", "is_localhost", "host_name", "ip_address", "device_name", "hostgroup_name",
                         "mac_address", "host_alias", "priority_name", "updated_by", "timestamp", "host_state_id"]
            table_columns = [
                ["host_id", "host_alias", "is_localhost", "host_name",
                    "ip_address", "mac_address", "host_state_id", "updated_by", "timestamp"],
                             ["device_name"],
                             [],
                             [],
                             [],
                             ["hostgroup_name"],
                             ["host_alias"],
                             ["priority_name"]
                             ]
            table_classes = [Host_child, DeviceType, UsersGroups,
                HostgroupsGroups, HostsHostgroups, Hostgroups, Host_parent, Priority]
            table_join = [
                "user_defined_outerjoin", "user_defined_outerjoin", "user_defined_outerjoin", "user_defined_outerjoin",
                "user_defined_outerjoin", "", "user_defined_outerjoin"]
            hgbll_obj = HostgroupBll()
            type_grid = "active_host"
            join_conditions = [
                [
                    {
                        "table_column": "device_type_id",
                        "join_with": {
                            "table_class": Host_child,
                            "table_column": "device_type_id"
                        }
                    }
                    ],
                [
                    {"table_column": "user_id",
                     "join_with": '%s' % (self.userid)
                     }
                    ],
                [
                    {
                        "table_column": "group_id",
                        "join_with": {
                            "table_class": UsersGroups,
                            "table_column": "group_id"
                        }
                    }
                    ],
                [
                    {
                        "table_column": "hostgroup_id",
                        "join_with": {
                            "table_class": HostgroupsGroups,
                            "table_column": "hostgroup_id"
                        }
                    }
                    ],
                [
                    {
                        "table_column": "hostgroup_id",
                        "join_with": {
                            "table_class": HostsHostgroups,
                            "table_column": "hostgroup_id"
                        }
                    }
                    ],
                [],
                [
                    {
                        "table_column": "priority_id",
                        "join_with": {
                            "table_class": Host_child,
                            "table_column": "priority_id"
                        }
                    }
                ]

            ]
            other_conditions = [
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "parent_name",
                    "value": Host_parent.host_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "is_deleted",
                    "value": 1,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "device_type_id",
                    "value": DeviceType.device_type_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": UsersGroups,
                    "table_column": "user_id",
                    "value": '%s' % (self.userid),
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": UsersGroups,
                    "table_column": "group_id",
                    "value": HostgroupsGroups.group_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": HostsHostgroups,
                    "table_column": "hostgroup_id",
                    "value": HostgroupsGroups.hostgroup_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "host_id",
                    "value": HostsHostgroups.host_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Host_child,
                    "table_column": "parent_name",
                    "value": Host_parent.host_id,
                    "rel": "and"
                }
            ]
            req_vars["iSortCol_0"] = int(req_vars["iSortCol_0"]) + 1 if int(
                req_vars["iSortCol_0"]) > 2 else int(req_vars["iSortCol_0"]) - 1
            hgbll_obj = HostgroupBll()
            diff_count = 5
            type_grid = "deleted_host"
            group_by = []
            # group_by=Host_child.host_alias
            hosts = hgbll_obj.get_data_table_sqlalchemy(
                a_columns, table_columns, table_classes, table_join, other_conditions, i_display_start, i_display_length, s_search,
                                                        sEcho, sSortDir_0, iSortCol_0, req_vars, join_conditions, group_by, diff_count)

            # hosts = session.query(Hosts.host_id, Hosts.is_localhost,
            # Hosts.host_name,
            # Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.host_state_id,DeviceType.device_name,Hosts.timestamp,Hosts.updated_by).filter(and_(Hosts.is_deleted
            # == 1,Hosts.device_type_id ==
            # DeviceType.device_type_id,UsersGroups.user_id=='%s'%(self.userid),UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id)).order_by(Hosts.host_name).all()
            # # execute query and fetch data
            return hosts
        except Exception, e:
            return e
        # finally:
            # session.close()                     # close the session object

    def grid_view_discovered_host(self, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, req_vars):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            ip_list = session.query(Hosts.ip_address).all()
            ip_list2 = []
            for i in ip_list:
                ip_list2.append(i[0])
            a_columns = ["discovered_host_id", "ip_address", "mac_address",
                "timestamp", "discovery_type_id", "device_name"]
            table_columns = [
                ["timestamp", "discovery_type_id", "discovery_id"],
                              ["discovered_host_id",
                                  "ip_address", "mac_address", "discovery_id"],
                              ["device_name", "device_type_id"]
                              ]
            table_classes = [Discovery, DiscoveredHosts, DeviceType]
            hgbll_obj = HostgroupBll()
            type_grid = "discovered_host"
            table_join = ["user_defined_outerjoin", "user_defined_outerjoin"]
            hgbll_obj = HostgroupBll()
            join_conditions = [
                [
                    {
                        "table_column": "discovery_id",
                        "join_with": {
                            "table_class": Discovery,
                            "table_column": "discovery_id"
                        }
                    }
                    ],
                [
                    {
                        "table_column": "device_type_id",
                        "join_with": {
                            "table_class": DiscoveredHosts,
                            "table_column": "device_type_id"
                        }
                    }
                ]
            ]

            other_conditions = [
                {
                    "type": "equal",
                    "table_class": Discovery,
                    "table_column": "discovery_id",
                    "value": DiscoveredHosts.discovery_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": DiscoveredHosts,
                    "table_column": "device_type_id",
                    "value": DeviceType.device_type_id,
                    "rel": "and"
                    },
                {
                    "type": "not in",
                    "table_class": DiscoveredHosts,
                    "table_column": "ip_address",
                    "value": ip_list2,
                    "rel": "and"
                }]
            req_vars["iSortingCols"] = 0
            hosts = hgbll_obj.get_data_table_sqlalchemy(
                a_columns, table_columns, table_classes, table_join, other_conditions, i_display_start, i_display_length,
                                                        s_search, sEcho, sSortDir_0, iSortCol_0, req_vars, join_conditions)
            hosts["ip_address"] = ip_list2
            # hosts =
            # session.query(DiscoveredHosts.discovered_host_id,DiscoveredHosts.ip_address,DiscoveredHosts.host_alias,DiscoveredHosts.mac_address,
            # Discovery.timestamp,Discovery.discovery_type_id,DeviceType.device_name).filter(and_(~DiscoveredHosts.ip_address.in_(session.query(Hosts.ip_address)),Discovery.discovery_id
            # == DiscoveredHosts.discovery_id,DiscoveredHosts.device_type_id ==
            # DeviceType.device_type_id))          # execute query and fetch
            # data
            session.close()                     # close the session object
            return hosts
        except Exception, e:
            return str(e)
#        finally:
#            session.close()                     # close the session object

    def grid_view_tcp_discovered_host(self, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, req_vars):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            a_columns = ["ne_id", "site_mac", "ip_address",
                "product_id", "timestamp"]
            table_columns = [["ne_id", "site_mac",
                "ip_address", "product_id", "timestamp"]]
            table_classes = [TcpDiscovery]
            table_join = [""]
            hgbll_obj = HostgroupBll()
            ip_list = session.query(Hosts.ip_address).all()
            ip_list2 = []
            for i in ip_list:
                ip_list2.append(i[0])
            other_conditions = [
                {
                    "type": "not in",
                    "table_class": TcpDiscovery,
                    "table_column": "ip_address",
                    "value": ip_list2,
                    "rel": "and"
                }]
            req_vars["iSortingCols"] = 0
            hosts = hgbll_obj.get_data_table_sqlalchemy(
                a_columns, table_columns, table_classes, table_join, other_conditions, i_display_start,
                                                        i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, req_vars)
            # hosts = session.query(TcpDiscovery.ne_id,TcpDiscovery.site_mac,
            # TcpDiscovery.ip_address,
            # TcpDiscovery.timestamp).filter(~TcpDiscovery.ip_address.in_(session.query(Hosts.ip_address))).all()
            # # execute query and fetch data
            return hosts
        except Exception, e:
            return str(e)
        finally:
            session.close()                     # close the session object

    def grid_view_active_host_report(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hosts = session.query(
                Hosts.host_id, Hosts.is_localhost, Hosts.host_name, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address, Hosts.created_by, Hosts.creation_time, Hosts.host_state_id, DeviceType.device_name).filter(and_(Hosts.is_deleted == 0, Hosts.host_state_id == HostState.enable, Hosts.device_type_id == DeviceType.device_type_id,
                                                                                                                                                                                                                                       UsersGroups.user_id == '%s' % (self.userid), UsersGroups.group_id == HostgroupsGroups.group_id, HostsHostgroups.hostgroup_id == HostgroupsGroups.hostgroup_id, Hosts.host_id == HostsHostgroups.host_id)).order_by(Hosts.host_name).all()          # execute query and fetch data
            return hosts
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def grid_view_disable_host_report(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hosts = session.query(Hosts.host_id, Hosts.is_localhost, Hosts.host_name, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address, Hosts.updated_by, Hosts.timestamp, Hosts.host_state_id, DeviceType.device_name).filter(
                and_(Hosts.is_deleted == 0, Hosts.host_state_id == HostState.disable, Hosts.device_type_id == DeviceType.device_type_id, UsersGroups.user_id == '%s' % (self.userid), UsersGroups.group_id == HostgroupsGroups.group_id, HostsHostgroups.hostgroup_id == HostgroupsGroups.hostgroup_id, Hosts.host_id == HostsHostgroups.host_id)).order_by(Hosts.host_name).all()          # execute query and fetch data
            return hosts
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def grid_view_deleted_host_report(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            # hosts = session.query(Hosts.host_id, Hosts.is_localhost,
            # Hosts.host_name,
            # Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.host_state_id,DeviceType.device_name,Hosts.timestamp,Users.first_name,
            # Users.last_name).filter(and_(Hosts.is_deleted ==
            # 1,Hosts.device_type_id ==
            # DeviceType.device_type_id,Hosts.updated_by ==
            # Users.user_id)).order_by(Hosts.host_name).all()          #
            # execute query and fetch data
            hosts = session.query(
                Hosts.host_id, Hosts.is_localhost, Hosts.host_name, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address, Hosts.host_state_id, DeviceType.device_name, Hosts.timestamp, Hosts.updated_by).filter(and_(Hosts.is_deleted == 1, Hosts.device_type_id == DeviceType.device_type_id, UsersGroups.user_id == '%s' % (self.userid),
                                  UsersGroups.group_id == HostgroupsGroups.group_id, HostsHostgroups.hostgroup_id == HostgroupsGroups.hostgroup_id, Hosts.host_id == HostsHostgroups.host_id)).order_by(Hosts.host_name).all()          # execute query and fetch data
            return hosts
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def grid_view_discovered_host_report(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hosts = session.query(
                DiscoveredHosts.discovered_host_id, DiscoveredHosts.ip_address, DiscoveredHosts.host_alias, DiscoveredHosts.mac_address, Discovery.timestamp, Discovery.discovery_type_id, DeviceType.device_name).filter(and_(~DiscoveredHosts.ip_address.in_(session.query(Hosts.ip_address)),
                                  Discovery.discovery_id == DiscoveredHosts.discovery_id, DiscoveredHosts.device_type_id == DeviceType.device_type_id))          # execute query and fetch data
            return hosts
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def grid_view_tcp_discovered_host_report(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hosts = session.query(TcpDiscovery.ne_id, TcpDiscovery.site_mac, TcpDiscovery.ip_address, TcpDiscovery.timestamp, TcpDiscovery.product_id).filter(~TcpDiscovery.ip_address.in_(
                session.query(Hosts.ip_address))).all()          # execute query and fetch data
            return hosts
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def host_default_details(self):
        host_other_details = SystemConfig.get_host_other_details()
        host_http_details = SystemConfig.get_host_http_details()
        host_snmp_details = SystemConfig.get_host_snmp_details()
        host_position_details = SystemConfig.get_default_lat_long()
        host_details_dic = {
            "host_id": "",
            "host_name": "host",
            "host_alias": "",
            "ip_address": "",
            "mac_address": "",
            "device_type": "",
            "ra_mac": "FF:FF:FF:FF:FF:FF",
            "node_type": 0,
            "master_mac": "",
            "host_state": str(host_other_details["host_state"]),
            "host_priority": str(host_other_details["host_priority"]),
            "host_vendor": "",
            "host_os": "",
            "host_parent": "",
            "hostgroup": "",
            "host_comment": "",
            "netmask": "",
            "gateway": "",
            "primary_dns": "",
            "secondary_dns": "",
            "dns_state": "",
            "odu100_management_mode": 0,
            "odu100_vlan_tag": "",
            "idu4_management_mode": 0,
            "idu4_vlan_tag": "",
            "idu4_tdm_ip": "",
            "ccu_dhcp_netmask": "",
            "http_username": str(host_http_details["username"]),
            "http_password": str(host_http_details["password"]),
            "http_port": str(host_http_details["port"]),
            "ssh_username": "",
            "ssh_password": "",
            "ssh_port": "",
            "read_community": str(host_snmp_details["read_comm"]),
            "write_community": str(host_snmp_details["write_comm"]),
            "snmp_version": str(host_snmp_details["version"]),
            "get_set_port": str(host_snmp_details["get_set_port"]),
            "trap_port": str(host_snmp_details["trap_port"]),
            "longitude": str(host_position_details["longitude"]),
            "latitude": str(host_position_details["latitude"]),
            "lock_position": "",
            "serial_number": "",
            "hardware_version": ""
        }
        return {"success": 0, "result": host_details_dic}

    def get_master_id_by_macaddress(self, mac_address):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        host_id = ""
        try:
            session = Session()                 # creating new session object
            hosts = session.query(
                Hosts.host_id).filter(Hosts.mac_address == mac_address).all()
            if len(hosts) > 0:
                host_id = hosts[0].host_id
            return host_id
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return host_id
        finally:
            session.close()                     # close the session object

    def get_master_id_by_ra_mac(self, ra_mac):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        host_id = ""
        try:
            session = Session()                 # creating new session object
            hosts = session.query(Hosts.host_id).join(HostAssets).filter(and_(
                Hosts.is_deleted == 0, HostAssets.ra_mac == ra_mac)).all()
            if len(hosts) > 0:
                host_id = hosts[0].host_id
            return host_id
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object

    def get_host_by_id(self, host_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        hostgroup = ""
        try:
            session = Session()                 # creating new session object
            hosts = session.query(
                Hosts.host_id, Hosts.host_name, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address, Hosts.device_type_id, Hosts.config_profile_id,
                                  Hosts.host_state_id, Hosts.priority_id, Hosts.host_vendor_id, Hosts.host_os_id, Hosts.parent_name,
                                  Hosts.comment, Hosts.netmask, Hosts.gateway, Hosts.primary_dns, Hosts.secondary_dns, Hosts.dns_state,
                                  Hosts.http_username, Hosts.http_password, Hosts.http_port, Hosts.ssh_username, Hosts.ssh_password,
                                  Hosts.ssh_port, Hosts.snmp_read_community, Hosts.snmp_write_community,
Hosts.snmp_version_id, Hosts.snmp_port, Hosts.snmp_trap_port, Hosts.lock_status, HostAssets.longitude, HostAssets.latitude, HostAssets.serial_number, HostAssets.hardware_version, HostVendor.vendor_name, HostOs.os_name, DeviceType.device_name, Hosts.firmware_mapping_id).filter(and_(Hosts.host_id == host_id, Hosts.host_asset_id == HostAssets.host_asset_id, Hosts.host_vendor_id == HostVendor.host_vendor_id, Hosts.host_os_id == HostOs.host_os_id, Hosts.device_type_id == DeviceType.device_type_id)).all()          # execute query and fetch data
            hostgroup_obj = session.query(HostsHostgroups).filter(
                HostsHostgroups.host_id == host_id).all()
            for hg_obj in hostgroup_obj:
                hostgroup = hg_obj.hostgroup_id

            ra_mac = "FF:FF:FF:FF:FF:FF"
            node_type = "0"
            master_mac = ""
            odu100_management_mode = 0
            odu100_vlan_tag = ""
            idu4_management_mode = 0
            idu4_vlan_tag = ""
            idu4_tdm_ip = ""
            ccu_dhcp_netmask = ""
            if len(hosts) == 1:
                host = hosts[0]
                if UNMPDeviceType.odu16 == host.device_type_id:
                    ra_mac_table_obj = session.query(GetOdu16RaStatusTable.ra_mac_address).filter(
                        GetOdu16RaStatusTable.host_id == host_id).all()
                    if len(ra_mac_table_obj) > 0:
                        ra_mac = ra_mac_table_obj[0].ra_mac_address

                    node_type_table_obj = session.query(
                        GetOdu16_ru_conf_table.default_node_type).filter(GetOdu16_ru_conf_table.host_id == host_id).all()
                    if len(node_type_table_obj) > 0:
                        node_type = str(
                            node_type_table_obj[0].default_node_type)

                    master_mac_table_obj = session.query(MasterSlaveLinking.master).filter(
                        and_(MasterSlaveLinking.slave == host_id)).all()
                    if len(master_mac_table_obj) > 0:
                        master_mac = master_mac_table_obj[0].master

                elif UNMPDeviceType.odu100 == host.device_type_id:
                    ra_mac_table_obj = session.query(Odu100RaStatusTable.raMacAddress).filter(
                        Odu100RaStatusTable.host_id == host_id).all()
                    if len(ra_mac_table_obj) > 0:
                        ra_mac = ra_mac_table_obj[0].raMacAddress

                    node_type_table_obj = session.query(Odu100RuConfTable.defaultNodeType).filter(
                        Odu100RuConfTable.config_profile_id == host.config_profile_id).all()
                    if len(node_type_table_obj) > 0:
                        node_type = str(node_type_table_obj[0].defaultNodeType)

                    master_mac_table_obj = session.query(MasterSlaveLinking.master).filter(
                        MasterSlaveLinking.slave == host_id).all()
                    if len(master_mac_table_obj) > 0:
                        master_mac = master_mac_table_obj[0].master

                    vlan_table_obj = session.query(Odu100IpConfigTable.managementMode, Odu100IpConfigTable.managementVlanTag).filter(
                        Odu100IpConfigTable.config_profile_id == host.config_profile_id).all()
                    if len(vlan_table_obj) > 0:
                        odu100_management_mode = vlan_table_obj[
                            0].managementMode
                        odu100_vlan_tag = vlan_table_obj[0].managementVlanTag

                elif UNMPDeviceType.ccu == host.device_type_id:
                    ccu_network_table_obj = session.query(
                        CcuNetworkConfigurationTable.ccuNCDHCPNetMask).filter(CcuNetworkConfigurationTable.host_id == host_id).all()
                    if len(ccu_network_table_obj) > 0:
                        ccu_dhcp_netmask = ccu_network_table_obj[
                            0].ccuNCDHCPNetMask

                host_details_dic = {
                    "host_id": str(host.host_id),
                    "host_name": host.host_name != None and host.host_name or "",
                    "host_alias": host.host_alias != None and host.host_alias or "",
                    "ip_address": host.ip_address != None and host.ip_address or "",
                    "mac_address": host.mac_address != None and host.mac_address or "",
                    "device_type": host.device_type_id != None and host.device_type_id or "",
                    "device_name": host.device_name != None and host.device_name or "",
                    "ra_mac": ra_mac,
                    "node_type": node_type,
                    "master_mac": str(master_mac),
                    "host_state": host.host_state_id != None and host.host_state_id or "",
                    "host_priority": host.priority_id != None and host.priority_id or "",
                    "host_vendor": host.host_vendor_id != None and str(host.host_vendor_id) or "",
                    "host_vendor_name": host.vendor_name != None and host.vendor_name or "",
                    "host_os": host.host_os_id != None and host.host_os_id or "",
                    "host_os_name": host.os_name != None and host.os_name or "",
                    "host_parent": host.parent_name != None and str(host.parent_name) or "",
                    "hostgroup": str(hostgroup),
                    "host_comment": host.comment != None and host.comment or "",
                    "netmask": host.netmask != None and host.netmask or "",
                    "gateway": host.gateway != None and host.gateway or "",
                    "primary_dns": host.primary_dns != None and host.primary_dns or "",
                    "secondary_dns": host.secondary_dns != None and host.secondary_dns or "",
                    "dns_state": host.dns_state != None and host.dns_state or "",
                    "odu100_management_mode": odu100_management_mode,
                    "odu100_vlan_tag": odu100_vlan_tag,
                    "idu4_management_mode": idu4_management_mode,
                    "idu4_vlan_tag": idu4_vlan_tag,
                    "idu4_tdm_ip": idu4_tdm_ip,
                    "ccu_dhcp_netmask": ccu_dhcp_netmask,
                    "http_username": host.http_username != None and host.http_username or "",
                    "http_password": host.http_password != None and host.http_password or "",
                    "http_port": host.http_port != None and host.http_port or "",
                    "ssh_username": host.ssh_username != None and host.ssh_username or "",
                    "ssh_password": host.ssh_password != None and host.ssh_password or "",
                    "ssh_port": host.ssh_port != None and host.ssh_port or "",
                    "read_community": host.snmp_read_community != None and host.snmp_read_community or "",
                    "write_community": host.snmp_write_community != None and host.snmp_write_community or "",
                    "snmp_version": host.snmp_version_id != None and host.snmp_version_id or "",
                    "get_set_port": host.snmp_port != None and host.snmp_port or "",
                    "trap_port": host.snmp_trap_port != None and host.snmp_trap_port or "",
                    "longitude": host.longitude != None and host.longitude or "",
                    "latitude": host.latitude != None and host.latitude or "",
                    "lock_position": host.lock_status != None and host.lock_status or "",
                    "serial_number": host.serial_number != None and host.serial_number or "",
                    "hardware_version": host.hardware_version != None and host.hardware_version or "",
                    "firmware_version": host.firmware_mapping_id != None and host.firmware_mapping_id or "",
                    "device_type": host.device_type_id != None and host.device_type_id or ""


                }
                return host_details_dic
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object

    def get_nms_instance_id(self, nms_name):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            nms = session.query(NmsInstance.nms_id).filter(
                NmsInstance.nms_name == nms_name).all()          # execute query and fetch data
            if len(nms) == 1:
                return nms[0]
            else:
                err = ErrorMessages()
                err.error_msg = err.no_nms_instance_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object
# raju

    def add(self, host_name, host_alias, ip_address, mac_address, device_type_id, netmask, gateway, primary_dns, secondary_dns, dns_state, odu100_management_mode, odu100_vlan_tag, idu4_management_mode, idu4_vlan_tag, idu4_tdm_ip, ccu_dhcp_netmask, timestamp, created_by, creation_time, is_deleted, updated_by, ne_id, site_id, host_state_id, priority_id, host_vendor_id, host_os_id, http_username, http_password, http_port, ssh_username, ssh_password, ssh_port, snmp_read_community, snmp_write_community, snmp_port, snmp_trap_port, snmp_version_id, comment, nms_instance, parent_name, lock_status, is_localhost, longitude, latitude, serial_number, hardware_version, hostgroup, ra_mac="", node_type="", master_id="", firmware_mapping_id="7.2.20", is_reconciliation=True):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            lic = LicenseBll()
            # this will be change according to generic approch
            if lic.check_license_for_host() == True:
            # if True:
                if self.validate(host_name, host_alias, ip_address, mac_address, device_type_id, netmask, gateway, primary_dns, secondary_dns, odu100_management_mode, odu100_vlan_tag, idu4_management_mode, idu4_vlan_tag, idu4_tdm_ip, ccu_dhcp_netmask, host_state_id, priority_id, host_vendor_id, host_os_id, http_username, http_password, http_port, ssh_username, ssh_password, ssh_port, snmp_read_community, snmp_write_community, snmp_port, snmp_trap_port, comment, longitude, latitude, serial_number, hardware_version):
                    if self.is_duplicate_host_for_add(host_name, host_alias, ip_address, mac_address):
                        # call 'create configuration profile' for odu16, odu100 and swt24.
                        #  config_profile_id  = create_config_profile()
                        config_profile_id = None

                        # get nms_id through nms_instance
                        nms_id = None
                        nms = self.get_nms_instance_id(nms_instance)
                        if isinstance(nms, ErrorMessages):
                            return nms
                        elif isinstance(nms, Exception):
                            return nms
                        else:
                            nms_id = nms.nms_id
                            # enter data into asset table
                            host_asset = HostAssets(
                                longitude, latitude, serial_number,
                                                    hardware_version, "0000-00-00 00:00:00", 0, None, None, None, None, ra_mac)
                            session.add(host_asset)
                            session.flush()
                            session.refresh(host_asset)
                            host_asset_id = host_asset.host_asset_id

                        reconcile_health = 0
                        reconcile_status = 0
                        host = Hosts(
                            host_name, host_alias, ip_address, mac_address, device_type_id, netmask, gateway, primary_dns, secondary_dns, dns_state, config_profile_id, timestamp, created_by, creation_time, is_deleted, updated_by, ne_id, site_id, host_state_id, priority_id, host_vendor_id, host_os_id, host_asset_id, http_username, http_password, http_port, snmp_read_community,
                                     snmp_write_community, snmp_port, snmp_trap_port, snmp_version_id, comment, nms_id, parent_name, lock_status, is_localhost, reconcile_health, reconcile_status, ssh_username, ssh_password, ssh_port, firmware_mapping_id)
                        session.add(host)
                        session.flush()
                        session.refresh(host)
                        services_list = self.get_services_from_templates(
                            host.device_type_id)
                        host_data = session.query(Hosts).filter(
                            and_(Hosts.host_id == host.host_id, Hosts.is_deleted == 0)).all()
                        n_bll = NagiosBll()
                        for srv in services_list:
                            # [service_description,check_command,max_check_attempts,normal_check_interval,retry_check_interval]
                            # new code
                            service = HostServices(
                                host.host_id, srv.service_description, srv.check_command,
                                                   srv.max_check_attempts, srv.normal_check_interval, srv.retry_check_interval, 0)
                            session.add(service)
                            if(flag_nagios_call == 1):
                                wnc = n_bll.add_new_service(
                                    str(host.host_name) + str(
                                        host.host_id), host.host_alias, srv.service_description,
                                                            srv.max_check_attempts, srv.normal_check_interval, srv.retry_check_interval, srv.check_command)
                                condition_nagios = wnc["success"] == 0
                        # add host status default entry
                        host_status = HostStatus(
                            host.ip_address, host.host_id, '0', 0)
                        session.add(host_status)
                        # END - add host status default entry
                        session.commit()
                        config_profile_id = None
                        temp_conf_id = None
                        obj_reconcilation = OduReconcilation()
                        ap_obj_reconciliation = Reconciliation()
                        idu_obj_reconciliation = IduReconcilation()
                        ccu_obj_reconciliation = CCUReconcilation()

                        if device_type_id == 'odu16':
                            config_profile_id = obj_reconcilation.odu16_add_current_config_profile(
                                host.host_id, 'odu16', 'odu16_', is_reconciliation)
                            # For multiple odu16 devices add
                            # odu16_add_default_config_profile(self,host_id,device_type_id,table_prefix,insert_update)
                            # config_profile_id = obj_reconcilation.odu16_add_default_config_profile(host.host_id,'odu16','odu16_',False)
                        # elif device_type_id == 'odu100':
                            # config_profile_id =
                            # obj_reconcilation.reconcilation_controller##(host.host_id,'odu100','odu100_',False)
                        elif device_type_id == 'odu100':
                            config_profile_id = obj_reconcilation.odu100_add_default_config_profile(
                                host.host_id, 'odu100', 'odu100_', datetime.now(), is_reconciliation, created_by)
                        elif device_type_id == 'idu4':
                            config_profile_id = idu_obj_reconciliation.default_reconciliation_controller(
                                host.host_id, 'idu4', 'idu_', True)
                        # elif device_type_id == 'swt4':
                            # config_profile_id = create_default_configprofile_for_swt4(host.host_id,'swt4','swt4_',False)
                        #################### reconciliation for ap ############
                        elif device_type_id == 'ap25':
                            config_profile_id = ap_obj_reconciliation.default_configuration_added(
                                host.host_id, 'ap25', 'ap25_', datetime.now(), created_by, is_reconciliation)
                        #################### reconciliation for ap #################################################
                        #################### reconciliation for ccu ###########
                        elif device_type_id == 'ccu':
                            config_profile_id = ccu_obj_reconciliation.default_reconciliation_controller(
                                host.host_id, 'ccu', 'ccu_', datetime.now(), created_by, is_reconciliation)
                        #################### reconciliation for ccu ###########

                        host_data = session.query(Hosts).filter(
                            and_(Hosts.host_id == host.host_id, Hosts.is_deleted == 0)).all()
                        if device_type_id == "odu100" and type(config_profile_id) == dict:
                            host_data[
                                0].config_profile_id = config_profile_id['result'][0]
                            host_data[
                                0].reconcile_health = config_profile_id['result'][1]
                            temp_conf_id = config_profile_id['result'][0]
                        else:
                            if len(host_data) > 0 and config_profile_id != None and type(config_profile_id) == tuple and len(config_profile_id) == 2:
                                host_data[
                                    0].config_profile_id = config_profile_id[0]
                                host_data[
                                    0].reconcile_health = config_profile_id[1]
                                temp_conf_id = config_profile_id[0]
                            elif len(host_data) > 0 and config_profile_id != None:
                                host_data[
                                    0].config_profile_id = config_profile_id
                                temp_conf_id = config_profile_id
                        if len(host_data) > 0:
                            host_name = "host" + str(host.host_id)
                            host_data[0].host_name = host_name

                        hostgroup_obj = HostsHostgroups(
                            host.host_id, hostgroup)
                        session.add(hostgroup_obj)
                        session.commit()
#                        ###############Anuj samariya ###########################
#		        if device_type_id == 'ap25':
#		            update_profile = ap_obj_reconciliation.update_configuration(host.host_id,'ap25')
#		            if update_profile["success"]==0:
#		                for i in update_profile["result"]:
#   		                    host_data[0].reconcile_health = i
#    	                session.commit()
                        ############### Reconciliation for ap #################

                                # ra_mac and node type and master mac address
                        if UNMPDeviceType.odu16 == device_type_id:
                            ra_mac_table_obj = session.query(GetOdu16RaStatusTable).filter(
                                GetOdu16RaStatusTable.host_id == host.host_id).all()
                            if len(ra_mac_table_obj) > 0:
                                ra_mac_table_obj[0].ra_mac_address = ra_mac
                            else:
                                ra_status_table = GetOdu16RaStatusTable(
                                    host.host_id, 0, ra_mac)
                                session.add(ra_status_table)

                            node_type_table_obj = session.query(GetOdu16_ru_conf_table).filter(
                                GetOdu16_ru_conf_table.host_id == host.host_id).all()
                            if len(node_type_table_obj) > 0:
                                node_type_table_obj[
                                    0].default_node_type = node_type

                            else:
                                ru_conf_table = GetOdu16_ru_conf_table(
                                    host.host_id, 0, None, node_type, None)
                                session.add(ru_conf_table)

                            if master_id != "" and master_id != None:
                                master_mac_table_obj = MasterSlaveLinking(
                                    master_id, host.host_id)
                                session.add(master_mac_table_obj)
                            session.commit()
                            # return host.host_id
                        elif UNMPDeviceType.odu100 == device_type_id:
                            if is_reconciliation == True:
                                obj_reconcilation.update_reconcilation_controller(
                                    host.host_id, device_type_id, "odu100_", datetime.now(), created_by)
                            ra_mac_table_obj = session.query(Odu100RaStatusTable).filter(
                                Odu100RaStatusTable.host_id == host.host_id).all()
                            if len(ra_mac_table_obj) > 0:
                                ra_mac_table_obj[0].raMacAddress = ra_mac
                            else:
                                ra_status_table = Odu100RaStatusTable(
                                    host.host_id, 1, None, ra_mac, None, None, None, 0, 0, datetime.now())
                                session.add(ra_status_table)

                            node_type_table_obj = session.query(Odu100RuConfTable).filter(
                                Odu100RuConfTable.config_profile_id == temp_conf_id).all()
                            if len(node_type_table_obj) > 0:
                                node_type_table_obj[
                                    0].defaultNodeType = node_type
                            else:
                                if temp_conf_id != None:
                                    ru_conf_table = Odu100RuConfTable(
                                        temp_conf_id, 1, None, node_type, None, None, None, None, 0, 0, 0, 0, 0)
                                    session.add(ru_conf_table)
                                    # pass

                            if master_id != "" and master_id != None:
                                master_mac_table_obj = MasterSlaveLinking(
                                    master_id, host.host_id)
                                session.add(master_mac_table_obj)

                            # manage vlan
                            vlan_table_obj = session.query(Odu100IpConfigTable).filter(
                                Odu100IpConfigTable.config_profile_id == temp_conf_id).all()
                            if len(vlan_table_obj) > 0:
                                vlan_table_obj[
                                    0].managementMode = odu100_management_mode
                                vlan_table_obj[
                                    0].managementVlanTag = odu100_vlan_tag
                            else:
                                if odu100_management_mode != None and odu100_vlan_tag != None:
                                    vlan_table = Odu100IpConfigTable(
                                        temp_conf_id, 1, None, ip_address, netmask, gateway, dns_state,
                                                                     odu100_management_mode, odu100_vlan_tag)
                                    session.add(vlan_table)
                            # end - manage vlan
                            session.commit()
                        elif UNMPDeviceType.idu4 == device_type_id:
                            if is_reconciliation == True:
                                idu_obj_reconciliation.update_device_reconcilation_controller(
                                    host.host_id, 'idu4', 'idu_', True, created_by)
                        elif UNMPDeviceType.ap25 == device_type_id:
                            if is_reconciliation == True:
                                update_profile = ap_obj_reconciliation.update_configuration(
                                    host.host_id, 'ap25', 'ap25_', datetime.now(), created_by)
                                if update_profile["success"] == 0:
                                    for i in update_profile["result"]:
                                        host_data[0].reconcile_health = i
                        elif UNMPDeviceType.ccu == device_type_id:
                            if is_reconciliation == True:
                                update_profile = ccu_obj_reconciliation.update_reconcilation_controller(
                                    host.host_id, 'ccu', 'ccu_', datetime.now(), created_by)
                                if update_profile["success"] == 0:
                                    for i in update_profile["result"]:
                                        host_data[0].reconcile_health = i
                            # manage vlan
                            vlan_table_obj = session.query(CcuNetworkConfigurationTable).filter(
                                CcuNetworkConfigurationTable.host_id == host.host_id).all()
                            if len(vlan_table_obj) > 0:
                                vlan_table_obj[
                                    0].ccuNCDHCPNetMask = ccu_dhcp_netmask
                            else:
                                if ccu_dhcp_netmask != None:
                                    vlan_table = CcuNetworkConfigurationTable(
                                        host.host_id, 1, mac_address, ip_address, netmask, "", "", ccu_dhcp_netmask, gateway)
                                    session.add(vlan_table)
                            # end - manage vlan

                        session.commit()

                        # ncbll = NagioConfigurationBll()
                        # wnc = ncbll.write_nagios_config(nms_instance)
                        if(flag_nagios_call == 0):
                            ncbll = NagioConfigurationBll()
                            wnc = ncbll.write_nagios_config(nms_instance)
                            condition_nagios = isinstance(wnc, bool)
                        else:
                            n_bll = NagiosBll()
                            wnc = n_bll.add_new_host(host_name,
                                                     host_alias, ip_address, parent_name, hostgroup)
                            condition_nagios = wnc["success"] == 0
                        if condition_nagios:
                            if flag_nagios_call:
                                SystemSetting.reload_nagios_config()
                        # if isinstance(wnc, bool):
                            el = EventLog()
                            el.log_event(
                                "Add New Host '%s'." % (ip_address), updated_by)
                            return host.host_id
                        else:
                            err = ErrorMessages()
                            err.error_msg = err.nagios_config_error
                            return err
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.duplicate_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.validation_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.license_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object

    def get_services_from_templates(self, device_type):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            services = session.query(ServiceTemplates).filter(
                ServiceTemplates.device_type_id == device_type).all()          # execute query and fetch data
            return services
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object

    def edit(self, host_id, host_name, host_alias, ip_address, mac_address, device_type_id, netmask, gateway, primary_dns, secondary_dns, dns_state, odu100_management_mode, odu100_vlan_tag, idu4_management_mode, idu4_vlan_tag, idu4_tdm_ip, ccu_dhcp_netmask, is_deleted, updated_by, host_state_id, priority_id, host_vendor_id, host_os_id, http_username, http_password, http_port, ssh_username, ssh_password, ssh_port, snmp_read_community, snmp_write_community, snmp_port, snmp_trap_port, snmp_version_id, comment, nms_instance, parent_name, lock_status, longitude, latitude, serial_number, hardware_version, hostgroup, ra_mac="", node_type="", master_id="", firmware_mapping_id="7.2.20"):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            temp_conf_id = None
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            if self.validate(host_name, host_alias, ip_address, mac_address, device_type_id, netmask, gateway, primary_dns, secondary_dns, odu100_management_mode, odu100_vlan_tag, idu4_management_mode, idu4_vlan_tag, idu4_tdm_ip, ccu_dhcp_netmask, host_state_id, priority_id, host_vendor_id, host_os_id, http_username, http_password, http_port, ssh_username, ssh_password, ssh_port, snmp_read_community, snmp_write_community, snmp_port, snmp_trap_port, comment, longitude, latitude, serial_number, hardware_version):
                if self.is_duplicate_host_for_edit(host_id, host_name, host_alias, ip_address, mac_address):
                    hosts = session.query(
                        Hosts).filter(Hosts.host_id == host_id).all()
                    if len(hosts) == 1:
                        host = hosts[0]
                        temp_conf_id = host.config_profile_id
                        rec = host.reconcile_health
                        # if device type is changed
                        if host.device_type_id != device_type_id:
                            if host.config_profile_id != None:
                                cursor.execute(
                                    "delete from config_profiles where config_profile_id = %s" % host.config_profile_id)
                            if host.host_id != None:
                                # delete services
                                cursor.execute(
                                    "delete from host_services where host_id = %s" % host.host_id)
                                # trap & alarm table will empty
                                cursor.execute(
                                    "delete from trap_alarms where agent_id = '%s'" % host.ip_address)
                                cursor.execute(
                                    "delete from trap_alarm_clear where agent_id = '%s'" % host.ip_address)
                                cursor.execute("delete from trap_alarm_current where agent_id = '%s'" %
                                               host.ip_address)
                                cursor.execute("delete from system_alarm_table where agent_id = '%s'" %
                                               host.ip_address)

                                if host.device_type_id == UNMPDeviceType.odu16:
                                    # odu 16 get table will empty
                                    cursor.execute(
                                        "delete from get_odu16_nw_interface_statistics_table where host_id = %s" % host.host_id)
                                    cursor.execute("delete from get_odu16_peer_node_status_table where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from get_odu16_ra_tdd_mac_statistics_entry where host_id = %s" % host.host_id)
                                    cursor.execute("delete from get_odu16_synch_statistics_table where host_id = %s" % host.host_id)
                                    # odu 16 analyze table will empty
                                    cursor.execute("delete from analyze_get_odu16_nw_interface_statistics_table where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from analyze_get_odu16_peer_node_status_table where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from analyze_get_odu16_ra_tdd_mac_statistics_entry where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from analyze_get_odu16_synch_statistics_table where host_id = %s" % host.host_id)

                                if host.device_type_id == UNMPDeviceType.odu100:
                                    # odu 100 get table will empty
                                    cursor.execute(
                                        "delete from odu100_nwInterfaceStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from odu100_raTddMacStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from odu100_raScanListTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from odu100_synchStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute("delete from odu100_peerNodeStatusTable where host_id = %s" % host.host_id)
                                    cursor.execute("delete from odu100_swStatusTable where host_id = %s" %
                                                   host.host_id)
                                    cursor.execute(
                                        "delete from odu100_hwDescTable where host_id = %s" % host.host_id)
                                    # odu 100 analyze table will empty
                                    cursor.execute("delete from analyze_odu100_nwInterfaceStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from analyze_odu100_peerNodeStatusTable where host_id = %s" % host.host_id)
                                    cursor.execute("delete from analyze_odu100_raTddMacStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute("delete from analyze_odu100_synchStatisticsTable where host_id = %s" % host.host_id)

                                if host.device_type_id == UNMPDeviceType.idu4:
                                    # idu 4 get table will empty
                                    cursor.execute("delete from idu_tdmoipNetworkInterfaceStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute("delete from idu_iduNetworkStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from idu_e1PortStatusTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from idu_linkStatusTable where host_id = %s" % host.host_id)
                                    cursor.execute("delete from idu_portSecondaryStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute("delete from idu_portstatisticsTable where host_id = %s" %
                                                   host.host_id)
                                    cursor.execute("delete from idu_swPrimaryPortStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from idu_iduInfoTable where host_id = %s" % host.host_id)
                                    cursor.execute("delete from idu_swStatusTable where host_id = %s" %
                                                   host.host_id)
                                    # idu 4 analyze table will empty
                                    cursor.execute(
                                        "delete from analyze_idu_portSecondaryStatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from analyze_idu_portstatisticsTable where host_id = %s" % host.host_id)
                                    cursor.execute(
                                        "delete from analyze_idu_swPrimaryPortStatisticsTable where host_id = %s" % host.host_id)

                                if(flag_nagios_call == 1):
                                    n_bll = NagiosBll()
                                    wnc = n_bll.delete_old_service(
                                        host.host_name)
                                    condition_nagios = wnc["success"] == 0

                                if host.device_type_id == UNMPDeviceType.ap25:
                                    # ap get table will empty
                                    cursor.execute("delete from ap25_statisticsTable where host_id = %s" %
                                                   host.host_id)
                                if device_type_id == UNMPDeviceType.ap25 or device_type_id == UNMPDeviceType.idu4 or device_type_id == UNMPDeviceType.generic or device_type_id == UNMPDeviceType.swt4:
                                    cursor.execute(
                                        "delete from master_slave_linking where master = %s OR slave = %s" % (host.host_id, host.host_id))

                            # recreate config profile
                            config_profile_id = None
                            obj_reconcilation = OduReconcilation()
                            ap_obj_reconciliation = Reconciliation()
                            idu_obj_reconciliation = IduReconcilation()
                            if device_type_id == UNMPDeviceType.odu16:
                                config_profile_id = obj_reconcilation.odu16_add_current_config_profile(
                                    host.host_id, 'odu16', 'odu16_', False)
                            elif device_type_id == UNMPDeviceType.odu100:
                                config_profile_id = obj_reconcilation.reconcilation_controller(
                                    host.host_id, 'odu100', 'odu100_', datetime.now(), False, updated_by)
                            elif device_type_id == UNMPDeviceType.idu4:
                                config_profile_id = idu_obj_reconciliation.new_device_reconcilation_controller(
                                    host.host_id, 'idu4', 'idu_', False, updated_by)
                            elif device_type_id == UNMPDeviceType.ap25:
                                config_profile_id = ap_obj_reconciliation.default_configuration_added(
                                    host.host_id, 'ap25', False)

                            if device_type_id == "odu100":
                                temp_conf_id = config_profile_id['result'][0]
                                rec = 0
                            else:
                                if config_profile_id != None and type(config_profile_id) == tuple and len(config_profile_id) == 2:
                                    # host_data[0].reconcile_health =
                                    # config_profile_id[1]
                                    temp_conf_id = config_profile_id[0]
                                    rec = 0
                                elif config_profile_id != None:
                                    temp_conf_id = config_profile_id
                                    rec = 0
                            # end - recreate config profile
                            # service recreation
                            services_list = self.get_services_from_templates(
                                device_type_id)
                            for srv in services_list:
                                # [service_description,check_command,max_check_attempts,normal_check_interval,retry_check_interval]
                                service = HostServices(
                                    host.host_id, srv.service_description, srv.check_command,
                                                       srv.max_check_attempts, srv.normal_check_interval, srv.retry_check_interval, 0)
                                session.add(service)
                                # if(flag_nagios_call==0):
                                #    ncbll = NagioConfigurationBll()
                                #    wnc = ncbll.write_nagios_config(nms_instance)
                                #    condition_nagios =  isinstance(wnc, bool)
                                if(flag_nagios_call == 1):
                                    n_bll = NagiosBll()
                                    wnc = n_bll.add_new_service(
                                        str(host.host_name), host.host_alias, srv.service_description,
                                                                srv.max_check_attempts, srv.normal_check_interval, srv.retry_check_interval, srv.check_command)
                                    condition_nagios = wnc["success"] == 0
                            # end - service recreation
                        # end - if device type is changed

                                # Firmware change for odu100 than truncate the
                                # odu100_raAclConfigTable table
                        if device_type_id == "odu100":
                            sel_query = "select firmware_mapping_id from hosts where host_id= '%s'" % (host_id)
                            cursor.execute(sel_query)
                            result = cursor.fetchall()
                            if len(result) > 0 and result[0][0] != None and result[0][0] != "" and firmware_mapping_id != result[0][0]:
                                del_query = " TRUNCATE TABLE  odu100_raAclConfigTable"  # empty the ACL table when firmware will update.
                                cursor.execute(del_query)
                            # Firmware changes code finish here

                        cursor.close()
                        db.commit()
                        db.close()

                        hosts = session.query(
                            Hosts).filter(Hosts.host_id == host_id).all()
                        if len(hosts) == 1:
                            host = hosts[0]
                            host.config_profile_id = temp_conf_id
                            host.host_name = host_name
                            host.host_alias = host_alias
                            host.ip_address = ip_address
                            host.mac_address = mac_address
                            host.device_type_id = device_type_id
                            host.netmask = netmask
                            host.gateway = gateway
                            host.primary_dns = primary_dns
                            host.secondary_dns = secondary_dns
                            host.dns_state = dns_state
                            host.is_deleted = is_deleted
                            host.updated_by = updated_by
                            host.host_state_id = host_state_id
                            host.priority_id = priority_id
                            host.host_vendor_id = host_vendor_id
                            host.host_os_id = host_os_id
                            host.http_username = http_username
                            host.http_password = http_password
                            host.http_port = http_port
                            host.ssh_username = ssh_username
                            host.ssh_password = ssh_password
                            host.ssh_port = ssh_port
                            host.snmp_read_community = snmp_read_community
                            host.snmp_write_community = snmp_write_community
                            host.snmp_port = snmp_port
                            host.snmp_trap_port = snmp_trap_port
                            host.snmp_version_id = snmp_version_id
                            host.comment = comment
                            host.parent_name = parent_name
                            host.lock_status = lock_status
                            host.is_localhost = 0
                            host.reconcile_health = rec
                            host.firmware_mapping_id = firmware_mapping_id

                            host_assets = session.query(HostAssets).filter(
                                HostAssets.host_asset_id == host.host_asset_id).all()

                            if len(host_assets) == 1:
                                host_asset = host_assets[0]
                                host_asset.longitude = longitude
                                host_asset.latitude = latitude
                                host_asset.serial_number = serial_number
                                host_asset.hardware_version = hardware_version
                                host_asset.ra_mac = ra_mac

                            hostgroup_obj = session.query(HostsHostgroups).filter(
                                HostsHostgroups.host_id == host_id).all()
                            for hg_obj in hostgroup_obj:
                                hg_obj.hostgroup_id = hostgroup
                            # edit host status entry
                            host_status = session.query(HostStatus).filter(
                                HostStatus.host_id == host_id).all()
                            if len(host_status) == 1:
                                host_stat = host_status[0]
                                host_stat.status = '0'
                            elif len(host_status) == 0:
                                # add host status default entry
                                host_status = HostStatus(
                                    ip_address, host_id, '0', 0)
                                session.add(host_status)
                                # END - add host status default entry
                            # END edit host status entry
                            session.commit()
                        # ra_mac and node type and master mac address
                        if UNMPDeviceType.odu16 == device_type_id:
                            ra_mac_table_obj = session.query(GetOdu16RaStatusTable).filter(
                                GetOdu16RaStatusTable.host_id == host.host_id).all()
                            if len(ra_mac_table_obj) > 0:
                                ra_mac_table_obj[0].ra_mac_address = ra_mac
                            else:
                                ra_status_table = GetOdu16RaStatusTable(
                                    host.host_id, 0, ra_mac)
                                session.add(ra_status_table)

                            node_type_table_obj = session.query(GetOdu16_ru_conf_table).filter(
                                GetOdu16_ru_conf_table.host_id == host.host_id).all()
                            if len(node_type_table_obj) > 0:
                                node_type_table_obj[
                                    0].default_node_type = node_type
                            else:
                                ru_conf_table = GetOdu16_ru_conf_table(
                                    host.host_id, 0, None, node_type, None)
                                session.add(ru_conf_table)

                            if master_id != "" and master_id != None:
                                master_mac_table_obj = MasterSlaveLinking(
                                    master_id, host.host_id)
                                session.add(master_mac_table_obj)
                            session.commit()

                        elif UNMPDeviceType.odu100 == device_type_id:
                            ra_mac_table_obj = session.query(Odu100RaStatusTable).filter(
                                Odu100RaStatusTable.host_id == host.host_id).all()
                            if len(ra_mac_table_obj) > 0:
                                ra_mac_table_obj[0].raMacAddress = ra_mac
                            else:
                                ra_status_table = Odu100RaStatusTable(
                                    host.host_id, 1, None, ra_mac, None, None, None)
                                session.add(ra_status_table)

                            node_type_table_obj = session.query(Odu100RuConfTable).filter(
                                Odu100RuConfTable.config_profile_id == temp_conf_id).all()
                            if len(node_type_table_obj) > 0:
                                node_type_table_obj[
                                    0].defaultNodeType = node_type
                            else:
                                if temp_conf_id != None:
                                    ru_conf_table = Odu100RuConfTable(
                                        temp_conf_id, 1, None, node_type, None, None, None, None, 0)
                                    session.add(ru_conf_table)

                            if master_id != "" and master_id != None:
                                master_mac_table_obj = session.query(MasterSlaveLinking).filter(
                                    MasterSlaveLinking.slave == host.host_id).all()
                                if len(master_mac_table_obj) > 0:
                                    master_mac_table_obj[0].master = master_id
                                else:
                                    master_mac_table_obj = MasterSlaveLinking(
                                        master_id, host.host_id)
                                    session.add(master_mac_table_obj)
                            # manage vlan
                            vlan_table_obj = session.query(Odu100IpConfigTable).filter(
                                Odu100IpConfigTable.config_profile_id == temp_conf_id).all()
                            if len(vlan_table_obj) > 0:
                                vlan_table_obj[
                                    0].managementMode = odu100_management_mode
                                vlan_table_obj[
                                    0].managementVlanTag = odu100_vlan_tag
                            else:
                                if odu100_management_mode != None and odu100_vlan_tag != None:
                                    vlan_table = Odu100IpConfigTable(
                                        temp_conf_id, 1, None, ip_address, netmask, gateway, dns_state,
                                                                     odu100_management_mode, odu100_vlan_tag)
                                    session.add(vlan_table)
                            # end - manage vlan
                            session.commit()
                        elif UNMPDeviceType.ccu == device_type_id:
                            # manage vlan
                            vlan_table_obj = session.query(CcuNetworkConfigurationTable).filter(
                                CcuNetworkConfigurationTable.host_id == host.host_id).all()
                            if len(vlan_table_obj) > 0:
                                vlan_table_obj[
                                    0].ccuNCDHCPNetMask = ccu_dhcp_netmask
                            else:
                                if ccu_dhcp_netmask != None:
                                    vlan_table = CcuNetworkConfigurationTable(
                                        host.host_id, 0, mac_address, ip_address, netmask, "", "", ccu_dhcp_netmask, gateway)
                                    session.add(vlan_table)
                            # end - manage vlan
                            session.commit()
                        # ncbll = NagioConfigurationBll()
                        # wnc = ncbll.write_nagios_config(nms_instance)

                        if(flag_nagios_call == 0):
                            ncbll = NagioConfigurationBll()
                            wnc = ncbll.write_nagios_config(nms_instance)
                            condition_nagios = isinstance(wnc, bool)
                        else:
                            n_bll = NagiosBll()
                            wnc = n_bll.edit_old_host(
                                host_name, host_alias, ip_address, parent_name, hostgroup)
                            condition_nagios = wnc["success"] == 0
                        if (condition_nagios):
                            if flag_nagios_call:
                                SystemSetting.reload_nagios_config()
                        # if isinstance(wnc, bool):
                            el = EventLog()
                            el.log_event(
                                "Edit Host '%s' Details." % (ip_address), updated_by)
                            return host.host_id  # [host.host_id,device_type_id,temp_conf_id,node_type]
                        else:
                            err = ErrorMessages()
                            err.error_msg = err.nagios_config_error
                            return err
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.no_record_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.duplicate_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            # import traceback
            # return traceback.format_exc()
            return e
        finally:
            session.close()                     # close the session object

    def add_deleted_host(self, host_ids, nms_instance, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            msg = ""
            for host_i in range(0, len(host_ids)):
                deleted_host = session.query(
                    Host.host_name, Hosts.host_alias, Host.ip_address,
                                             Host.mac_address).filter(Hosts.host_id == host_ids[host_i]).all()
                if len(deleted_host) > 0:
                    d_host = deleted_host[0]
                    if self.is_duplicate_host_for_add(d_host.host_name, d_host.host_alias, d_host.ip_address, d_host.mac_address):
                        hosts = session.query(
                            Hosts).filter(Hosts.host_id == host_id).all()
                        if len(hosts) == 1:
                            host.is_deleted = 0
                            host.host_name = "host" + str(host.host_id)
                            session.commit()
                            # ncbll = NagioConfigurationBll()
                            # wnc = ncbll.write_nagios_config(nms_instance)
                            # if isinstance(wnc, bool):
                            if(flag_nagios_call == 0):
                                ncbll = NagioConfigurationBll()
                                wnc = ncbll.write_nagios_config(nms_instance)
                                condition_nagios = isinstance(wnc, bool)
                            else:
                                n_bll = NagiosBll()
                                wnc = n_bll.add_new_host(
                                    hosts.host_name, hosts.host_alias, hosts.ip_address, hosts.parent_name)
                                condition_nagios = wnc["success"] == 0
                            # work here ... test it once

                            if (condition_nagios):
                                if(flag_nagios_call == 1):
                                    SystemSetting.reload_nagios_config()
                                return host.host_id
                            else:
                                err = ErrorMessages()
                                err.error_msg = err.nagios_config_error
                                return err
                        else:
                            err = ErrorMessages()
                            err.error_msg = err.no_record_error
                            return err
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.duplicate_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.no_record_error
                    return err
            # end for loop
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def delete(self, host_ids, nms_instance, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            # get localhost
            localhost = session.query(
                Hosts.host_id).filter(Hosts.is_localhost == 1).all()
            localhost_count = len(localhost)
            if localhost_count > 0:
                localhost_id = localhost[0].host_id

                host_childs = session.query(
                    Hosts).filter(Hosts.parent_name.in_(host_ids)).all()
                for hc in host_childs:
                    hc.parent_name = localhost_id
                session.commit()

                hosts = session.query(Hosts).filter(Hosts.host_id.in_(
                    host_ids)).all()          # execute query and fetch data
                host_count = len(hosts)
                if host_count > 0:
                    el = EventLog()
                    for hs in hosts:
                        el.log_event("Host '%s' Deleted [You can view it in deleted host]." %
                                     (hs.ip_address), updated_by)
                        hs.is_deleted = 1
                        hs.updated_by = updated_by
                        if(flag_nagios_call == 1):
                            n_bll = NagiosBll()
                            wnc = n_bll.delete_old_host(hs.host_name)
                            condition_nagios = wnc["success"] == 0
                    session.commit()
                    if(flag_nagios_call == 0):
                        ncbll = NagioConfigurationBll()
                        wnc = ncbll.write_nagios_config(nms_instance)
                        condition_nagios = isinstance(wnc, bool)
                    # ncbll = NagioConfigurationBll()
                    # wnc = ncbll.write_nagios_config(nms_instance)
    #                   n_bll=NagiosBll()
#                    wnc=n_bll.delete_old_host(host_name)
                    if (condition_nagios):
                        if(flag_nagios_call == 1):
                            SystemSetting.reload_nagios_config()
                    # if isinstance(wnc, bool):
                        return host_count
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.nagios_config_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.no_record_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def delete_deleted_host(self, host_ids, nms_instance, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            # get localhost
            localhost = session.query(
                Hosts.host_id).filter(Hosts.is_localhost == 1).all()
            localhost_count = len(localhost)
            if localhost_count > 0:
                localhost_id = localhost[0].host_id

                host_childs = session.query(
                    Hosts).filter(Hosts.parent_name.in_(host_ids)).all()
                for hc in host_childs:
                    hc.parent_name = localhost_id
                session.commit()

                hosts = session.query(Hosts).filter(Hosts.host_id.in_(
                    host_ids)).all()          # execute query and fetch data
                host_count = len(hosts)
                if host_count > 0:
                    db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
                    el = EventLog()
                    for hst in hosts:
                        cursor = db.cursor()
                        if hst.config_profile_id != None:
                            cursor.execute("delete from config_profiles where config_profile_id = %s" %
                                           hst.config_profile_id)
                        if hst.host_id != None:
                            # trap & alarm table will empty
                            cursor.execute(
                                "delete from trap_alarms where agent_id = '%s'" % hst.ip_address)
                            cursor.execute(
                                "delete from trap_alarm_clear where agent_id = '%s'" % hst.ip_address)
                            cursor.execute(
                                "delete from trap_alarm_current where agent_id = '%s'" % hst.ip_address)
                            cursor.execute(
                                "delete from system_alarm_table where agent_id = '%s'" % hst.ip_address)
                            cursor.execute(
                                "delete from host_status where host_ip = '%s'" % hst.ip_address)

                            if hst.device_type_id == UNMPDeviceType.odu16:
                                # odu 16 get table will empty
                                cursor.execute(
                                    "delete from get_odu16_nw_interface_statistics_table where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from get_odu16_peer_node_status_table where host_id = %s" % hst.host_id)
                                cursor.execute("delete from get_odu16_ra_tdd_mac_statistics_entry where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from get_odu16_synch_statistics_table where host_id = %s" % hst.host_id)
                                # odu 16 analyze table will empty
                                cursor.execute(
                                    "delete from analyze_get_odu16_nw_interface_statistics_table where host_id = %s" % hst.host_id)
                                cursor.execute("delete from analyze_get_odu16_peer_node_status_table where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from analyze_get_odu16_ra_tdd_mac_statistics_entry where host_id = %s" % hst.host_id)
                                cursor.execute("delete from analyze_get_odu16_synch_statistics_table where host_id = %s" % hst.host_id)

                            if hst.device_type_id == UNMPDeviceType.odu100:
                                # odu 100 get table will empty
                                cursor.execute(
                                    "delete from odu100_nwInterfaceStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from odu100_raTddMacStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute("delete from odu100_raScanListTable where host_id = %s" %
                                               hst.host_id)
                                cursor.execute(
                                    "delete from odu100_synchStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from odu100_peerNodeStatusTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from odu100_swStatusTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from odu100_hwDescTable where host_id = %s" % hst.host_id)
                                # odu 100 analyze table will empty
                                cursor.execute(
                                    "delete from analyze_odu100_nwInterfaceStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute("delete from analyze_odu100_peerNodeStatusTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from analyze_odu100_raTddMacStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from analyze_odu100_synchStatisticsTable where host_id = %s" % hst.host_id)

                            if hst.device_type_id == UNMPDeviceType.idu4:
                                # idu 4 get table will empty
                                cursor.execute(
                                    "delete from idu_tdmoipNetworkInterfaceStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from idu_iduNetworkStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from idu_e1PortStatusTable where host_id = %s" % hst.host_id)
                                cursor.execute("delete from idu_linkStatusTable where host_id = %s" %
                                               hst.host_id)
                                cursor.execute(
                                    "delete from idu_portSecondaryStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from idu_portstatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute(
                                    "delete from idu_swPrimaryPortStatisticsTable where host_id = %s" % hst.host_id)
                                # idu 4 analyze table will empty
                                cursor.execute("delete from analyze_idu_portSecondaryStatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute("delete from analyze_idu_portstatisticsTable where host_id = %s" % hst.host_id)
                                cursor.execute("delete from analyze_idu_swPrimaryPortStatisticsTable where host_id = %s" % hst.host_id)

                            if hst.device_type_id == UNMPDeviceType.ap25:
                                # ap get table will empty
                                cursor.execute(
                                    "delete from ap25_statisticsTable where host_id = %s" % hst.host_id)

                        if hst.host_asset_id != None:
                            cursor.execute("delete from host_assets where host_asset_id = %s" %
                                           hst.host_asset_id)
                        cursor.execute("delete from master_slave_linking where master = %s OR slave = %s" %
                                       (hst.host_id, hst.host_id))
                        cursor.execute(
                            "delete from hosts where host_id = %s" % hst.host_id)
                        cursor.close()
                        el.log_event(
                            "Host '%s' Deleted." % (hst.ip_address), updated_by)
                    db.commit()
                    db.close()
                    # ncbll = NagioConfigurationBll()
                    # wnc = ncbll.write_nagios_config(nms_instance)
                    wnc = True
                    if(flag_nagios_call == 0):
                        ncbll = NagioConfigurationBll()
                        wnc = ncbll.write_nagios_config(nms_instance)

                    if isinstance(wnc, bool):
                        return host_count
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.nagios_config_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.no_record_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object

    def validate(self, host_name, host_alias, ip_address, mac_address, device_type_id, netmask, gateway, primary_dns, secondary_dns, odu100_management_mode, odu100_vlan_tag, idu4_management_mode, idu4_vlan_tag, idu4_tdm_ip, ccu_dhcp_netmask, host_state_id, priority_id, host_vendor_id, host_os_id, http_username, http_password, http_port, ssh_username, ssh_password, ssh_port, snmp_read_community, snmp_write_community, snmp_port, snmp_trap_port, comment, longitude, latitude, serial_number, hardware_version):
        # Validation.is_required(host_name) and
        if Validation.is_alpha_numeric(host_name) and Validation.no_space(host_name) and Validation.is_required(host_alias) and Validation.is_alpha_numeric(host_alias) and \
           Validation.is_required(ip_address) and Validation.is_valid_ip(ip_address) and Validation.is_required(mac_address) and Validation.is_valid_mac(mac_address) and \
           Validation.is_required(device_type_id) and Validation.is_required(netmask) and Validation.is_required(gateway) and Validation.is_valid_netmask(netmask) and Validation.is_valid_ip(gateway) and \
           Validation.is_valid_ip(primary_dns) and Validation.is_valid_ip(secondary_dns) and Validation.is_required(host_state_id) and \
           Validation.is_required(priority_id) and Validation.is_alpha_numeric(http_username) and Validation.is_alpha_numeric(ssh_username) and Validation.is_required(host_vendor_id) and Validation.is_required(host_os_id) and \
           Validation.is_number(http_port) and Validation.is_number(ssh_port) and Validation.is_alpha_numeric(snmp_read_community) and Validation.is_alpha_numeric(snmp_write_community) and \
           Validation.is_number(snmp_port) and Validation.is_number(snmp_trap_port) and Validation.is_alpha_numeric(comment) and \
           Validation.is_number(longitude) and Validation.is_required(longitude) and Validation.is_number(latitude) and Validation.is_required(latitude) and Validation.is_alpha_numeric(serial_number) and Validation.is_alpha_numeric(hardware_version):
            if UNMPDeviceType.ap25 == device_type_id:
                if Validation.is_valid_ip(primary_dns) and Validation.is_valid_ip(secondary_dns):
                    return True
                else:
                    return False
            elif UNMPDeviceType.odu16 == device_type_id:
                return True
            elif UNMPDeviceType.odu100 == device_type_id:
                if Validation.is_required(odu100_management_mode) and Validation.is_integer(odu100_management_mode):
                    if int(odu100_management_mode) == 1:
                        if Validation.is_integer(odu100_vlan_tag) and Validation.is_required(odu100_vlan_tag) and int(odu100_vlan_tag) <= 4094 and int(odu100_vlan_tag) > 0:
                            return True
                        else:
                            return False
                    else:
                        return True
                else:
                    return False
            elif UNMPDeviceType.idu4 == device_type_id:
                if Validation.is_required(idu4_management_mode) and Validation.is_integer(idu4_management_mode):
                    if int(idu4_management_mode) == 1:
                        if Validation.is_required(idu4_vlan_tag) and Validation.is_integer(idu4_vlan_tag) and Validation.is_required(idu4_tdm_ip) and Validation.is_valid_ip(idu4_tdm_ip) and int(idu4_vlan_tag) <= 4094 and int(idu4_vlan_tag) > 0:
                            return True
                        else:
                            return False
                    else:
                        return True
                else:
                    return False
            elif UNMPDeviceType.idu8 == device_type_id:
                return True
            elif UNMPDeviceType.swt4 == device_type_id:
                return True
            elif UNMPDeviceType.ccu == device_type_id:
                if Validation.is_required(ccu_dhcp_netmask) and Validation.is_valid_ip(ccu_dhcp_netmask):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def is_duplicate_host_for_add(self, host_name, host_alias, ip_address, mac_address):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            host_count = session.query(Hosts).filter(and_(
                or_(Hosts.host_alias == host_alias, Hosts.ip_address == ip_address, Hosts.mac_address == mac_address), Hosts.is_deleted == 0)).count()
            if host_count == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()                     # close the session object

    def is_duplicate_host_for_edit(self, host_id, host_name, host_alias, ip_address, mac_address):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            host_count = session.query(Hosts).filter(and_(Hosts.host_id != host_id, or_(
                Hosts.host_name == host_name, Hosts.host_alias == host_alias, Hosts.ip_address == ip_address, Hosts.mac_address == mac_address), Hosts.is_deleted == 0)).count()
            if host_count == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()                     # close the session object

    def host_parents(self, host_id=None):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hosts = session.query(
                Hosts.host_id, Hosts.is_localhost, Hosts.host_name, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address).filter(and_(Hosts.is_deleted == 0,
                                  Hosts.host_id != host_id)).order_by(Hosts.host_alias).all()          # execute query and fetch data
            return hosts
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def host_parents2(self, user_id, host_id=None):

        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "SELECT DISTINCT hosts.host_id AS hosts_host_id, hosts.is_localhost AS hosts_is_localhost, hosts.host_name AS hosts_host_name, hosts.host_alias AS hosts_host_alias, hosts.ip_address AS hosts_ip_address, hosts.mac_address AS hosts_mac_address \
FROM hosts, users_groups, hostgroups_groups, hosts_hostgroups \
WHERE hosts.is_deleted = '0' AND hosts.host_id IS NOT NULL AND users_groups.user_id = '%s' AND users_groups.group_id = hostgroups_groups.group_id AND hosts_hostgroups.hostgroup_id = hostgroups_groups.hostgroup_id AND hosts.host_id = hosts_hostgroups.host_id OR hosts.ip_address = 'localhost' ORDER BY hosts.host_name" % (user_id)
            cursor.execute(sql)
            hosts = cursor.fetchall()
            cursor.close()
            return list(hosts)
        except Exception, e:
            return e
        finally:
            if isinstance(db, MySQLdb.connection):
                db.close()                     # close the session object

    def host_hostgroups(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hostgroups = session.query(Hostgroups.hostgroup_id, Hostgroups.hostgroup_name, Hostgroups.hostgroup_alias).filter(
                Hostgroups.is_deleted == 0).order_by(Hostgroups.hostgroup_alias).all()          # execute query and fetch data
            return hostgroups
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def host_hostgroups2(self, userid):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hostgroups = session.query(Hostgroups.hostgroup_id, Hostgroups.hostgroup_name, Hostgroups.hostgroup_alias).filter(
                and_(Hostgroups.is_deleted == 0, UsersGroups.user_id == '%s' % (userid), UsersGroups.group_id == HostgroupsGroups.group_id, HostgroupsGroups.hostgroup_id == Hostgroups.hostgroup_id)).order_by(Hostgroups.hostgroup_alias).all()          # execute query and fetch data
            return hostgroups
        except Exception, e:
            return e
        finally:
            session.close()

    def host_vendors(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            vendors = session.query(HostVendor.host_vendor_id, HostVendor.vendor_name).filter(
                HostVendor.is_deleted == 0).order_by(HostVendor.vendor_name).all()          # execute query and fetch data
            return vendors
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def host_os(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            os = session.query(HostOs.host_os_id, HostOs.os_name).filter(HostOs.is_deleted == 0).order_by(
                HostOs.sequence).all()          # execute query and fetch data
            return os
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def host_priority(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            priority = session.query(Priority.priority_id, Priority.priority_name).filter(
                Priority.is_deleted == 0).order_by(Priority.sequence).all()          # execute query and fetch data
            return priority
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def host_state(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            state = session.query(HostStates.host_state_id, HostStates.state_name).filter(
                HostStates.is_deleted == 0).order_by(HostStates.sequence).all()          # execute query and fetch data
            return state
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def device_type(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            device = session.query(DeviceType.device_type_id, DeviceType.device_name).filter(
                DeviceType.is_deleted == 0).order_by(DeviceType.sequence).all()          # execute query and fetch data
            return device
        except Exception, e:
            return e
        finally:
            session.close()

    def change_device_network_details(self, device_dict):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        result = {}
        chk = 0
        if len(device_dict) > 0:
            sqlalche_obj = Session()
            host_details = sqlalche_obj.query(
                Hosts).filter(Hosts.host_id == device_dict["host_id"]).all()
            if len(host_details) > 0:
                if host_details[0].config_profile_id == "" or host_details[0].config_profile_id == None:
                    result = {"success": 1, "result": "No Configuration exist"}
                    sqlalche_obj.close()
                    return result
                else:
                    change_net_config = {}
                    if device_dict["device_type_id"] == UNMPDeviceType.odu16:
                        ip_oid = ["1.3.6.1.4.1.26149.2.2.9.1.3.1",
                            "IpAddress", device_dict["ip_address"]]
                        netmask_oid = ["1.3.6.1.4.1.26149.2.2.9.1.4.1",
                            "IpAddress", device_dict["ip_network_mask"]]
                        gateway_oid = ["1.3.6.1.4.1.26149.2.2.9.1.5.1",
                            "IpAddress", device_dict["ip_gateway"]]
                        autoIp = ["1.3.6.1.4.1.26149.2.2.9.1.6.1",
                            "Integer32", device_dict["dhcp"]]
                        admin_state = [
                            '1.3.6.1.4.1.26149.2.2.9.1.2.1', 'Integer32', 0]
                        dic_odu = {'ip': ip_oid, 'netmask':
                            netmask_oid, 'gateway': gateway_oid, 'autoip': autoIp}
                        admin_dic = {'admin-1': admin_state}
                        change_net_config = pysnmp_set(dic_odu, host_details[0].ip_address, host_details[0]
                                                       .snmp_port, host_details[0].snmp_write_community, admin_dic)
                        admin_state = [
                            '1.3.6.1.4.1.26149.2.2.9.1.2.1', 'Integer32', 1]
                        admin_dic = {'admin': admin_state}
                        change_admin_state = pysnmp_set(
                            admin_dic, host_details[0].ip_address, host_details[0].snmp_port, host_details[0].snmp_write_community)

                    if device_dict["device_type_id"] == UNMPDeviceType.odu100:
                        ip_oid = ["1.3.6.1.4.1.26149.2.2.9.1.3.1",
                            "IpAddress", device_dict["ip_address"]]
                        netmask_oid = ["1.3.6.1.4.1.26149.2.2.9.1.4.1",
                            "IpAddress", device_dict["ip_network_mask"]]
                        gateway_oid = ["1.3.6.1.4.1.26149.2.2.9.1.5.1",
                            "IpAddress", device_dict["ip_gateway"]]
                        autoIp = ["1.3.6.1.4.1.26149.2.2.9.1.6.1",
                            "Integer32", device_dict["dhcp"]]
                        vlan_management = ['1.3.6.1.4.1.26149.2.2.9.1.7.1',
                            'Integer32', device_dict["odu100_management_mode"]]
                        vlan_tag = ['1.3.6.1.4.1.26149.2.2.9.1.8.1',
                            'Integer32', device_dict["odu100_vlan_tag"]]
                        admin_state = [
                            '1.3.6.1.4.1.26149.2.2.9.1.2.1', 'Integer32', 0]
                        dic_odu = {'ip': ip_oid, 'netmask': netmask_oid, 'gateway': gateway_oid, 'autoip':
                            autoIp, 'vlan_management': vlan_management, 'vlan_tag': vlan_tag}
                        admin_dic = {'admin-1': admin_state}
                        change_net_config = pysnmp_set(dic_odu, host_details[0].ip_address, host_details[0]
                                                       .snmp_port, host_details[0].snmp_write_community, admin_dic)
                        admin_state = [
                            '1.3.6.1.4.1.26149.2.2.9.1.2.1', 'Integer32', 1]
                        admin_dic = {'admin': admin_state}
                        change_admin_state = pysnmp_set(
                            admin_dic, host_details[0].ip_address, host_details[0].snmp_port, host_details[0].snmp_write_community)

                    if device_dict["device_type_id"] == UNMPDeviceType.idu4:
                        ip_oid = ["1.3.6.1.4.1.26149.2.1.2.4.1.2.0",
                            "IpAddress", device_dict["ip_address"]]
                        netmask_oid = ["1.3.6.1.4.1.26149.2.1.2.4.1.3.0",
                            "IpAddress", device_dict["ip_network_mask"]]
                        gateway_oid = ["1.3.6.1.4.1.26149.2.1.2.4.1.4.0",
                            "IpAddress", device_dict["ip_gateway"]]
                        autoIp = ["1.3.6.1.4.1.26149.2.1.2.4.1.5.0",
                            "Integer32", device_dict["dhcp"]]
                        dic_odu = {'ip': ip_oid, 'netmask':
                            netmask_oid, 'gateway': gateway_oid, 'autoip': autoIp}
                        change_net_config = pysnmp_set(
                            dic_odu, host_details[0].ip_address, host_details[0].snmp_port, host_details[0].snmp_write_community)

                    if device_dict["device_type_id"] == UNMPDeviceType.ccu:
                        netmask_oid = ["1.3.6.1.4.1.26149.3.5.1.4.0",
                            "OctetString", device_dict["ip_network_mask"]]
                        gateway_oid = ["1.3.6.1.4.1.26149.3.5.1.8.0",
                            "OctetString", device_dict["ip_gateway"]]
                        dhcp_netmask = ["1.3.6.1.4.1.26149.3.5.1.7.0",
                            "OctetString", device_dict["ccu_dhcp_netmask"]]
                        dic_odu = {'netmask': netmask_oid,
                            'gateway': gateway_oid, 'dhcp_netmask': dhcp_netmask}
                        change_net_config = pysnmp_seter(dic_odu, host_details[0].ip_address, int(
                            host_details[0].snmp_port), host_details[0].snmp_write_community)

                    if device_dict["device_type_id"] == UNMPDeviceType.ap25:
                        ip_oid = ["1.3.6.1.4.1.26149.10.1.2.1.0",
                            "OctetString", device_dict["ip_address"]]
                        netmask_oid = ["1.3.6.1.4.1.26149.10.1.2.2.0",
                            "OctetString", device_dict["ip_network_mask"]]
                        gateway_oid = ["1.3.6.1.4.1.26149.10.1.2.3.0",
                            "OctetString", device_dict["ip_gateway"]]
                        primarydns = ["1.3.6.1.4.1.26149.10.1.2.4.0",
                            "OctetString", device_dict["primarydns"]]
                        secondarydns = ["1.3.6.1.4.1.26149.10.1.2.5.0",
                            "OctetString", device_dict["secondarydns"]]
                        dic_ap = {
                            'ip': ip_oid, 'netmask': netmask_oid, 'gateway': gateway_oid,
                            'primarydns': primarydns, 'secondarydns': secondarydns}
                        change_net_config = pysnmp_set(
                            dic_ap, host_details[0].ip_address, host_details[0].snmp_port, host_details[0].snmp_write_community)
                    for i in range(0, 3):
                        if device_dict["device_type_id"] == UNMPDeviceType.ccu:
                            if change_net_config["success"] == 0:
                                break

                        if snmp_ping_ccu(str(device_dict["ip_address"]), str(host_details[0].snmp_read_community), int(host_details[0].snmp_port)) == 0:
                            change_net_config = {"result": {'ip': 0,
                                'netmask': 0, 'gateway': 0, 'autoip': 0}, "success": 0}
                            break
                        else:
                            change_net_config = {"success": 1}
                            result = {"result": "No response From device"}
                            time.sleep(5)
                            continue

                    if change_net_config["success"] == 0:
                        for i in change_net_config["result"]:
                            if change_net_config["result"][i] == 0:
                                # print chk
                                chk = 1
                            else:
                                chk = 2
                                break
                    else:
                        result = {"success": 1}
                        sqlalche_obj.close()
                        return result
                    if chk == 1:
                        if device_dict["device_type_id"] == UNMPDeviceType.odu16:
                            odu16_ip_details = sqlalche_obj.query(SetOdu16IPConfigTable).filter(
                                SetOdu16IPConfigTable.config_profile_id == host_details[0].config_profile_id).all()
                            if len(odu16_ip_details) > 0:
                                odu16_ip_details[
                                    0].ip_address = device_dict["ip_address"]
                                odu16_ip_details[
                                    0].ip_network_mask = device_dict["ip_network_mask"]
                                odu16_ip_details[
                                    0].ip_network_mask = device_dict["ip_gateway"]
                                odu16_ip_details[
                                    0].ip_network_mask = device_dict["dhcp"]
                            else:
                                odu16_detail = SetOdu16IPConfigTable(None, host_details[0].config_profile_id, 1, device_dict[
                                                                     "ip_address"], device_dict["ip_network_mask"], device_dict["ip_gateway"], device_dict["dhcp"])
                                sqlalche_obj.add(odu16_detail)
                            result = {"success": 0}
                        elif device_dict["device_type_id"] == UNMPDeviceType.odu100:

                            odu16_ip_details = sqlalche_obj.query(
                                Odu100IpConfigTable).filter(Odu100IpConfigTable.config_profile_id == host_details[0].config_profile_id).all()
                            if len(odu16_ip_details) > 0:
                                odu16_ip_details[
                                    0].ipAddress = device_dict["ip_address"]
                                odu16_ip_details[
                                    0].ipNetworkMask = device_dict["ip_network_mask"]
                                odu16_ip_details[
                                    0].ipDefaultGateway = device_dict["ip_gateway"]
                                odu16_ip_details[
                                    0].autoIpConfig = device_dict["dhcp"]
                            else:
                                odu100_detail = Odu100IpConfigTable(None, host_details[0].config_profile_id, 0, 1, device_dict[
                                                                    "ip_address"], device_dict["ip_network_mask"], device_dict["ip_gateway"], device_dict["dhcp"])
                                sqlalche_obj.add(odu100_detail)

                            result = {"success": 0}
                        elif device_dict["device_type_id"] == UNMPDeviceType.idu4:
                            odu16_ip_details = sqlalche_obj.query(IduNetworkConfigurationsTable).filter(
                                IduNetworkConfigurationsTable.config_profile_id == host_details[0].config_profile_id).all()
                            if len(odu16_ip_details) > 0:
                                odu16_ip_details[
                                    0].ipaddr = device_dict["ip_address"]
                                odu16_ip_details[
                                    0].netmask = device_dict["ip_network_mask"]
                                odu16_ip_details[
                                    0].gateway = device_dict["ip_gateway"]
                                odu16_ip_details[
                                    0].autoIpConfig = device_dict["dhcp"]
                            else:
                                idu_detail = IduNetworkConfigurationsTable(None, host_details[0].config_profile_id, 0, 1, device_dict[
                                                                           "ip_address"], device_dict["ip_network_mask"], device_dict["ip_gateway"], device_dict["dhcp"])
                                sqlalche_obj.add(idu_detail)
                            result = {"success": 0}
                        elif device_dict["device_type_id"] == UNMPDeviceType.ap25:
                            ap25_details = sqlalche_obj.query(Ap25AccesspointIPsettings).filter(
                                Ap25AccesspointIPsettings.config_profile_id == host_details[0].config_profile_id).all()
                            if len(ap25_details) > 0:
                                ap25_details[
                                    0].lanIPaddress = device_dict["ip_address"]
                                ap25_details[
                                    0].lanSubnetMask = device_dict["ip_network_mask"]
                                ap25_details[
                                    0].lanGatewayIP = device_dict["ip_gateway"]
                                ap25_details[
                                    0].lanPrimaryDNS = device_dict["primarydns"]
                                ap25_details[
                                    0].lanSecondaryDNS = device_dict["secondarydns"]
                            else:
                                ap25_detail = Ap25AccesspointIPsettings(host_details[0].config_profile_id, device_dict["ip_address"], device_dict[
                                                                        "ip_network_mask"], device_dict["ip_gateway"], device_dict["primarydns"], device_dict["secondarydns"])
                                sqlalche_obj.add(ap25_detail)
                            result = {"success": 0}

                        elif device_dict["device_type_id"] == UNMPDeviceType.ccu:
                            result = {"success": 0}

                        sqlalche_obj.commit()
                        sqlalche_obj.close()
                        return result
                    else:
                        result = {"success": 1,
                            "result": "Values Not Set.Retry Again"}
                        sqlalche_obj.close()
                        return result
            else:
                result = {"success": 1, "result": "No Host Exist"}
                sqlalche_obj.close()
                return result
        else:
            result = {"success": 1, "result": "Parameter Not Proper"}
            return result

    def odu_master(self, device_type_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            device = []
            if device_type_id == UNMPDeviceType.odu16:
                device = session.query(
                    Hosts.ip_address, Hosts.mac_address, Hosts.host_id).filter(and_(Hosts.is_deleted == 0, GetOdu16_ru_conf_table.host_id == Hosts.host_id, or_(GetOdu16_ru_conf_table.default_node_type == 0,
                                       GetOdu16_ru_conf_table.default_node_type == 2), Hosts.device_type_id == device_type_id)).all()          # execute query and fetch data
            elif device_type_id == UNMPDeviceType.odu100:
                device = session.query(
                    Hosts.ip_address, Hosts.mac_address, Hosts.host_id).filter(and_(Hosts.is_deleted == 0, Odu100RuConfTable.config_profile_id == Hosts.config_profile_id, or_(Odu100RuConfTable.defaultNodeType == 0,
                                       Odu100RuConfTable.defaultNodeType == 2), Hosts.device_type_id == device_type_id)).all()          # execute query and fetch data
            return device
        except Exception, e:
            return e
        finally:
            session.close()

    def is_duplicate_host_with_ip_address(self, ip_address):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            host = session.query(Hosts.host_id).filter(
                and_(Hosts.is_deleted == 0, Hosts.ip_address == ip_address)).count()          # execute query and fetch data
            if host == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()

    def is_duplicate_host_with_host_alias(self, host_alias):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            host = session.query(Hosts.host_id).filter(
                and_(Hosts.is_deleted == 0, Hosts.host_alias == host_alias)).count()          # execute query and fetch data
            if host == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()

    def is_duplicate_host_with_mac_address(self, mac_address):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            host = session.query(Hosts.host_id).filter(
                and_(Hosts.is_deleted == 0, Hosts.mac_address == mac_address)).count()          # execute query and fetch data
            if host == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()


class VendorBll(object):
    def grid_view(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            vendors = session.query(HostVendor.host_vendor_id, HostVendor.vendor_name, HostVendor.description).filter(
                HostVendor.is_deleted == 0).order_by(HostVendor.vendor_name).all()          # execute query and fetch data
            return vendors
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def get_vendor_by_id(self, host_vendor_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            vendors = session.query(HostVendor.host_vendor_id, HostVendor.vendor_name, HostVendor.description).filter(
                HostVendor.host_vendor_id == host_vendor_id).all()          # execute query and fetch data
            if len(vendors) == 1:
                return vendors[0]
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def add(self, vendor_name, description, timestamp, created_by, creation_time, is_deleted, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if self.validate(vendor_name, description):
                if self.is_duplicate_vendor_for_add(vendor_name):
                    vendor = HostVendor(vendor_name, description, timestamp,
                                        created_by, creation_time, updated_by, is_deleted)
                    session.add(vendor)
                    session.commit()
                    el = EventLog()
                    el.log_event(
                        "Add New Vendor '%s'." % (vendor_name), updated_by)
                    return vendor.host_vendor_id
                else:
                    err = ErrorMessages()
                    err.error_msg = err.duplicate_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def edit(self, host_vendor_id, vendor_name, description, timestamp, is_deleted, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if self.validate(vendor_name, description):
                if self.is_duplicate_vendor_for_edit(host_vendor_id, vendor_name):
                    vendors = session.query(HostVendor).filter(
                        HostVendor.host_vendor_id == host_vendor_id).all()
                    if len(vendors) == 1:
                        vendor = vendors[0]
                        vendor.vendor_name = vendor_name
                        vendor.description = description
                        vendor.timestamp = timestamp
                        vendor.is_deleted = is_deleted
                        vendor.updated_by = updated_by
                        session.commit()
                        el = EventLog()
                        el.log_event(
                            "Vendor '%s' Details Updated." % (vendor_name), updated_by)
                        return vendor.host_vendor_id
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.no_record_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.duplicate_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def delete(self, vendor_ids, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            vendors = session.query(HostVendor).filter(HostVendor.host_vendor_id.in_(
                vendor_ids)).all()          # execute query and fetch data
            vendor_count = len(vendors)
            if vendor_count > 0:
                el = EventLog()
                for vd in vendors:
                    el.log_event("Vendor '%s' Deleted." %
                                 (vd.vendor_name), updated_by)
                    session.delete(vd)
                session.commit()
                return vendor_count
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def validate(self, vendor_name, description):
        if Validation.is_alpha_numeric(vendor_name) and Validation.is_required(vendor_name) and Validation.is_required(description) and Validation.is_alpha_numeric(description):
            return True
        else:
            return False

    def is_duplicate_vendor_for_add(self, vendor_name):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            vendor_count = session.query(HostVendor).filter(
                HostVendor.vendor_name == vendor_name).count()
            if vendor_count == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()                     # close the session object

    def is_duplicate_vendor_for_edit(self, host_vendor_id, vendor_name):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            vendor_count = session.query(HostVendor).filter(
                and_(HostVendor.host_vendor_id != host_vendor_id, HostVendor.vendor_name == vendor_name)).count()
            if vendor_count == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()                     # close the session object


class BlackListMacBll(object):
    def grid_view(self):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            black_list_macs = session.query(BlackListMacs.black_list_mac_id, BlackListMacs.mac_address, BlackListMacs.description).filter(
                BlackListMacs.is_deleted == 0).order_by(BlackListMacs.mac_address).all()          # execute query and fetch data
            return black_list_macs
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object

    def get_black_list_mac_by_id(self, black_list_mac_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            black_list_macs = session.query(BlackListMacs.black_list_mac_id, BlackListMacs.mac_address, BlackListMacs.description).filter(
                BlackListMacs.black_list_mac_id == black_list_mac_id).all()          # execute query and fetch data
            if len(black_list_macs) == 1:
                return black_list_macs[0]
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def add(self, mac_address, description, timestamp, created_by, creation_time, is_deleted, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if self.validate(mac_address, description):
                if self.is_duplicate_black_list_mac_for_add(mac_address):
                    black_list_mac = BlackListMacs(
                        mac_address, description, timestamp,
                                                   created_by, creation_time, updated_by, is_deleted)
                    session.add(black_list_mac)
                    session.commit()
                    el = EventLog()
                    el.log_event(
                        "Add New Black Listed Host '%s'." % (mac_address), updated_by)
                    return black_list_mac.black_list_mac_id
                else:
                    err = ErrorMessages()
                    err.error_msg = err.duplicate_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def edit(self, black_list_mac_id, mac_address, description, timestamp, is_deleted, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            if self.validate(mac_address, description):
                if self.is_duplicate_black_list_mac_for_edit(black_list_mac_id, mac_address):
                    black_list_macs = session.query(BlackListMacs).filter(
                        BlackListMacs.black_list_mac_id == black_list_mac_id).all()
                    if len(black_list_macs) == 1:
                        black_list_mac = black_list_macs[0]
                        black_list_mac.mac_address = mac_address
                        black_list_mac.description = description
                        black_list_mac.timestamp = timestamp
                        black_list_mac.is_deleted = is_deleted
                        black_list_mac.updated_by = updated_by
                        session.commit()
                        el = EventLog()
                        el.log_event(
                            "Black Listed Host '%s' Updated." % (mac_address), updated_by)
                        return black_list_mac.black_list_mac_id
                    else:
                        err = ErrorMessages()
                        err.error_msg = err.no_record_error
                        return err
                else:
                    err = ErrorMessages()
                    err.error_msg = err.duplicate_error
                    return err
            else:
                err = ErrorMessages()
                err.error_msg = err.validation_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def delete(self, black_list_mac_ids, updated_by):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            black_list_macs = session.query(BlackListMacs).filter(BlackListMacs.black_list_mac_id.in_(
                black_list_mac_ids)).all()          # execute query and fetch data
            black_list_mac_count = len(black_list_macs)
            if black_list_mac_count > 0:
                el = EventLog()
                for vd in black_list_macs:
                    el.log_event(
                        "Black Listed Host '%s' Deleted." % (mac_address), updated_by)
                    session.delete(vd)
                session.commit()
                return black_list_mac_count
            else:
                err = ErrorMessages()
                err.error_msg = err.no_record_error
                return err
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return err
        finally:
            session.close()                     # close the session object

    def validate(self, mac_address, description):
        if Validation.is_valid_mac(mac_address) and Validation.is_required(mac_address) and Validation.is_required(description) and Validation.is_alpha_numeric(description):
            return True
        else:
            return False

    def is_duplicate_black_list_mac_for_add(self, mac_address):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            black_list_mac_count = session.query(BlackListMacs).filter(
                BlackListMacs.mac_address == mac_address).count()
            if black_list_mac_count == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()                     # close the session object

    def is_duplicate_black_list_mac_for_edit(self, black_list_mac_id, mac_address):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            black_list_mac_count = session.query(BlackListMacs).filter(
                and_(BlackListMacs.black_list_mac_id != black_list_mac_id, BlackListMacs.mac_address == mac_address)).count()
            if black_list_mac_count == 0:
                return True
            else:
                return False
        except Exception, e:
            return False
        finally:
            session.close()                     # close the session object


class ServiceBll(object):
    def __init__(self, userid=None):
        self.userid = userid

    def grid_view(self, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, req_vars):
        # Session = sessionmaker(bind=engine)     # making session of our
        # current database
        try:
            # session = Session()                 # creating new session object
            a_columns = ["host_id", "is_localhost", "host_name", "ip_address",
                "host_alias", "hostgroup_name", "device_name"]
            table_columns = [
                ["host_id", "is_localhost", "host_name",
                    "ip_address", "host_alias", "host_state_id"],
                           ["device_name"], ["hostgroup_name"]]
            # table_classes = [Hosts,DeviceType]
            # table_join = ["user_defined_outerjoin"]
            table_classes = [Hosts, DeviceType, Hostgroups,
                UsersGroups, HostgroupsGroups, HostsHostgroups]
            table_join = [
                "user_defined_outerjoin", "", "user_defined_outerjoin",
                "user_defined_outerjoin", "user_defined_outerjoin"]
            hgbll_obj = HostgroupBll()
            join_conditions = [
                [
                    {
                        "table_column": "device_type_id",
                        "join_with": {
                            "table_class": Hosts,
                            "table_column": "device_type_id"
                        }
                    }
                    ], [],
                [
                    {"table_column": "user_id",
                     "join_with": '%s' % (self.userid)
                     }
                    ],
                [
                    {
                        "table_column": "group_id",
                        "join_with": {
                            "table_class": UsersGroups,
                            "table_column": "group_id"
                        }
                    }
                    ],
                [
                    {
                        "table_column": "hostgroup_id",
                        "join_with": {
                            "table_class": HostgroupsGroups,
                            "table_column": "hostgroup_id"
                        }
                    }
                ]
            ]
            other_conditions = [
                {
                    "type": "equal",
                    "table_class": Hosts,
                    "table_column": "is_deleted",
                    "value": 0,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": Hosts,
                    "table_column": "host_state_id",
                    "value": HostState.enable,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": HostgroupsGroups,
                    "table_column": "group_id",
                    "value": UsersGroups.group_id,
                    "rel": "and"
                },
                {
                    "type": "equal",
                    "table_class": Hosts,
                    "table_column": "host_id",
                    "value": HostsHostgroups.host_id,
                    "rel": "and"
                    },
                {
                    "type": "equal",
                    "table_class": HostgroupsGroups,
                    "table_column": "hostgroup_id",
                    "value": Hostgroups.hostgroup_id,
                    "rel": "and"
                }
            ]
            req_vars["iSortCol_0"] = int(
                req_vars["iSortCol_0"]) + 1  # if int(req_vars["iSortCol_0"])>2 else int(req_vars["iSortCol_0"])-1
            # hosts = session.query(Hosts.host_id, Hosts.is_localhost,
            # Hosts.host_name,
            # Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.host_state_id,DeviceType.device_name).filter(and_(Hosts.is_deleted
            # == 0,Hosts.host_state_id == HostState.enable,Hosts.device_type_id
            # == DeviceType.device_type_id)).order_by(Hosts.host_name).all()
            # # execute query and fetch data
            hosts = hgbll_obj.get_data_table_sqlalchemy(
                a_columns, table_columns, table_classes, table_join, other_conditions, i_display_start, i_display_length,
                                                        s_search, sEcho, sSortDir_0, iSortCol_0, req_vars, join_conditions)
            return hosts
        except Exception, e:
            output = {
                "sEcho": 0,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "query": str(e),
                "other": other_conditions
            }
            return output

    def get_host_details(self, host_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hosts = session.query(Hosts.host_id, Hosts.host_name, Hosts.host_alias, Hosts.ip_address).filter(
                and_(Hosts.host_id == host_id)).all()          # execute query and fetch data
            return hosts
        except Exception, e:
            err = ErrorMessages()
            err.error_msg = err.db_error
            return e
        finally:
            session.close()                     # close the session object

    def grid_view_service(self, host_id):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            services = session.query(HostServices.service_description, HostServices.normal_check_interval, HostServices.host_id).filter(
                HostServices.host_id == host_id).order_by(HostServices.service_description).all()          # execute query and fetch data
            return services
        except Exception, e:
            return e
        finally:
            session.close()

    def set_service_time(self, hosts_list, service_name, service_time, user_name):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        total = []
        try:
            session = Session()
            # nms_instance = __file__.split("/")[3]
            for i in range(len(hosts_list)):                 # creating new session object
                services = session.query(HostServices).filter(and_(HostServices.host_id == hosts_list[i], HostServices.service_description == service_name[i]
                                         .replace('_', ' '))).update({HostServices.normal_check_interval: service_time[i]})
                if(flag_nagios_call == 0):
                    ncbll = NagioConfigurationBll()
                    wnc = ncbll.write_nagios_config(nms_instance)
                    condition_nagios = isinstance(wnc, bool)
                else:
                    n_bll = NagiosBll()
                    wnc = n_bll.edit_old_service(hosts_list[i], service_name[i].replace(
                        '_', ' '), service_time[i])  # (host_id, service_description, normal_check_interval)
                    condition_nagios = wnc["success"] == 0

                if (condition_nagios):
                    total.append(services)
                    session.commit()
                    SystemSetting.reload_nagios_config()

            # new return code
            return {"success": 0, "result": 1}

            ncbll = NagioConfigurationBll()
            wnc = ncbll.write_nagios_config(nms_instance)
            ng_cng = NagiosConfiguration()
            services = session.query(HostServices.service_description,
                                     HostServices.check_command,
                                     HostServices.max_check_attempts,
                                     HostServices.normal_check_interval,
                                     HostServices.retry_check_interval,
                                     Hosts.priority_id,
                                     Hosts.host_name).filter(and_(HostServices.is_deleted == 0, HostServices.host_id == Hosts.host_id, Hosts.is_deleted == 0)).all()
            s_config = ""
            s_config_dict = SystemConfig.get_service_config_details()
            use_template = s_config_dict["use_template"]
            max_check_attempts = s_config_dict["max_check_attempts"]
            normal_check_interval = s_config_dict["normal_check_interval"]
            retry_check_interval = s_config_dict["retry_check_interval"]

            for service in services:
                # normal_check_interval=priority_dict[service.priority_id] # new code
                # if(service.service_description.find("SNMP UPTIME")!=-1):
                #    normal_check_interval="1"
                #    retry_check_interval="1"
                #    max_check_attempts="2"
                # else:
                normal_check_interval = (service.normal_check_interval == None and s_config_dict[
                                         "normal_check_interval"]) or str(service.normal_check_interval)
                max_check_attempts = (service.max_check_attempts == None and s_config_dict[
                                      "max_check_attempts"]) or str(service.max_check_attempts)
                retry_check_interval = (service.retry_check_interval == None and s_config_dict[
                                        "retry_check_interval"]) or str(service.retry_check_interval)
                s_config += ng_cng.service_config(
                    use_template, service.host_name, service.service_description, max_check_attempts,
                                                  normal_check_interval, retry_check_interval, service.check_command)
            ng_cng.write_service_config_file(nms_instance, s_config)
            SystemSetting.reload_nagios_config()
            # el = EventLog()
            # el.log_event("Service time modified for added in unmp system",created_by)
            # if isinstance(wnc, bool):
        # 	el = EventLog()
        # 	el.log_event("New Hostgroup named "+hostgroup_name+" added in unmp system",created_by)
        # else:
            #    err = ErrorMessages()
            #    err.error_msg = err.nagios_config_error
            # return err
            return {"success": 0, "result": total}
        except Exception, e:
            return {"success": 1, "result": str(e)}
        finally:
            session.close()

##### Service ends


class NagioConfigurationBll(object):
    def write_nagios_config(self, nms_instance):
        Session = sessionmaker(
            bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            ng_cng = NagiosConfiguration()
            hostgroups = session.query(Hostgroups.hostgroup_name, Hostgroups.hostgroup_alias).filter(
                Hostgroups.is_deleted == 0).all()          # execute query and fetch data
            hg_config = ""
            for hostgroup in hostgroups:
                hg_config += ng_cng.hostgroup_config(
                    hostgroup.hostgroup_name, hostgroup.hostgroup_alias)
            ng_cng.write_hostgroup_config_file(nms_instance, hg_config)

            Parents = aliased(Hosts, name='parents')
            hosts = session.query(Hosts.host_name, Hosts.host_alias, Hosts.ip_address, Hosts.priority_id, Hostgroups.hostgroup_name, (
                Parents.host_name).label("parent")).outerjoin(Parents, Hosts.parent_name == Parents.host_id).filter(and_(Hosts.is_deleted == 0, HostsHostgroups.hostgroup_id == Hostgroups.hostgroup_id, Hosts.host_id == HostsHostgroups.host_id)).all()          # execute query and fetch data

            h_config = ""
            h_config_dict = SystemConfig.get_host_config_details()
            use_template = h_config_dict["use_template"]
            check_command = h_config_dict["check_command"]
            for host in hosts:
                h_config += ng_cng.host_config(
                    use_template, host.host_name, host.host_alias, host.ip_address, host.hostgroup_name, check_command, host.parent)
            ng_cng.write_host_config_file(nms_instance, h_config)
            ## Mahipal code
            priority_dict = {}
            priority_dict["high"] = "15"
            priority_dict["normal"] = "30"
            priority_dict["low"] = "60"

            services = session.query(HostServices.service_description,
                                     HostServices.check_command,
                                     HostServices.max_check_attempts,
                                     HostServices.normal_check_interval,
                                     HostServices.retry_check_interval,
                                     Hosts.priority_id,
                                     Hosts.host_name).filter(and_(HostServices.is_deleted == 0, HostServices.host_id == Hosts.host_id, Hosts.is_deleted == 0)).all()
            s_config = ""
            s_config_dict = SystemConfig.get_service_config_details()
            use_template = s_config_dict["use_template"]
            max_check_attempts = s_config_dict["max_check_attempts"]
            normal_check_interval = s_config_dict["normal_check_interval"]
            retry_check_interval = s_config_dict["retry_check_interval"]

            for service in services:
                normal_check_interval = priority_dict[
                    service.priority_id]  # new code
                # if(service.service_description.find("SNMP UPTIME")!=-1):
                #    normal_check_interval="1"
                #    retry_check_interval="1"
                #    max_check_attempts="2"
                # else:
                normal_check_interval = (service.normal_check_interval == None and s_config_dict[
                                         "normal_check_interval"]) or str(service.normal_check_interval)
                max_check_attempts = (service.max_check_attempts == None and s_config_dict[
                                      "max_check_attempts"]) or str(service.max_check_attempts)
                retry_check_interval = (service.retry_check_interval == None and s_config_dict[
                                        "retry_check_interval"]) or str(service.retry_check_interval)
                retry_check_interval = (service.retry_check_interval == None and s_config_dict[
                                        "retry_check_interval"]) or str(service.retry_check_interval)
                s_config += ng_cng.service_config(
                    use_template, service.host_name, service.service_description, max_check_attempts,
                                                  normal_check_interval, retry_check_interval, service.check_command)
            ng_cng.write_service_config_file(nms_instance, s_config)
            SystemSetting.reload_nagios_config()
            return True
        except Exception, e:
            return e
        finally:
            session.close()                     # close the session object


# add(host_name,host_alias,ip_address,mac_address,device_type_id,netmask,gateway,None,'','',None,'',None,1,'',None,None,host_state_id,priority_id,host_vendor_id,host_os_id,'','','','public','private','161','162','2c','','UNMP',parent_name,lock_status,1,longitude,latitude,'','',hostgroup,mac_address,node_type,master_id="")
# global mac_li_g,ip_li_g,no,lg,ln, is_second
# no = 1
# lg=72.26
# ln=23.26
# is_second = 1
def randomMAC():
    mac = [0x72, 0xff, 0xff,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def check_ip(first, second):
    for i in range(0, 4):
        if int(first[i]) <= int(second[i]):
            if int(first[i]) < int(second[i]):
                return 1
        else:
            return 0
    return 1


def ip_list(start_range, end_range):
    ip_li = []
    validate = 1
    first = start_range.split('.')
    second = end_range.split('.')
    if (len(first) == len(second) and len(first) == 4):
        for i in range(0, 4):
            if int(first[i]) <= int(second[i]):
                if int(first[i]) < int(second[i]):
                    break
            else:
                validate = 0
                break
        if validate == 1:
            while check_ip(first, second) == 1:
                if int(first[3]) != 255 or int(first[3]) != 1 or int(first[3]) != 2:
                    dst_ip_str = "%s.%s.%s.%s" % (
                        first[0], first[1], first[2], first[3])
                    ip_li.append(dst_ip_str)
                    if len(ip_li) > 99:
                        return ip_li

                first[3] = int(first[3]) + 1

                if int(first[3]) > 255:
                    first[3] = 0
                    first[2] = int(first[2]) + 1
                    if int(first[2]) > 255:
                        first[2] = 0
                        first[1] = int(first[1]) + 1
                        if int(first[1]) > 255:
                            first[1] = 0
                            first[0] = int(first[0]) + 1
                            if int(first[0]) > 255:
                                break


# add(ip_address,ip_address,ip_address,mac,device_type_id,"255.255.255.0","10.10.10.1",None,'','',None,'',None,1,'',None,None,'e',"normal",'1','lenny','','','','public','private','161','162','2c','','UNMP',parent_name,None,1,'76.24','23.26','','',hostgroup,mac,node_type,"")
#(host_name,host_alias,ip_address,mac_address,device_type_id,netmask,gateway,primary_dns,secondary_dns,dns_state,timestamp,created_by,creation_time,is_deleted,updated_by,ne_id,site_id,host_state_id,priority_id,host_vendor_id,host_os_id,http_username,http_password,http_port,snmp_read_community,snmp_write_community,snmp_port,snmp_trap_port,snmp_version_id,comment,nms_instance,parent_name,lock_status,is_localhost,longitude,latitude,serial_number,hardware_version,hostgroup,ra_mac="",node_type="",master_id=""):
def add_demo_host(ip_address, parent_name, mac, device_type_id, node_type, master_id="", hostgroup="7"):
    global no, lg, ln
#    lg+=2
#    ln+=2

    h = HostBll()
    rvalue = h.add(
        ip_address, ip_address, ip_address, mac, device_type_id, "255.255.255.0", "10.10.10.1", '', '', '', None, '', None, 0, '', None, None, 'e', "normal", '1', 'lenny', '', '', '', 'public', 'private', '161', '162', '2c', '',
                   'UNMP', parent_name, 'f', 1, '%.2f' % lg, '%.2f' % ln, '', '', hostgroup, mac, node_type, master_id)
    if isinstance(rvalue, ErrorMessages):
        print rvalue.error_msg
    elif isinstance(rvalue, Exception):
        print "Error : " + str(rvalue)
    else:
        print rvalue
    # print rvalue.error_msg
    print " add ", no
    no += 1
    return rvalue


def get_ip_mac():
    global mac_li_g, ip_li_g
    ip_address = ip_li_g.pop()
    a = 0
    while True:
        if a > 10:
            return (ip_address, mac)
        a = a + 1
        mac = randomMAC()
        if mac_li_g.count(mac) <= 0:
            mac_li_g.append(mac)
            return (ip_address, mac)


def demo_tree_host(idu, idu_parent):
    li = []
    global is_second
    if idu == "m":
        ip_address, mac = get_ip_mac()
        odu100m_parent = add_demo_host(
            ip_address, idu_parent, mac, "odu100", 0)
        print "odu100 M ", ip_address
        ip_address, mac = get_ip_mac()
        add_demo_host(ip_address, idu_parent, mac, "ap25", 0)
        print "AP  ", ip_address
        ip_address, mac = get_ip_mac()
        odu100s_parent = add_demo_host(
            ip_address, odu100m_parent, mac, "odu100", 1, odu100m_parent)
        print "odu100 S ", ip_address
        if is_second > 1:
            ip_address, mac = get_ip_mac()
            odu100s_parent = add_demo_host(
                ip_address, odu100m_parent, mac, "odu100", 1, odu100m_parent)
            print "odu100 S ", ip_address
            ip_address, mac = get_ip_mac()
            odu100s_parent = add_demo_host(
                ip_address, odu100m_parent, mac, "odu100", 1, odu100m_parent)
            print "odu100 S ", ip_address
            ip_address, mac = get_ip_mac()
            odu100s_parent = add_demo_host(
                ip_address, odu100m_parent, mac, "odu100", 1, odu100m_parent)
            print "odu100 S ", ip_address
        ip_address, mac = get_ip_mac()
        idu_parent = add_demo_host(ip_address, idu_parent, mac, "idu4", 0)
        print "IDU M ", ip_address
        ip_address, mac = get_ip_mac()
        idus_parent = add_demo_host(ip_address, odu100s_parent, mac, "idu4", 1)
        li = [idu_parent, idus_parent]
        is_second = 2
    if idu == "s":
        ip_address, mac = get_ip_mac()
        add_demo_host(ip_address, idu_parent, mac, "ap25", 0)
        ip_address, mac = get_ip_mac()
        add_demo_host(ip_address, idu_parent, mac, "ap25", 0)
        ip_address, mac = get_ip_mac()
        odu100m_parent = add_demo_host(ip_address, idu_parent, mac, "odu16", 0)
        ip_address, mac = get_ip_mac()
        odu100s_parent = add_demo_host(ip_address, odu100m_parent, mac,
                                        "odu16", 1, odu100m_parent)
        if is_second > 1:
            ip_address, mac = get_ip_mac()
            odu100s_parent = add_demo_host(
                ip_address, odu100m_parent, mac, "odu16", 1, odu100m_parent)
            ip_address, mac = get_ip_mac()
            odu100s_parent = add_demo_host(
                ip_address, odu100m_parent, mac, "odu16", 1, odu100m_parent)
            ip_address, mac = get_ip_mac()
            odu100s_parent = add_demo_host(
                ip_address, odu100m_parent, mac, "odu16", 1,
                                            odu100m_parent)
        ip_address, mac = get_ip_mac()
        idu_parent = add_demo_host(ip_address, odu100s_parent, mac, "idu4", 0)
        li.append(idu_parent)
        is_second = 4
    return li


def last_tree_host(idu, idu_parent):
    if idu == "m":
        ip_address, mac = get_ip_mac()
        add_demo_host(ip_address, idu_parent, mac, "ap25", 0)
        ip_address, mac = get_ip_mac()
        odu100m_parent = add_demo_host(
            ip_address, idu_parent, mac, "odu100", 0)
    if idu == "s":
        ip_address, mac = get_ip_mac()
        add_demo_host(ip_address, idu_parent, mac, "ap25", 0)
        ip_address, mac = get_ip_mac()
        odu100m_parent = add_demo_host(ip_address, idu_parent, mac, "odu16", 1)


# mac_li_g = []
# ip_li_g = ip_list("10.10.10.114","10.10.23.204")
# ip_li_g.reverse()
def get_mac():
    global mac_li_g
    a = 0
    while True:
        if a > 10:
            return mac
        a = a + 1
        mac = randomMAC()
        if mac_li_g.count(mac) <= 0:
            mac_li_g.append(mac)
            return mac


def p2mp_setup():
    global ip_li_g
    nli = [3, 4]
    odu100 = random.randint(3, 4)
    nli.remove(odu100)
    odu16 = nli[0]

    m100_li = []
    for i in range(0, odu100):
        ip_address = ip_li_g.pop(0)
        mac = get_mac()
        odu100m_parent = add_demo_host(ip_address, '1', mac, "odu100", 0)
        m100_li.append(odu100m_parent)

    m16_li = []
    for i in range(0, odu16):
        ip_address = ip_li_g.pop(0)
        mac = get_mac()
        odu16m_parent = add_demo_host(ip_address, '1', mac, "odu16", 0)
        m16_li.append(odu16m_parent)

    for i in m100_li:
        parent_name = i
        for k in range(0, odu100):
            ip_address = ip_li_g.pop(0)
            mac = get_mac()
            add_demo_host(ip_address, parent_name, mac,
                          "odu100", 1, parent_name)
    for i in m16_li:
        parent_name = i
        for k in range(0, odu16):
            ip_address = ip_li_g.pop(0)
            mac = get_mac()
            add_demo_host(
                ip_address, parent_name, mac, "odu16", 1, parent_name)


def all_firmware_detail():
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        firmware_result_dic = {}
        firmware_dic = {}
        sel_query = "select f.firmware_mapping_id, d.device_type_id from device_type as d left join firmware_mapping as f on d.device_type_id = f.device_type_id where d.is_deleted = 0"
        cursor.execute(sel_query)
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                if row[1] != 'unknown' and row[1] != None:
                    if row[1] in firmware_dic:
                        firmware_dic[row[1]].append(row[0])
                    else:
                        firmware_dic[row[1]] = [row[0]] if row[0] else []
        firmware_result_dic['success'] = 0
        firmware_result_dic['result'] = firmware_dic
        return firmware_result_dic
    except Exception, e:
        firmware_dic['success'] = 1
        firmware_dic['result'] = str(e[-1])
        return firmware_dic
    finally:
        cursor.close()
        db.close()


# p2mp_setup()

# ip_address,mac = get_ip_mac()
# odu100m_parent = add_demo_host(ip_address,'1',mac,"odu16",0)
# print "odu100 M ",ip_address
# ip_address,mac = get_ip_mac()
# print "IP >>> ",ip_address,mac,odu100m_parent
# odu100s_parent =  add_demo_host(ip_address,odu100m_parent,mac,"odu16",1,odu100m_parent)
# print "odu100 S ",ip_address

# ip_address,mac = get_ip_mac()
# idu_parent = add_demo_host(ip_address,'1',mac,"idu4",0)
# li = demo_tree_host('m',idu_parent)
# li1 = demo_tree_host('s',li[1])
# li2 = demo_tree_host('m',li[0])
# li = demo_tree_host('m',li1[0])
# last_tree_host('s',li2[1])
# last_tree_host('m',li[0])
# li1 = demo_tree_host('s',li[1])
# li2 = demo_tree_host('m',li2[0])
# last_tree_host('s',li2[1])
# last_tree_host('m',li[0])
# last_tree_host('m',li2[0])
