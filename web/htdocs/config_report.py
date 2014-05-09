#!/usr/bin/python2.6
from copy import deepcopy
import csv
from datetime import date, timedelta, datetime

import MySQLdb
import xlwt
from common_controller import object_model_di
from unmp_config import SystemConfig

# db=MySQLdb.connect("localhost","root","root","nms")
# cursor=db.cursor()
# q=" SELECT table_name,column_name FROM information_schema.columns WHERE
# table_name like 'odu100_%' AND table_schema = 'nms' "
di = {}
# cursor.execute(q)
# res=cursor.fetchall()
# for i in res:
#    di[i[0]+"."+i[1]] = i[1]


device_status = 'master'

order_report_dict = {
    'odu16': ['Radio Unit', 'LLC Configuration', 'Synchronization', 'ACL', 'Radio Frequency', 'Peer MAC', 'UNMP'],
    'odu100': ['Radio Unit', 'LLC Configuration', 'Synchronization', 'ACL', 'Radio Access', 'Peer MAC',
               'Preferred Channel List', 'UNMP'],
    '7.2.20': ['Radio Unit', 'LLC Configuration', 'Synchronization', 'ACL', 'Radio Access', 'Peer MAC',
               'Preferred Channel List', 'UNMP'],
    '7.2.25': ['Radio Unit', 'LLC Configuration', 'Synchronization', 'ACL', 'Radio Access', 'Peer MAC',
               'Preferred Channel List', 'UNMP', 'Packet Filter IP', 'Packet Filter MAC', 'Packet Filter Mode'],
    '7.2.29': ['Radio Unit', 'LLC Configuration', 'Synchronization', 'ACL', 'Radio Access', 'Peer MAC',
               'Preferred Channel List', 'UNMP', 'Packet Filter IP', 'Packet Filter MAC', 'Packet Filter Mode'],
    'idu': ['E1 port Configuration', 'Link Configuration', 'Temperature', 'Date & Time', 'UNMP',
            'Switch Port Configuration', 'Switch port Bandwidth control', 'Switch port QinQ ',
            'Mirroring port ', 'Switch port VLAN'],
    'ccu': ['Site info', 'Battery Solar Configuration', 'AUX IO', 'Alarm Threshold', 'Peer Info', 'CCU Control',
            'Status Data'],
    'ap25': ['Radio Configuration', 'VAP Configuration', 'ACL Configuration', 'Services', 'DHCP'],
}

