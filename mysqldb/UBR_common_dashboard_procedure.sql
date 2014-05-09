
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


delimiter //
 DROP PROCEDURE IF EXISTS `outage_graph`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `outage_graph`(IN start_odu INT,IN end_odu INT,start_date timestamp,end_date timestamp,device_type varchar(16))
BEGIN
 DECLARE host_id INT ;
 DECLARE done INT DEFAULT 0;
 DECLARE device VARCHAR(16);
 set device=concat('"',device_type,'%','"');
 DROP TEMPORARY TABLE IF EXISTS temptable1;
 CREATE TEMPORARY TABLE temptable1 ( testid integer not null auto_increment primary key,object_id integer);
 DROP TEMPORARY TABLE IF EXISTS temptable2;
 CREATE TEMPORARY TABLE temptable2 ( testid integer not null auto_increment primary key,ip_address varchar(32),state integer,state_time timestamp);
 set @a = end_odu;
 set @b = start_odu;
 set @query=concat('INSERT INTO temptable1 (object_id)(SELECT host_object_id from nagios_hosts  WHERE display_name like ',device ,' order by address  limit  ? offset ? )');
 prepare stmt from @query;
 execute stmt using @a,@b;
 BEGIN
  DECLARE getid CURSOR FOR SELECT object_id from temptable1 ;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
  open getid ;
  while start_odu < end_odu DO 
   fetch getid INTO host_id;
   IF !done THEN INSERT INTO temptable2 (ip_address,state,state_time) (select nh.address,nsh.state_type,nsh.state_time FROM  nagios_hosts as nh INNER JOIN nagios_statehistory as nsh ON nh.host_object_id=nsh.object_id where nsh.object_id = host_id and state_time BETWEEN start_date AND end_date ORDER BY nh.address,nsh.state_time);
   END IF;
   set start_odu=start_odu+1;
  END while; 
   IF (select count(ip_address) from temptable2) THEN
	select testid,ip_address,state,state_time from temptable2;
   else
	select address from temptable1 as temp INNER JOIN nagios_hosts as nagios ON temp.object_id=nagios.host_object_id;
	select * from temptable1;
   END IF;  
 END;
END;//	



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
   IF !done THEN INSERT INTO TempTable2 (rxBytes,txBytes,host_id,time_stamp)(SELECT if(nw.rx_bytes=1111111,0,nw.rx_bytes)as rx_bytes,if(nw.tx_bytes=1111111,0,nw.tx_bytes)as tx_bytes,name,nw.timestamp from get_odu16_nw_interface_statistics_table as nw where nw.index=interface_value and nw.host_id=id and date(nw.timestamp)=current_date() order by nw.timestamp desc limit 2);
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
   Insert Into temptable1 (signal_strength,host_name,time_stamp) (select IFNULL(if(odu.sig_strength=1111111,0,odu.sig_strength),0),name,odu.timestamp from   get_odu16_peer_node_status_table as odu where  odu.host_id = id  AND timeslot_index=interface_value AND date(odu.timestamp)=current_date() order by odu.timestamp desc limit 1 );
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
   Insert Into temptable1 (sysc_lost_counter,host_name,time_stamp) (select IFNULL(if(odu.sysc_lost_counter=1111111,0,odu.sysc_lost_counter),0),name,odu.timestamp from   get_odu16_synch_statistics_table as odu where  odu.host_id = id AND date(odu.timestamp)=current_date() order by odu.timestamp desc limit 2 );
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
   IF !done THEN INSERT INTO temptable1 (rx_crc_error,rx_phy_error,host_name,time_stamp) (select IFNULL(if(odu.rx_crc_errors=1111111,0,odu.rx_crc_errors),0),IFNULL(if(odu.rx_phy_error=1111111,0,odu.rx_phy_error),0),name,odu.timestamp FROM  get_odu16_ra_tdd_mac_statistics_entry as odu where odu.host_id = id  AND date(odu.timestamp)=current_date() order by odu.timestamp  desc limit 2 );
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
 DROP PROCEDURE IF EXISTS `odu_tdd_mac_error_statistics`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu_tdd_mac_error_statistics`(IN start_time TIMESTAMP, IN end_time TIMESTAMP,IN time_interval INT,IN ip_address VARCHAR(16))
BEGIN
 DROP TEMPORARY TABLE IF EXISTS TempTable1;
 CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, rx_crc_error integer, rx_phy_error integer, time_stamp timestamp);
 BEGIN
  while start_time > end_time DO 
   Insert Into TempTable1 (rx_crc_error,rx_phy_error,time_stamp) (select IFNULL((odu.rx_crc_errors),0),IFNULL((odu.rx_phy_error),0),odu.timestamp from  get_odu16_ra_tdd_mac_statistics_entry as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address=ip_address AND odu.timestamp BETWEEN  end_time  AND (end_time + INTERVAL time_interval MINUTE) order by odu.timestamp);
   set start_time=start_time - INTERVAL time_interval MINUTE;
  END while; 
  select * from TempTable1 ;
 END;
END;//


delimiter //
 DROP PROCEDURE IF EXISTS `odu_network_interface`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu_network_interface`(IN start_time TIMESTAMP, IN end_time TIMESTAMP,IN time_interval INT,IN interface_value INT,IN ip_address VARCHAR(16))
