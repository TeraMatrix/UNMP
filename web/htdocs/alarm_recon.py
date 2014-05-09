def view():
    """


    @return:
    """
    success = 1
    #
    try:
        s = ''
        s += """<div>
                <script type="text/javascript" src="js/unmp/main/alarm_recon.js"></script>
                <div id="outer_div">
                    <div id="details" name="%(id)s">
                        <table id="alarm_details" class="tt-table" cellspacing="0" cellpadding="0" width="100%%">
                            <colgroup><col width="15%%"/><col width="35%%"/><col width="15%%"/><col width="35%%"/></colgroup>
                            <tbody>
                                <tr>
                                    <th class="cell-title" colspan="4">Alarm Reconciliation Details</th>
                                </tr>
                                <tr>
                                    <td class="cell-label">Host Alias</td>
                                    <td class="cell-info">%(alias)s</td>
                                    <td class="cell-label">IP Address</td>
                                    <td class="cell-info">%(ip)s</td>
                                </tr>
                                <tr>
                                    <td class="cell-label">Last Run</td>
                                    <td class="cell-info" id="time">%(timestamp)s</td>
                                    <td class="cell-label">Message</td>
                                    <td class="cell-info" id="result">%(msg)s</td>
                                </tr>
                                <tr>
                                    <td class="cell-label">Host Status</td>
                                    <td class="cell-info" id="state">%(state)s</td>
                                    <td class="cell-label">Message</td>
                                    <td class="cell-info" id="output">%(output)s</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div id="alarm_actions" class="status_legend" style="margin-top:0px;padding-bottom:0px;padding-top:0px;">
                        <div id="op-status" style="margin-right:20px;margin-left:5px;vertical-align:middle;display:inline;">
                            <span>Process Status</span>
                            <img class="n-reconcile" id="img-status" name="img-status" \
                                src="images/host_status%(status)s.png" title="%(status_msg)s" \
                                style="width:14px;height:14px;margin-left:5px;vertical-align: middle;" \
                                original-title="%(status_msg)s">
                        </div>
                        <div id="alarm_recon_start" style="margin-left:25px;display:inline;">
                            <span>Reconcile Last </span>
                            <select id="recon_items" style="width:60px;">\
                                <option value="20" class='required' selected="selected">20</option>
                                <option value="40"  >40</option>
                                <option value="80"  >80</option>
                                <option value="120" >120</option>
                                <option value="200"  >200</option>
                                <option value="2000" >All</option>
                            </select>
                            <span> Alarms </span>
                            <button type="submit" class="yo-small yo-button" id="start_recon_alarm" style="margin-left:5px;min-width:50px;">
                                Start</button>
                        </div>
                        <a style="margin-left:25px;" href="status_snmptt.py?ip_address=%(ip)s-" >
                            Alarm dashboard</a>
                    </div>
                    <div id="alarm_table">
                    </div>
            </div></div>"""
        success = 0
    except Exception, e:
        s = e
    finally:
        return s

# useful comments
#<button type="submit" class="yo-small yo-button" id="show_recon_alarm" style="margin-left:25px;" >
#                            Show Reconcilied Alarms</button>