report_dict = {
    'odu16':
        {
            'master': {
                'Radio Unit': ['set_odu16_ru_conf_table.channel_bandwidth', 'set_odu16_ru_conf_table.sysnch_source',
                               'set_odu16_ru_conf_table.country_code'],
                'LLC Configuration': ['set_odu16_ra_llc_conf_table.llc_arq_enable',
                                      'set_odu16_ra_llc_conf_table.arq_win',
                                      'set_odu16_ra_llc_conf_table.frame_loss_threshold',
                                      'set_odu16_ra_llc_conf_table.leaky_bucket_timer_val',
                                      'set_odu16_ra_llc_conf_table.frame_loss_timeout', ],
                'Synchronization': ['set_odu16_sync_config_table.raster_time', 'set_odu16_sync_config_table.num_slaves',
                                    'set_odu16_sync_config_table.sync_loss_threshold',
                                    'set_odu16_sync_config_table.leaky_bucket_timer',
                                    'set_odu16_sync_config_table.sync_lost_timeout',
                                    'set_odu16_sync_config_table.sync_config_time_adjust'],
                'ACL': ['set_odu16_ra_conf_table.acl_mode', 'set_odu16_ra_acl_config_table.index',
                        'set_odu16_ra_acl_config_table.mac_address', ],
                'Radio Frequency': ['set_odu16_ra_tdd_mac_config.rf_channel_frequency',
                                    'set_odu16_ra_tdd_mac_config.rfcoding',
                                    'set_odu16_ra_tdd_mac_config.tx_power', 'set_odu16_ra_tdd_mac_config.pass_phrase',
                                    'set_odu16_ra_tdd_mac_config.max_crc_errors',
                                    'set_odu16_ra_tdd_mac_config.leaky_bucket_timer_value', ],
                'Peer MAC': ['set_odu16_sync_config_table.num_slaves', 'set_odu16_peer_config_table.index',
                             'set_odu16_peer_config_table.peer_mac_address', ],
                'UNMP': ['set_odu16_omc_conf_table.omc_ip_address', ],
            }
        },
    #--------------------------------------------
    # @TODO: Firmware model based sheet pickup
    #   Not possible till we don't have form
    #   information stored for perticulart model.
    #--------------------------------------------
    'odu100':
        {
            'master': {
                'Radio Unit': ['odu100_ruConfTable.channelBandwidth', 'odu100_ruConfTable.countryCode',
                               'odu100_ruConfTable.poeState', 'odu100_ruConfTable.alignmentControl'],
                'LLC Configuration': ['odu100_raLlcConfTable.arqWinHigh', 'odu100_raLlcConfTable.arqWinLow',
                                      'odu100_raLlcConfTable.frameLossThreshold',
                                      'odu100_raLlcConfTable.leakyBucketTimerVal',
                                      'odu100_raLlcConfTable.frameLossTimeout'],
                'Synchronization': ['odu100_syncConfigTable.rasterTime', 'odu100_syncConfigTable.syncLossThreshold',
                                    'odu100_syncConfigTable.leakyBucketTimer', 'odu100_syncConfigTable.syncLostTimeout',
                                    'odu100_syncConfigTable.syncConfigTimerAdjust',
                                    'odu100_syncConfigTable.percentageDownlinkTransmitTime', ],
                'ACL': ['odu100_raAclConfigTable.aclIndex', 'odu100_raAclConfigTable.macaddress',
                        'odu100_raConfTable.aclMode'],
                'Radio Access': ['odu100_raConfTable.numSlaves', 'odu100_raConfTable.ssID',
                                 'odu100_raTddMacConfigTable.encryptionType',
                                 'odu100_raTddMacConfigTable.passPhrase', 'odu100_raTddMacConfigTable.txPower',
                                 'odu100_raTddMacConfigTable.maxCrcErrors', 'odu100_syncConfigTable.leakyBucketTimer',
                                 'odu100_raConfTable.acm', 'odu100_raConfTable.dba',
                                 'odu100_raConfTable.guaranteedBroadcastBW',
                                 'odu100_raConfTable.acs', 'odu100_raConfTable.dfs', 'odu100_raConfTable.antennaPort',
                                 'odu100_raConfTable.linkDistance', ],
                'Peer MAC': ['odu100_peerConfigTable.peermacAddress', 'odu100_peerConfigTable.guaranteedUplinkBW',
                             'odu100_peerConfigTable.guaranteedDownlinkBW', 'odu100_peerConfigTable.maxDownlinkBW',
                             'odu100_peerConfigTable.maxUplinkBW', 'odu100_peerConfigTable.basicrateMCSIndex', ],
                'Preferred Channel List': ['odu100_raPreferredRFChannelTable.rafrequency'],
                'UNMP': ['odu100_omcConfTable.omcIpAddress'],
                'Packet Filter IP': ['odu100_ipFilterTable.ipFilterIndex', 'odu100_ipFilterTable.ipFilterIpAddress',
                                     'odu100_ipFilterTable.ipFilterNetworkMask'],
                'Packet Filter MAC': ['odu100_macFilterTable.macFilterIndex', 'odu100_macFilterTable.filterMacAddress'],
                'Packet Filter Mode': ['odu100_ruConfTable.ethFiltering'],
            },
            'slave': {
                'Radio Unit': ['odu100_ruConfTable.channelBandwidth', 'odu100_ruConfTable.countryCode',
                               'odu100_ruConfTable.poeState', 'odu100_ruConfTable.alignmentControl'],
                'LLC Configuration': ['odu100_raLlcConfTable.arqWinHigh', 'odu100_raLlcConfTable.arqWinLow',
                                      'odu100_raLlcConfTable.frameLossThreshold',
                                      'odu100_raLlcConfTable.leakyBucketTimerVal',
                                      'odu100_raLlcConfTable.frameLossTimeout'],
                'Synchronization': ['odu100_syncConfigTable.syncLossThreshold',
                                    'odu100_syncConfigTable.leakyBucketTimer',
                                    'odu100_syncConfigTable.syncLostTimeout', ],
                'ACL': ['odu100_raAclConfigTable.aclIndex', 'odu100_raAclConfigTable.macaddress',
                        'odu100_raConfTable.aclMode'],
                'Radio Access': ['odu100_raTddMacConfigTable.encryptionType',
                                 'odu100_raTddMacConfigTable.passPhrase', 'odu100_raTddMacConfigTable.txPower',
                                 'odu100_raTddMacConfigTable.maxCrcErrors', 'odu100_syncConfigTable.leakyBucketTimer',
                                 'odu100_raConfTable.antennaPort', ],
                'Peer MAC': ['odu100_peerConfigTable.peermacAddress', 'odu100_peerConfigTable.guaranteedUplinkBW',
                             'odu100_peerConfigTable.guaranteedDownlinkBW', 'odu100_peerConfigTable.maxDownlinkBW',
                             'odu100_peerConfigTable.maxUplinkBW', 'odu100_peerConfigTable.basicrateMCSIndex', ],
                'Preferred Channel List': ['odu100_raPreferredRFChannelTable.rafrequency'],
                'UNMP': ['odu100_omcConfTable.omcIpAddress'],
                'Packet Filter IP': ['odu100_ipFilterTable.ipFilterIndex', 'odu100_ipFilterTable.ipFilterIpAddress',
                                     'odu100_ipFilterTable.ipFilterNetworkMask'],
                'Packet Filter MAC': ['odu100_macFilterTable.macFilterIndex', 'odu100_macFilterTable.filterMacAddress'],
                'Packet Filter Mode': ['odu100_ruConfTable.ethFiltering'],
            }

        },
    'idu':
        {
            'master': {
                'E1 port Configuration': ['idu_e1PortConfigurationTable.portNumber',
                                          'idu_e1PortConfigurationTable.clockSource',
                                          'idu_e1PortConfigurationTable.lineType',
                                          'idu_e1PortConfigurationTable.adminState', ],
                'Link Configuration': ['idu_linkConfigurationTable.dstIPAddr', 'idu_linkConfigurationTable.srcBundleID',
                                       'idu_linkConfigurationTable.dstBundleID',
                                       'idu_linkConfigurationTable.portNumber',
                                       'idu_linkConfigurationTable.adminStatus',
                                       'idu_linkConfigurationTable.bundleNumber',
                                       'idu_linkConfigurationTable.bundleSize', 'idu_linkConfigurationTable.bufferSize',
                                       'idu_linkConfigurationTable.clockRecovery',
                                       'idu_linkConfigurationTable.rowStatus',
                                       'idu_linkConfigurationTable.tsaAssign'],
                'Temperature': ['idu_temperatureSensorConfigurationTable.tempMax',
                                'idu_temperatureSensorConfigurationTable.tempMin', ],
                'Date & Time': ['idu_rtcConfigurationTable.year', 'idu_rtcConfigurationTable.month',
                                'idu_rtcConfigurationTable.day', 'idu_rtcConfigurationTable.hour',
                                'idu_rtcConfigurationTable.min', 'idu_rtcConfigurationTable.sec', ],
                'UNMP': ['idu_omcConfigurationTable.omcIpAddress', ],
                'Switch Port Configuration': ['idu_switchPortconfigTable.switchportNum',
                                              'idu_switchPortconfigTable.swlinkMode',
                                              'idu_switchPortconfigTable.portvid',
                                              'idu_switchPortconfigTable.macauthState',
                                              'idu_switchPortconfigTable.mirroringdirection',
                                              'idu_switchPortconfigTable.portdotqmode',
                                              'idu_switchPortconfigTable.macflowcontrol'],
                'Switch port Bandwidth control': ['idu_switchPortconfigTable.swadminState',
                                                  'idu_portBwTable.switchportnum',
                                                  'idu_portBwTable.ingressbwvalue', 'idu_portBwTable.egressbwvalue', ],
                'Switch port QinQ ': ['idu_portqinqTable.switchportnumber', 'idu_portqinqTable.portqinqstate',
                                      'idu_portqinqTable.providertag', ],
                'Mirroring port ': ['idu_mirroringportTable.mirroringport', ],
                'Switch port VLAN': ['idu_vlanconfigTable.vlanid', 'idu_vlanconfigTable.vlanname',
                                     'idu_vlanconfigTable.memberports', 'idu_vlanconfigTable.vlantag'],
            }
        },

    'ccu':
        {
            'master': {
                'Site info': ['ccu_ccuSiteInformationTable.ccuSITSiteName'],
                'Battery Solar Configuration': ['ccu_ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity',
                                                'ccu_ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP',
                                                'ccu_ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount',
                                                'ccu_ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate'],
                'AUX IO': [
                    'ccu_ccuAuxIOTable.ccuAIExternalOutput1', 'ccu_ccuAuxIOTable.ccuAIExternalOutput2',
                    'ccu_ccuAuxIOTable.ccuAIExternalOutput3', 'ccu_ccuAuxIOTable.ccuAIExternalInput1AlarmType',
                    'ccu_ccuAuxIOTable.ccuAIExternalInput2AlarmType', 'ccu_ccuAuxIOTable.ccuAIExternalInput3AlarmType'],
                'Alarm Threshold': [
                    'ccu_ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm',
                    'ccu_ccuAlarmAndThresholdTable.ccuATPSMRequest',
                    'ccu_ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit',
                    'ccu_ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent',
                    'ccu_ccuAlarmAndThresholdTable.ccuATLowVoltageDisconnectLevel'],
                'Peer Info': [
                    'ccu_ccuPeerInformationTable.ccuPIPeer1MACID', 'ccu_ccuPeerInformationTable.ccuPIPeer2MACID',
                    'ccu_ccuPeerInformationTable.ccuPIPeer3MACID', 'ccu_ccuPeerInformationTable.ccuPIPeer4MACID'],
                'CCU Control': [
                    'ccu_ccuControlTable.ccuCTLoadTurnOff', 'ccu_ccuControlTable.ccuCTSMPSCharging'],
                'Status Data': [
                    'ccu_ccuStatusDataTable.ccuSDLastRebootReason',
                    'ccu_ccuStatusDataTable.ccuSDUpTimeSecs', 'ccu_ccuStatusDataTable.ccuSDKwHReading',
                    'ccu_ccuStatusDataTable.ccuSDBatteryHealth', 'ccu_ccuStatusDataTable.ccuSDBatteryState',
                    'ccu_ccuStatusDataTable.ccuSDLoadConnectedStatus', 'ccu_ccuStatusDataTable.ccuSDACAvailability',
                    'ccu_ccuStatusDataTable.ccuSDExternalChargingStatus',
                    'ccu_ccuStatusDataTable.ccuSDChargeDischargeCycle'],
            }
        },
    'ap25': {
        'master':
            {'Radio Configuration': [
                'ap25_radioSetup.radioState', 'ap25_radioSetup.radioAPmode',
                'ap25_radioSetup.radioCountryCode', 'ap25_radioSetup.numberofVAPs',
                'ap25_radioSetup.radioChannel', 'ap25_radioSetup.wifiMode',
                'ap25_radioSetup.radioChannelWidth', 'ap25_radioSetup.radioTXChainMask',
                'ap25_radioSetup.radioRXChainMask', 'ap25_radioSetup.radioTxPower',
                'ap25_radioSetup.radioGatingIndex', 'ap25_radioSetup.radioAggregation',
                'ap25_radioSetup.radioAggFrames', 'ap25_radioSetup.radioAggSize',
                'ap25_radioSetup.radioAggMinSize'],

             'VAP Configuration': [
                 'ap25_basicVAPconfigTable.vapselection_id',
                 'ap25_basicVAPconfigTable.vapBeaconInterval',
                 'ap25_basicVAPconfigTable.vapESSID',
                 'ap25_basicVAPconfigTable.vapFragmentationThresholdValue',
                 'ap25_basicVAPconfigTable.vapHiddenESSIDstate',
                 'ap25_basicVAPconfigTable.vapMode',
                 'ap25_basicVAPconfigTable.vapRTSthresholdValue',
                 'ap25_basicVAPconfigTable.vapRadioMac',
                 'ap25_basicVAPconfigTable.vapSecurityMode',
                 'ap25_basicVAPconfigTable.vlanid',
                 'ap25_basicVAPconfigTable.vlanpriority',
                 'ap25_radioSetup.radioManagementVLANstate',
             ],
             'ACL Configuration': [
                 'ap25_aclMacTable.aclMACsIndex', 'ap25_aclMacTable.macaddress', 'ap25_basicACLconfigTable.aclMode', ],
             'Services': ['ap25_services.upnpServerStatus', 'ap25_services.systemLogStatus',
                          'ap25_services.systemLogIP', 'ap25_services.systemLogPort'],
             'DHCP': [
                 'ap25_dhcpServer.dhcpServerStatus', 'ap25_dhcpServer.dhcpStartIPaddress',
                 'ap25_dhcpServer.dhcpEndIPaddress', 'ap25_dhcpServer.dhcpSubnetMask',
                 'ap25_dhcpServer.dhcpClientLeaseTime', ]
            }

    }
}

