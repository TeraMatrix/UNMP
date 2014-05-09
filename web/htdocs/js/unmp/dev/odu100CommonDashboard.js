var bandwidthChart;
var errorChart;
var signalChart;
var syncLostChart;
var outageGraph;

var totalODUInTheSystem = 0;

var nwBandwidth = null;
var errorGraph = null;
var rssiGraph = null;
var syncLost = null;
var outage = null;
var $spinLoading = null;
var $spinMainLoading = null;
var odu100CommonRecursionVar = null;

$(function () {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    getNumberOfODU100();
});

function odu100CommonDashboardGraphs(div, start, limit, interface_value) {
    $.ajax({
        type: "post",
        url: "odu100_network_interface_graph.py?start=" + start + "&limit=" + limit + "&interface_value=" + interface_value,
        cache: false,
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 3 || result.success == '3') {
                $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else {
                bandwidthChart = new Highcharts.Chart({
                    chart: {
                        renderTo: div,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: ''
                    },
                    subtitle: {
                        text: ''
                    },
                    xAxis: {
                        categories: result.odu_name
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Tx/Rx (kbps)'
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        x: 7,
                        verticalAlign: 'top',
                        y: 1,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: true
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.x + '</b><br/>' +
                                '<b>' + this.series.name + '</b>' + ': ' + Number(this.y).toFixed(2) + ' (Kbps)';
                        }
                    },
                    plotOptions: {
                        column: {
                            pointPadding: 0.2,
                            borderWidth: 0
                        }
                    },
                    series: [
                        {
                            name: 'Transmitted Bytes',
                            data: result.tx_interface

                        },
                        {
                            name: 'Recevied Bytes',
                            data: result.rx_interface

                        }
                    ]
                });
                $.yoDashboard.hideLoading(nwBandwidth);
            }
        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}


// ----- tdd mac error graph ------//
function odu100CommonDashboardErrorGraph(div, start, limit) {
    $.ajax({
        type: "post",
        url: "odu100_tdd_mac_error.py?start=" + start + "&limit=" + limit,
        cache: false,
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 3 || result.success == '3') {
                $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else {
                errorChart = new Highcharts.Chart({
                    chart: {
                        renderTo: div,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: ''
                    },
                    subtitle: {
                        text: ''
                    },
                    xAxis: {
                        categories: result.odu_name
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Count'
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        x: 7,
                        verticalAlign: 'top',
                        y: 1,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: true
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.x + '</b><br/>' +
                                '<b>' + this.series.name + '</b>' + ': ' + Number(this.y).toFixed(0) + ' (error)';
                        }
                    },
                    plotOptions: {
                        column: {
                            pointPadding: 0.2,
                            borderWidth: 0
                        }
                    },
                    series: [
                        {
                            color: "#696F9D",
                            name: 'Crc Error',
                            data: result.crc_error

                        },
                        {
                            color: "#AE2E52",
                            name: 'Phy Error',
                            data: result.phy_error

                        }
                    ]
                });
                $.yoDashboard.hideLoading(errorGraph);
            }
        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}


//-------- Signal strength graph --------//
function odu100CommonDashboardSignalStrengthGraph(div, start, limit, signalInterfaceValue) {
    $.ajax({
        type: "post",
        url: "odu100_peer_node_signal.py?start=" + start + "&limit=" + limit + "&interface_value=" + signalInterfaceValue,
        cache: false,
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 3 || result.success == '3') {
                $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else {
                signalChart = new Highcharts.Chart({
                    chart: {
                        renderTo: div,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: ''
                    },
                    xAxis: {
                        categories: result.odu_name
                    },
                    yAxis: {
                        title: {
                            text: 'dBm'
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        x: 7,
                        verticalAlign: 'top',
                        y: 1,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: true
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.x + '</b><br/>' +
                                '<b>' + this.series.name + '</b>' + ': ' + Number(this.y).toFixed(0) + '(dbm)';
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    series: [
                        {
                            color: "#30A33D",
                            name: 'Signal Strength',
                            data: result.signal
                        }
                    ]
                });
                $.yoDashboard.hideLoading(rssiGraph);

            }

        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}


//---- Sync lost Counter graph ---- //

function odu100CommonDashboardSyncLostGraph(div, start, limit) {
    $.ajax({
        type: "post",
        url: "odu100_synslost_counter.py?start=" + start + "&limit=" + limit,
        cache: false,
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 3 || result.success == '3') {
                $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else {
                syncLostChart = new Highcharts.Chart({
                    chart: {
                        renderTo: div,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: ''
                    },
                    xAxis: {
                        categories: result.odu_name
                    },
                    yAxis: {
                        title: {
                            text: 'Count'
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        x: 7,
                        verticalAlign: 'top',
                        y: 1,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: true
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.x + '</b><br/>' +
                                '<b>' + this.series.name + '</b>' + ': ' + Number(this.y).toFixed(0) + '';
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    series: [
                        {
                            color: "#DCCC21",
                            name: 'Sync Loss',
                            data: result.counter
                        }
                    ]
                });
                $.yoDashboard.hideLoading(syncLost);
            }

        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}


//------ get No. of odu in system -----//
function getNumberOfODU100() {
    if (odu100CommonRecursionVar != null) {
        clearTimeout(odu100CommonRecursionVar);
    }
    var refresh_time = ($("#refresh_time").val());
    var no_of_device = ($("#no_of_device").val());
    spinStart($spinLoading, $spinMainLoading);
    no_of_device = parseInt(no_of_device);
    $.ajax({
        type: "post",
        url: "get_no_of_odu100_devices.py",
        cache: false,
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 3 || result.success == '3') {
                $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else {
                totalODUInTheSystem = parseInt(result.output);
                if (totalODUInTheSystem == 0) {
                    $("#main_odu100_common_div").hide();
                    $("#show_message_div").html('Device not exists for graphs.')
                    spinStop($spinLoading, $spinMainLoading);
                }
                else {
                    nwBandwidth = $("#dashboard4").yoDashboard({
                        title: "Network Bandwidth Statistics Graph",
                        showRefreshButton: true,
                        showNextPreButton: true,
                        startFrom: 0,
                        itemLimit: no_of_device,
                        ajaxRequest: function (div_obj, start, limit, tab_value) {
                            odu100CommonDashboardGraphs(div_obj.attr("id"), start, limit, tab_value);
                            return true;
                        },
                        getTotalItem: function () {
                            return totalODUInTheSystem
                        },
                        showTabOption: true,
                        tabList: {value: [1, 2], name: ["eth0", "eth1"], selected: 1},
                        height: "180px"
                    });

                    errorGraph = $("#dashboard1").yoDashboard({
                        title: "CRC PHY Error Graph",
                        showRefreshButton: true,
                        showNextPreButton: true,
                        startFrom: 0,
                        itemLimit: no_of_device,
                        ajaxRequest: function (div_obj, start, limit) {
                            odu100CommonDashboardErrorGraph(div_obj.attr("id"), start, limit);
                            return true;
                        },
                        getTotalItem: function () {
                            return totalODUInTheSystem
                        },
                        showTabOption: true,
                        //tabList: {value:[1,2,3,4],name:["eth0","br0","ath0","ath1"],selected:1},
                        height: "180px"
                    });
                    rssiGraph = $("#dashboard3").yoDashboard({
                        title: "RSSI Graph",
                        showRefreshButton: true,
                        showNextPreButton: true,
                        startFrom: 0,
                        itemLimit: no_of_device,
                        ajaxRequest: function (div_obj, start, limit, tab_value) {
                            odu100CommonDashboardSignalStrengthGraph(div_obj.attr("id"), start, limit, tab_value);
                            return true;
                        },
                        getTotalItem: function () {
                            return totalODUInTheSystem
                        },
                        showTabOption: true,
                        tabList: {value: [1, 2, 3, 4, 5, 6, 7, 8], name: ["peer1", "peer2", "peer3", "peer4", "peer5", "peer6", "peer7", "peer8"], selected: 1},
                        height: "180px"
                    });
                    syncLost = $("#dashboard2").yoDashboard({
                        title: "Sync Loss Graph",
                        showRefreshButton: true,
                        showNextPreButton: true,
                        startFrom: 0,
                        itemLimit: no_of_device,
                        ajaxRequest: function (div_obj, start, limit, tab_value) {
                            odu100CommonDashboardSyncLostGraph(div_obj.attr("id"), start, limit);
                            return true;
                        },
                        getTotalItem: function () {
                            return totalODUInTheSystem
                        },
                        height: "180px"
                    });
                    outage = $("#dashboard5").yoDashboard({
                        title: "Device Reachability Graph",
                        showRefreshButton: true,
                        showNextPreButton: true,
                        startFrom: 0,
                        itemLimit: no_of_device,
                        ajaxRequest: function (div_obj, start, limit, tab_value) {
                            odu100CommonDashboardOutageGraph(div_obj.attr("id"), start, limit);
                            return true;
                        },
                        getTotalItem: function () {
                            return totalODUInTheSystem
                        },
                        height: "180px"
                    });

                    $("#show_graph").show();
                    spinStop($spinLoading, $spinMainLoading);
                    odu100CommonRecursionVar = setTimeout(function () {
                        getNumberOfODU100();
                    }, refresh_time * 60000);
                }
            }
        }
    });
}


//---- ODU Outage graph ---- //
function odu100CommonDashboardOutageGraph(div, start, limit) {
    $.ajax({
        type: "post",
        url: "odu100_common_dashboard_outage_graph.py?start=" + start + "&limit=" + limit,
        cache: false,
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 3 || result.success == '3') {
                $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else {
                outageGraph = new Highcharts.Chart({
                    chart: {
                        renderTo: div,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: ''
                    },
                    xAxis: {
                        categories: result.odu_name
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Percentage'
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        x: 7,
                        verticalAlign: 'top',
                        y: 1,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: true
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.x + '</b><br/>' +
                                '<b>' + this.series.name + '</b>' + ': ' + Number(this.y).toFixed(2) + '%';
                        }
                    },
                    plotOptions: {
                        column: {
                            stacking: 'normal'
                        }
                    },
                    series: [
                        {
                            color: "#B79292",
                            name: 'Reachable',
                            data: result.up_state
                        },
                        {
                            color: "#80699B",
                            name: 'Unreachable',
                            data: result.down_state
                        }
                    ]
                });
                $.yoDashboard.hideLoading(outage);
            }

        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}


// This function generate the report for odu  common devices.
function odu100CommonReportGeneration() {
    clearTimeout(odu100CommonRecursionVar);
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "odu100_common_dashboard_report_generating.py?error_start=" + String(errorGraph.options.startFrom) + "&error_limit=" + String(errorGraph.options.itemLimit) + "&nw_start=" + String(nwBandwidth.options.startFrom) + "&nw_limit=" + String(nwBandwidth.options.itemLimit) + "&nw_interface_value=" + String(nwBandwidth.options.tabList.selected) + "&ss_start=" + String(rssiGraph.options.startFrom) + "&ss_limit=" + String(rssiGraph.options.itemLimit) + "&ss_interface_value=" + String(rssiGraph.options.tabList.selected) + "&sync_start=" + String(syncLost.options.startFrom) + "&sync_limit=" + String(syncLost.options.itemLimit) + "&outage_start=" + String(outage.options.startFrom) + "&outage_limit=" + String(outage.options.itemLimit),
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
            }
            else if (result.success == 3 || result.success == '3') {
                $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
            }
            else {
                $().toastmessage('showSuccessToast', 'Report generated Successfully.');
                window.location = "report/odu100_common_table.pdf";
                getNumberOfODU100();
            }
            spinStop($spinLoading, $spinMainLoading);
            getNumberOfODU100();

        }
    });
}


