alter table get_odu16_nw_interface_statistics_table
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);

alter table get_odu16_synch_statistics_table
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);
alter table get_odu16_peer_node_status_table
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);


alter table get_odu16_ra_tdd_mac_statistics_entry 
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);



alter table event_log
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);


alter table odu100_nwInterfaceStatisticsTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);


alter table odu100_synchStatisticsTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);



alter table odu100_raTddMacStatisticsTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);


alter table odu100_raScanListTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);

alter table odu100_peerNodeStatusTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);

alter table idu_tdmoipNetworkInterfaceStatisticsTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);



alter table idu_iduNetworkStatisticsTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);


alter table idu_e1PortStatusTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);


alter table idu_linkStatusTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);



alter table idu_portSecondaryStatisticsTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);



alter table idu_portstatisticsTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);



alter table idu_swPrimaryPortStatisticsTable
PARTITION BY RANGE(TO_DAYS(timestamp) )
(
PARTITION p107 VALUES LESS THAN (TO_DAYS('2011-07-01')),
PARTITION p108 VALUES LESS THAN (TO_DAYS('2011-08-01')),
PARTITION p109 VALUES LESS THAN (TO_DAYS('2011-09-01')),
PARTITION p110 VALUES LESS THAN (TO_DAYS('2011-10-01')),
PARTITION p111 VALUES LESS THAN (TO_DAYS('2011-11-01')),
PARTITION p112 VALUES LESS THAN (TO_DAYS('2011-12-01')),
PARTITION p201 VALUES LESS THAN (TO_DAYS('2012-01-01')),
PARTITION p202 VALUES LESS THAN (TO_DAYS('2012-02-01')),
PARTITION p203 VALUES LESS THAN (TO_DAYS('2012-03-01')),
PARTITION p204 VALUES LESS THAN (TO_DAYS('2012-04-01')),
PARTITION p205 VALUES LESS THAN (TO_DAYS('2012-05-01')),
PARTITION p206 VALUES LESS THAN (TO_DAYS('2012-06-01')),
PARTITION p207 VALUES LESS THAN (TO_DAYS('2012-07-01')),
PARTITION p208 VALUES LESS THAN (TO_DAYS('2012-08-01')),
PARTITION p209 VALUES LESS THAN (TO_DAYS('2012-09-01')),
PARTITION p210 VALUES LESS THAN (TO_DAYS('2012-10-01')),
PARTITION p211 VALUES LESS THAN (TO_DAYS('2012-11-01')),
PARTITION p212 VALUES LESS THAN (TO_DAYS('2012-12-01'))
);

