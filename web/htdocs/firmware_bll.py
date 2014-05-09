#!/usr/bin/python2.6

from unmp_model import *
from utility import UNMPDeviceType
from unmp_config import SystemConfig
from sqlalchemy import and_, or_, desc, asc
from common_controller import *
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *
from pysnmp_ap import pysnmp_get_table
from py_module import snmp_ping
from ap_profiling_bll import errorStatus
import ftplib

oid_dict = {'peerNodeStatus': '1.3.6.1.4.1.26149.2.2.13.9.2.1',
            'peerconfig': '1.3.6.1.4.1.26149.2.2.13.9.1.1'}


class DeviceParameters(object):
    def get_device_parameter(self, host_id):
        global sqlalche_obj
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            device_list_param = []
            device_list_param = sqlalche_obj.session.query(
                Hosts.ip_address, Hosts.mac_address, Hosts.device_type_id, Hosts.config_profile_id).filter(
                Hosts.host_id == host_id).all()
            if device_list_param == None:
                device_list_param = []
            return device_list_param
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def device_list_profiling(self, ip_address, mac_address, selected_device):
        global sqlalche_obj
        device_list = []
        device_type = selected_device
        device_list_state = "enabled"
        # try block starts
        try:
            # here we create the session of sqlalchemy
            sqlalche_obj.sql_alchemy_db_connection_open()
            # this is the query which returns the multidimensional array of
            # hosts table and store in device_tuple
            device_list = sqlalche_obj.session.query(
                Hosts.host_id, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address).filter(
                and_(Hosts.is_deleted == 0, Hosts.ip_address.like('%s%%' % (ip_address)),
                     Hosts.mac_address.like('%s%%' % (mac_address)), Hosts.device_type_id == device_type)).order_by(
                Hosts.host_alias).order_by(Hosts.ip_address).all()
            return device_list
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()


