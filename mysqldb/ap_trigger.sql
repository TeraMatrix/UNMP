
DROP TRIGGER IF EXISTS `ap25_statisticsTable_trigger`;
DELIMITER //
CREATE TRIGGER `ap25_statisticsTable_trigger` BEFORE INSERT ON `ap25_statisticsTable`
 FOR EACH ROW BEGIN
        DECLARE old_time DATETIME;
        DECLARE n_time DATETIME;
        DECLARE hour_start VARCHAR(25);  
        DECLARE hour_end VARCHAR(25);  
        SELECT timestamp into old_time from ap25_statisticsTable where host_id=NEW.host_id and `index`=0 order by timestamp desc limit 1;
        ## HOURLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m-%d %H')>DATE_FORMAT(old_time, '%Y-%m-%d %H')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d %H'),':59:59');
                INSERT INTO `analyze_ap25_statisticsTable` (`analyze_ap25_statisticsTable_id`, `timestamp`,   `host_id`,`type`,
                  `index_0_statisticsRxPackets_Avg`,  `index_0_statisticsRxPackets_Min`,  `index_0_statisticsRxPackets_Max`,  `index_0_statisticsRxPackets_Total`, 
		  `index_0_statisticsTxPackets_Avg`,  `index_0_statisticsTxPackets_Min`,  `index_0_statisticsTxPackets_Max`,  `index_0_statisticsTxPackets_Total`, 
		  `index_0_statisticsRxError_Avg`,    `index_0_statisticsRxError_Min`,    `index_0_statisticsRxError_Max`,    `index_0_statisticsRxError_Total`, 
		  `index_0_statisticsTxError_Avg`,    `index_0_statisticsTxError_Min`,    `index_0_statisticsTxError_Max`,    `index_0_statisticsTxError_Total`)
                select NULL,CONCAT_WS(' ',DATE(t3.timestamp),HOUR(t3.timestamp)),t3.host_id,'HOURLY',
                AVG(t3.delta_statisticsRxPackets),MIN(t3.delta_statisticsRxPackets),MAX(t3.delta_statisticsRxPackets),SUM(t3.delta_statisticsRxPackets),
		AVG(t3.delta_statisticsTxPackets),MIN(t3.delta_statisticsTxPackets),MAX(t3.delta_statisticsTxPackets),SUM(t3.delta_statisticsTxPackets),
		AVG(t3.delta_statisticsRxError),MIN(t3.delta_statisticsRxError),MAX(t3.delta_statisticsRxError),SUM(t3.delta_statisticsRxError),
		AVG(t3.delta_statisticsTxError),MIN(t3.delta_statisticsTxError),MAX(t3.delta_statisticsTxError),SUM(t3.delta_statisticsTxError)
		
                from (
                    SELECT 
	                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
	                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=0 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=0) as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where t1.host_id=NEW.host_id and t1.`index`=0 and t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`statisticsRxError`<>1111111 and t2.`statisticsTxError`<>1111111  
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc
                ) as t3
                group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                order by t3.timestamp,t3.`index`,t3.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=1 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=1 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=1 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_1_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_1_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_1_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_1_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_1_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_1_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_1_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_1_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_1_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_1_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_1_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_1_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_1_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_1_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_1_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_1_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=2 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=2 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=2 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_2_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_2_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_2_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_2_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_2_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_2_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_2_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_2_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_2_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_2_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_2_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_2_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_2_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_2_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_2_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_2_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=3 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=3 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=3 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_3_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_3_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_3_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_3_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_3_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_3_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_3_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_3_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_3_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_3_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_3_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_3_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_3_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_3_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_3_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_3_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=4 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=4 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=4 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_4_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_4_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_4_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_4_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_4_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_4_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_4_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_4_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_4_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_4_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_4_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_4_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_4_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_4_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_4_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_4_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=5 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=5 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=5 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_5_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_5_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_5_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_5_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_5_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_5_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_5_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_5_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_5_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_5_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_5_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_5_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_5_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_5_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_5_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_5_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;





 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=6 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=6 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=6 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_6_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_6_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_6_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_6_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_6_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_6_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_6_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_6_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_6_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_6_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_6_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_6_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_6_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_6_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_6_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_6_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;





 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=7 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=7 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=7 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_7_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_7_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_7_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_7_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_7_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_7_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_7_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_7_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_7_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_7_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_7_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_7_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_7_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_7_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_7_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_7_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=8 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=8 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=8 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_8_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_8_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_8_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_8_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_8_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_8_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_8_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_8_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_8_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_8_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_8_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_8_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_8_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_8_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_8_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_8_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=9 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=9 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=9 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_9_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_9_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_9_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_9_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_9_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_9_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_9_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_9_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_9_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_9_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_9_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_9_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_9_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_9_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_9_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_9_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=10 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=10 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=10 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                    group by t3.host_id,t3.`index`,CONCAT(DATE(t3.timestamp),HOUR(t3.timestamp))
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_10_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_10_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_10_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_10_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_10_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_10_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_10_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_10_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_10_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_10_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_10_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_10_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_10_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_10_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_10_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_10_statisticsTxError_Total` =delta_statisticsTxError_Total
                where CONCAT_WS(' ',DATE(t5.timestamp),HOUR(t5.timestamp))=CONCAT_WS(' ',DATE(ap.timestamp),HOUR(ap.timestamp)) and 
                    t5.host_id=ap.host_id;



        END IF;
        
                ## DAILY
         IF (DATE(NEW.timestamp)>DATE(old_time)) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59');
                INSERT INTO `analyze_ap25_statisticsTable` (`analyze_ap25_statisticsTable_id`, `timestamp`,   `host_id`,`type`,
                  `index_0_statisticsRxPackets_Avg`,  `index_0_statisticsRxPackets_Min`,  `index_0_statisticsRxPackets_Max`,  `index_0_statisticsRxPackets_Total`, 
		  `index_0_statisticsTxPackets_Avg`,  `index_0_statisticsTxPackets_Min`,  `index_0_statisticsTxPackets_Max`,  `index_0_statisticsTxPackets_Total`, 
		  `index_0_statisticsRxError_Avg`,    `index_0_statisticsRxError_Min`,    `index_0_statisticsRxError_Max`,    `index_0_statisticsRxError_Total`, 
		  `index_0_statisticsTxError_Avg`,    `index_0_statisticsTxError_Min`,    `index_0_statisticsTxError_Max`,    `index_0_statisticsTxError_Total`)
               select NULL,DATE(t3.timestamp),t3.host_id,'DAILY',
                AVG(t3.delta_statisticsRxPackets),MIN(t3.delta_statisticsRxPackets),MAX(t3.delta_statisticsRxPackets),SUM(t3.delta_statisticsRxPackets),
		AVG(t3.delta_statisticsTxPackets),MIN(t3.delta_statisticsTxPackets),MAX(t3.delta_statisticsTxPackets),SUM(t3.delta_statisticsTxPackets),
		AVG(t3.delta_statisticsRxError),MIN(t3.delta_statisticsRxError),MAX(t3.delta_statisticsRxError),SUM(t3.delta_statisticsRxError),
		AVG(t3.delta_statisticsTxError),MIN(t3.delta_statisticsTxError),MAX(t3.delta_statisticsTxError),SUM(t3.delta_statisticsTxError)
		
                from (
                    SELECT 
	                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
	                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=0 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=0) as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where t1.host_id=NEW.host_id and t1.`index`=0 and t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`statisticsRxError`<>1111111 and t2.`statisticsTxError`<>1111111  
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc
                ) as t3
                group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                order by t3.timestamp,t3.`index`,t3.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=1 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=1 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=1 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_1_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_1_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_1_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_1_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_1_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_1_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_1_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_1_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_1_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_1_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_1_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_1_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_1_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_1_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_1_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_1_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=2 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=2 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=2 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_2_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_2_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_2_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_2_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_2_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_2_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_2_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_2_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_2_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_2_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_2_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_2_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_2_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_2_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_2_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_2_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=3 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=3 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=3 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_3_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_3_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_3_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_3_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_3_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_3_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_3_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_3_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_3_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_3_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_3_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_3_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_3_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_3_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_3_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_3_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=4 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=4 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=4 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_4_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_4_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_4_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_4_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_4_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_4_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_4_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_4_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_4_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_4_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_4_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_4_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_4_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_4_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_4_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_4_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=5 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=5 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=5 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_5_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_5_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_5_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_5_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_5_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_5_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_5_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_5_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_5_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_5_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_5_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_5_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_5_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_5_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_5_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_5_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;





 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=6 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=6 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=6 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_6_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_6_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_6_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_6_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_6_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_6_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_6_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_6_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_6_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_6_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_6_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_6_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_6_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_6_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_6_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_6_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;





 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=7 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=7 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=7 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_7_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_7_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_7_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_7_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_7_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_7_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_7_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_7_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_7_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_7_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_7_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_7_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_7_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_7_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_7_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_7_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=8 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=8 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=8 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_8_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_8_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_8_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_8_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_8_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_8_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_8_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_8_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_8_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_8_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_8_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_8_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_8_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_8_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_8_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_8_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=9 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=9 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=9 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_9_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_9_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_9_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_9_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_9_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_9_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_9_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_9_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_9_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_9_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_9_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_9_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_9_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_9_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_9_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_9_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;




 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=10 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=10 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=10 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                     group by t3.host_id,t3.`index`,DATE(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_10_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_10_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_10_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_10_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_10_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_10_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_10_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_10_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_10_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_10_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_10_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_10_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_10_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_10_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_10_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_10_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  DATE(t5.timestamp)=DATE(ap.timestamp) and  
                    t5.host_id=ap.host_id;



        END IF;
        
               ## WEEKLY
        IF (YEARWEEK(NEW.timestamp)>YEARWEEK(old_time)) 
            THEN
                SET hour_start=subdate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 00:00:00'), '%w') DAY);
                SET hour_end= adddate(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), INTERVAL 6-DATE_FORMAT(CONCAT(DATE_FORMAT(old_time,'%Y-%m-%d'),' 23:59:59'), '%w') DAY);
                INSERT INTO `analyze_ap25_statisticsTable` (`analyze_ap25_statisticsTable_id`, `timestamp`,   `host_id`,`type`,
                  `index_0_statisticsRxPackets_Avg`,  `index_0_statisticsRxPackets_Min`,  `index_0_statisticsRxPackets_Max`,  `index_0_statisticsRxPackets_Total`, 
		  `index_0_statisticsTxPackets_Avg`,  `index_0_statisticsTxPackets_Min`,  `index_0_statisticsTxPackets_Max`,  `index_0_statisticsTxPackets_Total`, 
		  `index_0_statisticsRxError_Avg`,    `index_0_statisticsRxError_Min`,    `index_0_statisticsRxError_Max`,    `index_0_statisticsRxError_Total`, 
		  `index_0_statisticsTxError_Avg`,    `index_0_statisticsTxError_Min`,    `index_0_statisticsTxError_Max`,    `index_0_statisticsTxError_Total`)
                select NULL,hour_start,t3.host_id,'WEEKLY',
                AVG(t3.delta_statisticsRxPackets),MIN(t3.delta_statisticsRxPackets),MAX(t3.delta_statisticsRxPackets),SUM(t3.delta_statisticsRxPackets),
		AVG(t3.delta_statisticsTxPackets),MIN(t3.delta_statisticsTxPackets),MAX(t3.delta_statisticsTxPackets),SUM(t3.delta_statisticsTxPackets),
		AVG(t3.delta_statisticsRxError),MIN(t3.delta_statisticsRxError),MAX(t3.delta_statisticsRxError),SUM(t3.delta_statisticsRxError),
		AVG(t3.delta_statisticsTxError),MIN(t3.delta_statisticsTxError),MAX(t3.delta_statisticsTxError),SUM(t3.delta_statisticsTxError)
		
                from (
                    SELECT 
	                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
	                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=0 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=0) as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where t1.host_id=NEW.host_id and t1.`index`=0 and t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`statisticsRxError`<>1111111 and t2.`statisticsTxError`<>1111111  
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc
                ) as t3
                   group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                order by t3.timestamp,t3.`index`,t3.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=1 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=1 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=1 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_1_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_1_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_1_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_1_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_1_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_1_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_1_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_1_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_1_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_1_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_1_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_1_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_1_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_1_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_1_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_1_statisticsTxError_Total` =delta_statisticsTxError_Total
             where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;

 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=2 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=2 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=2 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_2_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_2_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_2_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_2_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_2_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_2_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_2_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_2_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_2_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_2_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_2_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_2_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_2_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_2_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_2_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_2_statisticsTxError_Total` =delta_statisticsTxError_Total
             where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=3 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=3 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=3 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_3_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_3_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_3_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_3_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_3_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_3_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_3_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_3_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_3_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_3_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_3_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_3_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_3_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_3_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_3_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_3_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=4 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=4 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=4 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_4_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_4_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_4_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_4_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_4_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_4_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_4_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_4_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_4_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_4_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_4_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_4_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_4_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_4_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_4_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_4_statisticsTxError_Total` =delta_statisticsTxError_Total
              where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=5 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=5 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=5 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_5_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_5_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_5_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_5_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_5_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_5_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_5_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_5_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_5_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_5_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_5_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_5_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_5_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_5_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_5_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_5_statisticsTxError_Total` =delta_statisticsTxError_Total
               where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=6 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=6 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=6 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_6_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_6_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_6_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_6_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_6_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_6_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_6_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_6_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_6_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_6_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_6_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_6_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_6_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_6_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_6_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_6_statisticsTxError_Total` =delta_statisticsTxError_Total
             where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=7 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=7 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=7 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_7_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_7_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_7_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_7_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_7_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_7_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_7_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_7_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_7_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_7_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_7_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_7_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_7_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_7_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_7_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_7_statisticsTxError_Total` =delta_statisticsTxError_Total
              where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=8 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=8 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=8 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_8_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_8_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_8_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_8_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_8_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_8_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_8_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_8_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_8_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_8_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_8_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_8_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_8_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_8_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_8_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_8_statisticsTxError_Total` =delta_statisticsTxError_Total
              where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=9 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=9 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=9 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_9_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_9_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_9_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_9_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_9_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_9_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_9_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_9_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_9_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_9_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_9_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_9_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_9_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_9_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_9_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_9_statisticsTxError_Total` =delta_statisticsTxError_Total
              where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=10 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=10 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=10 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,YEARWEEK(t3.timestamp)
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_10_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_10_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_10_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_10_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_10_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_10_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_10_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_10_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_10_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_10_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_10_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_10_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_10_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_10_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_10_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_10_statisticsTxError_Total` =delta_statisticsTxError_Total
             where  subdate(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), INTERVAL DATE_FORMAT(CONCAT(DATE_FORMAT(t5.timestamp,'%Y-%m-%d'),' 00:00:00'), '%w') DAY)
                =DATE(ap.timestamp) and t5.host_id=ap.host_id;


        END IF;
        
        	## MONTHLY
        IF (DATE_FORMAT(NEW.timestamp, '%Y-%m')>DATE_FORMAT(old_time, '%Y-%m')) 
            THEN
                SET hour_start=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-01 00:00:00');
                SET hour_end=CONCAT(DATE_FORMAT(old_time,'%Y-%m'),'-31 23:59:59');
                INSERT INTO `analyze_ap25_statisticsTable` (`analyze_ap25_statisticsTable_id`, `timestamp`,   `host_id`,`type`,
                  `index_0_statisticsRxPackets_Avg`,  `index_0_statisticsRxPackets_Min`,  `index_0_statisticsRxPackets_Max`,  `index_0_statisticsRxPackets_Total`, 
		  `index_0_statisticsTxPackets_Avg`,  `index_0_statisticsTxPackets_Min`,  `index_0_statisticsTxPackets_Max`,  `index_0_statisticsTxPackets_Total`, 
		  `index_0_statisticsRxError_Avg`,    `index_0_statisticsRxError_Min`,    `index_0_statisticsRxError_Max`,    `index_0_statisticsRxError_Total`, 
		  `index_0_statisticsTxError_Avg`,    `index_0_statisticsTxError_Min`,    `index_0_statisticsTxError_Max`,    `index_0_statisticsTxError_Total`)
               select NULL,CONCAT(DATE_FORMAT(t3.timestamp, '%Y-%m'),'-01 00:00:00'),t3.host_id,'MONTHLY',
                AVG(t3.delta_statisticsRxPackets),MIN(t3.delta_statisticsRxPackets),MAX(t3.delta_statisticsRxPackets),SUM(t3.delta_statisticsRxPackets),
		AVG(t3.delta_statisticsTxPackets),MIN(t3.delta_statisticsTxPackets),MAX(t3.delta_statisticsTxPackets),SUM(t3.delta_statisticsTxPackets),
		AVG(t3.delta_statisticsRxError),MIN(t3.delta_statisticsRxError),MAX(t3.delta_statisticsRxError),SUM(t3.delta_statisticsRxError),
		AVG(t3.delta_statisticsTxError),MIN(t3.delta_statisticsTxError),MAX(t3.delta_statisticsTxError),SUM(t3.delta_statisticsTxError)
		
                from (
                    SELECT 
	                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
	                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=0 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=0) as t2 
                        on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where t1.host_id=NEW.host_id and t1.`index`=0 and t1.timestamp between hour_start and hour_end
         	           and t2.timestamp between hour_start and hour_end 
         	           and t2.`statisticsRxError`<>1111111 and t2.`statisticsTxError`<>1111111  
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc
                ) as t3
                   group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                order by t3.timestamp,t3.`index`,t3.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=1 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=1 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=1 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_1_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_1_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_1_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_1_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_1_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_1_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_1_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_1_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_1_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_1_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_1_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_1_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_1_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_1_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_1_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_1_statisticsTxError_Total` =delta_statisticsTxError_Total
             where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=2 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=2 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=2 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_2_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_2_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_2_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_2_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_2_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_2_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_2_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_2_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_2_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_2_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_2_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_2_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_2_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_2_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_2_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_2_statisticsTxError_Total` =delta_statisticsTxError_Total
             where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=3 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=3 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=3 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_3_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_3_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_3_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_3_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_3_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_3_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_3_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_3_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_3_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_3_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_3_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_3_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_3_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_3_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_3_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_3_statisticsTxError_Total` =delta_statisticsTxError_Total
                where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=4 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=4 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=4 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_4_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_4_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_4_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_4_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_4_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_4_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_4_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_4_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_4_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_4_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_4_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_4_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_4_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_4_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_4_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_4_statisticsTxError_Total` =delta_statisticsTxError_Total
               where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;

 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=5 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=5 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=5 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_5_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_5_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_5_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_5_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_5_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_5_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_5_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_5_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_5_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_5_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_5_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_5_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_5_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_5_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_5_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_5_statisticsTxError_Total` =delta_statisticsTxError_Total
               where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=6 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=6 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=6 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_6_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_6_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_6_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_6_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_6_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_6_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_6_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_6_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_6_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_6_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_6_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_6_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_6_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_6_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_6_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_6_statisticsTxError_Total` =delta_statisticsTxError_Total
             where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=7 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=7 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=7 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_7_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_7_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_7_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_7_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_7_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_7_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_7_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_7_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_7_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_7_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_7_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_7_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_7_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_7_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_7_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_7_statisticsTxError_Total` =delta_statisticsTxError_Total
              where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;



 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=8 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=8 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=8 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_8_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_8_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_8_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_8_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_8_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_8_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_8_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_8_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_8_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_8_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_8_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_8_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_8_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_8_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_8_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_8_statisticsTxError_Total` =delta_statisticsTxError_Total
               where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=9 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=9 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=9 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_9_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_9_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_9_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_9_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_9_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_9_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_9_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_9_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_9_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_9_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_9_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_9_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_9_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_9_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_9_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_9_statisticsTxError_Total` =delta_statisticsTxError_Total
               where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;


 		update analyze_ap25_statisticsTable as ap ,(select  t3.timestamp,t3.host_id,
                AVG(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Avg,MIN(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Min,
                MAX(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Max,SUM(t3.delta_statisticsRxPackets) as delta_statisticsRxPackets_Total,
                AVG(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Avg,MIN(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Min,
                MAX(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Max,SUM(t3.delta_statisticsTxPackets) as delta_statisticsTxPackets_Total,
                AVG(t3.delta_statisticsRxError) as delta_statisticsRxError_Avg,MIN(t3.delta_statisticsRxError) as delta_statisticsRxError_Min,
                MAX(t3.delta_statisticsRxError) as delta_statisticsRxError_Max,SUM(t3.delta_statisticsRxError) as delta_statisticsRxError_Total,
                AVG(t3.delta_statisticsTxError) as delta_statisticsTxError_Avg,MIN(t3.delta_statisticsTxError) as delta_statisticsTxError_Min,
                MAX(t3.delta_statisticsTxError) as delta_statisticsTxError_Max,SUM(t3.delta_statisticsTxError) as delta_statisticsTxError_Total
                from (
                SELECT 
                    if(t2.`statisticsRxPackets`>t1.`statisticsRxPackets`,t2.`statisticsRxPackets`-t1.`statisticsRxPackets`,0) as delta_statisticsRxPackets,
	                    if(t2.`statisticsTxPackets`>t1.`statisticsTxPackets`,t2.`statisticsTxPackets`-t1.`statisticsTxPackets`,0) as delta_statisticsTxPackets,
	                    if(t2.`statisticsRxError`>t1.`statisticsRxError`,t2.`statisticsRxError`-t1.`statisticsRxError`,0) as delta_statisticsRxError,
	                    if(t2.`statisticsTxError`>t1.`statisticsTxError`,t2.`statisticsTxError`-t1.`statisticsTxError`,0) as delta_statisticsTxError,
                    t2.host_id,t2.`index`,t2.timestamp
                    FROM ( select * from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=10 )as t1
                    inner join (select `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`,host_id,`index`,timestamp 
                    from `ap25_statisticsTable` where host_id=NEW.host_id and timestamp between hour_start and hour_end and `index`=10 ) as t2 
                    on t2.timestamp>t1.timestamp and t2.host_id=t1.host_id and t2.`index`=t1.`index`
                    where  t1.`index`=10 and t2.`statisticsRxError`<>1111111 and t2.`statisticsRxError`<>1111111 
                    group by t1.timestamp,t1.`index`
                    order by t1.timestamp asc ,t1.host_id asc , t1.`index` asc ) as t3
                        group by t3.host_id,t3.`index`,DATE_FORMAT(t3.timestamp, '%Y-%m')
                    order by t3.timestamp,t3.`index`,t3.host_id) as t5
                set 
                    `index_10_statisticsRxPackets_Avg` =delta_statisticsRxPackets_Avg,
		   `index_10_statisticsRxPackets_Min` =delta_statisticsRxPackets_Min,
		   `index_10_statisticsRxPackets_Max` =delta_statisticsRxPackets_Max,
		   `index_10_statisticsRxPackets_Total` =delta_statisticsRxPackets_Total,
		     `index_10_statisticsTxPackets_Avg` =delta_statisticsTxPackets_Avg,
		   `index_10_statisticsTxPackets_Min` =delta_statisticsTxPackets_Min,
		   `index_10_statisticsTxPackets_Max` =delta_statisticsTxPackets_Max,
		   `index_10_statisticsTxPackets_Total` =delta_statisticsTxPackets_Total,
		   `index_10_statisticsRxError_Avg` =delta_statisticsRxError_Avg,
		   `index_10_statisticsRxError_Min` =delta_statisticsRxError_Min,
		   `index_10_statisticsRxError_Max` =delta_statisticsRxError_Max,
		   `index_10_statisticsRxError_Total` =delta_statisticsRxError_Total,
		   `index_10_statisticsTxError_Avg` =delta_statisticsTxError_Avg,
		   `index_10_statisticsTxError_Min` =delta_statisticsTxError_Min,
		   `index_10_statisticsTxError_Max` =delta_statisticsTxError_Max,
		   `index_10_statisticsTxError_Total` =delta_statisticsTxError_Total
             where DATE_FORMAT(t5.timestamp, '%Y-%m')=DATE_FORMAT(ap.timestamp, '%Y-%m') and 
                    t5.host_id=ap.host_id;


        END IF;
    END
//
DELIMITER ;
