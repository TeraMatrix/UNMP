#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@version: 0.1
@note: All Functions that will use fetch data status of nagios configured devices using livestatus.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
import livestatus


class Nagios(object):
    '''
    @requires: Nothing
    @param object: object class to inherit
    @precondition: no pre-conditions
    @note: This Class define all the function which are related with nagios livestatus.
    '''

    @staticmethod
    def tactical_overview(html):
        '''
        @author: Yogesh Kumar
        @param html: html class object
        @var host_query: livestatus query to get hosts status
        @var service_query: livestatus query to get services status
        @return: host and service status
        @rtype: dictionary
        @note: this function gives you total number of ok, critical, warning and unknown state host and services [in dictionary form].
        '''
        host_query = \
            "GET hosts\n" \
            "Stats: state >= 0\n" \
            "Stats: state = 0\n" \
            "Stats: state = 1\n" \
            "Stats: state = 2\n" \
            "Stats: state >= 3\n" \
            "Filter: custom_variable_names < _REALNAME\n"

        service_query = \
            "GET services\n" \
            "Stats: state >= 0\n" \
            "Stats: state = 0\n" \
            "Stats: state = 1\n" \
            "Stats: state = 2\n" \
            "Stats: state >= 3\n" \
            "Filter: host_custom_variable_names < _REALNAME\n"

        try:
            hstdata = html.live.query_summed_stats(
                host_query)          # to execute the live status query which gives you status array i.e. [total hosts,ok status host,warning status host,critical status host,unknown status host]
            svcdata = html.live.query_summed_stats(
                service_query)       # to execute the live status query which gives you status array i.e. [total services,ok status service,warning status service,critical status service,unknown status service]
            return {"hosts": hstdata, "services": svcdata}
        except livestatus.MKLivestatusNotFoundError:
            return {"hosts": [0, 0, 0, 0, 0], "services": [0, 0, 0, 0, 0]}
