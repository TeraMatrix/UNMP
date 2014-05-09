
delimiter //
 DROP PROCEDURE IF EXISTS `trap_graph`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `trap_graph`(IN no_of_day INT,IN host_ip varchar(32))
BEGIN
 DECLARE start_point INT Default 0;
 DECLARE normal_count INT Default 0;
 DECLARE informational_count INT Default 0;
 DECLARE minor_count INT Default 0;
 DECLARE major_count INT Default 0;
 DECLARE critical_count INT Default 0;
 DROP TEMPORARY TABLE IF EXISTS temptable1;
 CREATE TEMPORARY TABLE temptable1 ( testid integer not null auto_increment primary key, normal integer,informationl integer,minor integer,major integer,critical integer,time_stamp timestamp);
 BEGIN
  while start_point < no_of_day DO 
   set normal_count=(SELECT count(ta.trap_event_id) FROM trap_alarms as ta  where ta.agent_id=host_ip AND date(timestamp)=current_date()-start_point AND (ta.serevity=0 OR ta.serevity=2));
   set informational_count=(SELECT count(ta.trap_event_id) FROM trap_alarms as ta  where ta.agent_id=host_ip AND ta.serevity=1 AND date(timestamp)=current_date()-start_point);
   set minor_count=(SELECT count(ta.trap_event_id) FROM trap_alarms as ta  where ta.agent_id=host_ip AND ta.serevity=3 AND date(timestamp)=current_date()-start_point);
   set major_count=(SELECT count(ta.trap_event_id) FROM trap_alarms as ta  where ta.agent_id=host_ip AND ta.serevity=4 AND date(timestamp)=current_date()-start_point);
   set critical_count=(SELECT count(ta.trap_event_id) FROM trap_alarms as ta  where ta.agent_id=host_ip AND ta.serevity=5 AND date(timestamp)=current_date()-start_point);
   INSERT INTO temptable1(normal,informationl,minor,major,critical,time_stamp)values(normal_count,informational_count,minor_count,major_count,critical_count,DATE_SUB(NOW(), INTERVAL start_point DAY));
  set start_point=start_point+1;
  END while; 
  SELECT * from temptable1;
 END;
END;//


 -- UBR procedure start here.....

delimiter //
DROP PROCEDURE IF EXISTS `odu_interface_graph`;//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu_interface_graph`(start_odu INT,end_odu INT, interface_value INT)
BEGIN
   DECLARE id VARCHAR(64) ;
   DECLARE name VARCHAR(32) ;
   DECLARE done INT DEFAULT 0;
   DECLARE start_limit INT(8) ;
   DECLARE delta_row INT(8) ;
   DROP TEMPORARY TABLE IF EXISTS TempTable1;
   CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
   DROP TEMPORARY TABLE IF EXISTS TempTable2;
   CREATE TEMPORARY TABLE TempTable2 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_id varchar(64) ,time_stamp timestamp);
   DROP TEMPORARY TABLE IF EXISTS TempTable3;
   CREATE TEMPORARY TABLE TempTable3 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_id varchar(64) ,time_stamp timestamp);
   DROP TEMPORARY TABLE IF EXISTS TempTable4;
   CREATE TEMPORARY TABLE TempTable4 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_id varchar(64) ,time_stamp timestamp);
   set @a = end_odu;
   set @b = start_odu;
   set @query='INSERT INTO TempTable1 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU16%" and is_deleted=0 order by ip_address  limit  ? offset ? )';
   prepare stmt from @query;
   execute stmt using @a,@b;
   set start_limit = start_odu;
           BEGIN
   DECLARE getid CURSOR FOR SELECT host_id,host_name from TempTable1 ;
   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
           open getid;
           while start_odu < end_odu DO
           fetch getid INTO id,name;
   IF !done THEN INSERT INTO TempTable2 (rxBytes,txBytes,host_id,time_stamp)(SELECT nw.rx_bytes,nw.tx_bytes,name,nw.timestamp from get_odu16_nw_interface_statistics_table as nw where nw.index=CAST(interface_value AS CHAR) and nw.host_id=id and date(nw.timestamp)=current_date() order by nw.timestamp desc limit 2);
   END IF;
      set start_odu=start_odu+1;
           END while;
           set delta_row=1;
           set start_limit=1;
   IF (SELECT count(host_id) from TempTable2) THEN
           INSERT INTO TempTable4(rxBytes,txBytes,host_id,time_stamp)(SELECT tm.rxBytes,tm.txBytes,tm.host_id,tm.time_stamp from TempTable2 tm);
   WHILE start_limit   <= start_odu DO INSERT INTO TempTable3 (rxBytes,txBytes,host_id,time_stamp)(SELECT IF(IFNULL((tm4.rxBytes-tm2.rxBytes),0)<0,0,IFNULL((tm4.rxBytes-tm2.rxBytes),0)),IF(IFNULL((tm4.txBytes-tm2.txBytes),0)<0,0,IFNULL((tm4.txBytes-tm2.txBytes),0)),tm2.host_id,tm2.time_stamp from TempTable4 tm4 INNER JOIN TempTable2 tm2 on tm4.testid=tm2.testid-1 where tm4.testid=delta_row);
      set start_limit=start_limit+1;
      set delta_row=delta_row+2;
    END WHILE ;
       SELECT rxBytes,txBytes,host_id,time_stamp from TempTable3;
   else
       SELECT host_name from TempTable1;
   END IF;
           END;
          END;//



