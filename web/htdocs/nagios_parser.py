import shelve
import datetime
import os
import tarfile
# NMS Instance
nms_instance = __file__.split("/")[3]
# nms_instance = "nms"
# Nagios path & path of shelve files
nagios_path = "/omd/sites/%s/etc/nagios/conf.d/" % (nms_instance)
db_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/nag_db/" % (
    nms_instance)
# Path of .cfg files & tar files with log
file_folder_to_be_backed = "/omd/sites/%s/etc/nagios/conf.d/" % (nms_instance)
backup_store_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/nag_db/" % (
    nms_instance)
backup_log = "/omd/sites/%s/share/check_mk/web/htdocs/download/nag_db/backup_log.log" % (
    nms_instance)
# Extraction path of tar files
tarfile_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/nag_db/" % (
    nms_instance)
extract_here = "/omd/sites/%s/etc/nagios/conf.d/" % (nms_instance)

verify_configuration = False
filepath_dict = {
    "command_cfg": nagios_path + 'commands.cfg',
    "contact_cfg": nagios_path + 'contacts.cfg',
    "contactgroup_cfg": nagios_path + 'contactgroup.cfg',
    "host_cfg": nagios_path + 'hosts.cfg',
    "hosttemplate_cfg": nagios_path + 'host_template.cfg',
    "hostdependency_cfg": nagios_path + 'hostdependency.cfg',
    "hostdependencytemplate_cfg": nagios_path + 'hostdependency_template.cfg',
    "hostescalation_cfg": nagios_path + 'hostescalation.cfg',
    "hostextinfo_cfg": nagios_path + 'hostextinfo.cfg',
    "hostgroup_cfg": nagios_path + 'hostgroups.cfg',

    "service_cfg": nagios_path + 'services.cfg',
    "servicegroup_cfg": nagios_path + 'servicegroups.cfg',
    "serviceextinfo_cfg": nagios_path + 'serviceextinfo.cfg',
    "servicetemplate_cfg": nagios_path + 'service_template.cfg',
    "servicedependency_cfg": nagios_path + 'servicedependency.cfg',
    "servicedependencytemplate_cfg": nagios_path + 'servicedependency_template.cfg',
    "serviceescalation_cfg": nagios_path + 'serviceescalation.cfg',

    "template_cfg": nagios_path + 'templates.cfg',
    "timeperiod_cfg": nagios_path + 'timeperiod.cfg',
}

filename_dict_mapping = {
    'hostextinfo.cfg': 'hostextinfo',
    'servicegroups.cfg': 'servicegroup',
    'hostdependency.cfg': 'hostdependency',
    'service_template.cfg': 'servicetemplate',
    'services.cfg': 'service',
    'servicedependency_template.cfg': 'servicedependencytemplate',
    'serviceescalation.cfg': 'serviceescalation',
    'contactgroup.cfg': 'contactgroup',
    'hostgroups.cfg': 'hostgroup',
    'host_template.cfg': 'hosttemplate',
    'hostdependency_template.cfg': 'hostdependencytemplate',
    'hosts.cfg': 'host',
    'contacts.cfg': 'contact',
    'commands.cfg': 'command',
    'templates.cfg': 'template',
    'servicedependency.cfg': 'servicedependency',
    'serviceextinfo.cfg': 'serviceextinfo',
    'timeperiod.cfg': 'timeperiod',
    'hostescalation.cfg': 'hostescalation',
}
definitions = {
    "host": "host",
    "command": "command",
    "contact": "contact",
    "contactgroup": "contactgroup",
    "host": "host",
    "hosttemplate": "host",
    "hostdependency": "hostdependency",
    "hostdependencytemplate": "hostdependency",
    "hostescalation": "hostescalation",
    "hostextinfo": "hostextinfo",
    "hostgroup": "hostgroup",
    "servicegroup": "servicegroup",
    "service": "service",
    "serviceextinfo": "serviceextinfo",
    "servicetemplate": "service",
    "servicedependency": "servicedependency",
    "servicedependencytemplate": "servicedependency",
    "serviceescalation": "serviceescalation",
    "timeperiod": "timeperiod"
}
# filepath_dict={"host_cfg"
# :"/omd/sites/nms/etc/nagios/conf.d/check_mk_templates.cfg"
# }

dicts_name = [
    "command", "contact", "contactgroup", "host", "hosttemplate", "hostdependency",
    "hostescalation", "hostextinfo", "hostgroup", "servicegroup", "service",
    "serviceextinfo", "servicetemplate", "servicedependency", "serviceescalation", "timeperiod"]
command = {}

contact = {}
contactgroup = {}

host = {}
hosttemplate = {}
hostdependency = {}
hostdependencytemplate = {}
hostescalation = {}
hostextinfo = {}

hostgroup = {}
servicegroup = {}

service = {}
serviceextinfo = {}
servicetemplate = {}
servicedependency = {}
servicedependencytemplate = {}
serviceescalation = {}

timeperiod = {}
exception_cfg = ["timeperiod"]
count_maintain_list = ["service", "servicedependency", "hostdependency",
                       "hostescalation", "serviceescalation", "hostextinfo", "serviceextinfo"]
count_list = [1, 1, 1, 1, 1, 1, 1]

# Create the directory ad db_path


def create_directory():
    # check if directory exists
    """


    @return:
    """
    try:
        os.makedirs(db_path)
        return 0
    except OSError:
        return 0
    except Exception, e:
        return 1

# create the backup file of config files