table_dict = {
    'odu100': {'oids': 'oids',
               'oids_multivalues': 'oids_multivalues',
    },
    '7.2.20': {'oids': 'odu100_7_2_20_oids',
               'oids_multivalues': 'odu100_7_2_20_oids_multivalues',
    },
    '7.2.25': {'oids': 'odu100_7_2_25_oids',
               'oids_multivalues': 'odu100_7_2_25_oids_multivalues',
    },
    '7.2.29': {'oids': 'odu100_7_2_29_oids',
               'oids_multivalues': 'odu100_7_2_29_oids_multivalues',
    },
    'ap25': {'oids': 'ap25_oids',
             'oids_multivalues': 'ap25_oids_multivalues',
    },
    'idu': {'oids': 'idu_oids',
            'oids_multivalues': 'idu_oids_multivalues',
    },
    'ccu': {'oids': 'ccu_oids',
            'oids_multivalues': 'ccu_oids_multivalues',
    },
    'odu16': {'oids': '',
              'oids_multivalues': '',
    }
}

complete_dict = {
    'odu16':
        {
            'set_odu16_ru_conf_table.channel_bandwidth': [],
            'set_odu16_ru_conf_table.sysnch_source': [],
            'set_odu16_ru_conf_table.country_code': [],

            'set_odu16_ra_llc_conf_table.llc_arq_enable': [],
            'set_odu16_ra_llc_conf_table.arq_win': [],
            'set_odu16_ra_llc_conf_table.frame_loss_threshold': [],
            'set_odu16_ra_llc_conf_table.leaky_bucket_timer_val': [],
            'set_odu16_ra_llc_conf_table.frame_loss_timeout': [],

            'set_odu16_sync_config_table.raster_time': [],
            'set_odu16_sync_config_table.num_slaves': [],
            'set_odu16_sync_config_table.sync_loss_threshold': [],
            'set_odu16_sync_config_table.leaky_bucket_timer': [],
            'set_odu16_sync_config_table.sync_lost_timeout': [],
            'set_odu16_sync_config_table.sync_config_time_adjust': [],

            'set_odu16_ra_conf_table.acl_mode': [],
            'set_odu16_ra_acl_config_table.index': [],
            'set_odu16_ra_acl_config_table.mac_address': [],

            'set_odu16_ra_tdd_mac_config.rf_channel_frequency': [],
            'set_odu16_ra_tdd_mac_config.rfcoding': [],
            'set_odu16_ra_tdd_mac_config.tx_power': [],
            'set_odu16_ra_tdd_mac_config.pass_phrase': [],
            'set_odu16_ra_tdd_mac_config.max_crc_errors': [],
            'set_odu16_ra_tdd_mac_config.leaky_bucket_timer_value': [],

            'set_odu16_sync_config_table.num_slaves': [],
            'set_odu16_peer_config_table.index': [],
            'set_odu16_peer_config_table.peer_mac_address': [],

            'set_odu16_omc_conf_table.omc_ip_address': [],
        },
    'odu100':
        {
            'odu100_ruConfTable.alignmentControl': [],
            'odu100_ruConfTable.channelBandwidth': [],
            'odu100_ruConfTable.countryCode': [],
            'odu100_ruConfTable.poeState': [],
            'odu100_ruConfTable.ethFiltering': [],

            'odu100_ipFilterTable.ipFilterIndex': [],
            'odu100_ipFilterTable.ipFilterIpAddress': [],
            'odu100_ipFilterTable.ipFilterNetworkMask': [],

            'odu100_macFilterTable.macFilterIndex': [],
            'odu100_macFilterTable.filterMacAddress': [],

            'odu100_raLlcConfTable.arqWinHigh': [],
            'odu100_raLlcConfTable.arqWinLow': [],
            'odu100_raLlcConfTable.frameLossThreshold': [],
            'odu100_raLlcConfTable.frameLossTimeout': [],
            'odu100_raLlcConfTable.leakyBucketTimerVal': [],

            'odu100_syncConfigTable.leakyBucketTimer': [],
            'odu100_syncConfigTable.percentageDownlinkTransmitTime': [],
            'odu100_syncConfigTable.rasterTime': [],
            'odu100_syncConfigTable.syncConfigTimerAdjust': [],
            'odu100_syncConfigTable.syncLossThreshold': [],
            'odu100_syncConfigTable.syncLostTimeout': [],

            'odu100_raAclConfigTable.aclIndex': [],
            'odu100_raAclConfigTable.macaddress': [],

            'odu100_raConfTable.aclMode': [],
            'odu100_raConfTable.acm': [],
            'odu100_raConfTable.acs': [],
            'odu100_raConfTable.antennaPort': [],
            'odu100_raConfTable.dba': [],
            'odu100_raConfTable.dfs': [],
            'odu100_raConfTable.guaranteedBroadcastBW': [],
            'odu100_raConfTable.linkDistance': [],
            'odu100_raConfTable.numSlaves': [],
            'odu100_raConfTable.ssID': [],

            'odu100_raTddMacConfigTable.encryptionType': [],
            'odu100_raTddMacConfigTable.leakyBucketTimerValue': [],
            'odu100_raTddMacConfigTable.maxCrcErrors': [],
            'odu100_raTddMacConfigTable.maxPower': [],
            'odu100_raTddMacConfigTable.passPhrase': [],
            'odu100_raTddMacConfigTable.txPower': [],

            'odu100_peerConfigTable.basicrateMCSIndex': [],
            'odu100_peerConfigTable.guaranteedDownlinkBW': [],
            'odu100_peerConfigTable.guaranteedUplinkBW': [],
            'odu100_peerConfigTable.maxDownlinkBW': [],
            'odu100_peerConfigTable.maxUplinkBW': [],
            'odu100_peerConfigTable.peermacAddress': [],

            'odu100_raPreferredRFChannelTable.rafrequency': [],

            'odu100_omcConfTable.omcIpAddress': [],

        },
    'ap25':
        {

            'ap25_radioSetup.radioState': [],
            'ap25_radioSetup.radioAPmode': [],
            'ap25_radioSetup.radioCountryCode': [],
            'ap25_radioSetup.numberofVAPs': [],
            'ap25_radioSetup.radioChannel': [],
            'ap25_radioSetup.wifiMode': [],
            'ap25_radioSetup.radioChannelWidth': [],
            'ap25_radioSetup.radioTXChainMask': [],
            'ap25_radioSetup.radioRXChainMask': [],
            'ap25_radioSetup.radioTxPower': [],
            'ap25_radioSetup.radioGatingIndex': [],
            'ap25_radioSetup.radioAggregation': [],
            'ap25_radioSetup.radioAggFrames': [],
            'ap25_radioSetup.radioAggSize': [],
            'ap25_radioSetup.radioAggMinSize': [],

            'ap25_basicVAPconfigTable.vapBeaconInterval': [],
            'ap25_basicVAPconfigTable.vapESSID': [],
            'ap25_basicVAPconfigTable.vapFragmentationThresholdValue': [],
            'ap25_basicVAPconfigTable.vapHiddenESSIDstate': [],
            'ap25_basicVAPconfigTable.vapMode': [],
            'ap25_basicVAPconfigTable.vapRTSthresholdValue': [],
            'ap25_basicVAPconfigTable.vapRadioMac': [],
            'ap25_basicVAPconfigTable.vapSecurityMode': [],
            'ap25_basicVAPconfigTable.vapselection_id': [],
            'ap25_basicVAPconfigTable.vlanid': [],
            'ap25_basicVAPconfigTable.vlanpriority': [],

            'ap25_radioSetup.radioManagementVLANstate': [],

            'ap25_aclMacTable.aclMACsIndex': [],
            'ap25_aclMacTable.macaddress': [],
            'ap25_basicACLconfigTable.aclMode': [],


            'ap25_services.upnpServerStatus': [],
            'ap25_services.systemLogStatus': [],
            'ap25_services.systemLogIP': [],
            'ap25_services.systemLogPort': [],

            'ap25_dhcpServer.dhcpServerStatus': [],
            'ap25_dhcpServer.dhcpStartIPaddress': [],
            'ap25_dhcpServer.dhcpEndIPaddress': [],
            'ap25_dhcpServer.dhcpSubnetMask': [],
            'ap25_dhcpServer.dhcpClientLeaseTime': [],

        },

    'idu':
        {
            'idu_e1PortConfigurationTable.portNumber': [],
            'idu_e1PortConfigurationTable.clockSource': [],
            'idu_e1PortConfigurationTable.lineType': [],
            'idu_e1PortConfigurationTable.adminState': [],

            'idu_linkConfigurationTable.dstIPAddr': [],
            'idu_linkConfigurationTable.srcBundleID': [],
            'idu_linkConfigurationTable.dstBundleID': [],
            'idu_linkConfigurationTable.portNumber': [],
            'idu_linkConfigurationTable.adminStatus': [],
            'idu_linkConfigurationTable.bundleNumber': [],
            'idu_linkConfigurationTable.bundleSize': [],
            'idu_linkConfigurationTable.bufferSize': [],
            'idu_linkConfigurationTable.clockRecovery': [],
            'idu_linkConfigurationTable.rowStatus': [],

            'idu_linkConfigurationTable.tsaAssign': [],
            'idu_temperatureSensorConfigurationTable.tempMax': [],
            'idu_temperatureSensorConfigurationTable.tempMin': [],
            'idu_rtcConfigurationTable.year': [],
            'idu_rtcConfigurationTable.month': [],
            'idu_rtcConfigurationTable.day': [],
            'idu_rtcConfigurationTable.hour': [],
            'idu_rtcConfigurationTable.min': [],
            'idu_rtcConfigurationTable.sec': [],

            'idu_omcConfigurationTable.omcIpAddress': [],

            'idu_switchPortconfigTable.switchportNum': [],
            'idu_switchPortconfigTable.swlinkMode': [],
            'idu_switchPortconfigTable.portvid': [],
            'idu_switchPortconfigTable.macauthState': [],
            'idu_switchPortconfigTable.mirroringdirection': [],
            'idu_switchPortconfigTable.portdotqmode': [],
            'idu_switchPortconfigTable.macflowcontrol': [],
            'idu_switchPortconfigTable.swadminState': [],

            'idu_portBwTable.switchportnum': [],
            'idu_portBwTable.ingressbwvalue': [],
            'idu_portBwTable.egressbwvalue': [],

            'idu_portqinqTable.switchportnumber': [],
            'idu_portqinqTable.portqinqstate': [],
            'idu_portqinqTable.providertag': [],

            'idu_mirroringportTable.mirroringport': [],

            'idu_vlanconfigTable.vlanid': [],
            'idu_vlanconfigTable.vlanname': [],
            'idu_vlanconfigTable.memberports': [],
            'idu_vlanconfigTable.vlantag': [],


        },
    'ccu': {
        'ccu_ccuSiteInformationTable.ccuSITSiteName': [],

        'ccu_ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity': [],
        'ccu_ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP': [],
        'ccu_ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount': [],
        'ccu_ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate': [],

        'ccu_ccuAuxIOTable.ccuAIExternalOutput1': [],
        'ccu_ccuAuxIOTable.ccuAIExternalOutput2': [],
        'ccu_ccuAuxIOTable.ccuAIExternalOutput3': [],
        'ccu_ccuAuxIOTable.ccuAIExternalInput1AlarmType': [],
        'ccu_ccuAuxIOTable.ccuAIExternalInput2AlarmType': [],
        'ccu_ccuAuxIOTable.ccuAIExternalInput3AlarmType': [],

        'ccu_ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm': [],
        'ccu_ccuAlarmAndThresholdTable.ccuATPSMRequest': [],
        'ccu_ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit': [],
        'ccu_ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent': [],
        'ccu_ccuAlarmAndThresholdTable.ccuATLowVoltageDisconnectLevel': [],

        'ccu_ccuPeerInformationTable.ccuPIPeer1MACID': [],
        'ccu_ccuPeerInformationTable.ccuPIPeer2MACID': [],
        'ccu_ccuPeerInformationTable.ccuPIPeer3MACID': [],
        'ccu_ccuPeerInformationTable.ccuPIPeer4MACID': [],

        'ccu_ccuControlTable.ccuCTLoadTurnOff': [],
        'ccu_ccuControlTable.ccuCTSMPSCharging': [],

        'ccu_ccuStatusDataTable.ccuSDLastRebootReason': [],
        'ccu_ccuStatusDataTable.ccuSDUpTimeSecs': [],
        'ccu_ccuStatusDataTable.ccuSDKwHReading': [],
        'ccu_ccuStatusDataTable.ccuSDBatteryHealth': [],
        'ccu_ccuStatusDataTable.ccuSDBatteryState': [],
        'ccu_ccuStatusDataTable.ccuSDLoadConnectedStatus': [],
        'ccu_ccuStatusDataTable.ccuSDACAvailability': [],
        'ccu_ccuStatusDataTable.ccuSDExternalChargingStatus': [],
        'ccu_ccuStatusDataTable.ccuSDChargeDischargeCycle': [],


    }

}

