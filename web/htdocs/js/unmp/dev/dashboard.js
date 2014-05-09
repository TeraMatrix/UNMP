var totalAPInTheSystem = 0;
var totalAPInGraph = 10;
var currentAPInGraph = 0;
var currentAPUserInGraph = 0;
var reload_time = 60000;
$(function () {
    reload_time = parseInt($("#refresh_time").val()) * 60000;
    getNumberOfAccessPoint();
    reload();
});
Date.prototype.addHours = function (h) {
    this.setHours(this.getHours() + h);
    return this;
}

Date.prototype.addMinutes = function (m) {
    this.setMinutes(this.getMinutes() + m);
    return this;
}
function reload() {
    systemUptime();
    ramDetails();
    proLastDetails();
    bandLastDetails();
    harddiskDetails();
    if ($("input[name='systemGraphNum']").val() == "4")
        bandDetails(1);
    else if ($("input[name='systemGraphNum']").val() == "5")
        bandDetails(2);
    //ramDetails()
    setTimeout(function () {
        reload();
    }, reload_time);
}
function reloadAPDashboard() {
    accessPointGraphs("");
    accessPointUserGraphs("");
    setTimeout(function () {
        reloadAPDashboard();
    }, reload_time);
}
function harddiskDetailsClick() {
    $("input[name='systemGraphNum']").val("1");
    harddiskDetails();
}
function harddiskDetails() {
    var chart1;
    $.ajax({
        type: "post",
        url: "harddisk_details.py",
        success: function (result) {
            // total,free,available,used
            result = result.split(",");
            $("#hdDetails").html("Total: " + result[0] + "GB; Free: " + result[1] + "GB;<br/>Available: " + result[2] + "GB; Used: " + result[3] + "GB;");
            var used = parseFloat(result[3]) * 100 / parseFloat(result[0]);
            var available = parseFloat(result[2]) * 100 / parseFloat(result[0]);
            used = parseInt(used);
            available = parseInt(available);
            var unused = 100 - used - available;
            if ($("input[name='systemGraphNum']").val() == "1") {
                chart1 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'nmsGraph',
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false
                    },
                    title: {
                        text: 'System Memory Details'
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.point.name + '</b>: ' + this.y + ' %';
                        }
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: false
                            },
                            showInLegend: true
                        }
                    },
                    series: [
                        {
                            type: 'pie',
                            name: 'Browser share',
                            data: [
                                ['Used', used],
                                ['Unused', unused],
                                ['Available', available]
                            ]
                        }
                    ]
                });
            }
        }
    })
}
function systemUptime() {
    $.ajax({
        type: "post",
        url: "system_uptime.py",
        success: function (result) {
            $("#upTimeDetails").html(result);
        }
    });
}
function ramDetailsClick() {
    $("input[name='systemGraphNum']").val("2");
    ramDetails()
}
function ramDetails() {
    var chart2;
    $.ajax({
        type: "post",
        url: "ram_details.py",
        success: function (result) {
            // total,free,available,used
            result = result.split(",");
            usedmemory = parseInt(result[0]);
            totalmemory = parseInt(result[0]) + parseInt(result[1]);
            $("#rmDetails").html((usedmemory < 1024 ? usedmemory + " MB" : parseFloat(usedmemory / 1024).toFixed(2) + " GB") + " (<span id=\"ramUsage\">" + parseFloat(usedmemory * 100 / totalmemory).toFixed(2) + "</span> %) of " + (totalmemory < 1024 ? totalmemory + " MB" : parseFloat(totalmemory / 1024).toFixed(2) + " GB"))

            var used = parseFloat(usedmemory * 100 / totalmemory);
            var available = 100 - used;
            if ($("input[name='systemGraphNum']").val() == "2") {
                chart2 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'nmsGraph',
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false
                    },
                    title: {
                        text: 'System RAM Details'
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.point.name + '</b>: ' + Highcharts.numberFormat(this.y, 2) + ' %';
                        }
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: false
                            },
                            showInLegend: true
                        }
                    },
                    series: [
                        {
                            type: 'pie',
                            name: 'Browser share',
                            data: [
                                ['Available', available],
                                ['Used', used]
                            ]
                        }
                    ]
                });
            }
        }
    })
}

