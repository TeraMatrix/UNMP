
DROP TRIGGER IF EXISTS odu100_raTddMacStatisticsTable_trigger;
delimiter |
CREATE TRIGGER odu100_raTddMacStatisticsTable_trigger BEFORE INSERT ON odu100_raTddMacStatisticsTable
    FOR EACH ROW BEGIN
        DECLARE old_time DATETIME;
        DECLARE n_time DATETIME;
        DECLARE hour_start VARCHAR(25);  
        DECLARE hour_end VARCHAR(25);  
        SELECT timestamp into old_time from odu100_raTddMacStatisticsTable where host_id=NEW.host_id order by timestamp desc limit 1;
        ## HOURLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m-%d %H')>DATE_FORMAT(old_time, '%Y-%m-%d %H')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':59:59');
                INSERT INTO `analyze_odu100_raTddMacStatisticsTable` (`analyze_odu100_raTddMacStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                `rx_crc_errors_Avg`, `rx_crc_errors_Min`, `rx_crc_errors_Max`, `rx_crc_errors_Total`, 
		`rx_phy_errors_Avg`, `rx_phy_errors_Min`, `rx_phy_errors_Max`, `rx_phy_errors_Total`,
		`rx_packets_Avg`, `rx_packets_Min`, `rx_packets_Max`, `rx_packets_Total`, 
		`tx_packets_Avg`, `tx_packets_Min`, `tx_packets_Max`, `tx_packets_Total`,  
		`rx_errors_Avg`, `rx_errors_Min`, `rx_errors_Max`, `rx_errors_Total`, 
		`tx_errors_Avg`, `tx_errors_Min`, `tx_errors_Max`, `tx_errors_Total`, 
		`rx_dropped_Avg`, `rx_dropped_Min`, `rx_dropped_Max`, `rx_dropped_Total`,
		`tx_dropped_Avg`, `tx_dropped_Min`, `tx_dropped_Max`, `tx_dropped_Total`)
                select NULL,CONCAT_WS(' ',DATE(t3.timestamp),HOUR(t3.timestamp)),t3.host_id,'HOURLY',
                AVG(t3.delta_rx0),MIN(t3.delta_rx0),MAX(t3.delta_rx0),SUM(t3.delta_rx0),
                AVG(t3.delta_tx0),MIN(t3.delta_tx0),MAX(t3.delta_tx0),SUM(t3.delta_tx0),
                AVG(t3.delta_rx_packets),MIN(t3.delta_rx_packets),MAX(t3.delta_rx_packets),SUM(t3.delta_rx_packets),
                AVG(t3.delta_tx_packets),MIN(t3.delta_tx_packets),MAX(t3.delta_tx_packets),SUM(t3.delta_tx_packets),
                AVG(t3.delta_rx_errors),MIN(t3.delta_rx_errors),MAX(t3.delta_rx_errors),SUM(t3.delta_rx_errors),
                AVG(t3.delta_tx_errors),MIN(t3.delta_tx_errors),MAX(t3.delta_tx_errors),SUM(t3.delta_tx_errors),
                AVG(t3.delta_rx_dropped),MIN(t3.delta_rx_dropped),MAX(t3.delta_rx_dropped),SUM(t3.delta_rx_dropped),
                AVG(t3.delta_tx_dropped),MIN(t3.delta_tx_dropped),MAX(t3.delta_tx_dropped),SUM(t3.delta_tx_dropped)
                from (
                    SELECT 
	                    if(t2.`rxCrcErrors`>t1.`rxCrcErrors`,t2.`rxCrcErrors`-t1.`rxCrcErrors`,0) as delta_rx0,
	                    if(t2.`rxPhyError`>t1.`rxPhyError`,t2.`rxPhyError`-t1.`rxPhyError`,0) as delta_tx0,
	                    if(t2.`rxpackets`>t1.`rxpackets`,t2.`rxpackets`-t1.`rxpackets`,0) as delta_rx_packets,
	                    if(t2.`txpackets`>t1.`txpackets`,t2.`txpackets`-t1.`txpackets`,0) as delta_tx_packets,
	                    if(t2.`rxerrors`>t1.`rxerrors`,t2.`rxerrors`-t1.`rxerrors`,0) as delta_rx_errors,
	                    if(t2.`txerrors`>t1.`txerrors`,t2.`txerrors`-t1.`txerrors`,0) as delta_tx_errors,
	                    if(t2.`rxdropped`>t1.`rxdropped`,t2.`rxdropped`-t1.`rxdropped`,0) as delta_rx_dropped,
	                    if(t2.`txdropped`>t1.`txdropped`,t2.`txdropped`-t1.`txdropped`,0) as delta_tx_dropped,
	                    t2.host_id,t2.timestamp
                    FROM ( select * from `odu100_raTddMacStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t1
                    inner join (select * from `odu100_raTddMacStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id 
                    where  t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`rxCrcErrors`<>1111111 and t2.`rxPhyError`<>1111111  
                    group by t1.timestamp
                    order by t1.timestamp asc ,t1.host_id asc 
                ) as t3
                group by t3.host_id,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                order by t3.timestamp,t3.host_id;
        END IF;
        ## DAILY
        IF (DATE(NEW.timestamp)>DATE(old_time)) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59');
                INSERT INTO `analyze_odu100_raTddMacStatisticsTable` (`analyze_odu100_raTddMacStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                `rx_crc_errors_Avg`, `rx_crc_errors_Min`, `rx_crc_errors_Max`, `rx_crc_errors_Total`, 
		`rx_phy_errors_Avg`, `rx_phy_errors_Min`, `rx_phy_errors_Max`, `rx_phy_errors_Total`,
		`rx_packets_Avg`, `rx_packets_Min`, `rx_packets_Max`, `rx_packets_Total`, 
		`tx_packets_Avg`, `tx_packets_Min`, `tx_packets_Max`, `tx_packets_Total`,  
		`rx_errors_Avg`, `rx_errors_Min`, `rx_errors_Max`, `rx_errors_Total`, 
		`tx_errors_Avg`, `tx_errors_Min`, `tx_errors_Max`, `tx_errors_Total`, 
		`rx_dropped_Avg`, `rx_dropped_Min`, `rx_dropped_Max`, `rx_dropped_Total`,
		`tx_dropped_Avg`, `tx_dropped_Min`, `tx_dropped_Max`, `tx_dropped_Total`)
                select NULL,DATE(t3.timestamp),t3.host_id,'DAILY',
                AVG(t3.delta_rx0),MIN(t3.delta_rx0),MAX(t3.delta_rx0),SUM(t3.delta_rx0),
                AVG(t3.delta_tx0),MIN(t3.delta_tx0),MAX(t3.delta_tx0),SUM(t3.delta_tx0),
                AVG(t3.delta_rx_packets),MIN(t3.delta_rx_packets),MAX(t3.delta_rx_packets),SUM(t3.delta_rx_packets),
                AVG(t3.delta_tx_packets),MIN(t3.delta_tx_packets),MAX(t3.delta_tx_packets),SUM(t3.delta_tx_packets),
                AVG(t3.delta_rx_errors),MIN(t3.delta_rx_errors),MAX(t3.delta_rx_errors),SUM(t3.delta_rx_errors),
                AVG(t3.delta_tx_errors),MIN(t3.delta_tx_errors),MAX(t3.delta_tx_errors),SUM(t3.delta_tx_errors),
                AVG(t3.delta_rx_dropped),MIN(t3.delta_rx_dropped),MAX(t3.delta_rx_dropped),SUM(t3.delta_rx_dropped),
                AVG(t3.delta_tx_dropped),MIN(t3.delta_tx_dropped),MAX(t3.delta_tx_dropped),SUM(t3.delta_tx_dropped)
                from (
                    SELECT 
	                    if(t2.`rxCrcErrors`>t1.`rxCrcErrors`,t2.`rxCrcErrors`-t1.`rxCrcErrors`,0) as delta_rx0,
	                    if(t2.`rxPhyError`>t1.`rxPhyError`,t2.`rxPhyError`-t1.`rxPhyError`,0) as delta_tx0,
	                    if(t2.`rxpackets`>t1.`rxpackets`,t2.`rxpackets`-t1.`rxpackets`,0) as delta_rx_packets,
	                    if(t2.`txpackets`>t1.`txpackets`,t2.`txpackets`-t1.`txpackets`,0) as delta_tx_packets,
	                    if(t2.`rxerrors`>t1.`rxerrors`,t2.`rxerrors`-t1.`rxerrors`,0) as delta_rx_errors,
	                    if(t2.`txerrors`>t1.`txerrors`,t2.`txerrors`-t1.`txerrors`,0) as delta_tx_errors,
	                    if(t2.`rxdropped`>t1.`rxdropped`,t2.`rxdropped`-t1.`rxdropped`,0) as delta_rx_dropped,
	                    if(t2.`txdropped`>t1.`txdropped`,t2.`txdropped`-t1.`txdropped`,0) as delta_tx_dropped,
	                    t2.host_id,t2.timestamp
                   FROM ( select * from `odu100_raTddMacStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t1
                    inner join (select * from `odu100_raTddMacStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id 
                    where t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`rxCrcErrors`<>1111111 and t2.`rxPhyError`<>1111111  
                    group by t1.timestamp
                    order by t1.timestamp asc ,t1.host_id asc 
                ) as t3
                group by t3.host_id,DATE(t3.timestamp)
                order by t3.timestamp,t3.host_id;
        END IF;
        ## WEEKLY
        IF (YEARWEEK(NEW.timestamp)>YEARWEEK(old_time)) 
            THEN
                SET hour_start=subdate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), '%w') DAY);
                SET hour_end= adddate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), INTERVAL 6-DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), '%w') DAY);
                
                INSERT INTO `analyze_odu100_raTddMacStatisticsTable` (`analyze_odu100_raTddMacStatisticsTable_id`, `timestamp`, `host_id`,`type`,
               `rx_crc_errors_Avg`, `rx_crc_errors_Min`, `rx_crc_errors_Max`, `rx_crc_errors_Total`, 
		`rx_phy_errors_Avg`, `rx_phy_errors_Min`, `rx_phy_errors_Max`, `rx_phy_errors_Total`,
		`rx_packets_Avg`, `rx_packets_Min`, `rx_packets_Max`, `rx_packets_Total`, 
		`tx_packets_Avg`, `tx_packets_Min`, `tx_packets_Max`, `tx_packets_Total`,  
		`rx_errors_Avg`, `rx_errors_Min`, `rx_errors_Max`, `rx_errors_Total`, 
		`tx_errors_Avg`, `tx_errors_Min`, `tx_errors_Max`, `tx_errors_Total`, 
		`rx_dropped_Avg`, `rx_dropped_Min`, `rx_dropped_Max`, `rx_dropped_Total`,
		`tx_dropped_Avg`, `tx_dropped_Min`, `tx_dropped_Max`, `tx_dropped_Total`)
                select NULL,hour_start,t3.host_id,'WEEKLY',
                AVG(t3.delta_rx0),MIN(t3.delta_rx0),MAX(t3.delta_rx0),SUM(t3.delta_rx0),
                AVG(t3.delta_tx0),MIN(t3.delta_tx0),MAX(t3.delta_tx0),SUM(t3.delta_tx0),
                AVG(t3.delta_rx_packets),MIN(t3.delta_rx_packets),MAX(t3.delta_rx_packets),SUM(t3.delta_rx_packets),
                AVG(t3.delta_tx_packets),MIN(t3.delta_tx_packets),MAX(t3.delta_tx_packets),SUM(t3.delta_tx_packets),
                AVG(t3.delta_rx_errors),MIN(t3.delta_rx_errors),MAX(t3.delta_rx_errors),SUM(t3.delta_rx_errors),
                AVG(t3.delta_tx_errors),MIN(t3.delta_tx_errors),MAX(t3.delta_tx_errors),SUM(t3.delta_tx_errors),
                AVG(t3.delta_rx_dropped),MIN(t3.delta_rx_dropped),MAX(t3.delta_rx_dropped),SUM(t3.delta_rx_dropped),
                AVG(t3.delta_tx_dropped),MIN(t3.delta_tx_dropped),MAX(t3.delta_tx_dropped),SUM(t3.delta_tx_dropped)
                from (
                    SELECT 
	                    if(t2.`rxCrcErrors`>t1.`rxCrcErrors`,t2.`rxCrcErrors`-t1.`rxCrcErrors`,0) as delta_rx0,
	                    if(t2.`rxPhyError`>t1.`rxPhyError`,t2.`rxPhyError`-t1.`rxPhyError`,0) as delta_tx0,
	                    if(t2.`rxpackets`>t1.`rxpackets`,t2.`rxpackets`-t1.`rxpackets`,0) as delta_rx_packets,
	                    if(t2.`txpackets`>t1.`txpackets`,t2.`txpackets`-t1.`txpackets`,0) as delta_tx_packets,
	                    if(t2.`rxerrors`>t1.`rxerrors`,t2.`rxerrors`-t1.`rxerrors`,0) as delta_rx_errors,
	                    if(t2.`txerrors`>t1.`txerrors`,t2.`txerrors`-t1.`txerrors`,0) as delta_tx_errors,
	                    if(t2.`rxdropped`>t1.`rxdropped`,t2.`rxdropped`-t1.`rxdropped`,0) as delta_rx_dropped,
	                    if(t2.`txdropped`>t1.`txdropped`,t2.`txdropped`-t1.`txdropped`,0) as delta_tx_dropped,
	                    t2.host_id,t2.timestamp
                    FROM ( select * from `odu100_raTddMacStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t1
                    inner join (select * from `odu100_raTddMacStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id 
                    where   t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`rxCrcErrors`<>1111111 and t2.`rxPhyError`<>1111111  
                    group by t1.timestamp
                    order by t1.timestamp asc ,t1.host_id asc 
                ) as t3
                group by t3.host_id,YEARWEEK(t3.timestamp)
                order by t3.timestamp,t3.host_id;
        END IF;
        ## MONTHLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m')>DATE_FORMAT(old_time, '%Y-%m')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-01 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-31 23:59:59');
                INSERT INTO `analyze_odu100_raTddMacStatisticsTable` (`analyze_odu100_raTddMacStatisticsTable_id`, `timestamp`, `host_id`,`type`,
               `rx_crc_errors_Avg`, `rx_crc_errors_Min`, `rx_crc_errors_Max`, `rx_crc_errors_Total`, 
		`rx_phy_errors_Avg`, `rx_phy_errors_Min`, `rx_phy_errors_Max`, `rx_phy_errors_Total`,
		`rx_packets_Avg`, `rx_packets_Min`, `rx_packets_Max`, `rx_packets_Total`, 
		`tx_packets_Avg`, `tx_packets_Min`, `tx_packets_Max`, `tx_packets_Total`,  
		`rx_errors_Avg`, `rx_errors_Min`, `rx_errors_Max`, `rx_errors_Total`, 
		`tx_errors_Avg`, `tx_errors_Min`, `tx_errors_Max`, `tx_errors_Total`, 
		`rx_dropped_Avg`, `rx_dropped_Min`, `rx_dropped_Max`, `rx_dropped_Total`,
		`tx_dropped_Avg`, `tx_dropped_Min`, `tx_dropped_Max`, `tx_dropped_Total`)
                select NULL,CONCAT(DATE_FORMAT(t3.timestamp, '%Y-%m'),'-01 00:00:00'),t3.host_id,'MONTHLY',
                AVG(t3.delta_rx0),MIN(t3.delta_rx0),MAX(t3.delta_rx0),SUM(t3.delta_rx0),
                AVG(t3.delta_tx0),MIN(t3.delta_tx0),MAX(t3.delta_tx0),SUM(t3.delta_tx0),
                AVG(t3.delta_rx_packets),MIN(t3.delta_rx_packets),MAX(t3.delta_rx_packets),SUM(t3.delta_rx_packets),
                AVG(t3.delta_tx_packets),MIN(t3.delta_tx_packets),MAX(t3.delta_tx_packets),SUM(t3.delta_tx_packets),
                AVG(t3.delta_rx_errors),MIN(t3.delta_rx_errors),MAX(t3.delta_rx_errors),SUM(t3.delta_rx_errors),
                AVG(t3.delta_tx_errors),MIN(t3.delta_tx_errors),MAX(t3.delta_tx_errors),SUM(t3.delta_tx_errors),
                AVG(t3.delta_rx_dropped),MIN(t3.delta_rx_dropped),MAX(t3.delta_rx_dropped),SUM(t3.delta_rx_dropped),
                AVG(t3.delta_tx_dropped),MIN(t3.delta_tx_dropped),MAX(t3.delta_tx_dropped),SUM(t3.delta_tx_dropped)
                from (
                    SELECT 
	                    if(t2.`rxCrcErrors`>t1.`rxCrcErrors`,t2.`rxCrcErrors`-t1.`rxCrcErrors`,0) as delta_rx0,
	                    if(t2.`rxPhyError`>t1.`rxPhyError`,t2.`rxPhyError`-t1.`rxPhyError`,0) as delta_tx0,
	                    if(t2.`rxpackets`>t1.`rxpackets`,t2.`rxpackets`-t1.`rxpackets`,0) as delta_rx_packets,
	                    if(t2.`txpackets`>t1.`txpackets`,t2.`txpackets`-t1.`txpackets`,0) as delta_tx_packets,
	                    if(t2.`rxerrors`>t1.`rxerrors`,t2.`rxerrors`-t1.`rxerrors`,0) as delta_rx_errors,
	                    if(t2.`txerrors`>t1.`txerrors`,t2.`txerrors`-t1.`txerrors`,0) as delta_tx_errors,
	                    if(t2.`rxdropped`>t1.`rxdropped`,t2.`rxdropped`-t1.`rxdropped`,0) as delta_rx_dropped,
	                    if(t2.`txdropped`>t1.`txdropped`,t2.`txdropped`-t1.`txdropped`,0) as delta_tx_dropped,
	                    t2.host_id,t2.timestamp
                   FROM ( select * from `odu100_raTddMacStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t1
                    inner join (select * from `odu100_raTddMacStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id
                    where t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`rxCrcErrors`<>1111111 and t2.`rxPhyError`<>1111111  
                    group by t1.timestamp
                    order by t1.timestamp asc ,t1.host_id asc
                ) as t3
                group by t3.host_id,DATE_FORMAT(t3.timestamp, '%Y-%m')
                order by t3.timestamp,t3.host_id;
        END IF;
    END;
|
delimiter ;



DROP TRIGGER IF EXISTS odu100_nwInterfaceStatisticsTable_trigger;
delimiter |
CREATE TRIGGER odu100_nwInterfaceStatisticsTable_trigger BEFORE INSERT ON odu100_nwInterfaceStatisticsTable
    FOR EACH ROW BEGIN
        DECLARE old_time DATETIME;
        DECLARE n_time DATETIME;
        DECLARE hour_start VARCHAR(25);  
        DECLARE hour_end VARCHAR(25);  
        SELECT timestamp into old_time from odu100_nwInterfaceStatisticsTable where host_id=NEW.host_id and `nwStatsIndex`='1' order by timestamp desc limit 1;
        ## HOURLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m-%d %H')>DATE_FORMAT(old_time, '%Y-%m-%d %H')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':59:59');
                INSERT INTO `analyze_odu100_nwInterfaceStatisticsTable` (`analyze_odu100_nwInterfaceStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                  `index_1_rx_packets_Avg`,  `index_1_rx_packets_Min`,  `index_1_rx_packets_Max`,  `index_1_rx_packets_Total`, 
		  `index_1_tx_packets_Avg`,  `index_1_tx_packets_Min`,  `index_1_tx_packets_Max`,  `index_1_tx_packets_Total`, 
		  `index_1_rx_bytes_Avg`,    `index_1_rx_bytes_Min`,    `index_1_rx_bytes_Max`,    `index_1_rx_bytes_Total`, 
		  `index_1_tx_bytes_Avg`,    `index_1_tx_bytes_Min`,    `index_1_tx_bytes_Max`,    `index_1_tx_bytes_Total`, 
		  `index_1_rx_errors_Avg`,   `index_1_rx_errors_Min`,   `index_1_rx_errors_Max`,   `index_1_rx_errors_Total`,
		  `index_1_tx_errors_Avg`,   `index_1_tx_errors_Min`,   `index_1_tx_errors_Max`,   `index_1_tx_errors_Total`, 
		  `index_1_rx_dropped_Avg`,  `index_1_rx_dropped_Min`,  `index_1_rx_dropped_Max`,  `index_1_rx_dropped_Total`,
		  `index_1_tx_dropped_Avg`,  `index_1_tx_dropped_Min`,  `index_1_tx_dropped_Max`,  `index_1_tx_dropped_Total`)		  
                select NULL,CONCAT_WS(' ',DATE(t3.timestamp),HOUR(t3.timestamp)),t3.host_id,'HOURLY',
                AVG(t3.delta_rx_packets),MIN(t3.delta_rx_packets),MAX(t3.delta_rx_packets),SUM(t3.delta_rx_packets),
		AVG(t3.delta_tx_packets),MIN(t3.delta_tx_packets),MAX(t3.delta_tx_packets),SUM(t3.delta_tx_packets),
		AVG(t3.delta_rx_bytes),MIN(t3.delta_rx_bytes),MAX(t3.delta_rx_bytes),SUM(t3.delta_rx_bytes),
		AVG(t3.delta_tx_bytes),MIN(t3.delta_tx_bytes),MAX(t3.delta_tx_bytes),SUM(t3.delta_tx_bytes),
		AVG(t3.delta_rx_errors),MIN(t3.delta_rx_errors),MAX(t3.delta_rx_errors),SUM(t3.delta_rx_errors),
		AVG(t3.delta_tx_errors),MIN(t3.delta_tx_errors),MAX(t3.delta_tx_errors),SUM(t3.delta_tx_errors),
		AVG(t3.delta_rx_dropped),MIN(t3.delta_rx_dropped),MAX(t3.delta_rx_dropped),SUM(t3.delta_rx_dropped),
		AVG(t3.delta_tx_dropped),MIN(t3.delta_tx_dropped),MAX(t3.delta_tx_dropped),SUM(t3.delta_tx_dropped)
                from (
                    SELECT 
	                    if(t2.`rxPackets`>t1.`rxPackets`,t2.`rxPackets`-t1.`rxPackets`,0) as delta_rx_packets,
	                    if(t2.`txPackets`>t1.`txPackets`,t2.`txPackets`-t1.`txPackets`,0) as delta_tx_packets,
	                    if(t2.`rxBytes`>t1.`rxBytes`,t2.`rxBytes`-t1.`rxBytes`,0) as delta_rx_bytes,
	                    if(t2.`txBytes`>t1.`txBytes`,t2.`txBytes`-t1.`txBytes`,0) as delta_tx_bytes,
	                    if(t2.`rxErrors`>t1.`rxErrors`,t2.`rxErrors`-t1.`rxErrors`,0) as delta_rx_errors,
	                    if(t2.`txErrors`>t1.`txErrors`,t2.`txErrors`-t1.`txErrors`,0) as delta_tx_errors,
	                    if(t2.`rxDropped`>t1.`rxDropped`,t2.`rxDropped`-t1.`rxDropped`,0) as delta_rx_dropped,
	                    if(t2.`txDropped`>t1.`txDropped`,t2.`txDropped`-t1.`txDropped`,0) as delta_tx_dropped,                  
	                    t2.host_id,t2.`nwStatsIndex`,t2.timestamp
                    FROM (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='1') as t1
                    inner join (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='1') as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`nwStatsIndex`=t1.`nwStatsIndex`
                    where t1.`nwStatsIndex`='1' and t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`rxBytes`<>1111111 and t2.`txBytes`<>1111111  
                    group by t1.timestamp,t1.`nwStatsIndex`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`nwStatsIndex` asc
                ) as t3
                group by t3.host_id,t3.`nwStatsIndex`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                order by t3.timestamp,t3.`nwStatsIndex`,t3.host_id;

                update analyze_odu100_nwInterfaceStatisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_rx_packets) as delta_rx_packets_Avg,MIN(t3.delta_rx_packets) as delta_rx_packets_Min,
                MAX(t3.delta_rx_packets) as delta_rx_packets_Max,SUM(t3.delta_rx_packets) as delta_rx_packets_Total,
                AVG(t3.delta_tx_packets) as delta_tx_packets_Avg,MIN(t3.delta_tx_packets) as delta_tx_packets_Min,
                MAX(t3.delta_tx_packets) as delta_tx_packets_Max,SUM(t3.delta_tx_packets) as delta_tx_packets_Total,
                AVG(t3.delta_rx_bytes) as delta_rx_bytes_Avg,MIN(t3.delta_rx_bytes) as delta_rx_bytes_Min,
                MAX(t3.delta_rx_bytes) as delta_rx_bytes_Max,SUM(t3.delta_rx_bytes) as delta_rx_bytes_Total,
                AVG(t3.delta_tx_bytes) as delta_tx_bytes_Avg,MIN(t3.delta_tx_bytes) as delta_tx_bytes_Min,
                MAX(t3.delta_tx_bytes) as delta_tx_bytes_Max,SUM(t3.delta_tx_bytes) as delta_tx_bytes_Total,
                AVG(t3.delta_rx_errors) as delta_rx_errors_Avg,MIN(t3.delta_rx_errors) as delta_rx_errors_Min,
                MAX(t3.delta_rx_errors) as delta_rx_errors_Max,SUM(t3.delta_rx_errors) as delta_rx_errors_Total,
                AVG(t3.delta_tx_errors) as delta_tx_errors_Avg,MIN(t3.delta_tx_errors) as delta_tx_errors_Min,
                MAX(t3.delta_tx_errors) as delta_tx_errors_Max,SUM(t3.delta_tx_errors) as delta_tx_errors_Total,
                AVG(t3.delta_rx_dropped) as delta_rx_dropped_Avg,MIN(t3.delta_rx_dropped) as delta_rx_dropped_Min,
                MAX(t3.delta_rx_dropped) as delta_rx_dropped_Max,SUM(t3.delta_rx_dropped) as delta_rx_dropped_Total,
                AVG(t3.delta_tx_dropped) as delta_tx_dropped_Avg,MIN(t3.delta_tx_dropped) as delta_tx_dropped_Min,
                MAX(t3.delta_tx_dropped) as delta_tx_dropped_Max,SUM(t3.delta_tx_dropped) as delta_tx_dropped_Total
                
                from (
                SELECT 
                    if(t2.`rxPackets`>t1.`rxPackets`,t2.`rxPackets`-t1.`rxPackets`,0) as delta_rx_packets,
	                    if(t2.`txPackets`>t1.`txPackets`,t2.`txPackets`-t1.`txPackets`,0) as delta_tx_packets,
	                    if(t2.`rxBytes`>t1.`rxBytes`,t2.`rxBytes`-t1.`rxBytes`,0) as delta_rx_bytes,
	                    if(t2.`txBytes`>t1.`txBytes`,t2.`txBytes`-t1.`txBytes`,0) as delta_tx_bytes,
	                    if(t2.`rxErrors`>t1.`rxErrors`,t2.`rxErrors`-t1.`rxErrors`,0) as delta_rx_errors,
	                    if(t2.`txErrors`>t1.`txErrors`,t2.`txErrors`-t1.`txErrors`,0) as delta_tx_errors,
	                    if(t2.`rxDropped`>t1.`rxDropped`,t2.`rxDropped`-t1.`rxDropped`,0) as delta_rx_dropped,
	                    if(t2.`txDropped`>t1.`txDropped`,t2.`txDropped`-t1.`txDropped`,0) as delta_tx_dropped,
                    t2.host_id,t2.`nwStatsIndex`,t2.timestamp
                    FROM (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='2') as t1
                    inner join (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='2') as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`nwStatsIndex`=t1.`nwStatsIndex`
                    where t1.`nwStatsIndex`='2' and t1.timestamp between hour_start and hour_end 
                                       and t2.timestamp between hour_start and hour_end 
                                       and t2.`rxBytes`<>1111111 and t2.`rxBytes`<>1111111 
                    group by t1.timestamp,t1.`nwStatsIndex`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`nwStatsIndex` asc ) as t3
                    group by t3.host_id,t3.`nwStatsIndex`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`nwStatsIndex`,t3.host_id) as t5
                set 
                    `index_2_rx_packets_Avg` =delta_rx_packets_Avg,
		   `index_2_rx_packets_Min` =delta_rx_packets_Min,
		   `index_2_rx_packets_Max` =delta_rx_packets_Max,
		   `index_2_rx_packets_Total` =delta_rx_packets_Total,
		     `index_2_tx_packets_Avg` =delta_tx_packets_Avg,
		   `index_2_tx_packets_Min` =delta_tx_packets_Min,
		   `index_2_tx_packets_Max` =delta_tx_packets_Max,
		   `index_2_tx_packets_Total` =delta_tx_packets_Total,
		   `index_2_rx_bytes_Avg` =delta_rx_bytes_Avg,
		   `index_2_rx_bytes_Min` =delta_rx_bytes_Min,
		   `index_2_rx_bytes_Max` =delta_rx_bytes_Max,
		   `index_2_rx_bytes_Total` =delta_rx_bytes_Total,
		   `index_2_tx_bytes_Avg` =delta_tx_bytes_Avg,
		   `index_2_tx_bytes_Min` =delta_tx_bytes_Min,
		   `index_2_tx_bytes_Max` =delta_tx_bytes_Max,
		   `index_2_tx_bytes_Total` =delta_tx_bytes_Total,
		    `index_2_rx_errors_Avg` =delta_rx_errors_Avg,
		   `index_2_rx_errors_Min` =delta_rx_errors_Min,
		   `index_2_rx_errors_Max` =delta_rx_errors_Max,
		   `index_2_rx_errors_Total` =delta_rx_errors_Total,
		    `index_2_tx_errors_Avg` =delta_tx_errors_Avg,
		   `index_2_tx_errors_Min` =delta_tx_errors_Min,
		   `index_2_tx_errors_Max` =delta_tx_errors_Max,
		   `index_2_tx_errors_Total` =delta_tx_errors_Total,
		     `index_2_rx_dropped_Avg` =delta_rx_dropped_Avg,
		   `index_2_rx_dropped_Min` =delta_rx_dropped_Min,
		   `index_2_rx_dropped_Max` =delta_rx_dropped_Max,
		   `index_2_rx_dropped_Total` =delta_rx_dropped_Total,
		     `index_2_tx_dropped_Avg` =delta_tx_dropped_Avg,
		   `index_2_tx_dropped_Min` =delta_tx_dropped_Min,
		   `index_2_tx_dropped_Max` =delta_tx_dropped_Max,
		   `index_2_tx_dropped_Total` =delta_tx_dropped_Total
		   
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;

                
        END IF;
        ## DAILY
        IF (DATE(NEW.timestamp)>DATE(old_time)) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59');
                INSERT INTO `analyze_odu100_nwInterfaceStatisticsTable` (`analyze_odu100_nwInterfaceStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                  `index_1_rx_packets_Avg`,  `index_1_rx_packets_Min`,  `index_1_rx_packets_Max`,  `index_1_rx_packets_Total`, 
		  `index_1_tx_packets_Avg`,  `index_1_tx_packets_Min`,  `index_1_tx_packets_Max`,  `index_1_tx_packets_Total`, 
		  `index_1_rx_bytes_Avg`,    `index_1_rx_bytes_Min`,    `index_1_rx_bytes_Max`,    `index_1_rx_bytes_Total`, 
		  `index_1_tx_bytes_Avg`,    `index_1_tx_bytes_Min`,    `index_1_tx_bytes_Max`,    `index_1_tx_bytes_Total`, 
		  `index_1_rx_errors_Avg`,   `index_1_rx_errors_Min`,   `index_1_rx_errors_Max`,   `index_1_rx_errors_Total`,
		  `index_1_tx_errors_Avg`,   `index_1_tx_errors_Min`,   `index_1_tx_errors_Max`,   `index_1_tx_errors_Total`, 
		  `index_1_rx_dropped_Avg`,  `index_1_rx_dropped_Min`,  `index_1_rx_dropped_Max`,  `index_1_rx_dropped_Total`,
		  `index_1_tx_dropped_Avg`,  `index_1_tx_dropped_Min`,  `index_1_tx_dropped_Max`,  `index_1_tx_dropped_Total`)
		  
                select NULL,DATE(t3.timestamp),t3.host_id,'DAILY',
                AVG(t3.delta_rx_packets),MIN(t3.delta_rx_packets),MAX(t3.delta_rx_packets),SUM(t3.delta_rx_packets),
	AVG(t3.delta_tx_packets),MIN(t3.delta_tx_packets),MAX(t3.delta_tx_packets),SUM(t3.delta_tx_packets),
	AVG(t3.delta_rx_bytes),MIN(t3.delta_rx_bytes),MAX(t3.delta_rx_bytes),SUM(t3.delta_rx_bytes),
	AVG(t3.delta_tx_bytes),MIN(t3.delta_tx_bytes),MAX(t3.delta_tx_bytes),SUM(t3.delta_tx_bytes),
	AVG(t3.delta_rx_errors),MIN(t3.delta_rx_errors),MAX(t3.delta_rx_errors),SUM(t3.delta_rx_errors),
	AVG(t3.delta_tx_errors),MIN(t3.delta_tx_errors),MAX(t3.delta_tx_errors),SUM(t3.delta_tx_errors),
	AVG(t3.delta_rx_dropped),MIN(t3.delta_rx_dropped),MAX(t3.delta_rx_dropped),SUM(t3.delta_rx_dropped),
	AVG(t3.delta_tx_dropped),MIN(t3.delta_tx_dropped),MAX(t3.delta_tx_dropped),SUM(t3.delta_tx_dropped)
	
                from (
                    SELECT 
	                    if(t2.`rxPackets`>t1.`rxPackets`,t2.`rxPackets`-t1.`rxPackets`,0) as delta_rx_packets,
	                    if(t2.`txPackets`>t1.`txPackets`,t2.`txPackets`-t1.`txPackets`,0) as delta_tx_packets,
	                    if(t2.`rxBytes`>t1.`rxBytes`,t2.`rxBytes`-t1.`rxBytes`,0) as delta_rx_bytes,
	                    if(t2.`txBytes`>t1.`txBytes`,t2.`txBytes`-t1.`txBytes`,0) as delta_tx_bytes,
	                    if(t2.`rxErrors`>t1.`rxErrors`,t2.`rxErrors`-t1.`rxErrors`,0) as delta_rx_errors,
	                    if(t2.`txErrors`>t1.`txErrors`,t2.`txErrors`-t1.`txErrors`,0) as delta_tx_errors,
	                    if(t2.`rxDropped`>t1.`rxDropped`,t2.`rxDropped`-t1.`rxDropped`,0) as delta_rx_dropped,
	                    if(t2.`txDropped`>t1.`txDropped`,t2.`txDropped`-t1.`txDropped`,0) as delta_tx_dropped,
	                    t2.host_id,t2.`nwStatsIndex`,t2.timestamp
                    FROM (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='1') as t1
                    inner join (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='1') as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`nwStatsIndex`=t1.`nwStatsIndex`
                    where t1.`nwStatsIndex`='1' and t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`rxBytes`<>1111111 and t2.`txBytes`<>1111111  
                    group by t1.timestamp,t1.`nwStatsIndex`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`nwStatsIndex` asc
                ) as t3
                group by t3.host_id,t3.`nwStatsIndex`,DATE(t3.timestamp)
                order by t3.timestamp,t3.`nwStatsIndex`,t3.host_id;

                update analyze_odu100_nwInterfaceStatisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_rx_packets) as delta_rx_packets_Avg,MIN(t3.delta_rx_packets) as delta_rx_packets_Min,
                MAX(t3.delta_rx_packets) as delta_rx_packets_Max,SUM(t3.delta_rx_packets) as delta_rx_packets_Total,
                AVG(t3.delta_tx_packets) as delta_tx_packets_Avg,MIN(t3.delta_tx_packets) as delta_tx_packets_Min,
                MAX(t3.delta_tx_packets) as delta_tx_packets_Max,SUM(t3.delta_tx_packets) as delta_tx_packets_Total,
                AVG(t3.delta_rx_bytes) as delta_rx_bytes_Avg,MIN(t3.delta_rx_bytes) as delta_rx_bytes_Min,
                MAX(t3.delta_rx_bytes) as delta_rx_bytes_Max,SUM(t3.delta_rx_bytes) as delta_rx_bytes_Total,
                AVG(t3.delta_tx_bytes) as delta_tx_bytes_Avg,MIN(t3.delta_tx_bytes) as delta_tx_bytes_Min,
                MAX(t3.delta_tx_bytes) as delta_tx_bytes_Max,SUM(t3.delta_tx_bytes) as delta_tx_bytes_Total,
                AVG(t3.delta_rx_errors) as delta_rx_errors_Avg,MIN(t3.delta_rx_errors) as delta_rx_errors_Min,
                MAX(t3.delta_rx_errors) as delta_rx_errors_Max,SUM(t3.delta_rx_errors) as delta_rx_errors_Total,
                AVG(t3.delta_tx_errors) as delta_tx_errors_Avg,MIN(t3.delta_tx_errors) as delta_tx_errors_Min,
                MAX(t3.delta_tx_errors) as delta_tx_errors_Max,SUM(t3.delta_tx_errors) as delta_tx_errors_Total,
                AVG(t3.delta_rx_dropped) as delta_rx_dropped_Avg,MIN(t3.delta_rx_dropped) as delta_rx_dropped_Min,
                MAX(t3.delta_rx_dropped) as delta_rx_dropped_Max,SUM(t3.delta_rx_dropped) as delta_rx_dropped_Total,
                AVG(t3.delta_tx_dropped) as delta_tx_dropped_Avg,MIN(t3.delta_tx_dropped) as delta_tx_dropped_Min,
                MAX(t3.delta_tx_dropped) as delta_tx_dropped_Max,SUM(t3.delta_tx_dropped) as delta_tx_dropped_Total
                from (
                SELECT 
                    if(t2.`rxPackets`>t1.`rxPackets`,t2.`rxPackets`-t1.`rxPackets`,0) as delta_rx_packets,
	                    if(t2.`txPackets`>t1.`txPackets`,t2.`txPackets`-t1.`txPackets`,0) as delta_tx_packets,
	                    if(t2.`rxBytes`>t1.`rxBytes`,t2.`rxBytes`-t1.`rxBytes`,0) as delta_rx_bytes,
	                    if(t2.`txBytes`>t1.`txBytes`,t2.`txBytes`-t1.`txBytes`,0) as delta_tx_bytes,
	                    if(t2.`rxErrors`>t1.`rxErrors`,t2.`rxErrors`-t1.`rxErrors`,0) as delta_rx_errors,
	                    if(t2.`txErrors`>t1.`txErrors`,t2.`txErrors`-t1.`txErrors`,0) as delta_tx_errors,
	                    if(t2.`rxDropped`>t1.`rxDropped`,t2.`rxDropped`-t1.`rxDropped`,0) as delta_rx_dropped,
	                    if(t2.`txDropped`>t1.`txDropped`,t2.`txDropped`-t1.`txDropped`,0) as delta_tx_dropped,
                    t2.host_id,t2.`nwStatsIndex`,t2.timestamp
                    FROM (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='2') as t1
                    inner join (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='2') as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`nwStatsIndex`=t1.`nwStatsIndex`
                    where t1.`nwStatsIndex`='2' and t1.timestamp between hour_start and hour_end 
                                       and t2.timestamp between hour_start and hour_end 
                                       and t2.`rxBytes`<>1111111 and t2.`rxBytes`<>1111111 
                    group by t1.timestamp,t1.`nwStatsIndex`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`nwStatsIndex` asc ) as t3
                    group by t3.host_id,t3.`nwStatsIndex`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`nwStatsIndex`,t3.host_id) as t5
                set 
                    `index_2_rx_packets_Avg` =delta_rx_packets_Avg,
		   `index_2_rx_packets_Min` =delta_rx_packets_Min,
		   `index_2_rx_packets_Max` =delta_rx_packets_Max,
		   `index_2_rx_packets_Total` =delta_rx_packets_Total,
		     `index_2_tx_packets_Avg` =delta_tx_packets_Avg,
		   `index_2_tx_packets_Min` =delta_tx_packets_Min,
		   `index_2_tx_packets_Max` =delta_tx_packets_Max,
		   `index_2_tx_packets_Total` =delta_tx_packets_Total,
		   `index_2_rx_bytes_Avg` =delta_rx_bytes_Avg,
		   `index_2_rx_bytes_Min` =delta_rx_bytes_Min,
		   `index_2_rx_bytes_Max` =delta_rx_bytes_Max,
		   `index_2_rx_bytes_Total` =delta_rx_bytes_Total,
		   `index_2_tx_bytes_Avg` =delta_tx_bytes_Avg,
		   `index_2_tx_bytes_Min` =delta_tx_bytes_Min,
		   `index_2_tx_bytes_Max` =delta_tx_bytes_Max,
		   `index_2_tx_bytes_Total` =delta_tx_bytes_Total,
		    `index_2_rx_errors_Avg` =delta_rx_errors_Avg,
		   `index_2_rx_errors_Min` =delta_rx_errors_Min,
		   `index_2_rx_errors_Max` =delta_rx_errors_Max,
		   `index_2_rx_errors_Total` =delta_rx_errors_Total,
		    `index_2_tx_errors_Avg` =delta_tx_errors_Avg,
		   `index_2_tx_errors_Min` =delta_tx_errors_Min,
		   `index_2_tx_errors_Max` =delta_tx_errors_Max,
		   `index_2_tx_errors_Total` =delta_tx_errors_Total,
		     `index_2_rx_dropped_Avg` =delta_rx_dropped_Avg,
		   `index_2_rx_dropped_Min` =delta_rx_dropped_Min,
		   `index_2_rx_dropped_Max` =delta_rx_dropped_Max,
		   `index_2_rx_dropped_Total` =delta_rx_dropped_Total,
		     `index_2_tx_dropped_Avg` =delta_tx_dropped_Avg,
		   `index_2_tx_dropped_Min` =delta_tx_dropped_Min,
		   `index_2_tx_dropped_Max` =delta_tx_dropped_Max,
		   `index_2_tx_dropped_Total` =delta_tx_dropped_Total
		   
                where  DATE(t5.timestamp)=DATE(ap.timestamp) and 
                    t5.host_id=ap.host_id;

                
        END IF;
        ## WEEKLY
        IF (YEARWEEK(NEW.timestamp)>YEARWEEK(old_time)) 
            THEN
                SET hour_start=subdate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), '%w') DAY);
                SET hour_end= adddate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), INTERVAL 6-DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), '%w') DAY);
                
                INSERT INTO `analyze_odu100_nwInterfaceStatisticsTable` (`analyze_odu100_nwInterfaceStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                  `index_1_rx_packets_Avg`,  `index_1_rx_packets_Min`,  `index_1_rx_packets_Max`,  `index_1_rx_packets_Total`, 
		  `index_1_tx_packets_Avg`,  `index_1_tx_packets_Min`,  `index_1_tx_packets_Max`,  `index_1_tx_packets_Total`, 
		  `index_1_rx_bytes_Avg`,    `index_1_rx_bytes_Min`,    `index_1_rx_bytes_Max`,    `index_1_rx_bytes_Total`, 
		  `index_1_tx_bytes_Avg`,    `index_1_tx_bytes_Min`,    `index_1_tx_bytes_Max`,    `index_1_tx_bytes_Total`, 
		  `index_1_rx_errors_Avg`,   `index_1_rx_errors_Min`,   `index_1_rx_errors_Max`,   `index_1_rx_errors_Total`,
		  `index_1_tx_errors_Avg`,   `index_1_tx_errors_Min`,   `index_1_tx_errors_Max`,   `index_1_tx_errors_Total`, 
		  `index_1_rx_dropped_Avg`,  `index_1_rx_dropped_Min`,  `index_1_rx_dropped_Max`,  `index_1_rx_dropped_Total`,
		  `index_1_tx_dropped_Avg`,  `index_1_tx_dropped_Min`,  `index_1_tx_dropped_Max`,  `index_1_tx_dropped_Total`)
		  
                select NULL,hour_start,t3.host_id,'WEEKLY',
                AVG(t3.delta_rx_packets),MIN(t3.delta_rx_packets),MAX(t3.delta_rx_packets),SUM(t3.delta_rx_packets),
	AVG(t3.delta_tx_packets),MIN(t3.delta_tx_packets),MAX(t3.delta_tx_packets),SUM(t3.delta_tx_packets),
	AVG(t3.delta_rx_bytes),MIN(t3.delta_rx_bytes),MAX(t3.delta_rx_bytes),SUM(t3.delta_rx_bytes),
	AVG(t3.delta_tx_bytes),MIN(t3.delta_tx_bytes),MAX(t3.delta_tx_bytes),SUM(t3.delta_tx_bytes),
	AVG(t3.delta_rx_errors),MIN(t3.delta_rx_errors),MAX(t3.delta_rx_errors),SUM(t3.delta_rx_errors),
	AVG(t3.delta_tx_errors),MIN(t3.delta_tx_errors),MAX(t3.delta_tx_errors),SUM(t3.delta_tx_errors),
	AVG(t3.delta_rx_dropped),MIN(t3.delta_rx_dropped),MAX(t3.delta_rx_dropped),SUM(t3.delta_rx_dropped),
	AVG(t3.delta_tx_dropped),MIN(t3.delta_tx_dropped),MAX(t3.delta_tx_dropped),SUM(t3.delta_tx_dropped)
	
                from (
                    SELECT 
	                    if(t2.`rxPackets`>t1.`rxPackets`,t2.`rxPackets`-t1.`rxPackets`,0) as delta_rx_packets,
	                    if(t2.`txPackets`>t1.`txPackets`,t2.`txPackets`-t1.`txPackets`,0) as delta_tx_packets,
	                    if(t2.`rxBytes`>t1.`rxBytes`,t2.`rxBytes`-t1.`rxBytes`,0) as delta_rx_bytes,
	                    if(t2.`txBytes`>t1.`txBytes`,t2.`txBytes`-t1.`txBytes`,0) as delta_tx_bytes,
	                    if(t2.`rxErrors`>t1.`rxErrors`,t2.`rxErrors`-t1.`rxErrors`,0) as delta_rx_errors,
	                    if(t2.`txErrors`>t1.`txErrors`,t2.`txErrors`-t1.`txErrors`,0) as delta_tx_errors,
	                    if(t2.`rxDropped`>t1.`rxDropped`,t2.`rxDropped`-t1.`rxDropped`,0) as delta_rx_dropped,
	                    if(t2.`txDropped`>t1.`txDropped`,t2.`txDropped`-t1.`txDropped`,0) as delta_tx_dropped,
	                    t2.host_id,t2.`nwStatsIndex`,t2.timestamp
                   FROM (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='1') as t1
                    inner join (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='1') as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`nwStatsIndex`=t1.`nwStatsIndex`
                    where t1.`nwStatsIndex`='1' and t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`rxBytes`<>1111111 and t2.`txBytes`<>1111111  
                    group by t1.timestamp,t1.`nwStatsIndex`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`nwStatsIndex` asc
                ) as t3
                group by t3.host_id,t3.`nwStatsIndex`,YEARWEEK(t3.timestamp)
                order by t3.timestamp,t3.`nwStatsIndex`,t3.host_id;

                update analyze_odu100_nwInterfaceStatisticsTable as ap ,(select  t3.timestamp,t3.host_id,
               AVG(t3.delta_rx_packets) as delta_rx_packets_Avg,MIN(t3.delta_rx_packets) as delta_rx_packets_Min,
                MAX(t3.delta_rx_packets) as delta_rx_packets_Max,SUM(t3.delta_rx_packets) as delta_rx_packets_Total,
                AVG(t3.delta_tx_packets) as delta_tx_packets_Avg,MIN(t3.delta_tx_packets) as delta_tx_packets_Min,
                MAX(t3.delta_tx_packets) as delta_tx_packets_Max,SUM(t3.delta_tx_packets) as delta_tx_packets_Total,
                AVG(t3.delta_rx_bytes) as delta_rx_bytes_Avg,MIN(t3.delta_rx_bytes) as delta_rx_bytes_Min,
                MAX(t3.delta_rx_bytes) as delta_rx_bytes_Max,SUM(t3.delta_rx_bytes) as delta_rx_bytes_Total,
                AVG(t3.delta_tx_bytes) as delta_tx_bytes_Avg,MIN(t3.delta_tx_bytes) as delta_tx_bytes_Min,
                MAX(t3.delta_tx_bytes) as delta_tx_bytes_Max,SUM(t3.delta_tx_bytes) as delta_tx_bytes_Total,
                AVG(t3.delta_rx_errors) as delta_rx_errors_Avg,MIN(t3.delta_rx_errors) as delta_rx_errors_Min,
                MAX(t3.delta_rx_errors) as delta_rx_errors_Max,SUM(t3.delta_rx_errors) as delta_rx_errors_Total,
                AVG(t3.delta_tx_errors) as delta_tx_errors_Avg,MIN(t3.delta_tx_errors) as delta_tx_errors_Min,
                MAX(t3.delta_tx_errors) as delta_tx_errors_Max,SUM(t3.delta_tx_errors) as delta_tx_errors_Total,
                AVG(t3.delta_rx_dropped) as delta_rx_dropped_Avg,MIN(t3.delta_rx_dropped) as delta_rx_dropped_Min,
                MAX(t3.delta_rx_dropped) as delta_rx_dropped_Max,SUM(t3.delta_rx_dropped) as delta_rx_dropped_Total,
                AVG(t3.delta_tx_dropped) as delta_tx_dropped_Avg,MIN(t3.delta_tx_dropped) as delta_tx_dropped_Min,
                MAX(t3.delta_tx_dropped) as delta_tx_dropped_Max,SUM(t3.delta_tx_dropped) as delta_tx_dropped_Total
                from (
                SELECT 
                    if(t2.`rxPackets`>t1.`rxPackets`,t2.`rxPackets`-t1.`rxPackets`,0) as delta_rx_packets,
	                    if(t2.`txPackets`>t1.`txPackets`,t2.`txPackets`-t1.`txPackets`,0) as delta_tx_packets,
	                    if(t2.`rxBytes`>t1.`rxBytes`,t2.`rxBytes`-t1.`rxBytes`,0) as delta_rx_bytes,
	                    if(t2.`txBytes`>t1.`txBytes`,t2.`txBytes`-t1.`txBytes`,0) as delta_tx_bytes,
	                    if(t2.`rxErrors`>t1.`rxErrors`,t2.`rxErrors`-t1.`rxErrors`,0) as delta_rx_errors,
	                    if(t2.`txErrors`>t1.`txErrors`,t2.`txErrors`-t1.`txErrors`,0) as delta_tx_errors,
	                    if(t2.`rxDropped`>t1.`rxDropped`,t2.`rxDropped`-t1.`rxDropped`,0) as delta_rx_dropped,
	                    if(t2.`txDropped`>t1.`txDropped`,t2.`txDropped`-t1.`txDropped`,0) as delta_tx_dropped,
                    t2.host_id,t2.`nwStatsIndex`,t2.timestamp
                    FROM (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='2') as t1
                    inner join (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='2') as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`nwStatsIndex`=t1.`nwStatsIndex`
                    where t1.`nwStatsIndex`='2' and t1.timestamp between hour_start and hour_end 
                                       and t2.timestamp between hour_start and hour_end 
                                       and t2.`rxBytes`<>1111111 and t2.`rxBytes`<>1111111 
                    group by t1.timestamp,t1.`nwStatsIndex`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`nwStatsIndex` asc ) as t3
                    group by t3.host_id,t3.`nwStatsIndex`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`nwStatsIndex`,t3.host_id) as t5
                set 
                    `index_2_rx_packets_Avg` =delta_rx_packets_Avg,
		   `index_2_rx_packets_Min` =delta_rx_packets_Min,
		   `index_2_rx_packets_Max` =delta_rx_packets_Max,
		   `index_2_rx_packets_Total` =delta_rx_packets_Total,
		     `index_2_tx_packets_Avg` =delta_tx_packets_Avg,
		   `index_2_tx_packets_Min` =delta_tx_packets_Min,
		   `index_2_tx_packets_Max` =delta_tx_packets_Max,
		   `index_2_tx_packets_Total` =delta_tx_packets_Total,
		   `index_2_rx_bytes_Avg` =delta_rx_bytes_Avg,
		   `index_2_rx_bytes_Min` =delta_rx_bytes_Min,
		   `index_2_rx_bytes_Max` =delta_rx_bytes_Max,
		   `index_2_rx_bytes_Total` =delta_rx_bytes_Total,
		   `index_2_tx_bytes_Avg` =delta_tx_bytes_Avg,
		   `index_2_tx_bytes_Min` =delta_tx_bytes_Min,
		   `index_2_tx_bytes_Max` =delta_tx_bytes_Max,
		   `index_2_tx_bytes_Total` =delta_tx_bytes_Total,
		    `index_2_rx_errors_Avg` =delta_rx_errors_Avg,
		   `index_2_rx_errors_Min` =delta_rx_errors_Min,
		   `index_2_rx_errors_Max` =delta_rx_errors_Max,
		   `index_2_rx_errors_Total` =delta_rx_errors_Total,
		    `index_2_tx_errors_Avg` =delta_tx_errors_Avg,
		   `index_2_tx_errors_Min` =delta_tx_errors_Min,
		   `index_2_tx_errors_Max` =delta_tx_errors_Max,
		   `index_2_tx_errors_Total` =delta_tx_errors_Total,
		     `index_2_rx_dropped_Avg` =delta_rx_dropped_Avg,
		   `index_2_rx_dropped_Min` =delta_rx_dropped_Min,
		   `index_2_rx_dropped_Max` =delta_rx_dropped_Max,
		   `index_2_rx_dropped_Total` =delta_rx_dropped_Total,
		     `index_2_tx_dropped_Avg` =delta_tx_dropped_Avg,
		   `index_2_tx_dropped_Min` =delta_tx_dropped_Min,
		   `index_2_tx_dropped_Max` =delta_tx_dropped_Max,
		   `index_2_tx_dropped_Total` =delta_tx_dropped_Total
		   
                where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;

                
        END IF;
        ## MONTHLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m')>DATE_FORMAT(old_time, '%Y-%m')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-01 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-31 23:59:59');
                INSERT INTO `analyze_odu100_nwInterfaceStatisticsTable` (`analyze_odu100_nwInterfaceStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                  `index_1_rx_packets_Avg`,  `index_1_rx_packets_Min`,  `index_1_rx_packets_Max`,  `index_1_rx_packets_Total`, 
		  `index_1_tx_packets_Avg`,  `index_1_tx_packets_Min`,  `index_1_tx_packets_Max`,  `index_1_tx_packets_Total`, 
		  `index_1_rx_bytes_Avg`,    `index_1_rx_bytes_Min`,    `index_1_rx_bytes_Max`,    `index_1_rx_bytes_Total`, 
		  `index_1_tx_bytes_Avg`,    `index_1_tx_bytes_Min`,    `index_1_tx_bytes_Max`,    `index_1_tx_bytes_Total`, 
		  `index_1_rx_errors_Avg`,   `index_1_rx_errors_Min`,   `index_1_rx_errors_Max`,   `index_1_rx_errors_Total`,
		  `index_1_tx_errors_Avg`,   `index_1_tx_errors_Min`,   `index_1_tx_errors_Max`,   `index_1_tx_errors_Total`, 
		  `index_1_rx_dropped_Avg`,  `index_1_rx_dropped_Min`,  `index_1_rx_dropped_Max`,  `index_1_rx_dropped_Total`,
		  `index_1_tx_dropped_Avg`,  `index_1_tx_dropped_Min`,  `index_1_tx_dropped_Max`,  `index_1_tx_dropped_Total`)
		  
				select NULL,CONCAT(DATE_FORMAT(t3.timestamp, '%Y-%m'),'-01 00:00:00'),t3.host_id,'MONTHLY',
                AVG(t3.delta_rx_packets),MIN(t3.delta_rx_packets),MAX(t3.delta_rx_packets),SUM(t3.delta_rx_packets),
	AVG(t3.delta_tx_packets),MIN(t3.delta_tx_packets),MAX(t3.delta_tx_packets),SUM(t3.delta_tx_packets),
	AVG(t3.delta_rx_bytes),MIN(t3.delta_rx_bytes),MAX(t3.delta_rx_bytes),SUM(t3.delta_rx_bytes),
	AVG(t3.delta_tx_bytes),MIN(t3.delta_tx_bytes),MAX(t3.delta_tx_bytes),SUM(t3.delta_tx_bytes),
	AVG(t3.delta_rx_errors),MIN(t3.delta_rx_errors),MAX(t3.delta_rx_errors),SUM(t3.delta_rx_errors),
	AVG(t3.delta_tx_errors),MIN(t3.delta_tx_errors),MAX(t3.delta_tx_errors),SUM(t3.delta_tx_errors),
	AVG(t3.delta_rx_dropped),MIN(t3.delta_rx_dropped),MAX(t3.delta_rx_dropped),SUM(t3.delta_rx_dropped),
	AVG(t3.delta_tx_dropped),MIN(t3.delta_tx_dropped),MAX(t3.delta_tx_dropped),SUM(t3.delta_tx_dropped)
                from (
                    SELECT 
	                    if(t2.rxPackets>t1.rxPackets,t2.rxPackets-t1.rxPackets,0) as delta_rx_packets,
	                    if(t2.`txPackets`>t1.`txPackets`,t2.`txPackets`-t1.`txPackets`,0) as delta_tx_packets,
	                    if(t2.`rxBytes`>t1.`rxBytes`,t2.`rxBytes`-t1.`rxBytes`,0) as delta_rx_bytes,
	                    if(t2.`txBytes`>t1.`txBytes`,t2.`txBytes`-t1.`txBytes`,0) as delta_tx_bytes,
	                    if(t2.`rxErrors`>t1.`rxErrors`,t2.`rxErrors`-t1.`rxErrors`,0) as delta_rx_errors,
	                    if(t2.`txErrors`>t1.`txErrors`,t2.`txErrors`-t1.`txErrors`,0) as delta_tx_errors,
	                    if(t2.`rxDropped`>t1.`rxDropped`,t2.`rxDropped`-t1.`rxDropped`,0) as delta_rx_dropped,
	                    if(t2.`txDropped`>t1.`txDropped`,t2.`txDropped`-t1.`txDropped`,0) as delta_tx_dropped,
	                    t2.host_id,t2.`nwStatsIndex`,t2.timestamp
                   FROM (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='1') as t1
                    inner join (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='1') as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`nwStatsIndex`=t1.`nwStatsIndex`
                    where t1.`nwStatsIndex`='1' and t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`rxBytes`<>1111111 and t2.`txBytes`<>1111111  
                    group by t1.timestamp,t1.`nwStatsIndex`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`nwStatsIndex` asc
                ) as t3
                group by t3.host_id,t3.`nwStatsIndex`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                order by t3.timestamp,t3.`nwStatsIndex`,t3.host_id;

                update analyze_odu100_nwInterfaceStatisticsTable as ap ,(select  t3.timestamp,t3.host_id,
               AVG(t3.delta_rx_packets) as delta_rx_packets_Avg,MIN(t3.delta_rx_packets) as delta_rx_packets_Min,
                MAX(t3.delta_rx_packets) as delta_rx_packets_Max,SUM(t3.delta_rx_packets) as delta_rx_packets_Total,
                AVG(t3.delta_tx_packets) as delta_tx_packets_Avg,MIN(t3.delta_tx_packets) as delta_tx_packets_Min,
                MAX(t3.delta_tx_packets) as delta_tx_packets_Max,SUM(t3.delta_tx_packets) as delta_tx_packets_Total,
                AVG(t3.delta_rx_bytes) as delta_rx_bytes_Avg,MIN(t3.delta_rx_bytes) as delta_rx_bytes_Min,
                MAX(t3.delta_rx_bytes) as delta_rx_bytes_Max,SUM(t3.delta_rx_bytes) as delta_rx_bytes_Total,
                AVG(t3.delta_tx_bytes) as delta_tx_bytes_Avg,MIN(t3.delta_tx_bytes) as delta_tx_bytes_Min,
                MAX(t3.delta_tx_bytes) as delta_tx_bytes_Max,SUM(t3.delta_tx_bytes) as delta_tx_bytes_Total,
                AVG(t3.delta_rx_errors) as delta_rx_errors_Avg,MIN(t3.delta_rx_errors) as delta_rx_errors_Min,
                MAX(t3.delta_rx_errors) as delta_rx_errors_Max,SUM(t3.delta_rx_errors) as delta_rx_errors_Total,
                AVG(t3.delta_tx_errors) as delta_tx_errors_Avg,MIN(t3.delta_tx_errors) as delta_tx_errors_Min,
                MAX(t3.delta_tx_errors) as delta_tx_errors_Max,SUM(t3.delta_tx_errors) as delta_tx_errors_Total,
                AVG(t3.delta_rx_dropped) as delta_rx_dropped_Avg,MIN(t3.delta_rx_dropped) as delta_rx_dropped_Min,
                MAX(t3.delta_rx_dropped) as delta_rx_dropped_Max,SUM(t3.delta_rx_dropped) as delta_rx_dropped_Total,
                AVG(t3.delta_tx_dropped) as delta_tx_dropped_Avg,MIN(t3.delta_tx_dropped) as delta_tx_dropped_Min,
                MAX(t3.delta_tx_dropped) as delta_tx_dropped_Max,SUM(t3.delta_tx_dropped) as delta_tx_dropped_Total
                
                from (
                SELECT 
                    if(t2.rxPackets>t1.rxPackets,t2.rxPackets-t1.rxPackets,0) as delta_rx_packets,
	                    if(t2.`txPackets`>t1.`txPackets`,t2.`txPackets`-t1.`txPackets`,0) as delta_tx_packets,
	                    if(t2.`rxBytes`>t1.`rxBytes`,t2.`rxBytes`-t1.`rxBytes`,0) as delta_rx_bytes,
	                    if(t2.`txBytes`>t1.`txBytes`,t2.`txBytes`-t1.`txBytes`,0) as delta_tx_bytes,
	                    if(t2.`rxErrors`>t1.`rxErrors`,t2.`rxErrors`-t1.`rxErrors`,0) as delta_rx_errors,
	                    if(t2.`txErrors`>t1.`txErrors`,t2.`txErrors`-t1.`txErrors`,0) as delta_tx_errors,
	                    if(t2.`rxDropped`>t1.`rxDropped`,t2.`rxDropped`-t1.`rxDropped`,0) as delta_rx_dropped,
	                    if(t2.`txDropped`>t1.`txDropped`,t2.`txDropped`-t1.`txDropped`,0) as delta_tx_dropped,
                    t2.host_id,t2.`nwStatsIndex`,t2.timestamp
                    FROM (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='2') as t1
                    inner join (select * from `odu100_nwInterfaceStatisticsTable` where host_id=NEW.host_id and  timestamp between hour_start and hour_end and `nwStatsIndex`='2') as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`nwStatsIndex`=t1.`nwStatsIndex`
                    where t1.`nwStatsIndex`='2' and t1.timestamp between hour_start and hour_end 
                                       and t2.timestamp between hour_start and hour_end 
                                       and t2.`rxBytes`<>1111111 and t2.`rxBytes`<>1111111 
                    group by t1.timestamp,t1.`nwStatsIndex`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`nwStatsIndex` asc ) as t3
                    group by t3.host_id,t3.`nwStatsIndex`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`nwStatsIndex`,t3.host_id) as t5
                set 
                    `index_2_rx_packets_Avg` =delta_rx_packets_Avg,
		   `index_2_rx_packets_Min` =delta_rx_packets_Min,
		   `index_2_rx_packets_Max` =delta_rx_packets_Max,
		   `index_2_rx_packets_Total` =delta_rx_packets_Total,
		     `index_2_tx_packets_Avg` =delta_tx_packets_Avg,
		   `index_2_tx_packets_Min` =delta_tx_packets_Min,
		   `index_2_tx_packets_Max` =delta_tx_packets_Max,
		   `index_2_tx_packets_Total` =delta_tx_packets_Total,
		   `index_2_rx_bytes_Avg` =delta_rx_bytes_Avg,
		   `index_2_rx_bytes_Min` =delta_rx_bytes_Min,
		   `index_2_rx_bytes_Max` =delta_rx_bytes_Max,
		   `index_2_rx_bytes_Total` =delta_rx_bytes_Total,
		   `index_2_tx_bytes_Avg` =delta_tx_bytes_Avg,
		   `index_2_tx_bytes_Min` =delta_tx_bytes_Min,
		   `index_2_tx_bytes_Max` =delta_tx_bytes_Max,
		   `index_2_tx_bytes_Total` =delta_tx_bytes_Total,
		    `index_2_rx_errors_Avg` =delta_rx_errors_Avg,
		   `index_2_rx_errors_Min` =delta_rx_errors_Min,
		   `index_2_rx_errors_Max` =delta_rx_errors_Max,
		   `index_2_rx_errors_Total` =delta_rx_errors_Total,
		    `index_2_tx_errors_Avg` =delta_tx_errors_Avg,
		   `index_2_tx_errors_Min` =delta_tx_errors_Min,
		   `index_2_tx_errors_Max` =delta_tx_errors_Max,
		   `index_2_tx_errors_Total` =delta_tx_errors_Total,
		     `index_2_rx_dropped_Avg` =delta_rx_dropped_Avg,
		   `index_2_rx_dropped_Min` =delta_rx_dropped_Min,
		   `index_2_rx_dropped_Max` =delta_rx_dropped_Max,
		   `index_2_rx_dropped_Total` =delta_rx_dropped_Total,
		     `index_2_tx_dropped_Avg` =delta_tx_dropped_Avg,
		   `index_2_tx_dropped_Min` =delta_tx_dropped_Min,
		   `index_2_tx_dropped_Max` =delta_tx_dropped_Max,
		   `index_2_tx_dropped_Total` =delta_tx_dropped_Total
		   
                where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;

                
        END IF;



    END;