column_report_names_dict = {

    'odu16':
        {
            'set_odu16_ru_conf_table.channel_bandwidth': 'Channel Bandwidth',
            'set_odu16_ru_conf_table.sysnch_source': 'Synch Source',
            'set_odu16_ru_conf_table.country_code': 'Country Code',

            'set_odu16_ra_llc_conf_table.llc_arq_enable': 'ARQ Mode',
            'set_odu16_ra_llc_conf_table.arq_win': 'ArqWin(Retransmit Window Size)',
            'set_odu16_ra_llc_conf_table.frame_loss_threshold': 'Frame Loss Threshold',
            'set_odu16_ra_llc_conf_table.leaky_bucket_timer_val': 'Leaky Bucket Timer',
            'set_odu16_ra_llc_conf_table.frame_loss_timeout': 'Frame Loss Time Out',

            'set_odu16_sync_config_table.raster_time': 'Raster Time',
            'set_odu16_sync_config_table.num_slaves': 'Number of Slaves',
            'set_odu16_sync_config_table.sync_loss_threshold': 'Sync Loss Threshold',
            'set_odu16_sync_config_table.leaky_bucket_timer': 'Leaky Bucket Timer',
            'set_odu16_sync_config_table.sync_lost_timeout': 'Sync Lost Timeout',
            'set_odu16_sync_config_table.sync_config_time_adjust': 'Sync Config Timer Adjust',

            'set_odu16_ra_conf_table.acl_mode': 'ACL Mode',
            'set_odu16_ra_acl_config_table.index': 'MAC Address Index',
            'set_odu16_ra_acl_config_table.mac_address': 'MAC Address',

            'set_odu16_ra_tdd_mac_config.rf_channel_frequency': ' TDD MAC RF',
            'set_odu16_ra_tdd_mac_config.rfcoding': ' TDD MAC RF Coding',
            'set_odu16_ra_tdd_mac_config.tx_power': ' TDD MAC TX Power',
            'set_odu16_ra_tdd_mac_config.pass_phrase': 'Pass Phrase',
            'set_odu16_ra_tdd_mac_config.max_crc_errors': 'Max CRC Errors',
            'set_odu16_ra_tdd_mac_config.leaky_bucket_timer_value': 'Leaky Bucket Timer',

            'set_odu16_sync_config_table.num_slaves': 'Number of Slaves',
            'set_odu16_peer_config_table.index': 'Timeslot MAC Address Index',
            'set_odu16_peer_config_table.peer_mac_address': 'Timeslot MAC Address',

            'set_odu16_omc_conf_table.omc_ip_address': 'UNMP IP',

        },
    'odu100':
        {
            'odu100_ruConfTable.alignmentControl': 'Alignment Control',
            'odu100_ruConfTable.channelBandwidth': 'Channel Bandwidth',
            'odu100_ruConfTable.countryCode': 'Country Code',
            'odu100_ruConfTable.poeState': 'POE State',
            'odu100_ruConfTable.ethFiltering': 'Filter Mode',

            'odu100_ipFilterTable.ipFilterIndex': 'Index',
            'odu100_ipFilterTable.ipFilterIpAddress': 'IP Address',
            'odu100_ipFilterTable.ipFilterNetworkMask': 'Network Mask',

            'odu100_macFilterTable.macFilterIndex': 'Index',
            'odu100_macFilterTable.filterMacAddress': 'MAC Address',

            'odu100_raLlcConfTable.arqWinHigh': 'Retransmit Window Size(High)',
            'odu100_raLlcConfTable.arqWinLow': 'Retransmit Window Size(Low)',
            'odu100_raLlcConfTable.frameLossThreshold': 'Frame Loss Threshold ',
            'odu100_raLlcConfTable.frameLossTimeout': 'Frame Loss Timeout',
            'odu100_raLlcConfTable.leakyBucketTimerVal': 'Leaky Bucket Timer ',

            'odu100_syncConfigTable.leakyBucketTimer': 'leaky Bucket Timer',
            'odu100_syncConfigTable.percentageDownlinkTransmitTime': '% Downlink Transmit Time',
            'odu100_syncConfigTable.rasterTime': 'Raster Time',
            'odu100_syncConfigTable.syncConfigTimerAdjust': 'Sync Config Timer Adjust',
            'odu100_syncConfigTable.syncLossThreshold': 'Sync Loss Threshold',
            'odu100_syncConfigTable.syncLostTimeout': 'Sync Lost Timeout',

            'odu100_raAclConfigTable.aclIndex': 'ACL Index',
            'odu100_raAclConfigTable.macaddress': 'MAC address',

            'odu100_raConfTable.aclMode': 'ACL Mode',
            'odu100_raConfTable.acm': 'ACM',
            'odu100_raConfTable.acs': 'ACS',
            'odu100_raConfTable.antennaPort': 'Antenna Port',
            'odu100_raConfTable.dba': 'DBA',
            'odu100_raConfTable.dfs': 'DFS',
            'odu100_raConfTable.guaranteedBroadcastBW': 'Guaranteed Broadcast Bandwidth',
            'odu100_raConfTable.linkDistance': 'Link Distance',
            'odu100_raConfTable.numSlaves': 'Number of Slaves',
            'odu100_raConfTable.ssID': 'SSID',

            'odu100_raTddMacConfigTable.encryptionType': 'Encryption Type',
            'odu100_raTddMacConfigTable.leakyBucketTimerValue': 'Leaky Bucket Timer Value',
            'odu100_raTddMacConfigTable.maxCrcErrors': 'Max CRC Errors',
            'odu100_raTddMacConfigTable.maxPower': 'Max Power',
            'odu100_raTddMacConfigTable.passPhrase': 'Pass Phrase',
            'odu100_raTddMacConfigTable.txPower': 'TX Power',

            'odu100_peerConfigTable.basicrateMCSIndex': 'Basic Rate MCS Index',
            'odu100_peerConfigTable.guaranteedDownlinkBW': 'Guaranteed Downlink Bandwidth',
            'odu100_peerConfigTable.guaranteedUplinkBW': 'Guaranteed Uplink Bandwidth',
            'odu100_peerConfigTable.maxDownlinkBW': 'Max Downlink Bandwidth',
            'odu100_peerConfigTable.maxUplinkBW': 'Nax Uplink Bandwidth',
            'odu100_peerConfigTable.peermacAddress': 'Peer MAC Address',

            'odu100_raPreferredRFChannelTable.rafrequency': 'RA frequency',
            'odu100_omcConfTable.omcIpAddress': 'UNMP IP Address',

        },

    'ap25':
        {

            'ap25_radioSetup.radioState': 'Radio',
            'ap25_radioSetup.radioAPmode': 'Startup mode',
            'ap25_radioSetup.radioCountryCode': ' Country ',
            'ap25_radioSetup.numberofVAPs': 'Number of VAPs',
            'ap25_radioSetup.radioChannel': ' Channel Frequency  ',
            'ap25_radioSetup.wifiMode': 'WIFI Mode',
            'ap25_radioSetup.radioChannelWidth': ' Channel Width',
            'ap25_radioSetup.radioTXChainMask': ' TX Chain Mask',
            'ap25_radioSetup.radioRXChainMask': ' RX Chain Mask',
            'ap25_radioSetup.radioTxPower': ' TX Power',
            'ap25_radioSetup.radioGatingIndex': ' Guard Interval',
            'ap25_radioSetup.radioAggregation': ' Aggregation',
            'ap25_radioSetup.radioAggFrames': ' Aggregation Frames',
            'ap25_radioSetup.radioAggSize': ' Aggregation Size',
            'ap25_radioSetup.radioAggMinSize': ' Aggregation Min Size',

            'ap25_radioSetup.radioManagementVLANstate': 'Radio Management VLAN state',

            'ap25_basicVAPconfigTable.vapBeaconInterval': 'Beacon Interval',
            'ap25_basicVAPconfigTable.vapESSID': 'ESSID',
            'ap25_basicVAPconfigTable.vapFragmentationThresholdValue': 'Fragmentation Threshold Value',
            'ap25_basicVAPconfigTable.vapHiddenESSIDstate': 'ESSID state',
            'ap25_basicVAPconfigTable.vapMode': 'VAP Mode',
            'ap25_basicVAPconfigTable.vapRTSthresholdValue': 'Threshold Value',
            'ap25_basicVAPconfigTable.vapRadioMac': 'Radio MAC',
            'ap25_basicVAPconfigTable.vapSecurityMode': 'Security Mode',
            'ap25_basicVAPconfigTable.vapselection_id': 'VAP',
            'ap25_basicVAPconfigTable.vlanid': 'VLAN ID',
            'ap25_basicVAPconfigTable.vlanpriority': 'VLAN Priority',

            'ap25_aclMacTable.aclMACsIndex': 'MAC Index',
            'ap25_aclMacTable.macaddress': 'MAC Address',
            'ap25_basicACLconfigTable.aclMode': 'ACL Mode',

            'ap25_services.upnpServerStatus': 'UPNP Server Status',
            'ap25_services.systemLogStatus': 'Log Status',
            'ap25_services.systemLogIP': 'Log IP',
            'ap25_services.systemLogPort': 'Logging Port',

            'ap25_dhcpServer.dhcpServerStatus': 'DHCP Server',
            'ap25_dhcpServer.dhcpStartIPaddress': 'Start IP Address',
            'ap25_dhcpServer.dhcpEndIPaddress': 'End IP Address',
            'ap25_dhcpServer.dhcpSubnetMask': 'Network Mask',
            'ap25_dhcpServer.dhcpClientLeaseTime': 'Lease Time',
        },
    'idu':
        {
            'idu_e1PortConfigurationTable.portNumber': 'Port Number',
            'idu_e1PortConfigurationTable.clockSource': 'Clock Source',
            'idu_e1PortConfigurationTable.lineType': 'Line Type',
            'idu_e1PortConfigurationTable.adminState': 'Admin State',

            'idu_linkConfigurationTable.dstIPAddr': 'Destination IP ',
            'idu_linkConfigurationTable.srcBundleID': 'Source Link ID ',
            'idu_linkConfigurationTable.dstBundleID': 'Destination Link ID ',
            'idu_linkConfigurationTable.portNumber': 'E1 Port Number',

            'idu_linkConfigurationTable.bundleNumber': 'Bundle Number',
            'idu_linkConfigurationTable.bundleSize': 'PayLoad Size ',
            'idu_linkConfigurationTable.bufferSize': 'Jitter Size(usec)',
            'idu_linkConfigurationTable.clockRecovery': 'Clock Recovery',
            'idu_linkConfigurationTable.adminStatus': 'Admin state',
            'idu_linkConfigurationTable.rowStatus': 'Row Status',
            'idu_linkConfigurationTable.tsaAssign': 'TSA Assign',

            'idu_temperatureSensorConfigurationTable.tempMax': 'Lower Threshold',
            'idu_temperatureSensorConfigurationTable.tempMin': 'Upper Threshold',
            'idu_rtcConfigurationTable.year': 'Years',
            'idu_rtcConfigurationTable.month': 'Months',
            'idu_rtcConfigurationTable.day': 'Days',
            'idu_rtcConfigurationTable.hour': 'Hours',
            'idu_rtcConfigurationTable.min': 'Minutes',
            'idu_rtcConfigurationTable.sec': 'Seconds',

            'idu_omcConfigurationTable.omcIpAddress': 'OMC IP Address',

            'idu_switchPortconfigTable.switchportNum': 'Port',
            'idu_switchPortconfigTable.swlinkMode': 'Link mode',
            'idu_switchPortconfigTable.portvid': 'Port VID',
            'idu_switchPortconfigTable.macauthState': 'MAC Auth State',
            'idu_switchPortconfigTable.mirroringdirection': 'Mirroring Direction',
            'idu_switchPortconfigTable.portdotqmode': 'Port DOTQ Mode',
            'idu_switchPortconfigTable.macflowcontrol': 'MAC Flow Control',
            'idu_switchPortconfigTable.swadminState': 'Admin State',

            'idu_portBwTable.switchportnum': 'Port',
            'idu_portBwTable.ingressbwvalue': 'Ingress (kbps)',
            'idu_portBwTable.egressbwvalue': 'Egress (kbps)',

            'idu_portqinqTable.switchportnumber': 'Port',
            'idu_portqinqTable.portqinqstate': 'QINQ State',
            'idu_portqinqTable.providertag': 'Provider Tag',

            'idu_mirroringportTable.mirroringport': 'Mirroring Port',

            'idu_vlanconfigTable.vlanid': 'VLAN ID',
            'idu_vlanconfigTable.vlanname': 'VLAN Name',
            'idu_vlanconfigTable.memberports': 'Member Ports',
            'idu_vlanconfigTable.vlantag': 'VLAN tag',

        },
    'ccu':
        {
            'ccu_ccuSiteInformationTable.ccuSITSiteName': 'Site Name',

            'ccu_ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity': 'Battery Capacity',
            'ccu_ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP': 'Solar Panel Capacity',
            'ccu_ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount': 'Solar Panel Count',
            'ccu_ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate': 'New Battery Installation Date',

            'ccu_ccuAuxIOTable.ccuAIExternalOutput1': 'External Output 1',
            'ccu_ccuAuxIOTable.ccuAIExternalOutput2': 'External Output 2',
            'ccu_ccuAuxIOTable.ccuAIExternalOutput3': 'External Output 3',

            'ccu_ccuAuxIOTable.ccuAIExternalInput1AlarmType': 'External Input 1 Alarm',
            'ccu_ccuAuxIOTable.ccuAIExternalInput2AlarmType': 'External Input 2 Alarm',
            'ccu_ccuAuxIOTable.ccuAIExternalInput3AlarmType': 'External Input 3 Alarm',

            'ccu_ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm': 'High Temperature Alarm',
            'ccu_ccuAlarmAndThresholdTable.ccuATPSMRequest': 'PSM Request',
            'ccu_ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit': 'SMPS Max Current Limit',
            'ccu_ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent': 'Peak Load Current',
            'ccu_ccuAlarmAndThresholdTable.ccuATLowVoltageDisconnectLevel': 'Low Voltage Disconnect Level',

            'ccu_ccuPeerInformationTable.ccuPIPeer1MACID': 'Peer 1 MAC',
            'ccu_ccuPeerInformationTable.ccuPIPeer2MACID': 'Peer 2 MAC',
            'ccu_ccuPeerInformationTable.ccuPIPeer3MACID': 'Peer 3 MAC',
            'ccu_ccuPeerInformationTable.ccuPIPeer4MACID': 'Peer 4 MAC',

            'ccu_ccuControlTable.ccuCTLoadTurnOff': 'Load Turn Off',
            'ccu_ccuControlTable.ccuCTSMPSCharging': 'SMPS Charging',

            'ccu_ccuStatusDataTable.ccuSDLastRebootReason': 'Last Reboot Reason',
            'ccu_ccuStatusDataTable.ccuSDUpTimeSecs': 'CCU Up Time',
            'ccu_ccuStatusDataTable.ccuSDKwHReading': 'AC Meter Reading',

            'ccu_ccuStatusDataTable.ccuSDBatteryHealth': 'Battery Health',
            'ccu_ccuStatusDataTable.ccuSDBatteryState': 'Battery Charging/Discharging State',
            'ccu_ccuStatusDataTable.ccuSDLoadConnectedStatus': 'Load Status',
            'ccu_ccuStatusDataTable.ccuSDACAvailability': 'AC Availability',
            'ccu_ccuStatusDataTable.ccuSDExternalChargingStatus': 'External Charging Status',
            'ccu_ccuStatusDataTable.ccuSDChargeDischargeCycle': 'Battery Charge/Discharge Cycles',

        }


}

