#! /usr/bin/python2.6
from json import JSONEncoder

import alarm_recon  # view
import alarm_recon_bll  # bll
from common_bll import Essential
from lib import *


def recon_display(h):
    global html
    try:
        html = h
        host_id = html.var('host_id')
        device_type = html.var('device_type')
        view_str = 'Unknown'
        success = 1
        # host_id = '94'
        user_id = html.req.session['user_id']
        if device_type == 'odu100' and host_id:
            es = Essential()
            if es.is_host_allow(user_id, host_id) == 0:
                arl = alarm_recon_bll.recon_bll(host_id)
                bll_dict = arl.get_all_info()
                if bll_dict['success'] == 0:
                    view_str = alarm_recon.view()
                    host_uptime = get_uptime_details(bll_dict['result']['ip'])
                    if host_uptime['success'] == 0:
                        bll_dict['result'][
                            'output'] = host_uptime['result'].get('output', '')
                        bll_dict['result'][
                            'state'] = host_uptime['result'].get('state', '')
                    else:
                        bll_dict['result']['output'] = host_uptime['result']
                        bll_dict['result']['state'] = 'Unknown'

                    if isinstance(view_str, str):
                        try:
                            view_str = view_str % (bll_dict['result'])
                            success = 0
                        except Exception, e:
                            view_str = str(e)
                else:
                    view_str = bll_dict['result']

                if success == 0:
                    # html.new_header("Alarm
                    # Reconciliation","recon_display.py","",[],["js/unmp/main/alarm_recon.js"])
                    html.write(view_str)
                    # html.new_footer()
                else:
                    # html.new_header("Alarm
                    # Reconciliation","recon_display.py","",[],["js/unmp/main/alarm_recon.js"])
                    html.write("<div class=\"error\" > %s </div>" % (view_str))
                    # html.new_footer()
            else:
                # html.new_header(" Warning : 404 Page Not Found","","")
                html.write("<div class=\"warning\" > No such host exists : : Access Restricted</div>")

        else:
            # html.new_header("Alarm
            # Reconciliation","recon_display.py","",[],["js/unmp/main/alarm_recon.js"])
            html.write(alarm_recon.view() + str(html.live))
            # html.new_footer()
    except Exception, e:
        html.write(
            "<div class=\"error\" > %s </div>" % (" Encounterd an Error "))
        # import traceback
        # html.new_header("Alarm Reconciliation","recon_display.py","",[],["js/unmp/main/alarm_recon.js"])
        # html.write("<div class=\"error\" > %s </div>"%(str(traceback.format_exc())))
        # html.new_footer()


def get_uptime_details(host_ip):
    success = 1
    result = {}
    try:
        if host_ip:
            # query_service = "GET services\nColumns: state
            # service_plugin_output service_long_plugin_output  \nFilter:
            # description = SNMP UPTIME \nFilter host_address = 172.22.0.120 \n
            # And: 2"
            query_service = "GET services\nColumns: state description service_plugin_output service_long_plugin_output \nFilter: host_address = " + \
                            host_ip
            html.live.set_prepend_site(True)
            services = html.live.query(query_service)
            services.sort()
            html.live.set_prepend_site(False)
            result['output'] = ''
            state = None
            temp = {0: ' OK ', 1: ' Warning ', 2: ' Critical ', 3: ' Unknown '}
            for site, state, description, output, all_output in services:
                all_device_detail = ' (' + str(
                    all_output).replace('\\n', '') + ')'
                # host_age=age
                if description != 'SNMP UPTIME':
                    continue
                if int(state) == 0:
                    s = output + str('' if all_device_detail.strip(
                    ) == '()' else all_device_detail)
                    find_str = "Host Uptime -"
                    if s.find(find_str) != -1:
                        result['output'] = s[
                                           s.find(find_str) + len(find_str):s.find(")") - 1]
                if description == 'SNMP UPTIME':
                    break

            result['state'] = "<span class=\"span-status-container icon-%s\">%s</span>" % (
                state, temp.get(int(state), 3))
            success = 0
        else:
            raise Exception(' uptime: Host ip address not found ')
    except Exception, e:
        import traceback
        #\n \            Filter: description = 'SNMP UPTIME'
        result = traceback.format_exc()  # str(e)
    finally:
        result_dict = {}
        result_dict['success'] = success
        if success == 0:
            result_dict['result'] = result
        else:
            result_dict['result'] = result
        return result_dict


def start_alarm(h):
    global html
    html = h
    host_id = html.var('host_id')
    recon_items = html.var('recon_items')
    user_id = html.req.session['user_id']
    result_dict = {'success': 1, 'result': 'Unknown Error', }
    if host_id:
        es = Essential()
        if es.is_host_allow(user_id, host_id) == 0:
            ar = alarm_recon_bll.AlarmRecon(host_id, recon_items)
            result_dict = ar.recon()
            if result_dict['success'] == 1 and isinstance(result_dict['result'], str):
                result_dict['error_got'] = result_dict['result']
                result_dict['result'] = " Alarm Reconciliation Process encounter an error, \n Please try later"
        else:
            result_dict = {'success': 1, 'result':
                'No such host exists : Access Restricted', }
    else:
        result_dict = {'success': 1, 'result': 'No such host found', }

    # html.req.content_type = 'application/json'
    # html.req.write(str(JSONEncoder().encode(result_dict)))
    html.write(str(result_dict))


def update_alarmview(h):
    global html
    html = h
    host_id = html.var('host_id')
    user_id = html.req.session['user_id']
    result_dict = {'success': 1, 'result': 'Unknown Error', }
    if host_id:
        es = Essential()
        if es.is_host_allow(user_id, host_id) == 0:
            arl = alarm_recon_bll.recon_bll(host_id)
            result_dict = arl.get_all_info()
            if result_dict['success'] == 0:
                host_uptime = get_uptime_details(result_dict['result']['ip'])
                if host_uptime['success'] == 0:
                    result_dict['result'][
                        'output'] = host_uptime['result'].get('output', '')
                    result_dict['result'][
                        'state'] = host_uptime['result'].get('state', '')
                else:
                    result_dict['result']['output'] = host_uptime['result']
                    result_dict['result']['state'] = 'Unknown'
                di_result = result_dict.pop('result')
                result_dict.update(di_result)
                result_dict['result'] = 'success'
            else:
                result_dict = {'success': 1, 'result': 'No such host found', }
        else:
            result_dict = {'success': 1, 'result':
                'No such host exists : Access Restricted', }
    else:
        result_dict = {'success': 1, 'result': 'No such host found', }

    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result_dict)))
    # html.write(str(result_dict))