|
delimiter ;


DROP TRIGGER IF EXISTS `odu100_peerNodeStatusTable_trigger`;
DELIMITER //
CREATE TRIGGER `odu100_peerNodeStatusTable_trigger` BEFORE INSERT ON `odu100_peerNodeStatusTable`
 FOR EACH ROW BEGIN
        DECLARE old_time DATETIME;
        DECLARE n_time DATETIME;
        DECLARE hour_start VARCHAR(25);  
        DECLARE hour_end VARCHAR(25);  
        SELECT timestamp into old_time from odu100_peerNodeStatusTable where host_id=NEW.host_id order by timestamp desc limit 1;
        ## HOURLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m-%d %H')>DATE_FORMAT(old_time, '%Y-%m-%d %H')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':59:59');
                INSERT INTO `analyze_odu100_peerNodeStatusTable` (`analyze_odu100_peerNodeStatusTable_id`, `timestamp`, `host_id`,`type`,
                `sig1_index_1_Min`, `sig1_index_1_Max`,`sig1_index_1_Range`)
                select NULL,DATE_FORMAT(timestamp, '%Y-%m-%d %H'),host_id,'HOURLY',minimum,maximum,
                if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`
                from (
                select timestamp,host_id,minimum,maximum,
                FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
                `count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
                `count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
                 from 
                (
                SELECT  
                timestamp,host_id,
                SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
                SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
                SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
                SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
                SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
                SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
                SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
                SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
                SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
                SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
                min(sigStrength1) as minimum,max(sigStrength1) as maximum
                FROM `odu100_peerNodeStatusTable` 
                where host_id=NEW.host_id and sigStrength1<>1111111 and timestamp between hour_start and hour_end and timeSlotIndex=1
                group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
                ) as t3
                ) as t4;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=2
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_2_Min`=t5.minimum,
		`sig1_index_2_Max`=t5.maximum, 
		`sig1_index_2_Range`=t5.`Most_values`

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;
		
		
		
				 

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=3
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_3_Min`=t5.minimum,
		`sig1_index_3_Max`=t5.maximum, 
		`sig1_index_3_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=4
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_4_Min`=t5.minimum,
		`sig1_index_4_Max`=t5.maximum, 
		`sig1_index_4_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=5
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_5_Min`=t5.minimum,
		`sig1_index_5_Max`=t5.maximum, 
		`sig1_index_5_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=6
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_6_Min`=t5.minimum,
		`sig1_index_6_Max`=t5.maximum, 
		`sig1_index_6_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=7
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_7_Min`=t5.minimum,
		`sig1_index_7_Max`=t5.maximum, 
		`sig1_index_7_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=8
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_8_Min`=t5.minimum,
		`sig1_index_8_Max`=t5.maximum, 
		`sig1_index_8_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=9
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_9_Min`=t5.minimum,
		`sig1_index_9_Max`=t5.maximum, 
		`sig1_index_9_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=10
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_10_Min`=t5.minimum,
		`sig1_index_10_Max`=t5.maximum, 
		`sig1_index_10_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=11
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_11_Min`=t5.minimum,
		`sig1_index_11_Max`=t5.maximum, 
		`sig1_index_11_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=12
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_12_Min`=t5.minimum,
		`sig1_index_12_Max`=t5.maximum, 
		`sig1_index_12_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=13
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_13_Min`=t5.minimum,
		`sig1_index_13_Max`=t5.maximum, 
		`sig1_index_13_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;		


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=14
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_14_Min`=t5.minimum,
		`sig1_index_14_Max`=t5.maximum, 
		`sig1_index_14_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;		
		

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=15
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_15_Min`=t5.minimum,
		`sig1_index_15_Max`=t5.maximum, 
		`sig1_index_15_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=16
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_16_Min`=t5.minimum,
		`sig1_index_16_Max`=t5.maximum, 
		`sig1_index_16_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;		
			update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=1
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_1_Min`=t5.minimum,
		`sig2_index_1_Max`=t5.maximum, 
		`sig2_index_1_Range`=t5.`Most_values`

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;
			
	
	
	
	
	
	
	update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=2
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_2_Min`=t5.minimum,
		`sig2_index_2_Max`=t5.maximum, 
		`sig2_index_2_Range`=t5.`Most_values`

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;
		
		
		
				 

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=3
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_3_Min`=t5.minimum,
		`sig2_index_3_Max`=t5.maximum, 
		`sig2_index_3_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=4
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_4_Min`=t5.minimum,
		`sig2_index_4_Max`=t5.maximum, 
		`sig2_index_4_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=5
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_5_Min`=t5.minimum,
		`sig2_index_5_Max`=t5.maximum, 
		`sig2_index_5_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=6
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_6_Min`=t5.minimum,
		`sig2_index_6_Max`=t5.maximum, 
		`sig2_index_6_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=7
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_7_Min`=t5.minimum,
		`sig2_index_7_Max`=t5.maximum, 
		`sig2_index_7_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=8
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_8_Min`=t5.minimum,
		`sig2_index_8_Max`=t5.maximum, 
		`sig2_index_8_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=9
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_9_Min`=t5.minimum,
		`sig2_index_9_Max`=t5.maximum, 
		`sig2_index_9_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=10
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_10_Min`=t5.minimum,
		`sig2_index_10_Max`=t5.maximum, 
		`sig2_index_10_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=11
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_11_Min`=t5.minimum,
		`sig2_index_11_Max`=t5.maximum, 
		`sig2_index_11_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=12
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_12_Min`=t5.minimum,
		`sig2_index_12_Max`=t5.maximum, 
		`sig2_index_12_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=13
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_13_Min`=t5.minimum,
		`sig2_index_13_Max`=t5.maximum, 
		`sig2_index_13_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;		


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=14
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_14_Min`=t5.minimum,
		`sig2_index_14_Max`=t5.maximum, 
		`sig2_index_14_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;		
		

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=15
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_15_Min`=t5.minimum,
		`sig2_index_15_Max`=t5.maximum, 
		`sig2_index_15_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=16
		group by host_id,timeSlotIndex,CONCAT(DATE(timestamp),HOUR(timestamp))
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_16_Min`=t5.minimum,
		`sig2_index_16_Max`=t5.maximum, 
		`sig2_index_16_Range`=t5.`Most_values`  

		where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
		t5.host_id=ap.host_id;		
				
        END IF;
        ## DAILY
        IF (DATE(NEW.timestamp)>DATE(old_time)) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59');
                INSERT INTO `analyze_odu100_peerNodeStatusTable` (`analyze_odu100_peerNodeStatusTable_id`, `timestamp`, `host_id`,`type`,
                `sig1_index_1_Min`, `sig1_index_1_Max`,`sig1_index_1_Range`  )
                select NULL,DATE(timestamp),host_id,'DAILY',minimum,maximum,
                if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

                from (
                select timestamp,host_id,minimum,maximum,
                FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
                `count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
                `count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
                 from 
                (
                SELECT  
                timestamp,host_id,
                SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
                SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
                SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
                SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
                SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
                SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
                SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
                SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
                SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
                SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
                min(sigStrength1) as minimum,max(sigStrength1) as maximum
                FROM `odu100_peerNodeStatusTable` 
                where host_id=NEW.host_id and sigStrength1<>1111111 and timestamp between hour_start and hour_end and timeSlotIndex=1
                group by host_id,timeSlotIndex,DATE(timestamp)
                ) as t3
                ) as t4;
                
                
		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=2
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_2_Min`=t5.minimum,
		`sig1_index_2_Max`=t5.maximum, 
		`sig1_index_2_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;
		
		
		
				 

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=3
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_3_Min`=t5.minimum,
		`sig1_index_3_Max`=t5.maximum, 
		`sig1_index_3_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=4
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_4_Min`=t5.minimum,
		`sig1_index_4_Max`=t5.maximum, 
		`sig1_index_4_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=5
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_5_Min`=t5.minimum,
		`sig1_index_5_Max`=t5.maximum, 
		`sig1_index_5_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=6
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_6_Min`=t5.minimum,
		`sig1_index_6_Max`=t5.maximum, 
		`sig1_index_6_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=7
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_7_Min`=t5.minimum,
		`sig1_index_7_Max`=t5.maximum, 
		`sig1_index_7_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=8
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_8_Min`=t5.minimum,
		`sig1_index_8_Max`=t5.maximum, 
		`sig1_index_8_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=9
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_9_Min`=t5.minimum,
		`sig1_index_9_Max`=t5.maximum, 
		`sig1_index_9_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=10
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_10_Min`=t5.minimum,
		`sig1_index_10_Max`=t5.maximum, 
		`sig1_index_10_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=11
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_11_Min`=t5.minimum,
		`sig1_index_11_Max`=t5.maximum, 
		`sig1_index_11_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=12
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_12_Min`=t5.minimum,
		`sig1_index_12_Max`=t5.maximum, 
		`sig1_index_12_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=13
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_13_Min`=t5.minimum,
		`sig1_index_13_Max`=t5.maximum, 
		`sig1_index_13_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=14
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_14_Min`=t5.minimum,
		`sig1_index_14_Max`=t5.maximum, 
		`sig1_index_14_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=15
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_15_Min`=t5.minimum,
		`sig1_index_15_Max`=t5.maximum, 
		`sig1_index_15_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=16
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_16_Min`=t5.minimum,
		`sig1_index_16_Max`=t5.maximum, 
		`sig1_index_16_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and 
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=1
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_1_Min`=t5.minimum,
		`sig2_index_1_Max`=t5.maximum, 
		`sig2_index_1_Range`=t5.`Most_values`

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;
			
	
	
	
	
	
	
	update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=2
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_2_Min`=t5.minimum,
		`sig2_index_2_Max`=t5.maximum, 
		`sig2_index_2_Range`=t5.`Most_values`

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;
		
		
		
				 

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=3
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_3_Min`=t5.minimum,
		`sig2_index_3_Max`=t5.maximum, 
		`sig2_index_3_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=4
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_4_Min`=t5.minimum,
		`sig2_index_4_Max`=t5.maximum, 
		`sig2_index_4_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=5
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_5_Min`=t5.minimum,
		`sig2_index_5_Max`=t5.maximum, 
		`sig2_index_5_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=6
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_6_Min`=t5.minimum,
		`sig2_index_6_Max`=t5.maximum, 
		`sig2_index_6_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=7
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_7_Min`=t5.minimum,
		`sig2_index_7_Max`=t5.maximum, 
		`sig2_index_7_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=8
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_8_Min`=t5.minimum,
		`sig2_index_8_Max`=t5.maximum, 
		`sig2_index_8_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=9
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_9_Min`=t5.minimum,
		`sig2_index_9_Max`=t5.maximum, 
		`sig2_index_9_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=10
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_10_Min`=t5.minimum,
		`sig2_index_10_Max`=t5.maximum, 
		`sig2_index_10_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=11
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_11_Min`=t5.minimum,
		`sig2_index_11_Max`=t5.maximum, 
		`sig2_index_11_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=12
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_12_Min`=t5.minimum,
		`sig2_index_12_Max`=t5.maximum, 
		`sig2_index_12_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=13
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_13_Min`=t5.minimum,
		`sig2_index_13_Max`=t5.maximum, 
		`sig2_index_13_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;		


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=14
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_14_Min`=t5.minimum,
		`sig2_index_14_Max`=t5.maximum, 
		`sig2_index_14_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;		
		

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=15
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_15_Min`=t5.minimum,
		`sig2_index_15_Max`=t5.maximum, 
		`sig2_index_15_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=16
		group by host_id,timeSlotIndex,DATE(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_16_Min`=t5.minimum,
		`sig2_index_16_Max`=t5.maximum, 
		`sig2_index_16_Range`=t5.`Most_values`  

		where DATE(t5.timestamp)=DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;		
		

        END IF;

        ## WEEKLY
        IF (YEARWEEK(NEW.timestamp)>YEARWEEK(old_time)) 
            THEN
                SET hour_start=subdate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), '%w') DAY);
                SET hour_end= adddate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), INTERVAL 6-DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), '%w') DAY);
                INSERT INTO `analyze_odu100_peerNodeStatusTable` (`analyze_odu100_peerNodeStatusTable_id`, `timestamp`, `host_id`,`type`,
                `sig1_index_1_Min`, `sig1_index_1_Max`,`sig1_index_1_Range`  )
                select NULL,hour_start,host_id,'WEEKLY',minimum,maximum,
                if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

                from (
                select timestamp,host_id,minimum,maximum,
                FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
                `count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
                `count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
                 from 
                (
                SELECT  
                timestamp,host_id,
                SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
                SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
                SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
                SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
                SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
                SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
                SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
                SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
                SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
                SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
                min(sigStrength1) as minimum,max(sigStrength1) as maximum
                FROM `odu100_peerNodeStatusTable` 
                where host_id=NEW.host_id and sigStrength1<>1111111 and timestamp between hour_start and hour_end and timeSlotIndex=1
                group by host_id,timeSlotIndex,YEARWEEK(timestamp)
                ) as t3
                ) as t4;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=2
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_2_Min`=t5.minimum,
		`sig1_index_2_Max`=t5.maximum, 
		`sig1_index_2_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;
		
		
		
				 

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=3
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_3_Min`=t5.minimum,
		`sig1_index_3_Max`=t5.maximum, 
		`sig1_index_3_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=4
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_4_Min`=t5.minimum,
		`sig1_index_4_Max`=t5.maximum, 
		`sig1_index_4_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=5
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_5_Min`=t5.minimum,
		`sig1_index_5_Max`=t5.maximum, 
		`sig1_index_5_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=6
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_6_Min`=t5.minimum,
		`sig1_index_6_Max`=t5.maximum, 
		`sig1_index_6_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=7
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_7_Min`=t5.minimum,
		`sig1_index_7_Max`=t5.maximum, 
		`sig1_index_7_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=8
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_8_Min`=t5.minimum,
		`sig1_index_8_Max`=t5.maximum, 
		`sig1_index_8_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=9
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_9_Min`=t5.minimum,
		`sig1_index_9_Max`=t5.maximum, 
		`sig1_index_9_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=10
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_10_Min`=t5.minimum,
		`sig1_index_10_Max`=t5.maximum, 
		`sig1_index_10_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=11
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_11_Min`=t5.minimum,
		`sig1_index_11_Max`=t5.maximum, 
		`sig1_index_11_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=12
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_12_Min`=t5.minimum,
		`sig1_index_12_Max`=t5.maximum, 
		`sig1_index_12_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=13
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_13_Min`=t5.minimum,
		`sig1_index_13_Max`=t5.maximum, 
		`sig1_index_13_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=14
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_14_Min`=t5.minimum,
		`sig1_index_14_Max`=t5.maximum, 
		`sig1_index_14_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=15
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_15_Min`=t5.minimum,
		`sig1_index_15_Max`=t5.maximum, 
		`sig1_index_15_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=16
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_16_Min`=t5.minimum,
		`sig1_index_16_Max`=t5.maximum, 
		`sig1_index_16_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;
		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=1
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_1_Min`=t5.minimum,
		`sig2_index_1_Max`=t5.maximum, 
		`sig2_index_1_Range`=t5.`Most_values`

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;
			
	
	
	
	
	
	
	update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=2
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_2_Min`=t5.minimum,
		`sig2_index_2_Max`=t5.maximum, 
		`sig2_index_2_Range`=t5.`Most_values`

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;
		
		
		
				 

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=3
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_3_Min`=t5.minimum,
		`sig2_index_3_Max`=t5.maximum, 
		`sig2_index_3_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=4
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_4_Min`=t5.minimum,
		`sig2_index_4_Max`=t5.maximum, 
		`sig2_index_4_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=5
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_5_Min`=t5.minimum,
		`sig2_index_5_Max`=t5.maximum, 
		`sig2_index_5_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=6
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_6_Min`=t5.minimum,
		`sig2_index_6_Max`=t5.maximum, 
		`sig2_index_6_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=7
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_7_Min`=t5.minimum,
		`sig2_index_7_Max`=t5.maximum, 
		`sig2_index_7_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=8
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_8_Min`=t5.minimum,
		`sig2_index_8_Max`=t5.maximum, 
		`sig2_index_8_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=9
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_9_Min`=t5.minimum,
		`sig2_index_9_Max`=t5.maximum, 
		`sig2_index_9_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=10
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_10_Min`=t5.minimum,
		`sig2_index_10_Max`=t5.maximum, 
		`sig2_index_10_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=11
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_11_Min`=t5.minimum,
		`sig2_index_11_Max`=t5.maximum, 
		`sig2_index_11_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=12
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_12_Min`=t5.minimum,
		`sig2_index_12_Max`=t5.maximum, 
		`sig2_index_12_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=13
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_13_Min`=t5.minimum,
		`sig2_index_13_Max`=t5.maximum, 
		`sig2_index_13_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;		


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=14
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_14_Min`=t5.minimum,
		`sig2_index_14_Max`=t5.maximum, 
		`sig2_index_14_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;		
		

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=15
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_15_Min`=t5.minimum,
		`sig2_index_15_Max`=t5.maximum, 
		`sig2_index_15_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=16
		group by host_id,timeSlotIndex,YEARWEEK(timestamp)
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_16_Min`=t5.minimum,
		`sig2_index_16_Max`=t5.maximum, 
		`sig2_index_16_Range`=t5.`Most_values`  

		where subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and  
		t5.host_id=ap.host_id;		
		


        END IF;


        ## MONTHLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m')>DATE_FORMAT(old_time, '%Y-%m')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-01 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-31 23:59:59');
                INSERT INTO `analyze_odu100_peerNodeStatusTable` (`analyze_odu100_peerNodeStatusTable_id`, `timestamp`, `host_id`,`type`,
                `sig1_index_1_Min`, `sig1_index_1_Max`,`sig1_index_1_Range`  )
                select NULL,CONCAT(DATE_FORMAT(timestamp, '%Y-%m'),'-01 00:00:00'),host_id,'MONTHLY',minimum,maximum,
                if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

                from (
                select timestamp,host_id,minimum,maximum,
                FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
                `count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
                `count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
                 from 
                (
                SELECT  
                timestamp,host_id,
                SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
                SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
                SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
                SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
                SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
                SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
                SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
                SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
                SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
                SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
                min(sigStrength1) as minimum,max(sigStrength1) as maximum
                FROM `odu100_peerNodeStatusTable` 
                where host_id=NEW.host_id and sigStrength1<>1111111 and timestamp between hour_start and hour_end and timeSlotIndex=1
                group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
                ) as t3
                ) as t4;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=2
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_2_Min`=t5.minimum,
		`sig1_index_2_Max`=t5.maximum, 
		`sig1_index_2_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;
		
		
		
		
				 

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=3
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_3_Min`=t5.minimum,
		`sig1_index_3_Max`=t5.maximum, 
		`sig1_index_3_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=4
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_4_Min`=t5.minimum,
		`sig1_index_4_Max`=t5.maximum, 
		`sig1_index_4_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=5
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_5_Min`=t5.minimum,
		`sig1_index_5_Max`=t5.maximum, 
		`sig1_index_5_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=6
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_6_Min`=t5.minimum,
		`sig1_index_6_Max`=t5.maximum, 
		`sig1_index_6_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=7
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_7_Min`=t5.minimum,
		`sig1_index_7_Max`=t5.maximum, 
		`sig1_index_7_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=8
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_8_Min`=t5.minimum,
		`sig1_index_8_Max`=t5.maximum, 
		`sig1_index_8_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=9
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_9_Min`=t5.minimum,
		`sig1_index_9_Max`=t5.maximum, 
		`sig1_index_9_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=10
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_10_Min`=t5.minimum,
		`sig1_index_10_Max`=t5.maximum, 
		`sig1_index_10_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=11
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_11_Min`=t5.minimum,
		`sig1_index_11_Max`=t5.maximum, 
		`sig1_index_11_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=12
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_12_Min`=t5.minimum,
		`sig1_index_12_Max`=t5.maximum, 
		`sig1_index_12_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=13
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_13_Min`=t5.minimum,
		`sig1_index_13_Max`=t5.maximum, 
		`sig1_index_13_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=14
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_14_Min`=t5.minimum,
		`sig1_index_14_Max`=t5.maximum, 
		`sig1_index_14_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=15
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_15_Min`=t5.minimum,
		`sig1_index_15_Max`=t5.maximum, 
		`sig1_index_15_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength1 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength1 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength1 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength1 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength1 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength1 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength1 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength1 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength1 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength1 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength1) as minimum,max(sigStrength1) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=16
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig1_index_16_Min`=t5.minimum,
		`sig1_index_16_Max`=t5.maximum, 
		`sig1_index_16_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and t5.host_id=ap.host_id;

	update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=1
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_1_Min`=t5.minimum,
		`sig2_index_1_Max`=t5.maximum, 
		`sig2_index_1_Range`=t5.`Most_values`

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;
			
	
	
	
	
	
	
	update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=2
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_2_Min`=t5.minimum,
		`sig2_index_2_Max`=t5.maximum, 
		`sig2_index_2_Range`=t5.`Most_values`

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;
		
		
		
				 

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=3
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_3_Min`=t5.minimum,
		`sig2_index_3_Max`=t5.maximum, 
		`sig2_index_3_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=4
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_4_Min`=t5.minimum,
		`sig2_index_4_Max`=t5.maximum, 
		`sig2_index_4_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=5
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_5_Min`=t5.minimum,
		`sig2_index_5_Max`=t5.maximum, 
		`sig2_index_5_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=6
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_6_Min`=t5.minimum,
		`sig2_index_6_Max`=t5.maximum, 
		`sig2_index_6_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=7
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_7_Min`=t5.minimum,
		`sig2_index_7_Max`=t5.maximum, 
		`sig2_index_7_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=8
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_8_Min`=t5.minimum,
		`sig2_index_8_Max`=t5.maximum, 
		`sig2_index_8_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;



		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=9
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_9_Min`=t5.minimum,
		`sig2_index_9_Max`=t5.maximum, 
		`sig2_index_9_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=10
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_10_Min`=t5.minimum,
		`sig2_index_10_Max`=t5.maximum, 
		`sig2_index_10_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=11
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_11_Min`=t5.minimum,
		`sig2_index_11_Max`=t5.maximum, 
		`sig2_index_11_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=12
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_12_Min`=t5.minimum,
		`sig2_index_12_Max`=t5.maximum, 
		`sig2_index_12_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=13
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_13_Min`=t5.minimum,
		`sig2_index_13_Max`=t5.maximum, 
		`sig2_index_13_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;		


		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=14
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_14_Min`=t5.minimum,
		`sig2_index_14_Max`=t5.maximum, 
		`sig2_index_14_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;		
		

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where host_id=NEW.host_id and  sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=15
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_15_Min`=t5.minimum,
		`sig2_index_15_Max`=t5.maximum, 
		`sig2_index_15_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;

		update `analyze_odu100_peerNodeStatusTable`  as ap ,
		(select timestamp,host_id,minimum,maximum,
		if(range_values=1,-5,
                  if(range_values=2,-15,
                    if(range_values=3,-25,
                        if(range_values=4,-35,
                            if(range_values=5,-45,
                                if(range_values=6,-55,
                                    if(range_values=7,-65,
                                        if(range_values=8,-75,
                                            if(range_values=9,-85,
                                                if(range_values=10,-95,-95)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                     )
                  )
                ) as `Most_values`  

		from (
		select timestamp,host_id,minimum,maximum,
		FIELD(GREATEST(`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`),
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`) as range_values,
		`count_100`,`count_2010`,`count_3020`,`count_4030`,`count_5040`,`count_6050`,`count_7060`,`count_8070`,`count_9080`,`count_9590`
		 from 
		(
		SELECT  
		timestamp,host_id,
		SUM(if(sigStrength2 between '-10' and '0',1,0))   as `count_100`,
		SUM(if(sigStrength2 between '-20' and '-10',1,0)) as `count_2010`,
		SUM(if(sigStrength2 between '-30' and '-20',1,0)) as `count_3020`,
		SUM(if(sigStrength2 between '-40' and '-30',1,0)) as `count_4030`,
		SUM(if(sigStrength2 between '-50' and '-40',1,0)) as `count_5040`,
		SUM(if(sigStrength2 between '-60' and '-50',1,0)) as `count_6050`,
		SUM(if(sigStrength2 between '-70' and '-60',1,0)) as `count_7060`,
		SUM(if(sigStrength2 between '-80' and '-70',1,0)) as `count_8070`,
		SUM(if(sigStrength2 between '-90' and '-80',1,0)) as `count_9080`,
		SUM(if(sigStrength2 between '-95' and '-90',1,0)) as `count_9590`,
		min(sigStrength2) as minimum,max(sigStrength2) as maximum
		FROM `odu100_peerNodeStatusTable` 
		where  host_id=NEW.host_id and sigStrength1<>1111111 and  timestamp between hour_start and hour_end and timeSlotIndex=16
		group by host_id,timeSlotIndex,DATE_FORMAT(timestamp, '%Y-%m')
		) as t3
		) as t4
		)as t5 

		set 
		`sig2_index_16_Min`=t5.minimum,
		`sig2_index_16_Max`=t5.maximum, 
		`sig2_index_16_Range`=t5.`Most_values`  

		where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and  
		t5.host_id=ap.host_id;		
		


        END IF;

    END