query_dict = {
    'odu16': {

        'set_odu16_ru_conf_table':
            {
                'id_type': 'config_profile_id'
            },

        'set_odu16_ra_llc_conf_table':
            {
                'id_type': 'config_profile_id'
            },

        'set_odu16_sync_config_table':
            {
                'id_type': 'config_profile_id'
            },

        'set_odu16_ra_conf_table':
            {
                'id_type': 'config_profile_id'
            },
        'set_odu16_ra_acl_config_table':
            {
                'id_type': 'config_profile_id'
            },

        'set_odu16_ra_tdd_mac_config':
            {
                'id_type': 'config_profile_id'
            },

        'set_odu16_sync_config_table':
            {
                'id_type': 'config_profile_id'
            },
        'set_odu16_omc_conf_table':
            {
                'id_type': 'config_profile_id'
            },
    },
    'odu100':
        {

            'ruConfTable':
                {
                    'id_type': 'config_profile_id'
                },
            'raLlcConfTable':
                {
                    'id_type': 'config_profile_id'
                },
            'syncConfigTable':
                {
                    'id_type': 'config_profile_id'
                },
            'raAclConfigTable':
                {
                    'id_type': 'config_profile_id'
                },
            'raConfTable':
                {
                    'id_type': 'config_profile_id'
                },
            'raTddMacConfigTable':
                {
                    'id_type': 'config_profile_id'
                },
            'peerConfigTable':
                {
                    'id_type': 'config_profile_id'
                },
            'raPreferredRFChannelTable':
                {
                    'id_type': 'config_profile_id'
                },
            'omcConfTable':
                {
                    'id_type': 'config_profile_id'
                }
        },

    'ap25':
        {
            'radioSetup':
                {
                    'id_type': 'config_profile_id'
                },
            'basicVAPconfigTable':
                {
                    'id_type': 'config_profile_id'
                },

            'aclMacTable':
                {
                    'id_type': 'config_profile_id'
                },
            'basicACLconfigTable':
                {
                    'id_type': 'config_profile_id'
                },

            'services':
                {
                    'id_type': 'config_profile_id'
                },

            'dhcpServer':
                {
                    'id_type': 'config_profile_id'
                },
        },

    'idu':
        {
            'e1PortConfigurationTable':
                {
                    'id_type': 'config_profile_id'
                },
            'linkConfigurationTable':
                {
                    'id_type': 'config_profile_id'
                },
            'temperatureSensorConfigurationTable':
                {
                    'id_type': 'config_profile_id'
                },
            'rtcConfigurationTable':
                {
                    'id_type': 'config_profile_id'
                },

            'omcConfigurationTable':
                {
                    'id_type': 'config_profile_id'
                },

            'switchPortconfigTable':
                {
                    'id_type': 'config_profile_id'
                },

            'portBwTable':
                {
                    'id_type': 'config_profile_id'
                },


            'portqinqTable':
                {
                    'id_type': 'config_profile_id'
                },

            'mirroringportTable':
                {
                    'id_type': 'config_profile_id'
                },

            'vlanconfigTable':
                {
                    'id_type': 'config_profile_id'
                },

        },
    'ccu':
        {
            'ccuSiteInformationTable':
                {
                    'id_type': 'config_profile_id'
                },

            'ccuBatteryPanelConfigTable':
                {
                    'id_type': 'config_profile_id'
                },

            'ccuAuxIOTable':
                {
                    'id_type': 'config_profile_id'
                },


            'ccuAlarmAndThresholdTable':
                {
                    'id_type': 'config_profile_id'
                },


            'ccuPeerInformationTable':
                {
                    'id_type': 'config_profile_id'
                },

            'ccuControlTable':
                {
                    'id_type': 'config_profile_id'
                },

            'ccuStatusDataTable':
                {
                    'id_type': 'host_id'
                },
        }

}