def create_backup(comment="", flag_write_to_log_file=True):
    """

    @param comment:
    @param flag_write_to_log_file:
    @return:
    """
    try:
        if flag_write_to_log_file:
            file_name = str(datetime.datetime.now())[:22]
            dst = '%s.tar.bz2' % os.path.join(backup_store_path, file_name)
            out = tarfile.TarFile.open(dst, 'w:bz2')
            out.add(file_folder_to_be_backed,
                    arcname=os.path.basename(file_folder_to_be_backed))
            out.close()
            if os.path.isfile(backup_log):
                f_obj = open(backup_log, "a")
            else:
                f_obj = open(backup_log, "w")
            f_obj.write("%s :: %s\n" % (file_name, comment))
            f_obj.close()
        return {"success": 0, "data": "backup made successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# restore backup files of a given tar file name


def restore_backup(file_name):
    """

    @param file_name:
    @return:
    """
    global tarfile_path
    try:
        comment = "Backup before config restore at time : %s" % (
            str(datetime.datetime.now())[:22])
        res = create_backup(comment)
        res = remove_directory(nagios_path, extension=".cfg")
        tarfile_path2 = tarfile_path + "%s.tar.bz2" % (file_name)
        out = tarfile.TarFile.open(tarfile_path2, 'r:bz2')
        # cwd = os.getcwd()
        to_directory = extract_here
        os.chdir(to_directory)
        out.extractall(".")
        out.close()
        return {"success": 0, "data": "backup restored successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# get all file names within a given directory and extension


def get_file_names(directory_path=db_path, extension=".tar.bz2"):
    """

    @param directory_path:
    @param extension:
    @return:
    """
    try:
        li = []
        for the_file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, the_file)
            try:
                if os.path.isfile(file_path) and file_path.endswith(extension):
                    li.append(the_file)
            except Exception, e:
                # print e
                return {"success": 1, "data": str(e)}
        log_path = db_path + "backup_log.log"
        return {"success": 0, "file_list": li, "log_path": log_path}
    except Exception, e:
        # print str(e)
        return {"success": 1, "data": str(e)}

# store file modification time in the shelve file


def store_file_modification_time(file_name=""):
    """

    @param file_name:
    """
    try:
        file_stat = os.stat(file_name)
        file_old_stats = {}
        file_old_stats["st_mtime"] = file_stat.st_mtime
        file_old_stats["st_ctime"] = file_stat.st_ctime
        new_stat = shelve.open(db_path + "access_data_info.dict")
        if new_stat != {} and "data" in new_stat:
            stats = new_stat["data"]
            stats[file_name] = file_old_stats
            new_stat["data"] = stats
        else:
            stats = {}
            stats[file_name] = file_old_stats
            new_stat["data"] = stats
        new_stat.close()
    except Exception, e:
        print str(e)

# check files if they are modified


def check_files_if_modified(file_name=""):
    # if file_name=="":
    """

    @param file_name:
    @return:
    """
    if not file_name.startswith("//"):
        file_name = nagios_path + file_name
    try:
        file_stat = os.stat(file_name)
        old_stat = shelve.open(db_path + "access_data_info.dict")
        if old_stat != {} and "data" in old_stat:
            stats = old_stat["data"]
            if stats != {} and file_name in stats:
                file_old_stats = stats[file_name]
                if file_stat.st_mtime == file_old_stats["st_mtime"]:
                    return {"success": 0, "data": "file not modified"}
                else:
                    return {"success": 1, "data": "files modified"}
            else:
                return {"success": 1, "data": "file not exists in info"}
        else:
            return {"success": 1, "data": "file not exists in info"}

        return {"success": 1, "data": "files modified"}
    except Exception, e:
        return {"success": 1, "data": str(file_name)}

# remove files from a directory of given extension


def remove_directory(directory_path, extension=".cfg"):
    """

    @param directory_path:
    @param extension:
    @return:
    """
    try:
        for the_file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, the_file)
            try:
                if os.path.isfile(file_path) and file_path.endswith(extension):
                    os.unlink(file_path)
            except Exception, e:
                # print e
                return {"success": 1, "data": str(e)}
        return {"success": 0, "data": "Deleted successfully"}
    except Exception, e:
        # print str(e)
        return {"success": 1, "data": str(e)}

# remove a file in a directory


def remove_directory_file(directory_path, filename=""):
    """

    @param directory_path:
    @param filename:
    @return:
    """
    try:
        for the_file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, the_file)
            try:
                if os.path.isfile(file_path) and the_file == filename:
                    os.unlink(file_path)
            except Exception, e:
                # print e
                return {"success": 1, "data": str(e)}
        return {"success": 0, "data": "Deleted successfully"}
    except Exception, e:
        # print str(e)
        return {"success": 1, "data": str(e)}

# validate if a template if correct by comparing it with source template


def check_valid_template(source_dict, check_dict, dict_name):
    # check validity of template
    # from the source template
    """

    @param source_dict:
    @param check_dict:
    @param dict_name:
    @return:
    """
    try:
        for key in source_dict:
            if source_dict[key] == "r":  # required value
                if key not in check_dict:  # its not present in check_dict
                    return key + " value not present in input file %s" % (dict_name)
        for key in check_dict:        # check validity of keys in check_dict
            if key not in source_dict:  # its not present in source_dict
                return key + " value not present in source template %s" % (dict_name)
        return 0
    except Exception, e:
        return str(e)

# load configuration files to memory ie RAM