delimiter //
DROP PROCEDURE IF EXISTS `odu_peer_node_signal`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu_peer_node_signal`(IN start_odu INT,IN end_odu INT,IN interface_value INT)
BEGIN
 DECLARE id VARCHAR(64) ;
 DECLARE name VARCHAR(32) ;
 DECLARE done INT DEFAULT 0;
 DROP TEMPORARY TABLE IF EXISTS temptable1;
 CREATE TEMPORARY TABLE temptable1 ( testid integer not null auto_increment primary key, signal_strength integer,host_name varchar(16), time_stamp timestamp);
 DROP TEMPORARY TABLE IF EXISTS temptable2;
 CREATE TEMPORARY TABLE temptable2 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
 set @a = end_odu;
 set @b = start_odu;
 set @query='INSERT INTO temptable2 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU16%" and is_deleted=0 order by ip_address  limit  ? offset ? )';
 prepare stmt from @query;
 execute stmt using @a,@b;

 BEGIN
  DECLARE getid CURSOR FOR SELECT host_id,host_name FROM  temptable2;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
  open getid ;
  while start_odu < end_odu DO 
   fetch getid INTO id,name;
   IF !done THEN 
   Insert Into temptable1 (signal_strength,host_name,time_stamp) (select IFNULL(odu.sig_strength,0),name,odu.timestamp from   get_odu16_peer_node_status_table as odu where  odu.host_id = id  AND odu.timeslot_index=CAST(interface_value AS CHAR) AND date(odu.timestamp)=current_date() order by odu.timestamp desc limit 1 );
   END IF;
   set start_odu=start_odu+1;
  END while; 
   IF (select count(signal_strength) from temptable1) THEN
	select signal_strength,host_name,time_stamp from temptable1;
   else
	select host_name from temptable2;
   END IF;  
 END;
END;//




delimiter //
DROP PROCEDURE IF EXISTS `odu_sync_lost_counter`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu_sync_lost_counter`(IN start_odu INT,IN end_odu INT)
BEGIN
 DECLARE id VARCHAR(64) ;
 DECLARE name VARCHAR(32) ;
 DECLARE done INT DEFAULT 0;
 DROP TEMPORARY TABLE IF EXISTS temptable1;
 CREATE TEMPORARY TABLE temptable1 ( testid integer not null auto_increment primary key, sysc_lost_counter bigint(20),host_name varchar(16), time_stamp timestamp);
 DROP TEMPORARY TABLE IF EXISTS temptable2;
 CREATE TEMPORARY TABLE temptable2 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
 set @a = end_odu;
 set @b = start_odu;
 set @query='INSERT INTO temptable2 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU16%" and is_deleted=0 order by ip_address  limit  ? offset ? )';
 prepare stmt from @query;
 execute stmt using @a,@b;
 BEGIN
  DECLARE getid CURSOR FOR SELECT host_id,host_name FROM  temptable2;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
  open getid ;
  while start_odu < end_odu DO 
   fetch getid INTO id,name;
   IF !done THEN 
   Insert Into temptable1 (sysc_lost_counter,host_name,time_stamp) (select IFNULL(odu.sysc_lost_counter,0),name,odu.timestamp from   get_odu16_synch_statistics_table as odu where  odu.host_id = id AND date(odu.timestamp)=current_date() order by odu.timestamp desc limit 2 );
   END IF;
   set start_odu=start_odu+1;
  END while; 
   IF (select count(host_name) from temptable1) THEN
