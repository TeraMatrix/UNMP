
DROP TRIGGER IF EXISTS idu_portstatisticsTable_trigger;
delimiter |
CREATE TRIGGER idu_portstatisticsTable_trigger BEFORE INSERT ON idu_portstatisticsTable
    FOR EACH ROW BEGIN
        DECLARE old_time DATETIME;
        DECLARE n_time DATETIME;
        DECLARE hour_start VARCHAR(25);  
        DECLARE hour_end VARCHAR(25);  
        SELECT timestamp into old_time from idu_portstatisticsTable where host_id=NEW.host_id and softwarestatportnum=NEW.softwarestatportnum order by timestamp desc limit 1;
        ## HOURLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m-%d %H')>DATE_FORMAT(old_time, '%Y-%m-%d %H')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':59:59');
                INSERT INTO `analyze_idu_portstatisticsTable` (`analyze_idu_portstatisticsTable_id`, `timestamp`, `host_id`, `type`,`softwarestatportnum`,
                `framerx_Avg`, `framerx_Min`, `framerx_Max`, `framerx_Total`, 
                `frametx_Avg`, `frametx_Min`, `frametx_Max`, `frametx_Total`, 
                `indiscards_Avg`, `indiscards_Min`, `indiscards_Max`, `indiscards_Total`, 
                `ingoodoctets_Avg`, `ingoodoctets_Min`, `ingoodoctets_Max`, `ingoodoctets_Total`, 
                `inbadoctet_Avg`, `inbadoctet_Min`, `inbadoctet_Max`, `inbadoctet_Total`, 
                `outoctets_Avg`, `outoctets_Min`, `outoctets_Max`, `outoctets_Total`) 
                select NULL,CONCAT_WS(' ',DATE(t3.timestamp),HOUR(t3.timestamp)),t3.host_id,'HOURLY',t3.software,
		AVG(t3.framerx),MIN(t3.framerx),MAX(t3.framerx),SUM(t3.framerx),
		AVG(t3.frametx),MIN(t3.frametx),MAX(t3.frametx),SUM(t3.frametx),
		AVG(t3.indiscards),MIN(t3.indiscards),MAX(t3.indiscards),SUM(t3.indiscards),
		AVG(t3.ingoodoctets),MIN(t3.ingoodoctets),MAX(t3.ingoodoctets),SUM(t3.ingoodoctets),
		AVG(t3.inbadoctet),MIN(t3.inbadoctet),MAX(t3.inbadoctet),SUM(t3.inbadoctet),
		AVG(t3.outoctets),MIN(t3.outoctets),MAX(t3.outoctets),SUM(t3.outoctets)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.softwarestatportnum=0,'odu',(if (idu.softwarestatportnum=2,'eth0','eth1')))) as software,    
		if(idu.framerx=1,idu.framerx,if(idu.framerx>idu2.framerx,idu.framerx-idu2.framerx,0)) as framerx,  
		if(idu.frametx=1,idu.frametx,if(idu.frametx>idu2.frametx,idu.frametx-idu2.frametx,0)) as frametx,  
		if(idu.indiscards=1,idu.indiscards,if(idu.indiscards>idu2.indiscards,idu.indiscards-idu2.indiscards,0)) as indiscards,  
		if(idu.ingoodoctets=1,idu.ingoodoctets,if(idu.ingoodoctets>idu2.ingoodoctets,idu.ingoodoctets-idu2.ingoodoctets,0)) as ingoodoctets,  
		if(idu.inbadoctet=1,idu.inbadoctet,if(idu.inbadoctet>idu2.inbadoctet,idu.inbadoctet-idu2.inbadoctet,0)) as inbadoctet,  
		if(idu.outoctets=1,idu.outoctets,if(idu.outoctets>idu2.outoctets,idu.outoctets-idu2.outoctets,0)) as outoctets
		from idu_portstatisticsTable as idu
		join(select * from idu_portstatisticsTable where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and softwarestatportnum=NEW.softwarestatportnum ) as idu2 on idu.timestamp>idu2.timestamp and idu.softwarestatportnum=idu2.softwarestatportnum 
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu.host_id=NEW.host_id
		and idu2.timestamp between  hour_start and hour_end  and idu.softwarestatportnum =NEW.softwarestatportnum and idu.host_id=NEW.host_id
		and idu.framerx<>1 and idu.frametx<>1  
		group by idu2.timestamp,idu2.softwarestatportnum
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.softwarestatportnum asc ) as t3
		group by t3.host_id,t3.software,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
		order by t3.timestamp,t3.software,t3.host_id;

        END IF;
        ## DAILY
        IF (DATE(NEW.timestamp)>DATE(old_time)) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59');
                INSERT INTO `analyze_idu_portstatisticsTable` (`analyze_idu_portstatisticsTable_id`, `timestamp`, `host_id`, `type`,`softwarestatportnum` ,
                `framerx_Avg`, `framerx_Min`, `framerx_Max`, `framerx_Total`, 
                `frametx_Avg`, `frametx_Min`, `frametx_Max`, `frametx_Total`, 
                `indiscards_Avg`, `indiscards_Min`, `indiscards_Max`, `indiscards_Total`, 
                `ingoodoctets_Avg`, `ingoodoctets_Min`, `ingoodoctets_Max`, `ingoodoctets_Total`, 
                `inbadoctet_Avg`, `inbadoctet_Min`, `inbadoctet_Max`, `inbadoctet_Total`, 
                `outoctets_Avg`, `outoctets_Min`, `outoctets_Max`, `outoctets_Total`) 
                
                select NULL,DATE(t3.timestamp),t3.host_id,'DAILY',
		t3.software,
		AVG(t3.framerx),MIN(t3.framerx),MAX(t3.framerx),SUM(t3.framerx),
		AVG(t3.frametx),MIN(t3.frametx),MAX(t3.frametx),SUM(t3.frametx),
		AVG(t3.indiscards),MIN(t3.indiscards),MAX(t3.indiscards),SUM(t3.indiscards),
		AVG(t3.ingoodoctets),MIN(t3.ingoodoctets),MAX(t3.ingoodoctets),SUM(t3.ingoodoctets),
		AVG(t3.inbadoctet),MIN(t3.inbadoctet),MAX(t3.inbadoctet),SUM(t3.inbadoctet),
		AVG(t3.outoctets),MIN(t3.outoctets),MAX(t3.outoctets),SUM(t3.outoctets)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.softwarestatportnum=0,'odu',(if (idu.softwarestatportnum=2,'eth0','eth1')))) as software,    
		if(idu.framerx=1,idu.framerx,if(idu.framerx>idu2.framerx,idu.framerx-idu2.framerx,0)) as framerx,  
		if(idu.frametx=1,idu.frametx,if(idu.frametx>idu2.frametx,idu.frametx-idu2.frametx,0)) as frametx,  
		if(idu.indiscards=1,idu.indiscards,if(idu.indiscards>idu2.indiscards,idu.indiscards-idu2.indiscards,0)) as indiscards,  
		if(idu.ingoodoctets=1,idu.ingoodoctets,if(idu.ingoodoctets>idu2.ingoodoctets,idu.ingoodoctets-idu2.ingoodoctets,0)) as ingoodoctets,  
		if(idu.inbadoctet=1,idu.inbadoctet,if(idu.inbadoctet>idu2.inbadoctet,idu.inbadoctet-idu2.inbadoctet,0)) as inbadoctet,  
		if(idu.outoctets=1,idu.outoctets,if(idu.outoctets>idu2.outoctets,idu.outoctets-idu2.outoctets,0)) as outoctets
		from idu_portstatisticsTable as idu
		join(select * from idu_portstatisticsTable
		where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and softwarestatportnum=NEW.softwarestatportnum
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.softwarestatportnum=idu2.softwarestatportnum 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.softwarestatportnum =NEW.softwarestatportnum
		and idu.framerx<>1 and idu.frametx<>1  
		group by idu2.timestamp,idu2.softwarestatportnum
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.softwarestatportnum asc ) as t3
		group by t3.host_id,t3.software,DATE(t3.timestamp)
		order by t3.timestamp,t3.software,t3.host_id;
		                
        END IF;
        ## WEEKLY
        IF (YEARWEEK(NEW.timestamp)>YEARWEEK(old_time)) 
            THEN
                SET hour_start=subdate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), '%w') DAY);
                SET hour_end= adddate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), INTERVAL 6-DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), '%w') DAY);
                
                INSERT INTO `analyze_idu_portstatisticsTable` (`analyze_idu_portstatisticsTable_id`, `timestamp`, `host_id`, `type`,`softwarestatportnum` ,
                `framerx_Avg`, `framerx_Min`, `framerx_Max`, `framerx_Total`, 
                `frametx_Avg`, `frametx_Min`, `frametx_Max`, `frametx_Total`, 
                `indiscards_Avg`, `indiscards_Min`, `indiscards_Max`, `indiscards_Total`, 
                `ingoodoctets_Avg`, `ingoodoctets_Min`, `ingoodoctets_Max`, `ingoodoctets_Total`, 
                `inbadoctet_Avg`, `inbadoctet_Min`, `inbadoctet_Max`, `inbadoctet_Total`, 
                `outoctets_Avg`, `outoctets_Min`, `outoctets_Max`, `outoctets_Total`) 
                select NULL,hour_start,t3.host_id,'WEEKLY',
		t3.software,
		AVG(t3.framerx),MIN(t3.framerx),MAX(t3.framerx),SUM(t3.framerx),
		AVG(t3.frametx),MIN(t3.frametx),MAX(t3.frametx),SUM(t3.frametx),
		AVG(t3.indiscards),MIN(t3.indiscards),MAX(t3.indiscards),SUM(t3.indiscards),
		AVG(t3.ingoodoctets),MIN(t3.ingoodoctets),MAX(t3.ingoodoctets),SUM(t3.ingoodoctets),
		AVG(t3.inbadoctet),MIN(t3.inbadoctet),MAX(t3.inbadoctet),SUM(t3.inbadoctet),
		AVG(t3.outoctets),MIN(t3.outoctets),MAX(t3.outoctets),SUM(t3.outoctets)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.softwarestatportnum=0,'odu',(if (idu.softwarestatportnum=2,'eth0','eth1')))) as software,    
		if(idu.framerx=1,idu.framerx,if(idu.framerx>idu2.framerx,idu.framerx-idu2.framerx,0)) as framerx,  
		if(idu.frametx=1,idu.frametx,if(idu.frametx>idu2.frametx,idu.frametx-idu2.frametx,0)) as frametx,  
		if(idu.indiscards=1,idu.indiscards,if(idu.indiscards>idu2.indiscards,idu.indiscards-idu2.indiscards,0)) as indiscards,  
		if(idu.ingoodoctets=1,idu.ingoodoctets,if(idu.ingoodoctets>idu2.ingoodoctets,idu.ingoodoctets-idu2.ingoodoctets,0)) as ingoodoctets,  
		if(idu.inbadoctet=1,idu.inbadoctet,if(idu.inbadoctet>idu2.inbadoctet,idu.inbadoctet-idu2.inbadoctet,0)) as inbadoctet,  
		if(idu.outoctets=1,idu.outoctets,if(idu.outoctets>idu2.outoctets,idu.outoctets-idu2.outoctets,0)) as outoctets
		from idu_portstatisticsTable as idu
		join(select * from idu_portstatisticsTable 
		where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and softwarestatportnum=NEW.softwarestatportnum
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.softwarestatportnum=idu2.softwarestatportnum 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.softwarestatportnum =NEW.softwarestatportnum
		and idu.framerx<>1 and idu.frametx<>1  
		group by idu2.timestamp,idu2.softwarestatportnum
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.softwarestatportnum asc ) as t3
		group by t3.host_id,t3.software,YEARWEEK(t3.timestamp)
		order by t3.timestamp,t3.software,t3.host_id;                
                
                
        END IF;
        ## MONTHLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m')>DATE_FORMAT(old_time, '%Y-%m')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-01 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-31 23:59:59');
                INSERT INTO `analyze_idu_portstatisticsTable` (`analyze_idu_portstatisticsTable_id`, `timestamp`, `host_id`, `type`,`softwarestatportnum` ,
                `framerx_Avg`, `framerx_Min`, `framerx_Max`, `framerx_Total`, 
                `frametx_Avg`, `frametx_Min`, `frametx_Max`, `frametx_Total`, 
                `indiscards_Avg`, `indiscards_Min`, `indiscards_Max`, `indiscards_Total`, 
                `ingoodoctets_Avg`, `ingoodoctets_Min`, `ingoodoctets_Max`, `ingoodoctets_Total`, 
                `inbadoctet_Avg`, `inbadoctet_Min`, `inbadoctet_Max`, `inbadoctet_Total`, 
                `outoctets_Avg`, `outoctets_Min`, `outoctets_Max`, `outoctets_Total`) 
                select NULL,CONCAT(DATE_FORMAT(t3.timestamp, '%Y-%m'),'-01 00:00:00'),t3.host_id,'MONTHLY',
		t3.software,
		AVG(t3.framerx),MIN(t3.framerx),MAX(t3.framerx),SUM(t3.framerx),
		AVG(t3.frametx),MIN(t3.frametx),MAX(t3.frametx),SUM(t3.frametx),
		AVG(t3.indiscards),MIN(t3.indiscards),MAX(t3.indiscards),SUM(t3.indiscards),
		AVG(t3.ingoodoctets),MIN(t3.ingoodoctets),MAX(t3.ingoodoctets),SUM(t3.ingoodoctets),
		AVG(t3.inbadoctet),MIN(t3.inbadoctet),MAX(t3.inbadoctet),SUM(t3.inbadoctet),
		AVG(t3.outoctets),MIN(t3.outoctets),MAX(t3.outoctets),SUM(t3.outoctets)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.softwarestatportnum=0,'odu',(if (idu.softwarestatportnum=2,'eth0','eth1')))) as software,    
		if(idu.framerx=1,idu.framerx,if(idu.framerx>idu2.framerx,idu.framerx-idu2.framerx,0)) as framerx,  
		if(idu.frametx=1,idu.frametx,if(idu.frametx>idu2.frametx,idu.frametx-idu2.frametx,0)) as frametx,  
		if(idu.indiscards=1,idu.indiscards,if(idu.indiscards>idu2.indiscards,idu.indiscards-idu2.indiscards,0)) as indiscards,  
		if(idu.ingoodoctets=1,idu.ingoodoctets,if(idu.ingoodoctets>idu2.ingoodoctets,idu.ingoodoctets-idu2.ingoodoctets,0)) as ingoodoctets,  
		if(idu.inbadoctet=1,idu.inbadoctet,if(idu.inbadoctet>idu2.inbadoctet,idu.inbadoctet-idu2.inbadoctet,0)) as inbadoctet,  
		if(idu.outoctets=1,idu.outoctets,if(idu.outoctets>idu2.outoctets,idu.outoctets-idu2.outoctets,0)) as outoctets
		from idu_portstatisticsTable as idu
		join(select * from idu_portstatisticsTable 
		where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and softwarestatportnum=NEW.softwarestatportnum
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.softwarestatportnum=idu2.softwarestatportnum 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.softwarestatportnum =NEW.softwarestatportnum
		and idu.framerx<>1 and idu.frametx<>1  
		group by idu2.timestamp,idu2.softwarestatportnum
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.softwarestatportnum asc ) as t3
		group by t3.host_id,t3.software,DATE_FORMAT(t3.timestamp, '%Y-%m')
		order by t3.timestamp,t3.software,t3.host_id;                
                
        END IF;
    END;
