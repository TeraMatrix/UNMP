var chartODUEth0;
var chartCrcPhy;
var chartSignalStrength;
var outage_graph;
var oduSyncLostChart;
var $spinLoading = null;
var $spinMainLoading = null;
var odu100_ip_address = null;
var odu100RecursionVar = null;
var limitFlag = 1; // limitFlag used for limit of show data on graph. 1 for 15 data show on graph and 1 means all data exists in date interval page.

var nwBandwidth = null;
var errorGraph100 = null;
var rssiGraph100 = null;
var syncLost100 = null;
var outage100 = null;
var alarmDetail100 = null;
var trapDetail100 = null;
var trapAllDetail = null;


$(function () {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    $("input[id='current_rept_div']").attr("checked", "checked");
    $("#device_type").change(function () {
        $("#filter_ip").val("");
        $("#filter_mac").val("");
    });
    oduGraphButtonClick();
    $('#odu_start_date, #odu_start_time, #odu_end_date,  #odu_end_time').calendricalDateTimeRange({
        isoTime: true
    });
    odu100_ip_address = $("input#ip_address").val();
    if (odu100_ip_address != undefined || odu100_ip_address != '') {
        graphInitiator();
    }
    $("input[id='btnSearch']").click(function () {
        //call the device list function on click of search button
        deviceList();
    })
    $("input[id='filter_ip']").keypress(function () {
        $("input[id='filter_mac']").val("");
    })
    // Slide up and slide down functionality starthere
    $("#tab_yo").slideUp('fast');
    $("#adSrhODU100").toggle(
        function () {
            $('#tab_yo').slideDown('slow', function () {
                limitFlag = 0;
                $("#adSrhODU100").val('Hide Search')
            });
        },
        function () {
            $('#tab_yo').slideUp('slow', function () {
                limitFlag = 1;
                $("#adSrhODU100").val('Advance Graph')
            });
            odu100AddDateTime();

        });
    // Slide up and slide down functionality end here
//	$("#page_tip").colorbox(
//	{
//	href:"page_tip_ubre_monitor_dashboard.py",
//	title: "Page Tip",
//	opacity: 0.4,
//	maxWidth: "80%",
//	width:"650px",
//	height:"450px",
//	onComplte:function(){}
//	})


});

function odu100AddDateTime() {
    $.ajax({
        type: "post",
        url: "add_date_time_on_slide_odu100.py",
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                return;
            }
            else {
                $("#odu_start_date").val(result.start_date);
                $("#odu_end_date").val(result.end_date);
                $("#odu_start_time").val(result.start_time);
                $("#odu_end_time").val(result.end_time);
            }
        }
    });
    return false; //always remamber this
}


function oduGraphButtonClick() {
    $("#odu_graph_show").click(function () {
        limitFlag = 0;
        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var h = cur_date.getHours();
        var mi = cur_date.getMinutes();
        var cdate = new Date(y, m, d, h, mi);
        var str1 = $("#odu_start_date").val();
        var str2 = $("#odu_end_date").val();
        var str3 = $("#odu_start_time").val();
        var str4 = $("#odu_end_time").val();
        str1 = str1.split("/");
        str2 = str2.split("/");
        str3 = str3.split(":");
        str4 = str4.split(":");
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0], str3[0], str3[1]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0], str4[0], str4[1]);
        if (date2 < date1) {
            $().toastmessage('showWarningToast', "End Date can't be greater than Start Date");
            return false;
        }
        else if (cdate < date1 || cdate < date2) {
            $().toastmessage('showWarningToast', "Dates can't be greater than current Date");
            return false;
        }
        else {
            graphInitiator();
        }

    });
}