BEGIN
 DROP TEMPORARY TABLE IF EXISTS TempTable2;
 DROP TEMPORARY TABLE IF EXISTS TempTable1;
 DROP TEMPORARY TABLE IF EXISTS TempTable3;
 CREATE TEMPORARY TABLE TempTable3 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer, time_stamp timestamp);
 CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer, time_stamp timestamp);
 CREATE TEMPORARY TABLE TempTable2 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer, time_stamp timestamp);
 BEGIN
   Insert Into TempTable2 (rxBytes,txBytes,time_stamp) (select (odu.rx_bytes),(odu.tx_bytes),odu.timestamp from get_odu16_nw_interface_statistics_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where  h.ip_address=ip_address AND  odu.timestamp >= end_time and odu.timestamp <= start_time and odu.index = interface_value order by odu.timestamp desc );
  INSERT INTO TempTable1 (rxBytes,txBytes,time_stamp)(SELECT t.rxBytes,t.txBytes,t.time_stamp FROM TempTable2 t);
  INSERT INTO TempTable3 (rxBytes,txBytes,time_stamp)(select IF(IFNULL((a.rxBytes-b.rxBytes),0)<0,0,IFNULL((a.rxBytes-b.rxBytes),0)),IF(IFNULL((a.txBytes-b.txBytes),0)<0,0,IFNULL((a.txBytes-b.txBytes),0)),a.time_stamp from TempTable2 a INNER JOIN TempTable1 b on a.testid=b.testid-1) ;
  select * from TempTable3 ;
 END;
END;//


delimiter //
 DROP PROCEDURE IF EXISTS `odu_synch_statistics`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu_synch_statistics`(IN start_time TIMESTAMP, IN end_time TIMESTAMP,IN time_interval INT,IN ip_address VARCHAR(16))
BEGIN
 DROP TEMPORARY TABLE IF EXISTS TempTable1;
 CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, sync_lost integer, time_stamp timestamp);
 BEGIN
  while start_time > end_time DO 
   Insert Into TempTable1 (sync_lost,time_stamp) (select IFNULL((odu.sysc_lost_counter),0),odu.timestamp from  get_odu16_synch_statistics_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address=ip_address AND odu.timestamp BETWEEN (start_time - INTERVAL time_interval MINUTE) AND start_time );
   set start_time=start_time - INTERVAL time_interval MINUTE;
  END while; 
  select * from TempTable1 ;
 END;
END;//



delimiter //
 DROP PROCEDURE IF EXISTS `odu_peer_node_signal_status`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu_peer_node_signal_status`(IN start_time TIMESTAMP, IN end_time TIMESTAMP,IN time_interval INT,IN interface_value INT,IN ip_address VARCHAR(16))
BEGIN
 DROP TEMPORARY TABLE IF EXISTS TempTable1;
 CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, signal_strength integer, time_stamp timestamp);
 BEGIN
   Insert Into TempTable1 (signal_strength,time_stamp) (select (IFNULL((odu.sig_strength),0)),odu.timestamp from   get_odu16_peer_node_status_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where odu.timestamp  >= end_time AND odu.timestamp <= start_time AND h.ip_address=ip_address  AND  timeslot_index=interface_value order by odu.timestamp desc );
  select * from TempTable1 ;
 END;
