var nwInterfaceChart;
var tdmoipNWInterfaceChart;
var iduTrapGraphChart;
var iduPortStatusChart;
var iduOutageChart;
$(function () {
    nwInterfaceGraph();
    iduDeviceInformation();
    tdmoipNWInterfaceGraph();
    iduPortStatusGraph();
    iduAlarmInformation();
    iduTrapGraph();
    iduOutageGraph();
});

function nwInterfaceGraph() {
    host_id = $("#idu_host_id").val();
    ip_address = $("#idu_ip_address").val();
    $.ajax({
        type: "post",
        url: "idu_network_interface_graph.py?host_id=" + host_id + "&ip_address=" + ip_address,
        data: $(this).serialize(),
        success: function (result) {
            try {
                nwResult = eval('(' + result + ')');
            }
            catch (err) {
                alert('Data not receive in proper format so please contact to your administrator.')
                return;
            }
            if (nwResult.success == 1 || nwResult.success == "1") {
                alert(nwResult.output);
                return;
            }
            else if (nwResult.success == 2 || nwResult.success == '2') {
                alert('Some problem occured due to database connection, so please contact your Administrator.');
                return;
            }
            else {
                $("#iduName").html(nwResult.idu_ip_address);
                nwInterfaceChart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'idu_nw_interface_div',
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 30
                    },
                    title: {
                        text: 'IDU Network Interface Graph',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'eth0(Rx/Tx)',
                        x: -20
                    },
                    xAxis: {
                        categories: nwResult.timestamp
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
                            return '<b> Time:</b>' + this.x + '</b><br/>' +
                                '<b>' + this.series.name + '</b>' + ': ' + this.y + 'Kbps';
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'top',
                        x: -10,
                        y: 100,
                        borderWidth: 0
                    },
                    series: [
                        {
                            name: 'Tx',
                            data: nwResult.txBytes
                        },
                        {
                            name: 'Rx',
                            data: nwResult.rxBytes
                        }
                    ]
                });
            }
        }
    });
}

function iduDeviceInformation() {
    host_id = $("#idu_host_id").val();
    ip_address = $("#idu_ip_address").val();

    $.ajax({
        type: "post",
        url: "idu_device_information.py?host_id=" + host_id + "&ip_address=" + ip_address,
        data: $(this).serialize(),
        success: function (result) {
            try {
                deviceResult = eval('(' + result + ')');
            }
            catch (err) {
                alert('Data not receive in proper format so please contact to your administrator.')
                return;
            }
            if (deviceResult.success == 1 || deviceResult.success == "1") {
                alert(deviceResult.output);
                return;
            }
            else if (deviceResult.success == 2 || deviceResult.success == '2') {
                alert('Some problem occured due to database connection, so please contact your Administrator.');
                return;
            }
            else {
                $("#idu_device_information").html(deviceResult.device_details)
            }
        }
    });
    return false;
}

function tdmoipNWInterfaceGraph() {
    host_id = $("#idu_host_id").val();
    ip_address = $("#idu_ip_address").val();
    $.ajax({
        type: "post",
        url: "idu_tdmoip_network_interface_graph.py?host_id=" + host_id + "&ip_address=" + ip_address,
        data: $(this).serialize(),
        success: function (result) {
            try {
                nwResult = eval('(' + result + ')');
            }
            catch (err) {
                alert('Data not receive in proper format so please contact to your administrator.')
                return;
            }
            if (nwResult.success == 1 || nwResult.success == "1") {
                alert(nwResult.output);
                return;
            }
            else if (nwResult.success == 2 || nwResult.success == '2') {
                alert('Some problem occured due to database connection, so please contact your Administrator.');
                return;
            }
            else {
                tdmoipNWInterfaceChart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'idu_tdmoip_nw_interface_div',
                        defaultSeriesType: 'line',
                        marginRight: 10,
                        marginBottom: 30
                    },
                    title: {
                        text: 'IDU TDMOIP Network Interface Graph',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'eth0(Rx/Tx)',
                        x: -20
                    },
                    xAxis: {
                        categories: nwResult.timestamp
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
                            return '<b> Time:</b>' + this.x + '</b><br/>' +
                                '<b>' + this.series.name + '</b>' + ': ' + this.y + 'Kbps';
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'top',
                        x: -10,
                        y: 100,
                        borderWidth: 0
                    },
                    series: [
                        {
                            name: 'Tx',
                            data: nwResult.tx_transmiting
                        },
                        {
                            name: 'Rx',
                            data: nwResult.rx_receving
                        }
                    ]
                });
            }
        }
    });
}


