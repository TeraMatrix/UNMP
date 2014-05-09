#!/usr/bin/python2.6

"""
@author: Yogesh Kumar,Rahul Gautam
@since: 03-Nov-2011
@version: 0.1
@note: All database and model's functions that are common.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""

# Import modules that contain the function and libraries
import datetime
import warnings

import MySQLdb
import psutil
import rrdtool

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import paramiko

from unmp_config import SystemConfig
from unmp_model import *


class DB():
    """
    db = DB()
    db.ready()
    rows, get_result = db.execute(query)
    db.close()
    if rows == -1:
        raise db.error
    db.done()

    TODO: just use db init and db close functions
    and look for how many cursor objects are open
    """

    def __init__(self):
        self.error = None
        self.cursor = None
        try:
            self.db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        except Exception:
            raise
        else:
            if not self.db.open:
                raise Exception("DB connection open() Error")

    def empty(self):
        """


        @return:
        """
        return ()

    def ready(self):
        """


        @raise:
        """
        try:
            self.cursor = self.db.cursor()
        except Exception:
            raise

    def execute(self, query):
        """

        @param query:
        @return:
        """
        try:
            row_affected = self.cursor.execute(query)
        except Exception, e:
            self.error = e
            return -1, self.empty
        else:
            return row_affected, self.cursor.fetchall()

    def execute_dui(self, query):
        """dui: delete, update, insert
        @param query:
        """
        try:
            row_affected = self.cursor.execute(query)
            self.db.commit()
        except Exception, e:
            self.error = e
            return -1
        else:
            return row_affected

    def done(self):
        """
        the data from the sql is fetched properly

        """
        if self.cursor:
            self.cursor.close()
            self.cursor = None

    def close(self):
        """
        since data from the SQL has been fetched
        close the connection object/ close the
        cursor object
        """
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.db.open:
            self.db.close()

    def __del__(self):
        self.close()


host_status_dict = {
    0: 'No operation',
    1: 'Firmware download',
    2: 'Firmware upgrade',
    3: 'Restore default config',
    4: 'Flash commit',
    5: 'Reboot',
    6: 'Site survey',
    7: 'Calculate BW',
    8: 'Uptime service',
    9: 'Statistics gathering',
    10: 'Reconciliation',
    11: 'Table reconciliation',
    12: 'Set operation',
    13: 'Live monitoring',
    14: 'Status capturing',
    15: 'Alarm Reconciliation'
}


def db_connect():
    """
    Used to connect to the database
        :: return database object ed in global_db variable
    """
    db = ''
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        # db = MySQLdb.connect("localhost","root","root","nmsp")
        # print " $$$ $$$ Database Connect successful "
    except MySQLdb.Error as e:
        db = str(e)
        pass  # print "/*/*/* MYSQLdb Exception (db connect) : "+str(e)
    except Exception as e:
        db = str(e)
        pass  # print "/*/*/* Database Exception (db connect) : "+str(e)
    finally:
        return db


class LocalSystemBll(object):
    """
    UNMP system dashboard
    """
    def harddisk_details(self):
        """


        @return:
        """
        harddisk = psutil.disk_usage('/')
        total = harddisk.total / (1024.0 * 1024.0 * 1024.0)
        free = harddisk.free / (1024.0 * 1024.0 * 1024.0)
        used = harddisk.used / (1024.0 * 1024.0 * 1024.0)
        unused = total - (free + used)
        return str('%.2f' % total) + "," + str('%.2f' % free) + "," \
               + str('%.2f' % unused) + "," + str('%.2f' % used)

    def system_uptime(self):
        """


        @return:
        """
        return datetime.datetime.fromtimestamp(psutil.BOOT_TIME
        ).strftime('%d-%B-%Y %H:%M:%S')

    def ram_details(self):
        """


        @return:
        """
        ram = psutil.phymem_usage()
        total = ram.total
        usePer = ram.percent
        used = total * usePer / 100
        free = total - used
        return "%.2f,%.2f" % (used / (1024.0 * 1024.0), free / (1024.0 * 1024.0))

    def convert_utc_to_ist(self, timestamp):
        """

        @param timestamp:
        @return:
        """
        offset_ist = 5.5
        return timestamp + ((offset_ist * 60) * 60000)

    def processor_details(self, total):
        """

        @param total:
        @return:
        """
        total_ = total
        total_sec = total * 10 + 10
        cpu = rrdtool.fetch('/omd/daemon/rrd/cpu.rrd', 'AVERAGE', '-s',
                            '-%ssec' % total_sec)
        data_series = []
        if len(cpu) == 3:
            timestamp = cpu[0]
            label = cpu[1]
            data = cpu[2]
            for i in range(len(label)):
                data_series.append({"name": str(label[i]).replace("_", " "),
                                    "data": []})

            for i in range(len(data)):
                if total != 0:
                    for lbl_i in range(0, len(label)):
                        if data[i][lbl_i] != None:
                            data_series[lbl_i]["data"].append(
                                {"x": self.convert_utc_to_ist(
                                    (timestamp[
                                         0] + (timestamp[2] * (i))) * 1000),
                                 "y": data[i][lbl_i]})
                            if lbl_i == 0:
                                total -= 1
        for i in range(len(data_series)):
            data_series[i]["data"] = data_series[i]["data"][:total_]
        return data_series

    def bandwidth_details(self, total):
        """

        @param total:
        @return:
        """
        total_ = total
        total_sec = total * 10 + 10
        interface = rrdtool.fetch('/omd/daemon/rrd/interface.rrd', 'AVERAGE',
                                  '-s', '-%ssec' % total_sec)
        data_series = []
        if len(interface) == 3:
            timestamp = interface[0]
            label = interface[1]
            data = interface[2]
            for i in range(len(label)):
                data_series.append({"name": str(label[i]).replace("_", " "),
                                    "data": []})

            for i in range(len(data)):
                if total != 0:
                    for lbl_i in range(0, len(label)):
                        if data[i][lbl_i] != None:
                            data_series[lbl_i]["data"].append(
                                {"x": self.convert_utc_to_ist(
                                    (timestamp[
                                         0] + (timestamp[2] * (i))) * 1000),
                                 "y": data[i][lbl_i] / 1024.0})
                            if lbl_i == 0:
                                total -= 1
        for i in range(len(data_series)):
            data_series[i]["data"] = data_series[i]["data"][:total_]
        return data_series


class EventLog():
    """
    @author: Rahul Gautam
    @since: 01-Dec-2011
    @version: 0.1
    @note: Logging Every Event and Action in Database
    @organization: Codescape Consultants Pvt. Ltd.
    @copyright: 2011 Rahul Gautam for Codescape Consultants Pvt. Ltd.
    @see: http://www.codescape.in

    """
    global_db = None

    def db_connect(self):
        """
        Used to connect to the database
            :: return database object in global_db variable
        """
        db = None
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            self.global_db = db
        except MySQLdb.Error as e:
            print "/*/*/* MYSQLdb Exception (db connect) : " + str(e)
        except Exception as e:
            print "/*/*/* Database Exception (db connect) : " + str(e)

    def db_close(self):
        """
        closes connection with the database
        """
        try:
            self.global_db.close()
        except Exception as e:
            print "/*/*/* Database Exception ( db close ) : " + str(e)

    def log_event(self,
                  description,
                  user_name,
                  level=0,
                  time1=None,
                  time2=datetime.datetime.now()):
        """





        @param description:
        @param user_name:
        @param level:
        @param time1:
        @param time2:
        @note: Used to log Event or Action in Database
        """

        try:
            if time1 is None:
                time_taken = '0'
            else:
                second = (time2 - time1).seconds
                microseconds = (time2 - time1).microseconds
                if second < 60:
                    time_taken = str(
                        second) + "." + str(microseconds / 1000) + " sec"
                elif second < 3600:
                    if second > 120:
                        level = 1  # warning
                    elif second > 300:
                        level = 2  # error
                    minute = int(second / 60)
                    second = second % 60
                    time_taken = str(minute) + " min," + str(second) + " sec"
                else:
                    hour = int(second / 3600)
                    minute = int((second - hour * 3600) / 60)
                    time_taken = str(hour) + " hour," + str(minute) + " min"
                    # print last_check
            self.db_connect()
            insert_query = "INSERT INTO `event_log` \
                                (`event_log_id`, `username`, `event_type_id`,\
                                    `description`, `timestamp`,`level`,`time_taken`) \
                            VALUES (NULL,\"%s\",NULL,\"%s\",\"%s\",\"%s\",\"%s\")\
                            " % (user_name, description, datetime.datetime.now(), level, time_taken)

            cursor = self.global_db.cursor()
            cursor.execute(insert_query)
            self.global_db.commit()
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()
        except Exception as e:
            self.db_close()
            # with open('/home/rahul/Desktop/ok.txt', 'w') as f:
            ##    f.write(str(e))


## USED FOR CIRCULAR CHECK : RAHUL GAUTAM
class Node:
    """

    @param name:
    """

    def __init__(self, name):
        self.name = name
        self.edges = []

    def addEdge(self, node):
        """

        @param node:
        """
        self.edges.append(node)


def dep_resolve(node, resolved, unresolved):
    """

    @param node:
    @param resolved:
    @param unresolved:
    @raise:
    """
    unresolved.append(node)
    for edge in node.edges:
        if edge not in resolved:
            if edge in unresolved:
                raise Exception('Circular reference detected between %s and %s\
                                    ' % (node.name, edge.name))
            dep_resolve(edge, resolved, unresolved)
    resolved.append(node)
    unresolved.remove(node)

##


class Essential(object):
    """
    @author: Rahul Gautam
    @since: 01-Dec-2011
    @version: 0.1
    @note: Logging Every Event and Action in Database
    @organization: Codescape Consultants Pvt. Ltd.
    @copyright: 2011 Rahul Gautam for Codescape Consultants Pvt. Ltd.
    @see: http://www.codescape.in

    """
    global_db = None

    def db_connect(self):
        """
        Used to connect to the database :: return database object ed in global_db variable
        """
        db = None
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            self.global_db = db
        except MySQLdb.Error as e:
            print "/*/*/* MYSQLdb Exception (db connect) : " + str(e)
        except Exception as e:
            print "/*/*/* Database Exception (db connect) : " + str(e)

    def db_close(self):
        """
        closes connection with the database
        """
        try:
            self.global_db.close()
        except Exception as e:
            print "/*/*/* Database Exception ( db close ) : " + str(e)

    def make_list(self, x):
        """

        @param x:
        @return:
        """
        x = map(str, x)
        if x[0] == self.child:
            x[1] = self.parent
        return x

    def circular_check(self, child, parent):
        """

        @param child:
        @param parent:
        @return:
        """
        result_dict = {}
        success = 1
        result_str = ''
        self.child = str(child)
        self.parent = str(parent)
        obj_dict = {}
        rel = ()
        try:
            self.db_connect()
            sel_query = "SELECT  `host_id` , `parent_name`, `ip_address` \
                            FROM  `hosts` \
                            WHERE is_deleted = 0"
            # rel = (('b', 'a'), ('c', 'a'), ('d', 'b'), ('e', 'b'), ('f',
            # 'd'), ('g', 'f'), ('h', 'e'))
            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            rel = cursor.fetchall()
            cursor.close()
            self.db_close()
            if len(rel) > 0:
                rel = map(self.make_list, rel)

                for tt in rel:
                    obj_dict[tt[0]] = Node(tt[2])
                for tt in rel:
                    if tt[1] == 'None':
                        continue
                    obj_dict[tt[1]].addEdge(obj_dict[tt[0]])

                try:
                    if len(obj_dict) > 0 and self.child in obj_dict:
                        dep_resolve(obj_dict[self.child], [], [])
                except Exception, e:
                    success = 1
                    result_str = str(e)
                    return
            success = 0
        except Exception, e:
            result_str = str(e)
            success = 2
        finally:
            result_dict['success'] = success
            result_dict['result'] = result_str
            return result_dict

    def get_hostgroup_ids(self, user_id):
        """

        @param user_id:
        @note: return hostgroup id as a list assigned to user
        """
        hostgroups_list = []
        try:
            self.db_connect()
            sel_query = """SELECT hostgroup_id \
                            FROM users_groups AS ug \
                            JOIN (SELECT hostgroup_id, group_id \
                                    FROM hostgroups_groups) AS hg \
                            ON ug.group_id = hg.group_id \
                            WHERE ug.user_id =  '%s'""" % (user_id)

            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            hostgroups_list = [str(i[0]) for i in result]
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()
        except Exception as e:
            self.db_close()
        finally:
            return hostgroups_list

    def get_host_id(self, value, what):
        """


        @param value:
        @param what:
        @note: return hostgroup id as a list assigned to user
        """
        host_id = None
        try:
            self.db_connect()
            sel_query = """SELECT host_id \
                            FROM hosts \
                            WHERE %s =  '%s'""" % (what, value)

            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                host_id = str(result[0][0])
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()
        except Exception as e:
            self.db_close()
        finally:
            return host_id

    def is_host_allow(self, user_id, hostid):
        """


        @param user_id:
        @param hostid:
        @note: Used Validate host and user mapping :: 1 is False
        """
        value = 1
        try:
            self.db_connect()
            sel_query = """SELECT hh.host_id \
                            FROM users_groups AS ug \
                            JOIN (SELECT hostgroup_id, group_id \
                                    FROM hostgroups_groups) AS hg \
                            ON ug.group_id = hg.group_id
                            JOIN (SELECT host_id, hostgroup_id \
                                    FROM hosts_hostgroups) AS hh \
                            ON hg.hostgroup_id = hh.hostgroup_id
                            WHERE ug.user_id =  '%s' and hh.host_id = '%s' \
                            """ % (user_id, hostid)

            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) < 1:
                value = 1
            else:
                value = 0
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()
        except Exception as e:
            self.db_close()
        finally:
            return value

    def host_status(self, hostid, status, host_ip=None, prev_status=0):
        """




        @param hostid:
        @param status:
        @param host_ip:
        @param prev_status:
        @host_status(1,0,None,10)
        @note: Used to update host operation status and varify it
        @dict: {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade',
                3:'Restore default config', 4:'Flash commit', 5:'Reboot',
                6:'Site survey', 7:'Calculate BW', 8:'Uptime service',
                9:'Statistics gathering', 10:'Reconciliation',
                11:'Table reconciliation', 12:'Set operation',
                13:'Live monitoring', 14:'Status capturing'}
        """
        value = 0
        try:
            self.db_connect()
            if hostid:
                sel_query = """select status \
                                from host_status  \
                                where host_id = '%s'""" % (hostid)
            elif host_ip:
                sel_query = """select status \
                                from host_status  \
                                where host_ip = '%s'""" % (host_ip)
            else:
                value = 0  # error 100
                return
            if status == None:
                value = 0  # error 100
                return
            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                if int(result[0][0]) == prev_status or \
                                int(result[0][0]) == int(status):

                    if hostid:
                        up_query = """update host_status set status='%s' \
                                        where host_id = '%s'\
                                        """ % (status, str(hostid))
                    elif host_ip:
                        up_query = """update host_status set status='%s \
                                        where host_ip = '%s'\
                                        """ % (status, host_ip)

                    cursor.execute(up_query)
                    self.global_db.commit()
                    value = 0
                else:
                    value = result[0][0]
            else:
                value = 0  # value = 100 no row found
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()
        except Exception as e:
            self.db_close()
        finally:
            return int(value)

    def get_hoststatus(self, hostid, host_ip=None):
        """


        @param hostid:
        @param host_ip:
        @note: Used to update host operation status and varify it
        """
        value = 0
        try:
            self.db_connect()
            if hostid:
                sel_query = """select status \
                                from host_status  \
                                where host_id = '%s'""" % (hostid)
            elif host_ip:
                sel_query = """select status \
                                from host_status  \
                                where host_ip = '%s'""" % (host_ip)
            else:
                value = 0  # error 100
                return
            cursor = self.global_db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                value = result[0][0]
            else:
                value = 0  # value = 100 no row found
            cursor.close()
            self.db_close()
        except MySQLdb.Error as e:
            self.db_close()
        except Exception as e:
            self.db_close()
        finally:
            return int(value)