function deviceList() {
    var device_type = "odu16,odu100";
    // this retreive the value of ipaddress textbox
    var ip_address = $("input[id='filter_ip']").val();
    // this retreive the value of macaddress textbox
    var mac_address = $("input[id='filter_mac']").val();
    // this retreive the value of selectdevicetype from select menu
    var selected_device_type = $("select[id='device_type']").val();
    // this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url
    odu100_ip_address = ip_address
    $.ajax({
        type: "post",
        url: "get_device_list_odu100_for_monitoring.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
        cache: false,
        success: function (result) {
            if (result == 0 || result == "0") {
                $("#odu100_show_msg").html("No Data exist.");
                $("#adSrhODU100").hide(); // hide the button
                $("#tab_yo").hide();
                $("#odu100_device_graph").hide();
                $("#odu100_host_info_div").hide();
                $("#report_button_div").hide();

            }
            else if (result == 1 || result == "1") {
                parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

            }
            else if (result == 2 || result == "2") {

                $("#odu100_show_msg").html("Please Try Again.");
                $("#adSrhODU100").hide(); // hide the button
                $("#tab_yo").hide();
                $("#odu100_device_graph").hide();
                $("#odu100_host_info_div").hide();
                $("#report_button_div").hide();

            }
            else {
                if (selected_device_type == 'odu16') {
                    parent.main.location = "odu_profiling1.py?host_id=" + result + "&device_type=" + selected_device_type + "&device_list_state=enabled";
                }
                else {
                    $("#adSrhODU100").show(); // show the button
                    $("input#filter_ip").val(result);
                    $("#odu100_show_msg").html("")
                    odu100_ip_address = $("input#ip_address").val();
//							$("#tab_yo").show();
                    $("#odu100_device_graph").show();
                    $("#odu100_host_info_div").show();
                    $("#report_button_div").show();
                    graphInitiator();
                }
            }
        }
    });
}


function odu100NetworkInterfacesTable(divId, interface_value) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    //var interface_value=1;
    $.ajax({
        type: "post",
        url: "odu100_network_interface_table_graph.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&interface_value=" + interface_value + "&limitFlag=" + limitFlag,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
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

                chartODUEth0 = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 25
                    },
                    title: {
                        text: 'Network Bandwidth Transfer Rate',
                        x: -20 //center
                    },
                    subtitle: {
                        text: ' ',
                        x: -20
                    },
                    xAxis: {
                        categories: result.time_stamp0
                    },
                    yAxis: {
                        title: {
                            text: 'Transfer Rate (Kbps)'
                        },
                        plotLines: [
                            {
                                value: 0,
                                width: 1,
                                color: '#808080'
                            }
                        ]
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.series.name + '</b><br/>' +
                                '<b>' + this.x + '</b>' + ': ' + this.y + '(Kbps)';
                        }
                    },
                    legend: {
                        align: 'left',
                        x: 11,
                        verticalAlign: 'top',
                        y: 1,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: true
                    },
                    series: [
                        {
                            name: 'Tx',
                            data: result.interface_tx
                        },
                        {
                            name: 'Rx',
                            data: result.interface_rx
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


function odu100ErrorGraph(div) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    $.ajax({
        type: "post",
        url: "odu100_error_graph.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&limitFlag=" + limitFlag,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            //alert(result)
            try {
                result = eval("(" + result + ")");
            } catch (err) {
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
                chartCrcPhy = new Highcharts.Chart({
                    chart: {
                        renderTo: div,
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 25
                    },
                    title: {
                        text: 'Error Transfer Rate',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'Crc/Phy Error',
                        x: -20
                    },
                    xAxis: {
                        categories: result.time_stamp
                    },
                    yAxis: {
                        title: {
                            text: 'Error Count'
                        },
                        plotLines: [
                            {
                                value: 0,
                                width: 1,
                                color: '#808080'
                            }
                        ]
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.series.name + '</b><br/>' +
                                '<b>' + this.x + '</b>' + ':' + this.y + '(Error Count)';
                        }
                    },
                    legend: {
                        align: 'left',
                        x: 11,
                        verticalAlign: 'top',
                        y: 1,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: true
                    },
                    series: [
                        {
                            name: 'Crc',
                            data: result.crc_error
                        },
                        {
                            name: 'Phy',
                            data: result.phy_error
                        }
                    ]
                });
                $.yoDashboard.hideLoading(errorGraph100);
            }
        }
    });

    return false;
}


