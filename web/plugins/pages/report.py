#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@date: 23-Oct-2011
@version: 0.1
@note: This contains miscellaneous's page & function links
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the page functions
import reporting_controller
import ubre_reporting_controller
import main_reporting_controller
import analyzed_reporting_controller
import history_reporting_controller
# map URLs to page rendering functions
pagehandlers.update({

    # Report
    "manage_crc_phy_report": reporting_controller.manage_crc_phy_report,
    "get_crc_phy_data": reporting_controller.get_crc_phy_data,
    "average_data_crc_phy": reporting_controller.average_data_crc_phy,
    "total_data_crc_phy": reporting_controller.total_data_crc_phy,
    "show_group_result": reporting_controller.show_group_result,
    "show_host_result": reporting_controller.show_host_result,
    "show_host_data_of_group": reporting_controller.show_host_data_of_group,
    "manage_rssi_report": reporting_controller.manage_rssi_report,
    "get_rssi_data": reporting_controller.get_rssi_data,
    "average_data_rssi": reporting_controller.average_data_rssi,
    "total_data_rssi": reporting_controller.total_data_rssi,
    "manage_network_usage_report": reporting_controller.manage_network_usage_report,
    "get_network_usage_data": reporting_controller.get_network_usage_data,
    "total_data_network_usage": reporting_controller.total_data_network_usage,
    "manage_network_outage_report": reporting_controller.manage_network_outage_report,
    "get_network_outage_data": reporting_controller.get_network_outage_data,
    "total_data_network_outage": reporting_controller.total_data_network_outage,
    "odu_excel_reporting": reporting_controller.odu_excel_reporting,
    "nw_bandwidth_excel_reporting": reporting_controller.nw_bandwidth_excel_reporting,
    "rssi_excel_reporting": reporting_controller.rssi_excel_reporting,
    "outage_excel_reporting": reporting_controller.outage_excel_reporting,
    "event_excel_reporting": reporting_controller.event_excel_reporting,
    "manage_trap_report": reporting_controller.manage_trap_report,
    "get_trap_data": reporting_controller.get_trap_data,
    "total_data_trap": reporting_controller.total_data_trap,
    "inventory_report": reporting_controller.inventory_report,
    "inventory_reprot_creating": reporting_controller.inventory_reprot_creating,
    # "page_tip_inventory_report": reporting_controller.page_tip_inventory_report,




    # UBRe (odu100) reporting
    "ubre_manage_crc_phy_report": ubre_reporting_controller.ubre_manage_crc_phy_report,
    "ubre_get_crc_phy_data": ubre_reporting_controller.ubre_get_crc_phy_data,
    "ubre_average_data_crc_phy": ubre_reporting_controller.ubre_average_data_crc_phy,
    "ubre_total_data_crc_phy": ubre_reporting_controller.ubre_total_data_crc_phy,
    "ubre_show_group_result": ubre_reporting_controller.ubre_show_group_result,
    "ubre_show_host_result": ubre_reporting_controller.ubre_show_host_result,
    "ubre_show_host_data_of_group": ubre_reporting_controller.ubre_show_host_data_of_group,
    "ubre_manage_rssi_report": ubre_reporting_controller.ubre_manage_rssi_report,
    "ubre_get_rssi_data": ubre_reporting_controller.ubre_get_rssi_data,
    "ubre_average_data_rssi": ubre_reporting_controller.ubre_average_data_rssi,
    "ubre_total_data_rssi": ubre_reporting_controller.ubre_total_data_rssi,
    "ubre_manage_network_usage_report": ubre_reporting_controller.ubre_manage_network_usage_report,
    "ubre_get_network_usage_data": ubre_reporting_controller.ubre_get_network_usage_data,
    "ubre_total_data_network_usage": ubre_reporting_controller.ubre_total_data_network_usage,
    "ubre_odu_excel_reporting": ubre_reporting_controller.ubre_odu_excel_reporting,
    "ubre_nw_bandwidth_excel_reporting": ubre_reporting_controller.ubre_nw_bandwidth_excel_reporting,
    "ubre_rssi_excel_reporting": ubre_reporting_controller.ubre_rssi_excel_reporting,
    # "ubre_help_crc_phy": ubre_reporting_controller.ubre_page_tip_crc_phy,
    # "ubre_help_rssi": ubre_reporting_controller.ubre_page_tip_rssi,
    # "ubre_help_network_usage": ubre_reporting_controller.ubre_page_tip_network_usage,


    # Main Reporting
    "main_report": main_reporting_controller.main_report,
    "main_report_ap25": main_reporting_controller.main_report,
    "main_report_idu4": main_reporting_controller.main_report,
    "main_report_odu16": main_reporting_controller.main_report,
    "main_report_odu100": main_reporting_controller.main_report,
    "main_reporting_get_host_data": main_reporting_controller.main_reporting_get_host_data,
    "main_reporting_get_columns_data": main_reporting_controller.main_reporting_get_columns_data,
    "main_reporting_get_excel": main_reporting_controller.main_reporting_get_excel,
    # "view_page_tip_main_reporting": main_reporting_controller.view_page_tip_main_reporting,

    # Analyzed Reporting
    "analyzed_report": analyzed_reporting_controller.analyzed_report,
    "analyzed_reporting_get_host_data": analyzed_reporting_controller.analyzed_reporting_get_host_data,
    "analyzed_reporting_get_columns_data": analyzed_reporting_controller.analyzed_reporting_get_columns_data,
    "analyzed_reporting_get_excel": analyzed_reporting_controller.analyzed_reporting_get_excel,
    # "view_page_tip_analyzed_reporting": analyzed_reporting_controller.view_page_tip_analyzed_reporting,
    "analyzed_reporting_get_column_range": analyzed_reporting_controller.analyzed_reporting_get_column_range,
    # trap Reporting
    "trapreport": main_reporting_controller.trap_main_report,
    "trap_main_reporting_get_host_data": main_reporting_controller.trap_main_reporting_get_host_data,
    "trap_main_reporting_get_excel": main_reporting_controller.trap_main_reporting_get_excel,
    # "trap_view_page_tip_main_reporting": main_reporting_controller.trap_view_page_tip_main_reporting,
    # HISTORICAL Reporting
    #"history_report" : history_reporting_controller.history_report,
    #"history_report_main" : history_reporting_controller.main_report,
    #"history_reporting_get_host_data":history_reporting_controller.history_reporting_get_host_data,
    #"history_reporting_get_columns_data":history_reporting_controller.history_reporting_get_columns_data,
    #"history_reporting_get_excel":history_reporting_controller.history_reporting_get_excel,
    #"view_page_tip_history_reporting":history_reporting_controller.view_page_tip_history_reporting,
    #"history_reporting_make_db":history_reporting_controller.history_reporting_make_db,
    #"check_db_status_historical":history_reporting_controller.check_db_status_historical,
    #"update_db_status_historical":history_reporting_controller.update_db_status_historical,
    #"clear_data_historical":history_reporting_controller.clear_data_historical,
    #"backup_data_check_historical":history_reporting_controller.backup_data_check_historical,
    #"backup_data_historical":history_reporting_controller.backup_data_historical,
    #"cleanup_data_historical":history_reporting_controller.cleanup_data_historical,
    "history_report": history_reporting_controller.history_report,
    "history_report_main": history_reporting_controller.main_report,
    "history_reporting_get_host_data": history_reporting_controller.history_reporting_get_host_data,
    "history_reporting_get_columns_data": history_reporting_controller.history_reporting_get_columns_data,
    "history_reporting_get_excel": history_reporting_controller.history_reporting_get_excel,
    # "view_page_tip_history_reporting": history_reporting_controller.view_page_tip_history_reporting,
    "history_reporting_make_db": history_reporting_controller.history_reporting_make_db,
    "check_db_status_historical": history_reporting_controller.check_db_status_historical,
    "update_db_status_historical": history_reporting_controller.update_db_status_historical,
    "clear_data_historical": history_reporting_controller.clear_data_historical,
    "backup_data_check_historical": history_reporting_controller.backup_data_check_historical,
    "backup_data_historical": history_reporting_controller.backup_data_historical,
    "cleanup_data_historical": history_reporting_controller.cleanup_data_historical,
    # "view_page_tip_main_history_reporting": history_reporting_controller.view_page_tip_main_history_reporting,

})