def load_configuration_to_memory(list_files=[]):
    """

    @param list_files:
    @return: @raise:
    """
    global count_list
    # load all .cfg files in memory which are present in nagios directory ie conf.d
    # load in memory the source dict
    definition_name = ""
    value_index = ""
    time1 = datetime.datetime.now()
    execfile(db_path + 'complete_template.dict', globals(), globals())
    try:
        if list_files == []:
            for r, d, f in os.walk(nagios_path):
                for files in f:
                    if files.endswith(".cfg"):
                        # list_files.append(os.path.join(r,files))
                        list_files.append(files)
        for file_name in range(len(list_files)):
            definition_name = ""
            store_file_modification_time(nagios_path + list_files[file_name])
            f_obj = open(nagios_path + list_files[file_name], 'r')
            li_read = f_obj.readlines()
            f_obj.close()
            li = []
            temp_str = ""
            for line in li_read:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                line = line.split('#')[0].strip()
                #                li.append(line)
                flag = 1
                if line.endswith('\\'):
                    temp_str += line[:-1]
                    flag = 0
                else:
                    if temp_str == "":
                        temp_str = line
                    else:
                        temp_str += line
                if flag:
                    li.append(temp_str)
                    temp_str = ""
            i = 0
            dict_name = ""
            while (i < len(li)):
                j = i + 1
                li[i] = li[i].strip()
                if li[i].startswith('define'):        # li[i] = define host{
                    dict_name = li[i].split()[1]
                    # get the name of definition
                    dict_name = dict_name.replace(
                        '{', '')  # replace any { if present
                    di_data = {}
                    # initialize data dict
                    while (j < len(li) and li[j].find('}') == -1):  # run till we reach end of file or find }
                        if li[j].strip() == "{":
                            j = j + 1
                            continue
                        data = li[j].split()
                        di_data[data[0]
                        ] = ' '.join(data[1:])  # make the key value pair
                        j = j + 1
                    if j == len(li):
                        raise Exception(
                            "Invalid configuration file.. invalid open & closing braces")
                i = j + 1
                if "name" in di_data:         # its a template definition for host or service
                    definition_name = "name"
                    dict_name = dict_name + "template"
                else:
                    definition_name = dict_name
                    # if definition_name=="service":
                    #    definition_name = definition_name + "_description"
                    if definition_name in count_maintain_list:
                    #                        if definition_name=="service":
                    #                            definition_name_service=di_data.get("service_description","")+di_data.get("host_name","")
                    #                        else:
                        index_count = count_maintain_list.index(
                            definition_name)
                        value_index = definition_name + \
                                      str(count_list[index_count])
                        count_list[index_count] += 1
                        # index_count=count_maintain_list.index(definition_name)
                        # definition_name = definition_name + str(count_list[index_count])
                        # value_index=definition_name + str(count_list[index_count])
                        # count_list[index_count]+=1
                    else:
                        definition_name = definition_name + "_name"
                check_valid_config_file = 0
                if dict_name not in exception_cfg and verify_configuration:
                    check_valid_config_file = check_valid_template(
                        eval(dict_name + "_dict"), di_data, dict_name)
                if check_valid_config_file == 0:
                    if definition_name in count_maintain_list:
                    #                        if definition_name=="service":
                    #                            eval(dict_name)[definition_name_service]=di_data
                    #                        else:
                        eval(dict_name)[value_index] = di_data
                        # eval(dict_name)[value_index]=di_data
                    else:
                        eval(dict_name)[di_data[definition_name]] = di_data
                else:
                    raise Exception(check_valid_config_file)
        time_var = datetime.datetime.now() - time1
        stats = str(
            time_var.seconds) + "." + str(time_var.microseconds) + " seconds"
        count_list = [1, 1, 1, 1, 1, 1, 1]
        return {"success": 0, "data": "files loaded successfully", "stats": stats}
    except Exception, e:
        return {"success": 1, "data": str(e)}


# load configuration into memory and shelve files
def load_configuration(list_files=[]):
    # write shelve files from the dict object present in memory
    """

    @param list_files:
    @return:
    """
    try:
        time1 = datetime.datetime.now()
        result = load_configuration_to_memory(list_files)
        if result['success'] == 0:
            remove_result = remove_directory(db_path, ".db")
            if remove_result["success"] == 0:
                pass
            else:
                return {"success": 1, "data": "Files couldn't be deleted %s"(remove_result["data"])}
            for dict_var in dicts_name:
                # print dict_var,eval(dict_var)
                db_dict = shelve.open(db_path + "%s.db" % (dict_var))
                db_dict["data"] = eval(dict_var)
                db_dict.close()
                # di = eval(dict_var)
                # di.clear()
            time_var = datetime.datetime.now() - time1
            stats = str(
                time_var.seconds) + "." + str(time_var.microseconds) + " seconds"
            return {"success": 0, "data": "Files written successfully", "stats": stats}
        else:
            # print result['data']
            return {"success": 1, "data": result['data']}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# function to forecefully write a file ie open it in 'w' mode


def nagios_force_sync_parser(shelve_name='hostgroup', file_name='hostgroups.cfg', updated_dict={},
                             attribute="hostgroup"):
    # write shelve files from the dict object present in memory
    """

    @param shelve_name:
    @param file_name:
    @param updated_dict:
    @param attribute:
    @return:
    """
    try:
        db_dict = shelve.open(db_path + "%s.db" % (shelve_name))
        db_dict["data"] = updated_dict
        db_dict.close()
        cfg_file = open(nagios_path + file_name, "w")
        write_li = []
        for data in updated_dict:
            write_li.append("define %s{\n" % (definitions[attribute]))
            for key in updated_dict[data]:
                if updated_dict[data][key] != "":
                    write_li.append(
                        "\t %s \t %s\n" % (key, updated_dict[data][key]))
            write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        store_file_modification_time(filepath_dict["%s_cfg" % (attribute)])
        return {"success": 0, "result": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "result": str(e)}

# load shelve files to memory


def load_db():
    # load shelve files to memory objects ie dicts in memory
    """


    @return:
    """
    try:
        time1 = datetime.datetime.now()
        for dict_var in dicts_name:
            db_dict = shelve.open(db_path + "%s.db" % (dict_var))
            di = eval(dict_var)
            di.clear()
            di.update(db_dict["data"])
            db_dict.close()
        time_var = datetime.datetime.now() - time1
        stats = str(
            time_var.seconds) + "." + str(time_var.microseconds) + " seconds"
        return {"success": 0, "data": "Files loaded successfully", "stats": stats}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# load given shelve file into memory


