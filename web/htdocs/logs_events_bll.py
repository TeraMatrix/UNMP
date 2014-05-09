#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 20-Apr-2012
@version: 0.1
@note: All Functions and Live Qauery Related with Logs and Events.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
from unmp_model import *
from time import time


class LogsEventsBll(object):
    def convert_time(self, time_stamp):
        time_range = [(86400, "days"), (3600, "hrs"), (60, "min"), (1, "sec")]
        str_time = " "
        current_time = int(time())
        remain_time = current_time - int(time_stamp)
        if remain_time <= 0:
            str_time = "%s %s" % (0, time_range[0][1])
        else:
            for i in range(len(time_range)):
                div_time = remain_time / time_range[i][0]
                if div_time >= 1:
                    str_time = " %s %s" % (
                        div_time, time_range[i][1]) + str_time
                    remain_time = remain_time - (time_range[i][0] * div_time)
                    break
        return int(time_stamp), str_time

    def get_hosts_dict(self):
        Session = sessionmaker(bind=engine)
        hosts_dict = {}
        try:
            session = Session()
            hosts = session.query(Hosts.host_name, Hosts.host_alias).filter(
                Hosts.is_deleted == 0).all()
            for hst in hosts:
                hosts_dict[hst.host_name] = hst.host_alias
        except Exception, e:
            pass
        return hosts_dict