|
delimiter ;


DROP TRIGGER IF EXISTS idu_swPrimaryPortStatisticsTable_trigger;
delimiter |
CREATE TRIGGER idu_swPrimaryPortStatisticsTable_trigger BEFORE INSERT ON idu_swPrimaryPortStatisticsTable
    FOR EACH ROW BEGIN
        DECLARE old_time DATETIME;
        DECLARE n_time DATETIME;
        DECLARE hour_start VARCHAR(25);  
        DECLARE hour_end VARCHAR(25);  
        SELECT timestamp into old_time from idu_swPrimaryPortStatisticsTable where host_id=NEW.host_id and swportnumber=NEW.swportnumber order by timestamp desc limit 1;
        ## HOURLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m-%d %H')>DATE_FORMAT(old_time, '%Y-%m-%d %H')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':59:59');
                INSERT INTO `analyze_idu_swPrimaryPortStatisticsTable` (`analyze_idu_swPrimaryPortStatisticsTable_id`, `timestamp`, `host_id`, `type`,`swportnumber`,
                `framesRx_Avg`, `framesRx_Min`, `framesRx_Max`, `framesRx_Total`, 
                `framesTx_Avg`, `framesTx_Min`, `framesTx_Max`, `framesTx_Total`, 
                `inDiscard_Avg`, `inDiscard_Min`, `inDiscard_Max`, `inDiscard_Total`, 
                `inGoodOctets_Avg`, `inGoodOctets_Min`, `inGoodOctets_Max`, `inGoodOctets_Total`, 
                `inBadOctets_Avg`, `inBadOctets_Min`, `inBadOctets_Max`, `inBadOctets_Total`, 
                `outOctets_Avg`, `outOctets_Min`, `outOctets_Max`, `outOctets_Total`) 
                select NULL,CONCAT_WS(' ',DATE(t3.timestamp),HOUR(t3.timestamp)),t3.host_id,'HOURLY',t3.software,
		AVG(t3.framesRx),MIN(t3.framesRx),MAX(t3.framesRx),SUM(t3.framesRx),
		AVG(t3.framesTx),MIN(t3.framesTx),MAX(t3.framesTx),SUM(t3.framesTx),
		AVG(t3.inDiscard),MIN(t3.inDiscard),MAX(t3.inDiscard),SUM(t3.inDiscard),
		AVG(t3.inGoodOctets),MIN(t3.inGoodOctets),MAX(t3.inGoodOctets),SUM(t3.inGoodOctets),
		AVG(t3.inBadOctets),MIN(t3.inBadOctets),MAX(t3.inBadOctets),SUM(t3.inBadOctets),
		AVG(t3.outOctets),MIN(t3.outOctets),MAX(t3.outOctets),SUM(t3.outOctets)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.swportnumber=0,'odu',(if (idu.swportnumber=2,'eth0','eth1')))) as software,    
		if(idu.framesRx=1,idu.framesRx,if(idu.framesRx>idu2.framesRx,idu.framesRx-idu2.framesRx,0)) as framesRx,  
		if(idu.framesTx=1,idu.framesTx,if(idu.framesTx>idu2.framesTx,idu.framesTx-idu2.framesTx,0)) as framesTx,  
		if(idu.inDiscard=1,idu.inDiscard,if(idu.inDiscard>idu2.inDiscard,idu.inDiscard-idu2.inDiscard,0)) as inDiscard,  
		if(idu.inGoodOctets=1,idu.inGoodOctets,if(idu.inGoodOctets>idu2.inGoodOctets,idu.inGoodOctets-idu2.inGoodOctets,0)) as inGoodOctets,  
		if(idu.inBadOctets=1,idu.inBadOctets,if(idu.inBadOctets>idu2.inBadOctets,idu.inBadOctets-idu2.inBadOctets,0)) as inBadOctets,  
		if(idu.outOctets=1,idu.outOctets,if(idu.outOctets>idu2.outOctets,idu.outOctets-idu2.outOctets,0)) as outOctets
		from idu_swPrimaryPortStatisticsTable as idu
		join(select * from idu_swPrimaryPortStatisticsTable 
		where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and swportnumber=NEW.swportnumber
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.swportnumber=idu2.swportnumber 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.swportnumber =NEW.swportnumber
		and idu.framesRx<>1 and idu.framesTx<>1  
		group by idu2.timestamp,idu2.swportnumber
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.swportnumber asc ) as t3
		group by t3.host_id,t3.software,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
		order by t3.timestamp,t3.software,t3.host_id;

        END IF;
        ## DAILY
        IF (DATE(NEW.timestamp)>DATE(old_time)) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59');
                INSERT INTO `analyze_idu_swPrimaryPortStatisticsTable` (`analyze_idu_swPrimaryPortStatisticsTable_id`, `timestamp`, `host_id`, `type`,`swportnumber` ,
                `framesRx_Avg`, `framesRx_Min`, `framesRx_Max`, `framesRx_Total`, 
                `framesTx_Avg`, `framesTx_Min`, `framesTx_Max`, `framesTx_Total`, 
                `inDiscard_Avg`, `inDiscard_Min`, `inDiscard_Max`, `inDiscard_Total`, 
                `inGoodOctets_Avg`, `inGoodOctets_Min`, `inGoodOctets_Max`, `inGoodOctets_Total`, 
                `inBadOctets_Avg`, `inBadOctets_Min`, `inBadOctets_Max`, `inBadOctets_Total`, 
                `outOctets_Avg`, `outOctets_Min`, `outOctets_Max`, `outOctets_Total`) 
                
                select NULL,DATE(t3.timestamp),t3.host_id,'DAILY',
		t3.software,
		AVG(t3.framesRx),MIN(t3.framesRx),MAX(t3.framesRx),SUM(t3.framesRx),
		AVG(t3.framesTx),MIN(t3.framesTx),MAX(t3.framesTx),SUM(t3.framesTx),
		AVG(t3.inDiscard),MIN(t3.inDiscard),MAX(t3.inDiscard),SUM(t3.inDiscard),
		AVG(t3.inGoodOctets),MIN(t3.inGoodOctets),MAX(t3.inGoodOctets),SUM(t3.inGoodOctets),
		AVG(t3.inBadOctets),MIN(t3.inBadOctets),MAX(t3.inBadOctets),SUM(t3.inBadOctets),
		AVG(t3.outOctets),MIN(t3.outOctets),MAX(t3.outOctets),SUM(t3.outOctets)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.swportnumber=0,'odu',(if (idu.swportnumber=2,'eth0','eth1')))) as software,    
		if(idu.framesRx=1,idu.framesRx,if(idu.framesRx>idu2.framesRx,idu.framesRx-idu2.framesRx,0)) as framesRx,  
		if(idu.framesTx=1,idu.framesTx,if(idu.framesTx>idu2.framesTx,idu.framesTx-idu2.framesTx,0)) as framesTx,  
		if(idu.inDiscard=1,idu.inDiscard,if(idu.inDiscard>idu2.inDiscard,idu.inDiscard-idu2.inDiscard,0)) as inDiscard,  
		if(idu.inGoodOctets=1,idu.inGoodOctets,if(idu.inGoodOctets>idu2.inGoodOctets,idu.inGoodOctets-idu2.inGoodOctets,0)) as inGoodOctets,  
		if(idu.inBadOctets=1,idu.inBadOctets,if(idu.inBadOctets>idu2.inBadOctets,idu.inBadOctets-idu2.inBadOctets,0)) as inBadOctets,  
		if(idu.outOctets=1,idu.outOctets,if(idu.outOctets>idu2.outOctets,idu.outOctets-idu2.outOctets,0)) as outOctets
		from idu_swPrimaryPortStatisticsTable as idu
		join(select * from idu_swPrimaryPortStatisticsTable 
		where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and swportnumber=NEW.swportnumber
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.swportnumber=idu2.swportnumber 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.swportnumber =NEW.swportnumber
		and idu.framesRx<>1 and idu.framesTx<>1  
		group by idu2.timestamp,idu2.swportnumber
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.swportnumber asc ) as t3
		group by t3.host_id,t3.software,DATE(t3.timestamp)
		order by t3.timestamp,t3.software,t3.host_id;
		                
        END IF;
        ## WEEKLY
        IF (YEARWEEK(NEW.timestamp)>YEARWEEK(old_time)) 
            THEN
                SET hour_start=subdate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), '%w') DAY);
                SET hour_end= adddate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), INTERVAL 6-DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), '%w') DAY);
                
                INSERT INTO `analyze_idu_swPrimaryPortStatisticsTable` (`analyze_idu_swPrimaryPortStatisticsTable_id`, `timestamp`, `host_id`, `type`,`swportnumber` ,
                `framesRx_Avg`, `framesRx_Min`, `framesRx_Max`, `framesRx_Total`, 
                `framesTx_Avg`, `framesTx_Min`, `framesTx_Max`, `framesTx_Total`, 
                `inDiscard_Avg`, `inDiscard_Min`, `inDiscard_Max`, `inDiscard_Total`, 
                `inGoodOctets_Avg`, `inGoodOctets_Min`, `inGoodOctets_Max`, `inGoodOctets_Total`, 
                `inBadOctets_Avg`, `inBadOctets_Min`, `inBadOctets_Max`, `inBadOctets_Total`, 
                `outOctets_Avg`, `outOctets_Min`, `outOctets_Max`, `outOctets_Total`) 
                select NULL,hour_start,t3.host_id,'WEEKLY',
		t3.software,
		AVG(t3.framesRx),MIN(t3.framesRx),MAX(t3.framesRx),SUM(t3.framesRx),
		AVG(t3.framesTx),MIN(t3.framesTx),MAX(t3.framesTx),SUM(t3.framesTx),
		AVG(t3.inDiscard),MIN(t3.inDiscard),MAX(t3.inDiscard),SUM(t3.inDiscard),
		AVG(t3.inGoodOctets),MIN(t3.inGoodOctets),MAX(t3.inGoodOctets),SUM(t3.inGoodOctets),
		AVG(t3.inBadOctets),MIN(t3.inBadOctets),MAX(t3.inBadOctets),SUM(t3.inBadOctets),
		AVG(t3.outOctets),MIN(t3.outOctets),MAX(t3.outOctets),SUM(t3.outOctets)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.swportnumber=0,'odu',(if (idu.swportnumber=2,'eth0','eth1')))) as software,    
		if(idu.framesRx=1,idu.framesRx,if(idu.framesRx>idu2.framesRx,idu.framesRx-idu2.framesRx,0)) as framesRx,  
		if(idu.framesTx=1,idu.framesTx,if(idu.framesTx>idu2.framesTx,idu.framesTx-idu2.framesTx,0)) as framesTx,  
		if(idu.inDiscard=1,idu.inDiscard,if(idu.inDiscard>idu2.inDiscard,idu.inDiscard-idu2.inDiscard,0)) as inDiscard,  
		if(idu.inGoodOctets=1,idu.inGoodOctets,if(idu.inGoodOctets>idu2.inGoodOctets,idu.inGoodOctets-idu2.inGoodOctets,0)) as inGoodOctets,  
		if(idu.inBadOctets=1,idu.inBadOctets,if(idu.inBadOctets>idu2.inBadOctets,idu.inBadOctets-idu2.inBadOctets,0)) as inBadOctets,  
		if(idu.outOctets=1,idu.outOctets,if(idu.outOctets>idu2.outOctets,idu.outOctets-idu2.outOctets,0)) as outOctets
		from idu_swPrimaryPortStatisticsTable as idu
		join(select * from idu_swPrimaryPortStatisticsTable where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and swportnumber=NEW.swportnumber
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.swportnumber=idu2.swportnumber 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.swportnumber =NEW.swportnumber
		and idu.framesRx<>1 and idu.framesTx<>1  
		group by idu2.timestamp,idu2.swportnumber
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.swportnumber asc ) as t3
		group by t3.host_id,t3.software,YEARWEEK(t3.timestamp)
		order by t3.timestamp,t3.software,t3.host_id;                
                
                
        END IF;
        ## MONTHLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m')>DATE_FORMAT(old_time, '%Y-%m')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-01 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-31 23:59:59');
                INSERT INTO `analyze_idu_swPrimaryPortStatisticsTable` (`analyze_idu_swPrimaryPortStatisticsTable_id`, `timestamp`, `host_id`, `type`,`swportnumber` ,
                `framesRx_Avg`, `framesRx_Min`, `framesRx_Max`, `framesRx_Total`, 
                `framesTx_Avg`, `framesTx_Min`, `framesTx_Max`, `framesTx_Total`, 
                `inDiscard_Avg`, `inDiscard_Min`, `inDiscard_Max`, `inDiscard_Total`, 
                `inGoodOctets_Avg`, `inGoodOctets_Min`, `inGoodOctets_Max`, `inGoodOctets_Total`, 
                `inBadOctets_Avg`, `inBadOctets_Min`, `inBadOctets_Max`, `inBadOctets_Total`, 
                `outOctets_Avg`, `outOctets_Min`, `outOctets_Max`, `outOctets_Total`) 
                select NULL,CONCAT(DATE_FORMAT(t3.timestamp, '%Y-%m'),'-01 00:00:00'),t3.host_id,'MONTHLY',
		t3.software,
		AVG(t3.framesRx),MIN(t3.framesRx),MAX(t3.framesRx),SUM(t3.framesRx),
		AVG(t3.framesTx),MIN(t3.framesTx),MAX(t3.framesTx),SUM(t3.framesTx),
		AVG(t3.inDiscard),MIN(t3.inDiscard),MAX(t3.inDiscard),SUM(t3.inDiscard),
		AVG(t3.inGoodOctets),MIN(t3.inGoodOctets),MAX(t3.inGoodOctets),SUM(t3.inGoodOctets),
		AVG(t3.inBadOctets),MIN(t3.inBadOctets),MAX(t3.inBadOctets),SUM(t3.inBadOctets),
		AVG(t3.outOctets),MIN(t3.outOctets),MAX(t3.outOctets),SUM(t3.outOctets)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.swportnumber=0,'odu',(if (idu.swportnumber=2,'eth0','eth1')))) as software,    
		if(idu.framesRx=1,idu.framesRx,if(idu.framesRx>idu2.framesRx,idu.framesRx-idu2.framesRx,0)) as framesRx,  
		if(idu.framesTx=1,idu.framesTx,if(idu.framesTx>idu2.framesTx,idu.framesTx-idu2.framesTx,0)) as framesTx,  
		if(idu.inDiscard=1,idu.inDiscard,if(idu.inDiscard>idu2.inDiscard,idu.inDiscard-idu2.inDiscard,0)) as inDiscard,  
		if(idu.inGoodOctets=1,idu.inGoodOctets,if(idu.inGoodOctets>idu2.inGoodOctets,idu.inGoodOctets-idu2.inGoodOctets,0)) as inGoodOctets,  
		if(idu.inBadOctets=1,idu.inBadOctets,if(idu.inBadOctets>idu2.inBadOctets,idu.inBadOctets-idu2.inBadOctets,0)) as inBadOctets,  
		if(idu.outOctets=1,idu.outOctets,if(idu.outOctets>idu2.outOctets,idu.outOctets-idu2.outOctets,0)) as outOctets
		from idu_swPrimaryPortStatisticsTable as idu
		join(select * from idu_swPrimaryPortStatisticsTable where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and swportnumber=NEW.swportnumber
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.swportnumber=idu2.swportnumber 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.swportnumber =NEW.swportnumber
		and idu.framesRx<>1 and idu.framesTx<>1  
		group by idu2.timestamp,idu2.swportnumber
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.swportnumber asc ) as t3
		group by t3.host_id,t3.software,DATE_FORMAT(t3.timestamp, '%Y-%m')
		order by t3.timestamp,t3.software,t3.host_id;                
                
        END IF;
    END;
