#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Mar-2011
@date: 23-Mar-2011
@version: 0.1
@note: --
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the page functions
import live_monitoring_controller
# import rrd_graph

# map URLs to page rendering functions
pagehandlers.update({
    # Live
    "live_monitoring": live_monitoring_controller.live_monitoring_page,
    "get_live_monitoring_graphs": live_monitoring_controller.get_live_monitoring_graphs,
    "get_graph_data": live_monitoring_controller.get_graph_data,
    "live_graph_action": live_monitoring_controller.live_graph_action,
    # "page_tip_live_monitoring": live_monitoring_controller.page_tip_live_monitoring,
    "settings_live_monitoring": live_monitoring_controller.settings_live_monitoring,
    "save_live_monitoring_config": live_monitoring_controller.save_live_monitoring_config,
    "load_live_monitoring_default_config": live_monitoring_controller.load_live_monitoring_default_config,
    "download_live_monitoring_excel_file": live_monitoring_controller.download_live_monitoring_excel_file,
    "download_live_monitoring_csv_file": live_monitoring_controller.download_live_monitoring_csv_file,
    # "help_live_monitoring": live_monitoring_controller.page_tip_live_monitoring,
    #"rrd":rrd_graph.rrd,
})