select sysc_lost_counter,host_name,time_stamp from temptable1;
   else
select host_name from temptable2;
   END IF;  
 END;
END;//



delimiter //
DROP PROCEDURE IF EXISTS `odu_tdd_mac_error`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu_tdd_mac_error`(IN start_odu INT,IN end_odu INT)
BEGIN
 DECLARE id VARCHAR(64) ;
 DECLARE name VARCHAR(32) ;
 DECLARE done INT DEFAULT 0;
 DROP TEMPORARY TABLE IF EXISTS temptable1;
 CREATE TEMPORARY TABLE temptable1 ( testid integer not null auto_increment primary key, rx_crc_error integer, rx_phy_error integer, host_name varchar(16),time_stamp timestamp);
 DROP TEMPORARY TABLE IF EXISTS temptable2;
 CREATE TEMPORARY TABLE temptable2 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
 set @a = end_odu;
 set @b = start_odu;
 set @query='INSERT INTO temptable2 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU16%" and is_deleted=0 order by ip_address  limit  ? offset ? )';
 prepare stmt from @query;
 execute stmt using @a,@b;
 BEGIN
  DECLARE getid CURSOR FOR SELECT host_id,host_name from temptable2 ;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

  open getid ;
  while start_odu < end_odu DO 
   fetch getid INTO id,name;
   IF !done THEN INSERT INTO temptable1 (rx_crc_error,rx_phy_error,host_name,time_stamp) (select IFNULL((odu.rx_crc_errors),0),IFNULL((odu.rx_phy_error),0),name,odu.timestamp FROM  get_odu16_ra_tdd_mac_statistics_entry as odu where odu.host_id = id  AND date(odu.timestamp)=current_date() order by odu.timestamp  desc limit 2 );
   END IF;
   set start_odu=start_odu+1;
  END while; 
   IF (select count(host_name) from temptable1) THEN
select rx_crc_error,rx_phy_error,host_name,time_stamp from temptable1;
   else
select host_name from temptable2;
   END IF;  
 END;
END;//



-- UBRe procedure start here....


delimiter //
DROP PROCEDURE IF EXISTS `odu100_interface_graph`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu100_interface_graph`(start_odu INT,end_odu INT, interface_value INT)
BEGIN
   DECLARE id VARCHAR(64) ;
   DECLARE name VARCHAR(32) ;
   DECLARE done INT DEFAULT 0;
   DECLARE start_limit INT(8) ;
   DECLARE delta_row INT(8) ;
   DROP TEMPORARY TABLE IF EXISTS TempTable1;
   CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
   DROP TEMPORARY TABLE IF EXISTS TempTable2;
   CREATE TEMPORARY TABLE TempTable2 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_id varchar(64) ,time_stamp timestamp);
   DROP TEMPORARY TABLE IF EXISTS TempTable3;
   CREATE TEMPORARY TABLE TempTable3 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_id varchar(64) ,time_stamp timestamp);
   DROP TEMPORARY TABLE IF EXISTS TempTable4;
   CREATE TEMPORARY TABLE TempTable4 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_id varchar(64) ,time_stamp timestamp);
   set @a = end_odu;
   set @b = start_odu;
   set @query='INSERT INTO TempTable1 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU100%" and is_deleted=0 order by ip_address  limit  ? offset ? )';
   prepare stmt from @query;
   execute stmt using @a,@b;
   set start_limit = start_odu;
           BEGIN
   DECLARE getid CURSOR FOR SELECT host_id,host_name from TempTable1 ;
   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
           open getid;
           while start_odu < end_odu DO
           fetch getid INTO id,name;
   IF !done THEN INSERT INTO TempTable2 (rxBytes,txBytes,host_id,time_stamp)(SELECT nw.rxBytes,nw.txBytes,name,nw.timestamp from odu100_nwInterfaceStatisticsTable as nw where nw.nwStatsIndex=CAST(interface_value AS CHAR) and nw.host_id=id and date(nw.timestamp)=current_date() order by nw.timestamp desc limit 2);
   END IF;
      set start_odu=start_odu+1;
           END while;
           set delta_row=1;
           set start_limit=1;
   IF (SELECT count(host_id) from TempTable2) THEN
           INSERT INTO TempTable4(rxBytes,txBytes,host_id,time_stamp)(SELECT tm.rxBytes,tm.txBytes,tm.host_id,tm.time_stamp from TempTable2 tm);
   WHILE start_limit   <= start_odu DO INSERT INTO TempTable3 (rxBytes,txBytes,host_id,time_stamp)(SELECT IF(IFNULL((tm4.rxBytes-tm2.rxBytes),0)<0,0,IFNULL((tm4.rxBytes-tm2.rxBytes),0)),IF(IFNULL((tm4.txBytes-tm2.txBytes),0)<0,0,IFNULL((tm4.txBytes-tm2.txBytes),0)),tm2.host_id,tm2.time_stamp from TempTable4 tm4 INNER JOIN TempTable2 tm2 on tm4.testid=tm2.testid-1 where tm4.testid=delta_row);
      set start_limit=start_limit+1;
      set delta_row=delta_row+2;
    END WHILE ;
       SELECT rxBytes,txBytes,host_id,time_stamp from TempTable3;
   else
       SELECT host_name from TempTable1;
   END IF;
           END;
          END;//