function odu100SyncLostGraph(divId) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();

    $.ajax({
        type: "post",
        url: "odu100_sync_lost_graph.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&limitFlag=" + limitFlag,
        data: $(this).serialize(),
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
                image_json = '['
                for (var i = 0; i < result.sync_lost.length; i++) {
                    if (result.sync_lost[i] == 0) {
                        image_json += "{'y':" + result.sync_lost[i] + ',' + "'marker':{'symbol':" + "'url(images/port-enable.png)'}}";
                    }
                    else {
                        image_json += "{'y':" + result.sync_lost[i] + ',' + "'marker':{'symbol':" + "'url(images/port-disable.png)'}}";
                    }
                    if (i != ((result.sync_lost).length) - 1)
                        image_json += ",";
                }
                image_json += ']'

                oduSyncLostChart = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        zoomType: 'xy'
                    },
                    title: {
                        text: 'Sync Lost Count'
                    },
                    subtitle: {
                        text: ''
                    },
                    xAxis: [
                        {
                            categories: result.sync_time_stamp
                        }
                    ],
                    yAxis: [
                        { // Primary yAxis
                            labels: {
                                formatter: function () {
                                    return this.value + '';
                                },
                                style: {
                                    color: '#89A54E'
                                }
                            },
                            title: {
                                text: '',
                                style: {
                                    color: '#89A54E'
                                }
                            }
                        }
                    ],
                    tooltip: {
                        formatter: function () {
                            return '' +
                                '<b>' + this.x + '</b><br/>' + '<b>sync lost :</b>' + this.y
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'top',
                        x: 51,
                        verticalAlign: 'top',
                        y: 10,
                        floating: true
                    },
                    series: [
                        {
                            color: '#4572A7',
                            type: 'column',
                            name: ' sync lost',
                            marker: {
                                symbol: 'diamond'
                            },
                            data: result.sync_lost
                        }

                        ,
                        {
                            color: '#89A54E',
                            type: 'spline',
                            border: '0px none',
                            marker: {
                                symbol: 'diamond'
                            },
                            data: eval(image_json)

                        }
                    ]
                });
                $.yoDashboard.hideLoading(syncLost100);
            }
        }
    });
}


function odu100SignalStrengthGraph(divId) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    $.ajax({
        type: "post",
        url: "odu100_signal_strength_graph.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&limitFlag=" + limitFlag,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            //alert(result)
            try {
                result = eval("(" + result + ")");
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
                chartSignalStrength = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: 'Signal Strength'
                    },
                    xAxis: {
                        categories: result.time_stamp
                    },
                    yAxis: {
                        title: {
                            text: 'signal strength '
                        }
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.series.name + '</b><br/>' +
                                '<b>' + this.x + '</b>' + ': ' + this.y + '(dbm)';
                        }
                    },
                    credits: {
                        enabled: false
                    },

                    series: eval(result.display_signal_strength)

                });
                $.yoDashboard.hideLoading(rssiGraph100);
            }
        }
    });
    return false;
}

function odu100TrapGraph(divId) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    $.ajax({
        type: "post",
        url: "odu100_trap_graph.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&limitFlag=" + limitFlag,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
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
                trap_graph = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: 'Last 5 Days Events Information'
                    },
                    xAxis: {
                        categories: result.output.timestamp
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Event count'
                        }
                    },
                    legend: {
                        align: 'right',
                        x: -11,
                        verticalAlign: 'top',
                        y: 20,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: false
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.x + '</b><br/>' +
                                '<b>' + this.series.name + '</b>' + ': ' + this.y + '<br/>' +
                                '<b>Total</b>: ' + this.point.stackTotal;
                        }
                    },
                    plotOptions: {
                        column: {
                            stacking: 'normal'
                        }
                    },
                    series: [
                        {
                            color: "#90D968",
                            name: 'Normal',
                            data: result.output.graph[0]
                        },
                        {
                            color: "#3C9C08",
                            name: 'Informational',
                            data: result.output.graph[1]
                        },
                        {
                            color: "#5185C1",
                            name: 'Minor',
                            data: result.output.graph[2]
                        },
                        {
                            color: "#ECDA3B",
                            name: 'Major',
                            data: result.output.graph[3]
                        },
                        {
                            color: "#EB2D23",
                            name: 'Critical',
                            data: result.output.graph[4]
                        }
                    ]
                });
                $.yoDashboard.hideLoading(trapAllDetail100);
            }
        },
        error: function (req, status, err) {
        }
    });

}


// ---- This function display the outage graph .
function odu100OutageGraph(divId) {
    $.ajax({
        type: "post",
        url: "odu100_outage_graph.py?ip_address=" + odu100_ip_address + "&limitFlag=" + limitFlag,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
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
                outage_graph = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: 'Last 5 Days Up/Down Statistics'
                    },
                    xAxis: {
                        categories: result.date_days
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Alarms count'
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'left',
                        x: 51,
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
                            name: 'Up State',
                            data: result.up_state
                        },
                        {
                            color: "#80699B",
                            name: 'Down State',
                            data: result.down_state
                        }
                    ]
                });
                $.yoDashboard.hideLoading(outage100);
            }
        },
        error: function (req, status, err) {
        }
    });
}