//
DELIMITER ;

DROP TRIGGER IF EXISTS odu100_synchStatisticsTable_trigger;
delimiter |
CREATE TRIGGER odu100_synchStatisticsTable_trigger BEFORE INSERT ON odu100_synchStatisticsTable
    FOR EACH ROW BEGIN
        DECLARE old_time DATETIME;
        DECLARE n_time DATETIME;
        DECLARE hour_start VARCHAR(25);  
        DECLARE hour_end VARCHAR(25);  
        SELECT timestamp into old_time from odu100_synchStatisticsTable where host_id=NEW.host_id order by timestamp desc limit 1;
        ## HOURLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m-%d %H')>DATE_FORMAT(old_time, '%Y-%m-%d %H')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':59:59');
                INSERT INTO `analyze_odu100_synchStatisticsTable` (`analyze_odu100_synchStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                `synch_loss_Avg`, `synch_loss_Min`, `synch_loss_Max`, `synch_loss_Total`)
		select NULL,CONCAT_WS(' ',DATE(t3.timestamp),HOUR(t3.timestamp)),t3.host_id,'HOURLY',
		AVG(t3.delta_synch_loss),MIN(t3.delta_synch_loss),MAX(t3.delta_synch_loss),SUM(t3.delta_synch_loss)
		from (
		SELECT 
		if(t2.`syncLostCounter`>t1.`syncLostCounter`,t2.`syncLostCounter`-t1.`syncLostCounter`,0) as delta_synch_loss,
		t2.host_id,t2.timestamp
		FROM (select `syncLostCounter`,host_id,timestamp from `odu100_synchStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t1
		inner join (select `syncLostCounter`,host_id,timestamp from `odu100_synchStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t2 
		on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t1.host_id=NEW.host_id
		where t1.timestamp between hour_start and hour_end 
		and t2.timestamp between hour_start and hour_end and t2.`syncLostCounter`<>1111111 
		group by t1.timestamp
		order by t1.timestamp asc ,t1.host_id asc  ) as t3
		group by t3.host_id,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
		order by t3.timestamp,t3.host_id;
        END IF;
        ## DAILY
        IF (DATE(NEW.timestamp)>DATE(old_time)) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59');
                INSERT INTO `analyze_odu100_synchStatisticsTable` (`analyze_odu100_synchStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                `synch_loss_Avg`, `synch_loss_Min`, `synch_loss_Max`, `synch_loss_Total`)
		select NULL,CONCAT_WS(' ',DATE(t3.timestamp),HOUR(t3.timestamp)),t3.host_id,'DAILY',
		AVG(t3.delta_synch_loss),MIN(t3.delta_synch_loss),MAX(t3.delta_synch_loss),SUM(t3.delta_synch_loss)
		from (
		SELECT 
		if(t2.`syncLostCounter`>t1.`syncLostCounter`,t2.`syncLostCounter`-t1.`syncLostCounter`,0) as delta_synch_loss,
		t2.host_id,t2.timestamp
		FROM (select `syncLostCounter`,host_id,timestamp from `odu100_synchStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t1
		inner join (select `syncLostCounter`,host_id,timestamp from `odu100_synchStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t2 
		on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t1.host_id=NEW.host_id
		where t1.timestamp between hour_start and hour_end 
		and t2.timestamp between hour_start and hour_end and t2.`syncLostCounter`<>1111111 
		group by t1.timestamp
		order by t1.timestamp asc ,t1.host_id asc  ) as t3

		group by t3.host_id,DATE(t3.timestamp)
		order by t3.timestamp,t3.host_id;

        END IF;
        ## WEEKLY
        IF (YEARWEEK(NEW.timestamp)>YEARWEEK(old_time)) 
            THEN
                SET hour_start=subdate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), '%w') DAY);
                SET hour_end= adddate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), INTERVAL 6-DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), '%w') DAY);
                
                INSERT INTO `analyze_odu100_synchStatisticsTable` (`analyze_odu100_synchStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                `synch_loss_Avg`, `synch_loss_Min`, `synch_loss_Max`, `synch_loss_Total`) 
                 select NULL,hour_start,t3.host_id,'WEEKLY',
		AVG(t3.delta_synch_loss),MIN(t3.delta_synch_loss),MAX(t3.delta_synch_loss),SUM(t3.delta_synch_loss)
		from (
		SELECT 
		if(t2.`syncLostCounter`>t1.`syncLostCounter`,t2.`syncLostCounter`-t1.`syncLostCounter`,0) as delta_synch_loss,
		t2.host_id,t2.timestamp
		FROM (select `syncLostCounter`,host_id,timestamp from `odu100_synchStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t1
		inner join (select `syncLostCounter`,host_id,timestamp from `odu100_synchStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t2 
		on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t1.host_id=NEW.host_id
		where t1.timestamp between hour_start and hour_end 
		and t2.timestamp between hour_start and hour_end and t2.`syncLostCounter`<>1111111 
		group by t1.timestamp
		order by t1.timestamp asc ,t1.host_id asc  ) as t3

		group by t3.host_id,YEARWEEK(t3.timestamp)
		order by t3.timestamp,t3.host_id;



        END IF;
        ## MONTHLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m')>DATE_FORMAT(old_time, '%Y-%m')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-01 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-31 23:59:59');
                INSERT INTO `analyze_odu100_synchStatisticsTable` (`analyze_odu100_synchStatisticsTable_id`, `timestamp`, `host_id`,`type`,
                `synch_loss_Avg`, `synch_loss_Min`, `synch_loss_Max`, `synch_loss_Total`)
                select NULL,CONCAT(DATE_FORMAT(t3.timestamp, '%Y-%m'),'-01 00:00:00'),t3.host_id,'MONTHLY',
		AVG(t3.delta_synch_loss),MIN(t3.delta_synch_loss),MAX(t3.delta_synch_loss),SUM(t3.delta_synch_loss)
		from (
		SELECT 
		if(t2.`syncLostCounter`>t1.`syncLostCounter`,t2.`syncLostCounter`-t1.`syncLostCounter`,0) as delta_synch_loss,
		t2.host_id,t2.timestamp
		FROM (select `syncLostCounter`,host_id,timestamp from `odu100_synchStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t1
		inner join (select `syncLostCounter`,host_id,timestamp from `odu100_synchStatisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end ) as t2 
		on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t1.host_id=NEW.host_id
		where t1.timestamp between hour_start and hour_end 
		and t2.timestamp between hour_start and hour_end and t2.`syncLostCounter`<>1111111 
		group by t1.timestamp
		order by t1.timestamp asc ,t1.host_id asc  ) as t3

		group by t3.host_id,DATE_FORMAT(t3.timestamp, '%Y-%m')
		order by t3.timestamp,t3.host_id;

        END IF;

    END;
|
delimiter ;