delimiter //
DROP PROCEDURE IF EXISTS `odu100_tdd_mac_error`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu100_tdd_mac_error`(IN start_odu INT,IN end_odu INT)
BEGIN
 DECLARE id VARCHAR(64) ;
 DECLARE name VARCHAR(32) ;
 DECLARE done INT DEFAULT 0;
 DROP TEMPORARY TABLE IF EXISTS temptable1;
 CREATE TEMPORARY TABLE temptable1 ( testid integer not null auto_increment primary key, rx_crc_error integer, rx_phy_error integer, host_name varchar(16),time_stamp timestamp);
 DROP TEMPORARY TABLE IF EXISTS temptable2;
 CREATE TEMPORARY TABLE temptable2 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
 set @a = end_odu;
 set @b = start_odu;
 set @query='INSERT INTO temptable2 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU100%" and is_deleted=0 order by ip_address  limit  ? offset ? )';
 prepare stmt from @query;
 execute stmt using @a,@b;
 BEGIN
  DECLARE getid CURSOR FOR SELECT host_id,host_name from temptable2 ;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

  open getid ;
  while start_odu < end_odu DO 
   fetch getid INTO id,name;
   IF !done THEN INSERT INTO temptable1 (rx_crc_error,rx_phy_error,host_name,time_stamp) (select (IFNULL((odu.rxCrcErrors),0)),(IFNULL((odu.rxPhyError),0)),name,odu.timestamp FROM  odu100_raTddMacStatisticsTable as odu where odu.host_id = id  AND date(odu.timestamp)=current_date() order by odu.timestamp  desc limit 2 );
   END IF;
   set start_odu=start_odu+1;
  END while; 
   IF (select count(host_name) from temptable1) THEN
select rx_crc_error,rx_phy_error,host_name,time_stamp from temptable1;
   else
select host_name from temptable2;
   END IF;  
 END;
END;//




delimiter //
DROP PROCEDURE IF EXISTS `odu100_peer_node_signal`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu100_peer_node_signal`(IN start_odu INT,IN end_odu INT,IN interface_value INT)
BEGIN
 DECLARE id VARCHAR(64) ;
 DECLARE name VARCHAR(32) ;
 DECLARE done INT DEFAULT 0;
 DROP TEMPORARY TABLE IF EXISTS temptable1;
 CREATE TEMPORARY TABLE temptable1 ( testid integer not null auto_increment primary key, signal_strength integer,host_name varchar(16), time_stamp timestamp);
 DROP TEMPORARY TABLE IF EXISTS temptable2;
 CREATE TEMPORARY TABLE temptable2 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
 set @a = end_odu;
 set @b = start_odu;
 set @query='INSERT INTO temptable2 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU100%" and is_deleted=0 order by ip_address  limit  ? offset ? )';
 prepare stmt from @query;
 execute stmt using @a,@b;

 BEGIN
  DECLARE getid CURSOR FOR SELECT host_id,host_name FROM  temptable2;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
  open getid ;
  while start_odu < end_odu DO 
   fetch getid INTO id,name;
   IF !done THEN 
   Insert Into temptable1 (signal_strength,host_name,time_stamp) (select IFNULL(odu.sigStrength1,0),name,odu.timestamp from   odu100_peerNodeStatusTable as odu where  odu.host_id = id  AND odu.timeSlotIndex=CAST(interface_value AS CHAR) AND date(odu.timestamp)=current_date() order by odu.timestamp desc limit 1 );
   END IF;
   set start_odu=start_odu+1;
  END while; 
   IF (select count(signal_strength) from temptable1) THEN
