import re
import datetime

fread = open("complete_db_structure.sql", 'r')
filedata = fread.readlines()

count = 0
count_year = int(raw_input("how many years:>"))  # license validity
now = datetime.datetime.now()

cur_yer = now.year
cur_mon = now.month

tableList = ["acknowledge",
             "alarm_recon",
             "actions",
             "black_list_macs",
             "cities",
             "countries",

             "ap25_accesspointIPsettings",
             "ap25_vapWEPsecurityConfigTable",
             "ap25_vapWPAsecurityConfigTable",
             "ap_client_ap_data",
             "ap_client_details",
             "ap25_versions",
             "ap25_aclMacTable",
             "ap25_aclStatisticsTable",
             "ap25_basicACLconfigTable",
             "ap25_basicConfiguration",
             "ap25_basicVAPconfigTable",
             "ap25_basicVAPsecurity",
             "ap25_dhcpServer",
             "ap25_oids",
             "ap25_oids_multivalues",
             "ap25_oid_table",
             "ap25_radioSelection",
             "ap25_radioSetup",
             "ap25_services",
             "ap25_vapSelection",
             "ap_connected_client",
             "ap_scheduling",
             "ap_scheduling_host_mapping",

             "get_ap25_bandwidth",
             "get_ap25_connected_user",
             "get_ap25_misc",

             "get_odu16_active_alarm_table",
             "get_odu16_hw_desc_table",
             "get_odu16_misc",
             "get_odu16_network_interface_status_table",
             "get_odu16_nw_interface_status_table",
             "get_odu16_peer_link_statistics_table",
             "get_odu16_peer_tunnel_statistics_table",

             "config_profiles",
             "config_profile_type",
             "device_type",
             "discovered_hosts",
             "discovery",
             "discovery_type",
             "error_description",
             "event_type",
             "firmware_list_table",

             "daemon_events",
             "daemon_timestamp",

             "ap25_apScanDataTable",
             "ap25_dhcpClientsTable"
             ]

partitionTableList = [
    "get_odu16_nw_interface_statistics_table",
    "get_odu16_synch_statistics_table",
    "get_odu16_peer_node_status_table",
    "get_odu16_ra_tdd_mac_statistics_entry",
    "event_log",
    "odu100_nwInterfaceStatisticsTable",
    "odu100_synchStatisticsTable",
    "odu100_raTddMacStatisticsTable",
    "odu100_raScanListTable",
    "odu100_peerNodeStatusTable",
    "idu_tdmoipNetworkInterfaceStatisticsTable",
    "idu_iduNetworkStatisticsTable",
    "idu_e1PortStatusTable",
    "idu_linkStatusTable",
    "idu_portSecondaryStatisticsTable",
    "idu_portstatisticsTable",
    "idu_swPrimaryPortStatisticsTable",
    "analyze_get_odu16_nw_interface_statistics_table",
    "analyze_get_odu16_peer_node_status_table",
    "analyze_get_odu16_ra_tdd_mac_statistics_entry",
    "analyze_get_odu16_synch_statistics_table",
    "analyze_idu_portSecondaryStatisticsTable",
    "analyze_idu_portstatisticsTable",
    "analyze_idu_swPrimaryPortStatisticsTable",
    "analyze_odu100_nwInterfaceStatisticsTable",
    "analyze_odu100_peerNodeStatusTable",
    "analyze_odu100_raTddMacStatisticsTable",
    "analyze_odu100_synchStatisticsTable",
    "ap25_statisticsTable",
    "ap25_vapClientStatisticsTable"
]

if cur_mon != 1:
    count_year += 1

for line in filedata:
    r3 = re.compile("CREATE TABLE IF NOT EXISTS (.*?)\s*`(.*?)`")
    matcher = r3.match(line)

    r4 = re.compile("nagios_*")
    r5 = re.compile("ccu_*")

    if matcher is not None:
        """
            include the nagios tables in the tables to be excluded
            include the ccu tables
        """
        tables4 = matcher.group(2)
        tables5 = matcher.group(2)

        m4 = r4.match(tables4)
        m5 = r5.match(tables5)

        if m4 is not None:
            tableList.append(tables4)
        if m5 is not None:
            tableList.append(tables5)

        if matcher.group(2) not in tableList and matcher.group(2) in partitionTableList:
                    count += 1
                    fwrite = open("resetPartition.sql", 'a')
                    fwrite.write("ALTER TABLE " + matcher.group(2) + "\n")
                    fwrite.write(
                        "PARTITION BY RANGE(TO_DAYS(timestamp) )" + "\n")
                    fwrite.write("(" + "\n")
                    j = 0
                    i = cur_yer
                    while j < count_year:
                        if j == 0 and cur_mon != 1:
                            x = cur_mon - 1
                            y = 12
                        elif j == count_year - 1 and cur_mon != 1:
                            x = 0
                            y = cur_mon + 1
                        else:
                            x = 0
                            y = 12
                        while x < y:
                            x += 1
                            writeThis = "PARTITION p" + str(x * i + x - 1) + \
                                " VALUES LESS THAN (TO_DAYS(" + "'" + str(i) + "-"\
                                + str(x) + "-" + "01" + "'" + "))"
                            fwrite.write(writeThis)
                            if j == count_year - 1 and x == y:
                                fwrite.write("\n")
                            else:
                                fwrite.write(", \n")
                        i += 1
                        j += 1
                    fwrite.write("); \n")
                    fwrite.close
fread.close()
print count
