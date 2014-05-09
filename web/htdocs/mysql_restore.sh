#!/usr/bin/sh
DIRS=$1
DB=$2
CUR_DB=$3
mysql -uroot -proot -e "DROP DATABASE IF EXISTS $DB;";
mysql -uroot -proot -e "CREATE DATABASE $DB;";
mysql -uroot -proot -e "CREATE TABLE $DB.report_template SELECT * FROM $CUR_DB.report_template;"
mysql -uroot -proot -e "CREATE TABLE $DB.report_query_dict SELECT * FROM $CUR_DB.report_query_dict;"
mysql -uroot -proot $DB  <$DIRS/hosts.sql;
mysql -uroot -proot $DB  <$DIRS/hostgroups.sql;
mysql -uroot -proot $DB  <$DIRS/hosts_hostgroups.sql;
mysql -uroot -proot $DB  <$DIRS/device_type.sql;
mysql -uroot -proot $DB  <$DIRS/get_odu16_nw_interface_statistics_table.sql;
mysql -uroot -proot $DB  <$DIRS/get_odu16_peer_node_status_table.sql;
mysql -uroot -proot $DB  <$DIRS/get_odu16_ra_tdd_mac_statistics_entry.sql;
mysql -uroot -proot $DB  <$DIRS/get_odu16_synch_statistics_table.sql;
mysql -uroot -proot $DB  <$DIRS/odu100_nwInterfaceStatisticsTable.sql;
mysql -uroot -proot $DB  <$DIRS/odu100_peerNodeStatusTable.sql;
mysql -uroot -proot $DB  <$DIRS/odu100_raTddMacStatisticsTable.sql;
mysql -uroot -proot $DB  <$DIRS/odu100_synchStatisticsTable.sql;
mysql -uroot -proot $DB  <$DIRS/idu_swPrimaryPortStatisticsTable.sql;
mysql -uroot -proot $DB  <$DIRS/idu_portSecondaryStatisticsTable.sql;
mysql -uroot -proot $DB  <$DIRS/idu_portstatisticsTable.sql;
mysql -uroot -proot $DB  <$DIRS/idu_linkStatusTable.sql;
mysql -uroot -proot $DB  <$DIRS/idu_e1PortStatusTable.sql;
mysql -uroot -proot $DB  <$DIRS/system_alarm_table.sql;
mysql -uroot -proot $DB  <$DIRS/trap_alarms.sql;
mysql -uroot -proot $DB  <$DIRS/ap25_statisticsTable.sql;
mysql -uroot -proot $DB  <$DIRS/ap25_vapClientStatisticsTable.sql;
echo " ok ";

 