select signal_strength,host_name,time_stamp from temptable1;
   else
select host_name from temptable2;
   END IF;  
 END;
END;//


delimiter //
DROP PROCEDURE IF EXISTS `odu100_sync_lost_counter`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu100_sync_lost_counter`(IN start_odu INT,IN end_odu INT)
BEGIN
 DECLARE id VARCHAR(64) ;
 DECLARE name VARCHAR(32) ;
 DECLARE done INT DEFAULT 0;
 DROP TEMPORARY TABLE IF EXISTS temptable1;
 CREATE TEMPORARY TABLE temptable1 ( testid integer not null auto_increment primary key, sysc_lost_counter bigint(20),host_name varchar(16), time_stamp timestamp);
 DROP TEMPORARY TABLE IF EXISTS temptable2;
 CREATE TEMPORARY TABLE temptable2 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
 set @a = end_odu;
 set @b = start_odu;
 set @query='INSERT INTO temptable2 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU100%" and is_deleted=0 order by ip_address  limit  ? offset ? )';
 prepare stmt from @query;
 execute stmt using @a,@b;
 BEGIN
  DECLARE getid CURSOR FOR SELECT host_id,host_name FROM  temptable2;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
  open getid ;
  while start_odu < end_odu DO 
   fetch getid INTO id,name;
   IF !done THEN 
   Insert Into temptable1 (sysc_lost_counter,host_name,time_stamp) (select IFNULL(odu.syncLostCounter,0),name,odu.timestamp from   odu100_synchStatisticsTable as odu where  odu.host_id = id AND date(odu.timestamp)=current_date() order by odu.timestamp desc limit 2 );
   END IF;
   set start_odu=start_odu+1;
  END while; 
   IF (select count(host_name) from temptable1) THEN
select sysc_lost_counter,host_name,time_stamp from temptable1;
   else
select host_name from temptable2;
   END IF;  
 END;
END;//