class FirmwareUpdate(object):
    def get_node_type(self, host_id, device_type):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        default_node_type = []
        host_data = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
        if len(host_data) > 0:
            config_profile_id = "" if host_data[
                                          0].config_profile_id == None else host_data[0].config_profile_id
        if device_type == UNMPDeviceType.odu16:
            default_node_type = sqlalche_obj.session.query(
                GetOdu16_ru_conf_table.default_node_type).filter(GetOdu16_ru_conf_table.host_id == host_id).all()
        elif device_type == UNMPDeviceType.odu100:
            default_node_type = sqlalche_obj.session.query(Odu100RuConfTable.defaultNodeType).filter(
                Odu100RuConfTable.config_profile_id == config_profile_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return default_node_type

    def get_master_host_id(self, host_id):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        master_host_id = []
        master_host_id = sqlalche_obj.session.query(
            MasterSlaveLinking.master).filter(MasterSlaveLinking.slave == host_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return master_host_id

    def get_master_slave_dic(self, master_host_id, master_slave_linking):
        global sqlalche_obj
        master_slave_list = []
        master_host_data = []
        master_firmware_data = []
        tunnel_status = 1
        link_status = 2
        sqlalche_obj.sql_alchemy_db_connection_open()
        if len(master_slave_linking) > 0:
            for i in range(0, len(master_slave_linking)):
                slave_host_data = sqlalche_obj.session.query(
                    Hosts.ip_address, Hosts.mac_address, Hosts.host_name, Hosts.host_asset_id).filter(
                    Hosts.host_id == master_slave_linking[i][0]).all()
                slave_firmware_data = sqlalche_obj.session.query(
                    HostAssets.firmware_status, HostAssets.firmware_type, HostAssets.firmware_file_name,
                    HostAssets.firmware_file_path).filter(
                    HostAssets.host_asset_id == slave_host_data[0].host_asset_id).all()
                master_slave_list.append(
                    {'node_type': 1, 'ip_address': slave_host_data[0].ip_address if len(slave_host_data) > 0 else "--",
                     'mac_address': slave_host_data[0].mac_address if len(slave_host_data) > 0 else "--",
                     'link_status': 0,
                     'tunnel_status': 2,
                     'firmware_status': "--" if slave_firmware_data[0].firmware_status == None else slave_firmware_data[
                         0].firmware_status if len(slave_firmware_data) > 0 else "--",
                     'firmware_type': "--" if slave_firmware_data[0].firmware_type == None else slave_firmware_data[
                         0].firmware_type if len(slave_firmware_data) > 0 else "--",
                     'firmware_status': "--" if slave_firmware_data[0].firmware_status == None else slave_firmware_data[
                         0].firmware_status if len(slave_firmware_data) > 0 else "--",
                     'firmware_file_name': "--" if slave_firmware_data[0].firmware_file_name == None else
                     slave_firmware_data[0].firmware_file_name if len(slave_firmware_data) > 0 else "--",
                     'firmware_file_path': "--" if slave_firmware_data[0].firmware_file_path == None else
                     slave_firmware_data[0].firmware_file_path if len(slave_firmware_data) > 0 else "--",
                     'host_id': str(master_slave_linking[i][0]), 'found': 0})

        host_data = sqlalche_obj.session.query(
            Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_read_community, Hosts.mac_address,
            Hosts.host_name).filter(Hosts.host_id == master_host_id).all()
        request_ping = snmp_ping(host_data[0].ip_address, host_data[0]
        .snmp_read_community, int(host_data[0].snmp_port))
        if int(request_ping) == 0:
            tunnel_status = 1
            link_status = 2
        else:
            tunnel_status = 2
            link_status = 0

        master_host_data = sqlalche_obj.session.query(
            Hosts.ip_address, Hosts.mac_address, Hosts.host_name, Hosts.host_asset_id).filter(
            Hosts.host_id == master_host_id).all()
        master_firmware_data = sqlalche_obj.session.query(HostAssets.firmware_status, HostAssets.firmware_type,
                                                          HostAssets.firmware_file_name,
                                                          HostAssets.firmware_file_path).filter(
            HostAssets.host_asset_id == master_host_data[0].host_asset_id).all()
        master_slave_list.append(
            {'node_type': 0, 'ip_address': master_host_data[0].ip_address if len(master_host_data) > 0 else "--",
             'mac_address': master_host_data[0].mac_address if len(master_host_data) > 0 else "--",
             'link_status': link_status,
             'tunnel_status': tunnel_status,
             'firmware_status': "--" if master_firmware_data[0].firmware_status == None else master_firmware_data[
                 0].firmware_status if len(master_firmware_data) > 0 else "--",
             'firmware_type': "--" if master_firmware_data[0].firmware_type == None else master_firmware_data[
                 0].firmware_type if len(master_firmware_data) > 0 else "--",
             'firmware_status': "--" if master_firmware_data[0].firmware_status == None else master_firmware_data[
                 0].firmware_status if len(master_firmware_data) > 0 else "--",
             'firmware_file_name': "--" if master_firmware_data[0].firmware_file_name == None else master_firmware_data[
                 0].firmware_file_name if len(master_firmware_data) > 0 else "--",
             'firmware_file_path': "--" if master_firmware_data[0].firmware_file_path == None else master_firmware_data[
                 0].firmware_file_path if len(master_firmware_data) > 0 else "--",
             'host_id': master_host_id, 'found': 0})
        return master_slave_list

    def get_master_slave_linking(self, master_id):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        master_slave_linking = []
        master_slave_linking = sqlalche_obj.session.query(
            MasterSlaveLinking.slave).filter(MasterSlaveLinking.master == master_id).all()
        master_slave_list = self.get_master_slave_dic(
            master_id, master_slave_linking)
        return master_slave_list

    def get_master_slave_update(self, master_host_id, master_slave_list, slave_list):

        for i in slave_list:
            for j in range(0, len(master_slave_list)):
                if i['host_id'] == master_slave_list[j]['host_id']:
                    master_slave_list[j].update(i)
                    break
                else:
                    if j == int(len(master_slave_list) - 1):
                        master_slave_list.append(i)
                    else:
                        continue
        return master_slave_list

    def get_master_slave_snmp(self, master_host_id, device_type):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        global errorStatus
        flag = 0
        host_data = []
        master_slave_list = []
        result_peer_node_status = []
        slave_host_data = []
        slave_firmware_data = []
        slave_host_id = []
        master_slave_update_list = []
        mac_address_dic = {}
        slave_list = []
        request_ping = 0
        found = 0
        result = 1
        macAddress = ""
        host_data = sqlalche_obj.session.query(
            Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_read_community, Hosts.mac_address, Hosts.host_name,
            Hosts.mac_address).filter(Hosts.host_id == master_host_id).all()
        if len(host_data) > 0:
            request_ping = snmp_ping(host_data[0].ip_address, host_data[0]
            .snmp_read_community, int(host_data[0].snmp_port))
            if request_ping == 0:
                result = 1
            elif request_ping == 1:
                result = "notPingMaster"
            elif request_ping == 2:
                result = "networkUnreachable"
            master_slave_list = self.get_master_slave_linking(master_host_id)
            if len(master_slave_list) > 0:
                result_peer_node_status = pysnmp_get_table(oid_dict['peerNodeStatus'], host_data[0].ip_address, int(
                    host_data[0].snmp_port), host_data[0].snmp_read_community)
                if result_peer_node_status["success"] == 0:
                    for i in result_peer_node_status["result"]:
                        if len(result_peer_node_status["result"][i]) > 0:
                            for j in master_slave_list:
                                if j["node_type"] == 1:
                                    if result_peer_node_status["result"][i][5] != "":
                                        macAddress = j["mac_address"] + ","
                                        if macAddress in result_peer_node_status["result"][i]:
                                            mac_address_dic[j["mac_address"]] = [
                                                result_peer_node_status["result"][i][2],
                                                result_peer_node_status["result"][i][3]]
                                        else:
                                            continue
                    if len(mac_address_dic) == 0:
                        return master_slave_list
                    else:
                        for i in master_slave_list:
                            if i["node_type"] == 1:
                                if i["mac_address"] in mac_address_dic:
                                    if device_type == UNMPDeviceType.odu16:
                                        slave_host_id = sqlalche_obj.session.query(
                                            GetOdu16RaStatusTable.host_id).filter(
                                            GetOdu16RaStatusTable.ra_mac_address == '%s' % (i["mac_address"])).all()
                                    else:
                                        slave_host_id = sqlalche_obj.session.query(
                                            Odu100RaStatusTable.host_id).filter(
                                            Odu100RaStatusTable.raMacAddress == '%s' % (i["mac_address"])).all()
                                if len(slave_host_id) > 0:
                                    slave_host_data = sqlalche_obj.session.query(Hosts.ip_address, Hosts.mac_address,
                                                                                 Hosts.host_name,
                                                                                 Hosts.host_asset_id).filter(
                                        Hosts.host_id == slave_host_id[0].host_id).all()
                                    slave_firmware_data = sqlalche_obj.session.query(HostAssets.firmware_status,
                                                                                     HostAssets.firmware_type,
                                                                                     HostAssets.firmware_file_name,
                                                                                     HostAssets.firmware_file_path).filter(
                                        HostAssets.host_asset_id == slave_host_data[0].host_asset_id).all()
                                    slave_list.append(
                                        {'node_type': 1, 'ip_address': slave_host_data[0].ip_address if len(
                                            slave_host_data) > 0 else "--",
                                         'mac_address': slave_host_data[0].mac_address if len(
                                             slave_host_data) > 0 else "--",
                                         'link_status': mac_address_dic[i["mac_address"]][0],
                                         'tunnel_status': mac_address_dic[i["mac_address"]][1],
                                         'firmware_status': "--" if slave_firmware_data[0].firmware_status == None else
                                         slave_firmware_data[0].firmware_status if len(
                                             slave_firmware_data) > 0 else "--",
                                         'firmware_type': "--" if slave_firmware_data[0].firmware_type == None else
                                         slave_firmware_data[0].firmware_type if len(slave_firmware_data) > 0 else "--",
                                         'firmware_status': "--" if slave_firmware_data[0].firmware_status == None else
                                         slave_firmware_data[0].firmware_status if len(
                                             slave_firmware_data) > 0 else "--",
                                         'firmware_file_name': "--" if slave_firmware_data[
                                                                           0].firmware_file_name == None else
                                         slave_firmware_data[0].firmware_file_name if len(
                                             slave_firmware_data) > 0 else "--",
                                         'firmware_file_path': "--" if slave_firmware_data[
                                                                           0].firmware_file_path == None else
                                         slave_firmware_data[0].firmware_file_path if len(
                                             slave_firmware_data) > 0 else "--",
                                         'host_id': str(slave_host_id[0].host_id), 'found': found})
                                else:
                                    discovered_host_exist = sqlalche_obj.session.query(DiscoveredHosts).filter(
                                        DiscoveredHosts.mac_address == '%s' % (i["mac_address"])).all()
                                    tcp_discovery_host_exist = sqlalche_obj.session.query(
                                        TcpDiscovery).filter(TcpDiscovery.site_mac == '%s' % (i["mac_address"])).all()
                                    if len(discovered_host_exist) > 0 or len(tcp_discovery_host_exist) > 0:
                                        found = 1
                                    else:
                                        found = 2
                                    slave_list.append(
                                        {'node_type': 1, 'ip_address': '',
                                         'mac_address': '',
                                         'link_status': mac_address_dic[i["mac_address"]][0],
                                         'tunnel_status': mac_address_dic[i["mac_address"]][1],
                                         'firmware_status': "--",
                                         'firmware_type': "--",
                                         'firmware_status': "--",
                                         'firmware_file_name': "--",
                                         'firmware_file_path': "--",
                                         'host_id': None, 'found': found})
                    master_slave_update_list = self.get_master_slave_update(
                        master_host_id, master_slave_list, slave_list)
                else:
                    flag = 1
                    return master_slave_list, result
            else:
                flag = 1
                result = "noSite"
            sqlalche_obj.sql_alchemy_db_connection_close()
            if flag == 0:
                return master_slave_update_list, result
            else:
                return result

    def directory_exists_here(self, directory_name):
        filelist = []
        self.ftp.retrlines('LIST', filelist.append)
        for f in filelist:
            if f.split()[-1] == directory_name:
                return True
        return False

    def select_firmware_table(self, device_type):
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        firmware_table = []
        firmware_table = sqlalche_obj.session.query(
            FirmwareListTable.firmware_file_name, FirmwareListTable.firmware_file_path).filter(
            FirmwareListTable.device_type == device_type).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return firmware_table

    def ftp_upload(self, file_path, device_type, filename):
        mkdir = True
        final_result = {}
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        obj_system_config = SystemConfig()
        result = ""
        # ftp_credentials = obj_system_config.get_ftp_details()
        try:
            try:
                f = ftplib.FTP("172.22.0.91", "unmpftp", "nms@123")
                # f =
                # ftplib.FTP(ftp_credentials["ip"],ftp_credentials["username"],ftp_credentials["password"])
            except ftplib.all_errors, e:
                errorcode_string = str(e).split(None, 1)
                final_result = {"success": 1, "result":
                    errorcode_string[1] + " Please Retry Again"}
            else:
                try:
                    f.cwd("/unmp-ftp/%s" % (device_type))
                except ftplib.all_errors, e:
                    f.mkd("/unmp-ftp/%s" % (device_type))
                fp = open(file_path, "rb")
                try:
                    result = f.storbinary(
                        'STOR /unmp-ftp/%s/%s' % (device_type, filename), fp)
                except ftplib.all_errors, e:
                    final_result = {"success": 1, "result":
                        "File not uploaded successfully.Please retry again"}
                if result == "226 Transfer complete.":
                    final_result = {"success": 0,
                                    "result": "File Uploaded SuccessFully"}
                    ftp_table = sqlalche_obj.session.query(
                        FirmwareListTable).filter(
                        and_(FirmwareListTable.device_type == device_type,
                             FirmwareListTable.firmware_file_name == filename)).all()
                    if len(ftp_table) == 0:
                        table_insert = FirmwareListTable(
                            device_type, filename, file_path)
                        sqlalche_obj.session.add(table_insert)
                    else:
                        ftp_table[0].firmware_file_path = file_path
                    sqlalche_obj.session.commit()
                else:
                    final_result = {"success": 1, "result":
                        "File not uploaded successfully.Please retry again"}
            return final_result
        except Exception as e:
            return str(e)

# obj = FirmwareUpdate()
# print obj.get_master_slave_snmp(11,'odu100')
# print
# obj.ftp_upload("/omd/sites/nms3/share/check_mk/web/htdocs/download/firmware_downloads/odu100/aa.img","odu100","aa.img")
