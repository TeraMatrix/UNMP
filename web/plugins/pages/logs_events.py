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
import logs_events_controller

# map URLs to page rendering functions
pagehandlers.update({
    # Logs Events
    "manage_logs": logs_events_controller.manage_logs,
    "search_logs": logs_events_controller.search_logs,
    "manage_events": logs_events_controller.manage_events,
    "search_events": logs_events_controller.search_events,
})
