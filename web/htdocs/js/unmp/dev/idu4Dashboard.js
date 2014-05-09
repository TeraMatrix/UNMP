var chartIDU4Eth0;
var chartIDU4TDMOIP;
var chartEvent;
var chartOutage;
var idu4RecursionVar = null;
var idu4IpAddress = null;
var $spinLoading = null;
var $spinMainLoading = null;
var limitFlag = 1;
var portChart = null;
var e1portChart = null;
var statusChart = null;
var selectLink = null;
var iduNWBandwidth = null;
var iduTDMOIPBandwidth = null;
var iduPortStatistics = null;
var iduEvent = null;
var iduOutage = null;
var iduLatestAlarm = null;
var iduLatestEvent = null;
var iduePortStatus = null;
var iduLinkStatus = null;
$(function () {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    $("input[id='current_rept_div']").attr("checked", "checked");
    $("#device_type").change(function () {
        $("#filter_ip").val("");
        $("#filter_mac").val("");
    });
    $('#odu_start_date, #odu_start_time, #odu_end_date,  #odu_end_time').calendricalDateTimeRange({
        isoTime: true
    });
    $("input[id='filter_ip']").keypress(function () {
        $("input[id='filter_mac']").val("");
    })
    idu4IpAddress = $("input#filter_ip").val();
    oduGraphButtonClick();

    graphInitiator();   // calling the function for graph showing
//	$("#page_tip").colorbox(
//	{
//	href:"page_tip_idu4_monitor_dashboard.py",
//	title: "Page Tip",
//	opacity: 0.4,
//	maxWidth: "80%",
//	width:"650px",
//	height:"450px",
//	onComplte:function(){}
//	})
    // Slide up and slide down functionality starthere
    $("#tab_yo").slideUp('fast');
    $("#adSrhIDU4").toggle(
        function () {
            $('#tab_yo').slideDown('slow', function () {
                limitFlag = 0;
                $("#adSrhIDU4").val('Hide Search')
            });
        },
        function () {
            $('#tab_yo').slideUp('slow', function () {
                limitFlag = 1;
                $("#adSrhIDU4").val('Advance Graph')
                idu4AddDateTime();

            });
        });
    // Slide up and slide down functionality end here

});

// This function update date and time
function idu4AddDateTime() {
    $.ajax({
        type: "post",
        url: "idu4_add_date_time_on_slide.py",
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


// Function for all graph initiator
function graphInitiator() {
    if (idu4RecursionVar != null) {
        clearTimeout(idu4RecursionVar);
    }
    if (idu4IpAddress == undefined || idu4IpAddress == '' || idu4IpAddress == null) {
        $("#tab_yo").hide();
        $("#idu4_show_msg").html('Data Not exists for graph.');
        $("#adSrhIDU4").hide(); // show the button
        $("#report_button_div").hide();
        $("#idu4_host_info_div").html("");
        $("#idu4_device_graph").hide();
        return;
    }
    var refresh_time = $("#refresh_time").val();
    $("#adSrhIDU4").show(); // show the button
    idu4DeviceDetail($('#idu4_host_info_div'));
    checkLink();
    iduNWBandwidth = $("#dashboard9").yoDashboard({
        title: "Network Bandwidth(Eth0)",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            idu4NetworkInterfacesTable(div_obj.attr("id"), 0);
            return true;
        },
        height: "180px"
    });
    iduTDMOIPBandwidth = $("#dashboard10").yoDashboard({
        title: "TDMOIP Network Bandwidth(Eth0)",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            idu4TDMOIPNetworkInterfacesTable(div_obj.attr("id"), 0);
            return true;
        },
        height: "180px"
    });
    iduEvent = $("#dashboard3").yoDashboard({
        title: "Event Informations",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            idu4EventGraph(div_obj.attr("id"));
            return true;
        },
        height: "180px"
    });
    iduOutage = $("#dashboard4").yoDashboard({
        title: "Outage Informations",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            idu4OutageGraph(div_obj.attr("id"));
            return true;
        },
        height: "180px"
    });
    iduLatestAlarm = $("#dashboard5").yoDashboard({
        title: "latest alarms",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            idu4EventAlarmTable(div_obj, 'alarm');
            return true;
        },
        height: "180px"
    });

    iduLatestEvent = $("#dashboard6").yoDashboard({
        title: "latest Events",
        showRefreshButton: true,
        ajaxRequest: function (div_obj) {
            idu4EventAlarmTable(div_obj, 'trap');
            return true;
        },
        height: "180px"
    });
    iduPortStatistics = $("#dashboard11").yoDashboard({
        title: "Port statistics",
        showRefreshButton: true,
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            idu4PortStatisticsGraph(div_obj.attr("id"), tab_value);
            return true;
        },
        showTabOption: true,
        tabList: {value: [0, 1, 2, 3, 4], name: ["odu", "etho", "eth1", "cpu", "maxima"], selected: 0},
        height: "180px"
    });

    iduePortStatus = $("#dashboard7").yoDashboard({
        title: "E1 Port Statistics",
        showRefreshButton: true,
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            idu4e1PortStatusTable(div_obj.attr("id"), tab_value);
            return true;
        },
        showTabOption: true,
        tabList: {value: [1, 2, 3, 4], name: ["port 1", "port 2", "port 3", "port 4"], selected: 1},
        height: "180px"
    });

    idu4RecursionVar = setTimeout(function () {
        graphInitiator();
        idu4AddDateTime();
    }, refresh_time * 60000);
}