END;//


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
   set @query='INSERT INTO TempTable1 (host_id,host_name)(SELECT host_id,ip_address from hosts WHERE device_type_id like "ODU%" order by ip_address  limit  ? offset ? )';
   prepare stmt from @query;
   execute stmt using @a,@b;
   set start_limit = start_odu;
           BEGIN
   DECLARE getid CURSOR FOR SELECT host_id,host_name from TempTable1 ;
   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
           open getid;
           while start_odu < end_odu DO
           fetch getid INTO id,name;
   IF !done THEN INSERT INTO TempTable2 (rxBytes,txBytes,host_id,time_stamp)(SELECT if(nw.rx_bytes=1111111,0,nw.rx_bytes) as rx_bytes,if(nw.tx_bytes=1111111,0,nw.tx_bytes)as tx_bytes,name,nw.timestamp from get_odu16_nw_interface_statistics_table as nw where nw.index=interface_value and nw.host_id=id and date(nw.timestamp)=current_date() order by nw.timestamp desc limit 2);
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
 DROP PROCEDURE IF EXISTS `odu100_network_interface`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu100_network_interface`(IN start_time TIMESTAMP, IN end_time TIMESTAMP,IN time_interval INT,IN interface_value INT,IN ip_address VARCHAR(16))
BEGIN
 DROP TEMPORARY TABLE IF EXISTS TempTable2;
 DROP TEMPORARY TABLE IF EXISTS TempTable1;
 DROP TEMPORARY TABLE IF EXISTS TempTable3;
 CREATE TEMPORARY TABLE TempTable3 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer, time_stamp timestamp);
 CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer, time_stamp timestamp);
 CREATE TEMPORARY TABLE TempTable2 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer, time_stamp timestamp);
 BEGIN
  while start_time > end_time - INTERVAL time_interval MINUTE DO 
   Insert Into TempTable2 (rxBytes,txBytes,time_stamp) (select (odu.rxBytes),(odu.txBytes),odu.timestamp from odu100_nwInterfaceStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where  h.ip_address=ip_address AND  odu.timestamp BETWEEN ((start_time - INTERVAL time_interval MINUTE) AND start_time) and odu.nwStatsIndex = interface_value  );
   set start_time=start_time - INTERVAL time_interval MINUTE;
  END while; 
  INSERT INTO TempTable1 (rxBytes,txBytes,time_stamp)(SELECT t.rxBytes,t.txBytes,t.time_stamp FROM TempTable2 t);
  INSERT INTO TempTable3 (rxBytes,txBytes,time_stamp)(select IF(IFNULL((a.rxBytes-b.rxBytes),0)<0,0,IFNULL((a.rxBytes-b.rxBytes),0)),IF(IFNULL((a.txBytes-b.txBytes),0)<0,0,IFNULL((a.txBytes-b.txBytes),0)),a.time_stamp from TempTable2 a INNER JOIN TempTable1 b on a.testid=b.testid-1) ;
  select * from TempTable3 ;
 END;
END;//


delimiter //
 DROP PROCEDURE IF EXISTS `odu100_tdd_mac_error_statistics`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu100_tdd_mac_error_statistics`(IN start_time TIMESTAMP, IN end_time TIMESTAMP,IN time_interval INT,IN ip_address VARCHAR(16))
BEGIN
 DROP TEMPORARY TABLE IF EXISTS TempTable1;
 CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, rx_crc_error integer, rx_phy_error integer, time_stamp timestamp);
 BEGIN
  while start_time > end_time DO 
   Insert Into TempTable1 (rx_crc_error,rx_phy_error,time_stamp) (select IFNULL((odu.rxCrcErrors),0),IFNULL((odu.rxPhyError),0),odu.timestamp from  odu100_raTddMacStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address=ip_address AND odu.timestamp BETWEEN (start_time - INTERVAL time_interval MINUTE) AND start_time );
   set start_time=start_time - INTERVAL time_interval MINUTE;
  END while; 
  select * from TempTable1 ;
 END;
END;//



