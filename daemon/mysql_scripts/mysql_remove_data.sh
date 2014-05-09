#!/usr/bin/sh

where_condition=$1;
DB=$2;
mysql -uroot -proot -e "DELETE FROM $DB.get_odu16_nw_interface_statistics_table $where_condition";
mysql -uroot -proot -e "DELETE FROM $DB.get_odu16_peer_node_status_table $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.get_odu16_ra_tdd_mac_statistics_entry $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.get_odu16_synch_statistics_table $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.odu100_nwInterfaceStatisticsTable $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.odu100_peerNodeStatusTable $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.odu100_raTddMacStatisticsTable $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.odu100_synchStatisticsTable $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.idu_swPrimaryPortStatisticsTable $where_condition" ;  
mysql -uroot -proot -e "DELETE FROM $DB.idu_portSecondaryStatisticsTable $where_condition";   
mysql -uroot -proot -e "DELETE FROM $DB.idu_portstatisticsTable $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.idu_linkStatusTable $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.idu_e1PortStatusTable $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.ap25_statisticsTable $where_condition"   ;
mysql -uroot -proot -e "DELETE FROM $DB.ap25_vapClientStatisticsTable $where_condition"   ;

echo " ok ";