function proDetails() {
    $("input[name='systemGraphNum']").val("3");
    var chart3;
    $.ajax({
        type: "post",
        url: "processor_details.py",
        success: function (result) {
            var jsonData = eval(result);
            // Ram Graph
            chart3 = new Highcharts.Chart({
                global: {
                    useUTC: false
                },
                chart: {
                    renderTo: 'nmsGraph',
                    defaultSeriesType: 'spline',
                    marginRight: 10,
                    events: {
                        load: function () {

                            // set up the updating of the chart each second
                            var series = this.series[0];
                            setInterval(function () {
                                var x = parseInt($("input[id='proUsageTime']").val()), // current time
                                    y = $("#proUsage").html();
                                series.addPoint([x, y], true, true);
                            }, 60000);
                        }
                    }
                },
                title: {
                    text: 'System Processor details'
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 100
                },
                yAxis: {
                    title: {
                        text: 'Usage %'
                    },
                    plotLines: [
                        {
                            value: 0,
                            width: 1,
                            color: '#DF5353'
                        }
                    ]
                },
                tooltip: {
                    formatter: function () {
                        return '<b>' + this.series.name + '</b><br/>' +
                            Highcharts.dateFormat('%H:%M', this.x) + '<br/>' +
                            Highcharts.numberFormat(this.y, 2) + " %";
                    }
                },
                legend: {
                    enabled: false
                },
                exporting: {
                    enabled: false
                },
                series: [
                    {
                        name: 'Processor Usage',
                        data: (function () {
                            // generate an array of random data
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            $.each(jsonData, function (i, dt) {
                                var prodate = dt.datestamp.split("-");
                                var protime = dt.timestamp.split(":");
                                data.push({
                                    x: (new Date(prodate[0], prodate[1], prodate[2], protime[0], protime[1], protime[2], 0)).addHours(5).addMinutes(30).getTime(),
                                    y: dt.cpuusage
                                });
                            });
                            return data;
                        })()
                    }
                ]
            });
        }
    });
}