def load_db_by_name(dict_name, is_cfg=0):
    # get a specific .cfg file definition from shelve... no need of parsing
    # the .cfg files as we already have them in shelve
    """

    @param dict_name:
    @param is_cfg:
    @return:
    """
    try:
        if is_cfg:
            dict_name = filename_dict_mapping[dict_name]
        db_dict = shelve.open(db_path + "%s.db" % (dict_name))
        di = eval(dict_name)
        di.clear()
        di.update(db_dict["data"])
        db_dict.close()
        # if di=={}:
        # pass
        # load_configuration([])
        return {"success": 0, "data": di}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# save shelve file


def set_db_by_name(dict_name):
    # write  a specific shelve file with fetching data from memory.
    """

    @param dict_name:
    @return:
    """
    try:
        db_dict = shelve.open(db_path + "%s.db" % (dict_name))
        db_dict["data"] = eval(dict_name)
        db_dict.close()
        return {"success": 0, "data": "File modified successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# get properties for a host name from shelve


def get_host_by_name(host_name):
    """

    @param host_name:
    @return:
    """
    try:
        dict_name = "host"
        di = load_db_by_name(dict_name)
        if di["success"] == 0:
            if host_name in di["data"]:
                return {"success": 0, "data": di["data"][host_name]}
            else:
                return {"success": 1, "data": "Host not found."}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# get service name properties from shelve


def get_service_by_name(service_name):
    """

    @param service_name:
    @return:
    """
    try:
        dict_name = "service"
        di = load_db_by_name(dict_name)
        if di["success"] == 0:
            if service_name in di["data"]:
                return {"success": 0, "data": di["data"][service_name]}
            else:
                return {"success": 1, "data": "Service not found."}
    except Exception, e:
        return {"success": 1, "data": str(e)}


# get properties of a hostgroup from shelve
def get_hostgroup_by_name(hostgroup_name):
    """

    @param hostgroup_name:
    @return:
    """
    try:
        dict_name = "hostgroup"
        di = load_db_by_name(dict_name)
        if di["success"] == 0:
            if hostgroup_name in di["data"]:
                return {"success": 0, "data": di["data"][hostgroup_name]}
            else:
                return {"success": 1, "data": "Hostgroup not found."}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# get properties of any attribute from shelve
# like fetching 'localhost' details from host shelve file


def get_attribute_by_name(attribute_name, attribute):
    """

    @param attribute_name:
    @param attribute:
    @return:
    """
    try:
        di = load_db_by_name(attribute)
        if di["success"] == 0:
            if attribute_name in di["data"]:
                return {"success": 0, "data": di["data"][attribute_name]}
            else:
                return {"success": 1, "data": "%s %s not found." % (attribute_name, attribute)}
    except Exception, e:
        return {"success": 1, "data": str(e)}


# write config file & shelve file after any modification in memory
def set_attribute_by_name(attribute_data, attribute, unique_name):
    """

    @param attribute_data:
    @param attribute:
    @param unique_name:
    @return:
    """
    try:
        db_dict = shelve.open(db_path + "%s.db" % (attribute))
        di = db_dict["data"]
        di[unique_name].update(attribute_data)
        db_dict["data"] = di
        db_dict.close()
        result_write = write_db_from_memory(attribute)
        if result_write["success"] == 0:
            return {"success": 0, "data": "%s modified successfully" % (unique_name)}
        else:
            return {"success": 1, "data": result_write["data"]}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# write shelve file after any modification in memory with extra data


def set_attribute_by_name_to_shelve(attribute_data, attribute, unique_name, extra_data={}):
    """

    @param attribute_data:
    @param attribute:
    @param unique_name:
    @param extra_data:
    @return:
    """
    try:
        db_dict = shelve.open(db_path + "%s.db" % (attribute))
        di = db_dict["data"]
        if unique_name in di:
            di[unique_name].update(attribute_data)
        else:
            di[unique_name] = {}
            di[unique_name].update(attribute_data)
            di[unique_name].update(extra_data)
        db_dict["data"] = di
        db_dict.close()
        return {"success": 0, "data": "%s modified successfully" % (unique_name)}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# write shelve file after any modification in memory


def complete_write_attribute_by_name_to_shelve(attribute_data, attribute, unique_name):
    """

    @param attribute_data:
    @param attribute:
    @param unique_name:
    @return:
    """
    try:
        db_dict = shelve.open(db_path + "%s.db" % (attribute))
        di = db_dict["data"]
        di[unique_name] = {}
        di[unique_name].update(attribute_data)
        db_dict["data"] = di
        db_dict.close()
        return {"success": 0, "data": "%s modified successfully" % (unique_name)}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# delete attribute from shelve file


def delete_attribute_by_name_from_shelve(attribute, unique_name):
    # write shelve file after any modification in memory
    """

    @param attribute:
    @param unique_name:
    @return:
    """
    try:
        db_dict = shelve.open(db_path + "%s.db" % (attribute))
        di = db_dict["data"]
        di_eval = eval(attribute)
        if unique_name in di:
            di.pop(unique_name)
        if unique_name in di_eval:
            di_eval.pop(unique_name)
        db_dict["data"] = di
        db_dict.close()
        return {"success": 0, "data": "%s deleted successfully" % (unique_name)}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# write nagios config files(.cfg) from memory of a given attribute like
# 'host','service'


def write_config_from_memory(attribute):
    # write objects to .cfg files from memory after modification to any
    # attributes
    """

    @param attribute:
    @return:
    """
    try:
        cfg_file = open(filepath_dict["%s_cfg" % (attribute)])
        attribute_dict = eval(attribute)
        write_li = []
        for data in attribute_dict:
            write_li.append("define %s{" % (attribute))
            for key in attribute_dict[data]:
                write_li.append(
                    "\t%s \t %s{" % (key, attribute_dict[data][key]))
            write_li.append("}")
        cfg_file.close()
        store_file_modification_time(filepath_dict["%s_cfg" % (attribute)])
        return {"success": 0, "data": "%s config file modified successfully" % (attribute)}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# write nagios config files(.cfg) by loading from shelve file of a given
# attribute like 'host','service'


def write_db_from_memory(attribute):
    # write objects to shelve file from memory
    """

    @param attribute:
    @return:
    """
    try:
        cfg_file = open(filepath_dict["%s_cfg" % (attribute)], "w")
        attribute_dict = shelve.open(db_path + "%s.db" % (attribute))["data"]
        # print attribute_dict
        write_li = []
        for data in attribute_dict:
            write_li.append("define %s{\n" % (attribute))
            for key in attribute_dict[data]:
                write_li.append(
                    "\t%s \t %s\n" % (key, attribute_dict[data][key]))
            write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        return {"success": 0, "data": "%s config file modified successfully" % (attribute)}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# write all configuration files from shelve file


def write_configuration(comment="nagios backup"):
    # write .cfg files from shelve files ..not from current memory
    """

    @param comment:
    @return:
    """
    backup_result = create_backup(comment)
    if backup_result["success"] == 0:
        remove_result = remove_directory(nagios_path, ".cfg")
        if remove_result["success"] == 0:
            pass
        else:
            return {"success": 1, "data": "Files couldn't be deleted %s"(remove_result["data"])}
    else:
        return {"success": 1, "data": " Backup couldn't be created %s"(backup_result["data"])}

    try:
        for attribute in dicts_name:
            attribute_dict = shelve.open(
                db_path + "%s.db" % (attribute))["data"]
            # print attribute
            # print attribute_dict
            if attribute_dict == {}:
                continue
            cfg_file = open(filepath_dict["%s_cfg" % (attribute)], "w")
            write_li = []
            for data in attribute_dict:
                write_li.append("define %s{\n" % (definitions[attribute]))
                for key in attribute_dict[data]:
                    write_li.append(
                        "\t %s \t %s\n" % (key, attribute_dict[data][key]))
                write_li.append("}\n\n")
            cfg_file.writelines(write_li)
            cfg_file.close()
            store_file_modification_time(filepath_dict["%s_cfg" % (attribute)])
        return {"success": 0, "data": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# write nagios config files(.cfg) from memory of a given filename


def write_configuration_file(file_name, comment="nagios backup", flag_write_to_log_file=True):
    # write .cfg files from shelve files ..not from current memory
    """

    @param file_name:
    @param comment:
    @param flag_write_to_log_file:
    @return:
    """
    backup_result = create_backup(comment, flag_write_to_log_file)
    if backup_result["success"] == 0:
        remove_result = remove_directory_file(nagios_path, file_name)
        if remove_result["success"] == 0:
            pass
        else:
            return {"success": 1, "data": "File couldn't be deleted %s"(remove_result["data"])}
    else:
        return {"success": 1, "data": " Backup couldn't be created %s"(backup_result["data"])}

    try:
        attribute = filename_dict_mapping[file_name]
        attribute_dict = shelve.open(db_path + "%s.db" % (attribute))["data"]
        if attribute_dict == {}:
            cfg_file = open(nagios_path + file_name, "w")
            cfg_file.close()
            return {"success": 0, "data": "empty dict"}
        cfg_file = open(nagios_path + file_name, "w")
        write_li = []
        for data in attribute_dict:
            write_li.append("define %s{\n" % (definitions[attribute]))
            for key in attribute_dict[data]:
                if attribute_dict[data][key] != "":
                    write_li.append(
                        "\t %s \t %s\n" % (key, attribute_dict[data][key]))
            write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        store_file_modification_time(filepath_dict["%s_cfg" % (attribute)])
        return {"success": 0, "data": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# check if files are modified and return them for a given file


def load_return_attribute(file_name):
    """

    @param file_name:
    @return:
    """
    modified_result = check_files_if_modified(
        file_name)  # file_name = file_name,is_cfg=1
    flag_modified = 0
    flag_load = 0
    # modified_result["success"] ==0 means that files are not modified
    if modified_result["success"] == 1:
        flag_modified = 1
    if flag_modified == 0:
        write_result = load_db_by_name(file_name, 1)
        if write_result["success"] == 1:
            flag_load = 1
    if flag_modified or flag_load:
        write_result = load_configuration([file_name])
    if write_result["success"] == 0:
        if eval(filename_dict_mapping[file_name]) == {}:
            load_configuration([file_name])

        return {"data": eval(filename_dict_mapping[file_name]), "success": 0}
    else:
        return {"data": write_result["data"], "success": 1}


# load nagios configuration for given dict_names and list of files
def load_nagios_config_inventory(dict_names=[], list_files=[]):
    """

    @param dict_names:
    @param list_files:
    @return: @raise:
    """
    global count_list
    # load all .cfg files in memory which are present in nagios directory ie conf.d
    # load in memory the source dict
    definition_name = ""
    value_index = ""
    time1 = datetime.datetime.now()
    try:
        for file_name in range(len(list_files)):
            # eval(dict_names[file_name]).clear()
            definition_name = ""
            # store_file_modification_time(nagios_path+list_files[file_name])
            f_obj = open(nagios_path + list_files[file_name], 'r')
            li_read = f_obj.readlines()
            f_obj.close()
            li = []
            temp_str = ""
            for line in li_read:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                line = line.split('#')[0].strip()
                #                li.append(line)
                flag = 1
                if line.endswith('\\'):
                    temp_str += line[:-1]
                    flag = 0
                else:
                    if temp_str == "":
                        temp_str = line
                    else:
                        temp_str += line
                if flag:
                    li.append(temp_str)
                    temp_str = ""
            i = 0
            dict_name = ""
            while (i < len(li)):
                j = i + 1
                li[i] = li[i].strip()
                if li[i].startswith('define'):        # li[i] = define host{
                    dict_name = li[i].split()[1]
                    # get the name of definition
                    dict_name = dict_name.replace(
                        '{', '')  # replace any { if present
                    di_data = {}
                    # initialize data dict
                    while (j < len(li) and li[j].find('}') == -1):  # run till we reach end of file or find }
                        if li[j].strip() == "{":
                            j = j + 1
                            continue
                        data = li[j].split()
                        di_data[data[0]
                        ] = ' '.join(data[1:])  # make the key value pair
                        j = j + 1
                    if j == len(li):
                        raise Exception(
                            "Invalid configuration file.. invalid open & closing braces")
                i = j + 1
                if "name" in di_data:         # its a template definition for host or service
                    definition_name = "name"
                    # dict_name = dict_names[file_name]
                else:
                    definition_name = dict_name
                    # if definition_name=="service":
                    #    definition_name = definition_name + "_description"
                    if definition_name == "service":
                        definition_name_service = di_data[
                                                      "service_description"] + di_data["host_name"]
                    else:
                        definition_name = definition_name + "_name"
                dict_name = dict_names[file_name]
                if definition_name == "service":
                    eval(dict_name)[definition_name_service] = di_data
                else:
                    eval(dict_name)[di_data[definition_name]] = di_data
        time_var = datetime.datetime.now() - time1
        stats = str(
            time_var.seconds) + "." + str(time_var.microseconds) + " seconds"
        count_list = [1, 1, 1, 1, 1, 1, 1]
        return {"success": 0, "data": "files loaded successfully", "stats": stats}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# add new object at end of configuration file
# this is called after addition of new object through inventory


def append_for_inventory_new_object(file_name, dict_name="host", attribute="host", new_host_dict={},
                                    comment="nagios backup"):
    # write .cfg files from shelve files ..not from current memory
    """

    @param file_name:
    @param dict_name:
    @param attribute:
    @param new_host_dict:
    @param comment:
    @return:
    """
    backup_result = create_backup(comment, False)
    if backup_result["success"] == 0:
        pass
    else:
        return {"success": 1, "data": " Backup couldn't be created %s"(backup_result["data"])}

    try:
        cfg_file = open(nagios_path + file_name, "a")
        write_li = []
        write_li.append("\ndefine %s{\n" % (attribute))
        for key in new_host_dict:
            write_li.append("\t%s \t %s\n" % (key, new_host_dict[key]))
        write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        # store_file_modification_time(filepath_dict["%s_cfg"%(attribute)])
        return {"success": 0, "result": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "result": str(e)}

# edit object of config files... this is called after editing of object through inventory
# we need to have unique name fow which we will edit


def edit_for_inventory_object(
        unique_name="localhost", file_name="hosts.cfg", attribute="host", dict_name="host", new_host_dict={},
        comment="nagios backup"):
    # write .cfg files from shelve files ..not from current memory
    """

    @param unique_name:
    @param file_name:
    @param attribute:
    @param dict_name:
    @param new_host_dict:
    @param comment:
    @return:
    """
    backup_result = create_backup(comment, False)
    if backup_result["success"] == 0:
        load_result = load_nagios_config_inventory([dict_name], [file_name])
        if load_result["success"] == 0:
            pass
        else:
            return load_result
    else:
        return {"success": 1, "data": " Backup couldn't be created %s"(backup_result["data"])}

    try:
        di = eval(dict_name)
        if unique_name in di:
            di[unique_name].update(new_host_dict)
        else:
            di[unique_name] = new_host_dict
        cfg_file = open(nagios_path + file_name, "w")
        write_li = []
        for data in di:
            if di[data] != {}:
                write_li.append("define %s{\n" % (attribute))
                for key in di[data]:
                    write_li.append("\t%s \t %s\n" % (key, di[data][key]))
            write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        # store_file_modification_time(filepath_dict["%s_cfg"%(attribute)])
        return {"success": 0, "data": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}


# edit object of config files... this is called after editing of object through inventory
# we don't have unique name here
def edit_for_inventory_object_without_unique(
        other_dict={}, file_name="hosts.cfg", attribute="host", dict_name="host",
        old_name='', new_name='', comment="nagios backup"):
    # write .cfg files from shelve files ..not from current memory
    """

    @param other_dict:
    @param file_name:
    @param attribute:
    @param dict_name:
    @param old_name:
    @param new_name:
    @param comment:
    @return:
    """
    backup_result = create_backup(comment, False)
    if backup_result["success"] == 0:
        load_result = load_nagios_config_inventory([dict_name], [file_name])
        if load_result["success"] == 0:
            pass
        else:
            return load_result
    else:
        return {"success": 1, "data": " Backup couldn't be created %s"(backup_result["data"])}

    try:
        di = eval(dict_name)
        for key in di:
            for i in other_dict.keys():
                if i in di[key]:
                    li_di_key_i = di[key][i].split(',')
                    if old_name in li_di_key_i:
                        li_di_key_i[li_di_key_i.index(old_name)] = new_name
                        di[key][i] = ','.join(li_di_key_i)

        cfg_file = open(nagios_path + file_name, "w")
        write_li = []
        for data in di:
            if di[data] != {}:
                write_li.append("define %s{\n" % (attribute))
                for key in di[data]:
                    write_li.append("\t%s \t %s\n" % (key, di[data][key]))
            write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        # store_file_modification_time(filepath_dict["%s_cfg"%(attribute)])
        return {"success": 0, "data": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}


# delete inventory object when we have unique name
def delete_for_inventory_object(unique_name="host3", file_name="hosts.cfg", attribute="host", dict_name="host",
                                replace_dict={}, comment="nagios backup", take_backup=1):
    # write .cfg files from shelve files ..not from current memory
    """

    @param unique_name:
    @param file_name:
    @param attribute:
    @param dict_name:
    @param replace_dict:
    @param comment:
    @param take_backup:
    @return:
    """
    if take_backup:
        backup_result = create_backup(comment, False)
        if backup_result["success"] == 0:
            pass
        else:
            return {"success": 1, "data": " Backup couldn't be created %s"(backup_result["data"])}

    load_result = load_nagios_config_inventory([dict_name], [file_name])
    if load_result["success"] == 0:
        pass
    else:
        return load_result
    try:
        di = eval(dict_name)
        if unique_name in di:
            u_data = di.pop(unique_name)
        cfg_file = open(nagios_path + file_name, "w")
        write_li = []
        for data in di:
            if di[data] != {}:
                write_li.append("define %s{\n" % (attribute))
                for key in di[data]:
                    if key in replace_dict:
                        write_li.append(
                            "\t%s \t %s\n" % (key, replace_dict[key]))
                    else:
                        write_li.append("\t%s \t %s\n" % (key, di[data][key]))
            write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        # store_file_modification_time(filepath_dict["%s_cfg"%(attribute)])
        return {"success": 0, "data": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}

# delete inventory object and modify the hosts file...


def delete_for_inventory_object_modify_hosts(old_dict_template, file_name="hosts.cfg", attribute="host",
                                             dict_name="host", replace_dict={}, comment="nagios backup", take_backup=1):
    # write .cfg files from shelve files ..not from current memory
    """

    @param old_dict_template:
    @param file_name:
    @param attribute:
    @param dict_name:
    @param replace_dict:
    @param comment:
    @param take_backup:
    @return:
    """
    if take_backup:
        backup_result = create_backup(comment, False)
        if backup_result["success"] == 0:
            pass
        else:
            return {"success": 1, "data": " Backup couldn't be created %s"(backup_result["data"])}

    load_result = load_nagios_config_inventory([dict_name], [file_name])
    if load_result["success"] == 0:
        pass
    else:
        return load_result
    try:
        di = eval(dict_name)
        cfg_file = open(nagios_path + file_name, "w")
        write_li = []
        for data in di:
            if di[data] != {}:
                write_li.append("define %s{\n" % (attribute))
                for key in di[data]:
                    if key in replace_dict:
                        temp_vals = di[data][key].split(',')
                        if old_dict_template[key] in temp_vals:
                            temp_vals.remove(old_dict_template[key])
                            temp_vals.insert(0, replace_dict[key])
                            di[data][key] = ','.join(temp_vals)

                        write_li.append("\t%s \t %s\n" % (key, di[data][key]))
                    else:
                        write_li.append("\t%s \t %s\n" % (key, di[data][key]))
            write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        # store_file_modification_time(filepath_dict["%s_cfg"%(attribute)])
        return {"success": 0, "result": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "result": str(e)}

# delete inventory files when we don't have unique name


def delete_for_inventory_object_without_unique_name(unique_attribute="host_name", unique_name="host3",
                                                    file_name="hosts.cfg", attribute="host", dict_name="host",
                                                    replace_dict={}, comment="nagios backup"):
    # write .cfg files from shelve files ..not from current memory
    """

    @param unique_attribute:
    @param unique_name:
    @param file_name:
    @param attribute:
    @param dict_name:
    @param replace_dict:
    @param comment:
    @return:
    """
    backup_result = create_backup(comment, False)
    if backup_result["success"] == 0:
        load_result = load_nagios_config_inventory([dict_name], [file_name])
        if load_result["success"] == 0:
            pass
        else:
            return load_result
    else:
        return {"success": 1, "data": " Backup couldn't be created %s"(backup_result["data"])}

    try:
        di = eval(dict_name)
        key_li = []
        for key in di.keys():
            di_data = di[key]
            if unique_attribute in di_data:
                li_data = [i.strip() for i in di_data[
                    unique_attribute].split(',')]
                if li_data.count(unique_name) != 0:
                    li_data.remove(unique_name)
                    di_data[unique_attribute] = ','.join(li_data)
            if di_data[unique_attribute] == "":
                di.pop(key)
            else:
                di[key] = di_data
            #        if di.has_key(unique_name):
            #            u_data=di.pop(unique_name)
        cfg_file = open(nagios_path + file_name, "w")
        write_li = []
        for data in di:
            if di[data] != {}:
                write_li.append("define %s{\n" % (attribute))
                for key in di[data]:
                    if key in replace_dict:
                        write_li.append(
                            "\t%s \t %s\n" % (key, replace_dict[key]))
                    else:
                        write_li.append("\t%s \t %s\n" % (key, di[data][key]))
            write_li.append("}\n\n")
        cfg_file.writelines(write_li)
        cfg_file.close()
        # store_file_modification_time(filepath_dict["%s_cfg"%(attribute)])
        return {"success": 0, "data": " config files modified successfully"}
    except Exception, e:
        return {"success": 1, "data": str(e)}


#
# print check_files_if_modified("/omd/sites/nms/etc/nagios/conf.d/hosts.cfg")
################ Loading from .cfg files ###################
## tutorial 1 : Fetch all objects from .cfg files to memory (imp)
# load=0
# if load==1:
#    load_result = load_configuration_to_memory()
#    if load_result["success"]==0:
#        print load_result["data"], load_result["stats"]
#        print "checking"
#        print hosttemplate
#    else:
#        print load_result["data"]
#
#
## tutorial 2 : Fetch all objects from .cfg files to memory and also Write shelve files from the .cfg files (imp)
# write = 0
# if write==1:
#    write_result = load_configuration()
#    if write_result["success"]==0:
#        print write_result["data"],write_result["stats"]
#    else:
#        print write_result["data"]
## tutorial 3 : Load any specific .cfg file to memory and write shelve file
# write = 0
# list_files=['hosts.cfg','commands.cfg']
# if write==1:
#    write_result = load_configuration(list_files)
#    if write_result["success"]==0:
#        print write_result["data"]
#    else:
#        print write_result["data"]

# tutorial 3 : Load any specific .cfg file to memory and write shelve file and return it
######################################### Modifying shelve files
#
#
## tutorial 4 : load all shelve files to memory
# print create_backup()
# load = 0
# if load==1:
#    load_result = load_db()
#    if load_result["success"]==0:
#        print load_result["data"]
#    else:
#        print load_result["data"]
#
## tutorial 5 :   load a shelve file into memory
# load = 0
# dict_name = "hosttemplate"
# if load==1:
#    load_result = load_db_by_name(dict_name)
#    if load_result["success"]==0:
#        print load_result["data"]
#    else:
#        print load_result["data"]
#
#
## tutorial 6 :   write a shelve file from memory
# write = 0
# dict_name = "host"
# if write==1:
#    write_result = set_db_by_name(dict_name)
#    if write_result["success"]==0:
#        print write_result["data"]
#    else:
#        print write_result["data"]
#
## tutorial 7 :   get an attribute value from shelve file
# load = 0
# attribute = "host"
# attribute_name = "localhost"
# if load==1:
#    load_result = get_attribute_by_name(attribute_name, attribute)
#    if load_result["success"]==0:
#        print load_result["data"]
#    else:
#        print load_result["data"]
#
## tutorial 8 :   set an attribute value from memory to shelve file
# load = 0
# attribute = "host"
# attribute_data = {'use': 'generic-host', 'check_command': 'check-host-alive',
#                  'hostgroups': 'Default', 'alias': 'UNMP Server System', 'host_name': 'localhost', 'address': 'localhost'}
# unique_name = "localhost"
# if load==1:
#    load_result = set_attribute_by_name(attribute_data, attribute , unique_name)
#    if load_result["success"]==0:
#        print load_result["data"]
#    else:
#        print load_result["data"]
#
## tutorial 9 :   write objects from memory to .cfg files
# write = 0
# attribute = "host"
# if write==1:
#    write_result = write_config_from_memory(attribute)
#    if write_result["success"]==0:
#        print write_result["data"]
#    else:
#        print write_result["data"]
#
## tutorial 10 :   write objects from memory to shelve file
# write = 0
# attribute = "host"
# if write==1:
#    write_result = write_db_from_memory(attribute)
#    if write_result["success"]==0:
#        print write_result["data"]
#    else:
#        print write_result["data"]
#
## tutorial 11 :   write .cfg config files from shelve (imp)
# write = 0
# if write==1:
#    write_result = write_configuration()
#    if write_result["success"]==0:
#        print write_result["data"]
#    else:
#        print write_result["data"]
#
# write = 0 #["timeperiods.cfg"]
# if write==1:
#    write_result = load_configuration()
#    if write_result["success"]==0:
#        print write_result["data"],write_result["stats"]
#    else:
#        print write_result["data"]


# print restore_backup("2012-07-16 18:49:07")

#
# load_for_inventory=0
# if load_for_inventory:
#    host={}
#    dict_names=["host","service"]
#    list_files=["hosts.cfg","services.cfg"]
#    print load_nagios_config_inventory(dict_names,list_files)
#    #print host
#    #print service
#
# append_new_host=0
# if append_new_host:
#    file_name="hosts.cfg"
#    dict_name="host"
#    attribute="host"
#    new_host_dict={"host_name":"mahipal","alias":"mahipal","address":"172.22.0.140","notification_options":"d,u,r,f,s","use":"generic-host"}
#    comment = "nagios backup before new host"
#    result=append_for_inventory_new_object(file_name,dict_name,attribute,new_host_dict,comment)
#    print result
#
# append_new_host=0
# if append_new_host:
#    file_name="hosts.cfg"
#    dict_name="host"
#    attribute="host"
#
#    new_host_dict={"host_name":"mahipal","alias":"mahipal","address":"172.22.0.140","notification_options":"d,u,r,f,s","use":"generic-host"}
#    comment = "nagios backup before new host"
#    result=append_for_inventory_new_object(file_name,dict_name,attribute,new_host_dict,comment)
#    print result
#
#
# append_new_service=0
# if append_new_service:
#    file_name="services.cfg"
#    dict_name="service"
#    attribute="service"
#    comment = "nagios backup before new service"
#    new_host_dict={"use":"generic-service","retry_check_interval":"1","check_command": "snmp_uptime!161",
#"host_name":      "host8","normal_check_interval":      "1","service_description":      "SNMP UPTIME2","max_check_attempts":      "2"}
#    result=append_for_inventory_new_object(file_name,dict_name,attribute,new_host_dict,comment)
#    print result
#
# edit_old_host=0
# if edit_old_host:
#    file_name="hosts.cfg"
#    dict_name="host"
#    attribute="host"
#    unique_name="mahipal"
#    comment="nagios backup before editing host"
#    new_host_dict={"host_name":"mahipal","alias":"mahipal","address":"172.22.0.150","notification_options":"d,u,r,f,s","use":"generic-host"}
#    result = edit_for_inventory_object(unique_name, file_name, attribute, dict_name, new_host_dict, comment)
#    print result
#
# delete_old_host=0
# if delete_old_host:
#    file_name="hosts.cfg"
#    dict_name="host"
#    attribute="host"
#    unique_name="mahipal"
#    comment="nagios backup before deleting host"
#    replace_dict={"parents":"localhost"}
#    result = delete_for_inventory_object(unique_name, file_name, attribute, dict_name,replace_dict, comment)
#    print result
#