delimiter //
 DROP PROCEDURE IF EXISTS `odu100_synch_statistics`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu100_synch_statistics`(IN start_time TIMESTAMP, IN end_time TIMESTAMP,IN time_interval INT,IN ip_address VARCHAR(16))
BEGIN
 DROP TEMPORARY TABLE IF EXISTS TempTable1;
 CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, sync_lost integer, time_stamp timestamp);
 BEGIN
  while start_time > end_time DO 
   Insert Into TempTable1 (sync_lost,time_stamp) (select IFNULL((odu.syncLostCounter),0),odu.timestamp from  odu100_synchStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address=ip_address AND odu.timestamp BETWEEN (start_time - INTERVAL time_interval MINUTE) AND start_time );
   set start_time=start_time - INTERVAL time_interval MINUTE;
  END while; 
  select * from TempTable1 ;
 END;
END;//




delimiter //
 DROP PROCEDURE IF EXISTS `odu100_peer_node_signal_status`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `odu100_peer_node_signal_status`(IN start_time TIMESTAMP, IN end_time TIMESTAMP,IN time_interval INT,IN interface_value INT,IN ip_address VARCHAR(16))
BEGIN
 DROP TEMPORARY TABLE IF EXISTS TempTable1;
 CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, signal_strength integer, time_stamp timestamp);
 BEGIN
   Insert Into TempTable1 (signal_strength,time_stamp) (select (IFNULL((odu.signalStrength),0)),odu.timestamp from   odu100_raScanListTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where odu.timestamp  >= end_time AND odu.timestamp <= start_time AND h.ip_address=ip_address  AND  raScanIndex=interface_value order by odu.timestamp desc  );
  select * from TempTable1 ;
 END;
END;//




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
   IF !done THEN INSERT INTO TempTable2 (rxBytes,txBytes,host_id,time_stamp)(SELECT if(nw.rxBytes=1111111,0,nw.rxBytes) as rxBytes,if(nw.txBytes=1111111,0,nw.txBytes) as txBytes,name,nw.timestamp from odu100_nwInterfaceStatisticsTable as nw where nw.nwStatsIndex=interface_value and nw.host_id=id and date(nw.timestamp)=current_date() order by nw.timestamp desc limit 2);
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
   IF !done THEN INSERT INTO temptable1 (rx_crc_error,rx_phy_error,host_name,time_stamp) (select (IFNULL(if(odu.rxCrcErrors=1111111,0,odu.rxCrcErrors),0)),(IFNULL(if(odu.rxPhyError=1111111,0,odu.rxPhyError),0)),name,odu.timestamp FROM  odu100_raTddMacStatisticsTable as odu where odu.host_id = id  AND date(odu.timestamp)=current_date() order by odu.timestamp  desc limit 2 );
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
   Insert Into temptable1 (signal_strength,host_name,time_stamp) (select IFNULL(if(odu.signalStrength=1111111,0,odu.signalStrength),0),name,odu.timestamp from   odu100_raScanListTable as odu where  odu.host_id = id  AND raScanIndex=interface_value AND date(odu.timestamp)=current_date() order by odu.timestamp desc limit 1 );
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
   Insert Into temptable1 (sysc_lost_counter,host_name,time_stamp) (select IFNULL(if(odu.syncLostCounter=1111111,0,odu.syncLostCounter),0),name,odu.timestamp from   odu100_synchStatisticsTable as odu where  odu.host_id = id AND date(odu.timestamp)=current_date() order by odu.timestamp desc limit 2 );
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




-- IDU Procedure
-- procedure calling 

delimiter //
DROP PROCEDURE IF EXISTS `idu_network_interface_common_dashboard`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `idu_network_interface_common_dashboard`(start_idu INT,end_idu INT,interface INT)
BEGIN
   DECLARE id VARCHAR(64) ;
   DECLARE name VARCHAR(32) ;
   DECLARE done INT DEFAULT 0;
   DECLARE start_limit INT(8) ;
   DECLARE delta_row INT(8) ;
   DROP TEMPORARY TABLE IF EXISTS TempTable1;
   CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
   DROP TEMPORARY TABLE IF EXISTS TempTable2;
   CREATE TEMPORARY TABLE TempTable2 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_name varchar(64) ,time_stamp timestamp);
   DROP TEMPORARY TABLE IF EXISTS TempTable3;
   CREATE TEMPORARY TABLE TempTable3 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_name varchar(64) ,time_stamp timestamp);
   DROP TEMPORARY TABLE IF EXISTS TempTable4;
   CREATE TEMPORARY TABLE TempTable4 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_name varchar(64) ,time_stamp timestamp);
   set @a = end_idu;
   set @b = start_idu;
   set @query='INSERT INTO TempTable1 (host_id,host_name)(SELECT host_id,host_name from hosts WHERE device_type_id like "idu%" order by ip_address  limit  ? offset ? )';
   prepare stmt from @query;
   execute stmt using @a,@b;
   set start_limit = start_idu;
           BEGIN
   DECLARE getid CURSOR FOR SELECT host_id,host_name from TempTable1 ;
   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
           open getid;
           while start_idu < end_idu DO
           fetch getid INTO id,name;
   IF !done THEN INSERT INTO TempTable2 (rxBytes,txBytes,host_name,time_stamp)(select IFNULL((idu.rxBytes),0),IFNULL((idu.txBytes),0),name,idu.timestamp FROM  idu_iduNetworkStatisticsTable as idu where idu.host_id = id AND idu.interfaceName=interface  order by idu.timestamp  desc limit 2);
   END IF;
      set start_idu=start_idu+1;
           END while;
           set delta_row=1;
           set start_limit=1;
           INSERT INTO TempTable4(rxBytes,txBytes,host_name,time_stamp)(SELECT tm.rxBytes,tm.txBytes,tm.host_name,tm.time_stamp from TempTable2 tm);
   WHILE start_limit   <= start_idu DO INSERT INTO TempTable3 (rxBytes,txBytes,host_name,time_stamp)(SELECT IF(IFNULL((tm4.rxBytes-tm2.rxBytes),0)<0,0,IFNULL((tm4.rxBytes-tm2.rxBytes),0)),IF(IFNULL((tm4.txBytes-tm2.txBytes),0)<0,0,IFNULL((tm4.txBytes-tm2.txBytes),0)),tm2.host_name,tm2.time_stamp from TempTable4 tm4 INNER JOIN TempTable2 tm2 on tm4.testid=tm2.testid-1 where tm4.testid=delta_row);
      set start_limit=start_limit+1;
      set delta_row=delta_row+2;
    END WHILE ;
           select * from TempTable3 ;
           END;
          END;//



-- idu TDMOIP network bandwidth
-- call idu_tdmoip_network_interface_common_dashboard(0,5,0)
delimiter //
DROP PROCEDURE IF EXISTS `idu_tdmoip_network_interface_common_dashboard`//
CREATE DEFINER=`root`@`localhost` PROCEDURE `idu_tdmoip_network_interface_common_dashboard`(start_idu INT,end_idu INT,interface INT)
BEGIN
   DECLARE id VARCHAR(64) ;
   DECLARE name VARCHAR(32) ;
   DECLARE done INT DEFAULT 0;
   DECLARE start_limit INT(8) ;
   DECLARE delta_row INT(8) ;
   DROP TEMPORARY TABLE IF EXISTS TempTable1;
   CREATE TEMPORARY TABLE TempTable1 ( testid integer not null auto_increment primary key, host_id varchar(64),host_name varchar(32) );
   DROP TEMPORARY TABLE IF EXISTS TempTable2;
   CREATE TEMPORARY TABLE TempTable2 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_name varchar(64) ,time_stamp timestamp);
   DROP TEMPORARY TABLE IF EXISTS TempTable3;
   CREATE TEMPORARY TABLE TempTable3 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_name varchar(64) ,time_stamp timestamp);
   DROP TEMPORARY TABLE IF EXISTS TempTable4;
   CREATE TEMPORARY TABLE TempTable4 ( testid integer not null auto_increment primary key, rxBytes integer, txBytes integer,host_name varchar(64) ,time_stamp timestamp);
   set @a = end_idu;
   set @b = start_idu;
   set @query='INSERT INTO TempTable1 (host_id,host_name)(SELECT host_id,host_name from hosts WHERE device_type_id like "idu%" order by ip_address  limit  ? offset ? )';
   prepare stmt from @query;
   execute stmt using @a,@b;
   set start_limit = start_idu;
           BEGIN
   DECLARE getid CURSOR FOR SELECT host_id,host_name from TempTable1 ;
   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
           open getid;
           while start_idu < end_idu DO
           fetch getid INTO id,name;
   IF !done THEN INSERT INTO TempTable2 (rxBytes,txBytes,host_name,time_stamp)(select IFNULL((idu.bytesReceived),0),IFNULL((idu.bytesTransmitted),0),name,idu.timestamp FROM  idu_tdmoipNetworkInterfaceStatisticsTable as idu where idu.host_id = id AND idu.indexid=interface  order by idu.timestamp  desc limit 2);
   END IF;
      set start_idu=start_idu+1;
           END while;
           set delta_row=1;
           set start_limit=1;
           INSERT INTO TempTable4(rxBytes,txBytes,host_name,time_stamp)(SELECT tm.rxBytes,tm.txBytes,tm.host_name,tm.time_stamp from TempTable2 tm);
   WHILE start_limit   <= start_idu DO INSERT INTO TempTable3 (rxBytes,txBytes,host_name,time_stamp)(SELECT IF(IFNULL((tm4.rxBytes-tm2.rxBytes),0)<0,0,IFNULL((tm4.rxBytes-tm2.rxBytes),0)),IF(IFNULL((tm4.txBytes-tm2.txBytes),0)<0,0,IFNULL((tm4.txBytes-tm2.txBytes),0)),tm2.host_name,tm2.time_stamp from TempTable4 tm4 INNER JOIN TempTable2 tm2 on tm4.testid=tm2.testid-1 where tm4.testid=delta_row);
      set start_limit=start_limit+1;
      set delta_row=delta_row+2;
    END WHILE ;
           select * from TempTable3 ;
           END;
          END;//