//------ This function  is call the odu_detail_information for showing the  silver information of particular device. ------


function deviceDetailInformation(divObj) {
//	host_id=$("input#host_id").val()
    $.ajax({
        type: "post",
        url: "odu100_device_information.py?ip_address=" + odu100_ip_address,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
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
                divObj.html(result.device_table);
            }
        },
        error: function (req, status, err) {
        }
    });
}

// ---- This function dispaly the some information for device dashboard in table form --//
function odu100trapAlarmInformation(divObj, table_option) {
    $.ajax({
        type: "post",
        url: "odu100_trap_information.py?ip_address=" + odu100_ip_address + "&table_option=" + table_option,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
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
                divObj.html(result.output);

            }
            if (table_option == 'alarm')
                $.yoDashboard.hideLoading(alarmDetail100);
            else
                $.yoDashboard.hideLoading(trapDetail100);

        },
        error: function (req, status, err) {
        }
    });
}


// Function for all graph initiator
function graphInitiator() {
    if (odu100RecursionVar != null) {
        clearTimeout(odu100RecursionVar);
    }
    if (odu100_ip_address == undefined || odu100_ip_address == '' || odu100_ip_address == null) {
        $("#tab_yo").hide();
        $("#odu100_show_msg").html('Data Not exists for graph.');
        $("#adSrhODU100").hide(); // hide the button
        $("#report_button_div").hide();
        $("#odu100_host_info_div").html("");
        $("#odu100_device_graph").hide();
        return;
    }

    var refresh_time = $("#refresh_time").val();
    $("#adSrhODU100").show(); // show the button
    spinStart($spinLoading, $spinMainLoading);
    deviceDetailInformation($('#odu100_host_info_div'));
    nwBandwidth = $("#dashboard6").yoDashboard({
        title: "Network Bandwidth Graph",
        showRefreshButton: true,
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            odu100NetworkInterfacesTable(div_obj.attr("id"), tab_value);
            return true;
        },
        showTabOption: true,
        tabList: {value: [1, 2], name: ["eth0", "eth1"], selected: 1},
        height: "180px"
    });
    errorGraph100 = $("#dashboard1").yoDashboard({
        title: "Error graph",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            odu100ErrorGraph(div_obj.attr("id"));
            return true;
        },
        height: "180px"
    });
    syncLost100 = $("#dashboard3").yoDashboard({
        title: "sync lost graph",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            odu100SyncLostGraph(div_obj.attr("id"));
            return true;
        },
        height: "180px"
    });
    rssiGraph100 = $("#dashboard2").yoDashboard({
        title: "Signal strength",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            odu100SignalStrengthGraph(div_obj.attr("id"));
            return true;
        },
        height: "180px"
    });
    trapAllDetail100 = $("#dashboard4").yoDashboard({
        title: "latest 5 days Events information",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            odu100TrapGraph(div_obj.attr("id"));
            return true;
        },
        height: "180px"
    });
    outage100 = $("#dashboard5").yoDashboard({
        title: "latest 5 days Outage graph",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            odu100OutageGraph(div_obj.attr("id"));
            return true;
        },
        height: "180px"
    });
    alarmDetail100 = $("#dashboard7").yoDashboard({
        title: "latest alarms",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            odu100trapAlarmInformation(div_obj, 'alarm');
            return true;
        },
        height: "180px"
    });

    trapDetail100 = $("#dashboard8").yoDashboard({
        title: "latest Events",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            odu100trapAlarmInformation(div_obj, 'trap');
            return true;
        },
        height: "180px"
    });
    spinStop($spinLoading, $spinMainLoading);
    odu100RecursionVar = setTimeout(function () {
        graphInitiator();
        odu100AddDateTime();
    }, refresh_time * 60000);
}


