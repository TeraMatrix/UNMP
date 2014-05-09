var a = 0;
var chart1 = null;
var chart2 = null;
var chart3 = null;
var chart4 = null;
var chart3SetInterval = null;
var chart4SetInterval = null;
var yo1 = null;
var yo2 = null;
var yo3 = null;


$(function () {
//	$("#page_tip").colorbox( //page tip
//		    	{
//			href:"view_page_tip_local_dashboard.py",
//			title: "Page Tip",
//			opacity: 0.4,
//			maxWidth: "80%",
//			width:"400px",
//			height:"400px"
//		    });

    setTimeout(function () {
        if (tactical_call != null) {
            clearTimeout(tactical_call);
        }
    }, 25000);
});
/* Demo Try End*/
$(function () {
    systemUptime();
    yo1 = $("#dashboard1").yoDashboard({
        title: "System RAM Statistics",
        showRefreshButton: true,
        showNextPreButton: false,
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            ramDetails(div_obj.attr("id"));
            return true;
        },
        showTabOption: false,
        height: "200px"
    });
    yo2 = $("#dashboard2").yoDashboard({
        title: "System Memory",
        showRefreshButton: true,
        showNextPreButton: false,
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            harddiskDetails(div_obj.attr("id"));
            return true;
        },
        showTabOption: false,
        height: "200px"
    });
    yo3 = $("#dashboard4").yoDashboard({
        title: "System CPU Utilization",
        showRefreshButton: true,
        showNextPreButton: false,
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            proDetails(div_obj.attr("id"))
            return true;
        },
        showTabOption: false,
        height: "200px"
    });
    yo4 = $("#dashboard3").yoDashboard({
        title: "System Network Statistics",
        showRefreshButton: true,
        showNextPreButton: false,
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            bandDetails(div_obj.attr("id"))
            return true;
        },
        showTabOption: false,
        height: "200px"
    });
});
function harddiskDetails(div_id) {
    $.ajax({
        type: "get",
        url: "system_harddisk_details.py",
        cache: false,
        success: function (result) {
            // total,free,available,used
            result = result.split(",");
            $("#sys_memory").html("Total: " + result[0] + "GB Free: " + result[1] + "GB<br/>Unused: " + result[2] + "GB Used: " + result[3] + "GB");
            var used = parseFloat(result[3]) * 100.0 / parseFloat(result[0]);
            var unused = parseFloat(result[2]) * 100.0 / parseFloat(result[0]);
            var free = 100 - (used + unused);
            chart1 && chart1.destroy();
            chart1 = null;
            chart1 = new Highcharts.Chart({
                chart: {
                    renderTo: div_id,
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false
                },
                title: {
                    text: ''
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
                            ['Used', used],
                            ['Unused', unused],
                            ['Free', free]
                        ]
                    }
                ]
            });
            $.yoDashboard.hideLoading(yo2);
        }
    });
}