class Connection(object):
    """Connects and logs into the specified hostname.
    Arguments that are not given are guessed from the environment."""

    def __init__(self,
                 host,
                 username=None,
                 private_key=None,
                 password=None,
                 port=22,
    ):
        self._sftp_live = False
        self._sftp = None
        if not username:
            username = os.environ['LOGNAME']

        # Log to a temporary file.
        # templog = tempfile.mkstemp('.txt', 'ssh-')[1]
        # paramiko.util.log_to_file(templog)

        # Begin the SSH transport.
        self._transport = paramiko.Transport((host, port))
        self._tranport_live = True
        # Authenticate the transport.
        if password:
            # Using Password.
            self._transport.connect(username=username, password=password)
        else:
            # Use Private Key.
            if not private_key:
                # Try to use default key.
                if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                    private_key = '~/.ssh/id_rsa'
                elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                    private_key = '~/.ssh/id_dsa'
                else:
                    raise TypeError(
                        "You have not specified a password or key.")

            private_key_file = os.path.expanduser(private_key)
            rsa_key = paramiko.RSAKey.from_private_key_file(private_key_file)
            self._transport.connect(username=username, pkey=rsa_key)

    def _sftp_connect(self):
        """Establish the SFTP connection."""
        if not self._sftp_live:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp_live = True

    def get(self, remotepath, localpath=None):
        """Copies a file between the remote host and the local host.
        @param remotepath:
        @param localpath:
        """
        if not localpath:
            localpath = os.path.split(remotepath)[1]
        self._sftp_connect()
        self._sftp.get(remotepath, localpath)

    def put(self, localpath, remotepath=None):
        """Copies a file between the local host and the remote host.
        @param localpath:
        @param remotepath:
        """
        if not remotepath:
            remotepath = os.path.split(localpath)[1]
        self._sftp_connect()
        self._sftp.put(localpath, remotepath)

    def execute(self, command):
        """Execute the given commands on a remote machine.
        @param command:
        """
        channel = self._transport.open_session()
        channel.exec_command(command)
        output = channel.makefile('rb', -1).readlines()
        if output:
            return output
        else:
            return channel.makefile_stderr('rb', -1).readlines()

    def run(self, command):
        """Execute the given commands on a remote machine.
        @param command:
        """
        channel = self._transport.open_session()
        channel.exec_command(command)

    def close(self):
        """Closes the connection and cleans up."""
        # Close SFTP Connection.
        if self._sftp_live:
            self._sftp.close()
            self._sftp_live = False
            # Close the SSH Transport.
        if self._tranport_live:
            self._transport.close()
            self._tranport_live = False

    def __del__(self):
        """Attempt to clean up if not explicitly closed."""
        self.close()


def agent_start(ip_address, username='root', pwd='public'):
    """Little test when called directly.
    @param ip_address:
    @param username:
    @param pwd:
    """
    # Set these to your own details.
    try:
        myssh = Connection(ip_address, username, None, pwd)
        # myssh.put('myssh.py')
        myssh.run("a=$( ps | grep snmpagent | grep -v grep | \
                    awk '{print $1}');\c=1;for i in $a;do if [ $c -gt 1 ];\
                    then kill -9 $i;fi;c=`expr ${c} + 1`;done;")
        myssh.run('/stureplan/sbin/snmpagent &')
        myssh.close()
        print " Agent START "
    except Exception, e:
        print "in shell ", str(e)