function checkLink() {
    $.ajax({
        type: "post",
        url: "idu4_get_link_value_name.py",
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            //alert(result)
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
                if (selectLink == null)
                    selectLink = result.link_value[0];
                iduLinkStatus = $("#dashboard2").yoDashboard({
                    title: "Link Status",
                    showRefreshButton: true,
                    ajaxRequest: function (div_obj, start, limit, tab_value) {
                        selectLink = tab_value;
                        idu4LinkStatusTable(div_obj.attr("id"), tab_value);
                        return true;
                    },
                    showTabOption: true,
                    tabList: {value: result.link_value, name: result.link_name, selected: selectLink},
                    height: "180px"
                });
            }
            $.yoDashboard.hideLoading(iduLinkStatus);
        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}


function oduGraphButtonClick() {
    $("#idu_graph_show").click(function () {
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


function idu4NetworkInterfacesTable(divId, interface_value) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    $.ajax({
        type: "post",
        url: "idu4_network_interface_graph.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&interface_value=" + interface_value + "&limitFlag=" + limitFlag,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            //alert(result)
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

                chartIDU4Eth0 = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 25
                    },
                    title: {
                        text: 'IDU4 TRANSFER RATE',
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

            }
            $.yoDashboard.hideLoading(iduNWBandwidth);
        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}


function idu4TDMOIPNetworkInterfacesTable(divId, interface_value) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    $.ajax({
        type: "post",
        url: "idu4_tdmoip_network_interface_graph.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&interface_value=" + interface_value + "&limitFlag=" + limitFlag,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            //alert(result)
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

                chartIDU4TDMOIP = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 25
                    },
                    title: {
                        text: 'IDU4 TDMOIP TRANSFER RATE',
                        x: -20 //center
                    },
                    subtitle: {
                        text: ' ',
                        x: -20
                    },
                    xAxis: {
                        categories: result.time_stamp
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
                            data: result.transmit
                        },
                        {
                            name: 'Rx',
                            data: result.receive
                        }
                    ]
                });

            }
            $.yoDashboard.hideLoading(iduTDMOIPBandwidth);

        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}

// This graph for port statistics

function idu4PortStatisticsGraph(divId, interface_value) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    $.ajax({
        type: "post",
        url: "idu4_port_statistics_graph.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&interface_value=" + interface_value + "&limitFlag=" + limitFlag,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            //alert(result)
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

                portChart = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 25
                    },
                    title: {
                        text: 'Port Transfer Rate',
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

            }
            $.yoDashboard.hideLoading(iduPortStatistics);
        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}


// ---- This function display the outage graph .
function idu4EventGraph(divId) {
    $.ajax({
        type: "post",
        url: "idu4_event_graph.py?ip_address=" + idu4IpAddress + "&limitFlag=" + limitFlag,
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
                chartEvent = new Highcharts.Chart({
                    chart: {
                        renderTo: divId,
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: 'Last 5 Days IDU4 Event Statistics'
                    },
                    xAxis: {
                        categories: result.output.timestamp
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Alarms count'
                        }
                    },
                    legend: {
                        align: 'right',
                        x: -100,
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
            }
            $.yoDashboard.hideLoading(iduEvent);
        },
        error: function (req, status, err) {
        }
    });
}


// ---- This function display the outage graph .
function idu4OutageGraph(divId) {
    $.ajax({
        type: "post",
        url: "idu4_outage_graph.py?ip_address=" + idu4IpAddress + "&limitFlag=" + limitFlag,
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
                            text: 'Up/Down state'
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
            }
            $.yoDashboard.hideLoading(iduOutage);
        },
        error: function (req, status, err) {
        }
    });
}


