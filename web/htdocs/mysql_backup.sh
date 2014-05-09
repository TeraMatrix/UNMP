#!/usr/bin/sh

DIRS=$1
mon=$2
where_condition=$2
DB_NAME=$3
rm -rf $DIRS
mkdir $DIRS
echo $where_condition
mysqldump -uroot -proot --databases $DB_NAME --tables hosts  --skip-add-locks >$DIRS/hosts.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables hostgroups  --skip-add-locks >$DIRS/hostgroups.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables hosts_hostgroups  --skip-add-locks >$DIRS/hosts_hostgroups.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables device_type  --skip-add-locks >$DIRS/device_type.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables get_odu16_nw_interface_statistics_table  --skip-add-locks --where="$where_condition">$DIRS/get_odu16_nw_interface_statistics_table.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables get_odu16_peer_node_status_table  --skip-add-locks --where="$where_condition">$DIRS/get_odu16_peer_node_status_table.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables get_odu16_ra_tdd_mac_statistics_entry  --skip-add-locks --where="$where_condition"> $DIRS/get_odu16_ra_tdd_mac_statistics_entry.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables get_odu16_synch_statistics_table  --skip-add-locks --where="$where_condition">$DIRS/get_odu16_synch_statistics_table.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables odu100_nwInterfaceStatisticsTable  --skip-add-locks --where="$where_condition">$DIRS/odu100_nwInterfaceStatisticsTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables odu100_peerNodeStatusTable  --skip-add-locks --where="$where_condition">$DIRS/odu100_peerNodeStatusTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables odu100_raTddMacStatisticsTable  --skip-add-locks --where="$where_condition">$DIRS/odu100_raTddMacStatisticsTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables odu100_synchStatisticsTable  --skip-add-locks --where="$where_condition">$DIRS/odu100_synchStatisticsTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables idu_swPrimaryPortStatisticsTable  --skip-add-locks --where="$where_condition">$DIRS/idu_swPrimaryPortStatisticsTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables idu_portSecondaryStatisticsTable  --skip-add-locks --where="$where_condition">$DIRS/idu_portSecondaryStatisticsTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables idu_portstatisticsTable  --skip-add-locks --where="$where_condition">$DIRS/idu_portstatisticsTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables idu_linkStatusTable  --skip-add-locks --where="$where_condition">$DIRS/idu_linkStatusTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables idu_e1PortStatusTable  --skip-add-locks --where="$where_condition">$DIRS/idu_e1PortStatusTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables system_alarm_table  --skip-add-locks --where="$where_condition">$DIRS/system_alarm_table.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables trap_alarms  --skip-add-locks --where="$where_condition">$DIRS/trap_alarms.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables ap25_statisticsTable  --skip-add-locks --where="$where_condition">$DIRS/ap25_statisticsTable.sql;
mysqldump -uroot -proot --databases $DB_NAME --tables ap25_vapClientStatisticsTable  --skip-add-locks --where="$where_condition">$DIRS/ap25_vapClientStatisticsTable.sql;
echo " ok "
