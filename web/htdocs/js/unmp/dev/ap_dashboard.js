var totalInterface = 0;
var eth0 = false;
var br0 = false;
var ath0 = false;
var ath1 = false;
var ath2 = false;
var ath3 = false;
var ath4 = false;
var ath5 = false;
var ath6 = false;
var ath7 = false;
var reload_time = 60000;
var selectedAPIp = 0;
var first = 0;
var second = 0;
$(function () {
    createAPTable();
    reload_time = parseInt($("#refresh_time").val()) * 60000;
});
function createAPTable() {
    eth0 = false;
    br0 = false;
    ath0 = false;
    ath1 = false;
    ath2 = false;
    ath3 = false;
    ath4 = false;
    ath5 = false;
    ath6 = false;
    ath7 = false;
    $.ajax({
        type: "get",
        url: "access_point_details_table.py",
        success: function (result) {
            result = eval("(" + result + ")");
            var table = $("<table/>").addClass("addform");
            var tr = $("<tr/>");
            //tr.append($("<th/>").text("S.No."));
            tr.append($("<th/>").text("Access Point"));
            //tr.append($("<th/>").text("Uptime"));
            //tr.append($("<th/>").text("Conn. User"));
            tr.append($("<th class='eth0'/>").text("eth0 (tx)"));
            tr.append($("<th class='eth0'/>").text("eth0 (rx)"));
            tr.append($("<th class='br0'/>").text("br0 (tx)"));
            tr.append($("<th class='br0'/>").text("br0 (rx)"));
            tr.append($("<th class='ath0'/>").text("ath0 (tx)"));
            tr.append($("<th class='ath0'/>").text("ath0 (rx)"));
            tr.append($("<th class='ath1'/>").text("ath1 (tx)"));
            tr.append($("<th class='ath1'/>").text("ath1 (rx)"));
            tr.append($("<th class='ath2'/>").text("ath2 (tx)"));
            tr.append($("<th class='ath2'/>").text("ath2 (rx)"));
            tr.append($("<th class='ath3'/>").text("ath3 (tx)"));
            tr.append($("<th class='ath3'/>").text("ath3 (rx)"));
            tr.append($("<th class='ath4'/>").text("ath4 (tx)"));
            tr.append($("<th class='ath4'/>").text("ath4 (rx)"));
            tr.append($("<th class='ath5'/>").text("ath5 (tx)"));
            tr.append($("<th class='ath5'/>").text("ath5 (rx)"));
            tr.append($("<th class='ath6'/>").text("ath6 (tx)"));
            tr.append($("<th class='ath6'/>").text("ath6 (rx)"));
            tr.append($("<th class='ath7'/>").text("ath7 (tx)"));
            tr.append($("<th class='ath7'/>").text("ath7 (rx)"));
            table.append(tr);
            for (var i = 0; i < result.apId.length; i++) {
                if (i == 0)
                    selectedAPIp = result.ap[i];
                tr = $("<tr>");
                if (i % 2 != 0)
                    tr.addClass("even");
                //tr.append($("<td/>").text(i));
                tr.append($("<td/>").html("<a href=\"javascript:getAPInterface('" + result.ap[i] + "',1)\">" + result.ap[i] + "</a>"));
                //tr.append($("<td/>").text(result.upTime[i]));
                //tr.append($("<td/>").text(result.connectedUser[i]));
                if (result.interfaces[i].eth0 != undefined) {
                    tr.append($("<td class='eth0'/>").text(result.interfaces[i].eth0[0]));
                    tr.append($("<td class='eth0'/>").text(result.interfaces[i].eth0[1]));
                    eth0 = true;
                }
                else {
                    tr.append($("<td class='eth0'/>").text("-"));
                    tr.append($("<td class='eth0'/>").text("-"));
                }
                if (result.interfaces[i].br0 != undefined) {
                    tr.append($("<td class='br0'/>").text(result.interfaces[i].br0[0]));
                    tr.append($("<td class='br0'/>").text(result.interfaces[i].br0[1]));
                    br0 = true;
                }
                else {
                    tr.append($("<td class='br0'/>").text("-"));
                    tr.append($("<td class='br0'/>").text("-"));
                }
                if (result.interfaces[i].ath0 != undefined) {
                    tr.append($("<td class='ath0'/>").text(result.interfaces[i].ath0[0]));
                    tr.append($("<td class='ath0'/>").text(result.interfaces[i].ath0[1]));
                    ath0 = true;
                }
                else {
                    tr.append($("<td class='ath0'/>").text("-"));
                    tr.append($("<td class='ath0'/>").text("-"));
                }
                if (result.interfaces[i].ath1 != undefined) {
                    tr.append($("<td class='ath1'/>").text(result.interfaces[i].ath1[0]));
                    tr.append($("<td class='ath1'/>").text(result.interfaces[i].ath1[1]));
                    ath1 = true;
                }
                else {
                    tr.append($("<td class='ath1'/>").text("-"));
                    tr.append($("<td class='ath1'/>").text("-"));
                }
                if (result.interfaces[i].ath2 != undefined) {
                    tr.append($("<td class='ath2'/>").text(result.interfaces[i].ath2[0]));
                    tr.append($("<td class='ath2'/>").text(result.interfaces[i].ath2[1]));
                    ath2 = true;
                }
                else {
                    tr.append($("<td class='ath2'/>").text("-"));
                    tr.append($("<td class='ath2'/>").text("-"));
                }
                if (result.interfaces[i].ath3 != undefined) {
                    tr.append($("<td class='ath3'/>").text(result.interfaces[i].ath3[0]));
                    tr.append($("<td class='ath3'/>").text(result.interfaces[i].ath3[1]));
                    ath3 = true;
                }
                else {
                    tr.append($("<td class='ath3'/>").text("-"));
                    tr.append($("<td class='ath3'/>").text("-"));
                }
                if (result.interfaces[i].ath4 != undefined) {
                    tr.append($("<td class='ath4'/>").text(result.interfaces[i].ath4[0]));
                    tr.append($("<td class='ath4'/>").text(result.interfaces[i].ath4[1]));
                    ath4 = true;
                }
                else {
                    tr.append($("<td class='ath4'/>").text("-"));
                    tr.append($("<td class='ath4'/>").text("-"));
                }
                if (result.interfaces[i].ath5 != undefined) {
                    tr.append($("<td class='ath5'/>").text(result.interfaces[i].ath5[0]));
                    tr.append($("<td class='ath5'/>").text(result.interfaces[i].ath5[1]));
                    ath5 = true;
                }
                else {
                    tr.append($("<td class='ath5'/>").text("-"));
                    tr.append($("<td class='ath5'/>").text("-"));
                }
                if (result.interfaces[i].ath6 != undefined) {
                    tr.append($("<td class='ath6'/>").text(result.interfaces[i].ath6[0]));
                    tr.append($("<td class='ath6'/>").text(result.interfaces[i].ath6[1]));
                    ath6 = true;
                }
                else {
                    tr.append($("<td class='ath6'/>").text("-"));
                    tr.append($("<td class='ath6'/>").text("-"));
                }
                if (result.interfaces[i].ath7 != undefined) {
                    tr.append($("<td class='ath7'/>").text(result.interfaces[i].ath7[0]));
                    tr.append($("<td class='ath7'/>").text(result.interfaces[i].ath7[1]));
                    ath7 = true;
                }
                else {
                    tr.append($("<td class='ath7'/>").text("-"));
                    tr.append($("<td class='ath7'/>").text("-"));
                }
                table.append(tr);
            }
            tr = $("<tr/>")
            tr.append($("<td colspan='1' style=\"font-size:9px;color:#555;\" />").text("Bandwidth in KB/Sec."));
            tr.append("<td colspan='2' class='eth0'/>");
            tr.append("<td colspan='2' class='br0'/>");
            tr.append("<td colspan='2' class='ath0'/>");
            tr.append("<td colspan='2' class='ath1'/>");
            tr.append("<td colspan='2' class='ath2'/>");
            tr.append("<td colspan='2' class='ath3'/>");
            tr.append("<td colspan='2' class='ath4'/>");
            tr.append("<td colspan='2' class='ath5'/>");
            tr.append("<td colspan='2' class='ath6'/>");
            tr.append("<td colspan='2' class='ath7'/>");
            table.append(tr);
            $("#apTableDiv").html(table);

            if (eth0)
                $(".eth0").show();
            else
                $(".eth0").hide();
            if (br0)
                $(".br0").show();
            else
                $(".br0").hide();
            if (ath0)
                $(".ath0").show();
            else
                $(".ath0").hide();
            if (ath1)
                $(".ath1").show();
            else
                $(".ath1").hide();
            if (ath2)
                $(".ath2").show();
            else
                $(".ath2").hide();
            if (ath3)
                $(".ath3").show();
            else
                $(".ath3").hide();
            if (ath4)
                $(".ath4").show();
            else
                $(".ath4").hide();
            if (ath5)
                $(".ath5").show();
            else
                $(".ath5").hide();
            if (ath6)
                $(".ath6").show();
            else
                $(".ath6").hide();
            if (ath7)
                $(".ath7").show();
            else
                $(".ath7").hide();
            if (first == 0) {
                getAPInterface(selectedAPIp, 0);
                first += 1;
            }
        }
    });
    setTimeout(function () {
        createAPTable();
    }, reload_time);
}
function getAPInterface(apIp, second) {
    selectedAPIp = apIp;
    $("#ap_name").html("Access Point - " + apIp);
    var charteth0;
    var chartbr0;
    var chartath0;
    var chartath1;
    var chartath2;
    var chartath3;
    var chartath4;
    var chartath5;
    var chartath6;
    var chartath7;
    $.ajax({
        type: "post",
        url: "ap_interfaces.py?apIp=" + apIp,
        success: function (result) {
            result = eval("(" + result + ")");
            totalInterface = 0;
            if (result.eth0 != undefined) {
                $(".teth0").show();
                totalInterface += 1;
                var jsonData = result.eth0;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                charteth0 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'eth0',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for eth0',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".teth0").hide();
            }
            if (result.br0 != undefined) {
                $(".tbr0").show();
                totalInterface += 1;
                var jsonData = result.br0;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartbr0 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'br0',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for br0',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tbr0").hide();
            }
            if (result.ath0 != undefined) {
                $(".tath0").show();
                totalInterface += 1;
                var jsonData = result.ath0;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartath0 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'ath0',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for ath0',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tath0").hide();
            }
            if (result.ath1 != undefined) {
                $(".tath1").show();
                totalInterface += 1;
                var jsonData = result.ath1;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartath1 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'ath1',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for ath1',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tath1").hide();
            }
            if (result.ath2 != undefined) {
                $(".tath2").show();
                totalInterface += 1;
                var jsonData = result.ath2;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartath2 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'ath2',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for ath2',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tath2").hide();
            }
            if (result.ath3 != undefined) {
                $(".tath3").show();
                totalInterface += 1;
                var jsonData = result.ath3;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartath3 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'ath3',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for ath3',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tath3").hide();
            }
            if (result.ath4 != undefined) {
                $(".tath4").show();
                totalInterface += 1;
                var jsonData = result.ath4;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartath4 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'ath4',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for ath4',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tath4").hide();
            }
            if (result.ath5 != undefined) {
                $(".tath5").show();
                totalInterface += 1;
                var jsonData = result.ath5;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartath5 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'ath5',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for ath5',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tath5").hide();
            }
            if (result.ath6 != undefined) {
                $(".tath6").show();
                totalInterface += 1;
                var jsonData = result.ath6;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartath6 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'ath6',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for ath6',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tath6").hide();
            }
            if (result.ath7 != undefined) {
                $(".tath7").show();
                totalInterface += 1;
                var jsonData = result.ath7;
                var time_x = [];
                var tx_y = [];
                var rx_y = [];
                $.each(jsonData, function (i, dt) {
                    strtime = dt.timestamp.substring(dt.timestamp.lastIndexOf(" "), dt.timestamp.lastIndexOf(":"));
                    time_x.push(strtime);
                    tx_y.push(dt.tx);
                    rx_y.push(dt.rx);
                });
                chartath7 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'ath7',
                        defaultSeriesType: 'line',
                        marginRight: 80,
                        marginBottom: 40,
                        animation: false
                    },
                    title: {
                        text: 'Bandwidth Usage',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'for ath7',
                        x: -20
                    },
                    xAxis: {
                        categories: time_x
                    },
                    yAxis: {
                        title: {
                            text: 'Bandwidth ( KB/sec )'
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
                                this.y + ' KB/sec';
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
            else {
                $(".tath7").hide();
            }
            if (totalInterface == 0) {
                $("#msg").text("No Interface for this Access Point.").show();
            }
        }
    });
    $.ajax({
        type: "get",
        url: "get_uptime_connected_client.py?ap_ip=" + selectedAPIp,
        success: function (result) {
            result = eval("(" + result + ")");
            $("#ap_details").html("Uptime: " + (result.uptime ? result.uptime : "Down") + " | Connected Clients: " + (result.clients ? result.clients : 0))
        }
    });
    if (second == 0) {
        setTimeout(function () {
            getAPInterface(selectedAPIp, 0);
        }, reload_time);
    }
    //numberOfConnectedUser(apIp);
}
