#!/usr/bin/python2.6
from datetime import date, timedelta, datetime
import MySQLdb
from unmp_config import SystemConfig
import json
from json import JSONEncoder
from operator import itemgetter


class OduSchedulingBll(object):
    """
    Scheduling Page
    """
# AVERAGE DATA FOR GIVEN DATE PERIOD
    def create_scheduler(self, odu_list, event, startDate, endDate, startTime, endTime, repeat, repeatType, daysun,
                         daymon, daytue, daywed, daythu, dayfri, daysat, monthjan, monthfeb, monthmar, monthapr,
                         monthmay, monthjun, monthjul, monthaug, monthsep, monthoct, monthnov, monthdec, dates,
                         firmware_file_name=""):
        """

        @param odu_list:
        @param event:
        @param startDate:
        @param endDate:
        @param startTime:
        @param endTime:
        @param repeat:
        @param repeatType:
        @param daysun:
        @param daymon:
        @param daytue:
        @param daywed:
        @param daythu:
        @param dayfri:
        @param daysat:
        @param monthjan:
        @param monthfeb:
        @param monthmar:
        @param monthapr:
        @param monthmay:
        @param monthjun:
        @param monthjul:
        @param monthaug:
        @param monthsep:
        @param monthoct:
        @param monthnov:
        @param monthdec:
        @param dates:
        @param firmware_file_name:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "INSERT INTO odu_schedule (event, start_date, end_date, start_time, end_time, is_repeated, repeat_type, sun, mon, tue, wed, thu,\
                             fri, sat, jan, feb, mar, apr, may, jun, jul, aug, sept, oct, nov, dece, day , is_deleted , is_success , update_time) VALUES ('%s','%s','%s','%s','%s',%s,'%s', %s, %s,\
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', 1 , 1, NULL ) " % (
            event, startDate, endDate, startTime, endTime, repeat, repeatType, daysun, daymon, daytue, daywed, daythu,
            dayfri, daysat, monthjan, monthfeb, monthmar, monthapr, monthmay, monthjun, monthjul, monthaug, monthsep,
            monthoct, monthnov, monthdec, dates)
            cursor.execute(sql)
            newId = cursor.lastrowid
            for oduId in odu_list:
                if oduId.strip() != "":
                    if event == "Firmware":
                        sql = "INSERT INTO odu_host_schedule(schedule_id,host_id,is_success,firmware_file_name) VALUES(%s,%s,1,'%s')" % (
                            newId, oduId, firmware_file_name)
                        cursor.execute(sql)  # continue from here
                    else:
                        sql = "INSERT INTO odu_host_schedule(schedule_id,host_id,is_success) VALUES(%s,%s,1)" % (
                        newId, oduId)
                        cursor.execute(sql)

            conn.commit()
            return str(newId)
        except Exception, e:
            conn.rollback()
            return (str(e))
        finally:
            conn.close()

    def get_hostgroup_device(self, user_id, hostgroup_id_list):
        """

        @param user_id:
        @param hostgroup_id_list:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            query = "select distinct dt.device_type_id,dt.device_name from hostgroups as hg \
			join (select hostgroup_id,host_id from hosts_hostgroups)  as hhg on hhg.hostgroup_id=hg.hostgroup_id \
			join (select host_id,device_type_id from hosts ) as h on h.host_id=hhg.host_id \
			join (select device_type_id,device_name,is_deleted from device_type) as dt on dt.device_type_id=h.device_type_id \
			where hhg.hostgroup_id IN (%s) and dt.is_deleted<>1 group  by hg.hostgroup_id ,dt.device_type_id order by dt.device_name" % ','.join(
                hostgroup_id_list)
            cursor.execute(query)
            result = cursor.fetchall()
            result_dict = {}
            result_dict["success"] = 0
            result_dict["result"] = result
            return result_dict
        except Exception, e:
            result_dict = {}
            result_dict["success"] = 1
            result_dict["result"] = str(e)
            return result_dict
        finally:
            conn.close()

    def odu_multiple_select_list(self, odu_list, selectListId, device_type):
        """

        @param odu_list:
        @param selectListId:
        @param device_type:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT host_id,ip_address FROM hosts \
                        WHERE device_type_id like '%s'  and is_deleted<>1 \
                        ORDER BY host_id DESC" % (device_type)
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def view_Scheduling_Details(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT os.schedule_id,os.update_time, h.host_alias , ohs.is_success,ohs.message FROM `odu_schedule` as os \
		join (select schedule_id,host_id,is_success,message from odu_host_schedule) as ohs on ohs.schedule_id=os.schedule_id \
		join (select host_name ,host_alias,host_id from hosts) as h on h.host_id=ohs.host_id where os.update_time<now() order by os.schedule_id desc,os.update_time desc "
            cursor.execute(sql)
            # 0 success
            # 1 part
            # 2 failed
            tp = cursor.fetchall()
            di = {}
            li = []
            id = 0
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            status = "0"
            for t in tp:
                if int(t[0]) in di:
                    li = di[int(t[0])]
                    grps = li.pop(2)
                    grps += "  , " + t[2]
                    if str(t[3]) == '1':
                        if str(t[4]) == "None" or str(t[4]) == "":
                            grps += ' ( failed )'
                        else:
                            grps += ' ( ' + str(t[4]) + ' ) '
                        if li[2] == '0':
                            li[2] = '1'
                        elif li[2] == '1':
                            li[2] = '1'
                        elif li[2] == '2':
                            li[2] = '2'
                    else:
                        grps += ' ( success )'
                        if li[2] == '0':
                            li[2] = '0'
                        elif li[2] == '2':
                            li[2] = '1'
                        else:
                            li[2] = '1'
                    li.insert(2, grps)
                    di[int(t[0])] = li
                else:
                    li = make_list(t)
                    grp = li.pop(2)
                    if str(t[3]) == '1':
                        if str(t[4]) == "None" or str(t[4]) == "":
                            grp += ' ( failed )'
                        else:
                            grp += ' ( ' + str(t[4]) + ' ) '
                            # grp += ' ( failed )'
                        status = "2"
                    else:
                        grp += ' ( success )'
                        status = "0"
                    li.insert(2, grp)
                    li[3] = status
                    di[int(t[0])] = li

            lis = di.values()
            for i in range(0, len(lis)):
                id = lis[i].pop(0)
                status = lis[i].pop(2)
                lis[i].pop(2)
                if status == '0':
                    lis[i].append("Successful Scheduling")
                elif str(status) == '2':
                    lis[i].append("Failed Scheduling")
                else:
                    lis[i].append("Partially Successful Scheduling")
            lis = sorted(lis, key=lambda lis: lis[int(0)], reverse=True)
            return lis

        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def load_non_repeative_events(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT * FROM odu_schedule WHERE is_repeated = 0"
            cursor.execute(sql)
            odu_schedule = cursor.fetchall()
            return odu_schedule
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def load_repeative_events(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT * FROM odu_schedule WHERE is_repeated = 1"
            cursor.execute(sql)
            odu_schedule = cursor.fetchall()
            return odu_schedule
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def event_resize(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT end_date,end_time FROM odu_schedule\
            WHERE schedule_id = %s" % scheduleId
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def event_resize_update(self, scheduleId, eDateObj):
        """

        @param scheduleId:
        @param eDateObj:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "UPDATE odu_schedule SET \
                 end_date = '%s', \
                 end_time = '%s' \
                 WHERE schedule_id = %s" % ((str(eDateObj.year) + "-" + str(eDateObj.month) + "-" + str(eDateObj.day)),
                                            (str(eDateObj.hour) + ":" + str(eDateObj.minute) + ":00"), scheduleId)
            cursor.execute(sql)
            conn.commit()
            return 0
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def event_drop(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT start_date,start_time,end_date,end_time,is_repeated,repeat_type,sun,mon,tue,wed,thu,fri,sat,day FROM odu_schedule\
                    WHERE schedule_id = %s" % scheduleId
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def event_drop_update(self, scheduleId, start_date, start_time, end_date, end_time, sun, mon, tue, wed, thu, fri,
                          sat, dates):
        """

        @param scheduleId:
        @param start_date:
        @param start_time:
        @param end_date:
        @param end_time:
        @param sun:
        @param mon:
        @param tue:
        @param wed:
        @param thu:
        @param fri:
        @param sat:
        @param dates:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "UPDATE odu_schedule SET \
                 start_date = '%s', \
                 start_time = '%s', \
                 end_date = '%s', \
                 end_time = '%s', \
                 sun = %s, \
                 mon = %s, \
                 tue = %s, \
                 wed = %s, \
                 thu = %s, \
                 fri = %s, \
                 sat = %s, \
                 day = %s \
                 WHERE schedule_id = %s" % (
            start_date, start_time, end_date, end_time, sun, mon, tue, wed, thu, fri, sat, dates, scheduleId)
            cursor.execute(sql)
            conn.commit()
            return 0
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def delete_odu_scheduler(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "delete FROM odu_schedule\
                WHERE schedule_id = %s" % scheduleId
            cursor.execute(sql)
            sql = "delete FROM odu_host_schedule\
                WHERE schedule_id = %s" % scheduleId
            cursor.execute(sql)
            conn.commit()
            return 0
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def view_odu_list(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "select device_type.device_name,hosts.ip_address,hosts.host_name,hosts.host_alias FROM hosts \
            join (select device_name , device_type_id from device_type) as device_type on device_type.device_type_id=hosts.device_type_id \
            INNER JOIN odu_host_schedule on odu_host_schedule.host_id = hosts.host_id \
            WHERE odu_host_schedule.schedule_id = %s" % scheduleId
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def get_odu_schedule_details(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "select * FROM odu_schedule \
                WHERE schedule_id = %s" % scheduleId
            cursor.execute(sql)
            result = cursor.fetchall()
            sql2 = "select firmware_file_name,hosts.device_type_id,device_type.device_name FROM odu_host_schedule \
			join (select device_type_id,host_id from hosts ) as hosts on hosts.host_id=odu_host_schedule.host_id \
			join (select device_name , device_type_id from device_type) as device_type on device_type.device_type_id=hosts.device_type_id \
	        	WHERE schedule_id = %s \
			group by hosts.device_type_id" % scheduleId
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            return result + result2
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def get_odu_schedule_details_odu(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "select * FROM odu_host_schedule \
                WHERE schedule_id = %s" % scheduleId
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def get_odu_schedule_details_make_list(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT hst.host_id,hst.ip_address from hosts as hst where is_deleted<>1 and hst.device_type_id=(select h.device_type_id FROM odu_host_schedule as ods \
			join ( select device_type_id, host_id from hosts ) as h on h.host_id=ods.host_id \
			where ods.schedule_id=%s group by h.device_type_id)" % scheduleId
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def update_odu_scheduler(self, event, startDate, endDate, startTime, endTime, repeat, repeatType, daysun, daymon,
                             daytue, daywed, daythu, dayfri, daysat, monthjan, monthfeb, monthmar, monthapr, monthmay,
                             monthjun, monthjul, monthaug, monthsep, monthoct, monthnov, monthdec, dates, scheduleId):
        """

        @param event:
        @param startDate:
        @param endDate:
        @param startTime:
        @param endTime:
        @param repeat:
        @param repeatType:
        @param daysun:
        @param daymon:
        @param daytue:
        @param daywed:
        @param daythu:
        @param dayfri:
        @param daysat:
        @param monthjan:
        @param monthfeb:
        @param monthmar:
        @param monthapr:
        @param monthmay:
        @param monthjun:
        @param monthjul:
        @param monthaug:
        @param monthsep:
        @param monthoct:
        @param monthnov:
        @param monthdec:
        @param dates:
        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "UPDATE odu_schedule SET event = '%s', start_date = '%s', end_date = '%s', start_time = '%s', end_time = '%s', is_repeated = %s, repeat_type = '%s', \
            sun = %s, mon = %s, tue = %s, wed = %s, thu = %s, fri = %s, sat = %s, jan = %s, feb = %s, mar = %s, apr = %s, may = %s, jun = %s, jul = %s, aug = %s, sept = %s, \
            oct = %s, nov = %s, dece = %s, day = '%s' , is_deleted=1 , is_success=1 , update_time=NULL WHERE schedule_id =\
             %s" % (
            event, startDate, endDate, startTime, endTime, repeat, repeatType, daysun, daymon, daytue, daywed, daythu,
            dayfri, daysat, monthjan, monthfeb, monthmar, monthapr, monthmay, monthjun, monthjul, monthaug, monthsep,
            monthoct, monthnov, monthdec, dates, scheduleId)
            cursor.execute(sql)
            conn.commit()
            return 0
        except Exception, e:
            return str(e)
        finally:
            conn.rollback()
            conn.close()

    def update_odu_scheduler_delete(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "DELETE FROM odu_host_schedule WHERE schedule_id = %s" % (
                scheduleId)
            cursor.execute(sql)
            conn.commit()
            return 0
        except Exception, e:
            return str(e)
        finally:
            conn.rollback()
            conn.close()

    def update_odu_scheduler_insert(self, scheduleId, oduId, event="Up", firmware_file_name=""):
        """

        @param scheduleId:
        @param oduId:
        @param event:
        @param firmware_file_name:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            # sql = "INSERT INTO
            # odu_host_schedule(schedule_id,host_id,is_success)
            # VALUES(%s,%s,1)" % (scheduleId,oduId)
            if event == "Firmware":
                sql = "INSERT INTO odu_host_schedule(schedule_id,host_id,is_success,firmware_file_name) VALUES(%s,%s,1,'%s')" % (
                    scheduleId, oduId, firmware_file_name)
                cursor.execute(sql)  # continue from here
            else:
                sql = "INSERT INTO odu_host_schedule(schedule_id,host_id,is_success) VALUES(%s,%s,1)" % (
                    scheduleId, oduId)
                cursor.execute(sql)
                # cursor.execute(sql)
            conn.commit()
            return 0
        except Exception, e:
            return str(e)
        finally:
            conn.rollback()
            conn.close()

    def crontab_select_schedule(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "select * from odu_schedule "
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()
        ####

    def crontab_details(self, scheduleId):
        """

        @param scheduleId:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT hosts.ip_address, hosts.http_username, hosts.http_password, hosts.http_port,hosts.device_type_id FROM odu_host_schedule \
                                INNER JOIN hosts on odu_host_schedule.host_id = hosts.host_id \
                                INNER JOIN (select schedule_id , is_deleted from odu_schedule ) as odu_schedule on odu_schedule.schedule_id=odu_host_schedule.schedule_id \
                                WHERE odu_host_schedule.schedule_id =%s " % (scheduleId)

            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

        ###

    def crontab_repeat_schedule(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT repeat_odu_schedule.repeat_odu_schedule_id, repeat_odu_schedule.datestamp, repeat_odu_schedule.timestamp, hosts.ip_address, hosts.http_username, hosts.http_password, hosts.http_port, repeat_odu_schedule.message, repeat_odu_schedule.event FROM repeat_odu_schedule \
                 INNER JOIN hosts on repeat_odu_schedule.host_id = hosts.host_id"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def radio_status(self):
        """


        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT host_id,host_name,ip_address,http_username,http_password,http_port FROM hosts WHERE device_type_id like 'odu%'"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()

    def radio_status_repeat(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            conn = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = conn.cursor()
            sql = "SELECT * FROM repeat_ap_schedule WHERE host_id = %s" % host_id
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception, e:
            return str(e)
        finally:
            conn.close()