def get_configuration_details(ip_address_list=[]):
    """

    @param ip_address_list:
    @return:
    """
    global device_status
    device_status = 'master'
    device = ''
    unique_id = ''
    device_type_id, config_profile_id = '', ''
    firmware_mapping_id, host_id = '', ''
    host_alias = ''
    device_type_name = ''

    # db=MySQLdb.connect("localhost","root","root","nms")
    host_info_list = []
    nms_instance = __file__.split(
        "/")[3]       # it gives instance name of nagios system
    global_device_dict = {}
    # get_configuration_details(ip_address_list)#['172.22.0.121'])#,'172.22.0.121'])
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()

        for unique_id in ip_address_list:
        # query="select device_type_id, config_profile_id,
        # host_id,host_alias,ip_address from hosts where ip_address = '%s' and
        # is_deleted=0 "%(ip_address)
            query = " select hosts.device_type_id, config_profile_id, firmware_mapping_id, host_id, host_alias, ip_address, \
			  d.device_name from hosts join device_type as d on d.device_type_id = hosts.device_type_id \
	where hosts.host_id = '%s' and hosts.is_deleted=0 " % (unique_id)
            cursor.execute(query)
            res = cursor.fetchall()
            if len(res) and len(res[0]):
                device_type_id = res[0][0]
                config_profile_id = res[0][1]
                firmware_mapping_id = res[0][2]
                host_id = res[0][3]
                host_alias = res[0][4]
                ip_address = res[0][5]
                host_info_list.append([host_alias, ip_address])
                device_type_name = res[0][6]
            device = device_type_id
            table_device = device_type_id

            #------------ for master slave device status --------------------
            from specific_dashboard_bll import get_master_slave_value   # import the function for master slave identification

            master_slava_statue = get_master_slave_value(res[0][5])
            device_status = 'slave' if master_slava_statue[
                                           'success'] == 0 and master_slava_statue['status'] > 0 else 'master'
            # -------------- ################### ----------------------------

            if device_type_id == 'odu100':
                table_device = object_model_di['odu100'].get(firmware_mapping_id)
            if device_type_id == 'idu4':
                device = 'idu'
                table_device = 'idu'

            di = {}

            device_dict = query_dict[device]
            for table_name in device_dict.keys():
                if device_type_id == 'odu16':
                    table_sql = table_name
                else:
                    table_sql = device + "_" + table_name
                di_table = device_dict[table_name]
                columns = []
                for i in complete_dict[device].keys():
                    temp_li = i.split('.')
                    if temp_li[0] == table_sql:
                        columns.append(temp_li[-1])

                di_table['columns'] = columns
                query = "select `%s` from %s where %s = '%s' " % (
                    '`,`'.join(columns), table_sql, di_table['id_type'], config_profile_id)
                cursor.execute(query)
                res = cursor.fetchall()
                for row in res:
                    if table_sql == "odu100_raPreferredRFChannelTable":
                        i = 0
                        temp_var = table_sql + '.' + di_table['columns'][0]
                        for val in range(len(row)):
                            if temp_var == table_sql + '.' + di_table['columns'][val]:
                                i += 1
                            temp_data_var = "Not Exists" if i > 1 or row[
                                val] == 0 else str(row[val])
                            complete_dict[device][table_sql + '.' +
                                                  di_table['columns'][val]].append(temp_data_var)
                    else:
                        for val in range(len(row)):
                            complete_dict[device][table_sql + '.' +
                                                  di_table['columns'][val]].append(str(row[val]))
                            # print table_sql+'.'+di_table['columns'][val]
                            # print
                            # complete_dict[device][table_sql+'.'+di_table['columns'][val]]
                if device_type_id != 'odu16':
                    query2 = "SELECT oids.coloumn_name, om.name, om.value \
                        FROM %s AS om \
        		        JOIN %s AS oids ON \
                            oids.oid_id = om.oid_id AND \
                            oids.table_name = '%s' AND \
                            oids.coloumn_name IN ('%s') " % (
                        table_dict[table_device]['oids_multivalues'],
                        table_dict[table_device]['oids'],
                        table_name, "' , '".join(di_table['columns']))

                    cursor.execute(query2)
                    res2 = cursor.fetchall()
                    for row in res2:
                        li_temp = complete_dict[
                            device].get(table_sql + '.' + row[0], [])
                        if str(row[1]) in li_temp:
                            index_temp = li_temp.index(str(row[1]))
                            li_temp[index_temp] = str(row[2])
                            complete_dict[
                                device][table_sql + '.' + row[0]] = li_temp

            d = report_dict[device][device_status]
            data = complete_dict[device]
            data_name = column_report_names_dict[device]

            for param in order_report_dict[table_device]:
                di = {}
                di['sheet_name'] = param
                di['main_title'] = param
                di['second_title'] = device_type_name  # host_alias_ip_address
                di['headings'] = [column_report_names_dict[device][j]
                                  for j in report_dict[device][device_status][param]]
                name_report = device_type_name + "_config.xls"
                path_report = '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance
                data_report = [complete_dict[device][j]
                               for j in report_dict[device][device_status][param]]
                m = max(map(len, [j for j in data_report]))

                for j in range(len(data_report)):
                    data_report[j].extend(
                        [' ' for j in range(0, m - len(data_report[j]))])
                data_report = zip(*data_report)
                di['data_report'] = data_report
                global_device_dict[str(unique_id) + param] = di

            for j in complete_dict.keys():
                for k in complete_dict[j].keys():
                    complete_dict[j][k] = []

        # print complete_dict['odu16']['set_odu16_ra_conf_table.acl_mode']
        # print complete_dict['odu16']['set_odu16_ra_acl_config_table.index']
        # print
        # complete_dict['odu16']['set_odu16_ra_acl_config_table.mac_address']
        status = get_excel_sheet(
            device, table_device, str(
                host_alias + "(" + ip_address + ")"), report_dict, column_report_names_dict,
            complete_dict, order_report_dict, global_device_dict, ip_address_list, device_type_name, host_info_list)
        #		status=get_csv_file(device,table_device,str(host_alias+"("+ip_address + ")"),report_dict,column_report_names_dict,
        # complete_dict,order_report_dict,global_device_dict,ip_address_list,device_type_name,host_info_list)
        return status
    except Exception, e:
        import traceback
        # print traceback.format_exc()
        return {'success': 1, 'result': str(traceback.format_exc())}