function odu100ReportGeneration() {
    if (odu100RecursionVar != null) {
        clearTimeout(odu100RecursionVar);
    }
    var select_option = $("input[name='option']:checked").val();
    if (select_option == 0) {
        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var h = cur_date.getHours();
        var mi = cur_date.getMinutes();
        var cdate = new Date(y, m, d, h, mi);
        var str1 = $("#odu_start_date").val();
        var str2 = $("#odu_end_date").val();
        var str3 = $("#odu_start_time").val();
        var str4 = $("#odu_end_time").val();
        str1 = str1.split("/");
        str2 = str2.split("/");
        str3 = str3.split(":");
        str4 = str4.split(":");
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0], str3[0], str3[1]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0], str4[0], str4[1]);
        if (date2 < date1) {
            $().toastmessage('showWarningToast', "End Date can't be greater than Start Date");
        }
        else if (cdate < date1 || cdate < date2) {
            $().toastmessage('showWarningToast', "Dates can't be greater than current Date");
        }
        else {

            var start_date = $("#odu_start_date").val();
            var start_time = $("#odu_start_time").val();
            var end_date = $("#odu_end_date").val();
            var end_time = $("#odu_end_time").val();
            spinStart($spinLoading, $spinMainLoading);
            $.ajax({
                type: "post",
                url: "odu100_device_report.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag,
                data: $(this).serialize(),
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                    } catch (err) {
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
                        $().toastmessage('showSuccessToast', 'Report Generated Successfully.');
                        window.location = "report/odutable.pdf";
                        graphInitiator();

                    }
                    spinStop($spinLoading, $spinMainLoading);

                }
            });
        }
    }
    else {
        var start_date = $("#odu_start_date").val();
        var start_time = $("#odu_start_time").val();
        var end_date = $("#odu_end_date").val();
        var end_time = $("#odu_end_time").val();
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: "odu100_device_report.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag,
            data: $(this).serialize(),
            cache: false,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                } catch (err) {
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
                    $().toastmessage('showSuccessToast', 'Report Generated Successfully.');
                    window.location = "report/odutable.pdf";
                    graphInitiator();

                }
                spinStop($spinLoading, $spinMainLoading);

            }
        });
    }
}


// Excel reprot genration
function odu100ExcelReportGeneration() {
    if (odu100RecursionVar != null) {
        clearTimeout(odu100RecursionVar);
    }
    var select_option = $("input[name='option']:checked").val();
    if (select_option == 0) {
        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var h = cur_date.getHours();
        var mi = cur_date.getMinutes();
        var cdate = new Date(y, m, d, h, mi);
        var str1 = $("#odu_start_date").val();
        var str2 = $("#odu_end_date").val();
        var str3 = $("#odu_start_time").val();
        var str4 = $("#odu_end_time").val();
        str1 = str1.split("/");
        str2 = str2.split("/");
        str3 = str3.split(":");
        str4 = str4.split(":");
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0], str3[0], str3[1]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0], str4[0], str4[1]);
        if (date2 < date1) {
            $().toastmessage('showWarningToast', "End Date can't be greater than Start Date");
        }
        else if (cdate < date1 || cdate < date2) {

            $().toastmessage('showWarningToast', "Dates can't be greater than current Date");
        }
        else {
            var start_date = $("#odu_start_date").val();
            var start_time = $("#odu_start_time").val();
            var end_date = $("#odu_end_date").val();
            var end_time = $("#odu_end_time").val();
            spinStart($spinLoading, $spinMainLoading);
            $.ajax({
                type: "post",
                url: "odu100_excel_report_genrating.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag,
                data: $(this).serialize(),
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                    } catch (err) {
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
                        $().toastmessage('showSuccessToast', 'Report Generated Successfully');
                        window.location = "download/ubre_specific_report.xls";
                        graphInitiator();

                    }
                    spinStop($spinLoading, $spinMainLoading);

                }
            });
        }

    }

    else {
        var start_date = $("#odu_start_date").val();
        var start_time = $("#odu_start_time").val();
        var end_date = $("#odu_end_date").val();
        var end_time = $("#odu_end_time").val();
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: "odu100_excel_report_genrating.py?ip_address=" + odu100_ip_address + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag,
            data: $(this).serialize(),
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                } catch (err) {
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
                    $().toastmessage('showSuccessToast', 'Report Generated Successfully.');
                    window.location = "download/ubre_specific_report.xls";
                    graphInitiator();
                }
                spinStop($spinLoading, $spinMainLoading);

            }
        });
    }
}



