# Import modules that contain the function and libraries
from datetime import date,timedelta,datetime
import subprocess,os,tarfile,calendar,time
MySql_file = '/omd/daemon/config.rg'
if(os.path.isfile(MySql_file)):    # getting variables from config file    
	execfile(MySql_file)
else:
	hostname = "localhost"
	username = "root"
	password = "root"
	schema = "nmsp"

def create_backup(month_var,schema):
        try:
            nms_instance = "UNMP"#__file__.split("/")[3]       # it gives instance name of nagios system
            month_var=month_var.split('_')
            year=month_var[0]
            month=month_var[1]
            cur_db=schema
            path_backup='/omd/daemon/mysql_backup' 
            path_temp='/omd/daemon/mysql_temp/%s_%s' %(year,month)
            str_time="timestamp between '%s-%s-01 00:00:00' and '%s-%s-31 23:59:59' " %(year,month,year,month)
            path_sh='/omd/daemon/mysql_backup.sh' 
            proc=subprocess.Popen(['sh',path_sh,path_temp,str_time,cur_db], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	    output, err = proc.communicate()
            buf_data = output
	    dstfolder = path_backup # where backup will be stored
	    fileorfolder = path_temp # which file you want backup of
	    time.sleep(5)
	    dst = '%s.tar.bz2' % os.path.join(dstfolder, os.path.basename(fileorfolder))
	    out = tarfile.TarFile.open(dst, 'w:bz2')
	    out.add(fileorfolder, arcname=os.path.basename(fileorfolder))
	    out.close()
	    return "done"
        except Exception,e:
            return str(e)  
            
def remove_data(month_var,schema):
        try:
            nms_instance = "UNMP"#__file__.split("/")[3]       # it gives instance name of nagios system
            month_var=month_var.split('_')
            year=month_var[0]
            month=month_var[1]
            cur_db=schema
            str_time=" where timestamp between '%s-%s-01 00:00:00' and '%s-%s-31 23:59:59' " %(year,month,year,month)
            path_sh='/omd/daemon/mysql_remove_data.sh' 
            proc=subprocess.Popen(['sh',path_sh,str_time,cur_db], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	    output, err = proc.communicate()
            buf_data = output
	    return buf_data
        except Exception,e:
            return str(e)  


now = datetime.now()
month_str=""
month_var=now.month-3
year_var=now.year
if month_var<=0:
    year_var=year_var-1
    mon=-mon
    mon=12-mon
d = datetime.now()
m = d.month
y = d.year
n = 10 # month till before you want
li = []
for i in range(3):
    m -= 1
if m < 0:
    y = d.year - 1
    m = 12 - abs(m)
elif m > 0:
    for i in range(0,m):
	li.append(str(y)+"_"+str(m))
	m -= 1
    y = y-1

for i in range(0,12-m-n):
    li.append(str(y)+"_"+str(12-i))

li.reverse() 
file_name=li[0]+"tar.bz2"
if(os.path.isfile(file_name)):
    pass
else:
    create_backup(li[0],schema)
    remove_data(li[0],schema)