|
delimiter ;


DROP TRIGGER IF EXISTS idu_portSecondaryStatisticsTable_trigger;
delimiter |
CREATE TRIGGER idu_portSecondaryStatisticsTable_trigger BEFORE INSERT ON idu_portSecondaryStatisticsTable
    FOR EACH ROW BEGIN
        DECLARE old_time DATETIME;
        DECLARE n_time DATETIME;
        DECLARE hour_start VARCHAR(25);  
        DECLARE hour_end VARCHAR(25);  
        SELECT timestamp into old_time from idu_portSecondaryStatisticsTable where host_id=NEW.host_id and switchPortNum=NEW.switchPortNum order by timestamp desc limit 1;
        ## HOURLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m-%d %H')>DATE_FORMAT(old_time, '%Y-%m-%d %H')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':59:59');
                INSERT INTO `analyze_idu_portSecondaryStatisticsTable` (`analyze_idu_portSecondaryStatisticsTable_id`, `timestamp`, `host_id`, `type`,`switchPortNum`,
                `inUnicast_Avg`, `inUnicast_Min`, `inUnicast_Max`, `inUnicast_Total`, 
                `outUnicast_Avg`, `outUnicast_Min`, `outUnicast_Max`, `outUnicast_Total`, 
                `inBroadcast_Avg`, `inBroadcast_Min`, `inBroadcast_Max`, `inBroadcast_Total`, 
                `outBroadcast_Avg`, `outBroadcast_Min`, `outBroadcast_Max`, `outBroadcast_Total`, 
                `inMulticast_Avg`, `inMulticast_Min`, `inMulticast_Max`, `inMulticast_Total`, 
                `outMulricast_Avg`, `outMulricast_Min`, `outMulricast_Max`, `outMulricast_Total`,
                `inUndersizeRx_Avg`, `inUndersizeRx_Min`, `inUndersizeRx_Max`, `inUndersizeRx_Total`, 
                `inFragmentsRx_Avg`, `inFragmentsRx_Min`, `inFragmentsRx_Max`, `inFragmentsRx_Total`, 
                `inOversizeRx_Avg`, `inOversizeRx_Min`, `inOversizeRx_Max`, `inOversizeRx_Total`, 
                `inJabberRx_Avg`, `inJabberRx_Min`, `inJabberRx_Max`, `inJabberRx_Total`, 
                `inMacRcvErrorRx_Avg`, `inMacRcvErrorRx_Min`, `inMacRcvErrorRx_Max`, `inMacRcvErrorRx_Total`, 
                `inFCSErrorRx_Avg`, `inFCSErrorRx_Min`, `inFCSErrorRx_Max`, `inFCSErrorRx_Total`,
                `outFCSErrorTx_Avg`, `outFCSErrorTx_Min`, `outFCSErrorTx_Max`, `outFCSErrorTx_Total`, 
                `deferedTx_Avg`, `deferedTx_Min`, `deferedTx_Max`, `deferedTx_Total`, 
                `collisionTx_Avg`, `collisionTx_Min`, `collisionTx_Max`, `collisionTx_Total`, 
                `lateTx_Avg`, `lateTx_Min`, `lateTx_Max`, `lateTx_Total`, 
                `exessiveTx_Avg`, `exessiveTx_Min`, `exessiveTx_Max`, `exessiveTx_Total`, 
                `singleTx_Avg`, `singleTx_Min`, `singleTx_Max`, `singleTx_Total`,
                `multipleTx_Avg`, `multipleTx_Min`, `multipleTx_Max`, `multipleTx_Total`)   
                select NULL,CONCAT_WS(' ',DATE(t3.timestamp),HOUR(t3.timestamp)),t3.host_id,'HOURLY',t3.software,
		AVG(t3.inUnicast),MIN(t3.inUnicast),MAX(t3.inUnicast),SUM(t3.inUnicast),
		AVG(t3.outUnicast),MIN(t3.outUnicast),MAX(t3.outUnicast),SUM(t3.outUnicast),
		AVG(t3.inBroadcast),MIN(t3.inBroadcast),MAX(t3.inBroadcast),SUM(t3.inBroadcast),
		AVG(t3.outBroadcast),MIN(t3.outBroadcast),MAX(t3.outBroadcast),SUM(t3.outBroadcast),
		AVG(t3.inMulticast),MIN(t3.inMulticast),MAX(t3.inMulticast),SUM(t3.inMulticast),
		AVG(t3.outMulricast),MIN(t3.outMulricast),MAX(t3.outMulricast),SUM(t3.outMulricast),
		AVG(t3.inUndersizeRx),MIN(t3.inUndersizeRx),MAX(t3.inUndersizeRx),SUM(t3.inUndersizeRx),
		AVG(t3.inFragmentsRx),MIN(t3.inFragmentsRx),MAX(t3.inFragmentsRx),SUM(t3.inFragmentsRx),
		AVG(t3.inOversizeRx),MIN(t3.inOversizeRx),MAX(t3.inOversizeRx),SUM(t3.inOversizeRx),
		AVG(t3.inJabberRx),MIN(t3.inJabberRx),MAX(t3.inJabberRx),SUM(t3.inJabberRx),
		AVG(t3.inMacRcvErrorRx),MIN(t3.inMacRcvErrorRx),MAX(t3.inMacRcvErrorRx),SUM(t3.inMacRcvErrorRx),
		AVG(t3.inFCSErrorRx),MIN(t3.inFCSErrorRx),MAX(t3.inFCSErrorRx),SUM(t3.inFCSErrorRx),
		AVG(t3.outFCSErrorTx),MIN(t3.outFCSErrorTx),MAX(t3.outFCSErrorTx),SUM(t3.outFCSErrorTx),
		AVG(t3.deferedTx),MIN(t3.deferedTx),MAX(t3.deferedTx),SUM(t3.deferedTx),
		AVG(t3.collisionTx),MIN(t3.collisionTx),MAX(t3.collisionTx),SUM(t3.collisionTx),
		AVG(t3.lateTx),MIN(t3.lateTx),MAX(t3.lateTx),SUM(t3.lateTx),
		AVG(t3.exessiveTx),MIN(t3.exessiveTx),MAX(t3.exessiveTx),SUM(t3.exessiveTx),
		AVG(t3.singleTx),MIN(t3.singleTx),MAX(t3.singleTx),SUM(t3.singleTx),
		AVG(t3.multipleTx),MIN(t3.multipleTx),MAX(t3.multipleTx),SUM(t3.multipleTx)
		
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.switchPortNum=0,'odu',(if (idu.switchPortNum=2,'eth0','eth1')))) as software,    
		if(idu.inUnicast=1,idu.inUnicast,if(idu.inUnicast>idu2.inUnicast,idu.inUnicast-idu2.inUnicast,0)) as inUnicast,  
		if(idu.outUnicast=1,idu.outUnicast,if(idu.outUnicast>idu2.outUnicast,idu.outUnicast-idu2.outUnicast,0)) as outUnicast,  
		if(idu.inBroadcast=1,idu.inBroadcast,if(idu.inBroadcast>idu2.inBroadcast,idu.inBroadcast-idu2.inBroadcast,0)) as inBroadcast,  
		if(idu.outBroadcast=1,idu.outBroadcast,if(idu.outBroadcast>idu2.outBroadcast,idu.outBroadcast-idu2.outBroadcast,0)) as outBroadcast,  
		if(idu.inMulticast=1,idu.inMulticast,if(idu.inMulticast>idu2.inMulticast,idu.inMulticast-idu2.inMulticast,0)) as inMulticast,  
		if(idu.outMulricast=1,idu.outMulricast,if(idu.outMulricast>idu2.outMulricast,idu.outMulricast-idu2.outMulricast,0)) as outMulricast,
		if(idu.inUndersizeRx=1,idu.inUndersizeRx,if(idu.inUndersizeRx>idu2.inUndersizeRx,idu.inUndersizeRx-idu2.inUndersizeRx,0)) as inUndersizeRx,  
		if(idu.inFragmentsRx=1,idu.inFragmentsRx,if(idu.inFragmentsRx>idu2.inFragmentsRx,idu.inFragmentsRx-idu2.inFragmentsRx,0)) as inFragmentsRx,  
		if(idu.inOversizeRx=1,idu.inOversizeRx,if(idu.inOversizeRx>idu2.inOversizeRx,idu.inOversizeRx-idu2.inOversizeRx,0)) as inOversizeRx,  
		if(idu.inJabberRx=1,idu.inJabberRx,if(idu.inJabberRx>idu2.inJabberRx,idu.inJabberRx-idu2.inJabberRx,0)) as inJabberRx,  
		if(idu.inMacRcvErrorRx=1,idu.inMacRcvErrorRx,if(idu.inMacRcvErrorRx>idu2.inMacRcvErrorRx,idu.inMacRcvErrorRx-idu2.inMacRcvErrorRx,0)) as inMacRcvErrorRx,  
		if(idu.inFCSErrorRx=1,idu.inFCSErrorRx,if(idu.inFCSErrorRx>idu2.inFCSErrorRx,idu.inFCSErrorRx-idu2.inFCSErrorRx,0)) as inFCSErrorRx,
		if(idu.outFCSErrorTx=1,idu.outFCSErrorTx,if(idu.outFCSErrorTx>idu2.outFCSErrorTx,idu.outFCSErrorTx-idu2.outFCSErrorTx,0)) as outFCSErrorTx,  
		if(idu.deferedTx=1,idu.deferedTx,if(idu.deferedTx>idu2.deferedTx,idu.deferedTx-idu2.deferedTx,0)) as deferedTx,  
		if(idu.collisionTx=1,idu.collisionTx,if(idu.collisionTx>idu2.collisionTx,idu.collisionTx-idu2.collisionTx,0)) as collisionTx,  
		if(idu.lateTx=1,idu.lateTx,if(idu.lateTx>idu2.lateTx,idu.lateTx-idu2.lateTx,0)) as lateTx,  
		if(idu.exessiveTx=1,idu.exessiveTx,if(idu.exessiveTx>idu2.exessiveTx,idu.exessiveTx-idu2.exessiveTx,0)) as exessiveTx,  
		if(idu.singleTx=1,idu.singleTx,if(idu.singleTx>idu2.singleTx,idu.singleTx-idu2.singleTx,0)) as singleTx,
		if(idu.multipleTx=1,idu.multipleTx,if(idu.multipleTx>idu2.multipleTx,idu.multipleTx-idu2.multipleTx,0)) as multipleTx
		
		from idu_portSecondaryStatisticsTable as idu
		join(select * from idu_portSecondaryStatisticsTable 
		where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and switchPortNum=NEW.switchPortNum
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.switchPortNum=idu2.switchPortNum 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.switchPortNum =NEW.switchPortNum
		and idu.inUnicast<>1 and idu.outUnicast<>1  
		group by idu2.timestamp,idu2.switchPortNum
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.switchPortNum asc ) as t3
		group by t3.host_id,t3.software,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
		order by t3.timestamp,t3.software,t3.host_id;

        END IF;
        ## DAILY
        IF (DATE(NEW.timestamp)>DATE(old_time)) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59');
                INSERT INTO `analyze_idu_portSecondaryStatisticsTable` (`analyze_idu_portSecondaryStatisticsTable_id`, `timestamp`, `host_id`, `type`,`switchPortNum` ,
                `inUnicast_Avg`, `inUnicast_Min`, `inUnicast_Max`, `inUnicast_Total`, 
                `outUnicast_Avg`, `outUnicast_Min`, `outUnicast_Max`, `outUnicast_Total`, 
                `inBroadcast_Avg`, `inBroadcast_Min`, `inBroadcast_Max`, `inBroadcast_Total`, 
                `outBroadcast_Avg`, `outBroadcast_Min`, `outBroadcast_Max`, `outBroadcast_Total`, 
                `inMulticast_Avg`, `inMulticast_Min`, `inMulticast_Max`, `inMulticast_Total`, 
                `outMulricast_Avg`, `outMulricast_Min`, `outMulricast_Max`, `outMulricast_Total`,
                `inUndersizeRx_Avg`, `inUndersizeRx_Min`, `inUndersizeRx_Max`, `inUndersizeRx_Total`, 
                `inFragmentsRx_Avg`, `inFragmentsRx_Min`, `inFragmentsRx_Max`, `inFragmentsRx_Total`, 
                `inOversizeRx_Avg`, `inOversizeRx_Min`, `inOversizeRx_Max`, `inOversizeRx_Total`, 
                `inJabberRx_Avg`, `inJabberRx_Min`, `inJabberRx_Max`, `inJabberRx_Total`, 
                `inMacRcvErrorRx_Avg`, `inMacRcvErrorRx_Min`, `inMacRcvErrorRx_Max`, `inMacRcvErrorRx_Total`, 
                `inFCSErrorRx_Avg`, `inFCSErrorRx_Min`, `inFCSErrorRx_Max`, `inFCSErrorRx_Total`,
                `outFCSErrorTx_Avg`, `outFCSErrorTx_Min`, `outFCSErrorTx_Max`, `outFCSErrorTx_Total`, 
                `deferedTx_Avg`, `deferedTx_Min`, `deferedTx_Max`, `deferedTx_Total`, 
                `collisionTx_Avg`, `collisionTx_Min`, `collisionTx_Max`, `collisionTx_Total`, 
                `lateTx_Avg`, `lateTx_Min`, `lateTx_Max`, `lateTx_Total`, 
                `exessiveTx_Avg`, `exessiveTx_Min`, `exessiveTx_Max`, `exessiveTx_Total`, 
                `singleTx_Avg`, `singleTx_Min`, `singleTx_Max`, `singleTx_Total`,
                `multipleTx_Avg`, `multipleTx_Min`, `multipleTx_Max`, `multipleTx_Total`)   
                
                select NULL,DATE(t3.timestamp),t3.host_id,'DAILY',
		t3.software,
		AVG(t3.inUnicast),MIN(t3.inUnicast),MAX(t3.inUnicast),SUM(t3.inUnicast),
		AVG(t3.outUnicast),MIN(t3.outUnicast),MAX(t3.outUnicast),SUM(t3.outUnicast),
		AVG(t3.inBroadcast),MIN(t3.inBroadcast),MAX(t3.inBroadcast),SUM(t3.inBroadcast),
		AVG(t3.outBroadcast),MIN(t3.outBroadcast),MAX(t3.outBroadcast),SUM(t3.outBroadcast),
		AVG(t3.inMulticast),MIN(t3.inMulticast),MAX(t3.inMulticast),SUM(t3.inMulticast),
		AVG(t3.outMulricast),MIN(t3.outMulricast),MAX(t3.outMulricast),SUM(t3.outMulricast),
		AVG(t3.inUndersizeRx),MIN(t3.inUndersizeRx),MAX(t3.inUndersizeRx),SUM(t3.inUndersizeRx),
		AVG(t3.inFragmentsRx),MIN(t3.inFragmentsRx),MAX(t3.inFragmentsRx),SUM(t3.inFragmentsRx),
		AVG(t3.inOversizeRx),MIN(t3.inOversizeRx),MAX(t3.inOversizeRx),SUM(t3.inOversizeRx),
		AVG(t3.inJabberRx),MIN(t3.inJabberRx),MAX(t3.inJabberRx),SUM(t3.inJabberRx),
		AVG(t3.inMacRcvErrorRx),MIN(t3.inMacRcvErrorRx),MAX(t3.inMacRcvErrorRx),SUM(t3.inMacRcvErrorRx),
		AVG(t3.inFCSErrorRx),MIN(t3.inFCSErrorRx),MAX(t3.inFCSErrorRx),SUM(t3.inFCSErrorRx),
		AVG(t3.outFCSErrorTx),MIN(t3.outFCSErrorTx),MAX(t3.outFCSErrorTx),SUM(t3.outFCSErrorTx),
		AVG(t3.deferedTx),MIN(t3.deferedTx),MAX(t3.deferedTx),SUM(t3.deferedTx),
		AVG(t3.collisionTx),MIN(t3.collisionTx),MAX(t3.collisionTx),SUM(t3.collisionTx),
		AVG(t3.lateTx),MIN(t3.lateTx),MAX(t3.lateTx),SUM(t3.lateTx),
		AVG(t3.exessiveTx),MIN(t3.exessiveTx),MAX(t3.exessiveTx),SUM(t3.exessiveTx),
		AVG(t3.singleTx),MIN(t3.singleTx),MAX(t3.singleTx),SUM(t3.singleTx),
		AVG(t3.multipleTx),MIN(t3.multipleTx),MAX(t3.multipleTx),SUM(t3.multipleTx)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.switchPortNum=0,'odu',(if (idu.switchPortNum=2,'eth0','eth1')))) as software,    
		if(idu.inUnicast=1,idu.inUnicast,if(idu.inUnicast>idu2.inUnicast,idu.inUnicast-idu2.inUnicast,0)) as inUnicast,  
		if(idu.outUnicast=1,idu.outUnicast,if(idu.outUnicast>idu2.outUnicast,idu.outUnicast-idu2.outUnicast,0)) as outUnicast,  
		if(idu.inBroadcast=1,idu.inBroadcast,if(idu.inBroadcast>idu2.inBroadcast,idu.inBroadcast-idu2.inBroadcast,0)) as inBroadcast,  
		if(idu.outBroadcast=1,idu.outBroadcast,if(idu.outBroadcast>idu2.outBroadcast,idu.outBroadcast-idu2.outBroadcast,0)) as outBroadcast,  
		if(idu.inMulticast=1,idu.inMulticast,if(idu.inMulticast>idu2.inMulticast,idu.inMulticast-idu2.inMulticast,0)) as inMulticast,  
		if(idu.outMulricast=1,idu.outMulricast,if(idu.outMulricast>idu2.outMulricast,idu.outMulricast-idu2.outMulricast,0)) as outMulricast,
		if(idu.inUndersizeRx=1,idu.inUndersizeRx,if(idu.inUndersizeRx>idu2.inUndersizeRx,idu.inUndersizeRx-idu2.inUndersizeRx,0)) as inUndersizeRx,  
		if(idu.inFragmentsRx=1,idu.inFragmentsRx,if(idu.inFragmentsRx>idu2.inFragmentsRx,idu.inFragmentsRx-idu2.inFragmentsRx,0)) as inFragmentsRx,  
		if(idu.inOversizeRx=1,idu.inOversizeRx,if(idu.inOversizeRx>idu2.inOversizeRx,idu.inOversizeRx-idu2.inOversizeRx,0)) as inOversizeRx,  
		if(idu.inJabberRx=1,idu.inJabberRx,if(idu.inJabberRx>idu2.inJabberRx,idu.inJabberRx-idu2.inJabberRx,0)) as inJabberRx,  
		if(idu.inMacRcvErrorRx=1,idu.inMacRcvErrorRx,if(idu.inMacRcvErrorRx>idu2.inMacRcvErrorRx,idu.inMacRcvErrorRx-idu2.inMacRcvErrorRx,0)) as inMacRcvErrorRx,  
		if(idu.inFCSErrorRx=1,idu.inFCSErrorRx,if(idu.inFCSErrorRx>idu2.inFCSErrorRx,idu.inFCSErrorRx-idu2.inFCSErrorRx,0)) as inFCSErrorRx,
		if(idu.outFCSErrorTx=1,idu.outFCSErrorTx,if(idu.outFCSErrorTx>idu2.outFCSErrorTx,idu.outFCSErrorTx-idu2.outFCSErrorTx,0)) as outFCSErrorTx,  
		if(idu.deferedTx=1,idu.deferedTx,if(idu.deferedTx>idu2.deferedTx,idu.deferedTx-idu2.deferedTx,0)) as deferedTx,  
		if(idu.collisionTx=1,idu.collisionTx,if(idu.collisionTx>idu2.collisionTx,idu.collisionTx-idu2.collisionTx,0)) as collisionTx,  
		if(idu.lateTx=1,idu.lateTx,if(idu.lateTx>idu2.lateTx,idu.lateTx-idu2.lateTx,0)) as lateTx,  
		if(idu.exessiveTx=1,idu.exessiveTx,if(idu.exessiveTx>idu2.exessiveTx,idu.exessiveTx-idu2.exessiveTx,0)) as exessiveTx,  
		if(idu.singleTx=1,idu.singleTx,if(idu.singleTx>idu2.singleTx,idu.singleTx-idu2.singleTx,0)) as singleTx,
		if(idu.multipleTx=1,idu.multipleTx,if(idu.multipleTx>idu2.multipleTx,idu.multipleTx-idu2.multipleTx,0)) as multipleTx
		from idu_portSecondaryStatisticsTable as idu
		join(select * from idu_portSecondaryStatisticsTable 
		where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and switchPortNum=NEW.switchPortNum
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.switchPortNum=idu2.switchPortNum 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.switchPortNum =NEW.switchPortNum
		and idu.inUnicast<>1 and idu.outUnicast<>1  
		group by idu2.timestamp,idu2.switchPortNum
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.switchPortNum asc ) as t3
		group by t3.host_id,t3.software,DATE(t3.timestamp)
		order by t3.timestamp,t3.software,t3.host_id;
		                
        END IF;
        ## WEEKLY
        IF (YEARWEEK(NEW.timestamp)>YEARWEEK(old_time)) 
            THEN
                SET hour_start=subdate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), '%w') DAY);
                SET hour_end= adddate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), INTERVAL 6-DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), '%w') DAY);
                
                INSERT INTO `analyze_idu_portSecondaryStatisticsTable` (`analyze_idu_portSecondaryStatisticsTable_id`, `timestamp`, `host_id`, `type`,`switchPortNum` ,
                `inUnicast_Avg`, `inUnicast_Min`, `inUnicast_Max`, `inUnicast_Total`, 
                `outUnicast_Avg`, `outUnicast_Min`, `outUnicast_Max`, `outUnicast_Total`, 
                `inBroadcast_Avg`, `inBroadcast_Min`, `inBroadcast_Max`, `inBroadcast_Total`, 
                `outBroadcast_Avg`, `outBroadcast_Min`, `outBroadcast_Max`, `outBroadcast_Total`, 
                `inMulticast_Avg`, `inMulticast_Min`, `inMulticast_Max`, `inMulticast_Total`, 
                `outMulricast_Avg`, `outMulricast_Min`, `outMulricast_Max`, `outMulricast_Total`,
                `inUndersizeRx_Avg`, `inUndersizeRx_Min`, `inUndersizeRx_Max`, `inUndersizeRx_Total`, 
                `inFragmentsRx_Avg`, `inFragmentsRx_Min`, `inFragmentsRx_Max`, `inFragmentsRx_Total`, 
                `inOversizeRx_Avg`, `inOversizeRx_Min`, `inOversizeRx_Max`, `inOversizeRx_Total`, 
                `inJabberRx_Avg`, `inJabberRx_Min`, `inJabberRx_Max`, `inJabberRx_Total`, 
                `inMacRcvErrorRx_Avg`, `inMacRcvErrorRx_Min`, `inMacRcvErrorRx_Max`, `inMacRcvErrorRx_Total`, 
                `inFCSErrorRx_Avg`, `inFCSErrorRx_Min`, `inFCSErrorRx_Max`, `inFCSErrorRx_Total`,
                `outFCSErrorTx_Avg`, `outFCSErrorTx_Min`, `outFCSErrorTx_Max`, `outFCSErrorTx_Total`, 
                `deferedTx_Avg`, `deferedTx_Min`, `deferedTx_Max`, `deferedTx_Total`, 
                `collisionTx_Avg`, `collisionTx_Min`, `collisionTx_Max`, `collisionTx_Total`, 
                `lateTx_Avg`, `lateTx_Min`, `lateTx_Max`, `lateTx_Total`, 
                `exessiveTx_Avg`, `exessiveTx_Min`, `exessiveTx_Max`, `exessiveTx_Total`, 
                `singleTx_Avg`, `singleTx_Min`, `singleTx_Max`, `singleTx_Total`,
                `multipleTx_Avg`, `multipleTx_Min`, `multipleTx_Max`, `multipleTx_Total`)  
                select NULL,hour_start,t3.host_id,'WEEKLY',
		t3.software,
		AVG(t3.inUnicast),MIN(t3.inUnicast),MAX(t3.inUnicast),SUM(t3.inUnicast),
		AVG(t3.outUnicast),MIN(t3.outUnicast),MAX(t3.outUnicast),SUM(t3.outUnicast),
		AVG(t3.inBroadcast),MIN(t3.inBroadcast),MAX(t3.inBroadcast),SUM(t3.inBroadcast),
		AVG(t3.outBroadcast),MIN(t3.outBroadcast),MAX(t3.outBroadcast),SUM(t3.outBroadcast),
		AVG(t3.inMulticast),MIN(t3.inMulticast),MAX(t3.inMulticast),SUM(t3.inMulticast),
		AVG(t3.outMulricast),MIN(t3.outMulricast),MAX(t3.outMulricast),SUM(t3.outMulricast),
		AVG(t3.inUndersizeRx),MIN(t3.inUndersizeRx),MAX(t3.inUndersizeRx),SUM(t3.inUndersizeRx),
		AVG(t3.inFragmentsRx),MIN(t3.inFragmentsRx),MAX(t3.inFragmentsRx),SUM(t3.inFragmentsRx),
		AVG(t3.inOversizeRx),MIN(t3.inOversizeRx),MAX(t3.inOversizeRx),SUM(t3.inOversizeRx),
		AVG(t3.inJabberRx),MIN(t3.inJabberRx),MAX(t3.inJabberRx),SUM(t3.inJabberRx),
		AVG(t3.inMacRcvErrorRx),MIN(t3.inMacRcvErrorRx),MAX(t3.inMacRcvErrorRx),SUM(t3.inMacRcvErrorRx),
		AVG(t3.inFCSErrorRx),MIN(t3.inFCSErrorRx),MAX(t3.inFCSErrorRx),SUM(t3.inFCSErrorRx),
		AVG(t3.outFCSErrorTx),MIN(t3.outFCSErrorTx),MAX(t3.outFCSErrorTx),SUM(t3.outFCSErrorTx),
		AVG(t3.deferedTx),MIN(t3.deferedTx),MAX(t3.deferedTx),SUM(t3.deferedTx),
		AVG(t3.collisionTx),MIN(t3.collisionTx),MAX(t3.collisionTx),SUM(t3.collisionTx),
		AVG(t3.lateTx),MIN(t3.lateTx),MAX(t3.lateTx),SUM(t3.lateTx),
		AVG(t3.exessiveTx),MIN(t3.exessiveTx),MAX(t3.exessiveTx),SUM(t3.exessiveTx),
		AVG(t3.singleTx),MIN(t3.singleTx),MAX(t3.singleTx),SUM(t3.singleTx),
		AVG(t3.multipleTx),MIN(t3.multipleTx),MAX(t3.multipleTx),SUM(t3.multipleTx)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.switchPortNum=0,'odu',(if (idu.switchPortNum=2,'eth0','eth1')))) as software,    
		if(idu.inUnicast=1,idu.inUnicast,if(idu.inUnicast>idu2.inUnicast,idu.inUnicast-idu2.inUnicast,0)) as inUnicast,  
		if(idu.outUnicast=1,idu.outUnicast,if(idu.outUnicast>idu2.outUnicast,idu.outUnicast-idu2.outUnicast,0)) as outUnicast,  
		if(idu.inBroadcast=1,idu.inBroadcast,if(idu.inBroadcast>idu2.inBroadcast,idu.inBroadcast-idu2.inBroadcast,0)) as inBroadcast,  
		if(idu.outBroadcast=1,idu.outBroadcast,if(idu.outBroadcast>idu2.outBroadcast,idu.outBroadcast-idu2.outBroadcast,0)) as outBroadcast,  
		if(idu.inMulticast=1,idu.inMulticast,if(idu.inMulticast>idu2.inMulticast,idu.inMulticast-idu2.inMulticast,0)) as inMulticast,  
		if(idu.outMulricast=1,idu.outMulricast,if(idu.outMulricast>idu2.outMulricast,idu.outMulricast-idu2.outMulricast,0)) as outMulricast,
		if(idu.inUndersizeRx=1,idu.inUndersizeRx,if(idu.inUndersizeRx>idu2.inUndersizeRx,idu.inUndersizeRx-idu2.inUndersizeRx,0)) as inUndersizeRx,  
		if(idu.inFragmentsRx=1,idu.inFragmentsRx,if(idu.inFragmentsRx>idu2.inFragmentsRx,idu.inFragmentsRx-idu2.inFragmentsRx,0)) as inFragmentsRx,  
		if(idu.inOversizeRx=1,idu.inOversizeRx,if(idu.inOversizeRx>idu2.inOversizeRx,idu.inOversizeRx-idu2.inOversizeRx,0)) as inOversizeRx,  
		if(idu.inJabberRx=1,idu.inJabberRx,if(idu.inJabberRx>idu2.inJabberRx,idu.inJabberRx-idu2.inJabberRx,0)) as inJabberRx,  
		if(idu.inMacRcvErrorRx=1,idu.inMacRcvErrorRx,if(idu.inMacRcvErrorRx>idu2.inMacRcvErrorRx,idu.inMacRcvErrorRx-idu2.inMacRcvErrorRx,0)) as inMacRcvErrorRx,  
		if(idu.inFCSErrorRx=1,idu.inFCSErrorRx,if(idu.inFCSErrorRx>idu2.inFCSErrorRx,idu.inFCSErrorRx-idu2.inFCSErrorRx,0)) as inFCSErrorRx,
		if(idu.outFCSErrorTx=1,idu.outFCSErrorTx,if(idu.outFCSErrorTx>idu2.outFCSErrorTx,idu.outFCSErrorTx-idu2.outFCSErrorTx,0)) as outFCSErrorTx,  
		if(idu.deferedTx=1,idu.deferedTx,if(idu.deferedTx>idu2.deferedTx,idu.deferedTx-idu2.deferedTx,0)) as deferedTx,  
		if(idu.collisionTx=1,idu.collisionTx,if(idu.collisionTx>idu2.collisionTx,idu.collisionTx-idu2.collisionTx,0)) as collisionTx,  
		if(idu.lateTx=1,idu.lateTx,if(idu.lateTx>idu2.lateTx,idu.lateTx-idu2.lateTx,0)) as lateTx,  
		if(idu.exessiveTx=1,idu.exessiveTx,if(idu.exessiveTx>idu2.exessiveTx,idu.exessiveTx-idu2.exessiveTx,0)) as exessiveTx,  
		if(idu.singleTx=1,idu.singleTx,if(idu.singleTx>idu2.singleTx,idu.singleTx-idu2.singleTx,0)) as singleTx,
		if(idu.multipleTx=1,idu.multipleTx,if(idu.multipleTx>idu2.multipleTx,idu.multipleTx-idu2.multipleTx,0)) as multipleTx
		from idu_portSecondaryStatisticsTable as idu
		join(select * from idu_portSecondaryStatisticsTable
		 where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and switchPortNum=NEW.switchPortNum
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.switchPortNum=idu2.switchPortNum 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.switchPortNum =NEW.switchPortNum
		and idu.inUnicast<>1 and idu.outUnicast<>1  
		group by idu2.timestamp,idu2.switchPortNum
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.switchPortNum asc ) as t3
		group by t3.host_id,t3.software,YEARWEEK(t3.timestamp)
		order by t3.timestamp,t3.software,t3.host_id;                
                
                
        END IF;
        ## MONTHLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m')>DATE_FORMAT(old_time, '%Y-%m')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-01 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-31 23:59:59');
                INSERT INTO `analyze_idu_portSecondaryStatisticsTable` (`analyze_idu_portSecondaryStatisticsTable_id`, `timestamp`, `host_id`, `type`,`switchPortNum` ,
                `inUnicast_Avg`, `inUnicast_Min`, `inUnicast_Max`, `inUnicast_Total`, 
                `outUnicast_Avg`, `outUnicast_Min`, `outUnicast_Max`, `outUnicast_Total`, 
                `inBroadcast_Avg`, `inBroadcast_Min`, `inBroadcast_Max`, `inBroadcast_Total`, 
                `outBroadcast_Avg`, `outBroadcast_Min`, `outBroadcast_Max`, `outBroadcast_Total`, 
                `inMulticast_Avg`, `inMulticast_Min`, `inMulticast_Max`, `inMulticast_Total`, 
                `outMulricast_Avg`, `outMulricast_Min`, `outMulricast_Max`, `outMulricast_Total`,
                `inUndersizeRx_Avg`, `inUndersizeRx_Min`, `inUndersizeRx_Max`, `inUndersizeRx_Total`, 
                `inFragmentsRx_Avg`, `inFragmentsRx_Min`, `inFragmentsRx_Max`, `inFragmentsRx_Total`, 
                `inOversizeRx_Avg`, `inOversizeRx_Min`, `inOversizeRx_Max`, `inOversizeRx_Total`, 
                `inJabberRx_Avg`, `inJabberRx_Min`, `inJabberRx_Max`, `inJabberRx_Total`, 
                `inMacRcvErrorRx_Avg`, `inMacRcvErrorRx_Min`, `inMacRcvErrorRx_Max`, `inMacRcvErrorRx_Total`, 
                `inFCSErrorRx_Avg`, `inFCSErrorRx_Min`, `inFCSErrorRx_Max`, `inFCSErrorRx_Total`,
                `outFCSErrorTx_Avg`, `outFCSErrorTx_Min`, `outFCSErrorTx_Max`, `outFCSErrorTx_Total`, 
                `deferedTx_Avg`, `deferedTx_Min`, `deferedTx_Max`, `deferedTx_Total`, 
                `collisionTx_Avg`, `collisionTx_Min`, `collisionTx_Max`, `collisionTx_Total`, 
                `lateTx_Avg`, `lateTx_Min`, `lateTx_Max`, `lateTx_Total`, 
                `exessiveTx_Avg`, `exessiveTx_Min`, `exessiveTx_Max`, `exessiveTx_Total`, 
                `singleTx_Avg`, `singleTx_Min`, `singleTx_Max`, `singleTx_Total`,
                `multipleTx_Avg`, `multipleTx_Min`, `multipleTx_Max`, `multipleTx_Total`) 
                select NULL,CONCAT(DATE_FORMAT(t3.timestamp, '%Y-%m'),'-01 00:00:00'),t3.host_id,'MONTHLY',
		t3.software,
		AVG(t3.inUnicast),MIN(t3.inUnicast),MAX(t3.inUnicast),SUM(t3.inUnicast),
		AVG(t3.outUnicast),MIN(t3.outUnicast),MAX(t3.outUnicast),SUM(t3.outUnicast),
		AVG(t3.inBroadcast),MIN(t3.inBroadcast),MAX(t3.inBroadcast),SUM(t3.inBroadcast),
		AVG(t3.outBroadcast),MIN(t3.outBroadcast),MAX(t3.outBroadcast),SUM(t3.outBroadcast),
		AVG(t3.inMulticast),MIN(t3.inMulticast),MAX(t3.inMulticast),SUM(t3.inMulticast),
		AVG(t3.outMulricast),MIN(t3.outMulricast),MAX(t3.outMulricast),SUM(t3.outMulricast),
		AVG(t3.inUndersizeRx),MIN(t3.inUndersizeRx),MAX(t3.inUndersizeRx),SUM(t3.inUndersizeRx),
		AVG(t3.inFragmentsRx),MIN(t3.inFragmentsRx),MAX(t3.inFragmentsRx),SUM(t3.inFragmentsRx),
		AVG(t3.inOversizeRx),MIN(t3.inOversizeRx),MAX(t3.inOversizeRx),SUM(t3.inOversizeRx),
		AVG(t3.inJabberRx),MIN(t3.inJabberRx),MAX(t3.inJabberRx),SUM(t3.inJabberRx),
		AVG(t3.inMacRcvErrorRx),MIN(t3.inMacRcvErrorRx),MAX(t3.inMacRcvErrorRx),SUM(t3.inMacRcvErrorRx),
		AVG(t3.inFCSErrorRx),MIN(t3.inFCSErrorRx),MAX(t3.inFCSErrorRx),SUM(t3.inFCSErrorRx),
		AVG(t3.outFCSErrorTx),MIN(t3.outFCSErrorTx),MAX(t3.outFCSErrorTx),SUM(t3.outFCSErrorTx),
		AVG(t3.deferedTx),MIN(t3.deferedTx),MAX(t3.deferedTx),SUM(t3.deferedTx),
		AVG(t3.collisionTx),MIN(t3.collisionTx),MAX(t3.collisionTx),SUM(t3.collisionTx),
		AVG(t3.lateTx),MIN(t3.lateTx),MAX(t3.lateTx),SUM(t3.lateTx),
		AVG(t3.exessiveTx),MIN(t3.exessiveTx),MAX(t3.exessiveTx),SUM(t3.exessiveTx),
		AVG(t3.singleTx),MIN(t3.singleTx),MAX(t3.singleTx),SUM(t3.singleTx),
		AVG(t3.multipleTx),MIN(t3.multipleTx),MAX(t3.multipleTx),SUM(t3.multipleTx)
		from (
		select 
		idu.timestamp,idu.host_id,
		(if(idu.switchPortNum=0,'odu',(if (idu.switchPortNum=2,'eth0','eth1')))) as software,    
		if(idu.inUnicast=1,idu.inUnicast,if(idu.inUnicast>idu2.inUnicast,idu.inUnicast-idu2.inUnicast,0)) as inUnicast,  
		if(idu.outUnicast=1,idu.outUnicast,if(idu.outUnicast>idu2.outUnicast,idu.outUnicast-idu2.outUnicast,0)) as outUnicast,  
		if(idu.inBroadcast=1,idu.inBroadcast,if(idu.inBroadcast>idu2.inBroadcast,idu.inBroadcast-idu2.inBroadcast,0)) as inBroadcast,  
		if(idu.outBroadcast=1,idu.outBroadcast,if(idu.outBroadcast>idu2.outBroadcast,idu.outBroadcast-idu2.outBroadcast,0)) as outBroadcast,  
		if(idu.inMulticast=1,idu.inMulticast,if(idu.inMulticast>idu2.inMulticast,idu.inMulticast-idu2.inMulticast,0)) as inMulticast,  
		if(idu.outMulricast=1,idu.outMulricast,if(idu.outMulricast>idu2.outMulricast,idu.outMulricast-idu2.outMulricast,0)) as outMulricast,
		if(idu.inUndersizeRx=1,idu.inUndersizeRx,if(idu.inUndersizeRx>idu2.inUndersizeRx,idu.inUndersizeRx-idu2.inUndersizeRx,0)) as inUndersizeRx,  
		if(idu.inFragmentsRx=1,idu.inFragmentsRx,if(idu.inFragmentsRx>idu2.inFragmentsRx,idu.inFragmentsRx-idu2.inFragmentsRx,0)) as inFragmentsRx,  
		if(idu.inOversizeRx=1,idu.inOversizeRx,if(idu.inOversizeRx>idu2.inOversizeRx,idu.inOversizeRx-idu2.inOversizeRx,0)) as inOversizeRx,  
		if(idu.inJabberRx=1,idu.inJabberRx,if(idu.inJabberRx>idu2.inJabberRx,idu.inJabberRx-idu2.inJabberRx,0)) as inJabberRx,  
		if(idu.inMacRcvErrorRx=1,idu.inMacRcvErrorRx,if(idu.inMacRcvErrorRx>idu2.inMacRcvErrorRx,idu.inMacRcvErrorRx-idu2.inMacRcvErrorRx,0)) as inMacRcvErrorRx,  
		if(idu.inFCSErrorRx=1,idu.inFCSErrorRx,if(idu.inFCSErrorRx>idu2.inFCSErrorRx,idu.inFCSErrorRx-idu2.inFCSErrorRx,0)) as inFCSErrorRx,
		if(idu.outFCSErrorTx=1,idu.outFCSErrorTx,if(idu.outFCSErrorTx>idu2.outFCSErrorTx,idu.outFCSErrorTx-idu2.outFCSErrorTx,0)) as outFCSErrorTx,  
		if(idu.deferedTx=1,idu.deferedTx,if(idu.deferedTx>idu2.deferedTx,idu.deferedTx-idu2.deferedTx,0)) as deferedTx,  
		if(idu.collisionTx=1,idu.collisionTx,if(idu.collisionTx>idu2.collisionTx,idu.collisionTx-idu2.collisionTx,0)) as collisionTx,  
		if(idu.lateTx=1,idu.lateTx,if(idu.lateTx>idu2.lateTx,idu.lateTx-idu2.lateTx,0)) as lateTx,  
		if(idu.exessiveTx=1,idu.exessiveTx,if(idu.exessiveTx>idu2.exessiveTx,idu.exessiveTx-idu2.exessiveTx,0)) as exessiveTx,  
		if(idu.singleTx=1,idu.singleTx,if(idu.singleTx>idu2.singleTx,idu.singleTx-idu2.singleTx,0)) as singleTx,
		if(idu.multipleTx=1,idu.multipleTx,if(idu.multipleTx>idu2.multipleTx,idu.multipleTx-idu2.multipleTx,0)) as multipleTx
		from idu_portSecondaryStatisticsTable as idu
		join(select * from idu_portSecondaryStatisticsTable 
		where host_id=NEW.host_id and timestamp between  hour_start and hour_end
		 and switchPortNum=NEW.switchPortNum
		 ) as idu2 on idu.timestamp>idu2.timestamp and idu.switchPortNum=idu2.switchPortNum 
		 and idu.host_id=NEW.host_id
		and idu.host_id=idu2.host_id where  idu.timestamp between  hour_start and hour_end  
		and idu2.timestamp between  hour_start and hour_end  and idu.switchPortNum =NEW.switchPortNum
		and idu.inUnicast<>1 and idu.outUnicast<>1  
		group by idu2.timestamp,idu2.switchPortNum
		order by idu2.host_id asc ,  idu2.timestamp asc , idu2.switchPortNum asc ) as t3
		group by t3.host_id,t3.software,DATE_FORMAT(t3.timestamp, '%Y-%m')
		order by t3.timestamp,t3.software,t3.host_id;                
                
        END IF;
    END;
|
delimiter ;


