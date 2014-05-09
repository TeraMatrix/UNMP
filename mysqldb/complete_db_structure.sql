SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


DROP TABLE IF EXISTS `acknowledge`;
CREATE TABLE IF NOT EXISTS `acknowledge` (
  `acknowledge_id` varchar(16) NOT NULL,
  `acknowledge_name` varchar(32) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `sequence` smallint(6) DEFAULT '0',
  PRIMARY KEY (`acknowledge_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `actions`;
CREATE TABLE IF NOT EXISTS `actions` (
  `action_id` varchar(64) NOT NULL,
  `action_name` varchar(32) DEFAULT NULL,
  `action_options` varchar(256) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `sequence` smallint(6) DEFAULT '0',
  PRIMARY KEY (`action_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `alarm_recon`;
CREATE TABLE IF NOT EXISTS `alarm_recon` (
  `alarm_recon_id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(120) NOT NULL DEFAULT ' ',
  `how_many` smallint(6) NOT NULL DEFAULT '-1' COMMENT 'Number of alarms reconciled.',
  `host_id` int(11) unsigned NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`alarm_recon_id`),
  UNIQUE KEY `fk_alarm_recon` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_ap25_statisticsTable`;
CREATE TABLE IF NOT EXISTS `analyze_ap25_statisticsTable` (
  `analyze_ap25_statisticsTable_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `index_0_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_0_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_4_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_5_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_6_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_7_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_8_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_9_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsRxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsRxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsRxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsRxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsTxPackets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsTxPackets_Min` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsTxPackets_Max` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsTxPackets_Total` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsRxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsRxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsRxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsRxError_Total` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsTxError_Avg` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsTxError_Min` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsTxError_Max` int(11) NOT NULL DEFAULT '0',
  `index_10_statisticsTxError_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_ap25_statisticsTable_id`,`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_get_odu16_nw_interface_statistics_table`;
CREATE TABLE IF NOT EXISTS `analyze_get_odu16_nw_interface_statistics_table` (
  `analyze_get_odu16_nw_interface_statistics_table_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `index_1_rx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_multicast_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_multicast_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_multicast_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_multicast_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_colisions_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_colisions_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_colisions_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_colisions_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_multicast_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_multicast_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_multicast_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_multicast_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_colisions_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_colisions_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_colisions_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_colisions_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_tx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_multicast_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_multicast_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_multicast_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_rx_multicast_Total` int(11) NOT NULL DEFAULT '0',
  `index_3_colisions_Avg` int(11) NOT NULL DEFAULT '0',
  `index_3_colisions_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_colisions_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_colisions_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_get_odu16_nw_interface_statistics_table_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_get_odu16_peer_node_status_table`;
CREATE TABLE IF NOT EXISTS `analyze_get_odu16_peer_node_status_table` (
  `analyze_get_odu16_peer_node_status_table_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `index_1_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_Range` int(11) NOT NULL DEFAULT '0',
  `index_1_Range_count` int(11) NOT NULL DEFAULT '0',
  `index_2_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_Range` int(11) NOT NULL DEFAULT '0',
  `index_2_Range_count` int(11) NOT NULL DEFAULT '0',
  `index_3_Min` int(11) NOT NULL DEFAULT '0',
  `index_3_Max` int(11) NOT NULL DEFAULT '0',
  `index_3_Range` int(11) NOT NULL DEFAULT '0',
  `index_3_Range_count` int(11) NOT NULL DEFAULT '0',
  `index_4_Min` int(11) NOT NULL DEFAULT '0',
  `index_4_Max` int(11) NOT NULL DEFAULT '0',
  `index_4_Range` int(11) NOT NULL DEFAULT '0',
  `index_4_Range_count` int(11) NOT NULL DEFAULT '0',
  `index_5_Min` int(11) NOT NULL DEFAULT '0',
  `index_5_Max` int(11) NOT NULL DEFAULT '0',
  `index_5_Range` int(11) NOT NULL DEFAULT '0',
  `index_5_Range_count` int(11) NOT NULL DEFAULT '0',
  `index_6_Min` int(11) NOT NULL DEFAULT '0',
  `index_6_Max` int(11) NOT NULL DEFAULT '0',
  `index_6_Range` int(11) NOT NULL DEFAULT '0',
  `index_6_Range_count` int(11) NOT NULL DEFAULT '0',
  `index_7_Min` int(11) NOT NULL DEFAULT '0',
  `index_7_Max` int(11) NOT NULL DEFAULT '0',
  `index_7_Range` int(11) NOT NULL DEFAULT '0',
  `index_7_Range_count` int(11) NOT NULL DEFAULT '0',
  `index_8_Min` int(11) NOT NULL DEFAULT '0',
  `index_8_Max` int(11) NOT NULL DEFAULT '0',
  `index_8_Range` int(11) NOT NULL DEFAULT '0',
  `index_8_Range_count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_get_odu16_peer_node_status_table_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_get_odu16_ra_tdd_mac_statistics_entry`;
CREATE TABLE IF NOT EXISTS `analyze_get_odu16_ra_tdd_mac_statistics_entry` (
  `analyze_get_odu16_ra_tdd_mac_statistics_entry_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `rx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `rx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `rx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `tx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `tx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `tx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `tx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `rx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `rx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `rx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `tx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `tx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `tx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `tx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `rx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `rx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `rx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `tx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `tx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `tx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `tx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `rx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `rx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `rx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `tx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `tx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `tx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `tx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `rx_crc_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_crc_errors_Min` int(11) NOT NULL DEFAULT '0',
  `rx_crc_errors_Max` int(11) NOT NULL DEFAULT '0',
  `rx_crc_errors_Total` int(11) NOT NULL DEFAULT '0',
  `rx_phy_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_phy_errors_Min` int(11) NOT NULL DEFAULT '0',
  `rx_phy_errors_Max` int(11) NOT NULL DEFAULT '0',
  `rx_phy_errors_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_get_odu16_ra_tdd_mac_statistics_entry_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_get_odu16_synch_statistics_table`;
CREATE TABLE IF NOT EXISTS `analyze_get_odu16_synch_statistics_table` (
  `analyze_get_odu16_synch_statistics_table_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `synch_loss_Avg` int(11) NOT NULL DEFAULT '0',
  `synch_loss_Min` int(11) NOT NULL DEFAULT '0',
  `synch_loss_Max` int(11) NOT NULL DEFAULT '0',
  `synch_loss_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_get_odu16_synch_statistics_table_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_idu_portSecondaryStatisticsTable`;
CREATE TABLE IF NOT EXISTS `analyze_idu_portSecondaryStatisticsTable` (
  `analyze_idu_portSecondaryStatisticsTable_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `switchPortNum` varchar(10) NOT NULL DEFAULT 'odu',
  `inUnicast_Avg` int(11) NOT NULL DEFAULT '0',
  `inUnicast_Min` int(11) NOT NULL DEFAULT '0',
  `inUnicast_Max` int(11) NOT NULL DEFAULT '0',
  `inUnicast_Total` int(11) NOT NULL DEFAULT '0',
  `outUnicast_Avg` int(11) NOT NULL DEFAULT '0',
  `outUnicast_Min` int(11) NOT NULL DEFAULT '0',
  `outUnicast_Max` int(11) NOT NULL DEFAULT '0',
  `outUnicast_Total` int(11) NOT NULL DEFAULT '0',
  `inBroadcast_Avg` int(11) NOT NULL DEFAULT '0',
  `inBroadcast_Min` int(11) NOT NULL DEFAULT '0',
  `inBroadcast_Max` int(11) NOT NULL DEFAULT '0',
  `inBroadcast_Total` int(11) NOT NULL DEFAULT '0',
  `outBroadcast_Avg` int(11) NOT NULL DEFAULT '0',
  `outBroadcast_Min` int(11) NOT NULL DEFAULT '0',
  `outBroadcast_Max` int(11) NOT NULL DEFAULT '0',
  `outBroadcast_Total` int(11) NOT NULL DEFAULT '0',
  `inMulticast_Avg` int(11) NOT NULL DEFAULT '0',
  `inMulticast_Min` int(11) NOT NULL DEFAULT '0',
  `inMulticast_Max` int(11) NOT NULL DEFAULT '0',
  `inMulticast_Total` int(11) NOT NULL DEFAULT '0',
  `outMulricast_Avg` int(11) NOT NULL DEFAULT '0',
  `outMulricast_Min` int(11) NOT NULL DEFAULT '0',
  `outMulricast_Max` int(11) NOT NULL DEFAULT '0',
  `outMulricast_Total` int(11) NOT NULL DEFAULT '0',
  `inUndersizeRx_Avg` int(11) NOT NULL DEFAULT '0',
  `inUndersizeRx_Min` int(11) NOT NULL DEFAULT '0',
  `inUndersizeRx_Max` int(11) NOT NULL DEFAULT '0',
  `inUndersizeRx_Total` int(11) NOT NULL DEFAULT '0',
  `inFragmentsRx_Avg` int(11) NOT NULL DEFAULT '0',
  `inFragmentsRx_Min` int(11) NOT NULL DEFAULT '0',
  `inFragmentsRx_Max` int(11) NOT NULL DEFAULT '0',
  `inFragmentsRx_Total` int(11) NOT NULL DEFAULT '0',
  `inOversizeRx_Avg` int(11) NOT NULL DEFAULT '0',
  `inOversizeRx_Min` int(11) NOT NULL DEFAULT '0',
  `inOversizeRx_Max` int(11) NOT NULL DEFAULT '0',
  `inOversizeRx_Total` int(11) NOT NULL DEFAULT '0',
  `inJabberRx_Avg` int(11) NOT NULL DEFAULT '0',
  `inJabberRx_Min` int(11) NOT NULL DEFAULT '0',
  `inJabberRx_Max` int(11) NOT NULL DEFAULT '0',
  `inJabberRx_Total` int(11) NOT NULL DEFAULT '0',
  `inMacRcvErrorRx_Avg` int(11) NOT NULL DEFAULT '0',
  `inMacRcvErrorRx_Min` int(11) NOT NULL DEFAULT '0',
  `inMacRcvErrorRx_Max` int(11) NOT NULL DEFAULT '0',
  `inMacRcvErrorRx_Total` int(11) NOT NULL DEFAULT '0',
  `inFCSErrorRx_Avg` int(11) NOT NULL DEFAULT '0',
  `inFCSErrorRx_Min` int(11) NOT NULL DEFAULT '0',
  `inFCSErrorRx_Max` int(11) NOT NULL DEFAULT '0',
  `inFCSErrorRx_Total` int(11) NOT NULL DEFAULT '0',
  `outFCSErrorTx_Avg` int(11) NOT NULL DEFAULT '0',
  `outFCSErrorTx_Min` int(11) NOT NULL DEFAULT '0',
  `outFCSErrorTx_Max` int(11) NOT NULL DEFAULT '0',
  `outFCSErrorTx_Total` int(11) NOT NULL DEFAULT '0',
  `deferedTx_Avg` int(11) NOT NULL DEFAULT '0',
  `deferedTx_Min` int(11) NOT NULL DEFAULT '0',
  `deferedTx_Max` int(11) NOT NULL DEFAULT '0',
  `deferedTx_Total` int(11) NOT NULL DEFAULT '0',
  `collisionTx_Avg` int(11) NOT NULL DEFAULT '0',
  `collisionTx_Min` int(11) NOT NULL DEFAULT '0',
  `collisionTx_Max` int(11) NOT NULL DEFAULT '0',
  `collisionTx_Total` int(11) NOT NULL DEFAULT '0',
  `lateTx_Avg` int(11) NOT NULL DEFAULT '0',
  `lateTx_Min` int(11) NOT NULL DEFAULT '0',
  `lateTx_Max` int(11) NOT NULL DEFAULT '0',
  `lateTx_Total` int(11) NOT NULL DEFAULT '0',
  `exessiveTx_Avg` int(11) NOT NULL DEFAULT '0',
  `exessiveTx_Min` int(11) NOT NULL DEFAULT '0',
  `exessiveTx_Max` int(11) NOT NULL DEFAULT '0',
  `exessiveTx_Total` int(11) NOT NULL DEFAULT '0',
  `singleTx_Avg` int(11) NOT NULL DEFAULT '0',
  `singleTx_Min` int(11) NOT NULL DEFAULT '0',
  `singleTx_Max` int(11) NOT NULL DEFAULT '0',
  `singleTx_Total` int(11) NOT NULL DEFAULT '0',
  `multipleTx_Avg` int(11) NOT NULL DEFAULT '0',
  `multipleTx_Min` int(11) NOT NULL DEFAULT '0',
  `multipleTx_Max` int(11) NOT NULL DEFAULT '0',
  `multipleTx_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_idu_portSecondaryStatisticsTable_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_idu_portstatisticsTable`;
CREATE TABLE IF NOT EXISTS `analyze_idu_portstatisticsTable` (
  `analyze_idu_portstatisticsTable_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `softwarestatportnum` varchar(10) NOT NULL DEFAULT 'odu',
  `framerx_Avg` int(11) NOT NULL DEFAULT '0',
  `framerx_Min` int(11) NOT NULL DEFAULT '0',
  `framerx_Max` int(11) NOT NULL DEFAULT '0',
  `framerx_Total` int(11) NOT NULL DEFAULT '0',
  `frametx_Avg` int(11) NOT NULL DEFAULT '0',
  `frametx_Min` int(11) NOT NULL DEFAULT '0',
  `frametx_Max` int(11) NOT NULL DEFAULT '0',
  `frametx_Total` int(11) NOT NULL DEFAULT '0',
  `indiscards_Avg` int(11) NOT NULL DEFAULT '0',
  `indiscards_Min` int(11) NOT NULL DEFAULT '0',
  `indiscards_Max` int(11) NOT NULL DEFAULT '0',
  `indiscards_Total` int(11) NOT NULL DEFAULT '0',
  `ingoodoctets_Avg` int(11) NOT NULL DEFAULT '0',
  `ingoodoctets_Min` int(11) NOT NULL DEFAULT '0',
  `ingoodoctets_Max` int(11) NOT NULL DEFAULT '0',
  `ingoodoctets_Total` int(11) NOT NULL DEFAULT '0',
  `inbadoctet_Avg` int(11) NOT NULL DEFAULT '0',
  `inbadoctet_Min` int(11) NOT NULL DEFAULT '0',
  `inbadoctet_Max` int(11) NOT NULL DEFAULT '0',
  `inbadoctet_Total` int(11) NOT NULL DEFAULT '0',
  `outoctets_Avg` int(11) NOT NULL DEFAULT '0',
  `outoctets_Min` int(11) NOT NULL DEFAULT '0',
  `outoctets_Max` int(11) NOT NULL DEFAULT '0',
  `outoctets_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_idu_portstatisticsTable_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_idu_swPrimaryPortStatisticsTable`;
CREATE TABLE IF NOT EXISTS `analyze_idu_swPrimaryPortStatisticsTable` (
  `analyze_idu_swPrimaryPortStatisticsTable_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `swportnumber` varchar(10) NOT NULL DEFAULT 'odu',
  `framesRx_Avg` int(11) NOT NULL DEFAULT '0',
  `framesRx_Min` int(11) NOT NULL DEFAULT '0',
  `framesRx_Max` int(11) NOT NULL DEFAULT '0',
  `framesRx_Total` int(11) NOT NULL DEFAULT '0',
  `framesTx_Avg` int(11) NOT NULL DEFAULT '0',
  `framesTx_Min` int(11) NOT NULL DEFAULT '0',
  `framesTx_Max` int(11) NOT NULL DEFAULT '0',
  `framesTx_Total` int(11) NOT NULL DEFAULT '0',
  `inDiscard_Avg` int(11) NOT NULL DEFAULT '0',
  `inDiscard_Min` int(11) NOT NULL DEFAULT '0',
  `inDiscard_Max` int(11) NOT NULL DEFAULT '0',
  `inDiscard_Total` int(11) NOT NULL DEFAULT '0',
  `inGoodOctets_Avg` int(11) NOT NULL DEFAULT '0',
  `inGoodOctets_Min` int(11) NOT NULL DEFAULT '0',
  `inGoodOctets_Max` int(11) NOT NULL DEFAULT '0',
  `inGoodOctets_Total` int(11) NOT NULL DEFAULT '0',
  `inBadOctets_Avg` int(11) NOT NULL DEFAULT '0',
  `inBadOctets_Min` int(11) NOT NULL DEFAULT '0',
  `inBadOctets_Max` int(11) NOT NULL DEFAULT '0',
  `inBadOctets_Total` int(11) NOT NULL DEFAULT '0',
  `outOctets_Avg` int(11) NOT NULL DEFAULT '0',
  `outOctets_Min` int(11) NOT NULL DEFAULT '0',
  `outOctets_Max` int(11) NOT NULL DEFAULT '0',
  `outOctets_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_idu_swPrimaryPortStatisticsTable_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_odu100_nwInterfaceStatisticsTable`;
CREATE TABLE IF NOT EXISTS `analyze_odu100_nwInterfaceStatisticsTable` (
  `analyze_odu100_nwInterfaceStatisticsTable_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `index_1_rx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_tx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_multicast_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_multicast_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_multicast_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_rx_multicast_Total` int(11) NOT NULL DEFAULT '0',
  `index_1_colisions_Avg` int(11) NOT NULL DEFAULT '0',
  `index_1_colisions_Min` int(11) NOT NULL DEFAULT '0',
  `index_1_colisions_Max` int(11) NOT NULL DEFAULT '0',
  `index_1_colisions_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_bytes_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_bytes_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_bytes_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_bytes_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_tx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_multicast_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_multicast_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_multicast_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_rx_multicast_Total` int(11) NOT NULL DEFAULT '0',
  `index_2_colisions_Avg` int(11) NOT NULL DEFAULT '0',
  `index_2_colisions_Min` int(11) NOT NULL DEFAULT '0',
  `index_2_colisions_Max` int(11) NOT NULL DEFAULT '0',
  `index_2_colisions_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_odu100_nwInterfaceStatisticsTable_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_odu100_peerNodeStatusTable`;
CREATE TABLE IF NOT EXISTS `analyze_odu100_peerNodeStatusTable` (
  `analyze_odu100_peerNodeStatusTable_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `sig1_index_1_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_1_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_1_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_1_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_1_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_1_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_2_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_2_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_2_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_2_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_2_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_2_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_3_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_3_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_3_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_3_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_3_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_3_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_4_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_4_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_4_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_4_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_4_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_4_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_5_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_5_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_5_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_5_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_5_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_5_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_6_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_6_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_6_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_6_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_6_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_6_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_7_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_7_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_7_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_7_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_7_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_7_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_8_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_8_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_8_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_8_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_8_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_8_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_9_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_9_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_9_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_9_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_9_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_9_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_10_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_10_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_10_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_10_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_10_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_10_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_11_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_11_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_11_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_11_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_11_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_11_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_12_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_12_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_12_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_12_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_12_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_12_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_13_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_13_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_13_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_13_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_13_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_13_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_14_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_14_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_14_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_14_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_14_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_14_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_15_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_15_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_15_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_15_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_15_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_15_Range` int(11) NOT NULL DEFAULT '0',
  `sig1_index_16_Min` int(11) NOT NULL DEFAULT '0',
  `sig1_index_16_Max` int(11) NOT NULL DEFAULT '0',
  `sig1_index_16_Range` int(11) NOT NULL DEFAULT '0',
  `sig2_index_16_Min` int(11) NOT NULL DEFAULT '0',
  `sig2_index_16_Max` int(11) NOT NULL DEFAULT '0',
  `sig2_index_16_Range` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_odu100_peerNodeStatusTable_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_odu100_raTddMacStatisticsTable`;
CREATE TABLE IF NOT EXISTS `analyze_odu100_raTddMacStatisticsTable` (
  `analyze_odu100_raTddMacStatisticsTable_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `rx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `rx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `rx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `tx_packets_Avg` int(11) NOT NULL DEFAULT '0',
  `tx_packets_Min` int(11) NOT NULL DEFAULT '0',
  `tx_packets_Max` int(11) NOT NULL DEFAULT '0',
  `tx_packets_Total` int(11) NOT NULL DEFAULT '0',
  `rx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `rx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `rx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `tx_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `tx_errors_Min` int(11) NOT NULL DEFAULT '0',
  `tx_errors_Max` int(11) NOT NULL DEFAULT '0',
  `tx_errors_Total` int(11) NOT NULL DEFAULT '0',
  `rx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `rx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `rx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `tx_dropped_Avg` int(11) NOT NULL DEFAULT '0',
  `tx_dropped_Min` int(11) NOT NULL DEFAULT '0',
  `tx_dropped_Max` int(11) NOT NULL DEFAULT '0',
  `tx_dropped_Total` int(11) NOT NULL DEFAULT '0',
  `rx_crc_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_crc_errors_Min` int(11) NOT NULL DEFAULT '0',
  `rx_crc_errors_Max` int(11) NOT NULL DEFAULT '0',
  `rx_crc_errors_Total` int(11) NOT NULL DEFAULT '0',
  `rx_phy_errors_Avg` int(11) NOT NULL DEFAULT '0',
  `rx_phy_errors_Min` int(11) NOT NULL DEFAULT '0',
  `rx_phy_errors_Max` int(11) NOT NULL DEFAULT '0',
  `rx_phy_errors_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_odu100_raTddMacStatisticsTable_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `analyze_odu100_synchStatisticsTable`;
CREATE TABLE IF NOT EXISTS `analyze_odu100_synchStatisticsTable` (
  `analyze_odu100_synchStatisticsTable_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `host_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'HOURLY',
  `synch_loss_Avg` int(11) NOT NULL DEFAULT '0',
  `synch_loss_Min` int(11) NOT NULL DEFAULT '0',
  `synch_loss_Max` int(11) NOT NULL DEFAULT '0',
  `synch_loss_Total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`analyze_odu100_synchStatisticsTable_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_accesspointIPsettings`;
CREATE TABLE IF NOT EXISTS `ap25_accesspointIPsettings` (
  `ap25_accesspointIPsettings_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `lanIPaddress` varchar(16) DEFAULT NULL,
  `lanSubnetMask` varchar(16) DEFAULT NULL,
  `lanGatewayIP` varchar(16) DEFAULT NULL,
  `lanPrimaryDNS` varchar(16) DEFAULT NULL,
  `lanSecondaryDNS` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`ap25_accesspointIPsettings_id`),
  KEY `FK_ap25_accesspointIPsettings_id` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_aclMacTable`;
CREATE TABLE IF NOT EXISTS `ap25_aclMacTable` (
  `ap25_aclMacTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned NOT NULL,
  `vapselection_id` int(10) unsigned NOT NULL,
  `aclMACsIndex` smallint(5) unsigned DEFAULT NULL,
  `macaddress` varchar(18) DEFAULT NULL,
  PRIMARY KEY (`ap25_aclMacTable_id`),
  KEY `FK_ap25_aclMacTable_id` (`vapselection_id`),
  KEY `FK_ap25_aclMac_config` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_aclStatisticsTable`;
CREATE TABLE IF NOT EXISTS `ap25_aclStatisticsTable` (
  `ap25_aclStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned NOT NULL,
  `aclTotalsINDEX` int(32) DEFAULT NULL,
  `vapNumber` int(10) DEFAULT NULL,
  `totalMACentries` int(10) DEFAULT NULL,
  PRIMARY KEY (`ap25_aclStatisticsTable_id`),
  KEY `FK_ap25_aclStatistics_config` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_basicACLconfigTable`;
CREATE TABLE IF NOT EXISTS `ap25_basicACLconfigTable` (
  `ap25_basicACLconfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned NOT NULL,
  `vapselection_id` int(10) unsigned DEFAULT NULL,
  `aclState` smallint(6) DEFAULT NULL,
  `aclMode` smallint(6) DEFAULT NULL,
  `aclAddMAC` varchar(18) DEFAULT NULL,
  `aclDeleteOneMAC` varchar(10) DEFAULT NULL,
  `aclDeleteAllMACs` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ap25_basicACLconfigTable_id`),
  KEY `FK_ap25_basicACLsetup` (`vapselection_id`),
  KEY `FK_ap25_vapWEPsecuritySetup_config_id` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_basicConfiguration`;
CREATE TABLE IF NOT EXISTS `ap25_basicConfiguration` (
  `ap25_basicConfiguration_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `accesspointName` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`ap25_basicConfiguration_id`),
  KEY `FK_ap25_basicConfiguration_id` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_basicVAPconfigTable`;
CREATE TABLE IF NOT EXISTS `ap25_basicVAPconfigTable` (
  `ap25_basicVAPconfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned NOT NULL,
  `vapselection_id` int(10) unsigned NOT NULL,
  `vapESSID` varchar(32) DEFAULT NULL,
  `vapHiddenESSIDstate` smallint(6) DEFAULT NULL,
  `vapRTSthresholdValue` smallint(6) DEFAULT NULL,
  `vapFragmentationThresholdValue` smallint(6) DEFAULT NULL,
  `vapBeaconInterval` smallint(6) DEFAULT NULL,
  `vlanId` int(10) DEFAULT NULL,
  `vlanPriority` int(10) DEFAULT NULL,
  `vapMode` int(10) DEFAULT NULL,
  `vapSecurityMode` smallint(6) DEFAULT NULL,
  `vapRadioMac` varchar(20) NOT NULL,
  PRIMARY KEY (`ap25_basicVAPconfigTable_id`),
  KEY `FK_ap25_basicVAPsetup` (`vapselection_id`),
  KEY `FK_basicVAPsetup_config` (`config_profile_id`),
  KEY `ap25_basicVAPsetup_ibfk_2` (`vapselection_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_basicVAPsecurity`;
CREATE TABLE IF NOT EXISTS `ap25_basicVAPsecurity` (
  `ap25_basicVAPsecurity_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned NOT NULL,
  `vapselection_id` int(10) unsigned DEFAULT NULL,
  `vapSecurityMode` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`ap25_basicVAPsecurity_id`),
  KEY `FK_ap25_basicVAPsecurity_id` (`vapselection_id`),
  KEY `FK_basicVAPsecurity_config` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_dhcpServer`;
CREATE TABLE IF NOT EXISTS `ap25_dhcpServer` (
  `ap25_dhcpServer_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned NOT NULL,
  `dhcpServerStatus` tinyint(4) DEFAULT NULL,
  `dhcpStartIPaddress` varchar(16) DEFAULT NULL,
  `dhcpEndIPaddress` varchar(16) DEFAULT NULL,
  `dhcpSubnetMask` varchar(16) DEFAULT NULL,
  `dhcpClientLeaseTime` int(8) unsigned DEFAULT NULL,
  PRIMARY KEY (`ap25_dhcpServer_id`),
  KEY `ap25_dhcpServer_id` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 ;

DROP TABLE IF EXISTS `ap25_oids`;
CREATE TABLE IF NOT EXISTS `ap25_oids` (
  `oid_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_type_id` varchar(16) DEFAULT NULL,
  `oid` varchar(256) DEFAULT NULL,
  `oid_name` varchar(256) DEFAULT NULL,
  `oid_type` varchar(16) DEFAULT NULL,
  `access` smallint(6) DEFAULT NULL,
  `default_value` varchar(256) DEFAULT NULL,
  `min_value` varchar(128) DEFAULT NULL,
  `max_value` varchar(256) DEFAULT NULL,
  `indexes` varchar(256) DEFAULT NULL,
  `dependent_id` int(10) unsigned DEFAULT NULL,
  `multivalue` smallint(6) DEFAULT '0',
  `table_name` varchar(128) DEFAULT NULL,
  `coloumn_name` varchar(128) DEFAULT NULL,
  `indexes_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`oid_id`),
  KEY `FK_oids` (`device_type_id`),
  KEY `FK_oids_dependant_id` (`dependent_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_oids_multivalues`;
CREATE TABLE IF NOT EXISTS `ap25_oids_multivalues` (
  `oids_multivalue_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `oid_id` int(10) unsigned DEFAULT NULL,
  `value` varchar(128) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`oids_multivalue_id`),
  KEY `FK_oids_multivalues` (`oid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_oid_table`;
CREATE TABLE IF NOT EXISTS `ap25_oid_table` (
  `table_name` varchar(64) NOT NULL,
  `table_oid` varchar(64) NOT NULL,
  `varbinds` tinyint(4) NOT NULL DEFAULT '15',
  `is_recon` int(11) NOT NULL DEFAULT '1' COMMENT '1 = run reconciliation for table',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '0 = reconciliation has not been run',
  `isNode` tinyint(10) NOT NULL DEFAULT '1',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_radioSelection`;
CREATE TABLE IF NOT EXISTS `ap25_radioSelection` (
  `ap25_radioSelection_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `radio` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ap25_radioSelection_id`),
  KEY `FK_ap25_radioSelection_id` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_radioSetup`;
CREATE TABLE IF NOT EXISTS `ap25_radioSetup` (
  `ap25_radioSetup_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `radioState` smallint(6) DEFAULT NULL,
  `radioAPmode` smallint(6) DEFAULT NULL,
  `radioManagementVLANstate` smallint(6) DEFAULT NULL,
  `radioCountryCode` int(10) NOT NULL,
  `numberOfVAPs` smallint(6) DEFAULT NULL,
  `radioChannel` smallint(6) DEFAULT NULL,
  `wifiMode` smallint(6) DEFAULT NULL,
  `radioTxPower` smallint(6) DEFAULT NULL,
  `radioGatingIndex` smallint(6) DEFAULT NULL,
  `radioAggregation` smallint(6) DEFAULT NULL,
  `radioAggFrames` int(32) DEFAULT NULL,
  `radioAggSize` int(32) DEFAULT NULL,
  `radioAggMinSize` int(32) DEFAULT NULL,
  `radioChannelWidth` smallint(6) DEFAULT NULL,
  `radioTXChainMask` smallint(6) DEFAULT NULL,
  `radioRXChainMask` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`ap25_radioSetup_id`),
  KEY `FK_ap25_radioSetup_id` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_services`;
CREATE TABLE IF NOT EXISTS `ap25_services` (
  `ap25_services_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `upnpServerStatus` smallint(6) DEFAULT NULL,
  `systemLogStatus` smallint(6) DEFAULT NULL,
  `systemLogIP` varchar(16) DEFAULT NULL,
  `systemLogPort` int(4) DEFAULT NULL,
  `systemTime` varchar(31) DEFAULT NULL,
  PRIMARY KEY (`ap25_services_id`),
  KEY `FK_ap25_services` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_statisticsTable`;
CREATE TABLE IF NOT EXISTS `ap25_statisticsTable` (
  `ap25_systemInfo_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned NOT NULL,
  `index` int(11) NOT NULL,
  `statisticsInterface` varchar(30) NOT NULL,
  `statisticsRxPackets` int(10) unsigned NOT NULL,
  `statisticsTxPackets` int(10) unsigned NOT NULL,
  `statisticsRxError` int(10) unsigned NOT NULL,
  `statisticsTxError` int(10) unsigned NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`ap25_systemInfo_id`,`timestamp`),
  KEY `FK_ap25_systemInfo_id` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_vapClientStatisticsTable`;
CREATE TABLE IF NOT EXISTS `ap25_vapClientStatisticsTable` (
  `ap25_vapClientStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `vap_id` tinyint(4) NOT NULL DEFAULT '1',
  `slNum` int(16) unsigned DEFAULT NULL,
  `addressMAC` varchar(18) DEFAULT NULL,
  `aid` int(32) DEFAULT NULL,
  `chan` int(32) DEFAULT NULL,
  `txRate` varchar(11) DEFAULT NULL,
  `rxRate` varchar(11) DEFAULT NULL,
  `rssi` int(32) DEFAULT NULL,
  `idle` int(32) DEFAULT NULL,
  `txSEQ` int(32) DEFAULT NULL,
  `rxSEQ` int(32) DEFAULT NULL,
  `caps` varchar(11) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`ap25_vapClientStatisticsTable_id`,`timestamp`),
  KEY `FK_ap25_vapClientStatisticsTable_id` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_vapSelection`;
CREATE TABLE IF NOT EXISTS `ap25_vapSelection` (
  `ap25_vapSelection_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `totalVAPsPresent` int(10) DEFAULT NULL,
  `selectVap` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`ap25_vapSelection_id`),
  KEY `FK_ap25_vapSelection_id` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_vapWEPsecurityConfigTable`;
CREATE TABLE IF NOT EXISTS `ap25_vapWEPsecurityConfigTable` (
  `ap25_vapWEPsecurityConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned NOT NULL,
  `basicVAPconfigIndex` int(10) unsigned DEFAULT NULL,
  `vapWEPmode` smallint(6) DEFAULT NULL,
  `vapWEPprimaryKey` smallint(6) DEFAULT NULL,
  `vapWEPkey1` varchar(22) DEFAULT NULL,
  `vapWEPkey2` varchar(22) DEFAULT NULL,
  `vapWEPkey3` varchar(22) DEFAULT NULL,
  `vapWEPkey4` varchar(22) DEFAULT NULL,
  PRIMARY KEY (`ap25_vapWEPsecurityConfigTable_id`),
  KEY `FK_ap25_vapWEPsecuritySetup_id` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_vapWPAsecurityConfigTable`;
CREATE TABLE IF NOT EXISTS `ap25_vapWPAsecurityConfigTable` (
  `ap25_vapWPAsecurityConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned NOT NULL,
  `vapselection_id` int(10) unsigned NOT NULL,
  `vapWPAmode` smallint(6) DEFAULT NULL,
  `vapWPAcypher` smallint(6) DEFAULT NULL,
  `vapWPArekeyInterval` int(11) unsigned DEFAULT NULL,
  `vapWPAmasterReKey` int(11) unsigned DEFAULT NULL,
  `vapWEPrekeyInt` int(11) unsigned DEFAULT NULL,
  `vapWPAkeyMode` smallint(6) DEFAULT NULL,
  `vapWPAconfigPSKPassPhrase` varchar(33) DEFAULT NULL,
  `vapWPArsnPreAuth` smallint(6) DEFAULT NULL,
  `vapWPArsnPreAuthInterface` varchar(16) DEFAULT NULL,
  `vapWPAeapReAuthPeriod` int(6) unsigned DEFAULT NULL,
  `vapWPAserverIP` varchar(16) DEFAULT NULL,
  `vapWPAserverPort` int(4) DEFAULT NULL,
  `vapWPAsharedSecret` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`ap25_vapWPAsecurityConfigTable_id`),
  KEY `FK_ap25_vapWPAsecuritysetup_config` (`config_profile_id`),
  KEY `FK_vapselection_id` (`vapselection_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_versions`;
CREATE TABLE IF NOT EXISTS `ap25_versions` (
  `ap25_versions_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `hardwareVersion` varchar(15) DEFAULT NULL,
  `softwareVersion` varchar(25) DEFAULT NULL,
  `bootLoaderVersion` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`ap25_versions_id`),
  KEY `FK_ap25_versions_id` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap_client_ap_data`;
CREATE TABLE IF NOT EXISTS `ap_client_ap_data` (
  `ap_client_ap_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` int(11) unsigned NOT NULL,
  `client_id` int(11) NOT NULL,
  `client_mac` varchar(20) NOT NULL,
  `vap_id` tinyint(4) NOT NULL DEFAULT '1',
  `slNum` int(16) unsigned DEFAULT NULL,
  `aid` int(32) DEFAULT NULL,
  `chan` int(32) DEFAULT NULL,
  `txRate` varchar(11) DEFAULT NULL,
  `rxRate` varchar(11) DEFAULT NULL,
  `rssi` int(32) DEFAULT NULL,
  `idle` int(32) DEFAULT NULL,
  `total_tx` int(32) unsigned DEFAULT NULL,
  `total_rx` int(32) unsigned DEFAULT NULL,
  `caps` varchar(11) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`ap_client_ap_data_id`),
  KEY `fk_ap_client_ap_data` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap_client_details`;
CREATE TABLE IF NOT EXISTS `ap_client_details` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_name` varchar(32) NOT NULL,
  `mac` varchar(20) NOT NULL,
  `total_tx` int(10) unsigned NOT NULL,
  `total_rx` int(10) unsigned NOT NULL,
  `first_seen_time` datetime NOT NULL,
  `first_seen_ap_id` int(11) NOT NULL,
  `last_seen_time` datetime NOT NULL,
  `last_seen_ap_id` int(11) NOT NULL,
  `client_ip` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_apScanDataTable`;
CREATE TABLE IF NOT EXISTS `ap25_apScanDataTable` (
  `ap25_apScanDataTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned NOT NULL,
  `macAddress` varchar(20) NOT NULL,
  `essid` varchar(32) NOT NULL,
  `frequency` varchar(10) NOT NULL,
  `quality` varchar(10) NOT NULL,
  `signalLevel` varchar(10) NOT NULL,
  `noiseLevel` varchar(10) NOT NULL,
  `beconIntervel` varchar(10) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ap25_apScanDataTable_id`),
  KEY `host_id` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap25_dhcpClientsTable`;
CREATE TABLE IF NOT EXISTS `ap25_dhcpClientsTable` (
  `ap25_dhcpClientsTable_id` int(10) NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned NOT NULL,
  `dhcpClientsMACaddress` varchar(20) NOT NULL,
  `dhcpClientsIPaddress` varchar(16) NOT NULL,
  `dhcpClientsExpiresIn` varchar(32) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ap25_dhcpClientsTable_id`),
  KEY `ap25_dhcpClientsTable_host_id` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ;

DROP TABLE IF EXISTS `ap_connected_client`;
CREATE TABLE IF NOT EXISTS `ap_connected_client` (
  `ap_connected_client_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` int(11) unsigned NOT NULL,
  `client_id` int(11) NOT NULL,
  `client_mac` varchar(20) NOT NULL,
  `state` enum('0','1') NOT NULL COMMENT '''0'' means disconnected,''1'' means connected',
  PRIMARY KEY (`ap_connected_client_id`),
  KEY `fk_ap_connected_client` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap_scheduling`;
CREATE TABLE IF NOT EXISTS `ap_scheduling` (
  `ap_scheduling_id` varchar(64) NOT NULL,
  `event` varchar(16) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `is_repeated` smallint(6) DEFAULT NULL,
  `repeat_type` varchar(16) DEFAULT NULL,
  `sun` smallint(6) DEFAULT NULL,
  `mon` smallint(6) DEFAULT NULL,
  `tue` smallint(6) DEFAULT NULL,
  `wed` smallint(6) DEFAULT NULL,
  `thu` smallint(6) DEFAULT NULL,
  `fri` smallint(6) DEFAULT NULL,
  `sat` smallint(6) DEFAULT NULL,
  `jan` smallint(6) DEFAULT NULL,
  `feb` smallint(6) DEFAULT NULL,
  `mar` smallint(6) DEFAULT NULL,
  `apr` smallint(6) DEFAULT NULL,
  `may` smallint(6) DEFAULT NULL,
  `jun` smallint(6) DEFAULT NULL,
  `jul` smallint(6) DEFAULT NULL,
  `aug` smallint(6) DEFAULT NULL,
  `sept` smallint(6) DEFAULT NULL,
  `oct` smallint(6) DEFAULT NULL,
  `nov` smallint(6) DEFAULT NULL,
  `dece` smallint(6) DEFAULT NULL,
  `day` smallint(6) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NULL DEFAULT NULL,
  `updated_by` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`ap_scheduling_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ap_scheduling_host_mapping`;
CREATE TABLE IF NOT EXISTS `ap_scheduling_host_mapping` (
  `ap_scheduling_host_mapping_id` varchar(64) NOT NULL,
  `ap_scheduling_id` varchar(64) DEFAULT NULL,
  `host_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`ap_scheduling_host_mapping_id`),
  KEY `FK_ap_scheduling_host_mapping_scheduling` (`ap_scheduling_id`),
  KEY `FK_ap_scheduling_host_mapping_host` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `black_list_macs`;
CREATE TABLE IF NOT EXISTS `black_list_macs` (
  `black_list_mac_id` varchar(64) NOT NULL,
  `mac_address` varchar(32) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `cteation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`black_list_mac_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `ccu_ccuAlarmAndThresholdTable`
--
DROP TABLE IF EXISTS `ccu_ccuAlarmAndThresholdTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuAlarmAndThresholdTable` (
  `ccu_ccuAlarmAndThresholdTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ccuATIndex` int(10) unsigned DEFAULT NULL,
  `ccuATHighTemperatureAlarm` tinyint(3) unsigned DEFAULT NULL,
  `ccuATPSMRequest` tinyint(3) unsigned DEFAULT NULL,
  `ccuATSMPSMaxCurrentLimit` smallint(5) unsigned DEFAULT NULL,
  `ccuATPeakLoadCurrent` smallint(5) unsigned DEFAULT NULL,
  `ccuATLowVoltageDisconnectLevel` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`ccu_ccuAlarmAndThresholdTable_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;


--
-- Table structure for table `ccu_ccuAuxIOTable`
--
DROP TABLE IF EXISTS `ccu_ccuAuxIOTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuAuxIOTable` (
  `ccu_ccuAuxIOTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ccuAIIndex` int(10) DEFAULT NULL,
  `ccuAIExternalOutput1` tinyint(4) DEFAULT NULL,
  `ccuAIExternalOutput2` tinyint(4) DEFAULT NULL,
  `ccuAIExternalOutput3` tinyint(4) DEFAULT NULL,
  `ccuAIExternalInput1` tinyint(4) NOT NULL,
  `ccuAIExternalInput2` tinyint(4) NOT NULL,
  `ccuAIExternalInput3` tinyint(4) NOT NULL,
  `ccuAIExternalInput1AlarmType` tinyint(4) DEFAULT NULL,
  `ccuAIExternalInput2AlarmType` tinyint(4) DEFAULT NULL,
  `ccuAIExternalInput3AlarmType` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`ccu_ccuAuxIOTable_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ccu_ccuBatteryPanelConfigTable`
--
DROP TABLE IF EXISTS `ccu_ccuBatteryPanelConfigTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuBatteryPanelConfigTable` (
  `ccu_ccuBatteryPanelConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ccuBPCIndex` int(10) DEFAULT NULL,
  `ccuBPCSiteBatteryCapacity` smallint(6) DEFAULT NULL,
  `ccuBPCSiteSolarPanelwP` smallint(6) DEFAULT NULL,
  `ccuBPCSiteSolarPanelCount` smallint(6) DEFAULT NULL,
  `ccuBPCNewBatteryInstallationDate` varchar(13) DEFAULT NULL,
  PRIMARY KEY (`ccu_ccuBatteryPanelConfigTable_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ccu_ccuControlTable`
--
DROP TABLE IF EXISTS `ccu_ccuControlTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuControlTable` (
  `ccu_ccuControlTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ccuCTIndex` int(10) DEFAULT NULL,
  `ccuCTLoadTurnOff` smallint(6) DEFAULT NULL,
  `ccuCTSMPSCharging` tinyint(4) DEFAULT NULL,
  `ccuCTRestoreDefault` tinyint(4) DEFAULT NULL,
  `ccuCTCCUReset` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`ccu_ccuControlTable_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `ccu_ccuInformationTable`
--
DROP TABLE IF EXISTS `ccu_ccuInformationTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuInformationTable` (
  `ccu_ccuInformationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `ccuITIndex` int(10) DEFAULT NULL,
  `ccuITSiteCCUType` int(10) DEFAULT NULL,
  `ccuITCCUId` varchar(20) DEFAULT NULL,
  `ccuITSerialNumber` varchar(20) DEFAULT NULL,
  `ccuITHardwareVersion` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`ccu_ccuInformationTable_id`),
  KEY `host_id` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;

-- --------------------------------------------------------

--
-- Table structure for table `ccu_ccuNetworkConfigurationTable`
--
DROP TABLE IF EXISTS `ccu_ccuNetworkConfigurationTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuNetworkConfigurationTable` (
  `ccu_ccuNetworkConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `ccuNCIndex` int(10) DEFAULT NULL,
  `ccuNCMACAddress` varchar(20) DEFAULT NULL,
  `ccuNCCCUIP` varchar(18) DEFAULT NULL,
  `ccuNCCCUNetMask` varchar(18) DEFAULT NULL,
  `ccuNCOMCIP` varchar(18) DEFAULT NULL,
  `ccuNCDHCPAssignedIP` varchar(18) DEFAULT NULL,
  `ccuNCDHCPNetMask` varchar(18) DEFAULT NULL,
  `ccuNCDefaultGateway` varchar(18) DEFAULT NULL,
  PRIMARY KEY (`ccu_ccuNetworkConfigurationTable_id`),
  KEY `host_id` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=26 ;


--
-- Table structure for table `ccu_ccuPeerInformationTable`
--
DROP TABLE IF EXISTS `ccu_ccuPeerInformationTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuPeerInformationTable` (
  `ccu_ccuPeerInformationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ccuPIIndex` int(10) DEFAULT NULL,
  `ccuPIPeer1MACID` varchar(20) DEFAULT NULL,
  `ccuPIPeerIP1` varchar(20) NOT NULL,
  `ccuPIPeer2MACID` varchar(20) DEFAULT NULL,
  `ccuPIPeerIP2` varchar(20) NOT NULL,
  `ccuPIPeer3MACID` varchar(20) DEFAULT NULL,
  `ccuPIPeerIP3` varchar(20) NOT NULL,
  `ccuPIPeer4MACID` varchar(20) DEFAULT NULL,
  `ccuPIPeerIP4` varchar(20) NOT NULL,
  PRIMARY KEY (`ccu_ccuPeerInformationTable_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

--
-- Table structure for table `ccu_ccuRealTimeStatusTable`
--
DROP TABLE IF EXISTS `ccu_ccuRealTimeStatusTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuRealTimeStatusTable` (
  `ccu_ccuRealTimeStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `ccuRTSIndex` int(10) unsigned DEFAULT NULL,
  `ccuRTSSystemVoltage` int(10) DEFAULT NULL,
  `ccuRTSSolarCurrent` int(10) DEFAULT NULL,
  `ccuRTSSMPSCurrent` varchar(32) DEFAULT NULL,
  `ccuRTSBatteryCurrent` int(10) DEFAULT NULL,
  `ccuRTSLoadCurrent` int(10) DEFAULT NULL,
  `ccuRTSBatterySOC` int(10) DEFAULT NULL,
  `ccuRTSInternalTemperature` int(10) DEFAULT NULL,
  `ccuRTSBatteryAmbientTemperature` int(10) DEFAULT NULL,
  `ccuRTSSMPSTemperature` int(10) DEFAULT NULL,
  `ccuRTSACVoltageReading` int(10) DEFAULT NULL,
  `ccuRTSAlarmStatusByte` int(10) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`ccu_ccuRealTimeStatusTable_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ccu_ccuRealTimeStatusTable`
--


-- --------------------------------------------------------

--
-- Table structure for table `ccu_ccuSiteInformationTable`
--
DROP TABLE IF EXISTS `ccu_ccuSiteInformationTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuSiteInformationTable` (
  `ccu_ccuSiteInformationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ccuSITIndex` int(10) DEFAULT NULL,
  `ccuSITSiteName` varchar(65) DEFAULT NULL,
  PRIMARY KEY (`ccu_ccuSiteInformationTable_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 ;


--
-- Table structure for table `ccu_ccuSoftwareInformationTable`
--
DROP TABLE IF EXISTS `ccu_ccuSoftwareInformationTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuSoftwareInformationTable` (
  `ccu_ccuSoftwareInformationTable_id` int(10) NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned NOT NULL,
  `ccuSIIndex` int(32) unsigned DEFAULT NULL,
  `ccuSIActiveSoftwareVersion` varchar(20) DEFAULT NULL,
  `ccuSIBackupSoftwareVersion` varchar(20) DEFAULT NULL,
  `ccuSICommunicationProtocolVersion` varchar(20) DEFAULT NULL,
  `ccuSIBootLoaderVersion` varchar(13) NOT NULL,
  PRIMARY KEY (`ccu_ccuSoftwareInformationTable_id`),
  KEY `host_id` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 ;


-- --------------------------------------------------------

--
-- Table structure for table `ccu_ccuStatusDataTable`
--
DROP TABLE IF EXISTS `ccu_ccuStatusDataTable`;
CREATE TABLE IF NOT EXISTS `ccu_ccuStatusDataTable` (
  `ccu_ccuStatusDataTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `ccuSDIndex` int(10) unsigned DEFAULT NULL,
  `ccuSDLastRebootReason` int(10) DEFAULT NULL,
  `ccuSDUpTimeSecs` varchar(32) DEFAULT NULL,
  `ccuSDKwHReading` int(64) DEFAULT NULL,
  `ccuSDBatteryHealth` int(10) DEFAULT NULL,
  `ccuSDBatteryState` int(10) DEFAULT NULL,
  `ccuSDLoadConnectedStatus` int(10) DEFAULT NULL,
  `ccuSDACAvailability` int(10) DEFAULT NULL,
  `ccuSDExternalChargingStatus` int(10) DEFAULT NULL,
  `ccuSDChargeDischargeCycle` int(10) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`ccu_ccuStatusDataTable_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;



-- --------------------------------------------------------

--
-- Table structure for table `ccu_oids`
--
DROP TABLE IF EXISTS `ccu_oids`;
CREATE TABLE IF NOT EXISTS `ccu_oids` (
  `oid_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_type_id` varchar(16) DEFAULT NULL,
  `oid` varchar(256) DEFAULT NULL,
  `oid_name` varchar(256) DEFAULT NULL,
  `oid_type` varchar(16) DEFAULT NULL,
  `access` smallint(6) DEFAULT NULL,
  `default_value` varchar(256) DEFAULT NULL,
  `min_value` varchar(128) DEFAULT NULL,
  `max_value` varchar(256) DEFAULT NULL,
  `indexes` varchar(256) DEFAULT NULL,
  `dependent_id` int(10) unsigned DEFAULT NULL,
  `multivalue` smallint(6) DEFAULT '0',
  `table_name` varchar(128) DEFAULT NULL,
  `coloumn_name` varchar(128) DEFAULT NULL,
  `indexes_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`oid_id`),
  KEY `FK_oids` (`device_type_id`),
  KEY `FK_oids_dependant_id` (`dependent_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=111 ;


--
-- Table structure for table `ccu_oids_multivalues`
--
DROP TABLE IF EXISTS `ccu_oids_multivalues`;
CREATE TABLE IF NOT EXISTS `ccu_oids_multivalues` (
  `oids_multivalue_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `oid_id` int(10) unsigned DEFAULT NULL,
  `value` varchar(128) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`oids_multivalue_id`),
  KEY `FK_oids_multivalues` (`oid_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=56 ;


--
-- Table structure for table `ccu_oid_table`
--
DROP TABLE IF EXISTS `ccu_oid_table`;
CREATE TABLE IF NOT EXISTS `ccu_oid_table` (
  `table_name` varchar(64) NOT NULL,
  `table_oid` varchar(64) NOT NULL,
  `varbinds` tinyint(4) NOT NULL DEFAULT '15',
  `is_recon` int(11) NOT NULL DEFAULT '1' COMMENT '1 = run reconciliation for table',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '0 = reconciliation has not been run',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `cities`;
CREATE TABLE IF NOT EXISTS `cities` (
  `city_id` varchar(64) NOT NULL,
  `city_name` varchar(64) DEFAULT NULL,
  `state_id` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`city_id`),
  KEY `FK_cities_states` (`state_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `config_profiles`;
CREATE TABLE IF NOT EXISTS `config_profiles` (
  `config_profile_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_type_id` varchar(16) DEFAULT NULL,
  `profile_name` varchar(64) DEFAULT NULL,
  `config_profile_type_id` varchar(16) DEFAULT NULL,
  `parent_id` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`config_profile_id`),
  KEY `FK_odu_config_profiles_device_type` (`device_type_id`),
  KEY `FK_odu_config_profiles_type` (`config_profile_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `config_profile_type`;
CREATE TABLE IF NOT EXISTS `config_profile_type` (
  `config_profile_type_id` varchar(16) NOT NULL,
  `config_profile_type` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`config_profile_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `countries`;
CREATE TABLE IF NOT EXISTS `countries` (
  `country_id` varchar(64) NOT NULL,
  `country_name` varchar(64) DEFAULT NULL,
  `country_code` varchar(16) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `daemon_events`;
CREATE TABLE IF NOT EXISTS `daemon_events` (
  `daemon_event_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `daemon_name` varchar(16) DEFAULT NULL,
  `error_no` int(16) DEFAULT NULL,
  `state` smallint(6) DEFAULT NULL COMMENT '0 for critical, 1 for normal',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `short_description` varchar(64) DEFAULT NULL,
  `is_viewed` smallint(6) DEFAULT '0' COMMENT '0 for viewed 1 for not viewed',
  PRIMARY KEY (`daemon_event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `daemon_timestamp`;
CREATE TABLE IF NOT EXISTS `daemon_timestamp` (
  `daemon_timestamp_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `daemon_name` varchar(32) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`daemon_timestamp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `device_type`;
CREATE TABLE IF NOT EXISTS `device_type` (
  `device_type_id` varchar(16) NOT NULL,
  `device_name` varchar(64) DEFAULT NULL,
  `sdm_discovery_id` varchar(8) DEFAULT NULL,
  `sdm_discovery_value` varchar(64) DEFAULT NULL,
  `vnl_discovery_value` varchar(64) DEFAULT NULL,
  `ping_discovery_value` varchar(64) DEFAULT NULL,
  `snmp_discovery_value` varchar(64) DEFAULT NULL,
  `upnp_discovery_value` varchar(64) DEFAULT NULL,
  `icon_name` varchar(64) NOT NULL,
  `mib_name` varchar(32) DEFAULT NULL,
  `mib_path` varchar(256) DEFAULT NULL,
  `table_prefix` varchar(32) NOT NULL,
  `is_generic` smallint(6) DEFAULT '1',
  `is_deleted` smallint(6) DEFAULT '0',
  `sequence` smallint(6) DEFAULT '0',
  PRIMARY KEY (`device_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `discovered_hosts`;
CREATE TABLE IF NOT EXISTS `discovered_hosts` (
  `discovered_host_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `discovery_id` int(10) unsigned DEFAULT '0',
  `host_alias` varchar(64) DEFAULT NULL,
  `ip_address` varchar(16) DEFAULT NULL,
  `device_type_id` varchar(16) DEFAULT NULL,
  `mac_address` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`discovered_host_id`),
  KEY `FK_discovered_hosts` (`device_type_id`),
  KEY `FK_discovered_hosts_discovery` (`discovery_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `discovery`;
CREATE TABLE IF NOT EXISTS `discovery` (
  `discovery_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `discovery_type_id` varchar(64) DEFAULT NULL,
  `ip_start_range` varchar(16) DEFAULT NULL,
  `ip_end_range` varchar(16) DEFAULT NULL,
  `timeout` int(11) DEFAULT NULL,
  `snmp_community` varchar(32) DEFAULT NULL,
  `snmp_port` varchar(8) DEFAULT NULL,
  `snmp_version` varchar(8) DEFAULT NULL,
  `sdm_device_list` varchar(64) DEFAULT NULL,
  `scheduling_id` varchar(8) DEFAULT NULL,
  `service_management` varchar(16) DEFAULT NULL,
  `done_percent` int(8) NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`discovery_id`),
  KEY `FK_discovery` (`scheduling_id`),
  KEY `FK_discovery_type` (`discovery_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `discovery_type`;
CREATE TABLE IF NOT EXISTS `discovery_type` (
  `discovery_type_id` varchar(16) NOT NULL,
  `discovery_type` varchar(16) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  `sequence` smallint(6) DEFAULT '0',
  PRIMARY KEY (`discovery_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `error_description`;
CREATE TABLE IF NOT EXISTS `error_description` (
  `error_no` int(16) NOT NULL,
  `error_causes` text,
  `probable_solution` text,
  PRIMARY KEY (`error_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `event_log`;
CREATE TABLE IF NOT EXISTS `event_log` (
  `event_log_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `event_type_id` int(10) unsigned DEFAULT '0',
  `description` text NOT NULL,
  `timestamp` datetime NOT NULL,
  `level` tinyint(4) NOT NULL DEFAULT '0',
  `time_taken` varchar(20) NOT NULL,
  PRIMARY KEY (`event_log_id`,`timestamp`),
  KEY `index_event_type_id` (`event_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 ;


DROP TABLE IF EXISTS `event_type`;
CREATE TABLE IF NOT EXISTS `event_type` (
  `event_type_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_name` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`event_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `firmware_list_table`;
CREATE TABLE IF NOT EXISTS `firmware_list_table` (
  `firmware_list_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_type` varchar(10) DEFAULT NULL,
  `firmware_file_name` varchar(50) DEFAULT NULL,
  `firmware_file_path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`firmware_list_table_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_ap25_bandwidth`;
CREATE TABLE IF NOT EXISTS `get_ap25_bandwidth` (
  `get_ap25_bandwidth_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `interface` varchar(16) DEFAULT NULL,
  `tx` int(10) unsigned DEFAULT NULL,
  `rx` int(10) unsigned DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`get_ap25_bandwidth_id`),
  KEY `FK_get_ap25_bandwidth_hosts` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_ap25_connected_user`;
CREATE TABLE IF NOT EXISTS `get_ap25_connected_user` (
  `get_ap25_connected_user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `user_mac_address` varchar(24) DEFAULT NULL,
  `vap` smallint(6) DEFAULT NULL,
  `tx` int(10) unsigned DEFAULT NULL,
  `rx` int(10) unsigned DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`get_ap25_connected_user_id`),
  KEY `FK_get_ap25_connected_user_hosts` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_ap25_misc`;
CREATE TABLE IF NOT EXISTS `get_ap25_misc` (
  `get_ap25_misc_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `sys_up_time` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`get_ap25_misc_id`),
  KEY `FK_get_ap25_misc` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_active_alarm_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_active_alarm_table` (
  `get_odu16_active_alarm_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `trap_timestamp` int(10) unsigned DEFAULT NULL,
  `perceived_severity` smallint(6) DEFAULT NULL,
  `event_type` int(32) DEFAULT NULL,
  `event_id` varchar(32) DEFAULT NULL,
  `managed_object_type` int(32) DEFAULT NULL,
  `managed_object_id` varchar(32) DEFAULT NULL,
  `component_type` int(32) DEFAULT NULL,
  `component_id` varchar(32) DEFAULT NULL,
  `event_desc` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_active_alarm_table_id`),
  KEY `FK_get_odu16_active_alarm_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_hw_desc_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_hw_desc_table` (
  `get_odu16_hw_desc_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `hw_version` varchar(128) DEFAULT NULL,
  `hw_serial_no` varbinary(64) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_hw_desc_table_id`),
  KEY `FK_get_odu16_hw_desc_table` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_misc`;
CREATE TABLE IF NOT EXISTS `get_odu16_misc` (
  `get_odu16_misc_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `sys_descr` varchar(256) DEFAULT NULL,
  `sys_object_id` varchar(32) DEFAULT NULL,
  `sys_up_time` varchar(64) DEFAULT NULL,
  `sys_services` int(32) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_misc_id`),
  KEY `FK_get_odu16_misc` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_network_interface_status_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_network_interface_status_table` (
  `get_odu16_network_interface_status_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `name` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_network_interface_status_table_id`),
  KEY `FK_get_odu16_network_interface_status_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_nw_interface_statistics_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_nw_interface_statistics_table` (
  `get_odu16_nw_interface_statistics_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `index` smallint(6) DEFAULT NULL,
  `rx_packets` int(10) unsigned DEFAULT '0',
  `tx_packets` int(10) unsigned DEFAULT '0',
  `rx_bytes` int(10) unsigned DEFAULT '0',
  `tx_bytes` int(10) unsigned DEFAULT '0',
  `rx_errors` int(10) unsigned DEFAULT '0',
  `tx_errors` int(10) unsigned DEFAULT '0',
  `rx_dropped` int(10) unsigned DEFAULT '0',
  `tx_dropped` int(10) unsigned DEFAULT '0',
  `rx_multicast` int(10) unsigned DEFAULT '0',
  `colisions` int(10) unsigned DEFAULT '0',
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`get_odu16_nw_interface_statistics_table_id`,`timestamp`),
  KEY `FK_get_odu16_nw_interface_statistics_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_nw_interface_status_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_nw_interface_status_table` (
  `get_odu16_nw_interface_status_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `nw_interface_name` varchar(16) DEFAULT NULL,
  `operational_state` smallint(6) DEFAULT NULL,
  `mac_address` varchar(24) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_nw_interface_status_table_id`),
  KEY `FK_get_odu16_nw_interface_status_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_peer_link_statistics_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_peer_link_statistics_table` (
  `get_odu16_peer_link_statistics_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `rx_packet` int(10) unsigned DEFAULT '0',
  `tx_packet` int(10) unsigned DEFAULT '0',
  `rx_succ_bytes` int(10) unsigned DEFAULT '0',
  `tx_succ_bytes` int(10) unsigned DEFAULT '0',
  `rx_droped` int(10) unsigned DEFAULT '0',
  `tx_droped` int(10) unsigned DEFAULT '0',
  `rx_discovery` int(10) unsigned DEFAULT '0',
  `tx_discovery` int(10) unsigned DEFAULT '0',
  `rx_arqs` int(10) unsigned DEFAULT '0',
  `tx_arqs` int(10) unsigned DEFAULT '0',
  `rx_retransmissions` int(10) unsigned DEFAULT '0',
  `tx_transmissions` int(10) unsigned DEFAULT '0',
  `rx_data_frames` int(10) unsigned DEFAULT '0',
  `tx_data_frames` int(10) unsigned DEFAULT '0',
  `rx_link_frames` int(10) unsigned DEFAULT '0',
  `tx_link_frames` int(10) unsigned DEFAULT '0',
  `rx_lost_data_frames` int(10) unsigned DEFAULT '0',
  `rx_lost_link_frames` int(10) unsigned DEFAULT '0',
  `peer_link_statistics_signal_strength` int(10) DEFAULT '0',
  `tx_retransmissions_arq5` int(10) unsigned DEFAULT '0',
  `tx_retransmissions_arq4` int(10) unsigned DEFAULT '0',
  `tx_retransmissions_arq3` int(10) unsigned DEFAULT '0',
  `tx_retransmissions_arq2` int(10) unsigned DEFAULT '0',
  `tx_retransmissions_arq1` int(10) unsigned DEFAULT '0',
  `tx_retransmissions_arq0` int(10) unsigned DEFAULT '0',
  `rx_retransmissions_arq5` int(10) unsigned DEFAULT '0',
  `rx_retransmissions_arq4` int(10) unsigned DEFAULT '0',
  `rx_retransmissions_arq3` int(10) unsigned DEFAULT '0',
  `rx_retransmissions_arq2` int(10) unsigned DEFAULT '0',
  `rx_retransmissions_arq1` int(10) unsigned DEFAULT '0',
  `rx_retransmissions_arq0` int(10) unsigned DEFAULT '0',
  `rx_arq_not_handled` int(10) unsigned DEFAULT '0',
  `tx_retransmission_arq` int(10) unsigned DEFAULT '0',
  `tx_retransmission_no_frame` int(10) unsigned DEFAULT '0',
  `tx_available_throughput` int(10) unsigned DEFAULT '0',
  `rx_duplicated` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`get_odu16_peer_link_statistics_table_id`),
  KEY `FK_get_odu16_peer_link_statistics_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_peer_node_status_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_peer_node_status_table` (
  `get_odu16_peer_node_status_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `index` smallint(6) DEFAULT NULL,
  `timeslot_index` smallint(6) DEFAULT NULL,
  `link_status` varchar(16) DEFAULT NULL,
  `tunnel_status` varchar(16) DEFAULT NULL,
  `sig_strength` int(10) DEFAULT NULL,
  `peer_mac_addr` varchar(24) DEFAULT NULL,
  `ssidentifier` varchar(32) DEFAULT NULL,
  `peer_node_status_raster_time` int(10) unsigned DEFAULT '0',
  `peer_node_status_num_slaves` int(10) unsigned DEFAULT '0',
  `peer_node_status_timer_adjust` int(10) unsigned DEFAULT '0',
  `peer_node_status_rf_config` varchar(16) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`get_odu16_peer_node_status_table_id`,`timestamp`),
  KEY `FK_get_odu16_peer_node_status_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_peer_tunnel_statistics_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_peer_tunnel_statistics_table` (
  `get_odu16_peer_tunnel_statistics_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `rx_packet` int(10) unsigned DEFAULT '0',
  `tx_packet` int(10) unsigned DEFAULT '0',
  `rx_success_bytes` int(10) unsigned DEFAULT '0',
  `tx_success_bytes` int(10) unsigned DEFAULT '0',
  `rx_bundles` int(10) unsigned DEFAULT '0',
  `tx_bundles` int(10) unsigned DEFAULT '0',
  `rx_fragmented_frames` int(10) unsigned DEFAULT '0',
  `tx_fragmented_frames` int(10) unsigned DEFAULT '0',
  `rx_fragments` int(10) unsigned DEFAULT '0',
  `tx_fragments` int(10) unsigned DEFAULT '0',
  `rx_droped` int(10) unsigned DEFAULT '0',
  `tx_droped` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`get_odu16_peer_tunnel_statistics_table_id`),
  KEY `FK_get_odu16_peer_tunnel_statistics_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ra_channel_list_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_ra_channel_list_table` (
  `get_odu16_ra_channel_list_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `channel_number` int(10) unsigned DEFAULT NULL,
  `frequency` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`get_odu16_ra_channel_list_table_id`),
  KEY `FK_get_odu16_ra_channel_list_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ra_conf_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_ra_conf_table` (
  `get_odu16_ra_conf_table_id` varchar(64) NOT NULL,
  `host_id` int(10) unsigned DEFAULT NULL,
  `ra_operational_state` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_ra_conf_table_id`),
  KEY `FK_get_odu16_ra_conf_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ra_scan_list_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_ra_scan_list_table` (
  `get_odu16_ra_scan_list_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `ssid` varchar(32) DEFAULT NULL,
  `signal_strength` int(10) DEFAULT '0',
  `mac_addr` varchar(24) DEFAULT NULL,
  `raster_time` int(10) unsigned DEFAULT '0',
  `timeslot` int(10) unsigned DEFAULT '0',
  `max_slaves` int(10) unsigned DEFAULT '0',
  `rf_coding` smallint(6) DEFAULT NULL,
  `channel_num` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`get_odu16_ra_scan_list_table_id`),
  KEY `FK_get_odu16_ra_scan_list_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ra_status_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_ra_status_table` (
  `get_odu16_ra_status_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `current_timeslot` int(10) unsigned DEFAULT '0',
  `ra_mac_address` varchar(24) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_ra_status_table_id`),
  KEY `FK_get_odu16_ra_status_table` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ra_tdd_mac_statistics_entry`;
CREATE TABLE IF NOT EXISTS `get_odu16_ra_tdd_mac_statistics_entry` (
  `get_odu16_ra_tdd_mac_statistics_entry_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `index` int(10) unsigned DEFAULT '0',
  `rx_packets` int(10) unsigned DEFAULT '0',
  `tx_packets` int(10) unsigned DEFAULT '0',
  `rx_bytes` int(10) unsigned DEFAULT '0',
  `tx_bytes` int(10) unsigned DEFAULT '0',
  `rx_errors` int(10) unsigned DEFAULT '0',
  `tx_errors` int(10) unsigned DEFAULT '0',
  `rx_dropped` int(10) unsigned DEFAULT '0',
  `tx_dropped` int(10) unsigned DEFAULT '0',
  `rx_crc_errors` int(10) unsigned DEFAULT '0',
  `rx_phy_error` int(10) unsigned DEFAULT '0',
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`get_odu16_ra_tdd_mac_statistics_entry_id`,`timestamp`),
  KEY `FK_get_odu16_ra_tdd_mac_statistics_entry` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ra_tdd_mac_status_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_ra_tdd_mac_status_table` (
  `get_odu16_ra_tdd_mac_status_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `rf_chan_freq` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`get_odu16_ra_tdd_mac_status_table_id`),
  KEY `FK_get_odu16_ra_tdd_mac_status_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ru_conf_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_ru_conf_table` (
  `get_odu16_ru_conf_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `op_state` smallint(6) DEFAULT NULL,
  `object_model_version` varchar(32) DEFAULT NULL,
  `default_node_type` smallint(6) DEFAULT NULL,
  `no_radio_interfaces` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_ru_conf_table_id`),
  KEY `FK_get_odu16_ru_conf_table` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ru_om_operations_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_ru_om_operations_table` (
  `get_odu16_ru_om_operations_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `om_operation_result` smallint(6) DEFAULT NULL,
  `om_specific_cause` int(32) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_ru_om_operations_table_id`),
  KEY `FK_get_odu16_ru_om_operations_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_ru_status_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_ru_status_table` (
  `get_odu16_ru_status_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `last_reboot_reason` int(10) unsigned DEFAULT NULL,
  `is_config_commited_to_flash` smallint(6) DEFAULT NULL,
  `up_time` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`get_odu16_ru_status_table_id`),
  KEY `FK_get_odu16_ru_status_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_snmp`;
CREATE TABLE IF NOT EXISTS `get_odu16_snmp` (
  `get_odu16_snmp_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `snmp_in_pkts` int(10) unsigned DEFAULT NULL,
  `snmp_out_pkts` int(10) unsigned DEFAULT NULL,
  `snmp_in_bad_versions` int(10) unsigned DEFAULT NULL,
  `snmp_in_bad_community_names` int(10) unsigned DEFAULT NULL,
  `snmp_in_bad_community_uses` int(10) unsigned DEFAULT NULL,
  `snmp_in_asn_parse_errs` int(10) unsigned DEFAULT NULL,
  `snmp_in_too_bigs` int(10) unsigned DEFAULT NULL,
  `snmp_in_no_such_names` int(10) unsigned DEFAULT NULL,
  `snmp_in_bad_values` int(10) unsigned DEFAULT NULL,
  `snmp_in_read_onlys` int(10) unsigned DEFAULT NULL,
  `snmp_in_gen_errs` int(10) unsigned DEFAULT NULL,
  `snmp_in_total_req_vars` int(10) unsigned DEFAULT NULL,
  `snmp_in_total_set_vars` int(10) unsigned DEFAULT NULL,
  `snmp_in_get_requests` int(10) unsigned DEFAULT NULL,
  `snmp_in_get_nexts` int(10) unsigned DEFAULT NULL,
  `snmp_in_set_requests` int(10) unsigned DEFAULT NULL,
  `snmp_in_get_responses` int(10) unsigned DEFAULT NULL,
  `snmp_in_traps` int(10) unsigned DEFAULT NULL,
  `snmp_out_too_bigs` int(10) unsigned DEFAULT NULL,
  `snmp_out_no_such_names` int(10) unsigned DEFAULT NULL,
  `snmp_out_bad_values` int(10) unsigned DEFAULT NULL,
  `snmp_out_gen_errs` int(10) unsigned DEFAULT NULL,
  `snmp_out_get_requests` int(10) unsigned DEFAULT NULL,
  `snmp_out_get_nexts` int(10) unsigned DEFAULT NULL,
  `snmp_out_set_requests` int(10) unsigned DEFAULT NULL,
  `snmp_out_get_responses` int(10) unsigned DEFAULT NULL,
  `snmp_out_traps` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`get_odu16_snmp_id`),
  KEY `FK_get_odu16_snmp` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_sw_status_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_sw_status_table` (
  `get_odu16_sw_status_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `active_version` varchar(32) DEFAULT NULL,
  `passive_version` varchar(32) DEFAULT NULL,
  `bootloader_version` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_sw_status_table_id`),
  KEY `FK_get_odu16_sw_status_table` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_synch_statistics_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_synch_statistics_table` (
  `get_odu16_synch_statistics_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `index` smallint(6) DEFAULT NULL,
  `sysc_lost_counter` int(10) unsigned DEFAULT '0',
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`get_odu16_synch_statistics_table_id`,`timestamp`),
  KEY `FK_get_odu16_synch_statistics_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `get_odu16_sync_config_table`;
CREATE TABLE IF NOT EXISTS `get_odu16_sync_config_table` (
  `get_odu16_sync_config_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `synch_state` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`get_odu16_sync_config_table_id`),
  KEY `FK_get_odu16_sync_config_table` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `graph_ajax_call_information`;
CREATE TABLE IF NOT EXISTS `graph_ajax_call_information` (
  `user_id` varchar(64) NOT NULL,
  `graph_id` varchar(64) NOT NULL,
  `url` varchar(128) NOT NULL,
  `method` varchar(32) NOT NULL,
  `other_data` varchar(128) NOT NULL,
  KEY `graph_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `graph_calculation_table`;
CREATE TABLE IF NOT EXISTS `graph_calculation_table` (
  `user_id` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL,
  `graph_cal_id` tinyint(5) NOT NULL,
  `graph_cal_name` varchar(32) NOT NULL,
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `graph_field_table`;
CREATE TABLE IF NOT EXISTS `graph_field_table` (
  `user_id` varchar(64) NOT NULL,
  `graph_name` varchar(64) NOT NULL,
  `graph_field_value` varchar(64) NOT NULL,
  `graph_field_display_name` varchar(32) NOT NULL,
  `is_checked` smallint(2) NOT NULL,
  `tool_tip_title` varchar(64) NOT NULL,
  KEY `graph_name` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `graph_interface_table`;
CREATE TABLE IF NOT EXISTS `graph_interface_table` (
  `user_id` varchar(64) NOT NULL,
  `graph_name` varchar(64) NOT NULL,
  `interface_value` smallint(3) NOT NULL,
  `interface_display_name` varchar(32) NOT NULL,
  `is_selected` smallint(2) NOT NULL,
  KEY `graph_name` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `graph_templet_table`;
CREATE TABLE IF NOT EXISTS `graph_templet_table` (
  `graph_display_id` varchar(64) NOT NULL,
  `graph_display_name` varchar(256) NOT NULL,
  `user_id` varchar(64) NOT NULL,
  `is_disabled` smallint(2) NOT NULL,
  `device_type_id` varchar(64) NOT NULL,
  `graph_id` smallint(5) NOT NULL,
  `graph_tab_option` smallint(2) NOT NULL,
  `refresh_button` smallint(2) NOT NULL,
  `next_pre_option` smallint(2) NOT NULL,
  `start_value` smallint(5) NOT NULL,
  `end_value` smallint(5) NOT NULL,
  `graph_width` smallint(5) NOT NULL,
  `graph_height` smallint(5) NOT NULL,
  `graph_cal_id` int(10) NOT NULL,
  `show_type` tinyint(2) NOT NULL,
  `show_field` tinyint(2) NOT NULL,
  `show_cal_type` tinyint(2) NOT NULL,
  `show_tab_option` tinyint(2) NOT NULL,
  `graph_title` varchar(128) NOT NULL,
  `graph_subtitle` varchar(128) NOT NULL,
  `auto_refresh_time_second` int(10) NOT NULL,
  `is_deleted` smallint(2) NOT NULL,
  `dashboard_type` tinyint(5) NOT NULL DEFAULT '0',
  PRIMARY KEY (`graph_display_id`,`user_id`),
  KEY `FK_user_id` (`user_id`),
  KEY `FK_graph_id` (`graph_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `graph_type`;
CREATE TABLE IF NOT EXISTS `graph_type` (
  `graph_id` smallint(5) NOT NULL AUTO_INCREMENT,
  `graph_name` varchar(20) NOT NULL,
  `graph_type` varchar(20) NOT NULL,
  PRIMARY KEY (`graph_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `groups`;
CREATE TABLE IF NOT EXISTS `groups` (
  `group_id` varchar(64) NOT NULL,
  `group_name` varchar(64) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `updated_by` varchar(64) DEFAULT NULL,
  `role_id` varchar(64) DEFAULT NULL,
  `is_default` smallint(6) DEFAULT '0',
  PRIMARY KEY (`group_id`),
  KEY `FK_groups` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `historical_info`;
CREATE TABLE IF NOT EXISTS `historical_info` (
  `historical_info_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(64) NOT NULL,
  `user_name` varchar(64) NOT NULL,
  `database_name` varchar(64) NOT NULL,
  `year_month` varchar(15) NOT NULL,
  `start_time` datetime NOT NULL,
  `status` tinyint(4) NOT NULL,
  `last_access_time` datetime NOT NULL,
  PRIMARY KEY (`historical_info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `hostgroups`;
CREATE TABLE IF NOT EXISTS `hostgroups` (
  `hostgroup_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hostgroup_name` varchar(64) DEFAULT NULL,
  `hostgroup_alias` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `updated_by` varchar(64) DEFAULT NULL,
  `is_default` smallint(6) DEFAULT '0',
  PRIMARY KEY (`hostgroup_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `hostgroups_groups`;
CREATE TABLE IF NOT EXISTS `hostgroups_groups` (
  `hostgroup_group_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hostgroup_id` int(10) unsigned DEFAULT NULL,
  `group_id` varchar(64) NOT NULL,
  PRIMARY KEY (`hostgroup_group_id`),
  KEY `FK_hostgroups_groups_groups` (`group_id`),
  KEY `FK_hostgroups_groups_hostgroups` (`hostgroup_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `firmware_mapping`;
CREATE TABLE IF NOT EXISTS `firmware_mapping` (
  `firmware_mapping_id` varchar(16) NOT NULL,
  `device_type_id` varchar(16) DEFAULT NULL,
  `firmware_desc` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`firmware_mapping_id`),
  KEY `FK_firmware_mapping` (`device_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `hosts`;
CREATE TABLE IF NOT EXISTS `hosts` (
  `host_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_name` varchar(64) DEFAULT NULL,
  `host_alias` varchar(64) DEFAULT NULL,
  `ip_address` varchar(16) DEFAULT NULL,
  `mac_address` varchar(20) DEFAULT NULL,
  `device_type_id` varchar(16) DEFAULT NULL,
  `netmask` varchar(32) DEFAULT NULL,
  `gateway` varchar(32) DEFAULT NULL,
  `primary_dns` varchar(32) DEFAULT NULL,
  `secondary_dns` varchar(32) DEFAULT NULL,
  `dns_state` varchar(16) DEFAULT NULL,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL COMMENT 'Who Created this Host',
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'Date Of Creation',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `updated_by` varchar(64) DEFAULT NULL,
  `ne_id` int(10) unsigned DEFAULT NULL,
  `site_id` int(10) unsigned DEFAULT NULL,
  `host_state_id` char(1) DEFAULT 'd',
  `priority_id` varchar(16) DEFAULT NULL,
  `host_vendor_id` int(10) unsigned DEFAULT '0',
  `host_os_id` varchar(16) DEFAULT NULL,
  `host_asset_id` int(10) unsigned DEFAULT '0',
  `http_username` varchar(64) DEFAULT NULL,
  `http_password` varchar(64) DEFAULT NULL,
  `http_port` varchar(8) DEFAULT NULL,
  `snmp_read_community` varchar(32) DEFAULT NULL,
  `snmp_write_community` varchar(32) DEFAULT NULL,
  `snmp_port` varchar(8) DEFAULT NULL,
  `snmp_trap_port` varchar(8) DEFAULT NULL,
  `snmp_version_id` varchar(8) DEFAULT NULL,
  `comment` varchar(256) DEFAULT NULL,
  `nms_id` varchar(64) DEFAULT NULL,
  `parent_name` int(10) unsigned DEFAULT '0',
  `lock_status` char(8) NOT NULL DEFAULT 'f',
  `is_localhost` smallint(6) NOT NULL DEFAULT '0',
  `reconcile_health` smallint(6) NOT NULL DEFAULT '0',
  `reconcile_status` smallint(6) NOT NULL DEFAULT '0',
  `ssh_username` varchar(64) DEFAULT NULL,
  `ssh_password` varchar(64) DEFAULT NULL,
  `ssh_port` int(11) DEFAULT NULL,
  `firmware_mapping_id` varchar(16) NULL,
  PRIMARY KEY (`host_id`),
  KEY `FK_hosts` (`created_by`),
  KEY `FK_hosts_assets` (`host_asset_id`),
  KEY `FK_hosts_vendors` (`host_vendor_id`),
  KEY `FK_hosts_device_type` (`device_type_id`),
  KEY `FK_hosts_os` (`host_os_id`),
  KEY `FK_hosts_priority` (`priority_id`),
  KEY `FK_hosts_sites` (`site_id`),
  KEY `FK_hosts_states` (`host_state_id`),
  KEY `FK_hosts_nms_instance` (`nms_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `hosts_hostgroups`;
CREATE TABLE IF NOT EXISTS `hosts_hostgroups` (
  `host_hostgroup_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT '0',
  `hostgroup_id` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`host_hostgroup_id`),
  KEY `FK_hosts_hostgroups_hosts` (`host_id`),
  KEY `FK_hosts_hostgroups_hostgroups` (`hostgroup_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `host_alert_action_mapping`;
CREATE TABLE IF NOT EXISTS `host_alert_action_mapping` (
  `host_alert_action_mapping_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_alert_masking_id` int(10) unsigned DEFAULT '0',
  `acknowlegde_id` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` varchar(64) DEFAULT NULL,
  `next_scheduling` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`host_alert_action_mapping_id`),
  KEY `FK_host_alert_action_mapping` (`host_alert_masking_id`),
  KEY `FK_host_alert_action_mapping_ack` (`acknowlegde_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `host_alert_masking`;
CREATE TABLE IF NOT EXISTS `host_alert_masking` (
  `host_alert_masking_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_object_id` int(10) unsigned DEFAULT '0',
  `current_status` smallint(6) DEFAULT NULL,
  `group_id` varchar(64) DEFAULT NULL,
  `action_id` varchar(16) DEFAULT NULL,
  `scheduling_minutes` int(16) DEFAULT NULL,
  `is_repeated` smallint(6) DEFAULT NULL,
  `acknowledge_id` varchar(16) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`host_alert_masking_id`),
  KEY `FK_host_alert_masking_group_groups` (`group_id`),
  KEY `FK_host_alert_masking_ack` (`acknowledge_id`),
  KEY `FK_host_alert_masking_action` (`action_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `host_assets`;
CREATE TABLE IF NOT EXISTS `host_assets` (
  `host_asset_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `longitude` varchar(32) DEFAULT NULL,
  `latitude` varchar(32) DEFAULT NULL,
  `serial_number` varchar(32) DEFAULT NULL,
  `hardware_version` varchar(32) DEFAULT NULL,
  `firmware_update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `firmware_status` enum('0','1','2','3','4','5','6','7','10','11','12','13','14','15','16','20','21','22','23','24','25','26') NOT NULL,
  `firmware_type` varchar(10) DEFAULT NULL,
  `firmware_file_name` varchar(50) DEFAULT NULL,
  `firmware_msg` varchar(64) DEFAULT NULL,
  `firmware_file_path` varchar(50) DEFAULT NULL,
  `ra_mac` varchar(18) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`host_asset_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `host_os`;
CREATE TABLE IF NOT EXISTS `host_os` (
  `host_os_id` varchar(16) NOT NULL,
  `os_name` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `sequence` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`host_os_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `host_services`;
CREATE TABLE IF NOT EXISTS `host_services` (
  `host_service_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `service_description` varchar(64) DEFAULT NULL,
  `check_command` varchar(256) DEFAULT NULL,
  `max_check_attempts` int(8) DEFAULT NULL,
  `normal_check_interval` int(8) DEFAULT NULL,
  `retry_check_interval` int(8) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`host_service_id`),
  KEY `FK_host_services` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `host_states`;
CREATE TABLE IF NOT EXISTS `host_states` (
  `host_state_id` char(1) NOT NULL DEFAULT '',
  `state_name` varchar(32) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `sequence` smallint(6) DEFAULT '0',
  PRIMARY KEY (`host_state_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `host_status`;
CREATE TABLE IF NOT EXISTS `host_status` (
  `status_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_ip` varchar(32) NOT NULL,
  `host_id` int(10) unsigned NOT NULL,
  `status` enum('0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20') NOT NULL DEFAULT '0' COMMENT '0 ''No operation'', 1 ''firmware start download'', 2 ''firmware upgrade'', 3 ''Restore default config'', 4 ''flash commit'', 5 ''Reboot'', 6 ''site survey'', 7 ''calculate BW'', 8 ''snmp uptime plugin'', 9 ''walk plugin'', 10 ''reconciliation'', 11 ''local reconciliation'', 12 ''',
  `plugin_status` tinyint(4) NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`status_id`),
  KEY `host_status_host_id` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `host_vendor`;
CREATE TABLE IF NOT EXISTS `host_vendor` (
  `host_vendor_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `vendor_name` varchar(64) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`host_vendor_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_aclportTable`;
CREATE TABLE IF NOT EXISTS `idu_aclportTable` (
  `idu_aclportTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `aclportnum` int(8) DEFAULT NULL,
  `aclindex` int(10) unsigned DEFAULT NULL,
  `aclmacaddress` varchar(32) DEFAULT NULL,
  `portrowstatus` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_aclportTable_id`),
  KEY `FK_idu_aclportTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_alarmOutConfigTable`;
CREATE TABLE IF NOT EXISTS `idu_alarmOutConfigTable` (
  `idu_alarmOutConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `alarmOutPin` int(8) DEFAULT NULL,
  `alarmPinState` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_alarmOutConfigTable_id`),
  KEY `FK_idu_alarmOutConfigTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_alarmPortConfigurationTable`;
CREATE TABLE IF NOT EXISTS `idu_alarmPortConfigurationTable` (
  `idu_alarmPortConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `alarmPin` int(8) DEFAULT NULL,
  `alarmAdminStatus` int(8) DEFAULT NULL,
  `alarmString` varchar(256) DEFAULT NULL,
  `alarmLevel` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_alarmPortConfigurationTable_id`),
  KEY `FK_idu_alarmPortConfigurationTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_atuconfigTable`;
CREATE TABLE IF NOT EXISTS `idu_atuconfigTable` (
  `idu_atuconfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `atuid` int(10) unsigned DEFAULT NULL,
  `atustate` int(8) DEFAULT NULL,
  `entrytype` int(8) DEFAULT NULL,
  `priority` int(10) unsigned DEFAULT NULL,
  `macaddress` varchar(32) DEFAULT NULL,
  `atumemberports` int(32) DEFAULT NULL,
  PRIMARY KEY (`idu_atuconfigTable_id`),
  KEY `FK_idu_atuconfigTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_e1PortConfigurationTable`;
CREATE TABLE IF NOT EXISTS `idu_e1PortConfigurationTable` (
  `idu_e1PortConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `portNumber` int(32) DEFAULT NULL,
  `adminState` int(8) DEFAULT NULL,
  `clockSource` int(8) DEFAULT NULL,
  `lineType` int(8) DEFAULT NULL,
  `lineCode` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_e1PortConfigurationTable_id`),
  KEY `FK_idu_e1PortConfigurationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_e1PortStatusTable`;
CREATE TABLE IF NOT EXISTS `idu_e1PortStatusTable` (
  `idu_e1PortStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `portNum` int(32) DEFAULT NULL,
  `opStatus` int(8) DEFAULT NULL,
  `los` int(8) DEFAULT NULL,
  `lof` int(8) DEFAULT NULL,
  `ais` int(8) DEFAULT NULL,
  `rai` int(8) DEFAULT NULL,
  `rxFrameSlip` int(8) DEFAULT NULL,
  `txFrameSlip` int(8) DEFAULT NULL,
  `bpv` int(32) DEFAULT NULL,
  `adptClkState` int(8) DEFAULT NULL,
  `holdOverStatus` int(8) DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`idu_e1PortStatusTable_id`,`timestamp`),
  KEY `FK_idu_e1PortStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_iduAdminStateTable`;
CREATE TABLE IF NOT EXISTS `idu_iduAdminStateTable` (
  `idu_iduAdminStateTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `stateId` int(32) DEFAULT NULL,
  `adminstate` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`idu_iduAdminStateTable_id`),
  KEY `FK_idu_iduAdminStateTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_iduInfoTable`;
CREATE TABLE IF NOT EXISTS `idu_iduInfoTable` (
  `idu_iduInfoTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `infoIndex` int(32) DEFAULT NULL,
  `hwSerialNumber` varchar(32) DEFAULT NULL,
  `hwType` smallint(6) DEFAULT NULL,
  `hwConfigE1` smallint(6) DEFAULT NULL,
  `hwConfigEth` smallint(6) DEFAULT NULL,
  `hwConfigAlarm` smallint(6) DEFAULT NULL,
  `systemterfaceMac` varchar(32) DEFAULT NULL,
  `tdmoipInterfaceMac` varchar(32) DEFAULT NULL,
  `currentTemperature` int(16) DEFAULT NULL,
  `sysUptime` int(10) unsigned DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`idu_iduInfoTable_id`),
  KEY `FK_idu_iduInfoTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_iduNetworkStatisticsTable`;
CREATE TABLE IF NOT EXISTS `idu_iduNetworkStatisticsTable` (
  `idu_iduNetworkStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `interfaceName` int(8) DEFAULT NULL,
  `rxPackets` int(10) unsigned DEFAULT NULL,
  `txPackets` int(10) unsigned DEFAULT NULL,
  `rxBytes` int(10) unsigned DEFAULT NULL,
  `txBytes` int(10) unsigned DEFAULT NULL,
  `rxErrors` int(10) unsigned DEFAULT NULL,
  `txErrors` int(10) unsigned DEFAULT NULL,
  `rxDropped` int(10) unsigned DEFAULT NULL,
  `txDropped` int(10) unsigned DEFAULT NULL,
  `multicasts` int(10) unsigned DEFAULT NULL,
  `collisions` int(10) unsigned DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`idu_iduNetworkStatisticsTable_id`,`timestamp`),
  KEY `FK_idu_iduNetworkStatisticsTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_iduOmOperationsTable`;
CREATE TABLE IF NOT EXISTS `idu_iduOmOperationsTable` (
  `idu_iduOmOperationsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `omIndex` int(32) DEFAULT NULL,
  `omOperationReq` int(8) DEFAULT NULL,
  `userName` varchar(16) DEFAULT NULL,
  `password` varchar(16) DEFAULT NULL,
  `ftpServerAddress` varchar(32) DEFAULT NULL,
  `pathName` varchar(128) DEFAULT NULL,
  `omOperationResult` int(8) DEFAULT NULL,
  `omSpecificCause` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_iduOmOperationsTable_id`),
  KEY `FK_idu_iduOmOperationsTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_linkConfigurationTable`;
CREATE TABLE IF NOT EXISTS `idu_linkConfigurationTable` (
  `idu_linkConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `portNumber` int(10) DEFAULT NULL,
  `bundleNumber` int(32) DEFAULT NULL,
  `adminStatus` int(8) DEFAULT NULL,
  `srcBundleID` int(32) DEFAULT NULL,
  `dstBundleID` int(32) DEFAULT NULL,
  `dstIPAddr` varchar(32) DEFAULT NULL,
  `tsaAssign` varchar(32) DEFAULT NULL,
  `clockRecovery` int(8) DEFAULT NULL,
  `bundleSize` int(32) DEFAULT NULL,
  `bufferSize` int(32) DEFAULT NULL,
  `rowStatus` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_linkConfigurationTable_id`),
  KEY `FK_idu_linkConfigurationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_linkStatisticsTable`;
CREATE TABLE IF NOT EXISTS `idu_linkStatisticsTable` (
  `idu_linkStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `bundlenumber` int(32) DEFAULT NULL,
  `portNum` tinyint(4) DEFAULT NULL,
  `goodFramesToEth` int(10) unsigned DEFAULT NULL,
  `goodFramesRx` int(10) unsigned DEFAULT NULL,
  `lostPacketsAtRx` int(10) unsigned DEFAULT NULL,
  `discardedPackets` int(10) unsigned DEFAULT NULL,
  `reorderedPackets` int(10) unsigned DEFAULT NULL,
  `underrunEvents` int(10) unsigned DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`idu_linkStatisticsTable_id`),
  KEY `FK_idu_linkStatisticsTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_linkStatusTable`;
CREATE TABLE IF NOT EXISTS `idu_linkStatusTable` (
  `idu_linkStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `bundleNum` int(32) DEFAULT NULL,
  `portNum` tinyint(4) DEFAULT NULL,
  `operationalStatus` int(8) DEFAULT NULL,
  `minJBLevel` int(32) DEFAULT NULL,
  `maxJBLevel` int(32) DEFAULT NULL,
  `underrunOccured` int(8) DEFAULT NULL,
  `overrunOccured` int(8) DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`idu_linkStatusTable_id`,`timestamp`),
  KEY `FK_idu_linkStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_mirroringportTable`;
CREATE TABLE IF NOT EXISTS `idu_mirroringportTable` (
  `idu_mirroringportTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `mirroringindexid` int(32) DEFAULT NULL,
  `mirroringport` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_mirroringportTable_id`),
  KEY `FK_idu_mirroringportTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_networkConfigurationsTable`;
CREATE TABLE IF NOT EXISTS `idu_networkConfigurationsTable` (
  `idu_networkConfigurationsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `interface` int(8) DEFAULT NULL,
  `ipaddr` varchar(32) DEFAULT NULL,
  `netmask` varchar(32) DEFAULT NULL,
  `gateway` varchar(32) DEFAULT NULL,
  `autoIpConfig` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_networkConfigurationsTable_id`),
  KEY `FK_idu_networkConfigurationsTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_oids`;
CREATE TABLE IF NOT EXISTS `idu_oids` (
  `oid_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_type_id` varchar(16) DEFAULT NULL,
  `oid` varchar(256) DEFAULT NULL,
  `oid_name` varchar(256) DEFAULT NULL,
  `oid_type` varchar(16) DEFAULT NULL,
  `access` smallint(6) DEFAULT NULL,
  `default_value` varchar(256) DEFAULT NULL,
  `min_value` varchar(128) DEFAULT NULL,
  `max_value` varchar(256) DEFAULT NULL,
  `indexes` varchar(256) DEFAULT NULL,
  `dependent_id` int(10) unsigned DEFAULT NULL,
  `multivalue` smallint(6) DEFAULT '0',
  `table_name` varchar(128) DEFAULT NULL,
  `coloumn_name` varchar(128) DEFAULT NULL,
  `indexes_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`oid_id`),
  KEY `FK_oids` (`device_type_id`),
  KEY `FK_oids_dependant_id` (`dependent_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_oids_multivalues`;
CREATE TABLE IF NOT EXISTS `idu_oids_multivalues` (
  `oids_multivalue_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `oid_id` int(10) unsigned DEFAULT NULL,
  `value` varchar(128) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`oids_multivalue_id`),
  KEY `FK_oids_multivalues` (`oid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_oid_table`;
CREATE TABLE IF NOT EXISTS `idu_oid_table` (
  `table_name` varchar(64) NOT NULL,
  `table_oid` varchar(64) NOT NULL,
  `varbinds` tinyint(4) NOT NULL DEFAULT '20'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_omcConfigurationTable`;
CREATE TABLE IF NOT EXISTS `idu_omcConfigurationTable` (
  `idu_omcConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `omcIndex` int(32) DEFAULT NULL,
  `omcIpAddress` varchar(32) DEFAULT NULL,
  `periodicStatsTimer` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`idu_omcConfigurationTable_id`),
  KEY `FK_idu_omcConfigurationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_poeConfigurationTable`;
CREATE TABLE IF NOT EXISTS `idu_poeConfigurationTable` (
  `idu_poeConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `indexId` int(32) DEFAULT NULL,
  `poeAdminStatus` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_poeConfigurationTable_id`),
  KEY `FK_idu_poeConfigurationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_portBwTable`;
CREATE TABLE IF NOT EXISTS `idu_portBwTable` (
  `idu_portBwTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `switchportnum` int(8) DEFAULT NULL,
  `egressbwvalue` int(32) DEFAULT NULL,
  `ingressbwvalue` int(32) DEFAULT NULL,
  PRIMARY KEY (`idu_portBwTable_id`),
  KEY `FK_idu_portBwTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_portqinqTable`;
CREATE TABLE IF NOT EXISTS `idu_portqinqTable` (
  `idu_portqinqTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `switchportnumber` int(8) DEFAULT NULL,
  `portqinqstate` int(8) DEFAULT NULL,
  `providertag` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`idu_portqinqTable_id`),
  KEY `FK_idu_portqinqTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_portSecondaryStatisticsTable`;
CREATE TABLE IF NOT EXISTS `idu_portSecondaryStatisticsTable` (
  `idu_portSecondaryStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `switchPortNum` int(8) DEFAULT NULL,
  `inUnicast` int(32) DEFAULT NULL,
  `outUnicast` int(32) DEFAULT NULL,
  `inBroadcast` int(32) DEFAULT NULL,
  `outBroadcast` int(32) DEFAULT NULL,
  `inMulticast` int(32) DEFAULT NULL,
  `outMulricast` int(32) DEFAULT NULL,
  `inUndersizeRx` int(32) DEFAULT NULL,
  `inFragmentsRx` int(32) DEFAULT NULL,
  `inOversizeRx` int(32) DEFAULT NULL,
  `inJabberRx` int(32) DEFAULT NULL,
  `inMacRcvErrorRx` int(32) DEFAULT NULL,
  `inFCSErrorRx` int(32) DEFAULT NULL,
  `outFCSErrorTx` int(32) DEFAULT NULL,
  `deferedTx` int(32) DEFAULT NULL,
  `collisionTx` int(32) DEFAULT NULL,
  `lateTx` int(32) DEFAULT NULL,
  `exessiveTx` int(32) DEFAULT NULL,
  `singleTx` int(32) DEFAULT NULL,
  `multipleTx` int(32) DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`idu_portSecondaryStatisticsTable_id`,`timestamp`),
  KEY `FK_idu_portSecondaryStatisticsTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_portstatbadframeTable`;
CREATE TABLE IF NOT EXISTS `idu_portstatbadframeTable` (
  `idu_portstatbadframeTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `switchbadframeport` int(8) DEFAULT NULL,
  `inundersizerx` int(10) unsigned DEFAULT NULL,
  `infragmnetsrx` int(10) unsigned DEFAULT NULL,
  `inoversizerx` int(10) unsigned DEFAULT NULL,
  `inmacrcverrorrx` int(10) unsigned DEFAULT NULL,
  `injabberrx` int(10) unsigned DEFAULT NULL,
  `infcserrorrx` int(32) DEFAULT NULL,
  `outfcserrtx` int(10) unsigned DEFAULT NULL,
  `defferedtx` int(10) unsigned DEFAULT NULL,
  `collisiontx` int(10) unsigned DEFAULT NULL,
  `latetx` int(32) DEFAULT NULL,
  `excessivetx` int(32) DEFAULT NULL,
  `singletx` int(32) DEFAULT NULL,
  `multipletx` int(32) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`idu_portstatbadframeTable_id`),
  KEY `FK_idu_portstatbadframeTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_portstatgoodframeTable`;
CREATE TABLE IF NOT EXISTS `idu_portstatgoodframeTable` (
  `idu_portstatgoodframeTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `softwaregoodframeportnum` int(8) DEFAULT NULL,
  `inunicast` int(10) unsigned DEFAULT NULL,
  `outunicast` int(10) unsigned DEFAULT NULL,
  `inbroadcast` int(10) unsigned DEFAULT NULL,
  `outbroadcast` int(10) unsigned DEFAULT NULL,
  `inmulticast` int(10) unsigned DEFAULT NULL,
  `outmulticast` int(10) unsigned DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`idu_portstatgoodframeTable_id`),
  KEY `FK_idu_portstatgoodframeTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_portstatisticsTable`;
CREATE TABLE IF NOT EXISTS `idu_portstatisticsTable` (
  `idu_portstatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `softwarestatportnum` int(8) DEFAULT NULL,
  `framerx` int(10) unsigned DEFAULT NULL,
  `frametx` int(10) unsigned DEFAULT NULL,
  `indiscards` int(32) DEFAULT NULL,
  `ingoodoctets` int(32) DEFAULT NULL,
  `inbadoctet` int(32) DEFAULT NULL,
  `outoctets` int(32) DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`idu_portstatisticsTable_id`,`timestamp`),
  KEY `FK_idu_portstatisticsTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_rtcConfigurationTable`;
CREATE TABLE IF NOT EXISTS `idu_rtcConfigurationTable` (
  `idu_rtcConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `rtcIndex` int(32) DEFAULT NULL,
  `year` int(32) DEFAULT NULL,
  `month` int(32) DEFAULT NULL,
  `day` int(32) DEFAULT NULL,
  `hour` int(32) DEFAULT NULL,
  `min` int(32) DEFAULT NULL,
  `sec` int(32) DEFAULT NULL,
  PRIMARY KEY (`idu_rtcConfigurationTable_id`),
  KEY `FK_idu_rtcConfigurationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_sectorIdentificationTable`;
CREATE TABLE IF NOT EXISTS `idu_sectorIdentificationTable` (
  `idu_sectorIdentificationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `sectorIndex` int(32) DEFAULT NULL,
  `countryCode` int(32) DEFAULT NULL,
  `operatorCode` int(32) DEFAULT NULL,
  `deploymentCode` int(32) DEFAULT NULL,
  `sectorCode` int(32) DEFAULT NULL,
  PRIMARY KEY (`idu_sectorIdentificationTable_id`),
  KEY `FK_idu_sectorIdentificationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_switchPortconfigTable`;
CREATE TABLE IF NOT EXISTS `idu_switchPortconfigTable` (
  `idu_switchPortconfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `switchportNum` int(8) DEFAULT NULL,
  `swadminState` int(8) DEFAULT NULL,
  `swlinkMode` int(8) DEFAULT NULL,
  `portvid` int(10) unsigned DEFAULT NULL,
  `macauthState` int(8) DEFAULT NULL,
  `mirroringdirection` int(8) DEFAULT NULL,
  `portdotqmode` int(8) DEFAULT NULL,
  `macflowcontrol` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_switchPortconfigTable_id`),
  KEY `FK_idu_switchPortconfigTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_switchportstatusTable`;
CREATE TABLE IF NOT EXISTS `idu_switchportstatusTable` (
  `idu_switchportstatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `switchstatportnum` int(8) DEFAULT NULL,
  `opstate` int(8) DEFAULT NULL,
  `linkspeed` int(8) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`idu_switchportstatusTable_id`),
  KEY `FK_idu_switchportstatusTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_swPrimaryPortStatisticsTable`;
CREATE TABLE IF NOT EXISTS `idu_swPrimaryPortStatisticsTable` (
  `idu_swPrimaryPortStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `swportnumber` int(8) DEFAULT NULL,
  `framesRx` int(32) DEFAULT NULL,
  `framesTx` int(32) DEFAULT NULL,
  `inDiscard` int(32) DEFAULT NULL,
  `inGoodOctets` int(32) DEFAULT NULL,
  `inBadOctets` int(32) DEFAULT NULL,
  `outOctets` int(32) DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`idu_swPrimaryPortStatisticsTable_id`,`timestamp`),
  KEY `FK_idu_swPrimaryPortStatisticsTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_swStatusTable`;
CREATE TABLE IF NOT EXISTS `idu_swStatusTable` (
  `idu_swStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `swStatusIndex` int(32) DEFAULT NULL,
  `activeVersion` varchar(32) DEFAULT NULL,
  `passiveVersion` varchar(32) DEFAULT NULL,
  `bootloaderVersion` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`idu_swStatusTable_id`),
  KEY `FK_idu_swStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_sysOmcRegistrationTable`;
CREATE TABLE IF NOT EXISTS `idu_sysOmcRegistrationTable` (
  `idu_sysOmcRegistrationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `sysOmcRegistrationIndex` int(32) DEFAULT NULL,
  `sysOmcRegisterContactAddr` varchar(32) DEFAULT NULL,
  `sysOmcRegisterContactPerson` varchar(32) DEFAULT NULL,
  `sysOmcRegisterContactMobile` varchar(32) DEFAULT NULL,
  `sysOmcRegisterAlternateContact` varchar(32) DEFAULT NULL,
  `sysOmcRegisterContactEmail` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`idu_sysOmcRegistrationTable_id`),
  KEY `FK_idu_sysOmcRegistrationTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_tdmoipNetworkInterfaceConfigurationTable`;
CREATE TABLE IF NOT EXISTS `idu_tdmoipNetworkInterfaceConfigurationTable` (
  `idu_tdmoipNetworkInterfaceConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `interfaceid` int(32) DEFAULT NULL,
  `ipaddress` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`idu_tdmoipNetworkInterfaceConfigurationTable_id`),
  KEY `FK_idu_tdmoipNetworkInterfaceConfigurationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_tdmoipNetworkInterfaceStatisticsTable`;
CREATE TABLE IF NOT EXISTS `idu_tdmoipNetworkInterfaceStatisticsTable` (
  `idu_tdmoipNetworkInterfaceStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `indexid` int(32) DEFAULT NULL,
  `bytesTransmitted` int(10) unsigned DEFAULT NULL,
  `bytesReceived` int(10) unsigned DEFAULT NULL,
  `framesTransmittedOk` int(10) unsigned DEFAULT NULL,
  `framesReceivedOk` int(10) unsigned DEFAULT NULL,
  `goodClassifiedFramesRx` int(10) unsigned DEFAULT NULL,
  `checksumErrorPackets` int(10) unsigned DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`idu_tdmoipNetworkInterfaceStatisticsTable_id`,`timestamp`),
  KEY `FK_idu_tdmoipNetworkInterfaceStatisticsTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_temperatureSensorConfigurationTable`;
CREATE TABLE IF NOT EXISTS `idu_temperatureSensorConfigurationTable` (
  `idu_temperatureSensorConfigurationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `tempIndex` int(32) DEFAULT NULL,
  `tempMax` int(32) DEFAULT NULL,
  `tempMin` int(32) DEFAULT NULL,
  PRIMARY KEY (`idu_temperatureSensorConfigurationTable_id`),
  KEY `FK_idu_temperatureSensorConfigurationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `idu_vlanconfigTable`;
CREATE TABLE IF NOT EXISTS `idu_vlanconfigTable` (
  `idu_vlanconfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `vlanid` int(10) unsigned DEFAULT NULL,
  `vlanname` varchar(16) DEFAULT NULL,
  `vlantype` int(8) DEFAULT NULL,
  `vlantag` int(10) unsigned DEFAULT NULL,
  `memberports` int(32) DEFAULT NULL,
  `vlanrowstatus` int(8) DEFAULT NULL,
  PRIMARY KEY (`idu_vlanconfigTable_id`),
  KEY `FK_idu_vlanconfigTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `license_details`;
CREATE TABLE IF NOT EXISTS `license_details` (
  `license_id` varchar(32) NOT NULL,
  `issued_client` varchar(32) NOT NULL,
  `issue_date` datetime NOT NULL,
  `expire_date` datetime NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `license_info`;
CREATE TABLE IF NOT EXISTS `license_info` (
  `minutes` int(32) NOT NULL,
  `last_check_date` datetime NOT NULL,
  `is_valid` tinyint(2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `localhost_bandwidth`;
CREATE TABLE IF NOT EXISTS `localhost_bandwidth` (
  `localhost_bandwidth_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `interface` varchar(16) DEFAULT NULL,
  `tx` int(10) unsigned DEFAULT NULL,
  `rx` int(10) unsigned DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`localhost_bandwidth_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `localhost_cpu_usage`;
CREATE TABLE IF NOT EXISTS `localhost_cpu_usage` (
  `localhost_cpu_usage_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `cpu_usage` float(32,4) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`localhost_cpu_usage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `login_info`;
CREATE TABLE IF NOT EXISTS `login_info` (
  `user_name` varchar(64) NOT NULL,
  `is_logged_in` smallint(6) NOT NULL,
  `session_id` varchar(64) NOT NULL,
  `login_time` datetime NOT NULL,
  `next_time_delete` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `master_slave_linking`;
CREATE TABLE IF NOT EXISTS `master_slave_linking` (
  `master_slave_linking_id` int(11) NOT NULL AUTO_INCREMENT,
  `master` int(11) NOT NULL,
  `slave` int(11) NOT NULL,
  PRIMARY KEY (`master_slave_linking_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `modules`;
CREATE TABLE IF NOT EXISTS `modules` (
  `module_id` varchar(64) NOT NULL,
  `module_name` varchar(32) DEFAULT NULL,
  `page_link_id` varchar(64) DEFAULT NULL,
  `is_default` smallint(6) DEFAULT '0',
  `is_deleted` smallint(6) DEFAULT '0',
  `page_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`module_id`),
  KEY `FK_modules_page` (`page_id`),
  KEY `FK_modules_page_link` (`page_link_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `nagios_acknowledgements`;
CREATE TABLE IF NOT EXISTS `nagios_acknowledgements` (
  `acknowledgement_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `entry_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `entry_time_usec` int(11) NOT NULL DEFAULT '0',
  `acknowledgement_type` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `state` smallint(6) NOT NULL DEFAULT '0',
  `author_name` varchar(64) NOT NULL DEFAULT '',
  `comment_data` varchar(255) NOT NULL DEFAULT '',
  `is_sticky` smallint(6) NOT NULL DEFAULT '0',
  `persistent_comment` smallint(6) NOT NULL DEFAULT '0',
  `notify_contacts` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`acknowledgement_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Current and historical host and service acknowledgements';

DROP TABLE IF EXISTS `nagios_commands`;
CREATE TABLE IF NOT EXISTS `nagios_commands` (
  `command_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `command_line` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`command_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`object_id`,`config_type`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Command definitions';

DROP TABLE IF EXISTS `nagios_commenthistory`;
CREATE TABLE IF NOT EXISTS `nagios_commenthistory` (
  `commenthistory_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `entry_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `entry_time_usec` int(11) NOT NULL DEFAULT '0',
  `comment_type` smallint(6) NOT NULL DEFAULT '0',
  `entry_type` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `comment_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `internal_comment_id` int(11) NOT NULL DEFAULT '0',
  `author_name` varchar(64) NOT NULL DEFAULT '',
  `comment_data` varchar(255) NOT NULL DEFAULT '',
  `is_persistent` smallint(6) NOT NULL DEFAULT '0',
  `comment_source` smallint(6) NOT NULL DEFAULT '0',
  `expires` smallint(6) NOT NULL DEFAULT '0',
  `expiration_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `deletion_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `deletion_time_usec` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`commenthistory_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`comment_time`,`internal_comment_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical host and service comments';

DROP TABLE IF EXISTS `nagios_comments`;
CREATE TABLE IF NOT EXISTS `nagios_comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `entry_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `entry_time_usec` int(11) NOT NULL DEFAULT '0',
  `comment_type` smallint(6) NOT NULL DEFAULT '0',
  `entry_type` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `comment_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `internal_comment_id` int(11) NOT NULL DEFAULT '0',
  `author_name` varchar(64) NOT NULL DEFAULT '',
  `comment_data` varchar(255) NOT NULL DEFAULT '',
  `is_persistent` smallint(6) NOT NULL DEFAULT '0',
  `comment_source` smallint(6) NOT NULL DEFAULT '0',
  `expires` smallint(6) NOT NULL DEFAULT '0',
  `expiration_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`comment_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`comment_time`,`internal_comment_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `nagios_configfiles`;
CREATE TABLE IF NOT EXISTS `nagios_configfiles` (
  `configfile_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `configfile_type` smallint(6) NOT NULL DEFAULT '0',
  `configfile_path` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`configfile_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`configfile_type`,`configfile_path`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Configuration files';

DROP TABLE IF EXISTS `nagios_configfilevariables`;
CREATE TABLE IF NOT EXISTS `nagios_configfilevariables` (
  `configfilevariable_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `configfile_id` int(11) NOT NULL DEFAULT '0',
  `varname` varchar(64) NOT NULL DEFAULT '',
  `varvalue` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`configfilevariable_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Configuration file variables';

DROP TABLE IF EXISTS `nagios_conninfo`;
CREATE TABLE IF NOT EXISTS `nagios_conninfo` (
  `conninfo_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `agent_name` varchar(32) NOT NULL DEFAULT '',
  `agent_version` varchar(8) NOT NULL DEFAULT '',
  `disposition` varchar(16) NOT NULL DEFAULT '',
  `connect_source` varchar(16) NOT NULL DEFAULT '',
  `connect_type` varchar(16) NOT NULL DEFAULT '',
  `connect_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `disconnect_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_checkin_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `bytes_processed` int(11) NOT NULL DEFAULT '0',
  `lines_processed` int(11) NOT NULL DEFAULT '0',
  `entries_processed` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`conninfo_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='NDO2DB daemon connection information';

DROP TABLE IF EXISTS `nagios_contactgroups`;
CREATE TABLE IF NOT EXISTS `nagios_contactgroups` (
  `contactgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `contactgroup_object_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`contactgroup_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`contactgroup_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Contactgroup definitions';

DROP TABLE IF EXISTS `nagios_contactgroup_members`;
CREATE TABLE IF NOT EXISTS `nagios_contactgroup_members` (
  `contactgroup_member_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `contactgroup_id` int(11) NOT NULL DEFAULT '0',
  `contact_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`contactgroup_member_id`),
  UNIQUE KEY `instance_id` (`contactgroup_id`,`contact_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Contactgroup members';

DROP TABLE IF EXISTS `nagios_contactnotificationmethods`;
CREATE TABLE IF NOT EXISTS `nagios_contactnotificationmethods` (
  `contactnotificationmethod_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `contactnotification_id` int(11) NOT NULL DEFAULT '0',
  `start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `start_time_usec` int(11) NOT NULL DEFAULT '0',
  `end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_time_usec` int(11) NOT NULL DEFAULT '0',
  `command_object_id` int(11) NOT NULL DEFAULT '0',
  `command_args` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`contactnotificationmethod_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`contactnotification_id`,`start_time`,`start_time_usec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical record of contact notification methods';

DROP TABLE IF EXISTS `nagios_contactnotifications`;
CREATE TABLE IF NOT EXISTS `nagios_contactnotifications` (
  `contactnotification_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `notification_id` int(11) NOT NULL DEFAULT '0',
  `contact_object_id` int(11) NOT NULL DEFAULT '0',
  `start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `start_time_usec` int(11) NOT NULL DEFAULT '0',
  `end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_time_usec` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`contactnotification_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`contact_object_id`,`start_time`,`start_time_usec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical record of contact notifications';

DROP TABLE IF EXISTS `nagios_contacts`;
CREATE TABLE IF NOT EXISTS `nagios_contacts` (
  `contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `contact_object_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(64) NOT NULL DEFAULT '',
  `email_address` varchar(255) NOT NULL DEFAULT '',
  `pager_address` varchar(64) NOT NULL DEFAULT '',
  `host_timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `service_timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `host_notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `service_notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `can_submit_commands` smallint(6) NOT NULL DEFAULT '0',
  `notify_service_recovery` smallint(6) NOT NULL DEFAULT '0',
  `notify_service_warning` smallint(6) NOT NULL DEFAULT '0',
  `notify_service_unknown` smallint(6) NOT NULL DEFAULT '0',
  `notify_service_critical` smallint(6) NOT NULL DEFAULT '0',
  `notify_service_flapping` smallint(6) NOT NULL DEFAULT '0',
  `notify_service_downtime` smallint(6) NOT NULL DEFAULT '0',
  `notify_host_recovery` smallint(6) NOT NULL DEFAULT '0',
  `notify_host_down` smallint(6) NOT NULL DEFAULT '0',
  `notify_host_unreachable` smallint(6) NOT NULL DEFAULT '0',
  `notify_host_flapping` smallint(6) NOT NULL DEFAULT '0',
  `notify_host_downtime` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`contact_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`contact_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Contact definitions';

DROP TABLE IF EXISTS `nagios_contactstatus`;
CREATE TABLE IF NOT EXISTS `nagios_contactstatus` (
  `contactstatus_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `contact_object_id` int(11) NOT NULL DEFAULT '0',
  `status_update_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `host_notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `service_notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `last_host_notification` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_service_notification` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_attributes` int(11) NOT NULL DEFAULT '0',
  `modified_host_attributes` int(11) NOT NULL DEFAULT '0',
  `modified_service_attributes` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`contactstatus_id`),
  UNIQUE KEY `contact_object_id` (`contact_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Contact status';

DROP TABLE IF EXISTS `nagios_contact_addresses`;
CREATE TABLE IF NOT EXISTS `nagios_contact_addresses` (
  `contact_address_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `contact_id` int(11) NOT NULL DEFAULT '0',
  `address_number` smallint(6) NOT NULL DEFAULT '0',
  `address` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`contact_address_id`),
  UNIQUE KEY `contact_id` (`contact_id`,`address_number`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Contact addresses';

DROP TABLE IF EXISTS `nagios_contact_notificationcommands`;
CREATE TABLE IF NOT EXISTS `nagios_contact_notificationcommands` (
  `contact_notificationcommand_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `contact_id` int(11) NOT NULL DEFAULT '0',
  `notification_type` smallint(6) NOT NULL DEFAULT '0',
  `command_object_id` int(11) NOT NULL DEFAULT '0',
  `command_args` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`contact_notificationcommand_id`),
  UNIQUE KEY `contact_id` (`contact_id`,`notification_type`,`command_object_id`,`command_args`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Contact host and service notification commands';

DROP TABLE IF EXISTS `nagios_customvariables`;
CREATE TABLE IF NOT EXISTS `nagios_customvariables` (
  `customvariable_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `has_been_modified` smallint(6) NOT NULL DEFAULT '0',
  `varname` varchar(255) NOT NULL DEFAULT '',
  `varvalue` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`customvariable_id`),
  UNIQUE KEY `object_id_2` (`object_id`,`config_type`,`varname`),
  KEY `varname` (`varname`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Custom variables';

DROP TABLE IF EXISTS `nagios_customvariablestatus`;
CREATE TABLE IF NOT EXISTS `nagios_customvariablestatus` (
  `customvariablestatus_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `status_update_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `has_been_modified` smallint(6) NOT NULL DEFAULT '0',
  `varname` varchar(255) NOT NULL DEFAULT '',
  `varvalue` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`customvariablestatus_id`),
  UNIQUE KEY `object_id_2` (`object_id`,`varname`),
  KEY `varname` (`varname`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Custom variable status information';

DROP TABLE IF EXISTS `nagios_dbversion`;
CREATE TABLE IF NOT EXISTS `nagios_dbversion` (
  `name` varchar(10) NOT NULL DEFAULT '',
  `version` varchar(10) NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `nagios_downtimehistory`;
CREATE TABLE IF NOT EXISTS `nagios_downtimehistory` (
  `downtimehistory_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `downtime_type` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `entry_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `author_name` varchar(64) NOT NULL DEFAULT '',
  `comment_data` varchar(255) NOT NULL DEFAULT '',
  `internal_downtime_id` int(11) NOT NULL DEFAULT '0',
  `
  triggered_by_id` int(11) NOT NULL DEFAULT '0',
  `is_fixed` smallint(6) NOT NULL DEFAULT '0',
  `duration` smallint(6) NOT NULL DEFAULT '0',
  `scheduled_start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `scheduled_end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `was_started` smallint(6) NOT NULL DEFAULT '0',
  `actual_start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `actual_start_time_usec` int(11) NOT NULL DEFAULT '0',
  `actual_end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `actual_end_time_usec` int(11) NOT NULL DEFAULT '0',
  `was_cancelled` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`downtimehistory_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`object_id`,`entry_time`,`internal_downtime_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical scheduled host and service downtime';

DROP TABLE IF EXISTS `nagios_eventhandlers`;
CREATE TABLE IF NOT EXISTS `nagios_eventhandlers` (
  `eventhandler_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `eventhandler_type` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `state` smallint(6) NOT NULL DEFAULT '0',
  `state_type` smallint(6) NOT NULL DEFAULT '0',
  `start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `start_time_usec` int(11) NOT NULL DEFAULT '0',
  `end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_time_usec` int(11) NOT NULL DEFAULT '0',
  `command_object_id` int(11) NOT NULL DEFAULT '0',
  `command_args` varchar(255) NOT NULL DEFAULT '',
  `command_line` varchar(255) NOT NULL DEFAULT '',
  `timeout` smallint(6) NOT NULL DEFAULT '0',
  `early_timeout` smallint(6) NOT NULL DEFAULT '0',
  `execution_time` double NOT NULL DEFAULT '0',
  `return_code` smallint(6) NOT NULL DEFAULT '0',
  `output` varchar(255) NOT NULL DEFAULT '',
  `long_output` text NOT NULL,
  PRIMARY KEY (`eventhandler_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`object_id`,`start_time`,`start_time_usec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical host and service event handlers';

DROP TABLE IF EXISTS `nagios_externalcommands`;
CREATE TABLE IF NOT EXISTS `nagios_externalcommands` (
  `externalcommand_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `entry_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `command_type` smallint(6) NOT NULL DEFAULT '0',
  `command_name` varchar(128) NOT NULL DEFAULT '',
  `command_args` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`externalcommand_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical record of processed external commands';

DROP TABLE IF EXISTS `nagios_flappinghistory`;
CREATE TABLE IF NOT EXISTS `nagios_flappinghistory` (
  `flappinghistory_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `event_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `event_time_usec` int(11) NOT NULL DEFAULT '0',
  `event_type` smallint(6) NOT NULL DEFAULT '0',
  `reason_type` smallint(6) NOT NULL DEFAULT '0',
  `flapping_type` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `percent_state_change` double NOT NULL DEFAULT '0',
  `low_threshold` double NOT NULL DEFAULT '0',
  `high_threshold` double NOT NULL DEFAULT '0',
  `comment_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `internal_comment_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`flappinghistory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Current and historical record of host and service flapping';

DROP TABLE IF EXISTS `nagios_hostchecks`;
CREATE TABLE IF NOT EXISTS `nagios_hostchecks` (
  `hostcheck_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `host_object_id` int(11) NOT NULL DEFAULT '0',
  `check_type` smallint(6) NOT NULL DEFAULT '0',
  `is_raw_check` smallint(6) NOT NULL DEFAULT '0',
  `current_check_attempt` smallint(6) NOT NULL DEFAULT '0',
  `max_check_attempts` smallint(6) NOT NULL DEFAULT '0',
  `state` smallint(6) NOT NULL DEFAULT '0',
  `state_type` smallint(6) NOT NULL DEFAULT '0',
  `start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `start_time_usec` int(11) NOT NULL DEFAULT '0',
  `end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_time_usec` int(11) NOT NULL DEFAULT '0',
  `command_object_id` int(11) NOT NULL DEFAULT '0',
  `command_args` varchar(255) NOT NULL DEFAULT '',
  `command_line` varchar(255) NOT NULL DEFAULT '',
  `timeout` smallint(6) NOT NULL DEFAULT '0',
  `early_timeout` smallint(6) NOT NULL DEFAULT '0',
  `execution_time` double NOT NULL DEFAULT '0',
  `latency` double NOT NULL DEFAULT '0',
  `return_code` smallint(6) NOT NULL DEFAULT '0',
  `output` varchar(255) NOT NULL DEFAULT '',
  `long_output` text NOT NULL,
  `perfdata` text NOT NULL,
  PRIMARY KEY (`hostcheck_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`host_object_id`,`start_time`,`start_time_usec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical host checks';

DROP TABLE IF EXISTS `nagios_hostdependencies`;
CREATE TABLE IF NOT EXISTS `nagios_hostdependencies` (
  `hostdependency_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `host_object_id` int(11) NOT NULL DEFAULT '0',
  `dependent_host_object_id` int(11) NOT NULL DEFAULT '0',
  `dependency_type` smallint(6) NOT NULL DEFAULT '0',
  `inherits_parent` smallint(6) NOT NULL DEFAULT '0',
  `timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `fail_on_up` smallint(6) NOT NULL DEFAULT '0',
  `fail_on_down` smallint(6) NOT NULL DEFAULT '0',
  `fail_on_unreachable` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hostdependency_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`host_object_id`,`dependent_host_object_id`,`dependency_type`,`inherits_parent`,`fail_on_up`,`fail_on_down`,`fail_on_unreachable`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Host dependency definitions';

DROP TABLE IF EXISTS `nagios_hostescalations`;
CREATE TABLE IF NOT EXISTS `nagios_hostescalations` (
  `hostescalation_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `host_object_id` int(11) NOT NULL DEFAULT '0',
  `timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `first_notification` smallint(6) NOT NULL DEFAULT '0',
  `last_notification` smallint(6) NOT NULL DEFAULT '0',
  `notification_interval` double NOT NULL DEFAULT '0',
  `escalate_on_recovery` smallint(6) NOT NULL DEFAULT '0',
  `escalate_on_down` smallint(6) NOT NULL DEFAULT '0',
  `escalate_on_unreachable` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hostescalation_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`host_object_id`,`timeperiod_object_id`,`first_notification`,`last_notification`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Host escalation definitions';

DROP TABLE IF EXISTS `nagios_hostescalation_contactgroups`;
CREATE TABLE IF NOT EXISTS `nagios_hostescalation_contactgroups` (
  `hostescalation_contactgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `hostescalation_id` int(11) NOT NULL DEFAULT '0',
  `contactgroup_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hostescalation_contactgroup_id`),
  UNIQUE KEY `instance_id` (`hostescalation_id`,`contactgroup_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Host escalation contact groups';

DROP TABLE IF EXISTS `nagios_hostescalation_contacts`;
CREATE TABLE IF NOT EXISTS `nagios_hostescalation_contacts` (
  `hostescalation_contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `hostescalation_id` int(11) NOT NULL DEFAULT '0',
  `contact_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hostescalation_contact_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`hostescalation_id`,`contact_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `nagios_hostgroups`;
CREATE TABLE IF NOT EXISTS `nagios_hostgroups` (
  `hostgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `hostgroup_object_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`hostgroup_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`hostgroup_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Hostgroup definitions';

DROP TABLE IF EXISTS `nagios_hostgroup_members`;
CREATE TABLE IF NOT EXISTS `nagios_hostgroup_members` (
  `hostgroup_member_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `hostgroup_id` int(11) NOT NULL DEFAULT '0',
  `host_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hostgroup_member_id`),
  UNIQUE KEY `instance_id` (`hostgroup_id`,`host_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Hostgroup members';

DROP TABLE IF EXISTS `nagios_hosts`;
CREATE TABLE IF NOT EXISTS `nagios_hosts` (
  `host_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `host_object_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(64) NOT NULL DEFAULT '',
  `display_name` varchar(64) NOT NULL DEFAULT '',
  `address` varchar(128) NOT NULL DEFAULT '',
  `check_command_object_id` int(11) NOT NULL DEFAULT '0',
  `check_command_args` varchar(255) NOT NULL DEFAULT '',
  `eventhandler_command_object_id` int(11) NOT NULL DEFAULT '0',
  `eventhandler_command_args` varchar(255) NOT NULL DEFAULT '',
  `notification_timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `check_timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `failure_prediction_options` varchar(64) NOT NULL DEFAULT '',
  `check_interval` double NOT NULL DEFAULT '0',
  `retry_interval` double NOT NULL DEFAULT '0',
  `max_check_attempts` smallint(6) NOT NULL DEFAULT '0',
  `first_notification_delay` double NOT NULL DEFAULT '0',
  `notification_interval` double NOT NULL DEFAULT '0',
  `notify_on_down` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_unreachable` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_recovery` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_flapping` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_downtime` smallint(6) NOT NULL DEFAULT '0',
  `stalk_on_up` smallint(6) NOT NULL DEFAULT '0',
  `stalk_on_down` smallint(6) NOT NULL DEFAULT '0',
  `stalk_on_unreachable` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_enabled` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_on_up` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_on_down` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_on_unreachable` smallint(6) NOT NULL DEFAULT '0',
  `low_flap_threshold` double NOT NULL DEFAULT '0',
  `high_flap_threshold` double NOT NULL DEFAULT '0',
  `process_performance_data` smallint(6) NOT NULL DEFAULT '0',
  `freshness_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `freshness_threshold` smallint(6) NOT NULL DEFAULT '0',
  `passive_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `event_handler_enabled` smallint(6) NOT NULL DEFAULT '0',
  `active_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `retain_status_information` smallint(6) NOT NULL DEFAULT '0',
  `retain_nonstatus_information` smallint(6) NOT NULL DEFAULT '0',
  `notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `obsess_over_host` smallint(6) NOT NULL DEFAULT '0',
  `failure_prediction_enabled` smallint(6) NOT NULL DEFAULT '0',
  `notes` varchar(255) NOT NULL DEFAULT '',
  `notes_url` varchar(255) NOT NULL DEFAULT '',
  `action_url` varchar(255) NOT NULL DEFAULT '',
  `icon_image` varchar(255) NOT NULL DEFAULT '',
  `icon_image_alt` varchar(255) NOT NULL DEFAULT '',
  `vrml_image` varchar(255) NOT NULL DEFAULT '',
  `statusmap_image` varchar(255) NOT NULL DEFAULT '',
  `have_2d_coords` smallint(6) NOT NULL DEFAULT '0',
  `x_2d` smallint(6) NOT NULL DEFAULT '0',
  `y_2d` smallint(6) NOT NULL DEFAULT '0',
  `have_3d_coords` smallint(6) NOT NULL DEFAULT '0',
  `x_3d` double NOT NULL DEFAULT '0',
  `y_3d` double NOT NULL DEFAULT '0',
  `z_3d` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`host_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`host_object_id`),
  KEY `host_object_id` (`host_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Host definitions';

DROP TABLE IF EXISTS `nagios_hoststatus`;
CREATE TABLE IF NOT EXISTS `nagios_hoststatus` (
  `hoststatus_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `host_object_id` int(11) NOT NULL DEFAULT '0',
  `status_update_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `output` varchar(255) NOT NULL DEFAULT '',
  `long_output` text NOT NULL,
  `perfdata` text NOT NULL,
  `current_state` smallint(6) NOT NULL DEFAULT '0',
  `has_been_checked` smallint(6) NOT NULL DEFAULT '0',
  `should_be_scheduled` smallint(6) NOT NULL DEFAULT '0',
  `current_check_attempt` smallint(6) NOT NULL DEFAULT '0',
  `max_check_attempts` smallint(6) NOT NULL DEFAULT '0',
  `last_check` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `next_check` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `check_type` smallint(6) NOT NULL DEFAULT '0',
  `last_state_change` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_hard_state_change` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_hard_state` smallint(6) NOT NULL DEFAULT '0',
  `last_time_up` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_time_down` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_time_unreachable` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `state_type` smallint(6) NOT NULL DEFAULT '0',
  `last_notification` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `next_notification` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `no_more_notifications` smallint(6) NOT NULL DEFAULT '0',
  `notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `problem_has_been_acknowledged` smallint(6) NOT NULL DEFAULT '0',
  `acknowledgement_type` smallint(6) NOT NULL DEFAULT '0',
  `current_notification_number` smallint(6) NOT NULL DEFAULT '0',
  `passive_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `active_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `event_handler_enabled` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_enabled` smallint(6) NOT NULL DEFAULT '0',
  `is_flapping` smallint(6) NOT NULL DEFAULT '0',
  `percent_state_change` double NOT NULL DEFAULT '0',
  `latency` double NOT NULL DEFAULT '0',
  `execution_time` double NOT NULL DEFAULT '0',
  `scheduled_downtime_depth` smallint(6) NOT NULL DEFAULT '0',
  `failure_prediction_enabled` smallint(6) NOT NULL DEFAULT '0',
  `process_performance_data` smallint(6) NOT NULL DEFAULT '0',
  `obsess_over_host` smallint(6) NOT NULL DEFAULT '0',
  `modified_host_attributes` int(11) NOT NULL DEFAULT '0',
  `event_handler` varchar(255) NOT NULL DEFAULT '',
  `check_command` varchar(255) NOT NULL DEFAULT '',
  `normal_check_interval` double NOT NULL DEFAULT '0',
  `retry_check_interval` double NOT NULL DEFAULT '0',
  `check_timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hoststatus_id`),
  UNIQUE KEY `object_id` (`host_object_id`),
  KEY `instance_id` (`instance_id`),
  KEY `status_update_time` (`status_update_time`),
  KEY `current_state` (`current_state`),
  KEY `check_type` (`check_type`),
  KEY `state_type` (`state_type`),
  KEY `last_state_change` (`last_state_change`),
  KEY `notifications_enabled` (`notifications_enabled`),
  KEY `problem_has_been_acknowledged` (`problem_has_been_acknowledged`),
  KEY `active_checks_enabled` (`active_checks_enabled`),
  KEY `passive_checks_enabled` (`passive_checks_enabled`),
  KEY `event_handler_enabled` (`event_handler_enabled`),
  KEY `flap_detection_enabled` (`flap_detection_enabled`),
  KEY `is_flapping` (`is_flapping`),
  KEY `percent_state_change` (`percent_state_change`),
  KEY `latency` (`latency`),
  KEY `execution_time` (`execution_time`),
  KEY `scheduled_downtime_depth` (`scheduled_downtime_depth`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Current host status information';

DROP TABLE IF EXISTS `nagios_host_contactgroups`;
CREATE TABLE IF NOT EXISTS `nagios_host_contactgroups` (
  `host_contactgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `host_id` int(11) NOT NULL DEFAULT '0',
  `contactgroup_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`host_contactgroup_id`),
  UNIQUE KEY `instance_id` (`host_id`,`contactgroup_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Host contact groups';

DROP TABLE IF EXISTS `nagios_host_contacts`;
CREATE TABLE IF NOT EXISTS `nagios_host_contacts` (
  `host_contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `host_id` int(11) NOT NULL DEFAULT '0',
  `contact_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`host_contact_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`host_id`,`contact_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `nagios_host_parenthosts`;
CREATE TABLE IF NOT EXISTS `nagios_host_parenthosts` (
  `host_parenthost_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `host_id` int(11) NOT NULL DEFAULT '0',
  `parent_host_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`host_parenthost_id`),
  UNIQUE KEY `instance_id` (`host_id`,`parent_host_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Parent hosts';

DROP TABLE IF EXISTS `nagios_instances`;
CREATE TABLE IF NOT EXISTS `nagios_instances` (
  `instance_id` smallint(6) NOT NULL AUTO_INCREMENT,
  `instance_name` varchar(64) NOT NULL DEFAULT '',
  `instance_description` varchar(128) NOT NULL DEFAULT '',
  PRIMARY KEY (`instance_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 COMMENT='Location names of various Nagios installations';

DROP TABLE IF EXISTS `nagios_logentries`;
CREATE TABLE IF NOT EXISTS `nagios_logentries` (
  `logentry_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` int(11) NOT NULL DEFAULT '0',
  `logentry_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `entry_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `entry_time_usec` int(11) NOT NULL DEFAULT '0',
  `logentry_type` int(11) NOT NULL DEFAULT '0',
  `logentry_data` varchar(255) NOT NULL DEFAULT '',
  `realtime_data` smallint(6) NOT NULL DEFAULT '0',
  `inferred_data_extracted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`logentry_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical record of log entries';

DROP TABLE IF EXISTS `nagios_notifications`;
CREATE TABLE IF NOT EXISTS `nagios_notifications` (
  `notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `notification_type` smallint(6) NOT NULL DEFAULT '0',
  `notification_reason` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `start_time_usec` int(11) NOT NULL DEFAULT '0',
  `end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_time_usec` int(11) NOT NULL DEFAULT '0',
  `state` smallint(6) NOT NULL DEFAULT '0',
  `output` varchar(255) NOT NULL DEFAULT '',
  `long_output` text NOT NULL,
  `escalated` smallint(6) NOT NULL DEFAULT '0',
  `contacts_notified` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`notification_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`object_id`,`start_time`,`start_time_usec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical record of host and service notifications';

DROP TABLE IF EXISTS `nagios_objects`;
CREATE TABLE IF NOT EXISTS `nagios_objects` (
  `object_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `objecttype_id` smallint(6) NOT NULL DEFAULT '0',
  `name1` varchar(128) NOT NULL DEFAULT '',
  `name2` varchar(128) DEFAULT NULL,
  `is_active` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`object_id`),
  KEY `objecttype_id` (`objecttype_id`,`name1`,`name2`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Current and historical objects of all kinds';

DROP TABLE IF EXISTS `nagios_processevents`;
CREATE TABLE IF NOT EXISTS `nagios_processevents` (
  `processevent_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `event_type` smallint(6) NOT NULL DEFAULT '0',
  `event_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `event_time_usec` int(11) NOT NULL DEFAULT '0',
  `process_id` int(11) NOT NULL DEFAULT '0',
  `program_name` varchar(16) NOT NULL DEFAULT '',
  `program_version` varchar(20) NOT NULL DEFAULT '',
  `program_date` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`processevent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical Nagios process events';

DROP TABLE IF EXISTS `nagios_programstatus`;
CREATE TABLE IF NOT EXISTS `nagios_programstatus` (
  `programstatus_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `status_update_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `program_start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `program_end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_currently_running` smallint(6) NOT NULL DEFAULT '0',
  `process_id` int(11) NOT NULL DEFAULT '0',
  `daemon_mode` smallint(6) NOT NULL DEFAULT '0',
  `last_command_check` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_log_rotation` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `active_service_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `passive_service_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `active_host_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `passive_host_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `event_handlers_enabled` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_enabled` smallint(6) NOT NULL DEFAULT '0',
  `failure_prediction_enabled` smallint(6) NOT NULL DEFAULT '0',
  `process_performance_data` smallint(6) NOT NULL DEFAULT '0',
  `obsess_over_hosts` smallint(6) NOT NULL DEFAULT '0',
  `obsess_over_services` smallint(6) NOT NULL DEFAULT '0',
  `modified_host_attributes` int(11) NOT NULL DEFAULT '0',
  `modified_service_attributes` int(11) NOT NULL DEFAULT '0',
  `global_host_event_handler` varchar(255) NOT NULL DEFAULT '',
  `global_service_event_handler` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`programstatus_id`),
  UNIQUE KEY `instance_id` (`instance_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Current program status information';

DROP TABLE IF EXISTS `nagios_runtimevariables`;
CREATE TABLE IF NOT EXISTS `nagios_runtimevariables` (
  `runtimevariable_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `varname` varchar(64) NOT NULL DEFAULT '',
  `varvalue` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`runtimevariable_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`varname`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Runtime variables from the Nagios daemon';

DROP TABLE IF EXISTS `nagios_scheduleddowntime`;
CREATE TABLE IF NOT EXISTS `nagios_scheduleddowntime` (
  `scheduleddowntime_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `downtime_type` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `entry_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `author_name` varchar(64) NOT NULL DEFAULT '',
  `comment_data` varchar(255) NOT NULL DEFAULT '',
  `internal_downtime_id` int(11) NOT NULL DEFAULT '0',
  `triggered_by_id` int(11) NOT NULL DEFAULT '0',
  `is_fixed` smallint(6) NOT NULL DEFAULT '0',
  `duration` smallint(6) NOT NULL DEFAULT '0',
  `scheduled_start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `scheduled_end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `was_started` smallint(6) NOT NULL DEFAULT '0',
  `actual_start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `actual_start_time_usec` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`scheduleddowntime_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`object_id`,`entry_time`,`internal_downtime_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Current scheduled host and service downtime';

DROP TABLE IF EXISTS `nagios_servicechecks`;
CREATE TABLE IF NOT EXISTS `nagios_servicechecks` (
  `servicecheck_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `service_object_id` int(11) NOT NULL DEFAULT '0',
  `check_type` smallint(6) NOT NULL DEFAULT '0',
  `current_check_attempt` smallint(6) NOT NULL DEFAULT '0',
  `max_check_attempts` smallint(6) NOT NULL DEFAULT '0',
  `state` smallint(6) NOT NULL DEFAULT '0',
  `state_type` smallint(6) NOT NULL DEFAULT '0',
  `start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `start_time_usec` int(11) NOT NULL DEFAULT '0',
  `end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_time_usec` int(11) NOT NULL DEFAULT '0',
  `command_object_id` int(11) NOT NULL DEFAULT '0',
  `command_args` varchar(255) NOT NULL DEFAULT '',
  `command_line` varchar(255) NOT NULL DEFAULT '',
  `timeout` smallint(6) NOT NULL DEFAULT '0',
  `early_timeout` smallint(6) NOT NULL DEFAULT '0',
  `execution_time` double NOT NULL DEFAULT '0',
  `latency` double NOT NULL DEFAULT '0',
  `return_code` smallint(6) NOT NULL DEFAULT '0',
  `output` varchar(255) NOT NULL DEFAULT '',
  `long_output` text NOT NULL,
  `perfdata` text NOT NULL,
  PRIMARY KEY (`servicecheck_id`),
  KEY `instance_id` (`instance_id`),
  KEY `service_object_id` (`service_object_id`),
  KEY `start_time` (`start_time`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical service checks';

DROP TABLE IF EXISTS `nagios_servicedependencies`;
CREATE TABLE IF NOT EXISTS `nagios_servicedependencies` (
  `servicedependency_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `service_object_id` int(11) NOT NULL DEFAULT '0',
  `dependent_service_object_id` int(11) NOT NULL DEFAULT '0',
  `dependency_type` smallint(6) NOT NULL DEFAULT '0',
  `inherits_parent` smallint(6) NOT NULL DEFAULT '0',
  `timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `fail_on_ok` smallint(6) NOT NULL DEFAULT '0',
  `fail_on_warning` smallint(6) NOT NULL DEFAULT '0',
  `fail_on_unknown` smallint(6) NOT NULL DEFAULT '0',
  `fail_on_critical` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`servicedependency_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`service_object_id`,`dependent_service_object_id`,`dependency_type`,`inherits_parent`,`fail_on_ok`,`fail_on_warning`,`fail_on_unknown`,`fail_on_critical`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Service dependency definitions';

DROP TABLE IF EXISTS `nagios_serviceescalations`;
CREATE TABLE IF NOT EXISTS `nagios_serviceescalations` (
  `serviceescalation_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `service_object_id` int(11) NOT NULL DEFAULT '0',
  `timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `first_notification` smallint(6) NOT NULL DEFAULT '0',
  `last_notification` smallint(6) NOT NULL DEFAULT '0',
  `notification_interval` double NOT NULL DEFAULT '0',
  `escalate_on_recovery` smallint(6) NOT NULL DEFAULT '0',
  `escalate_on_warning` smallint(6) NOT NULL DEFAULT '0',
  `escalate_on_unknown` smallint(6) NOT NULL DEFAULT '0',
  `escalate_on_critical` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`serviceescalation_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`service_object_id`,`timeperiod_object_id`,`first_notification`,`last_notification`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Service escalation definitions';

DROP TABLE IF EXISTS `nagios_serviceescalation_contactgroups`;
CREATE TABLE IF NOT EXISTS `nagios_serviceescalation_contactgroups` (
  `serviceescalation_contactgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `serviceescalation_id` int(11) NOT NULL DEFAULT '0',
  `contactgroup_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`serviceescalation_contactgroup_id`),
  UNIQUE KEY `instance_id` (`serviceescalation_id`,`contactgroup_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Service escalation contact groups';

DROP TABLE IF EXISTS `nagios_serviceescalation_contacts`;
CREATE TABLE IF NOT EXISTS `nagios_serviceescalation_contacts` (
  `serviceescalation_contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `serviceescalation_id` int(11) NOT NULL DEFAULT '0',
  `contact_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`serviceescalation_contact_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`serviceescalation_id`,`contact_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `nagios_servicegroups`;
CREATE TABLE IF NOT EXISTS `nagios_servicegroups` (
  `servicegroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `servicegroup_object_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`servicegroup_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`servicegroup_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Servicegroup definitions';

DROP TABLE IF EXISTS `nagios_servicegroup_members`;
CREATE TABLE IF NOT EXISTS `nagios_servicegroup_members` (
  `servicegroup_member_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `servicegroup_id` int(11) NOT NULL DEFAULT '0',
  `service_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`servicegroup_member_id`),
  UNIQUE KEY `instance_id` (`servicegroup_id`,`service_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Servicegroup members';

DROP TABLE IF EXISTS `nagios_services`;
CREATE TABLE IF NOT EXISTS `nagios_services` (
  `service_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `host_object_id` int(11) NOT NULL DEFAULT '0',
  `service_object_id` int(11) NOT NULL DEFAULT '0',
  `display_name` varchar(64) NOT NULL DEFAULT '',
  `check_command_object_id` int(11) NOT NULL DEFAULT '0',
  `check_command_args` varchar(255) NOT NULL DEFAULT '',
  `eventhandler_command_object_id` int(11) NOT NULL DEFAULT '0',
  `eventhandler_command_args` varchar(255) NOT NULL DEFAULT '',
  `notification_timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `check_timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `failure_prediction_options` varchar(64) NOT NULL DEFAULT '',
  `check_interval` double NOT NULL DEFAULT '0',
  `retry_interval` double NOT NULL DEFAULT '0',
  `max_check_attempts` smallint(6) NOT NULL DEFAULT '0',
  `first_notification_delay` double NOT NULL DEFAULT '0',
  `notification_interval` double NOT NULL DEFAULT '0',
  `notify_on_warning` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_unknown` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_critical` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_recovery` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_flapping` smallint(6) NOT NULL DEFAULT '0',
  `notify_on_downtime` smallint(6) NOT NULL DEFAULT '0',
  `stalk_on_ok` smallint(6) NOT NULL DEFAULT '0',
  `stalk_on_warning` smallint(6) NOT NULL DEFAULT '0',
  `stalk_on_unknown` smallint(6) NOT NULL DEFAULT '0',
  `stalk_on_critical` smallint(6) NOT NULL DEFAULT '0',
  `is_volatile` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_enabled` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_on_ok` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_on_warning` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_on_unknown` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_on_critical` smallint(6) NOT NULL DEFAULT '0',
  `low_flap_threshold` double NOT NULL DEFAULT '0',
  `high_flap_threshold` double NOT NULL DEFAULT '0',
  `process_performance_data` smallint(6) NOT NULL DEFAULT '0',
  `freshness_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `freshness_threshold` smallint(6) NOT NULL DEFAULT '0',
  `passive_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `event_handler_enabled` smallint(6) NOT NULL DEFAULT '0',
  `active_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `retain_status_information` smallint(6) NOT NULL DEFAULT '0',
  `retain_nonstatus_information` smallint(6) NOT NULL DEFAULT '0',
  `notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `obsess_over_service` smallint(6) NOT NULL DEFAULT '0',
  `failure_prediction_enabled` smallint(6) NOT NULL DEFAULT '0',
  `notes` varchar(255) NOT NULL DEFAULT '',
  `notes_url` varchar(255) NOT NULL DEFAULT '',
  `action_url` varchar(255) NOT NULL DEFAULT '',
  `icon_image` varchar(255) NOT NULL DEFAULT '',
  `icon_image_alt` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`service_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`service_object_id`),
  KEY `service_object_id` (`service_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Service definitions';

DROP TABLE IF EXISTS `nagios_servicestatus`;
CREATE TABLE IF NOT EXISTS `nagios_servicestatus` (
  `servicestatus_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `service_object_id` int(11) NOT NULL DEFAULT '0',
  `status_update_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `output` varchar(255) NOT NULL DEFAULT '',
  `long_output` text NOT NULL,
  `perfdata` text NOT NULL,
  `current_state` smallint(6) NOT NULL DEFAULT '0',
  `has_been_checked` smallint(6) NOT NULL DEFAULT '0',
  `should_be_scheduled` smallint(6) NOT NULL DEFAULT '0',
  `current_check_attempt` smallint(6) NOT NULL DEFAULT '0',
  `max_check_attempts` smallint(6) NOT NULL DEFAULT '0',
  `last_check` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `next_check` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `check_type` smallint(6) NOT NULL DEFAULT '0',
  `last_state_change` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_hard_state_change` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_hard_state` smallint(6) NOT NULL DEFAULT '0',
  `last_time_ok` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_time_warning` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_time_unknown` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_time_critical` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `state_type` smallint(6) NOT NULL DEFAULT '0',
  `last_notification` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `next_notification` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `no_more_notifications` smallint(6) NOT NULL DEFAULT '0',
  `notifications_enabled` smallint(6) NOT NULL DEFAULT '0',
  `problem_has_been_acknowledged` smallint(6) NOT NULL DEFAULT '0',
  `acknowledgement_type` smallint(6) NOT NULL DEFAULT '0',
  `current_notification_number` smallint(6) NOT NULL DEFAULT '0',
  `passive_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `active_checks_enabled` smallint(6) NOT NULL DEFAULT '0',
  `event_handler_enabled` smallint(6) NOT NULL DEFAULT '0',
  `flap_detection_enabled` smallint(6) NOT NULL DEFAULT '0',
  `is_flapping` smallint(6) NOT NULL DEFAULT '0',
  `percent_state_change` double NOT NULL DEFAULT '0',
  `latency` double NOT NULL DEFAULT '0',
  `execution_time` double NOT NULL DEFAULT '0',
  `scheduled_downtime_depth` smallint(6) NOT NULL DEFAULT '0',
  `failure_prediction_enabled` smallint(6) NOT NULL DEFAULT '0',
  `process_performance_data` smallint(6) NOT NULL DEFAULT '0',
  `obsess_over_service` smallint(6) NOT NULL DEFAULT '0',
  `modified_service_attributes` int(11) NOT NULL DEFAULT '0',
  `event_handler` varchar(255) NOT NULL DEFAULT '',
  `check_command` varchar(255) NOT NULL DEFAULT '',
  `normal_check_interval` double NOT NULL DEFAULT '0',
  `retry_check_interval` double NOT NULL DEFAULT '0',
  `check_timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`servicestatus_id`),
  UNIQUE KEY `object_id` (`service_object_id`),
  KEY `instance_id` (`instance_id`),
  KEY `status_update_time` (`status_update_time`),
  KEY `current_state` (`current_state`),
  KEY `check_type` (`check_type`),
  KEY `state_type` (`state_type`),
  KEY `last_state_change` (`last_state_change`),
  KEY `notifications_enabled` (`notifications_enabled`),
  KEY `problem_has_been_acknowledged` (`problem_has_been_acknowledged`),
  KEY `active_checks_enabled` (`active_checks_enabled`),
  KEY `passive_checks_enabled` (`passive_checks_enabled`),
  KEY `event_handler_enabled` (`event_handler_enabled`),
  KEY `flap_detection_enabled` (`flap_detection_enabled`),
  KEY `is_flapping` (`is_flapping`),
  KEY `percent_state_change` (`percent_state_change`),
  KEY `latency` (`latency`),
  KEY `execution_time` (`execution_time`),
  KEY `scheduled_downtime_depth` (`scheduled_downtime_depth`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Current service status information';

DROP TABLE IF EXISTS `nagios_service_contactgroups`;
CREATE TABLE IF NOT EXISTS `nagios_service_contactgroups` (
  `service_contactgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `service_id` int(11) NOT NULL DEFAULT '0',
  `contactgroup_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`service_contactgroup_id`),
  UNIQUE KEY `instance_id` (`service_id`,`contactgroup_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Service contact groups';

DROP TABLE IF EXISTS `nagios_service_contacts`;
CREATE TABLE IF NOT EXISTS `nagios_service_contacts` (
  `service_contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `service_id` int(11) NOT NULL DEFAULT '0',
  `contact_object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`service_contact_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`service_id`,`contact_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `nagios_statehistory`;
CREATE TABLE IF NOT EXISTS `nagios_statehistory` (
  `statehistory_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `state_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `state_time_usec` int(11) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `state_change` smallint(6) NOT NULL DEFAULT '0',
  `state` smallint(6) NOT NULL DEFAULT '0',
  `state_type` smallint(6) NOT NULL DEFAULT '0',
  `current_check_attempt` smallint(6) NOT NULL DEFAULT '0',
  `max_check_attempts` smallint(6) NOT NULL DEFAULT '0',
  `last_state` smallint(6) NOT NULL DEFAULT '-1',
  `last_hard_state` smallint(6) NOT NULL DEFAULT '-1',
  `output` varchar(255) NOT NULL DEFAULT '',
  `long_output` text NOT NULL,
  PRIMARY KEY (`statehistory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical host and service state changes';

DROP TABLE IF EXISTS `nagios_systemcommands`;
CREATE TABLE IF NOT EXISTS `nagios_systemcommands` (
  `systemcommand_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `start_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `start_time_usec` int(11) NOT NULL DEFAULT '0',
  `end_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_time_usec` int(11) NOT NULL DEFAULT '0',
  `command_line` varchar(255) NOT NULL DEFAULT '',
  `timeout` smallint(6) NOT NULL DEFAULT '0',
  `early_timeout` smallint(6) NOT NULL DEFAULT '0',
  `execution_time` double NOT NULL DEFAULT '0',
  `return_code` smallint(6) NOT NULL DEFAULT '0',
  `output` varchar(255) NOT NULL DEFAULT '',
  `long_output` text NOT NULL,
  PRIMARY KEY (`systemcommand_id`),
  KEY `instance_id` (`instance_id`),
  KEY `start_time` (`start_time`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical system commands that are executed';

DROP TABLE IF EXISTS `nagios_timedeventqueue`;
CREATE TABLE IF NOT EXISTS `nagios_timedeventqueue` (
  `timedeventqueue_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `event_type` smallint(6) NOT NULL DEFAULT '0',
  `queued_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `queued_time_usec` int(11) NOT NULL DEFAULT '0',
  `scheduled_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `recurring_event` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`timedeventqueue_id`),
  KEY `instance_id` (`instance_id`),
  KEY `event_type` (`event_type`),
  KEY `scheduled_time` (`scheduled_time`),
  KEY `object_id` (`object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Current Nagios event queue';

DROP TABLE IF EXISTS `nagios_timedevents`;
CREATE TABLE IF NOT EXISTS `nagios_timedevents` (
  `timedevent_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `event_type` smallint(6) NOT NULL DEFAULT '0',
  `queued_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `queued_time_usec` int(11) NOT NULL DEFAULT '0',
  `event_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `event_time_usec` int(11) NOT NULL DEFAULT '0',
  `scheduled_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `recurring_event` smallint(6) NOT NULL DEFAULT '0',
  `object_id` int(11) NOT NULL DEFAULT '0',
  `deletion_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `deletion_time_usec` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`timedevent_id`),
  KEY `instance_id` (`instance_id`),
  KEY `event_type` (`event_type`),
  KEY `scheduled_time` (`scheduled_time`),
  KEY `object_id` (`object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Historical events from the Nagios event queue';

DROP TABLE IF EXISTS `nagios_timeperiods`;
CREATE TABLE IF NOT EXISTS `nagios_timeperiods` (
  `timeperiod_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `config_type` smallint(6) NOT NULL DEFAULT '0',
  `timeperiod_object_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`timeperiod_id`),
  UNIQUE KEY `instance_id` (`instance_id`,`config_type`,`timeperiod_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Timeperiod definitions';

DROP TABLE IF EXISTS `nagios_timeperiod_timeranges`;
CREATE TABLE IF NOT EXISTS `nagios_timeperiod_timeranges` (
  `timeperiod_timerange_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` smallint(6) NOT NULL DEFAULT '0',
  `timeperiod_id` int(11) NOT NULL DEFAULT '0',
  `day` smallint(6) NOT NULL DEFAULT '0',
  `start_sec` int(11) NOT NULL DEFAULT '0',
  `end_sec` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`timeperiod_timerange_id`),
  UNIQUE KEY `instance_id` (`timeperiod_id`,`day`,`start_sec`,`end_sec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Timeperiod definitions';

DROP TABLE IF EXISTS `nms_graphs`;
CREATE TABLE IF NOT EXISTS `nms_graphs` (
  `nms_graphs_id` varchar(64) NOT NULL,
  `device_type_id` varchar(16) NOT NULL,
  `tablename` varchar(64) NOT NULL,
  `is_deleted` smallint(6) NOT NULL,
  PRIMARY KEY (`nms_graphs_id`),
  KEY `fk_device_type_id` (`device_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `nms_instance`;
CREATE TABLE IF NOT EXISTS `nms_instance` (
  `nms_id` varchar(64) NOT NULL,
  `nms_name` varchar(32) DEFAULT NULL,
  `longitude` varchar(32) DEFAULT NULL,
  `latitude` varchar(32) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`nms_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswATUConfigTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswATUConfigTable` (
  `odu100_eswATUConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `eswATUConfigAtuId` int(32) DEFAULT NULL,
  `eswATUConfigEntryType` int(8) DEFAULT NULL,
  `eswATUConfigPriorityVal` int(32) DEFAULT NULL,
  `eswATUConfigMacAddress` varchar(32) DEFAULT NULL,
  `eswATUConfigMemberPorts` int(10) unsigned DEFAULT NULL,
  `eswATUConfigRowStatus` int(8) DEFAULT NULL,
  PRIMARY KEY (`odu100_eswATUConfigTable_id`),
  KEY `FK_odu100_eswATUConfigTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswBadFramesTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswBadFramesTable` (
  `odu100_eswBadFramesTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `eswBadFramesPortNum` int(32) DEFAULT NULL,
  `eswBadFramesInUndersizeRx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesInFragmentsRx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesInOversizeRx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesInJabberRx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesInFCSErrRx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesOutFCSErrTx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesDeferredTx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesCollisionsTx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesLateTx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesExcessiveTx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesSingleTx` int(10) unsigned DEFAULT NULL,
  `eswBadFramesMultipleTx` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`odu100_eswBadFramesTable_id`),
  KEY `FK_odu100_eswBadFramesTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswGoodFramesTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswGoodFramesTable` (
  `odu100_eswGoodFramesTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `eswGoodFramesPortNum` int(32) DEFAULT NULL,
  `eswGoodFramesInUnicast` int(10) unsigned DEFAULT NULL,
  `eswGoodFramesOutUnicast` int(10) unsigned DEFAULT NULL,
  `eswGoodFramesInBCast` int(10) unsigned DEFAULT NULL,
  `eswGoodFramesOutBCast` int(10) unsigned DEFAULT NULL,
  `eswGoodFramesInMCast` int(10) unsigned DEFAULT NULL,
  `eswGoodFramesOutMcast` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`odu100_eswGoodFramesTable_id`),
  KEY `FK_odu100_eswGoodFramesTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswMirroringPortTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswMirroringPortTable` (
  `odu100_eswMirroringPortTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `eswMirroringPortIndexId` int(32) DEFAULT NULL,
  `eswMirroringPort` int(32) DEFAULT NULL,
  `eswMirroringPortSecond` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_eswMirroringPortTable_id`),
  KEY `FK_odu100_eswMirroringPortTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswPortAccessListTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswPortAccessListTable` (
  `odu100_eswPortAccessListTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `eswPortACLPortNum` int(32) DEFAULT NULL,
  `eswPortACLSecIndex` int(32) DEFAULT NULL,
  `eswPortACLMacAddress` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_eswPortAccessListTable_id`),
  KEY `FK_odu100_eswPortAccessListTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswPortBwTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswPortBwTable` (
  `odu100_eswPortBwTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `eswPortBwPortNum` int(32) DEFAULT NULL,
  `eswPortBwEgressBw` int(32) DEFAULT NULL,
  `eswPortBwIngressBw` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_eswPortBwTable_id`),
  KEY `FK_odu100_eswPortBwTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswPortConfigTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswPortConfigTable` (
  `odu100_eswPortConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `eswPortConfigPortNum` int(32) DEFAULT NULL,
  `eswPortConfigAdminState` int(8) DEFAULT NULL,
  `eswPortConfigLinkMode` int(8) DEFAULT NULL,
  `eswPortConfigPortVid` int(32) DEFAULT NULL,
  `eswPortConfigAuthState` int(8) DEFAULT NULL,
  `eswPortConfigMirrDir` int(8) DEFAULT NULL,
  `eswPortConfigDotqMode` int(8) DEFAULT NULL,
  `eswPortConfigMacFlowControl` int(8) DEFAULT NULL,
  PRIMARY KEY (`odu100_eswPortConfigTable_id`),
  KEY `FK_odu100_eswPortConfigTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswPortQinQTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswPortQinQTable` (
  `odu100_eswPortQinQTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `eswPortQinQPortNum` int(32) DEFAULT NULL,
  `eswPortQinQAuthState` int(8) DEFAULT NULL,
  `eswPortQinQProviderTag` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_eswPortQinQTable_id`),
  KEY `FK_odu100_eswPortQinQTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswPortStatisticsTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswPortStatisticsTable` (
  `odu100_eswPortStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `eswPortStatisticsPortNum` int(32) DEFAULT NULL,
  `eswPortStatisticsInDiscards` int(10) unsigned DEFAULT NULL,
  `eswPortStatisticsInGoodOctets` int(10) unsigned DEFAULT NULL,
  `eswPortStatisticsInBadOctets` int(32) DEFAULT NULL,
  `eswPortStatisticsOutOctets` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`odu100_eswPortStatisticsTable_id`),
  KEY `FK_odu100_eswPortStatisticsTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswPortStatusTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswPortStatusTable` (
  `odu100_eswPortStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `eswPortStatusPortNum` int(32) DEFAULT NULL,
  `eswPortStatusOpState` int(8) DEFAULT NULL,
  `eswPortStatusLinkSpeed` int(8) DEFAULT NULL,
  `eswPortStatusMacFlowControl` int(8) DEFAULT NULL,
  PRIMARY KEY (`odu100_eswPortStatusTable_id`),
  KEY `FK_odu100_eswPortStatusTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_eswVlanConfigTable`;
CREATE TABLE IF NOT EXISTS `odu100_eswVlanConfigTable` (
  `odu100_eswVlanConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `eswVlanConfigVlanId` int(32) DEFAULT NULL,
  `eswVlanConfigVlanName` varchar(8) DEFAULT NULL,
  `eswVlanConfigVlanType` int(8) DEFAULT NULL,
  `eswVlanConfigVlanTag` int(32) DEFAULT NULL,
  `eswVlanConfigMemberPorts` int(10) unsigned DEFAULT NULL,
  `eswVlanConfigRowStatus` int(8) DEFAULT NULL,
  PRIMARY KEY (`odu100_eswVlanConfigTable_id`),
  KEY `FK_odu100_eswVlanConfigTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_hwDescTable`;
CREATE TABLE IF NOT EXISTS `odu100_hwDescTable` (
  `odu100_hwDescTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `hwDescIndex` int(32) DEFAULT NULL,
  `hwVersion` varchar(128) DEFAULT NULL,
  `hwSerialNo` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`odu100_hwDescTable_id`),
  KEY `FK_odu100_hwDescTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_ipConfigTable`;
CREATE TABLE IF NOT EXISTS `odu100_ipConfigTable` (
  `odu100_ipConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ipConfigIndex` int(32) DEFAULT NULL,
  `adminState` int(8) DEFAULT NULL,
  `ipAddress` varchar(32) DEFAULT NULL,
  `ipNetworkMask` varchar(32) DEFAULT NULL,
  `ipDefaultGateway` varchar(32) DEFAULT NULL,
  `autoIpConfig` int(8) DEFAULT NULL,
  `managementMode` tinyint(4) DEFAULT NULL,
  `managementVlanTag` int(11) DEFAULT NULL,
  PRIMARY KEY (`odu100_ipConfigTable_id`),
  KEY `FK_odu100_ipConfigTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_nwInterfaceStatisticsTable`;
CREATE TABLE IF NOT EXISTS `odu100_nwInterfaceStatisticsTable` (
  `odu100_nwInterfaceStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `nwStatsIndex` enum('0','1','2') DEFAULT '0',
  `rxPackets` int(10) unsigned DEFAULT NULL,
  `txPackets` int(10) unsigned DEFAULT NULL,
  `rxBytes` int(10) unsigned DEFAULT NULL,
  `txBytes` int(10) unsigned DEFAULT NULL,
  `rxErrors` int(10) unsigned DEFAULT NULL,
  `txErrors` int(10) unsigned DEFAULT NULL,
  `rxDropped` int(10) unsigned DEFAULT NULL,
  `txDropped` int(10) unsigned DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_nwInterfaceStatisticsTable_id`,`timestamp`),
  KEY `FK_odu100_nwInterfaceStatisticsTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_nwInterfaceStatusTable`;
CREATE TABLE IF NOT EXISTS `odu100_nwInterfaceStatusTable` (
  `odu100_nwInterfaceStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `nwStatusIndex` int(32) DEFAULT NULL,
  `nwInterfaceName` varchar(16) DEFAULT NULL,
  `operationalState` int(8) DEFAULT NULL,
  `macAddress` varchar(32) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_nwInterfaceStatusTable_id`),
  KEY `FK_odu100_nwInterfaceStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `odu100_omcConfTable`;
CREATE TABLE IF NOT EXISTS `odu100_omcConfTable` (
  `odu100_omcConfTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `omcConfIndex` int(32) DEFAULT NULL,
  `omcIpAddress` varchar(32) DEFAULT NULL,
  `periodicStatsTimer` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_omcConfTable_id`),
  KEY `FK_odu100_omcConfTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_peerConfigTable`;
CREATE TABLE IF NOT EXISTS `odu100_peerConfigTable` (
  `odu100_peerConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `timeslotIndex` int(32) DEFAULT NULL,
  `peermacAddress` varchar(32) DEFAULT NULL,
  `guaranteedUplinkBW` int(32) DEFAULT NULL,
  `guaranteedDownlinkBW` int(32) DEFAULT NULL,
  `basicrateMCSIndex` int(32) DEFAULT NULL,
  `maxUplinkBW` int(11) DEFAULT NULL,
  `maxDownlinkBW` int(11) DEFAULT NULL,
  PRIMARY KEY (`odu100_peerConfigTable_id`),
  KEY `FK_odu100_peerConfigTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_peerLinkStatisticsTable`;
CREATE TABLE IF NOT EXISTS `odu100_peerLinkStatisticsTable` (
  `odu100_peerLinkStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(10) unsigned DEFAULT NULL,
  `timeslotindex` int(10) unsigned DEFAULT NULL,
  `txdroped` int(10) unsigned DEFAULT NULL,
  `rxDataSubFrames` int(10) unsigned DEFAULT NULL,
  `txDataSubFrames` int(10) unsigned DEFAULT NULL,
  `signalstrength1` int(32) DEFAULT NULL,
  `txRetransmissions5` int(10) unsigned DEFAULT NULL,
  `txRetransmissions4` int(10) unsigned DEFAULT NULL,
  `txRetransmissions3` int(10) unsigned DEFAULT NULL,
  `txRetransmissions2` int(10) unsigned DEFAULT NULL,
  `txRetransmissions1` int(10) unsigned DEFAULT NULL,
  `txRetransmissions0` int(10) unsigned DEFAULT NULL,
  `rxRetransmissions5` int(10) unsigned DEFAULT NULL,
  `rxRetransmissions4` int(10) unsigned DEFAULT NULL,
  `rxRetransmissions3` int(10) unsigned DEFAULT NULL,
  `rxRetransmissions2` int(10) unsigned DEFAULT NULL,
  `rxRetransmissions1` int(10) unsigned DEFAULT NULL,
  `rxRetransmissions0` int(10) unsigned DEFAULT NULL,
  `rxBroadcastDataSubFrames` int(10) unsigned DEFAULT NULL,
  `rateIncreases` int(10) unsigned DEFAULT NULL,
  `rateDecreases` int(10) unsigned DEFAULT NULL,
  `emptyRasters` int(10) unsigned DEFAULT NULL,
  `rxDroppedTpPkts` int(10) unsigned DEFAULT NULL,
  `rxDroppedRadioPkts` int(10) unsigned DEFAULT NULL,
  `signalstrength2` int(32) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_peerLinkStatisticsTable_id`),
  KEY `FK_odu100_peerLinkStatisticsTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_peerNodeStatusTable`;
CREATE TABLE IF NOT EXISTS `odu100_peerNodeStatusTable` (
  `odu100_peerNodeStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `timeSlotIndex` int(32) DEFAULT NULL,
  `linkStatus` int(8) DEFAULT NULL,
  `tunnelStatus` int(8) DEFAULT NULL,
  `sigStrength1` int(32) DEFAULT NULL,
  `peerMacAddr` varchar(32) DEFAULT NULL,
  `ssIdentifier` varchar(32) DEFAULT NULL,
  `peerNodeStatusNumSlaves` int(10) unsigned DEFAULT NULL,
  `peerNodeStatusrxRate` int(32) DEFAULT NULL,
  `peerNodeStatustxRate` int(32) DEFAULT NULL,
  `allocatedTxBW` int(32) DEFAULT NULL,
  `allocatedRxBW` int(32) DEFAULT NULL,
  `usedTxBW` int(32) DEFAULT NULL,
  `usedRxBW` int(32) DEFAULT NULL,
  `txbasicRate` int(32) DEFAULT NULL,
  `sigStrength2` int(32) DEFAULT NULL,
  `rxbasicRate` int(32) DEFAULT NULL,
  `txLinkQuality` int(32) DEFAULT NULL,
  `peerNodeStatustxTime` int(32) DEFAULT NULL,
  `peerNodeStatusrxTime` int(32) DEFAULT NULL,
  `negotiatedMaxUplinkBW` int(11) DEFAULT '0',
  `negotiatedMaxDownlinkBW` int(11) DEFAULT '0',
  `peerNodeStatuslinkDistance` int(11) DEFAULT '0',
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_peerNodeStatusTable_id`,`timestamp`),
  KEY `FK_odu100_peerNodeStatusTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_peerRateStatisticsTable`;
CREATE TABLE IF NOT EXISTS `odu100_peerRateStatisticsTable` (
  `odu100_peerRateStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `mcsIndex` int(32) DEFAULT NULL,
  `timeSlotindex` int(32) DEFAULT NULL,
  `peerrate` int(10) unsigned DEFAULT NULL,
  `per` int(32) DEFAULT NULL,
  `ticks` int(10) unsigned DEFAULT NULL,
  `ticksMinimumRateTx` int(10) unsigned DEFAULT NULL,
  `ticksWasted` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`odu100_peerRateStatisticsTable_id`),
  KEY `FK_odu100_peerRateStatisticsTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_peerTunnelStatisticsTable`;
CREATE TABLE IF NOT EXISTS `odu100_peerTunnelStatisticsTable` (
  `odu100_peerTunnelStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `tsIndex` int(32) DEFAULT NULL,
  `rxPacket` int(10) unsigned DEFAULT NULL,
  `txPacket` int(10) unsigned DEFAULT NULL,
  `rxBundles` int(10) unsigned DEFAULT NULL,
  `txBundles` int(10) unsigned DEFAULT NULL,
  `rxDroped` int(10) unsigned DEFAULT NULL,
  `txDroped` int(10) unsigned DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_peerTunnelStatisticsTable_id`),
  KEY `FK_odu100_peerTunnelStatisticsTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raAclConfigTable`;
CREATE TABLE IF NOT EXISTS `odu100_raAclConfigTable` (
  `odu100_raAclConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `aclIndex` int(32) DEFAULT NULL,
  `macaddress` varchar(32) DEFAULT NULL,
  `rowSts` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_raAclConfigTable_id`),
  KEY `FK_odu100_raAclConfigTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raChannelListTable`;
CREATE TABLE IF NOT EXISTS `odu100_raChannelListTable` (
  `odu100_raChannelListTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `raChanIndex` int(32) DEFAULT NULL,
  `channelNumber` int(32) DEFAULT NULL,
  `frequency` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_raChannelListTable_id`),
  KEY `FK_odu100_raChannelListTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raConfTable`;
CREATE TABLE IF NOT EXISTS `odu100_raConfTable` (
  `odu100_raConfTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `raAdminState` int(8) DEFAULT NULL,
  `aclMode` int(8) DEFAULT NULL,
  `ssID` varchar(32) DEFAULT NULL,
  `guaranteedBroadcastBW` int(32) DEFAULT NULL,
  `dba` int(8) DEFAULT NULL,
  `acm` int(8) DEFAULT NULL,
  `acs` int(8) DEFAULT NULL,
  `dfs` int(8) DEFAULT NULL,
  `numSlaves` int(32) DEFAULT NULL,
  `antennaPort` int(8) DEFAULT NULL,
  `linkDistance` int(10) NOT NULL DEFAULT '0',
  `anc` int(8) DEFAULT NULL,
  PRIMARY KEY (`odu100_raConfTable_id`),
  KEY `FK_odu100_raConfTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raLlcConfTable`;
CREATE TABLE IF NOT EXISTS `odu100_raLlcConfTable` (
  `odu100_raLlcConfTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `arqWinLow` int(32) DEFAULT NULL,
  `arqWinHigh` int(32) DEFAULT NULL,
  `frameLossThreshold` int(32) DEFAULT NULL,
  `leakyBucketTimerVal` int(32) DEFAULT NULL,
  `frameLossTimeout` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_raLlcConfTable_id`),
  KEY `FK_odu100_raLlcConfTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raPreferredRFChannelTable`;
CREATE TABLE IF NOT EXISTS `odu100_raPreferredRFChannelTable` (
  `odu100_raPreferredRFChannelTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `preindex` int(32) DEFAULT NULL,
  `preindex1` int(32) DEFAULT NULL,
  `rafrequency` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_raPreferredRFChannelTable_id`),
  KEY `FK_odu100_raPreferredRFChannelTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raScanListTable`;
CREATE TABLE IF NOT EXISTS `odu100_raScanListTable` (
  `odu100_raScanListTable_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` tinyint(4) DEFAULT NULL,
  `raScanIndex` tinyint(4) DEFAULT NULL,
  `ssid` varchar(32) DEFAULT NULL,
  `signalStrength` int(32) DEFAULT NULL,
  `macAddr` varchar(32) DEFAULT NULL,
  `rastertime` int(32) DEFAULT NULL,
  `timeslot` int(32) DEFAULT NULL,
  `maxSlaves` int(32) DEFAULT NULL,
  `channelNum` int(32) DEFAULT NULL,
  `basicRate` int(32) DEFAULT NULL,
  `radfs` int(8) DEFAULT NULL,
  `raacm` int(8) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_raScanListTable_id`,`timestamp`),
  KEY `FK_odu100_raScanListTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raSiteSurveyResultTable`;
CREATE TABLE IF NOT EXISTS `odu100_raSiteSurveyResultTable` (
  `odu100_raSiteSurveyResultTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `scanIndex` int(32) DEFAULT NULL,
  `scanIndex1` int(32) DEFAULT NULL,
  `rfChannelFrequency` int(32) DEFAULT NULL,
  `numCrcErrors` int(32) DEFAULT NULL,
  `maxRslCrcError` int(32) DEFAULT NULL,
  `numPhyErrors` int(32) DEFAULT NULL,
  `maxRslPhyError` int(32) DEFAULT NULL,
  `maxRslValidFrames` int(32) DEFAULT NULL,
  `channelnumber` int(32) DEFAULT NULL,
  `noiseFloor` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_raSiteSurveyResultTable_id`),
  KEY `FK_odu100_raSiteSurveyResultTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raStatusTable`;
CREATE TABLE IF NOT EXISTS `odu100_raStatusTable` (
  `odu100_raStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `currentTimeSlot` int(32) DEFAULT NULL,
  `raMacAddress` varchar(32) DEFAULT NULL,
  `raoperationalState` int(8) DEFAULT NULL,
  `unusedTxTimeUL` int(32) DEFAULT NULL,
  `unusedTxTimeDL` int(32) DEFAULT NULL,
  `ancStatus` enum('0','1') DEFAULT NULL,
  `ancHwAvailable` enum('0','1') DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_raStatusTable_id`),
  KEY `FK_odu100_raStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 ;

DROP TABLE IF EXISTS `odu100_raTddMacConfigTable`;
CREATE TABLE IF NOT EXISTS `odu100_raTddMacConfigTable` (
  `odu100_raTddMacConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `passPhrase` varchar(64) DEFAULT NULL,
  `txPower` int(32) DEFAULT NULL,
  `maxPower` int(32) DEFAULT NULL,
  `maxCrcErrors` int(32) DEFAULT NULL,
  `leakyBucketTimerValue` int(32) DEFAULT NULL,
  `encryptionType` int(8) DEFAULT NULL,
  PRIMARY KEY (`odu100_raTddMacConfigTable_id`),
  KEY `FK_odu100_raTddMacConfigTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raTddMacStatisticsTable`;
CREATE TABLE IF NOT EXISTS `odu100_raTddMacStatisticsTable` (
  `odu100_raTddMacStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(10) unsigned DEFAULT NULL,
  `rxpackets` int(10) unsigned DEFAULT NULL,
  `txpackets` int(10) unsigned DEFAULT NULL,
  `rxerrors` int(10) unsigned DEFAULT NULL,
  `txerrors` int(10) unsigned DEFAULT NULL,
  `rxdropped` int(10) unsigned DEFAULT NULL,
  `txdropped` int(10) unsigned DEFAULT NULL,
  `rxCrcErrors` int(10) unsigned DEFAULT NULL,
  `rxPhyError` int(10) unsigned DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_raTddMacStatisticsTable_id`,`timestamp`),
  KEY `FK_odu100_raTddMacStatisticsTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raTddMacStatusTable`;
CREATE TABLE IF NOT EXISTS `odu100_raTddMacStatusTable` (
  `odu100_raTddMacStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `rfChanFreq` int(32) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_raTddMacStatusTable_id`),
  KEY `FK_odu100_raTddMacStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_raValidPhyRatesTable`;
CREATE TABLE IF NOT EXISTS `odu100_raValidPhyRatesTable` (
  `odu100_raValidPhyRatesTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `raIndex` int(32) DEFAULT NULL,
  `mcsindex` int(32) DEFAULT NULL,
  `spatialStreams` int(32) DEFAULT NULL,
  `modulationType` int(8) DEFAULT NULL,
  `codingRate` int(8) DEFAULT NULL,
  `rate` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_raValidPhyRatesTable_id`),
  KEY `FK_odu100_raValidPhyRatesTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_ruConfTable`;
CREATE TABLE IF NOT EXISTS `odu100_ruConfTable` (
  `odu100_ruConfTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `confIndex` int(32) DEFAULT NULL,
  `adminstate` int(8) DEFAULT NULL,
  `defaultNodeType` int(8) DEFAULT NULL,
  `channelBandwidth` int(8) DEFAULT NULL,
  `synchSource` int(8) DEFAULT NULL,
  `countryCode` int(8) DEFAULT NULL,
  `poeState` int(8) DEFAULT NULL,
  `alignmentControl` int(32) DEFAULT NULL,
  `ethFiltering` int(2) NOT NULL,
  `poePort2State` int(8) DEFAULT NULL,
  `poePort4State` int(8) DEFAULT NULL,
  `poePort6State` int(8) DEFAULT NULL,
  PRIMARY KEY (`odu100_ruConfTable_id`),
  KEY `FK_odu100_ruConfTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_ruDateTimeTable`;
CREATE TABLE IF NOT EXISTS `odu100_ruDateTimeTable` (
  `odu100_ruDateTimeTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `dateIndex` int(16) DEFAULT NULL,
  `year` int(16) DEFAULT NULL,
  `month` int(16) DEFAULT NULL,
  `day` int(16) DEFAULT NULL,
  `hour` int(16) DEFAULT NULL,
  `min` int(16) DEFAULT NULL,
  `sec` int(16) DEFAULT NULL,
  PRIMARY KEY (`odu100_ruDateTimeTable_id`),
  KEY `FK_odu100_ruDateTimeTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_ruOmOperationsTable`;
CREATE TABLE IF NOT EXISTS `odu100_ruOmOperationsTable` (
  `odu100_ruOmOperationsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `omIndex` int(32) DEFAULT NULL,
  `omOperationReq` int(8) DEFAULT NULL,
  `userName` varchar(16) DEFAULT NULL,
  `password` varchar(16) DEFAULT NULL,
  `ftpServerAddress` varchar(32) DEFAULT NULL,
  `pathName` varchar(128) DEFAULT NULL,
  `omOperationResult` int(8) DEFAULT NULL,
  `omSpecificCause` int(8) DEFAULT NULL,
  `listOfChannels` varchar(256) DEFAULT NULL,
  `txTime` int(32) DEFAULT NULL,
  `txRate` int(32) DEFAULT NULL,
  `txBW` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_ruOmOperationsTable_id`),
  KEY `FK_odu100_ruOmOperationsTable` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_ruStatusTable`;
CREATE TABLE IF NOT EXISTS `odu100_ruStatusTable` (
  `odu100_ruStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `statusIndex` int(32) DEFAULT NULL,
  `lastRebootReason` int(32) DEFAULT NULL,
  `isConfigCommitedToFlash` int(16) DEFAULT NULL,
  `upTime` int(10) unsigned DEFAULT NULL,
  `poeStatus` int(8) DEFAULT NULL,
  `cpuId` int(8) DEFAULT NULL,
  `ruoperationalState` int(8) DEFAULT NULL,
  `nodeBandwidth` int(11) DEFAULT NULL,
  `poePort2Status` int(8) DEFAULT NULL,
  `poePort4Status` int(8) DEFAULT NULL,
  `poePort6Status` int(8) DEFAULT NULL,
  PRIMARY KEY (`odu100_ruStatusTable_id`),
  KEY `FK_odu100_ruStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;



DROP TABLE IF EXISTS `odu100_swStatusTable`;
CREATE TABLE IF NOT EXISTS `odu100_swStatusTable` (
  `odu100_swStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `swStatusIndex` int(32) DEFAULT NULL,
  `activeVersion` varchar(32) DEFAULT NULL,
  `passiveVersion` varchar(32) DEFAULT NULL,
  `bootloaderVersion` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`odu100_swStatusTable_id`),
  KEY `FK_odu100_swStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `odu100_ipFilterTable`;
CREATE TABLE IF NOT EXISTS `odu100_ipFilterTable` (
  `odu100_ipFilterTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `ipFilterIndex` int(10) DEFAULT NULL,
  `ipFilterIpAddress` varchar(16) DEFAULT NULL,
  `ipFilterNetworkMask` varchar(16) NOT NULL DEFAULT '255.255.255.0',
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_ipFilterTable_id`),
  KEY `FK_odu100_ipFilterTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `odu100_macFilterTable`;
CREATE TABLE IF NOT EXISTS `odu100_macFilterTable` (
  `odu100_macFilterTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `macFilterIndex` int(10) DEFAULT NULL,
  `filterMacAddress` varchar(19) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_macFilterTable_id`),
  KEY `FK_odu100_macFilterTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;





DROP TABLE IF EXISTS `odu100_syncConfigTable`;
CREATE TABLE IF NOT EXISTS `odu100_syncConfigTable` (
  `odu100_syncConfigTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `syncConfigIndex` int(32) DEFAULT NULL,
  `adminStatus` int(8) DEFAULT NULL,
  `synchState` int(8) DEFAULT NULL,
  `rasterTime` int(32) DEFAULT NULL,
  `syncLossThreshold` int(32) DEFAULT NULL,
  `leakyBucketTimer` int(32) DEFAULT NULL,
  `syncLostTimeout` int(32) DEFAULT NULL,
  `syncConfigTimerAdjust` int(32) DEFAULT NULL,
  `percentageDownlinkTransmitTime` int(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_syncConfigTable_id`),
  KEY `FK_odu100_syncConfigTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_synchStatisticsTable`;
CREATE TABLE IF NOT EXISTS `odu100_synchStatisticsTable` (
  `odu100_synchStatisticsTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `synchStatsIndex` int(32) DEFAULT NULL,
  `syncLostCounter` int(10) unsigned DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_synchStatisticsTable_id`,`timestamp`),
  KEY `FK_odu100_synchStatisticsTable` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_synchStatusTable`;
CREATE TABLE IF NOT EXISTS `odu100_synchStatusTable` (
  `odu100_synchStatusTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `synchStatsIndex` int(32) DEFAULT NULL,
  `syncoperationalState` int(8) DEFAULT NULL,
  `syncrasterTime` int(32) DEFAULT NULL,
  `timerAdjust` int(32) DEFAULT NULL,
  `syncpercentageDownlinkTransmitTime` int(32) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`odu100_synchStatusTable_id`),
  KEY `FK_odu100_synchStatusTable` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu100_sysOmcRegistrationTable`;
CREATE TABLE IF NOT EXISTS `odu100_sysOmcRegistrationTable` (
  `odu100_sysOmcRegistrationTable_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `sysOmcRegistrationIndex` int(32) DEFAULT NULL,
  `sysOmcRegisterContactAddr` varchar(32) DEFAULT NULL,
  `sysOmcRegisterContactPerson` varchar(32) DEFAULT NULL,
  `sysOmcRegisterContactMobile` varchar(32) DEFAULT NULL,
  `sysOmcRegisterAlternateContact` varchar(32) DEFAULT NULL,
  `sysOmcRegisterContactEmail` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`odu100_sysOmcRegistrationTable_id`),
  KEY `FK_odu100_sysOmcRegistrationTable` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu_host_schedule`;
CREATE TABLE IF NOT EXISTS `odu_host_schedule` (
  `odu_schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `schedule_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `is_success` tinyint(4) NOT NULL DEFAULT '1',
  `firmware_file_name` varchar(500) NOT NULL,
  `message` varchar(200) NOT NULL,
  PRIMARY KEY (`odu_schedule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `odu_schedule`;
CREATE TABLE IF NOT EXISTS `odu_schedule` (
  `schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(16) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `is_repeated` smallint(6) DEFAULT NULL,
  `repeat_type` varchar(16) DEFAULT NULL,
  `sun` smallint(6) DEFAULT NULL,
  `mon` smallint(6) DEFAULT NULL,
  `tue` smallint(6) DEFAULT NULL,
  `wed` smallint(6) DEFAULT NULL,
  `thu` smallint(6) DEFAULT NULL,
  `fri` smallint(6) DEFAULT NULL,
  `sat` smallint(6) DEFAULT NULL,
  `jan` smallint(6) DEFAULT NULL,
  `feb` smallint(6) DEFAULT NULL,
  `mar` smallint(6) DEFAULT NULL,
  `apr` smallint(6) DEFAULT NULL,
  `may` smallint(6) DEFAULT NULL,
  `jun` smallint(6) DEFAULT NULL,
  `jul` smallint(6) DEFAULT NULL,
  `aug` smallint(6) DEFAULT NULL,
  `sept` smallint(6) DEFAULT NULL,
  `oct` smallint(6) DEFAULT NULL,
  `nov` smallint(6) DEFAULT NULL,
  `dece` smallint(6) DEFAULT NULL,
  `day` smallint(6) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NULL DEFAULT NULL,
  `updated_by` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  `is_success` tinyint(4) NOT NULL DEFAULT '0',
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`schedule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `odu100_7_2_20_oids`;
CREATE TABLE IF NOT EXISTS `odu100_7_2_20_oids` (
  `oid_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_type_id` varchar(16) DEFAULT NULL,
  `oid` varchar(256) DEFAULT NULL,
  `oid_name` varchar(256) DEFAULT NULL,
  `oid_type` varchar(16) DEFAULT NULL,
  `access` smallint(6) DEFAULT NULL,
  `default_value` varchar(256) DEFAULT NULL,
  `min_value` varchar(128) DEFAULT NULL,
  `max_value` varchar(256) DEFAULT NULL,
  `indexes` varchar(256) DEFAULT NULL,
  `dependent_id` int(10) unsigned DEFAULT NULL,
  `multivalue` smallint(6) DEFAULT '0',
  `table_name` varchar(128) DEFAULT NULL,
  `coloumn_name` varchar(128) DEFAULT NULL,
  `indexes_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`oid_id`),
  KEY `FK_oids` (`device_type_id`),
  KEY `FK_oids_dependant_id` (`dependent_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=242 ;

-- --------------------------------------------------------

--
-- Table structure for table `odu100_7_2_20_oids_multivalues`
--
DROP TABLE IF EXISTS `odu100_7_2_20_oids_multivalues`;
CREATE TABLE IF NOT EXISTS `odu100_7_2_20_oids_multivalues` (
  `oids_multivalue_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `oid_id` int(10) unsigned DEFAULT NULL,
  `value` varchar(128) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`oids_multivalue_id`),
  KEY `FK_oids_multivalues` (`oid_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=131 ;

-- --------------------------------------------------------

--
-- Table structure for table `odu100_7_2_20_oid_table`
--
DROP TABLE IF EXISTS `odu100_7_2_20_oid_table`;
CREATE TABLE IF NOT EXISTS `odu100_7_2_20_oid_table` (
  `table_name` varchar(64) NOT NULL,
  `table_oid` varchar(64) NOT NULL,
  `varbinds` tinyint(4) NOT NULL DEFAULT '15',
  `is_recon` int(11) NOT NULL DEFAULT '1' COMMENT '1 = run reconciliation for table',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '0 = reconciliation has not been run',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `odu100_7_2_25_oids`
--
DROP TABLE IF EXISTS `odu100_7_2_25_oids`;
CREATE TABLE IF NOT EXISTS `odu100_7_2_25_oids` (
  `oid_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_type_id` varchar(16) DEFAULT NULL,
  `oid` varchar(256) DEFAULT NULL,
  `oid_name` varchar(256) DEFAULT NULL,
  `oid_type` varchar(16) DEFAULT NULL,
  `access` smallint(6) DEFAULT NULL,
  `default_value` varchar(256) DEFAULT NULL,
  `min_value` varchar(128) DEFAULT NULL,
  `max_value` varchar(256) DEFAULT NULL,
  `indexes` varchar(256) DEFAULT NULL,
  `dependent_id` int(10) unsigned DEFAULT NULL,
  `multivalue` smallint(6) DEFAULT '0',
  `table_name` varchar(128) DEFAULT NULL,
  `coloumn_name` varchar(128) DEFAULT NULL,
  `indexes_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`oid_id`),
  KEY `FK_oids` (`device_type_id`),
  KEY `FK_oids_dependant_id` (`dependent_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=262 ;

-- --------------------------------------------------------

--
-- Table structure for table `odu100_7_2_25_oids_multivalues`
--
DROP TABLE IF EXISTS `odu100_7_2_25_oids_multivalues`;
CREATE TABLE IF NOT EXISTS `odu100_7_2_25_oids_multivalues` (
  `oids_multivalue_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `oid_id` int(10) unsigned DEFAULT NULL,
  `value` varchar(128) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`oids_multivalue_id`),
  KEY `FK_oids_multivalues` (`oid_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=167 ;

-- --------------------------------------------------------

--
-- Table structure for table `odu100_7_2_25_oid_table`
--
DROP TABLE IF EXISTS `odu100_7_2_25_oid_table`;
CREATE TABLE IF NOT EXISTS `odu100_7_2_25_oid_table` (
  `table_name` varchar(64) NOT NULL,
  `table_oid` varchar(64) NOT NULL,
  `varbinds` tinyint(4) NOT NULL DEFAULT '15',
  `is_recon` int(11) NOT NULL DEFAULT '1' COMMENT '1 = run reconciliation for table',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '0 = reconciliation has not been run',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------




DROP TABLE IF EXISTS `pages`;
CREATE TABLE IF NOT EXISTS `pages` (
  `page_id` varchar(64) NOT NULL,
  `page_name` varchar(64) DEFAULT NULL,
  `page_link_id` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `snapin_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`page_id`),
  KEY `FK_pages` (`snapin_id`),
  KEY `FK_pages_link` (`page_link_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `pages_link`;
CREATE TABLE IF NOT EXISTS `pages_link` (
  `pages_link_id` varchar(64) NOT NULL,
  `page_link` varchar(256) DEFAULT NULL,
  `is_deleted` smallint(6) DEFAULT '0',
  PRIMARY KEY (`pages_link_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `priority`;
CREATE TABLE IF NOT EXISTS `priority` (
  `priority_id` varchar(16) NOT NULL,
  `priority_name` varchar(32) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `sequence` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`priority_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `report_query_dict`;
CREATE TABLE IF NOT EXISTS `report_query_dict` (
  `report_query_dict_id` int(11) NOT NULL AUTO_INCREMENT,
  `device_type` varchar(32) NOT NULL,
  `report_type` varchar(32) NOT NULL,
  `columns` varchar(2000) NOT NULL,
  `table_name` varchar(200) NOT NULL,
  `join` varchar(1000) NOT NULL,
  `where` varchar(500) NOT NULL,
  `group_by` varchar(1000) NOT NULL,
  `order_by` varchar(100) NOT NULL,
  `group_the_data` enum('0','1') NOT NULL DEFAULT '0',
  `find_delta` enum('0','1') NOT NULL DEFAULT '0',
  `default_data` enum('0','1') NOT NULL DEFAULT '0',
  `group_the_data_variables` varchar(100) NOT NULL,
  `find_delta_variables` varchar(100) NOT NULL,
  `default_data_variables` varchar(100) NOT NULL,
  `group_the_data_details` varchar(500) NOT NULL,
  `find_delta_details` varchar(500) NOT NULL,
  `default_data_details` varchar(500) NOT NULL,
  PRIMARY KEY (`report_query_dict_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `report_query_dict_analyzed`;
CREATE TABLE IF NOT EXISTS `report_query_dict_analyzed` (
  `report_query_dict_analyzed_id` int(11) NOT NULL AUTO_INCREMENT,
  `device_type` varchar(32) NOT NULL,
  `report_type` varchar(32) NOT NULL,
  `range_type` varchar(10) NOT NULL,
  `columns` varchar(10000) NOT NULL,
  `table_name` varchar(200) NOT NULL,
  `join` varchar(1000) NOT NULL,
  `where` varchar(500) NOT NULL,
  `group_by` varchar(1000) NOT NULL,
  `order_by` varchar(100) NOT NULL,
  PRIMARY KEY (`report_query_dict_analyzed_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `report_template`;
CREATE TABLE IF NOT EXISTS `report_template` (
  `template_id` int(11) NOT NULL AUTO_INCREMENT,
  `template_name` varchar(32) NOT NULL,
  `device_type` varchar(20) NOT NULL,
  `report_type` varchar(20) NOT NULL,
  `report_name` varchar(32) NOT NULL,
  `column_selected` varchar(500) DEFAULT NULL,
  `mapping_selected` varchar(500) DEFAULT NULL,
  `column_non_selected` varchar(500) DEFAULT NULL,
  `mapping_non_selected` varchar(500) DEFAULT NULL,
  `sheet_name` varchar(20) DEFAULT NULL,
  `main_title` varchar(20) DEFAULT NULL,
  `second_title` varchar(40) DEFAULT NULL,
  `created_by` varchar(32) DEFAULT NULL,
  `generate_method` enum('0','1') NOT NULL DEFAULT '0',
  PRIMARY KEY (`template_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `report_template_analyzed`;
CREATE TABLE IF NOT EXISTS `report_template_analyzed` (
  `template_id` int(11) NOT NULL AUTO_INCREMENT,
  `template_name` varchar(100) NOT NULL,
  `device_type` varchar(20) NOT NULL,
  `report_type` varchar(100) NOT NULL,
  `report_name` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `column_selected` varchar(5000) DEFAULT NULL,
  `mapping_selected` varchar(5000) DEFAULT NULL,
  `column_non_selected` varchar(500) DEFAULT NULL,
  `mapping_non_selected` varchar(500) DEFAULT NULL,
  `sheet_name` varchar(100) DEFAULT NULL,
  `main_title` varchar(20) DEFAULT NULL,
  `second_title` varchar(40) DEFAULT NULL,
  `created_by` varchar(32) DEFAULT NULL,
  `generate_method` enum('0','1') NOT NULL DEFAULT '0',
  PRIMARY KEY (`template_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `retry_ap_scheduling`;
CREATE TABLE IF NOT EXISTS `retry_ap_scheduling` (
  `retry_ap_scheduling_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `retry_date` date DEFAULT NULL,
  `retry_time` time DEFAULT NULL,
  `host_id` int(10) unsigned DEFAULT NULL,
  `message` varchar(256) DEFAULT NULL,
  `event` varchar(16) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`retry_ap_scheduling_id`),
  KEY `FK_retry_ap_scheduling` (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `role_id` varchar(64) NOT NULL,
  `role_name` varchar(64) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `parent_id` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `is_default` tinyint(4) NOT NULL DEFAULT '1',
  `updated_by` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `role_pages_link`;
CREATE TABLE IF NOT EXISTS `role_pages_link` (
  `role_pages_link_id` varchar(64) NOT NULL,
  `role_id` varchar(64) DEFAULT NULL,
  `pages_link_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`role_pages_link_id`),
  KEY `FK_role_pages_link` (`role_id`),
  KEY `FK_role_role_pages_link` (`pages_link_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `scheduling`;
CREATE TABLE IF NOT EXISTS `scheduling` (
  `scheduling_id` varchar(8) NOT NULL,
  `scheduling_name` varchar(16) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `sequence` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`scheduling_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `service_templates`;
CREATE TABLE IF NOT EXISTS `service_templates` (
  `service_template_id` varchar(64) NOT NULL,
  `device_type_id` varchar(16) DEFAULT NULL,
  `template_name` varchar(32) DEFAULT NULL,
  `service_description` varchar(64) DEFAULT NULL,
  `check_command` varchar(256) DEFAULT NULL,
  `max_check_attempts` int(8) DEFAULT NULL,
  `normal_check_interval` int(8) DEFAULT NULL,
  `retry_check_interval` int(8) DEFAULT NULL,
  `remark` varchar(256) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`service_template_id`),
  KEY `FK_service_templates` (`device_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_ip_config_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_ip_config_table` (
  `set_odu16_ip_config_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `admin_state` smallint(6) DEFAULT NULL,
  `ip_address` varchar(16) NOT NULL,
  `ip_network_mask` varchar(16) NOT NULL,
  `ip_default_gateway` varchar(16) NOT NULL,
  `auto_ip_config` int(16) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_ip_config_table_id`),
  KEY `FK_set_ru_ip_config_table` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_misc`;
CREATE TABLE IF NOT EXISTS `set_odu16_misc` (
  `set_odu16_misc_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `sys_contact` varchar(256) DEFAULT NULL,
  `sys_name` varchar(256) DEFAULT NULL,
  `sys_location` varchar(256) DEFAULT NULL,
  `snmp_enable_authen_traps` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_misc_id`),
  KEY `FK_set_odu16_misc` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_network_interface_config_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_network_interface_config_table` (
  `set_odu16_network_interface_config_entry_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ssid` varchar(32) DEFAULT NULL,
  `index` int(16) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_network_interface_config_entry_id`),
  KEY `FK_set_ru_network_interface_config_table` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_omc_conf_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_omc_conf_table` (
  `set_odu16_omc_conf_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `omc_ip_address` varchar(32) DEFAULT NULL,
  `periodic_stats_timer` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`set_odu16_omc_conf_table_id`),
  KEY `FK_set_ru_omc_conf_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_om_operations_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_om_operations_table` (
  `set_odu16_om_operations_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `om_operation_req` int(8) DEFAULT NULL,
  `user_name` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `ftp_server_address` varchar(32) DEFAULT NULL,
  `path_name` varchar(256) DEFAULT NULL,
  `enable_swam` int(8) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_om_operations_table_id`),
  KEY `FK_set_ru_om_operations_table` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_peer_config_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_peer_config_table` (
  `set_odu16_peer_config_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `peer_mac_address` text,
  `index` int(16) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_peer_config_table_id`),
  KEY `FK_set_ru_peer_config_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_ra_acl_config_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_ra_acl_config_table` (
  `set_odu16_ra_acl_config_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `mac_address` text,
  `index` int(16) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_ra_acl_config_table_id`),
  KEY `FK_set_ru_ra_acl_config_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_ra_conf_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_ra_conf_table` (
  `set_odu16_ra_conf_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `raAdminState` smallint(6) DEFAULT NULL,
  `acl_mode` smallint(6) DEFAULT NULL,
  `ssid` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_ra_conf_table_id`),
  KEY `FK_set_ru_ra_conf_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_ra_llc_conf_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_ra_llc_conf_table` (
  `set_odu16_ra_llc_conf_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `llc_arq_enable` smallint(6) DEFAULT NULL,
  `arq_win` int(10) unsigned DEFAULT NULL,
  `frame_loss_threshold` int(10) unsigned DEFAULT NULL,
  `leaky_bucket_timer_val` int(10) unsigned DEFAULT NULL,
  `frame_loss_timeout` int(32) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_ra_llc_conf_table_id`),
  KEY `FK_set_ru_ra_llc_conf_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_ra_tdd_mac_config`;
CREATE TABLE IF NOT EXISTS `set_odu16_ra_tdd_mac_config` (
  `set_odu16_ra_tdd_mac_config_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `rf_channel_frequency` int(32) DEFAULT NULL,
  `pass_phrase` varchar(64) DEFAULT NULL,
  `rfcoding` smallint(6) DEFAULT NULL,
  `tx_power` int(10) unsigned DEFAULT NULL,
  `max_power` int(10) unsigned DEFAULT NULL,
  `max_crc_errors` int(10) unsigned DEFAULT NULL,
  `leaky_bucket_timer_value` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`set_odu16_ra_tdd_mac_config_table_id`),
  KEY `FK_set_ru_ra_tdd_mac_config` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_ru_conf_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_ru_conf_table` (
  `set_odu16_ru_conf_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `adminstate` smallint(6) DEFAULT NULL,
  `channel_bandwidth` int(8) DEFAULT NULL,
  `sysnch_source` int(8) DEFAULT NULL,
  `country_code` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_ru_conf_table_id`),
  KEY `FK_set_ru_conf_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_ru_date_time_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_ru_date_time_table` (
  `set_odu16_ru_date_time_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `year` int(8) DEFAULT NULL,
  `month` int(8) DEFAULT NULL,
  `day` int(8) DEFAULT NULL,
  `hour` int(8) DEFAULT NULL,
  `min` int(8) DEFAULT NULL,
  `sec` int(8) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_ru_date_time_table_id`),
  KEY `FK_set_ru_date_time_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_sync_config_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_sync_config_table` (
  `set_odu16_sync_config_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `adminStatus` smallint(6) DEFAULT NULL,
  `raster_time` int(32) DEFAULT NULL,
  `num_slaves` int(32) DEFAULT NULL,
  `sync_loss_threshold` int(10) unsigned DEFAULT NULL,
  `leaky_bucket_timer` int(10) unsigned DEFAULT NULL,
  `sync_lost_timeout` int(10) unsigned DEFAULT NULL,
  `sync_config_time_adjust` int(32) DEFAULT NULL,
  `sync_config_broadcast_enable` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_sync_config_table_id`),
  KEY `FK_set_ru_sync_config_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `set_odu16_sys_omc_registration_table`;
CREATE TABLE IF NOT EXISTS `set_odu16_sys_omc_registration_table` (
  `set_odu16_sys_omc_registration_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `sys_omc_register_contact_addr` varchar(128) DEFAULT NULL,
  `sys_omc_register_contact_person` varchar(32) DEFAULT NULL,
  `sys_omc_register_contact_mobile` varchar(16) DEFAULT NULL,
  `sys_omc_register_alternate_contact` varchar(64) DEFAULT NULL,
  `sys_omc_register_contact_email` varchar(64) DEFAULT NULL,
  `sys_omc_register_active_card_hwld` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_site_direction` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_site_landmark` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_site_latitude` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_site_longitude` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_state` varchar(32) DEFAULT NULL,
  `sys_omc_register_country` varchar(32) DEFAULT NULL,
  `sys_omc_register_city` varchar(32) DEFAULT NULL,
  `sys_omc_register_sitebldg` varchar(32) DEFAULT NULL,
  `sys_omc_registersitefloor` varchar(32) DEFAULT NULL,
  `site_mac` varchar(32) DEFAULT NULL,
  `product_id` int(16) DEFAULT NULL,
  PRIMARY KEY (`set_odu16_sys_omc_registration_table_id`),
  KEY `FK_set_ru _sys_omc_registration_table` (`config_profile_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `sites`;
CREATE TABLE IF NOT EXISTS `sites` (
  `site_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `site_name` varchar(64) DEFAULT NULL,
  `ip_address` varchar(32) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `updated_by` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `snapins`;
CREATE TABLE IF NOT EXISTS `snapins` (
  `snapin_id` varchar(64) NOT NULL,
  `snapin_name` varchar(64) DEFAULT NULL,
  `author` varchar(32) NOT NULL DEFAULT 'cscape',
  `description` varchar(128) DEFAULT NULL,
  `is_menu` smallint(6) DEFAULT '0',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`snapin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `snmp_advance_options`;
CREATE TABLE IF NOT EXISTS `snmp_advance_options` (
  `snmp_advance_option_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) unsigned DEFAULT NULL,
  `discovery_id` int(10) unsigned DEFAULT NULL,
  `snmp_username` varchar(64) DEFAULT NULL,
  `snmp_password` varchar(64) DEFAULT NULL,
  `authentication_key` varchar(64) DEFAULT NULL,
  `authentication_protocol` varchar(64) DEFAULT NULL,
  `private_password` varchar(64) DEFAULT NULL,
  `private_key` varchar(64) DEFAULT NULL,
  `private_protocol` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`snmp_advance_option_id`),
  KEY `FK_snmp_advance_options_hosts` (`host_id`),
  KEY `FK_snmp_advance_options_discovery` (`discovery_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `states`;
CREATE TABLE IF NOT EXISTS `states` (
  `state_id` varchar(64) NOT NULL,
  `state_name` varchar(64) DEFAULT NULL,
  `country_id` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`state_id`),
  KEY `FK_states` (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_1p_remarking`;
CREATE TABLE IF NOT EXISTS `swt4_1p_remarking` (
  `switch_1p_remarking_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `p_remarking` tinyint(4) NOT NULL,
  `p802_remarking` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_1p_remarking_id`),
  KEY `FK_switch_1p_remarking` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_802_1p_based_priority`;
CREATE TABLE IF NOT EXISTS `swt4_802_1p_based_priority` (
  `switch_802_1p_based_priority_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `p802` tinyint(4) NOT NULL,
  `priority` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_802_1p_based_priority_id`),
  KEY `FK_switch_802_1p_based_priority` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_bandwidth_control`;
CREATE TABLE IF NOT EXISTS `swt4_bandwidth_control` (
  `switch_bandwidth_control_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `cpu_protection` int(11) NOT NULL,
  `port` tinyint(4) NOT NULL,
  `type` tinyint(4) NOT NULL,
  `state` tinyint(4) NOT NULL,
  `rate` int(11) NOT NULL,
  PRIMARY KEY (`switch_bandwidth_control_id`),
  KEY `FK_switch_bandwidth_control` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_dscp_based_priority`;
CREATE TABLE IF NOT EXISTS `swt4_dscp_based_priority` (
  `switch_dscp_based_priority_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `dscp` varchar(8) NOT NULL,
  `priority` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_dscp_based_priority_id`),
  KEY `FK_switch_dscp_based_priority` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_igmp_snooping`;
CREATE TABLE IF NOT EXISTS `swt4_igmp_snooping` (
  `switch_igmp_snooping_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `igmp_snooping` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_igmp_snooping_id`),
  KEY `FK_switch_igmp_snooping` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_information`;
CREATE TABLE IF NOT EXISTS `swt4_information` (
  `switch_information_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `device_type` varchar(18) NOT NULL,
  `serial_no` varchar(18) NOT NULL,
  `mac_address` varchar(18) NOT NULL,
  `ip_address` varchar(15) NOT NULL,
  `subnet_mask` varchar(15) NOT NULL,
  `gateway` varchar(15) NOT NULL,
  `firmware_version` varchar(18) NOT NULL,
  `hardware_version` varchar(18) NOT NULL,
  `boot_loader_version` varchar(8) NOT NULL,
  `current_location` varchar(12) NOT NULL,
  `system_uptime` varchar(32) NOT NULL,
  PRIMARY KEY (`switch_information_id`),
  KEY `FK_switch_information` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_ip_base_priority`;
CREATE TABLE IF NOT EXISTS `swt4_ip_base_priority` (
  `swt4_ip_base_priority_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `ip_base_priority` int(8) DEFAULT NULL,
  `ip_type` int(8) DEFAULT NULL,
  `ip_address` varchar(16) DEFAULT NULL,
  `network_mask` varchar(16) DEFAULT NULL,
  `priority` int(8) DEFAULT NULL,
  PRIMARY KEY (`swt4_ip_base_priority_id`),
  KEY `FK_swt4_ip_base_priority` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_ip_settings`;
CREATE TABLE IF NOT EXISTS `swt4_ip_settings` (
  `switch_ip_settings_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `mode` varchar(12) NOT NULL,
  `ip_address` varchar(15) NOT NULL,
  `subnet_mask` varchar(15) NOT NULL,
  `gateway` varchar(15) NOT NULL,
  PRIMARY KEY (`switch_ip_settings_id`),
  KEY `FK_switch_ip_settings` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_mac_address_table`;
CREATE TABLE IF NOT EXISTS `swt4_mac_address_table` (
  `switch_mac_address_table_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `type` tinyint(4) NOT NULL,
  `mac_address` tinyint(4) NOT NULL,
  `entry` tinyint(4) NOT NULL,
  `port` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_mac_address_table_id`),
  UNIQUE KEY `FK_switch_mac_address_table` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_packet_scheduling`;
CREATE TABLE IF NOT EXISTS `swt4_packet_scheduling` (
  `switch_packet_scheduling_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `scheduling_algorithm` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_packet_scheduling_id`),
  KEY `FK_switch_packet_scheduling` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_port_based_priority`;
CREATE TABLE IF NOT EXISTS `swt4_port_based_priority` (
  `switch_port_based_priority_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `port` tinyint(4) NOT NULL,
  `priority` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_port_based_priority_id`),
  KEY `FK_switch_port_based_priority` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_port_mapping`;
CREATE TABLE IF NOT EXISTS `swt4_port_mapping` (
  `switch_port_mapping_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `mirror_direction` tinyint(4) NOT NULL,
  `mirroring_port` tinyint(4) NOT NULL,
  `mirrored_port_list` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_port_mapping_id`),
  KEY `FK_switch_port_mapping` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_port_mirroring`;
CREATE TABLE IF NOT EXISTS `swt4_port_mirroring` (
  `swt4_port_mirroring_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `mirror_direction` smallint(6) NOT NULL,
  `mirroring_port_list` smallint(6) NOT NULL,
  `mirrored_port_list` smallint(6) NOT NULL,
  PRIMARY KEY (`swt4_port_mirroring_id`),
  UNIQUE KEY `FK_swt4_port_mirroring` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_port_settings`;
CREATE TABLE IF NOT EXISTS `swt4_port_settings` (
  `swt4_port_settings_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `link_fault_pass_through` smallint(6) NOT NULL,
  `port` smallint(6) NOT NULL,
  `state` smallint(6) NOT NULL,
  `speed` smallint(6) NOT NULL,
  `flow_control` smallint(6) NOT NULL,
  PRIMARY KEY (`swt4_port_settings_id`),
  KEY `FK_switch_port_settings` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_port_statistics`;
CREATE TABLE IF NOT EXISTS `swt4_port_statistics` (
  `switch_port_statistics_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `port` tinyint(4) NOT NULL,
  `state` tinyint(4) NOT NULL,
  `speed` tinyint(4) NOT NULL,
  `flow_control` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_port_statistics_id`),
  KEY `FK_switch_port_statistics` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_qos_arbitration`;
CREATE TABLE IF NOT EXISTS `swt4_qos_arbitration` (
  `switch_qos_arbitration_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `priority` varchar(15) NOT NULL,
  `level` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_qos_arbitration_id`),
  KEY `FK_switch_qos_arbitration` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_queue_based_priority`;
CREATE TABLE IF NOT EXISTS `swt4_queue_based_priority` (
  `switch_queue_based_priority_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `qid_map` tinyint(4) NOT NULL,
  `priority` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_queue_based_priority_id`),
  KEY `FK_switch_queue_based_priority` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_queue_weight_based`;
CREATE TABLE IF NOT EXISTS `swt4_queue_weight_based` (
  `switch_queue_weight_based` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `queue` tinyint(4) NOT NULL,
  `weight` tinyint(4) NOT NULL,
  PRIMARY KEY (`switch_queue_weight_based`),
  KEY `FK_switch_queue_weight_based` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_storm_control`;
CREATE TABLE IF NOT EXISTS `swt4_storm_control` (
  `switch_storm_control_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `strom_type` tinyint(4) NOT NULL,
  `state` tinyint(4) NOT NULL,
  `rate` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`switch_storm_control_id`),
  KEY `FK_switch_storm_control` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `swt4_vlan_settings`;
CREATE TABLE IF NOT EXISTS `swt4_vlan_settings` (
  `swt4_vlan_settings_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `config_profile_id` int(10) unsigned DEFAULT NULL,
  `vlan_ingress_filter` smallint(6) NOT NULL,
  `vlan_pass_all` smallint(6) NOT NULL,
  `port` smallint(6) NOT NULL,
  `pvid` smallint(6) NOT NULL,
  `mode` smallint(6) NOT NULL,
  PRIMARY KEY (`swt4_vlan_settings_id`),
  KEY `FK_swt4_vlan_settings` (`config_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `system_alarm_table`;
CREATE TABLE IF NOT EXISTS `system_alarm_table` (
  `system_alarm_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` int(10) DEFAULT NULL,
  `event_id` varchar(32) DEFAULT NULL,
  `trap_id` varchar(32) DEFAULT NULL,
  `agent_id` varchar(32) DEFAULT NULL,
  `trap_date` varchar(32) DEFAULT NULL,
  `trap_receive_date` varchar(32) DEFAULT NULL,
  `serevity` int(16) DEFAULT NULL,
  `trap_event_id` varchar(32) DEFAULT NULL,
  `trap_event_type` varchar(32) DEFAULT NULL,
  `manage_obj_id` varchar(32) DEFAULT NULL,
  `manage_obj_name` varchar(32) DEFAULT NULL,
  `component_id` varchar(32) DEFAULT NULL,
  `trap_ip` varchar(32) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`system_alarm_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tcp_discovery`;
CREATE TABLE IF NOT EXISTS `tcp_discovery` (
  `ne_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sys_omc_register_contact_addr` varchar(128) DEFAULT NULL,
  `sys_omc_register_contact_person` varchar(32) DEFAULT NULL,
  `sys_omc_register_contact_mobile` varchar(16) DEFAULT NULL,
  `sys_omc_register_alternate_contact` varchar(64) DEFAULT NULL,
  `sys_omc_register_contact_email` varchar(64) DEFAULT NULL,
  `sys_omc_register_active_card_hwld` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_site_direction` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_site_landmark` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_site_latitude` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_site_longitude` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_state` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_country` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_city` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_sitebldg` varchar(32) DEFAULT NULL,
  `sys_omc_registerne_sitefloor` varchar(32) DEFAULT NULL,
  `site_mac` varchar(32) DEFAULT NULL,
  `product_id` int(16) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ip_address` varchar(32) DEFAULT NULL,
  `is_set` smallint(6) NOT NULL DEFAULT '1',
  PRIMARY KEY (`ne_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tcp_health_check`;
CREATE TABLE IF NOT EXISTS `tcp_health_check` (
  `tcp_health_check_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ne_id` int(10) unsigned DEFAULT NULL,
  `health_check` int(64) DEFAULT '0',
  `ip_address` varchar(32) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`tcp_health_check_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `total_count_item`;
CREATE TABLE IF NOT EXISTS `total_count_item` (
  `user_id` varchar(64) NOT NULL,
  `graph_id` varchar(64) NOT NULL,
  `url` varchar(128) NOT NULL,
  `method` varchar(16) NOT NULL,
  `other_data` varchar(128) NOT NULL,
  KEY `graph_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `trap_alarms`;
CREATE TABLE IF NOT EXISTS `trap_alarms` (
  `trap_alarm_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_id` varchar(32) DEFAULT NULL,
  `trap_id` varchar(32) DEFAULT NULL,
  `agent_id` varchar(32) DEFAULT NULL,
  `trap_date` varchar(32) DEFAULT NULL,
  `trap_receive_date` varchar(32) DEFAULT NULL,
  `serevity` int(16) DEFAULT NULL,
  `trap_event_id` varchar(32) DEFAULT NULL,
  `trap_event_type` varchar(32) DEFAULT NULL,
  `manage_obj_id` varchar(32) DEFAULT NULL,
  `manage_obj_name` varchar(32) DEFAULT NULL,
  `component_id` varchar(32) DEFAULT NULL,
  `trap_ip` varchar(32) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `device_sent_date` datetime NOT NULL,
  `is_reconcile` enum('0','1') NOT NULL DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`trap_alarm_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `trap_alarm_action_mapping`;
CREATE TABLE IF NOT EXISTS `trap_alarm_action_mapping` (
  `trap_alarm_action_mapping_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `trap_alarm_masking_id` int(10) unsigned DEFAULT NULL,
  `acknowledge_id` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` varchar(64) DEFAULT NULL,
  `next_scheduling` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`trap_alarm_action_mapping_id`),
  KEY `FK_trap_alarm_action_mapping` (`trap_alarm_masking_id`),
  KEY `FK_trap_alarm_action_mapping_ack` (`acknowledge_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `trap_alarm_clear`;
CREATE TABLE IF NOT EXISTS `trap_alarm_clear` (
  `trap_alarm_clear_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_id` varchar(32) DEFAULT NULL,
  `trap_id` varchar(32) DEFAULT NULL,
  `agent_id` varchar(32) DEFAULT NULL,
  `trap_date` varchar(32) DEFAULT NULL,
  `trap_receive_date` varchar(32) DEFAULT NULL,
  `serevity` int(16) DEFAULT NULL,
  `trap_event_id` varchar(32) DEFAULT NULL,
  `trap_event_type` varchar(32) DEFAULT NULL,
  `manage_obj_id` varchar(32) DEFAULT NULL,
  `manage_obj_name` varchar(32) DEFAULT NULL,
  `component_id` varchar(32) DEFAULT NULL,
  `trap_ip` varchar(32) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `device_sent_date` datetime NOT NULL,
  `is_reconcile` enum('0','1') NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`trap_alarm_clear_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `trap_alarm_current`;
CREATE TABLE IF NOT EXISTS `trap_alarm_current` (
  `trap_alarm_current_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_id` varchar(32) DEFAULT NULL,
  `trap_id` varchar(32) DEFAULT NULL,
  `agent_id` varchar(32) DEFAULT NULL,
  `trap_date` varchar(32) DEFAULT NULL,
  `trap_receive_date` varchar(32) DEFAULT NULL,
  `serevity` int(16) DEFAULT NULL,
  `trap_event_id` varchar(32) DEFAULT NULL,
  `trap_event_type` varchar(32) DEFAULT NULL,
  `manage_obj_id` varchar(32) DEFAULT NULL,
  `manage_obj_name` varchar(32) DEFAULT NULL,
  `component_id` varchar(32) DEFAULT NULL,
  `trap_ip` varchar(32) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `device_sent_date` datetime NOT NULL,
  `is_reconcile` enum('0','1') NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`trap_alarm_current_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `trap_alarm_field_table`;
CREATE TABLE IF NOT EXISTS `trap_alarm_field_table` (
  `trap_alarm_field` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `field_name` varchar(32) NOT NULL,
  `field_type` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`trap_alarm_field`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `trap_alarm_masking`;
CREATE TABLE IF NOT EXISTS `trap_alarm_masking` (
  `trap_alarm_masking_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `trap_alarm_field` int(10) unsigned DEFAULT '0',
  `trap_alarm_value` varchar(128) DEFAULT NULL,
  `action_id` varchar(64) DEFAULT NULL,
  `group_id` varchar(64) DEFAULT NULL,
  `scheduling_minutes` int(16) DEFAULT NULL,
  `is_repeated` smallint(6) DEFAULT NULL,
  `description` text,
  `acknowledge_id` varchar(16) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` varchar(64) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`trap_alarm_masking_id`),
  KEY `FK_trap_alarm_masking` (`group_id`),
  KEY `FK_trap_alarm_masking_actions` (`action_id`),
  KEY `FK_trap_alarm_masking_ack` (`acknowledge_id`),
  KEY `FK_trap_alarm_masking_field` (`trap_alarm_field`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `trap_id_mapping`;
CREATE TABLE IF NOT EXISTS `trap_id_mapping` (
  `trap_id_mapping_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `trap_event_type` varchar(32) DEFAULT NULL,
  `trap_event_id` varchar(32) DEFAULT NULL,
  `is_alarm` smallint(6) DEFAULT NULL,
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `trap_clear_mapping_id` varchar(32) DEFAULT NULL,
  `trap_clear_mapping_type` varchar(32) DEFAULT NULL,
  `device_type` varchar(20) NOT NULL DEFAULT 'ubr',
  `trap_severity` int(2) NOT NULL DEFAULT '9',
  `clear_severity` int(2) NOT NULL DEFAULT '9',
  `priority_id` varchar(16) DEFAULT 'high',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT 'a',
  `creation_time` timestamp NULL DEFAULT NULL,
  `updated_by` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`trap_id_mapping_id`),
  KEY `FK_trap_id_mapping` (`priority_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` varchar(64) NOT NULL,
  `first_name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `designation` varchar(64) DEFAULT NULL,
  `company_name` varchar(64) DEFAULT NULL,
  `mobile_no` varchar(16) DEFAULT NULL,
  `address` varchar(128) DEFAULT NULL,
  `city_id` varchar(64) DEFAULT NULL,
  `state_id` varchar(64) DEFAULT NULL,
  `country_id` varchar(64) DEFAULT NULL,
  `email_id` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `users_groups`;
CREATE TABLE IF NOT EXISTS `users_groups` (
  `user_group_id` varchar(64) NOT NULL,
  `user_id` varchar(64) DEFAULT NULL,
  `group_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`user_group_id`),
  KEY `FK_users_groups` (`group_id`),
  KEY `FK_users_groups_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `user_login`;
CREATE TABLE IF NOT EXISTS `user_login` (
  `user_login_id` varchar(64) NOT NULL,
  `user_id` varchar(64) DEFAULT NULL,
  `user_name` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(64) DEFAULT NULL,
  `creation_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0',
  `updated_by` varchar(64) DEFAULT NULL,
  `nms_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`user_login_id`),
  KEY `FK_user_login` (`user_id`),
  KEY `FK_user_login_nms_instance` (`nms_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `alarm_recon`
  ADD CONSTRAINT `alarm_recon_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;
  
ALTER TABLE `ap25_accesspointIPsettings`
  ADD CONSTRAINT `ap25_accesspointIPsettings_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_aclMacTable`
  ADD CONSTRAINT `ap25_aclMacTable_ibfk_1` FOREIGN KEY (`vapselection_id`) REFERENCES `ap25_basicVAPconfigTable` (`vapselection_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ap25_aclMacTable_ibfk_2` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_aclStatisticsTable`
  ADD CONSTRAINT `ap25_aclStatisticsTable_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_basicACLconfigTable`
  ADD CONSTRAINT `ap25_basicACLconfigTable_ibfk_1` FOREIGN KEY (`vapselection_id`) REFERENCES `ap25_vapSelection` (`ap25_vapSelection_id`),
  ADD CONSTRAINT `ap25_basicACLconfigTable_ibfk_3` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ap25_basicACLconfigTable_ibfk_4` FOREIGN KEY (`vapselection_id`) REFERENCES `ap25_vapSelection` (`ap25_vapSelection_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_basicConfiguration`
  ADD CONSTRAINT `ap25_basicConfiguration_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_basicVAPconfigTable`
  ADD CONSTRAINT `ap25_basicVAPconfigTable_ibfk_2` FOREIGN KEY (`vapselection_id`) REFERENCES `ap25_vapSelection` (`ap25_vapSelection_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ap25_basicVAPconfigTable_ibfk_4` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ap25_basicVAPconfigTable_ibfk_5` FOREIGN KEY (`vapselection_id`) REFERENCES `ap25_vapSelection` (`ap25_vapSelection_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_basicVAPsecurity`
  ADD CONSTRAINT `ap25_basicVAPsecurity_ibfk_1` FOREIGN KEY (`vapselection_id`) REFERENCES `ap25_vapSelection` (`ap25_vapSelection_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ap25_basicVAPsecurity_ibfk_2` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_dhcpServer`
  ADD CONSTRAINT `ap25_dhcpServer_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_oids`
  ADD CONSTRAINT `FK_ap25_oids` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_ap25_oids_dependant_id` FOREIGN KEY (`dependent_id`) REFERENCES `ap25_oids` (`oid_id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `ap25_radioSelection`
  ADD CONSTRAINT `ap25_radioSelection_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_radioSetup`
  ADD CONSTRAINT `ap25_radioSetup_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_services`
  ADD CONSTRAINT `ap25_services_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_vapSelection`
  ADD CONSTRAINT `ap25_vapSelection_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_vapWEPsecurityConfigTable`
  ADD CONSTRAINT `ap25_vapWEPsecurityConfigTable_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_vapWPAsecurityConfigTable`
  ADD CONSTRAINT `ap25_vapWPAsecurityConfigTable_ibfk_2` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ap25_vapWPAsecurityConfigTable_ibfk_3` FOREIGN KEY (`vapselection_id`) REFERENCES `ap25_vapSelection` (`ap25_vapSelection_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap25_versions`
  ADD CONSTRAINT `ap25_versions_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap_client_ap_data`
  ADD CONSTRAINT `ap_client_ap_data_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `host_status` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap_connected_client`
  ADD CONSTRAINT `ap_connected_client_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `ap_scheduling_host_mapping`
  ADD CONSTRAINT `FK_ap_scheduling_host_mapping_host` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_ap_scheduling_host_mapping_scheduling` FOREIGN KEY (`ap_scheduling_id`) REFERENCES `ap_scheduling` (`ap_scheduling_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuAlarmAndThresholdTable`
--
ALTER TABLE `ccu_ccuAlarmAndThresholdTable`
  ADD CONSTRAINT `ccu_ccuAlarmAndThresholdTable_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuAuxIOTable`
--
ALTER TABLE `ccu_ccuAuxIOTable`
  ADD CONSTRAINT `ccu_ccuAuxIOTable_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuBatteryPanelConfigTable`
--
ALTER TABLE `ccu_ccuBatteryPanelConfigTable`
  ADD CONSTRAINT `ccu_ccuBatteryPanelConfigTable_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuControlTable`
--
ALTER TABLE `ccu_ccuControlTable`
  ADD CONSTRAINT `ccu_ccuControlTable_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuInformationTable`
--
ALTER TABLE `ccu_ccuInformationTable`
  ADD CONSTRAINT `ccu_ccuInformationTable_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuNetworkConfigurationTable`
--
ALTER TABLE `ccu_ccuNetworkConfigurationTable`
  ADD CONSTRAINT `ccu_ccuNetworkConfigurationTable_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuPeerInformationTable`
--
ALTER TABLE `ccu_ccuPeerInformationTable`
  ADD CONSTRAINT `ccu_ccuPeerInformationTable_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuRealTimeStatusTable`
--
ALTER TABLE `ccu_ccuRealTimeStatusTable`
  ADD CONSTRAINT `ccu_ccuRealTimeStatusTable_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuSiteInformationTable`
--
ALTER TABLE `ccu_ccuSiteInformationTable`
  ADD CONSTRAINT `ccu_ccuSiteInformationTable_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuSoftwareInformationTable`
--
ALTER TABLE `ccu_ccuSoftwareInformationTable`
  ADD CONSTRAINT `ccu_ccuSoftwareInformationTable_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ccu_ccuStatusDataTable`
--
ALTER TABLE `ccu_ccuStatusDataTable`
  ADD CONSTRAINT `ccu_ccuStatusDataTable_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `cities`
  ADD CONSTRAINT `FK_cities_states` FOREIGN KEY (`state_id`) REFERENCES `states` (`state_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `config_profiles`
  ADD CONSTRAINT `FK_odu_config_profiles_device_type` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_odu_config_profiles_type` FOREIGN KEY (`config_profile_type_id`) REFERENCES `config_profile_type` (`config_profile_type_id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `discovered_hosts`
  ADD CONSTRAINT `FK_discovered_hosts` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_discovered_hosts_discovery` FOREIGN KEY (`discovery_id`) REFERENCES `discovery` (`discovery_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `discovery`
  ADD CONSTRAINT `FK_discovery` FOREIGN KEY (`scheduling_id`) REFERENCES `scheduling` (`scheduling_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_discovery_type` FOREIGN KEY (`discovery_type_id`) REFERENCES `discovery_type` (`discovery_type_id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `get_ap25_bandwidth`
  ADD CONSTRAINT `FK_get_ap25_bandwidth_hosts` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_ap25_connected_user`
  ADD CONSTRAINT `FK_get_ap25_connected_user_hosts` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_ap25_misc`
  ADD CONSTRAINT `FK_get_ap25_misc` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_active_alarm_table`
  ADD CONSTRAINT `FK_get_odu16_active_alarm_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_hw_desc_table`
  ADD CONSTRAINT `FK_get_odu16_hw_desc_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_misc`
  ADD CONSTRAINT `FK_get_odu16_misc` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_network_interface_status_table`
  ADD CONSTRAINT `FK_get_odu16_network_interface_status_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_nw_interface_status_table`
  ADD CONSTRAINT `FK_get_odu16_nw_interface_status_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_peer_link_statistics_table`
  ADD CONSTRAINT `FK_get_odu16_peer_link_statistics_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_peer_tunnel_statistics_table`
  ADD CONSTRAINT `FK_get_odu16_peer_tunnel_statistics_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_ra_channel_list_table`
  ADD CONSTRAINT `FK_get_odu16_ra_channel_list_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_ra_conf_table`
  ADD CONSTRAINT `FK_get_odu16_ra_conf_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_ra_scan_list_table`
  ADD CONSTRAINT `FK_get_odu16_ra_scan_list_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_ra_status_table`
  ADD CONSTRAINT `FK_get_odu16_ra_status_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_ra_tdd_mac_status_table`
  ADD CONSTRAINT `FK_get_odu16_ra_tdd_mac_status_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_ru_conf_table`
  ADD CONSTRAINT `FK_get_odu16_ru_conf_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_ru_om_operations_table`
  ADD CONSTRAINT `FK_get_odu16_ru_om_operations_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_ru_status_table`
  ADD CONSTRAINT `FK_get_odu16_ru_status_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_snmp`
  ADD CONSTRAINT `FK_get_odu16_snmp` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_sw_status_table`
  ADD CONSTRAINT `FK_get_odu16_sw_status_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `get_odu16_sync_config_table`
  ADD CONSTRAINT `FK_get_odu16_sync_config_table` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `graph_ajax_call_information`
  ADD CONSTRAINT `graph_ajax_call_information_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `graph_calculation_table`
  ADD CONSTRAINT `graph_calculation_table_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `graph_field_table`
  ADD CONSTRAINT `graph_field_table_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `graph_interface_table`
  ADD CONSTRAINT `graph_interface_table_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `graph_templet_table`
  ADD CONSTRAINT `graph_templet_table_foregin_key` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `groups`
  ADD CONSTRAINT `FK_groups` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `hostgroups_groups`
  ADD CONSTRAINT `FK_hostgroups_groups_groups` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hostgroups_groups_hostgroups` FOREIGN KEY (`hostgroup_id`) REFERENCES `hostgroups` (`hostgroup_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `firmware_mapping`
  ADD CONSTRAINT `FK_firmware_mapping` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `hosts`
  ADD CONSTRAINT `FK_hosts_assets` FOREIGN KEY (`host_asset_id`) REFERENCES `host_assets` (`host_asset_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hosts_device_type` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hosts_nms_instance` FOREIGN KEY (`nms_id`) REFERENCES `nms_instance` (`nms_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hosts_os` FOREIGN KEY (`host_os_id`) REFERENCES `host_os` (`host_os_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hosts_priority` FOREIGN KEY (`priority_id`) REFERENCES `priority` (`priority_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hosts_sites` FOREIGN KEY (`site_id`) REFERENCES `sites` (`site_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hosts_states` FOREIGN KEY (`host_state_id`) REFERENCES `host_states` (`host_state_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hosts_vendors` FOREIGN KEY (`host_vendor_id`) REFERENCES `host_vendor` (`host_vendor_id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `hosts_hostgroups`
  ADD CONSTRAINT `FK_hosts_hostgroups_hostgroups` FOREIGN KEY (`hostgroup_id`) REFERENCES `hostgroups` (`hostgroup_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_hosts_hostgroups_hosts` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `host_alert_action_mapping`
  ADD CONSTRAINT `FK_host_alert_action_mapping` FOREIGN KEY (`host_alert_masking_id`) REFERENCES `host_alert_masking` (`host_alert_masking_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_host_alert_action_mapping_ack` FOREIGN KEY (`acknowlegde_id`) REFERENCES `acknowledge` (`acknowledge_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `host_alert_masking`
  ADD CONSTRAINT `FK_host_alert_masking_ack` FOREIGN KEY (`acknowledge_id`) REFERENCES `acknowledge` (`acknowledge_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_host_alert_masking_action` FOREIGN KEY (`action_id`) REFERENCES `actions` (`action_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_host_alert_masking_group_groups` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `host_services`
  ADD CONSTRAINT `FK_host_services` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `host_status`
  ADD CONSTRAINT `host_status_host_id` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `host_status_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_aclportTable`
  ADD CONSTRAINT `FK_idu_aclportTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_alarmOutConfigTable`
  ADD CONSTRAINT `FK_idu_alarmOutConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_alarmPortConfigurationTable`
  ADD CONSTRAINT `FK_idu_alarmPortConfigurationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_atuconfigTable`
  ADD CONSTRAINT `FK_idu_atuconfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_e1PortConfigurationTable`
  ADD CONSTRAINT `FK_idu_e1PortConfigurationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_iduAdminStateTable`
  ADD CONSTRAINT `FK_idu_iduAdminStateTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_iduInfoTable`
  ADD CONSTRAINT `FK_idu_iduInfoTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_iduOmOperationsTable`
  ADD CONSTRAINT `FK_idu_iduOmOperationsTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_linkConfigurationTable`
  ADD CONSTRAINT `FK_idu_linkConfigurationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_linkStatisticsTable`
  ADD CONSTRAINT `FK_idu_linkStatisticsTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_mirroringportTable`
  ADD CONSTRAINT `FK_idu_mirroringportTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_networkConfigurationsTable`
  ADD CONSTRAINT `FK_idu_networkConfigurationsTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_oids`
  ADD CONSTRAINT `FK_idu_oids` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_idu_oids_dependant_id` FOREIGN KEY (`dependent_id`) REFERENCES `idu_oids` (`oid_id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `idu_oids_multivalues`
  ADD CONSTRAINT `FK_idu_oids_multivalues` FOREIGN KEY (`oid_id`) REFERENCES `idu_oids` (`oid_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_omcConfigurationTable`
  ADD CONSTRAINT `FK_idu_omcConfigurationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_poeConfigurationTable`
  ADD CONSTRAINT `FK_idu_poeConfigurationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_portBwTable`
  ADD CONSTRAINT `FK_idu_portBwTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_portqinqTable`
  ADD CONSTRAINT `FK_idu_portqinqTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_portstatbadframeTable`
  ADD CONSTRAINT `FK_idu_portstatbadframeTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_portstatgoodframeTable`
  ADD CONSTRAINT `FK_idu_portstatgoodframeTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_rtcConfigurationTable`
  ADD CONSTRAINT `FK_idu_rtcConfigurationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_sectorIdentificationTable`
  ADD CONSTRAINT `FK_idu_sectorIdentificationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_switchPortconfigTable`
  ADD CONSTRAINT `FK_idu_switchPortconfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_switchportstatusTable`
  ADD CONSTRAINT `FK_idu_switchportstatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_swStatusTable`
  ADD CONSTRAINT `FK_idu_swStatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_sysOmcRegistrationTable`
  ADD CONSTRAINT `FK_idu_sysOmcRegistrationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_tdmoipNetworkInterfaceConfigurationTable`
  ADD CONSTRAINT `FK_idu_tdmoipNetworkInterfaceConfigurationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_temperatureSensorConfigurationTable`
  ADD CONSTRAINT `FK_idu_temperatureSensorConfigurationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `idu_vlanconfigTable`
  ADD CONSTRAINT `FK_idu_vlanconfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `modules`
  ADD CONSTRAINT `FK_modules_page` FOREIGN KEY (`page_id`) REFERENCES `pages` (`page_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_modules_page_link` FOREIGN KEY (`page_link_id`) REFERENCES `pages_link` (`pages_link_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswATUConfigTable`
  ADD CONSTRAINT `FK_odu100_eswATUConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswBadFramesTable`
  ADD CONSTRAINT `FK_odu100_eswBadFramesTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswGoodFramesTable`
  ADD CONSTRAINT `FK_odu100_eswGoodFramesTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswMirroringPortTable`
  ADD CONSTRAINT `FK_odu100_eswMirroringPortTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswPortAccessListTable`
  ADD CONSTRAINT `FK_odu100_eswPortAccessListTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswPortBwTable`
  ADD CONSTRAINT `FK_odu100_eswPortBwTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswPortConfigTable`
  ADD CONSTRAINT `FK_odu100_eswPortConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswPortQinQTable`
  ADD CONSTRAINT `FK_odu100_eswPortQinQTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswPortStatisticsTable`
  ADD CONSTRAINT `FK_odu100_eswPortStatisticsTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswPortStatusTable`
  ADD CONSTRAINT `FK_odu100_eswPortStatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_eswVlanConfigTable`
  ADD CONSTRAINT `FK_odu100_eswVlanConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_hwDescTable`
  ADD CONSTRAINT `FK_odu100_hwDescTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_ipConfigTable`
  ADD CONSTRAINT `FK_odu100_ipConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_nwInterfaceStatusTable`
  ADD CONSTRAINT `FK_odu100_nwInterfaceStatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_omcConfTable`
  ADD CONSTRAINT `FK_odu100_omcConfTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_peerConfigTable`
  ADD CONSTRAINT `FK_odu100_peerConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_peerLinkStatisticsTable`
  ADD CONSTRAINT `FK_odu100_peerLinkStatisticsTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_peerRateStatisticsTable`
  ADD CONSTRAINT `FK_odu100_peerRateStatisticsTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_peerTunnelStatisticsTable`
  ADD CONSTRAINT `FK_odu100_peerTunnelStatisticsTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raAclConfigTable`
  ADD CONSTRAINT `FK_odu100_raAclConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raChannelListTable`
  ADD CONSTRAINT `FK_odu100_raChannelListTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raConfTable`
  ADD CONSTRAINT `FK_odu100_raConfTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raLlcConfTable`
  ADD CONSTRAINT `FK_odu100_raLlcConfTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raPreferredRFChannelTable`
  ADD CONSTRAINT `FK_odu100_raPreferredRFChannelTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raSiteSurveyResultTable`
  ADD CONSTRAINT `FK_odu100_raSiteSurveyResultTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raStatusTable`
  ADD CONSTRAINT `FK_odu100_raStatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raTddMacConfigTable`
  ADD CONSTRAINT `FK_odu100_raTddMacConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raTddMacStatusTable`
  ADD CONSTRAINT `FK_odu100_raTddMacStatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_raValidPhyRatesTable`
  ADD CONSTRAINT `FK_odu100_raValidPhyRatesTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_ruConfTable`
  ADD CONSTRAINT `FK_odu100_ruConfTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_ruDateTimeTable`
  ADD CONSTRAINT `FK_odu100_ruDateTimeTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_ruOmOperationsTable`
  ADD CONSTRAINT `FK_odu100_ruOmOperationsTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_ruStatusTable`
  ADD CONSTRAINT `FK_odu100_ruStatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_swStatusTable`
  ADD CONSTRAINT `FK_odu100_swStatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_syncConfigTable`
  ADD CONSTRAINT `FK_odu100_syncConfigTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_synchStatusTable`
  ADD CONSTRAINT `FK_odu100_synchStatusTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_sysOmcRegistrationTable`
  ADD CONSTRAINT `FK_odu100_sysOmcRegistrationTable` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `pages`
  ADD CONSTRAINT `FK_pages` FOREIGN KEY (`snapin_id`) REFERENCES `snapins` (`snapin_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_pages_link` FOREIGN KEY (`page_link_id`) REFERENCES `pages_link` (`pages_link_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `retry_ap_scheduling`
  ADD CONSTRAINT `FK_retry_ap_scheduling` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `role_pages_link`
  ADD CONSTRAINT `FK_role_pages_link` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_role_role_pages_link` FOREIGN KEY (`pages_link_id`) REFERENCES `pages_link` (`pages_link_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `service_templates`
  ADD CONSTRAINT `FK_service_templates` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_ip_config_table`
  ADD CONSTRAINT `FK_set_ru_ip_config_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_misc`
  ADD CONSTRAINT `FK_set_odu16_misc` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_network_interface_config_table`
  ADD CONSTRAINT `FK_set_ru_network_interface_config_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_omc_conf_table`
  ADD CONSTRAINT `FK_set_ru_omc_conf_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_om_operations_table`
  ADD CONSTRAINT `FK_set_ru_om_operations_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_peer_config_table`
  ADD CONSTRAINT `FK_set_ru_peer_config_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_ra_acl_config_table`
  ADD CONSTRAINT `FK_set_ru_ra_acl_config_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_ra_conf_table`
  ADD CONSTRAINT `FK_set_ru_ra_conf_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_ra_llc_conf_table`
  ADD CONSTRAINT `FK_set_ru_ra_llc_conf_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_ra_tdd_mac_config`
  ADD CONSTRAINT `FK_set_ru_ra_tdd_mac_config` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_ru_conf_table`
  ADD CONSTRAINT `FK_set_ru_conf_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_ru_date_time_table`
  ADD CONSTRAINT `FK_set_ru_date_time_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_sync_config_table`
  ADD CONSTRAINT `FK_set_ru_sync_config_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `set_odu16_sys_omc_registration_table`
  ADD CONSTRAINT `FK_set_ru _sys_omc_registration_table` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `snmp_advance_options`
  ADD CONSTRAINT `FK_snmp_advance_options_discovery` FOREIGN KEY (`discovery_id`) REFERENCES `discovery` (`discovery_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_snmp_advance_options_hosts` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `states`
  ADD CONSTRAINT `FK_states` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_1p_remarking`
  ADD CONSTRAINT `swt4_1p_remarking_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_802_1p_based_priority`
  ADD CONSTRAINT `swt4_802_1p_based_priority_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_bandwidth_control`
  ADD CONSTRAINT `swt4_bandwidth_control_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_dscp_based_priority`
  ADD CONSTRAINT `swt4_dscp_based_priority_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_igmp_snooping`
  ADD CONSTRAINT `swt4_igmp_snooping_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_information`
  ADD CONSTRAINT `swt4_information_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_ip_base_priority`
  ADD CONSTRAINT `FK_swt4_ip_base_priority` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_ip_settings`
  ADD CONSTRAINT `swt4_ip_settings_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_mac_address_table`
  ADD CONSTRAINT `swt4_mac_address_table_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_packet_scheduling`
  ADD CONSTRAINT `swt4_packet_scheduling_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_port_based_priority`
  ADD CONSTRAINT `swt4_port_based_priority_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_port_mapping`
  ADD CONSTRAINT `swt4_port_mapping_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_port_mirroring`
  ADD CONSTRAINT `swt4_port_mirroring_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_port_settings`
  ADD CONSTRAINT `swt4_port_settings_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_port_statistics`
  ADD CONSTRAINT `swt4_port_statistics_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_qos_arbitration`
  ADD CONSTRAINT `swt4_qos_arbitration_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_queue_based_priority`
  ADD CONSTRAINT `swt4_queue_based_priority_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_queue_weight_based`
  ADD CONSTRAINT `swt4_queue_weight_based_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_storm_control`
  ADD CONSTRAINT `swt4_storm_control_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `swt4_vlan_settings`
  ADD CONSTRAINT `swt4_vlan_settings_ibfk_1` FOREIGN KEY (`config_profile_id`) REFERENCES `config_profiles` (`config_profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `total_count_item`
  ADD CONSTRAINT `total_count_item_foreign_key` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `trap_alarm_action_mapping`
  ADD CONSTRAINT `FK_trap_alarm_action_mapping` FOREIGN KEY (`trap_alarm_masking_id`) REFERENCES `trap_alarm_masking` (`trap_alarm_masking_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_trap_alarm_action_mapping_ack` FOREIGN KEY (`acknowledge_id`) REFERENCES `acknowledge` (`acknowledge_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `trap_alarm_masking`
  ADD CONSTRAINT `FK_trap_alarm_masking` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_trap_alarm_masking_ack` FOREIGN KEY (`acknowledge_id`) REFERENCES `acknowledge` (`acknowledge_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_trap_alarm_masking_actions` FOREIGN KEY (`action_id`) REFERENCES `actions` (`action_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_trap_alarm_masking_field` FOREIGN KEY (`trap_alarm_field`) REFERENCES `trap_alarm_field_table` (`trap_alarm_field`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `trap_id_mapping`
  ADD CONSTRAINT `FK_trap_id_mapping` FOREIGN KEY (`priority_id`) REFERENCES `priority` (`priority_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `users_groups`
  ADD CONSTRAINT `FK_users_groups` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_users_groups_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `user_login`
  ADD CONSTRAINT `FK_user_login` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_user_login_nms_instance` FOREIGN KEY (`nms_id`) REFERENCES `nms_instance` (`nms_id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `odu100_ipFilterTable`
  ADD CONSTRAINT `FK_odu100_ipFilterTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `odu100_macFilterTable`
  ADD CONSTRAINT `FK_odu100_macFilterTable` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE CASCADE ON UPDATE CASCADE;  
ALTER TABLE `odu100_7_2_20_oids`
  ADD CONSTRAINT `FK_oids` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_oids_dependant_id` FOREIGN KEY (`dependent_id`) REFERENCES `oids` (`oid_id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `odu100_7_2_20_oids_multivalues`
  ADD CONSTRAINT `FK_oids_multivalues` FOREIGN KEY (`oid_id`) REFERENCES `oids` (`oid_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `odu100_7_2_25_oids`
  ADD CONSTRAINT `FK_oids` FOREIGN KEY (`device_type_id`) REFERENCES `device_type` (`device_type_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_oids_dependant_id` FOREIGN KEY (`dependent_id`) REFERENCES `oids` (`oid_id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `odu100_7_2_25_oids_multivalues`
  ADD CONSTRAINT `FK_oids_multivalues` FOREIGN KEY (`oid_id`) REFERENCES `oids` (`oid_id`) ON DELETE CASCADE ON UPDATE CASCADE;
SET FOREIGN_KEY_CHECKS=1;