function systemUptime() {
    $.ajax({
        type: "get",
        url: "system_uptime.py",
        cache: false,
        success: function (result) {
            $("#sys_uptime").html(result);
        }
    });
}
function ramDetails(div_id) {
    $.ajax({
        type: "get",
        url: "system_ram.py",
        cache: false,
        success: function (result) {
            // total,free,available,used
            result = result.split(",");
            usedmemory = parseFloat(result[0]);
            totalmemory = parseFloat(result[0]) + parseFloat(result[1]);
            $("#sys_ram").html((usedmemory < 1024 ? usedmemory + " MB" : parseFloat(usedmemory / 1024.0).toFixed(2) + " GB") + " (<span id=\"ramUsage\">" + parseFloat(usedmemory * 100 / totalmemory).toFixed(2) + "</span> %) of " + (totalmemory < 1024 ? totalmemory + " MB" : parseFloat(totalmemory / 1024.0).toFixed(2) + " GB"))

            var used = usedmemory * 100.0 / totalmemory;
            var free = 100 - used;
            chart2 && chart2.destroy();
            chart2 = null;
            chart2 = new Highcharts.Chart({
                chart: {
                    renderTo: div_id,
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false
                },
                title: {
                    text: ''
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
                            ['Used', used],
                            ['Free', free]
                        ]
                    }
                ]
            });
            $.yoDashboard.hideLoading(yo1);
        }
    });
}
function convertUTC2IST(timestamp) {
    var offsetIST = 5.5;
    var d = new Date(timestamp);
    var istDateTime = new Date(d.getTime() + ((offsetIST * 60) * 60000));
    return istDateTime.getTime();
}
function proDetails(div_id) {
    $.ajax({
        type: "get",
        url: "system_processor_details.py?total=12",
        cache: false,
        success: function (result) {
            var cpuState = "";
            cpuState += String(result.length) + " CPU" + (result.length > 1 && "s" || "");
            cpuState += " ("
            for (var i = 0; i < result.length; i++) {
                if (i > 0)
                    cpuState += " ";
                cpuState += "" + String(result[i]["name"]) + ": " + parseFloat(result[i]["data"][result[i]["data"].length - 1]["y"]).toFixed(2) + "%"
            }
            cpuState += ")"
            $("#cpu_usage").html(cpuState);
            // Ram Graph
            chart3SetInterval && clearInterval(chart3SetInterval);
            chart3 && chart3.destroy();
            chart3 = null;
            chart3 = new Highcharts.Chart({
                global: {
                    useUTC: false
                },
                chart: {
                    renderTo: div_id,
                    defaultSeriesType: 'areaspline',
                    marginRight: 20,
                    animation: {
                        duration: 1000
                    },
                    events: {
                        load: function () {

                            // set up the updating of the chart each second
                            var series = this.series;
                            chart3SetInterval = setInterval(function () {
                                $.ajax({
                                    type: "get",
                                    url: "system_processor_details.py?total=1",
                                    cache: false,
                                    success: function (result) {
                                        var cpuState = "";
                                        cpuState += String(result.length) + " CPU" + (result.length > 1 && "s" || "");
                                        cpuState += " ("
                                        for (var i = 0; i < result.length; i++) {
                                            if (i > 0)
                                                cpuState += " ";
                                            cpuState += "" + String(result[i]["name"]) + ": " + parseFloat(result[i]["data"][result[i]["data"].length - 1]["y"]).toFixed(2) + "%"
                                        }
                                        cpuState += ")"
                                        $("#cpu_usage").html(cpuState);
                                        if (result.length == series.length) {
                                            for (var i = 0; i < series.length; i++) {
                                                if (result[i].data.length > 0)
                                                    series[i].addPoint([result[i]["data"][0]["x"], result[i]["data"][0]["y"]], true, true);
                                            }
                                            /*x = res.processor[0].x;
                                             y = res.processor[0].y
                                             $("#cpu_usage").html(parseFloat(y).toFixed(2) + " %");
                                             series.addPoint([x, y], true, true);*/
                                        }
                                    }
                                });
                            }, 10000);
                        }
                    }
                },
                title: {
                    text: ''
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 100,
                    labels: {
                        formatter: function () {
                            //var monthStr = Highcharts.dateFormat('%b', this.value);
                            //var firstLetter = monthStr.substring(0, 1);
                            //return firstLetter;
                            return Highcharts.dateFormat('%H:%M:%S', this.value);
                        }
                    }
                },
                yAxis: {
                    title: {
                        text: 'CPU Usage %'
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
                            Highcharts.dateFormat('%H:%M:%S', this.x) + '<br/>' +
                            Highcharts.numberFormat(this.y, 2) + " %";
                    }
                },
                legend: {
                    enabled: true
                },
                exporting: {
                    enabled: false
                },
                series: result
            });
            $.yoDashboard.hideLoading(yo3);
        }
    });
}
function bandDetails(div_id) {
    $.ajax({
        type: "get",
        url: "system_bandwidth_details.py?total=12",
        cache: false,
        success: function (result) {
            var bandState = "";
            for (var i = 0; i < result.length; i++) {
                if (i > 0)
                    bandState += " ";
                bandState += "" + String(result[i]["name"]) + ": " + parseFloat(result[i]["data"][result[i]["data"].length - 1]["y"]).toFixed(2) + " KiB/s"
            }
            $("#band_usage").html(bandState);
            // Bandwidth Graph
            chart4SetInterval && clearInterval(chart4SetInterval);
            chart4 && chart4.destroy();
            chart4 = null;
            chart4 = new Highcharts.Chart({
                global: {
                    useUTC: false
                },
                chart: {
                    renderTo: div_id,
                    defaultSeriesType: 'spline',
                    marginRight: 20,
                    animation: {
                        duration: 1000
                    },
                    events: {
                        load: function () {

                            // set up the updating of the chart each second
                            var series = this.series;
                            chart4SetInterval = setInterval(function () {
                                $.ajax({
                                    type: "get",
                                    url: "system_bandwidth_details.py?total=1",
                                    cache: false,
                                    success: function (result) {
                                        if (result.length == series.length) {
                                            var bandState = "";
                                            for (var i = 0; i < result.length; i++) {
                                                if (i > 0)
                                                    bandState += " ";
                                                bandState += "" + String(result[i]["name"]) + ": " + parseFloat(result[i]["data"][result[i]["data"].length - 1]["y"]).toFixed(2) + " KiB/s"
                                            }
                                            $("#band_usage").html(bandState);
                                            for (var i = 0; i < series.length; i++) {
                                                if (result[i].data.length > 0)
                                                    series[i].addPoint([result[i]["data"][0]["x"], result[i]["data"][0]["y"]], true, true);
                                            }
                                            /*x = res.processor[0].x;
                                             y = res.processor[0].y
                                             $("#cpu_usage").html(parseFloat(y).toFixed(2) + " %");
                                             series.addPoint([x, y], true, true);*/
                                        }
                                    }
                                });
                            }, 10000);
                        }
                    }
                },
                title: {
                    text: ''
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 100,
                    labels: {
                        formatter: function () {
                            //var monthStr = Highcharts.dateFormat('%b', this.value);
                            //var firstLetter = monthStr.substring(0, 1);
                            //return firstLetter;
                            return Highcharts.dateFormat('%H:%M:%S', this.value);
                        }
                    }
                },
                yAxis: {
                    title: {
                        text: 'KiB/sec'
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
                            Highcharts.dateFormat('%H:%M:%S', this.x) + '<br/>' +
                            Highcharts.numberFormat(this.y, 2) + " KiB/sec";
                    }
                },
                legend: {
                    enabled: true
                },
                exporting: {
                    enabled: false
                },
                series: result
            });
            $.yoDashboard.hideLoading(yo4);
        }
    });
}
