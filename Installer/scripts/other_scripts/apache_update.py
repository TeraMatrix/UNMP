import sys
import os

arg_li = sys.argv

if len(arg_li) == 2:
    instance_name = arg_li[1]
    file_path = '/omd/sites/%s/etc/apache/apache.conf'%instance_name
    if os.path.isfile(file_path):
        f = open(file_path,'r')
        li = f.readlines()
        f.close()
        flag_li = 0
        for i in range(0,len(li)):
            if li[i].find('Timeout'):
                pass
            else:
                li[i] = 'Timeout 360\n'
                
            if li[i].find('KeepAliveTimeout'):
                pass
            else:
                li[i] = 'KeepAliveTimeout 8\n'
                
            if li[i].find('KeepAlive '):
                pass
            else:
                li[i] = 'KeepAlive On\n'

            if li[i].find('MaxKeepAliveRequests'):
                pass
            else:
                li[i] = 'MaxKeepAliveRequests 100\n'

            if li[i].find("AddType application/octet-stream .csv") != -1:
                flag_li = 1
                
        if flag_li == 0:
            li.append("AddType application/octet-stream .csv\n")
            li.append("AddType application/octet-stream .xls\n")
            li.append("AddType application/octet-stream .doc\n")
            li.append("AddType application/octet-stream .avi\n")
            li.append("AddType application/octet-stream .mpg\n")
            li.append("AddType application/octet-stream .mov\n")
            li.append("AddType application/octet-stream .pdf\n")
            li.append("AddType application/octet-stream .xlsx\n")
            li.append("AddType application/octet-stream .docx\n")       

        f = open(file_path,'w')
        f.writelines(li)
        f.close()


