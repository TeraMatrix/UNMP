#!/usr/bin/python2.6
# import the packeges
from json import JSONEncoder

#@TODO: all * should be removed
from common_controller import *
from lib import *
from nms_config import *
from odu_controller import *
from unmp_dashboard_bll import DashboardBll
from error_message import ErrorMessageClass
from nagios_livestatus import Nagios


# create the global object of sp_bll_obj
global sp_bll_obj, err_obj
err_obj = ErrorMessageClass()
sp_bll_obj = DashboardBll()


def unmp_common_graph_creation(h):
    global html, sp_bll_obj
    html = h
    graph_id = html.var("graph_id")
    device_type = html.var("device_type")
    if graph_id is not None and graph_id.strip() == 'mouReachablity':
        tactical_list = Nagios.tactical_overview(html)
        json_data = []
        json_data.append(
            {'Ok': tactical_list['hosts'][1], 'Warning': tactical_list['hosts'][2],
             'Critical': tactical_list['hosts'][3], 'Unknown': tactical_list['hosts'][4]})
        result_dict = {'success': 0, 'timestamp': [], 'data':
            json_data, 'graph_title': "", 'graph_sub_title': ""}
    else:
        result_dict = sp_bll_obj.common_graph_json(device_type, graph_id)
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(result_dict)))


def dashlet_hoststats(h):
    global html
    html = h
    table = [
        (_("Up"), "#0b3",
         "searchhost&is_host_scheduled_downtime_depth=0&hst0=on",
         "Stats: state = 0\n"
         "Stats: scheduled_downtime_depth = 0\n"
         "StatsAnd: 2\n"),

        (_("Down"), "#FFF354",
         "searchhost&is_host_scheduled_downtime_depth=0&hst1=on",
         "Stats: state = 1\n"
         "Stats: scheduled_downtime_depth = 0\n"
         "StatsAnd: 2\n"),

        (_("Unreachable"), "#f00",
         "searchhost&is_host_scheduled_downtime_depth=0&hst2=on",
         "Stats: state = 2\n"
         "Stats: scheduled_downtime_depth = 0\n"
         "StatsAnd: 2\n"),

        (_("Unknown"), "#0af",
         "searchhost&search=1&is_host_scheduled_downtime_depth=1",
         "Stats: scheduled_downtime_depth > 0\n"
        )
    ]
    filter = "Filter: custom_variable_names < _REALNAME\n"
    render_statistics("hoststats", "hosts", table, filter)


def render_statistics(pie_id, what, table, filter):
    html_list = []
    try:
        html_list.append("<div class=dashlet>")
        # Is the query restricted to a certain WATO-path?
        query = "GET %s\n" % what
        for entry in table:
            query += entry[3]
        query += filter

        result = html.live.query_summed_stats(query)
        pies = zip(table, result)
        total = sum([x[1] for x in pies])

        html_list.append('<table class="hoststats%s" style="float:right">' % (
            len(pies) > 1 and " narrow" or ""))
        table_entries = pies
        while len(table_entries) < 4:
            table_entries = table_entries + [(("", "#95BBCD",
                                               "", ""), "&nbsp;")]
        table_entries.append(((_("Total"), "", "all%s" % what, ""), total))
        for (name, color, viewurl, query), count in table_entries:
            url = "#"
            # html_list.append('<tr><th><a href="%s">%s</a></th>' % (url,
            # name))
            html_list.append('<tr><th>%s</th>' % (name))
            style = ''
            if color:
                style = ' style="background-color: %s"' % color
            html_list.append('<td class=color%s>'
                             #'</td><td><a href="%s">%s</a></td></tr>' % (style, url, count))
                             '</td><td>%s</td></tr>' % (style, count))

        html_list.append("</table>")
        html_list.append("</div>")
    except Exception, e:
        html_list = [""]
    html.write("".join(html_list))
