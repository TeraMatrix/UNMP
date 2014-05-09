#!/usr/bin/python2.6

import os.path
import sys
import htmllib
import config
from lib import *


def create_maps(h):
    global html
    html = h
    sitename = __file__.split("/")[3]
    html.new_header("Network Map")
    html.write(
        "<div class=\"loading\" style=\"display:block;\"><img src='images/loading.gif' alt='loading...'/></div>")
    html.write(
        "<script>setTimeout(function(){ parent.main.location='/%s/nagvis/index.php?mod=Map&act=view&show=Test4'; },2000);</script>" % sitename)
    data = """define global {
  context_menu=1
  context_template=default
  hover_menu=1
  hover_delay=0
  hover_template=default
  hover_childs_show=1
  hover_childs_limit=10
  hover_childs_order=asc
  hover_childs_sort=s
  iconset=std_small
  line_arrow=forward
  line_cut=0.5
  label_show=1
  label_text=[name]
  label_x=-20
  label_y=+20
  label_width=auto
  label_background=transparent
  label_border=transparent
  label_style=
  only_hard_states=0
  recognize_services=1
  url_target=_self
  map_image=Test.png
}"""
    try:
        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: name parents\n"
        hosts = html.live.query(query)
        hosts.sort()
        html.live.set_prepend_site(False)
        x = 0
        y = 40
        x1 = 800
        # y1=350
        parent = []
        parent = "localhost"
        host_array = {}
        parent_array = []
        relation = []
        all_host = []
        child_host = []
        relation_dic = {}
        temp1 = []
        level = []
        prafull = []
        temp = []
        temp3 = []
        temp2 = []
        check = 0
        i = 0
        j = 0
        count = 1
        flag = 0
        #  host_array[host]=[x,y]
        for site, host, parents in hosts:
            # html.write(host)
            if host == 'localhost':
                host_array[host] = [630, 50]
                data += "\ndefine host {\
				\nhost_name=%s\
				  \nz=98\
				  \nview_type=icon\
				  \nurl=/%s/check_mk/view.py?view_name=host&host=[host_name]&site=\
				 \nx=%s\
				 \ny=%s\
				\n}" % (host, sitename, host_array[host][0], host_array[host][1])
            for p in parents:
                parent_array.append([])
                parent_array[j].append(host)
                parent_array[j].append(p)
                j += 1
            i += 1
            # html.write("hi prafull ")
            all_host.append(host)

        for j in range(len(parent_array)):    # only one time execution
            temp = []
            child_host.append(parent_array[j][0])
            for k in range(len(parent_array)):
                if parent == parent_array[k][1]:
                    temp.append(parent_array[k][0])
                    flag = 1

                    # html.write(parent_array[k][0])
                k += 1
                #	if flag==1:
                #		y+=100
                #		x=0
                #		flag=0
                #	parent=temp1[j]
                #			html.write(str(temp))
            if j == 0:
                # html.write("hi test")
                temp3 = temp
                temp4 = len(temp)
                # 	html.write(str(temp4))
                #	html.write("")

        temp = []
        i = 0
        temp.append("localhost")
        yo = []
        yo_i = 0
        while len(temp) > 0:
            temp2 = []
            for host in temp:
            # html.write(str(host))
                temp3 = []
                for k in range(len(parent_array)):
                    if host == parent_array[k][1]:
                        yo_i += 1
                        temp2.append(
                            parent_array[k][0])
                        temp1.append(
                            parent_array[k][1])
                        # relation_dic = {"temp2.append(parent_array[k][1])":"temp1.append(parent_array[k][0])" }
                        # html.write(relation_dic)
                        temp3.append(
                            parent_array[k][0])
                        # child_host.append(parent_array[k][0])
                        # html.write("after data fill
                        # ")
                    k += 1
                yo.append(yo_i)
                yo_i = 0

            y += 200
            x = 0

            for host in temp2:
                count += 1
                if len(temp2) > 100:
                    x1 = (len(temp2) - 800) + x1
                else:
                    x1 = x1

                x += x1 / len(temp2)
                host_array[host] = [x, y]
                #			html.write(str(host_array[host]))
                # html.write("set node position  ")
                data += "\ndefine host {\
					\nhost_name=%s\
					  \nz=98\
					  \nview_type=icon\
					  \nurl=/%s/check_mk/view.py?view_name=host&host=[host_name]&site=\
					 \nx=%s\
					 \ny=%s\
					\n}" % (host, sitename, host_array[host][0], host_array[host][1])
            temp = []
            temp = temp2
            # html.write(str(temp))
            i += 1
            yo = []

        y += 200
        x = 0
        count = 0
        #		html.write(str(i))
        #		html.write(str(child_host))
        for host in all_host:
            if host not in child_host:
                if "localhost" != host:
                    if count > 6:
                        x = 0
                        y += 70
                    count += 1
                    x += 100
                    #					html.write(str(host))
                    host_array[host] = [x, y]
                    data += "\ndefine host {\
					\nhost_name=%s\
					  \nz=98\
					  \nview_type=icon\
					  \nurl=/%s/check_mk/view.py?view_name=host&host=[host_name]&site=\
					 \nx=%s\
					 \ny=%s\
					\n}" % (host, sitename, host_array[host][0], host_array[host][1])

                    # mail_dict[i]=[host,temp3]
                    # html.write(str(mail_dict[1]))
                #		for i in range(len(mail_dict)):
                #			html.write(str(mail_dict[i]))
                #			html.write("<br></br>")
                #		html.write(str(mail_dict))
                # html.write("after ")
                #		html.write(str(prafull))
        for p in parent_array:
            data += "\ndefine host {\
				\nhost_name=%s\
				\nx=%s,%s\
				\ny=%s,%s\
				\nview_type=line\
				\nline_type=11\
				\n}" % (p[1], host_array[p[1]][0], host_array[p[0]][0], host_array[p[1]][1], host_array[p[0]][1])

        # os.chmod('/omd/sites/%s/etc/nagvis/maps/Test4.cfg' %
        # sitename, 777)
        f1 = open(
            '/omd/sites/%s/etc/nagvis/maps/Test4.cfg' % sitename, 'w')
        f1.writelines(data)

        f1.close()
        # html.write(str(parent_array))
    except Exception, e:
        # html.write(str(sys.exc_info()))
        html.write("Eception")
    html.new_footer()