function proLastDetails() {
    $.ajax({
        type: "post",
        url: "processor_last_details.py",
        success: function (result) {
            var jsonData = eval(result);
            $.each(jsonData, function (i, dt) {
                var prodate = dt.datestamp.split("-");
                var protime = dt.timestamp.split(":");
                var proTimstamp = (new Date(prodate[0], prodate[1], prodate[2], protime[0], protime[1], protime[2], 0)).addHours(5).addMinutes(30).getTime();
                $("#proDetails").html("CPU <span id=\"proUsage\">" + parseFloat(dt.cpuusage).toFixed(2) + "</span> %" + "<input type=\"hidden\" id=\"proUsageTime\" name=\"proUsageTime\" value=\"" + proTimstamp + "\" />");
            });
        }
    });
}
function bandLastDetails() {
    var lastInterface = "";
    $.ajax({
        type: "post",
        url: "bandwidth_last_details.py",
        success: function (result) {
            var jsonData = eval(result);
            $.each(jsonData, function (i, dt) {
                if (lastInterface == "" && lastInterface != dt.inter) {
                    lastInterface = dt.inter;
                    $("#interface1Details").html("<span id=\"inter1\" style=\"font-weight:bold;\">" + dt.inter + "</span> Tx: " + parseFloat(dt.tx).toFixed(2) + " MB/min. Rx: " + parseFloat(dt.rx).toFixed(2) + " MB/min.");
                    //$("#interface2").hide();
                }
                else if (lastInterface != dt.inter) {
                    $("#interface2Details").html("<span id=\"inter2\" style=\"font-weight:bold;\">" + dt.inter + "</span> Tx: " + parseFloat(dt.tx).toFixed(2) + " MB/min. Rx: " + parseFloat(dt.rx).toFixed(2) + " MB/min.");
                    $("#interface2").show();
                }
            });
        }
    });
}
function bandDetails(id) {
    if (id == 1) {
        $("input[name='systemGraphNum']").val("4");
    }
    else if (id == 2) {
        $("input[name='systemGraphNum']").val("5");
    }
    //alert($("#inter" + id).html());
    var chart4;
    $.ajax({
        type: "post",
        url: "bandwidth_details.py?inter=" + $("#inter" + id).html(),
        success: function (result) {
            var jsonData = eval(result);
            var time_x = [];
            var tx_y = [];
            var rx_y = [];
            $.each(jsonData, function (i, dt) {
                strtime = dt.timestamp.substring(0, dt.timestamp.lastIndexOf(":"));
                time_x.push(strtime);
                tx_y.push(dt.tx);
                rx_y.push(dt.rx);
            });
            chart4 = new Highcharts.Chart({
                chart: {
                    renderTo: 'nmsGraph',
                    defaultSeriesType: 'line',
                    marginRight: 80,
                    marginBottom: 25,
                    animation: false
                },
                title: {
                    text: 'Bandwidth Usage',
                    x: -20 //center
                },
                subtitle: {
                    text: 'for ' + $("#inter" + id).html(),
                    x: -20
                },
                xAxis: {
                    categories: time_x
                },
                yAxis: {
                    title: {
                        text: 'Bandwidth (MB)'
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
                        return '<b>' + this.series.name + '</b>(' + this.x + ')<br/>' +
                            this.y + ' MB/min';
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
                        data: tx_y
                    },
                    {
                        name: 'Rx',
                        data: rx_y
                    }
                ],
                plotOptions: {
                    line: {
                        animation: false
                    }
                }
            });
        }
    });
}
function getNumberOfAccessPoint() {
    $.ajax({
        type: "post",
        url: "get_number_of_aps.py",
        success: function (result) {
            totalAPInTheSystem = result;
            if (totalAPInTheSystem == 0) {
                $("#apGraphHead, #apGraph, #apUserGraphHead, #apUserGraph").hide();
            }
            else {
                $("#apGraphHead, #apGraph, #apUserGraphHead, #apUserGraph").show();
                reloadAPDashboard();
            }
        }
    })
}
function accessPointGraphs(action) {
    var chart5;
    if (action == "next") {
        if ($("#nextAP").hasClass("imgbuttondisable")) {
            return false;
        }
        else {
            currentAPInGraph = currentAPInGraph + totalAPInGraph;
        }
    }
    else if (action == "previous") {
        if ($("#previousAP").hasClass("imgbuttondisable")) {
            return false;
        }
        else {
            currentAPInGraph = currentAPInGraph - totalAPInGraph;
            if (currentAPInGraph < 0) {
                currentAPInGraph = 0;
            }
        }
    }
    if (totalAPInTheSystem <= (currentAPInGraph + totalAPInGraph)) {
        $("#nextAP").removeClass("imgbutton").addClass("imgbuttondisable");
    }
    else {
        $("#nextAP").removeClass("imgbuttondisable").addClass("imgbutton");
    }
    if (currentAPInGraph > 0) {
        $("#previousAP").removeClass("imgbuttondisable").addClass("imgbutton");
    }
    else {
        $("#previousAP").removeClass("imgbutton").addClass("imgbuttondisable");
    }
    $.ajax({
        type: "post",
        url: "ap_graph.py?start=" + currentAPInGraph + "&limit=" + totalAPInGraph,
        success: function (result) {
            result = eval("(" + result + ")");
            for (a = result.name.length; a < totalAPInGraph; a++) {
                result.name[a] = " ";
                result.tx[a] = "0";
                result.rx[a] = "0";
            }
            chart5 = new Highcharts.Chart({
                chart: {
                    renderTo: 'apGraph'
                },
                title: {
                    text: ' '
                },
                xAxis: {
                    categories: result.name
                },
                yAxis: {
                    title: {
                        text: 'Bandwidth ( KB/sec )'
                    }
                },
                tooltip: {
                    formatter: function () {
                        var s;
                        if (this.point.name) { // the pie chart
                            s = '' +
                                this.point.name + ': ' + this.y + ' KB/sec';
                        } else {
                            s = '<b>AP: </b>' +
                                this.x + '<br/><b>Bandwidth: </b>' + this.y + ' KB/sec';
                        }
                        return s;
                    }
                },
                labels: {
                    items: [
                        {
                            html: 'Tx/Rx',
                            style: {
                                left: '0px',
                                top: '0px',
                                color: 'black'
                            }
                        }
                    ]
                },
                series: [
                    {
                        type: 'column',
                        name: 'Tx',
                        data: result.tx,
                        color: '#AA4643' // John's color
                    },
                    {
                        type: 'column',
                        name: 'Rx',
                        data: result.rx,
                        color: '#89A54E' // Joe's color
                    },
                    {
                        type: 'spline',
                        name: 'Average',
                        data: result.avrg
                    },
                    {
                        type: 'pie',
                        name: 'Total Tx/Rx',
                        data: [
                            {
                                name: 'Rx',
                                y: result.totalRx,
                                color: '#89A54E' // Joe's color
                            },
                            {
                                name: 'Tx',
                                y: result.totalTx,
                                color: '#AA4643' // John's color
                            }
                        ],
                        center: [60, 0],
                        size: 40,
                        showInLegend: false,
                        dataLabels: {
                            enabled: false
                        }
                    }
                ]
            });
        }
    });
}
function accessPointUserGraphs(action) {
    var chart6;
    if (action == "next") {
        if ($("#nextAPUser").hasClass("imgbuttondisable")) {
            return false;
        }
        else {
            currentAPUserInGraph = currentAPUserInGraph + totalAPInGraph;
        }
    }
    else if (action == "previous") {
        if ($("#previousAPUser").hasClass("imgbuttondisable")) {
            return false;
        }
        else {
            currentAPUserInGraph = currentAPUserInGraph - totalAPInGraph;
            if (currentAPUserInGraph < 0) {
                currentAPUserInGraph = 0;
            }
        }
    }
    if (totalAPInTheSystem <= (currentAPUserInGraph + totalAPInGraph)) {
        $("#nextAPUser").removeClass("imgbutton").addClass("imgbuttondisable");
    }
    else {
        $("#nextAPUser").removeClass("imgbuttondisable").addClass("imgbutton");
    }
    if (currentAPUserInGraph > 0) {
        $("#previousAPUser").removeClass("imgbuttondisable").addClass("imgbutton");
    }
    else {
        $("#previousAPUser").removeClass("imgbutton").addClass("imgbuttondisable");
    }
    $.ajax({
        type: "post",
        url: "ap_user_graph.py?start=" + currentAPUserInGraph + "&limit=" + totalAPInGraph,
        success: function (result) {
            result = eval("(" + result + ")");
            for (a = result.name.length; a < totalAPInGraph; a++) {
                result.name[a] = " ";
                result.user[a] = "0";
            }
            chart6 = new Highcharts.Chart({
                chart: {
                    renderTo: 'apUserGraph',
                    defaultSeriesType: 'column',
                    margin: [ 50, 50, 100, 80]
                },
                title: {
                    text: ' '
                },
                xAxis: {
                    categories: result.name,
                    labels: {
                        rotation: -20,
                        align: 'right',
                        style: {
                            font: 'normal 10px Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Number of Users'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    formatter: function () {
                        return '<b>' + this.x + '</b><br/>' +
                            'Connected Users: ' + Highcharts.numberFormat(this.y, 0);
                    }
                },
                series: [
                    {
                        name: 'User',
                        data: result.user,
                        dataLabels: {
                            enabled: true,
                            rotation: -90,
                            color: '#FFFFFF',
                            align: 'right',
                            x: -3,
                            y: 10,
                            formatter: function () {
                                return this.y;
                            },
                            style: {
                                font: 'normal 10px Verdana, sans-serif'
                            }
                        }
                    }
                ]
            });
        }
    });
}