function idu4DeviceDetail(divObj) {
    $.ajax({
        type: "post",
        url: "idu4_device_details.py?ip_address=" + idu4IpAddress,
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


// Link status table
function idu4LinkStatusTable(divObj, interface_value) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    $.ajax({
        type: "post",
        url: "idu4_link_status_table.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&limitFlag=" + limitFlag + "&interface_value=" + interface_value,
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
                $("#dashboard1").html(result.table_result); // create the table
                statusChart = new Highcharts.Chart({
                    chart: {
                        renderTo: divObj,
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 25
                    },
                    title: {
                        text: 'Link Status',
                        x: -20 //center
                    },
                    subtitle: {
                        text: ' ',
                        x: -20
                    },
                    xAxis: {
                        categories: result.graph_result[6]
                    },
                    yAxis: {
                        title: {
                            text: 'count'
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
                        align: 'middle',
                        x: 0,
                        y: 0,
                        verticalAlign: 'bottom',
                        y: 1,
                        floating: true,
                        backgroundColor: '#FFFFFF',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: true
                    },
                    series: [
                        {
                            name: 'Good Frame(etho)',
                            data: result.graph_result[0]
                        },
                        {
                            name: 'Good Frame(Rx)',
                            data: result.graph_result[1]
                        },
                        {
                            name: 'Lost Packet',
                            data: result.graph_result[2]
                        },
                        {
                            name: 'Discard Packets',
                            data: result.graph_result[3]
                        },
                        {
                            name: 'Record Packets',
                            data: result.graph_result[4]
                        },
                        {
                            name: 'Under Run Events',
                            data: result.graph_result[5]
                        }
                    ]
                });


            }
            $.yoDashboard.hideLoading(iduePortStatus);
        },
        error: function (req, status, err) {
        }
    });
}


// This is used for E1 port statistics
function idu4e1PortStatusTable(divObj, interface_value) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();

    $.ajax({
        type: "post",
        url: "idu4_e1_port_status_table.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&interface_value=" + interface_value + "&limitFlag=" + limitFlag,
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
                $("#dashboard8").html(result.e1_port_table);
                e1portChart = new Highcharts.Chart({
                    chart: {
                        renderTo: divObj,
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 25
                    },
                    title: {
                        text: 'E1 Port Statistics',
                        x: -20 //center
                    },
                    subtitle: {
                        text: ' ',
                        x: -20
                    },
                    xAxis: {
                        categories: result.time_stamp
                    },
                    yAxis: {
                        title: {
                            text: 'error count'
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
                            name: 'BPV error count',
                            data: result.e1_port_graph
                        }
                    ]
                });


            }
            $.yoDashboard.hideLoading(iduePortStatus);
        },
        error: function (req, status, err) {
        }
    });
}


// ---- This function dispaly the some information for device dashboard in table form --//
function idu4EventAlarmTable(divObj, table_option) {
    $.ajax({
        type: "post",
        url: "idu4_alarm_event_table.py?ip_address=" + idu4IpAddress + "&table_option=" + table_option,
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
                $.yoDashboard.hideLoading(iduLatestAlarm);
            else
                $.yoDashboard.hideLoading(iduLatestEvent);

        },
        error: function (req, status, err) {
        }
    });
}


// PDF reprot genration
function idu4PDFReportGeneration() {
    if (idu4RecursionVar != null) {
        clearTimeout(idu4RecursionVar);
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
                url: "idu4_pdf_generating.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag,
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
                        $().toastmessage('showSuccessToast', 'Report generated Successfully.');
                        window.location = "download/IDU4_PDF_Report.pdf";
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
            url: "idu4_pdf_generating.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag,
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
                    $().toastmessage('showSuccessToast', 'Report generated Successfully.');
                    window.location = "download/IDU4_PDF_Report.pdf";
                    graphInitiator();

                }
                spinStop($spinLoading, $spinMainLoading);

            }
        });
    }
}


// PDF reprot genration
function idu4ExcelReportGeneration() {
    if (idu4RecursionVar != null) {
        clearTimeout(idu4RecursionVar);
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
                url: "idu4_excel_generating.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag,
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
                        $().toastmessage('showSuccessToast', 'Report generated Successfully.');
                        window.location = "download/IDU4_excel.xls";
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
            url: "idu4_excel_generating.py?ip_address=" + idu4IpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag,
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
                    $().toastmessage('showSuccessToast', 'Report generated Successfully.');
                    window.location = "download/IDU4_excel.xls";
                    graphInitiator();

                }
                spinStop($spinLoading, $spinMainLoading);

            }
        });
    }
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
    idu4IpAddress = ip_address
    $.ajax({
        type: "post",
        url: "get_device_list_odu100_for_monitoring.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
        cache: false,
        success: function (result) {
            if (result == 0 || result == "0") {
                $("#odu100_show_msg").html("No Data exist.")
                $("#adSrhIDU4").hide(); // hide the button
                $("#tab_yo").hide();
                $("#odu100_device_graph").hide();
                $("#odu100_host_info_div").hide();
                $("#report_button_div").hide();


            }
            else if (result == 1 || result == "1") {
                parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

            }
            else if (result == 2 || result == "2") {

                $("#odu100_show_msg").html("Please Try Again.")
                $("#adSrhIDU4").hide(); // hide the button
                $("#tab_yo").hide();
                $("#odu100_device_graph").hide();
                $("#odu100_host_info_div").hide();
                $("#report_button_div").hide();

            }
            else {
                $("#odu100_show_msg").html("")
                $("#adSrhIDU4").show(); // show the button
                $("#tab_yo").show();
                $("input#filter_ip").val(result);
                idu4IpAddress = result;
                $("#odu100_device_graph").show();
                $("#odu100_host_info_div").show();
                $("#report_button_div").show();
                graphInitiator();
            }
        }
    });
}

