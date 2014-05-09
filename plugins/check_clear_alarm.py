#!/usr/bin/python2.6 -tt
import time
import sys

import logging

global file_name
global pidfile

file_name = "/omd/daemon/tmp/Clear.time"
pidfile = "/omd/daemon/tmp/unmp-clearalarm.pid"


def get_status():
    global pidfile
    try:
        pf = file(pidfile, 'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None
    except Exception,err:
        return 3
    try:
        procfile = file("/proc/%d/status" % pid, 'r')
        procfile.close()
    except IOError,err:
        return 2		#+str(type(pid))# sys.stdout.write("  *Probably Daemon Service is not running. There is not a process with the PID specified in PidFile  **try to start it\n")
    except TypeError,err:
        return 1		#+str(type(pid))#sys.stdout.write("  *Daemon Service is not running. \n")
    except Exception,err:
        return 3	
    return pid 			#sys.stdout.write("  *Daemon Service with the PID %d is  OK \n" % pid)


def read_time():
    global file_name
    try:
        f = open(file_name,'r')
    except IOError, err:
        return 1
    return f.readlines()


def main():
    try:
        status = ""
        some_problem = 0
        start_time = " -- "
        stop_time = " -- "
        __t = []
        _t = type(__t)
        file_lines = read_time()
 
        if type(file_lines) == _t:
            if len(file_lines) > 1:
                start_time = file_lines[0]    
                stop_time = file_lines[1]
            else:
                start_time = file_lines[0]
        elif file_lines == 1:
            some_problem = 1
            status = " Not able to read Start Stop time of Daemon "    

        pid = get_status()
        if pid == 2:
            NOT_UP = 1
            some_problem = 1
            status = "*Probably Daemon Service is not running. There is not a process with the PID specified in PidFile \n  **try to start it"
        elif pid == 3:
            some_problem = 1
            NOT_UP = 1
            status = " Nagios Plugin for Daemon Status Check is giving Error \n Please Contact your SuperAdmin, Nothing you can do about it"
        elif pid == 1:
            NOT_UP = 1
        else:
            NOT_UP = 0
   

            
    except Exception as e:
        some_problem = 1
        NOT_UP = 1
        status = " Nagios Plugin for Daemon Status is giving Error \n Please Contact your SuperAdmin, Nothing you can do about it"

    finally:
        if NOT_UP == 0 and some_problem == 0 :
            print " UNMP - Clear Alarm is Running   : OK"		
            print " daemon process id   : %s "%str(pid)
            print " Start Time   : %s "%str(start_time)
            print " Last Stop Time  : %s "%str(stop_time)
            sys.exit(0)
        if NOT_UP == 0 and some_problem == 1:
            print " UNMP - Clear Alarm is Running   : Warning"  #not able to  start time
            print " daemon process id   : %s "%str(pid)
            print " Start Time   : %s "%str(start_time)
            print " Last Stop Time  : %s "%str(stop_time)
            print " Special Comment : %s "%str(status)
            sys.exit(1)
        if NOT_UP == 1 and some_problem == 1:
            print " UNMP - Clear Alarm is NOT running   : Critical"
            print " Stop Time   : %s "%str(stop_time)
            print " Last Start Time  : %s "%str(start_time)
            print " Special Comment : %s "%str(status)
            sys.exit(3)
        else:
            print " UNMP - Clear Alarm is NOT running   : Critical"
            print " Stop Time   : %s "%str(stop_time)
            print " Last Start Time  : %s "%str(start_time)
            sys.exit(2)

  	#print " OUTPUT : NOT_UP : ",NOT_UP," || dict_for_nagios : ",dict_for_nagios," || total devices : ",total_devices," || set_devices : ",set_devices," || "
if __name__ == '__main__':
    main()

