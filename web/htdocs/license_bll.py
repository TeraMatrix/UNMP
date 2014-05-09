#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 03-Nov-2011
@version: 0.1
@note: All database and model's functions that are use in license module.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in


@date: 21-Jan-2011
@version: 1.1
@note: Add new function that validate license file.
'''

# Import modules that contain the function and libraries
from unmp_model import *
from sqlalchemy.orm import sessionmaker
import xml.dom.minidom,os,sys,random,datetime
from datetime import datetime
#import #logging
#logging.basicConfig(filename='/omd/daemon/index_unmp.#log',format='%(levelname)s: %(asctime)s >> %(message)s', level=#logging.DEBUG)
#log = #logging.get#logger('#login')
from license import License

class LicenseBll(object):
    """
    @author: Yogesh
    @since: 22-Dec-2011
    @version: 0.1
    @note: License Upload and Manage Lincence Functions
    @organization: Codescape Consultants Pvt. Ltd.
    @copyright: 2011 Yogesh for Codescape Consultants Pvt. Ltd.
    @see: http://www.codescape.in
    """
    def get_license(self,salt_word):
        #nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        nms_instance = 'UNMP'
        try:
            license_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/license" % nms_instance
            if(os.path.isfile(license_file)):						# check config.xml file exist or not
                license_text = self.decoder(license_file,"123456")
                dom = xml.dom.minidom.parseString(license_text)			# create xml dom object of license.xml file
                return dom
            else:
                return 0                        
        except Exception,e:
            return str(e)    
        
    def allowed_license(self):
        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        try:
            Session = sessionmaker(bind=engine)     # making session of our current database
            session = Session()                 # creating new session object        
            license_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/license" % nms_instance
            if(os.path.isfile(license_file)):						# check config.xml file exist or not
                license_text = self.decoder(license_file,"123456")
                dom = xml.dom.minidom.parseString(license_text)			# create xml dom object of license.xml file
                company = ""
                date = ""
                dom_element = dom.getElementsByTagName("licensedto")			# get the element by tag name
                for elem in dom_element:
                    company = elem.getAttribute("name")
                    date = elem.getAttribute("expiredate")
                    lic_id = elem.getAttribute("id")
                liInfoObj = session.query(LicenseInfo.minutes).all()    
                if len(liInfoObj) > 0:
                    mins = int(liInfoObj[0][0])
                    date_li = []
                    format_li = [" Year, "," Month, "," Days, "," Hours, "," Mins, "]
                    if mins:
                        year = mins/525600
                        date_li.append(year)
                        mins = mins - (year*525600)
                        month = mins/43800
                        date_li.append(month)
                        mins = mins - (month*43800)
                        days = mins/1400
                        date_li.append(days)
                        mins = mins - (days*1440)
                        hours = mins/60
                        date_li.append(hours)
                        mins = mins - (hours*60)    
                        date_li.append(mins)
                        date = ""
                        for i in range(0,len(date_li)):
                            if date_li[i] > 0:
                                date += str(date_li[i])+format_li[i]
                        if len(date) > 3:
                            date = date[:-2]
                    else:
                        date = " 0 mins (Expired)"

                            
                host = [0,0,0]
                host[0] = self.get_allowed_object(dom,"host")
                host[1] = self.get_total_host()
                host[2] = int(host[0]) - int(host[1])
                
                ap25=[0,0,0]
                ap25[0] = self.get_tag_value(dom,"host","ap25")
                ap25[1] = self.get_total_host("ap25")[1] 
                ap25[2] = int(ap25[0]) - int(ap25[1])

                
                idu4=[0,0,0]
                idu4[0] = self.get_tag_value(dom,"host","idu4")
                idu4[1] = self.get_total_host("idu4")[1]
                idu4[2] = int(idu4[0]) - int(idu4[1])
                
                ubr=[0,0,0]
                ubr[0] = self.get_tag_value(dom,"host","odu16")
                ubr[1] = self.get_total_host("odu16")[1]
                ubr[2] = int(ubr[0]) - int(ubr[1])
                
                ubre=[0,0,0]
                ubre[0] = self.get_tag_value(dom,"host","odu100")
                ubre[1] = self.get_total_host("odu100")[1]
                ubre[2] = int(ubre[0]) - int(ubre[1])
                
                unknown=[0,0,0]
                unknown[0] = self.get_tag_value(dom,"host","unknown")
                unknown[1] = self.get_total_host("unknown")[1]
                unknown[2] = int(unknown[0]) - int(unknown[1])


                hostgroup = [0,0,0]
                hostgroup[0] = self.get_allowed_object(dom,"hostgroup")
                hostgroup[1] = self.get_total_hostgroup()
                hostgroup[2] = int(hostgroup[0]) - int(hostgroup[1])

                user = [0,0,0]
                user[0] = self.get_allowed_object(dom,"user")
                user[1] = self.get_total_user()
                user[2] = int(user[0]) - int(user[1])
                
                super_admin=[0,0,0]
                super_admin[0] = self.get_tag_value(dom,"user","SuperAdmin")
                super_admin[1] = self.get_total_user("SuperAdmin")[1]
                super_admin[2] = int(super_admin[0]) - int(super_admin[1])
                
                admin=[0,0,0]
                admin[0] = self.get_tag_value(dom,"user","Admin")
                admin[1] = self.get_total_user("Admin")[1]
                admin[2] = int(admin[0]) - int(admin[1])
                
                operator=[0,0,0]
                operator[0] = self.get_tag_value(dom,"user","User")
                operator[1] = self.get_total_user("User")[1]
                operator[2] = int(operator[0]) - int(operator[1])
                
                guest=[0,0,0]
                guest[0] = self.get_tag_value(dom,"user","Guest")
                guest[1] = self.get_total_user("Guest")[1]
                guest[2] = int(guest[0]) - int(guest[1])

                usergroup = [0,0,0]
                usergroup[0] =self.get_allowed_object(dom,"usergroup")
                usergroup[1] = self.get_total_usergroup()
                usergroup[2] = int(usergroup[0]) - int(usergroup[1])
                
                host_device_type= [ap25,idu4,ubr,ubre,unknown]
                user_type = [super_admin,admin,operator,guest]

                return company,date,host,hostgroup,user,usergroup,host_device_type,user_type
            else:
                return "license file not found."
        except Exception,e:
            return e

    def update_license_details(self):
        try:
            Session = sessionmaker(bind=engine)     # making session of our current database
            session = Session()                 # creating new session object
            dom = self.get_license("#xs34S")                
            dom_elements = dom.getElementsByTagName("licensedto")
            for elem in dom_elements:
                lic_id = elem.getAttribute("id")
                issue_date = elem.getAttribute("issuedate")
                expire_date = elem.getAttribute("expiredate")
                name = elem.getAttribute("name")
                idt = datetime.strptime(issue_date,"%Y-%m-%d")
                edt = datetime.strptime(expire_date,"%Y-%m-%d")
                dl = edt -idt
                ms = divmod(dl.days * 86400 + dl.seconds, 60)[0]
                liObj = LicenseDetails(lic_id,name,issue_date,expire_date)
                session.add(liObj)
                liInfoObj = session.query(LicenseInfo).all()
                liInfoObj[0].minutes = int(ms)
                liInfoObj[0].last_check_date = datetime.now()
                liInfoObj[0].is_valid = 0    
            session.commit()                           
        except Exception,e:
            print str(e)
        finally:
            session.close()                     # close the session object           

    def get_allowed_object(self,dom,tagname,attrname=None):
        dom_element = dom.getElementsByTagName(tagname)			# get the element by tag name
        value = []
        for elem in dom_element:
            value.append(str(elem.getAttribute("allow")))
            if attrname:
                value.append(str(elem.getAttribute(attrname)))
        if attrname:
            return value
        else:
            return value[0] if len(value) > 0 else ""

    def get_tag_value(self,dom,tagname,attribute):
        dom_element = dom.getElementsByTagName(tagname)			# get the element by tag name
        value = ""
        for elem in dom_element:
            value = elem.getAttribute(attribute)
        return value
        
    def get_allowed_host(self,device_type=None):
        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        try:
            license_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/license" % nms_instance
            if(os.path.isfile(license_file)):						# check config.xml file exist or not
                license_text = self.decoder(license_file,"123456")
                dom = xml.dom.minidom.parseString(license_text)			# create xml dom object of license.xml file
                host = 0
                host = self.get_allowed_object(dom,"host")
                if device_type:
                    host = self.get_allowed_object(dom,"host",device_type)
                return host
            else:
                return 0
        except Exception,e:
            return e
    
    def update_device_type(self):  
        try:
            Session = sessionmaker(bind=engine)     # making session of our current database
            session = Session()                 # creating new session object
            devices = session.query(DeviceType.device_type_id).all()
            if len(devices) > 0:
                devices = sum(devices,())
            dom = self.get_license("#xs34S")                
            dom_elements = dom.getElementsByTagName("host")
            for elem in dom_elements:
                for device in devices:
                    if device == 'unknown':
                        pass
                    else:
                        temp = elem.getAttribute(device)
                        if temp != '':
                            deviceObj = session.query(DeviceType).filter(DeviceType.device_type_id==device).all()
                            deviceObj[0].is_deleted = 0
            session.commit()                           
        except Exception,e:
            pass
        finally:
            session.close()                     # close the session object                    
            
    def get_allowed_hostgroup(self):
        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        try:
            license_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/license" % nms_instance
            if(os.path.isfile(license_file)):						# check config.xml file exist or not
                license_text = self.decoder(license_file,"123456")
                dom = xml.dom.minidom.parseString(license_text)			# create xml dom object of license.xml file
                hostgroup = 0
                hostgroup = self.get_allowed_object(dom,"hostgroup")
                return hostgroup
            else:
                return 0
        except Exception,e:
            return e

    def get_allowed_user(self,user_group=None):
        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        try:
            license_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/license" % nms_instance
            if(os.path.isfile(license_file)):						# check config.xml file exist or not
                license_text = self.decoder(license_file,"123456")
                dom = xml.dom.minidom.parseString(license_text)			# create xml dom object of license.xml file
                user = 0
                user = self.get_allowed_object(dom,"user")
                if user_group:
                    user = self.get_allowed_object(dom,"user",user_group)
                return user
            else:
                return 0
        except Exception,e:
            return e

    def get_allowed_usergroup(self):
        nms_instance = __file__.split("/")[3]       # it gives instance name of nagios system
        try:
            license_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/license" % nms_instance
            if(os.path.isfile(license_file)):						# check config.xml file exist or not
                license_text = self.decoder(license_file,"123456")
                dom = xml.dom.minidom.parseString(license_text)			# create xml dom object of license.xml file
                usergroup = 0
                usergroup = self.get_allowed_object(dom,"usergroup")
                return usergroup
            else:
                return 0
        except Exception,e:
            return e

    def get_total_host(self,device_type=None):
        Session = sessionmaker(bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hosts = []
            hosts.append(session.query(Hosts).count())          # execute query and fetch data
            if device_type:
                hosts.append(session.query(Hosts).filter(Hosts.device_type_id==device_type).count())          # execute query and fetch data                            
            if device_type:
                return hosts
            else:
                return hosts[0] if len(hosts) > 0 else 0

        except Exception,e:
            return e
        finally:
            session.close()                     # close the session object

    def get_total_hostgroup(self):
        Session = sessionmaker(bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            hostgroups = session.query(Hostgroups).count()          # execute query and fetch data
            return hostgroups
        except Exception,e:
            return e
        finally:
            session.close()                     # close the session object

    def get_total_user(self,user_group=None):
        Session = sessionmaker(bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            users = []
            users.append(session.query(Users).count())          # execute query and fetch data
            if user_group:
                users.append(session.query(UsersGroups.group_id).filter(and_(UsersGroups.group_id==Groups.group_id,Groups.group_name==user_group)).count())          # execute query and fetch data            
            if user_group:
                return users
            else:
                return users[0] if len(users) > 0 else 0
        except Exception,e:
            return e
        finally:
            session.close()                     # close the session object

    def get_total_usergroup(self):
        Session = sessionmaker(bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            usergroups = session.query(Groups).filter(Groups.is_default == 0).count()          # execute query and fetch data
            return usergroups
        except Exception,e:
            return e
        finally:
            session.close()                     # close the session object

    def check_license_for_host(self,device_type=None):
        try:
            if device_type:
                allowed_host_li = self.get_allowed_host(device_type)
                total_host_li = self.get_total_host(device_type)            
                host = int(allowed_host_li[0]) - int(total_host_li[0])
                host_co = int(allowed_host_li[1]) - int(total_host_li[1])
            else:        
                host = int(self.get_allowed_host()) - int(self.get_total_host())
            #return " eeeeeee %s,%s"%(str(allowed_host_li),str(total_host_li))
            if host>0:
               if device_type:
                    if host_co > 0:
                        return True
                    else:
                        return "deviceTypeFalse"
               else:
                    return True
            else:
                return False
        except Exception,e:
            return e
    
    def get_device_type(self,host_id):
        Session = sessionmaker(bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            device_type = session.query(Hosts.device_type_id).filter(Hosts.host_id==host_id).all()         # execute query and fetch data
            return device_type[0][0] if len(device_type) > 0 else "unknown"
        except Exception,e:
            return str(e)
        finally:
            session.close()           
    
    def check_license_for_host_edit(self,device_type=None,host_id=None):
        try:
            if device_type != self.get_device_type(host_id):
                allowed_host_li = self.get_allowed_host(device_type)
                total_host_li = self.get_total_host(device_type)            
                host = int(allowed_host_li[0]) - int(total_host_li[0])
                host_co = int(allowed_host_li[1]) - int(total_host_li[1])
                #return " eeeeeee %s,%s"%(str(allowed_host_li),str(total_host_li))
                if host_co > 0:
                    return True
                else:
                    return False
            else:
                return True
        except Exception,e:
            return e            

    def check_license_for_hostgroup(self):
        try:
            hostgroup = int(self.get_allowed_hostgroup()) - int(self.get_total_hostgroup())
            if hostgroup>0:
                return True
            else:
                return False
        except Exception,e:
            return False
    
    def get_group_name(self,user_id):
        Session = sessionmaker(bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            usergroups = session.query(Groups.group_name).filter(and_(Groups.group_id==UsersGroups.group_id,UsersGroups.user_id==user_id)).all()         # execute query and fetch data
            return usergroups[0][0] if len(usergroups) > 0 else "default"
        except Exception,e:
            return str(e)
        finally:
            session.close()            
        
    def check_license_for_user(self,user_group=None):
        try:
            if user_group:
                allowed_user_li = self.get_allowed_user(user_group)
                total_user_li = self.get_total_user(user_group)            
                user = int(allowed_user_li[0]) - int(total_user_li[0])
                user_co = int(allowed_user_li[1]) - int(total_user_li[1])            
            else:
                user = int(self.get_allowed_user()) - int(self.get_total_user())
#            return " dddddddd %s,%s eeeeeee %s,%s"%(user,user_co,str(allowed_user_li),str(total_user_li))
            if user>0:
                if user_group:
                    if user_co > 0:
                        return True
                    else:
                        return "groupFlase"
                else:
                    return True
            else:
                return False
        except Exception,e:
            return False
                
    
    def check_license_for_group(self,user_group=None,user_id=None):
        try:
            #f = open('/omd/daemon/abc.txt','w+')
            #f.write(user_group)
            #f.write(user_id)
            #f.write(self.get_group_name(user_id))
            if user_group != self.get_group_name(user_id):         
                allowed_user_li = self.get_allowed_user(user_group)
                total_user_li = self.get_total_user(user_group)            
                user_co = int(allowed_user_li[1]) - int(total_user_li[1])            
    #            return " dddddddd %s eeeeeee %s,%s"%(user_co,str(allowed_user_li),str(total_user_li))                
                if user_co > 0:
                    return True
                else:
                    return False
            else:
                return True
            #f.close()                 
        except Exception,e:
            #f.write("sssss"+str(e))
            #f.close()
            return False
            
    def check_license_for_useringroup(self,user_group=None):
        try:
        
            allowed_user_li = self.get_allowed_user(user_group)
            total_user_li = self.get_total_user(user_group)            
            user_co = int(allowed_user_li[1]) - int(total_user_li[1])            
#            return " dddddddd %s eeeeeee %s,%s"%(user_co,str(allowed_user_li),str(total_user_li))                

            if user_co > 0:
                return user_co
            else:
                return 0
                
        except Exception,e:
            return 0
                        
    def check_license_for_usergroup(self):
        try:
            usergroup = int(self.get_allowed_usergroup()) - int(self.get_total_usergroup())
            if usergroup>0:
                return True
            else:
                return False
        except Exception,e:
            return False

    def encoder(self,path,pwd,topath):
        k = long(pwd) # key   # password in int
        f1 = open( path, "rb") # xml file path
        bytearr = map (ord, f1.read() ) 
        f1.close()
        f2 = open( topath, "wb" ) # path for .rg file to write
        random.seed(k)
        x_str = ""
        for i in range(len(bytearr)):
            byt = (bytearr[i] + random.randint(0, 255)) % 256
            f2.write(chr(byt))
        f2.close()

    def decoder(self,path,pwd):
        k = long(pwd) # key
        f1 = open( path, "rb")
        bytearr = map (ord, f1.read())
        f1.close()
        random.seed(k)
        x_str = ""
        for i in range(len(bytearr)):
            byt = ((bytearr[i] - random.randint(0, 255)) + 256 ) % 256
            x_str += chr(byt)
        return x_str
        
    def validate_license(self,file_data):
        session = None
        try:
            Session = sessionmaker(bind=engine)     # making session of our current database    
            k = long("123456") # key
            bytearr = map (ord, file_data)
            random.seed(k)
            license_text = ""
            if file_data == None or file_data == "":
                return {"success":1,"msg":"noLicenseFile"}
             
            for i in range(len(bytearr)):
                byt = ((bytearr[i] - random.randint(0, 255)) + 256 ) % 256
                license_text += chr(byt)
        except Exception,e:
            return {"success":1,"msg":str(e)}
                   
            
        try:
            dom = xml.dom.minidom.parseString(license_text)            # create xml dom object of license.xml file
            company = None
            expire_date = None
            dom_element = dom.getElementsByTagName("licensedto")            # get the element by tag name
            for elem in dom_element:
                company = elem.getAttribute("name")
                expire_date = elem.getAttribute("expiredate")
                lic_id = elem.getAttribute("id")
                issue_date = elem.getAttribute("issuedate")
            dom_element = dom.getElementsByTagName("host")            # get the element by tag name
            for elem in dom_element:
                allow_host = elem.getAttribute("allow")
                ubr_host = elem.getAttribute("odu16")
                ubre_host = elem.getAttribute("odu100")
                idu_host = elem.getAttribute("idu4")
                ap_host = elem.getAttribute("ap25")
            dom_element = dom.getElementsByTagName("user")            # get the element by tag name
            for elem in dom_element:
                allow_user = elem.getAttribute("allow")
                su_user = elem.getAttribute("SuperAdmin")
                admin_user = elem.getAttribute("Admin")
                op_user = elem.getAttribute("User")
                guest_user = elem.getAttribute("Guest")

            

            if company == None or expire_date == None or lic_id == None or issue_date == None:
                return {"success":1,"msg":"invalidLicenseFile"}
            else:
                session = Session()                 # creating new session object
                is_negative = 0
                liObj = session.query(LicenseDetails.license_id).filter(LicenseDetails.license_id==lic_id).all()
                #liObj2 = session.query(LicenseDetails.issued_client).filter(LicenseDetails.issued_client!=company).all()                
                if len(liObj) <= 0: #and len(liObj2) <= 0: 
                    date_obj = datetime.strptime(expire_date,"%Y-%m-%d")
                    now_date_obj = datetime.now()
                    if now_date_obj<=date_obj:
                        #log.info(" ok 1")
                        host = [0,0,0]
                        host[0] = self.get_allowed_object(dom,"host")
                        host[1] = self.get_total_host()
                        host[2] = int(host[0]) - int(host[1])
                        if host[2] < 0:
                            is_negative = 1
                        ap25=[0,0,0]
                        ap25[0] = self.get_tag_value(dom,"host","ap25")
                        ap25[1] = self.get_total_host("ap25")[1]
                        ap25[2] = int(ap25[0]) - int(ap25[1])
                        if ap25[2] < 0:
                            is_negative = 1
                                                    
                        idu4=[0,0,0]
                        idu4[0] = self.get_tag_value(dom,"host","idu4")
                        idu4[1] = self.get_total_host("idu4")[1]
                        idu4[2] = int(idu4[0]) - int(idu4[1])
                        if idu4[2] < 0:
                            is_negative = 1
                                                    
                        ubr=[0,0,0]
                        ubr[0] = self.get_tag_value(dom,"host","odu16")
                        ubr[1] = self.get_total_host("odu16")[1]
                        ubr[2] = int(ubr[0]) - int(ubr[1])
                        if ubr[2] < 0:
                            is_negative = 1                        
                        
                        ubre=[0,0,0]
                        ubre[0] = self.get_tag_value(dom,"host","odu100")
                        ubre[1] = self.get_total_host("odu100")[1]
                        ubre[2] = int(ubre[0]) - int(ubre[1])
                        if ubre[2] < 0:
                            is_negative = 1                        
                        
                        unknown=[0,0,0]
                        unknown[0] = self.get_tag_value(dom,"host","unknown")
                        unknown[1] = self.get_total_host("unknown")[1]
                        unknown[2] = int(unknown[0]) - int(unknown[1])
                        if unknown[2] < 0:
                            is_negative = 1

                        hostgroup = [0,0,0]
                        hostgroup[0] = self.get_allowed_object(dom,"hostgroup")
                        hostgroup[1] = self.get_total_hostgroup()
                        hostgroup[2] = int(hostgroup[0]) - int(hostgroup[1])
                        if hostgroup[2] < 0:
                            is_negative = 1                        

                        user = [0,0,0]
                        user[0] = self.get_allowed_object(dom,"user")
                        user[1] = self.get_total_user()
                        user[2] = int(user[0]) - int(user[1])
                        if user[2] < 0:
                            is_negative = 1                        
                        
                        super_admin=[0,0,0]
                        super_admin[0] = self.get_tag_value(dom,"user","SuperAdmin")
                        super_admin[1] = self.get_total_user("SuperAdmin")[1]
                        super_admin[2] = int(super_admin[0]) - int(super_admin[1])
                        if super_admin[2] < 0:
                            is_negative = 1                        
                        
                        admin=[0,0,0]
                        admin[0] = self.get_tag_value(dom,"user","Admin")
                        admin[1] = self.get_total_user("Admin")[1]
                        admin[2] = int(admin[0]) - int(admin[1])
                        if admin[2] < 0:
                            is_negative = 1                        
                        
                        operator=[0,0,0]
                        operator[0] = self.get_tag_value(dom,"user","User")
                        operator[1] = self.get_total_user("User")[1]
                        operator[2] = int(operator[0]) - int(operator[1])
                        if operator[2] < 0:
                            is_negative = 1                        
                        
                        guest=[0,0,0]
                        guest[0] = self.get_tag_value(dom,"user","Guest")
                        guest[1] = self.get_total_user("Guest")[1]
                        guest[2] = int(guest[0]) - int(guest[1])
                        if guest[2] < 0:
                            is_negative = 1                        
                        

                        usergroup = [0,0,0]
                        usergroup[0] =self.get_allowed_object(dom,"usergroup")
                        usergroup[1] = self.get_total_usergroup()
                        usergroup[2] = int(usergroup[0]) - int(usergroup[1])
                        if usergroup[2] < 0:
                            is_negative = 1                        
                            
                        if is_negative:
                            host_device_type= [ap25,idu4,ubr,ubre,unknown]
                            user_type = [super_admin,admin,operator,guest]
                            #log.info(" ok 4")
                            html_str = License.invalid_license(host,hostgroup,user,usergroup,host_device_type,user_type)
                            #log.info(" ok 5")
                            return {"success":2,"msg":"invalidLicenseFile","data":html_str}
                        else:
                            return {"success":0}
                    else:
                        return {"success":1,"msg":"expiredLicenseFile"} 
                else:
                    return {"success":1,"msg":"invalidLicenseFile"}
        except Exception,e:
            return {"success":1,"msg":"invalidLicenseFile"}
        finally:
            if session != None:
                session.close()             

            
#l = LicenseBll()
#print "ok"
#l.update_license_details()
