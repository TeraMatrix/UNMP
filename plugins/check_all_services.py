#!/usr/bin/python2.6 -tt
import sys
import subprocess


def main():
    msg_dict = {"ndo2db": "ndo2db (pid", "snmptt": "snmptt (pid"}
                                   #,"snmpd":"snmpd (pid","snmptrapd":"snmptrapd (pid","MySQL":"MySQL running"}
    result_dict = {"ndo2db": 0, "snmptt": 0}
        #,"snmpd":0,"snmptrapd":0,"MySQL":0}
    result_str = ""
    try:
        NOT_UP = 0
        some_problem = 0
        status = ""
        try:
            proc = subprocess.Popen(["service", "--status-all"],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, _ = proc.communicate()
            code = proc.wait()
        except ValueError as e:
            some_problem = 1
            NOT_UP = 1
            status = " Nagios Plugin for All Services Status is giving Error \n Please Contact your SuperAdmin, Nothing you can do about it"
        except Exception as e:
            some_problem = 1
            NOT_UP = 1
            status = " Nagios Plugin for All Services Status is giving Error \n Please Contact your SuperAdmin, Nothing you can do about it "

        if some_problem == 0:
            if str(code) == str(0):
                for key in msg_dict:
                    if output.find(msg_dict[key]) == -1:
                        result_dict[key] = 1
            else:
                NOT_UP = 1
                status = " Command output is None "
        flag = 0
        for key in result_dict:
            if result_dict[key]:
                NOT_UP = 1
                if flag == 0:
                    result_str += "Service " + key + " is NOT runing"
                    flag = 1
                else:
                    result_str += "\nService " + key + " is NOT runing"

    except Exception as e:
        some_problem = 1
        NOT_UP = 1
        status = " Nagios Plugin for All Services Status is giving Error \n Please Contact your SuperAdmin, Nothing you can do about it"

    finally:
        if NOT_UP == 0 and some_problem == 0:
            print " All Services is Running   : OK"
            sys.exit(0)
        if NOT_UP == 0 and some_problem == 1:
            print " All Services is Running   : Warning"
            sys.exit(1)
        if NOT_UP == 1 and some_problem == 0:
            print " Services is NOT Running "
            print result_str
            sys.exit(2)
        if NOT_UP == 1 and some_problem == 1:
            print status
            sys.exit(4)
        else:
            print " All Services is NOT running   : UNKNOWN"
            sys.exit(4)

if __name__ == '__main__':
    main()