// this function display the port status information
function iduPortStatusGraph() {
    host_id = $("#idu_host_id").val();
    ip_address = $("#idu_ip_address").val();
    $.ajax({
        type: "post",
        url: "idu_port_status_graph.py?host_id=" + host_id + "&ip_address=" + ip_address,
        data: $(this).serialize(),
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                alert('Data not receive in proper format so please contact to your administrator.')
                return;
            }
            if (result.success == 1 || result.success == "1") {
                alert(result.output);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                alert('Some problem occured due to database connection, so please contact your Administrator.');
                return;
            }
            else {
                image_json = '['
                for (var i = 0; i < result.link_speed.length; i++) {
                    if (result.link_speed[i] == 0) {
                        image_json += "{'y':" + result.link_speed[i] + ',' + "'marker':{'symbol':" + "'url(images/port-enable.png)'}}";
                    }
                    else {
                        image_json += "{'y':" + result.link_speed[i] + ',' + "'marker':{'symbol':" + "'url(images/port-disable.png)'}}";
                    }
                    if (i != ((result.link_speed).length) - 1)
                        image_json += ",";
                }
                image_json += ']'

                iduPortStatusChart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'idu_port_status_div',
                        zoomType: 'xy'
                    },
                    title: {
                        text: 'IDU Port Status'
                    },
                    subtitle: {
                        text: 'Port/speed'
                    },
                    xAxis: [
                        {
                            categories: result.port_name
                        }
                    ],
                    yAxis: [
                        { // Primary yAxis
                            labels: {
                                formatter: function () {
                                    return this.value + 'mbps';
                                },
                                style: {
                                    color: '#89A54E'
                                }
                            },
                            title: {
                                text: 'speed',
                                style: {
                                    color: '#89A54E'
                                }
                            }
                        }
                    ],
                    tooltip: {
                        formatter: function () {
                            return '' +
                                '<b>' + this.x + '</b>' + ': ' + this.y + 'mbps'
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'top',
                        x: 100,
                        verticalAlign: 'top',
                        y: 10,
                        floating: true//,
                        //backgroundColor: Highcharts.theme.legendBackgroundColor || '#FFFFFF'
                    },
                    series: [
                        {
                            color: '#4572A7',
                            type: 'column',
                            name: 'speed',
                            marker: {
                                symbol: 'diamond'
                            },
                            data: result.link_speed
                        }

                        ,
                        {
                            color: '#89A54E',
                            type: 'spline',
                            name: 'speed',
                            border: '0px none',
                            marker: {
                                symbol: 'diamond'
                            },
                            data: eval(image_json)

                        }
                    ]
                });
            }
        }
    });
}


// This function show the latest IDU trap and alarm information.
function iduAlarmInformation() {
    host_id = $("#idu_host_id").val();
    ip_address = $("#idu_ip_address").val();
    $.ajax({
        type: "post",
        url: "idu_trap_information.py?host_id=" + host_id + "&ip_address=" + ip_address,
        data: $(this).serialize(),
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
                alert('Data not receive in proper format so please contact to your administrator.')
                return;
            }
            if (result.success == 1 || result.success == "1") {
                alert(result.output);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                alert('Some problem occured due to database connection, so please contact your Administrator.');
                return;
            }
            else {
                $("#idu_current_alarm_div").html(result.alarm_output);
                $("#idu_current_trap_div").html(result.trap_output);
            }
        }
    });
}


// --- This function is call idu_trap_graph and this display the 10 day graph of particular device.
function iduTrapGraph() {
    host_id = $("#idu_host_id").val();
    ip_address = $("#idu_ip_address").val();
    $.ajax({
        type: "post",
        url: "idu_trap_graph.py?host_id=" + host_id + "&ip_address=" + ip_address,
        data: $(this).serialize(),
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                alert("Data not receive in proper format so please contact to your administrator.");
                return;
            }
            if (result.success == 1 || result.success == "1") {
                alert(result.output);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                alert('Some problem occured due to database connection and services, so please contact your Administrator.');
                return;
            }
            else {
                iduTrapGraphChart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'idu_trap_graph_div',
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: 'Last 10 Days Traps Inforamation'
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
                                '<b>' + this.series.name + '</b>' + ': ' + this.y + '<br/>' +
                                '<b>Total</b>:' + this.point.stackTotal;
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
        },
        error: function (req, status, err) {
        }
    });
}


// ---- This function display the outage graph .-----
function iduOutageGraph() {
    host_id = $("#idu_host_id").val();
    ip_address = $("#idu_ip_address").val();
    $.ajax({
        type: "post",
        url: "idu_outage_graph.py?host_id=" + host_id + "&ip_address=" + ip_address,
        data: $(this).serialize(),
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                alert("Data not receive in proper format so please contact to your administrator.");
                return;
            }
            if (result.success == 1 || result.success == "1") {
                alert(result.output);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                alert('Some problem occured due to database connection, so please contact your Administrator.');
                return;
            }
            else {
                iduOutageChart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'idu_outage_graph_div',
                        defaultSeriesType: 'column'
                    },
                    title: {
                        text: 'Last 10 Days IDU Up/Down Statistics'
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
        },
        error: function (req, status, err) {
        }
    });
}


