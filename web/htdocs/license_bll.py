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
import logging
import traceback
logging.basicConfig(filename='/omd/daemon/log/error_log',format='%(levelname)s: %(asctime)s : %(module)s >> %(message)s', level=logging.DEBUG)
log = logging.getLogger('License')
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
    def __init__(self):
        pass
    
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


                host = {}
                device_names = self.get_pretty_devicename()
                for k,v in self.get_tag_attributes(dom,"host").items():
                    temp_li = [0,0,0,0]
                    temp_li[1] = v
                    if k == 'allow':
                        temp_li[2] = self.get_total_host()
                        temp_li[0] = 'Host '
                    else:
                        temp_li[2] = self.get_total_host(k)[1] 
                        temp_li[0] = device_names.get(k,k)
                    temp_li[3] = int(temp_li[1]) - int(temp_li[2])
                    host[k] = temp_li
                                            
                hostgroup_li = [0,0,0,0]
                hostgroup_li[0] = 'Host Group'
                hostgroup_li[1] = self.get_allowed_object(dom,"hostgroup")
                hostgroup_li[2] = self.get_total_hostgroup()
                hostgroup_li[3] = int(hostgroup_li[1]) - int(hostgroup_li[2])
                

                user = {}
                for k,v in self.get_tag_attributes(dom,"user").items():
                    temp_li = [0,0,0,0]
                    temp_li[1] = v
                    if k == 'allow':
                        temp_li[2] = self.get_total_user()
                        temp_li[0] = 'User '
                    else:
                        temp_li[2] = self.get_total_user(k)[1]
                        temp_li[0] = k
                    temp_li[3] = int(temp_li[1]) - int(temp_li[2])
                    user[k] = temp_li                

                usergroup_li = [0,0,0,0]
                usergroup_li[0] = 'User Group'
                usergroup_li[1] =self.get_allowed_object(dom,"usergroup")
                usergroup_li[2] = self.get_total_usergroup()
                usergroup_li[3] = int(usergroup_li[1]) - int(usergroup_li[2])

                return_dict = {}
                return_dict['host'] = host
                return_dict['hostgroup'] = {'allow' :hostgroup_li}
                return_dict['user'] = user
                return_dict['usergroup'] = {'allow' :usergroup_li}            
                return company,date,return_dict
            else:
                return "license file not found."
        except Exception,e:
            #log.error(traceback.format_exc())
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

    def get_tag_attributes(self,dom,tagname):
        dom_element = dom.getElementsByTagName(tagname)			# get the element by tag name
        atr_dict = {}
        for elem in dom_element:
            for (atr,val) in elem.attributes.items():
                atr_dict[str(atr)] = str(val)
        return atr_dict

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
            dom = self.get_license("#xs34S")                
            dom_dict = self.get_tag_attributes(dom,"host")
            device_list = [ k for k,v in dom_dict.items() if v != '' and int(v) > 0 ]
            if device_list > 0:
                for device in session.query(DeviceType).filter(DeviceType.device_type_id.in_(device_list)):
                    device.is_deleted = 0
                session.commit()                           
        except Exception,e:
            import traceback
            #log.error(traceback.format_exc())
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

    def get_pretty_devicename(self):
        Session = sessionmaker(bind=engine)     # making session of our current database
        try:
            session = Session()                 # creating new session object
            device_names = {}
            # execute query and fetch data                            
            for k,v in session.query(DeviceType.device_type_id, DeviceType.device_name):
                device_names[k] = v
            return device_names
        except Exception,e:
            return {} #,e
        finally:
            session.close()         
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
                        host = {}
                        device_names = self.get_pretty_devicename()
                        css_style = 'color: red;'
                        for k,v in self.get_tag_attributes(dom,"host").items():
                            temp_li = ['',0,0,0,0]
                            temp_li[2] = v
                            if k == 'allow':
                                temp_li[3] = self.get_total_host()
                                temp_li[1] = 'Host '
                            else:
                                temp_li[3] = self.get_total_host(k)[1] 
                                temp_li[1] = device_names.get(k,k)
                            temp_li[4] = int(temp_li[2]) - int(temp_li[3])
                            if temp_li[4] < 0:
                                is_negative = 1
                                temp_li[0] = css_style
                            host[k] = temp_li
                        if is_negative:
                            if len(host.get('allow')) > 3:
                                host.get('allow')[0] = css_style                                                                
                        hostgroup_li = ['',0,0,0,0]
                        hostgroup_li[1] = 'Host Group'
                        hostgroup_li[2] = self.get_allowed_object(dom,"hostgroup")
                        hostgroup_li[3] = self.get_total_hostgroup()
                        hostgroup_li[4] = int(hostgroup_li[2]) - int(hostgroup_li[3])
                        if hostgroup_li[4] < 0:
                            hostgroup_li[0] = css_style
                            is_negative = 1 

                        user = {}
                        user_negative = 0
                        for k,v in self.get_tag_attributes(dom,"user").items():
                            temp_li = ['',0,0,0,0]
                            temp_li[2] = v
                            if k == 'allow':
                                temp_li[3] = self.get_total_user()
                                temp_li[1] = 'User '
                            else:
                                temp_li[3] = self.get_total_user(k)[1]
                                temp_li[1] = k
                            temp_li[4] = int(temp_li[2]) - int(temp_li[3])
                            if temp_li[4] < 0:
                                temp_li[0] = css_style
                                is_negative = 1
                                user_negative = 1
                            user[k] = temp_li                
                        if user_negative:
                            if len(user.get('allow')) > 3:
                                user.get('allow')[0] = css_style
                        usergroup_li = ['',0,0,0,0]
                        usergroup_li[1] = 'User Group'
                        usergroup_li[2] =self.get_allowed_object(dom,"usergroup")
                        usergroup_li[3] = self.get_total_usergroup()
                        usergroup_li[4] = int(usergroup_li[2]) - int(usergroup_li[3])
                        if usergroup_li[4] < 0:
                            usergroup_li[0] = css_style
                            is_negative = 1 

                        if is_negative:
                            return_dict = {}
                            return_dict['host'] = host
                            return_dict['hostgroup'] = {'allow' :hostgroup_li}
                            return_dict['user'] = user
                            return_dict['usergroup'] = {'allow' :usergroup_li}                         
                            #log.info(" ok 4 "+str(return_dict))
                            html_str = License.invalid_license(return_dict)
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