def get_excel_sheet(
        device, table_device, host_alias_ip_address, report_dict, column_report_names_dict,
        complete_dict, order_report_dict, global_device_dict, ip_address_list, device_type_name, host_info_list):
    """

    @param device:
    @param table_device:
    @param host_alias_ip_address:
    @param report_dict:
    @param column_report_names_dict:
    @param complete_dict:
    @param order_report_dict:
    @param global_device_dict:
    @param ip_address_list:
    @param device_type_name:
    @param host_info_list:
    @return:
    """
    try:
        global device_status
        flag = 0
        # print __file__
        i = 4
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        style = xlwt.XFStyle()  # Create Style
        borders = xlwt.Borders()  # Create Borders
        borders.left = xlwt.Borders.THIN  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 23
        borders.right_colour = 23
        borders.top_colour = 23
        borders.bottom_colour = 23
        style.borders = borders  # Add
        pattern = xlwt.Pattern()  # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = 16
        # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 =
        # Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark
        # Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark
        # Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes
        # on...
        style.pattern = pattern  # Add Pattern to Style

        font = xlwt.Font()  # Create Font
        font.bold = True  # Set font to Bold
        #        style = xlwt.XFStyle() # Create Style
        font.colour_index = 0x09
        style.font = font  # Add Bold Font to Style

        alignment = xlwt.Alignment()  # Create Alignment
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
        #        style = xlwt.XFStyle() # Create Style
        style.alignment = alignment  # Add Alignment to Style

        style1 = xlwt.XFStyle()  # Create Style
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style1.alignment = alignment  # Add Alignment to Style
        xls_book = xlwt.Workbook(encoding='ascii')
        for param in order_report_dict[table_device]:
            sheet_name = param
            main_title = param
            if len(ip_address_list) > 1:
                second_title = device_type_name
            else:
                second_title = host_alias_ip_address
            i = 4
            headings = ['Host Alias', 'IP Address'] + [column_report_names_dict[
                                                           device][j] for j in
                                                       report_dict[device][device_status][param]]
            name_report = second_title + "_config.xls"
            path_report = '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance
            data_report = []
            for ip_address in ip_address_list:
                if data_report == []:
                    if str(ip_address) + param in global_device_dict:
                        temp_data_report = global_device_dict[
                            str(ip_address) + param]['data_report']
                    else:
                        temp_data_report = []
                    temp_host_info_list = deepcopy(host_info_list)
                    data_report1 = [temp_host_info_list[ip_address_list.index(
                        ip_address)] for j in range(len(temp_data_report))]
                    for j in range(len(data_report1)):
                        data_report.append(
                            data_report1[j])  # temp_data_report[i])
                    for j in range(len(temp_data_report)):
                        data_report[
                            j] = data_report[j] + list(temp_data_report[j])
                    #                    	data_report[j].extend(temp_data_report[j])
                else:
                    if str(ip_address) + param in global_device_dict:
                        temp_data_report = global_device_dict[
                            str(ip_address) + param]['data_report']
                    else:
                        temp_data_report = []
                    data_report1 = []
                    temp_host_info_list = deepcopy(host_info_list)
                    data_report1 = [temp_host_info_list[ip_address_list.index(
                        ip_address)] for j in range(len(temp_data_report))]
                    l = len(data_report)
                    for j in range(len(data_report1)):
                        data_report.append(
                            data_report1[j])  # temp_data_report[i])
                    for j in range(len(data_report1)):
                        data_report[j +
                                    l] = data_report[j + l] + list(temp_data_report[j])
                    #                    	data_report[j+l].extend(temp_data_report[j])

            if data_report == []:
                pass
                flag = 1
                # continue
            else:
                flag = 1

            sheet_no = 1
            xls_sheet = xls_book.add_sheet(
                str(sheet_name), cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            top_bar_length = 4 if len(headings) < 4 else len(headings) - 1
            xls_sheet.write_merge(0, 0, 0, top_bar_length, main_title, style)
            xls_sheet.write_merge(1, 1, 0, top_bar_length, second_title, style)
            xls_sheet.write_merge(2, 2, 0, top_bar_length, "")
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')

            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for row in data_report:
                for k in range(len(row)):
                    width = 5000
                    xls_sheet.write(i, k, str(row[k]), style1)
                    xls_sheet.col(k).width = width
                i = i + 1
        if flag == 0:
            result_dict = {"success": "1", "result": "data not available"}
            return result_dict
        xls_book.save(path_report + name_report)
        result_dict = {"success": "0", "result": "report successfully generated", "file":
            name_report, "filename": name_report, "path_report": path_report}
        return result_dict
    except Exception, e:
        import traceback

        return {'success': 1, 'result': str(traceback.format_exc())}


def get_csv_file(
        device, table_device, host_alias_ip_address, report_dict, column_report_names_dict,
        complete_dict, order_report_dict, global_device_dict, ip_address_list, device_type_name, host_info_list):
    """

    @param device:
    @param table_device:
    @param host_alias_ip_address:
    @param report_dict:
    @param column_report_names_dict:
    @param complete_dict:
    @param order_report_dict:
    @param global_device_dict:
    @param ip_address_list:
    @param device_type_name:
    @param host_info_list:
    @return:
    """
    try:
        global device_status
        flag = 1
        device_status = 'master'
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        for param in order_report_dict[table_device]:
            sheet_name = param
            main_title = param
            if len(ip_address_list) > 1:
                second_title = device_type_name
            else:
                second_title = host_alias_ip_address
            i = 4
            headings = ['Host Alias', 'IP Address'] + [column_report_names_dict[
                                                           device][j] for j in
                                                       report_dict[device][device_status][param]]
            name_report = second_title + "_config.csv"
            path_report = '/omd/sites/%s/share/check_mk/web/htdocs/download/' % nms_instance
            data_report = []
            for ip_address in ip_address_list:
                if data_report == []:
                    if str(ip_address) + param in global_device_dict:
                        temp_data_report = global_device_dict[
                            str(ip_address) + param]['data_report']
                    else:
                        temp_data_report = []
                    temp_host_info_list = deepcopy(host_info_list)
                    data_report1 = [temp_host_info_list[ip_address_list.index(
                        ip_address)] for j in range(len(temp_data_report))]
                    for j in range(len(data_report1)):
                        data_report.append(
                            data_report1[j])  # temp_data_report[i])
                    for j in range(len(temp_data_report)):
                        data_report[
                            j] = data_report[j] + list(temp_data_report[j])
                else:
                    if str(ip_address) + param in global_device_dict:
                        temp_data_report = global_device_dict[
                            str(ip_address) + param]['data_report']
                    else:
                        temp_data_report = []
                    data_report1 = []
                    temp_host_info_list = deepcopy(host_info_list)
                    data_report1 = [temp_host_info_list[ip_address_list.index(
                        ip_address)] for j in range(len(temp_data_report))]
                    l = len(data_report)
                    for j in range(len(data_report1)):
                        data_report.append(
                            data_report1[j])  # temp_data_report[i])
                    for j in range(len(data_report1)):
                        data_report[j +
                                    l] = data_report[j + l] + list(temp_data_report[j])
                    ofile = open(path_report + name_report, "wb")
            writer = csv.writer(ofile, delimiter=',', quotechar='"')
            blank_row = ["", "", ""]
            i = len(data_report[0])
            if i % 2 == 0:
                j = i / 2
                i = i + 1
            else:
                j = (i - 1) / 2
            main_row = []
            second_row = []
            for m in range(i):
                main_row.append("")
                second_row.append("")
            main_row[j] = main_title
            second_row[j] = second_title
            i = 0
            for row1 in data_report:
                if i == 0:
                    writer.writerow(main_row)
                    writer.writerow(second_row)
                    writer.writerow(blank_row)
                    writer.writerow(headings)
                i += 1
                writer.writerow(row1)
            ofile.close()

        if flag == 0:
            result_dict = {"success": "1", "result": "data not available"}
            return result_dict
            # xls_book.save(path_report+name_report)
        result_dict = {"success": "0", "result": "report successfully generated", "file":
            name_report, "filename": name_report, "path_report": path_report + "/" + name_report}
        return result_dict
    except Exception, e:
        result_dict = {"success": "1", "result": str(e)}
        return result_dict

        #print "report creation call "
        #print get_configuration_details((5,))