var $spinLoading = null;
var $spinMainLoading = null;
var hostId = null;
var hostObj = null;
var graphObj = null;
var $hostDetailsContainerObj = null;
var isLive = null;
var unit = null;
var $liveMonitoringContainer = null;
var liveChartObj = null;
var liveChartSetInterval = null;
var selectedGraphName = null;
var selectedStartBtn = null;
var selectedStopBtn = null;
var rrdGraph = {};
var isSaveSetting = false;
var $settingDiv = null;
var $liveMonitoringDiv = null;
var $hostDetailsDiv = null;
var $dataTableObj = null;
var tableI = 0;
var $form = {
    "name": null,
    "graph_name_div": null,
    "desc": null,
    "is_localhost": null,
    "is_snmp": null,
    "oid_table": null,
    "row_index": null,
    "row": null,
    "column_index": null,
    "column": null,
    "ds_name": null,
    "ds_type": null,
    "ds_heartbeat": null,
    "ds_lower_limit": null,
    "ds_upper_limit": null,
    "unit": null,
    "rra_cf": null,
    "rra_dataset": null,
    "rrd_file_name": null,
    "timestamp": null,
    "show_ds": null,
    "dyn_ds_name": null,
    "get_dyn_name": null,
    "unreachable_value": null,
    "rrd_table_div": null,
    "rra_table_div": null,
    "rrd_size": null,
    "rrd_step": 0,
    "total_rra": 0
};
var graphAjax = {
    type: "get",
    url: "get_graph_data.py",
    data: {}
};
var startStopGraph = {
    type: "get",
    url: "live_graph_action.py",
    data: {}
};
var messages = {
    "unknownError": "UNMP Server is busy at the moment, please try again later",
    "dbError": "UNMP Database Server is busy at the moment, please try again later",
    "noRecordError": "No such record found",
    "sysError": "UNMP Server is busy at the moment, please try again later",
    "nagiosConfigError": "UNMP Server is busy at the moment, please try again later time.",
    "StartStopError": "UNMP Server is busy at the moment, please try again later",
    "validationError": "Invalid configuration values are entered, please recheck",
    "saveSettingSuccess": "Live Monitoring configuration settings saved successfully",
    "loadDefaultConfig": "Default configuration loaded successfully",
    "excelFileDownload": "Excel report downloaded successfully",
    "csvFileDownload": "CSV report downloaded successfully",
    "RRDFileCantDelete": "Old configuration could not delete"
};
Array.prototype.getUnique = function () {
    var u = {}, a = [];
    for (var i = 0, l = this.length; i < l; ++i) {
        if (u.hasOwnProperty(this[i])) {
            continue;
        }
        a.push(this[i]);
        u[this[i]] = 1;
    }
    return a;
}
/**
 * Grid theme for Highcharts JS
 * @author Torstein Hønsi
 */

Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

Highcharts.theme = {
    colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
    chart: {
        backgroundColor: {
            linearGradient: [0, 0, 500, 500],
            stops: [
                [0, 'rgb(255, 255, 255)'],
                [1, 'rgb(255, 255, 255)']
            ]
        },
        borderColor: '#FFF',
        borderWidth: 1,
        plotBackgroundColor: 'rgba(255, 255, 255, .9)',
        plotShadow: true,
        plotBorderWidth: 1
    },
    title: {
        style: {
            color: '#000',
            font: 'bold 16px "Trebuchet MS", Verdana, sans-serif'
        }
    },
    subtitle: {
        style: {
            color: '#666666',
            font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'
        }
    },
    xAxis: {
        gridLineWidth: 1,
        lineColor: '#000',
        tickColor: '#000',
        labels: {
            style: {
                color: '#000',
                font: '11px Trebuchet MS, Verdana, sans-serif'
            }
        },
        title: {
            style: {
                color: '#333',
                fontWeight: 'bold',
                fontSize: '12px',
                fontFamily: 'Trebuchet MS, Verdana, sans-serif'

            }
        }
    },
    yAxis: {
        minorTickInterval: 'auto',
        lineColor: '#000',
        lineWidth: 1,
        tickWidth: 1,
        tickColor: '#000',
        labels: {
            style: {
                color: '#000',
                font: '11px Trebuchet MS, Verdana, sans-serif'
            }
        },
        title: {
            style: {
                color: '#333',
                fontWeight: 'bold',
                fontSize: '12px',
                fontFamily: 'Trebuchet MS, Verdana, sans-serif'
            }
        }
    },
    legend: {
        itemStyle: {
            font: '9pt Trebuchet MS, Verdana, sans-serif',
            color: 'black'

        },
        itemHoverStyle: {
            color: '#039'
        },
        itemHiddenStyle: {
            color: 'gray'
        }
    },
    labels: {
        style: {
            color: '#99b'
        }
    }
};

// Apply the theme
var highchartsOptions = Highcharts.setOptions(Highcharts.theme);
function createTable(selectedGraphName, headData, data) {
    $dataTableObj = $("#" + String(selectedGraphName) + "_table_div").dataTable({
        "bDestroy": true,
        "bJQueryUI": true,
        "bProcessing": true,
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "bStateSave": false,
        "aaData": data,
        "oLanguage": {
            "sInfo": "_START_ - _END_ of _TOTAL_",
            "sInfoEmpty": "0 - 0 of 0",
            "sInfoFiltered": "(of _MAX_)"
        },
        "aoColumns": headData
    });
    $dataTableObj.fnSort([
        [0, 'desc']
    ]);
}
function createGraph(graphName, graphFullName) {
    selectedGraphName = String(graphName);
    selectedStartBtn = $("#" + selectedGraphName + "_start");
    selectedStopBtn = $("#" + selectedGraphName + "_stop");
    liveChartSetInterval && clearInterval(liveChartSetInterval);
    liveChartObj && liveChartObj.destroy();
    liveChartObj = null;
    var recCfValue = $("#" + String(graphName) + "_select").val().split(",");
    $.ajax({
        type: graphAjax.type,
        url: graphAjax.url,
        data: $.extend({
            "graph_name": String(selectedGraphName),
            "device_type": hostObj["device_type"],
            "ip_address": hostObj["ip_address"],
            "host_id": hostObj["host_id"],
            "total": 15,
            "resolution": recCfValue[0],
            "cf": recCfValue[1]
        }, graphAjax.data),
        cache: false,
        success: function (result) {
            isLive = result["is_live"];
            unit = result["unit"];
            if (isLive == true) {
                selectedStartBtn.hide();
                selectedStopBtn.show();
            }
            else {
                selectedStartBtn.show();
                selectedStopBtn.hide();
            }
            result = result["data_series"];
            liveChartObj = new Highcharts.Chart({
                chart: {
                    renderTo: String(selectedGraphName) + "_graph_div",
                    defaultSeriesType: 'spline',
                    marginRight: 120,
                    animation: {
                        duration: 1000
                    },
                    events: {
                        load: function () {

                            // set up the updating of the chart each second
                            if (isLive == true) {
                                var series = this.series;
                                liveChartSetInterval = setInterval(function () {
                                    $.ajax({
                                        type: graphAjax.type,
                                        url: graphAjax.url,
//                                        cache: false,
                                        data: $.extend({
                                            "graph_name": String(selectedGraphName),
                                            "device_type": hostObj["device_type"],
                                            "ip_address": hostObj["ip_address"],
                                            "host_id": hostObj["host_id"],
                                            "total": 1,
                                            "resolution": recCfValue[0],
                                            "cf": recCfValue[1]
                                        }, graphAjax.data),
                                        cache: false,
                                        success: function (result) {
                                            isLive = result["is_live"];
                                            if (isLive == true) {
                                                selectedStartBtn.hide();
                                                selectedStopBtn.show();
                                            }
                                            else {
                                                selectedStartBtn.show();
                                                selectedStopBtn.hide();
                                                liveChartSetInterval && clearInterval(liveChartSetInterval);
                                            }
                                            // add new row in table
                                            //result = {"is_live": true, "data_series": [{"data": [{"y": -26.082489800000001, "x": 1341829160000}], "name": "link1"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link2"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link3"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link4"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link5"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link6"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link7"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link8"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link9"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link10"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link11"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link12"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link13"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link14"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link15"}, {"data": [{"y": 0.0, "x": 1341829160000}], "name": "link16"}], "success": 0, "unit": "dBm"}
                                            var success = result["success"];
                                            result = result["data_series"];
                                            if (success != undefined && success == 0) {
                                                var newData = [];
                                                for (var i = 0; i < result.length; i++) {
                                                    for (var j = 0; j < result[i]["data"].length; j++) {
                                                        if (i == 0) {
                                                            newData[newData.length] = [];
                                                            newData[j][newData[j].length] = String(tableI);
                                                            var tDate = new Date(result[i]["data"][j]["x"]);
                                                            newData[j][newData[j].length] = timestampFormat(tDate);
                                                            tableI++;
                                                        }
                                                        newData[j][newData[j].length] = result[i]["data"][j]["y"] == null && "-" || result[i]["data"][j]["y"].toFixed(2);
                                                    }
                                                }
                                                $dataTableObj.fnAddData(newData);
                                            }

                                            if (result.length == series.length) {
                                                for (var i = 0; i < series.length; i++) {
                                                    if (result[i].data.length > 0)
                                                        series[i].addPoint([result[i]["data"][0]["x"], result[i]["data"][0]["y"]], true, true);
                                                }
                                            }
                                        }
                                    });
                                }, parseInt($("#" + String(graphName) + "_select").val().split(",")[0]) * 1000);
                            }
                        }
                    }
                },
                title: {
                    text: String(graphFullName)
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
                        text: String(unit)
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
                            Highcharts.numberFormat(this.y) + " " + String(unit);
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
            // create table
            /*
             result=[{"data": [{"y": 0, "x": 1341061911000.0}, {"y": 0, "x": 1341061971000.0}, {"y": 0, "x": 1341062031000.0}, {"y": 0, "x": 1341062091000.0}, {"y": 0, "x": 1341062151000.0}, {"y": 0, "x": 1341062211000.0}, {"y": 0, "x": 1341062271000.0}, {"y": 0, "x": 1341062331000.0}, {"y": 0, "x": 1341062391000.0}, {"y": 0, "x": 1341062451000.0}, {"y": 0, "x": 1341062511000.0}, {"y": 0, "x": 1341062571000.0}, {"y": 0, "x": 1341062631000.0}, {"y": 0, "x": 1341062691000.0}, {"y": 0, "x": 1341062751000.0}], "name": "CRC"}, {"data": [{"y": 0, "x": 1341061911000.0}, {"y": 0, "x": 1341061971000.0}, {"y": 0, "x": 1341062031000.0}, {"y": 0, "x": 1341062091000.0}, {"y": 0, "x": 1341062151000.0}, {"y": 0, "x": 1341062211000.0}, {"y": 0, "x": 1341062271000.0}, {"y": 0, "x": 1341062331000.0}, {"y": 0, "x": 1341062391000.0}, {"y": 0, "x": 1341062451000.0}, {"y": 0, "x": 1341062511000.0}, {"y": 0, "x": 1341062571000.0}, {"y": 0, "x": 1341062631000.0}, {"y": 0, "x": 1341062691000.0}, {"y": 0, "x": 1341062751000.0}], "name": "PHY"}]

             */
            var data = [];
            var headData = [
                { "sTitle": "S.No.", "sClass": "center", "sWidth": "50px"},
                { "sTitle": "Timestamp", "sClass": "center", "sWidth": "180px"}
            ];
            for (var i = 0; i < result.length; i++) {
                headData[headData.length] = {"sTitle": result[i]["name"], "sClass": "center", "asSorting": ["desc"]};
                tableI = result[i]["data"].length;
                for (var j = 0; j < result[i]["data"].length; j++) {
                    if (i == 0) {
                        data[data.length] = [];
                        data[j][data[j].length] = String(j + 1);
                        var tDate = new Date(result[i]["data"][j]["x"]);
                        data[j][data[j].length] = timestampFormat(tDate);
                    }
                    data[j][data[j].length] = result[i]["data"][j]["y"] == null && "-" || result[i]["data"][j]["y"].toFixed(2);

                }
            }
            createTable(selectedGraphName, headData, data);
        }
    });
}
function timestampFormat(dateObj) {
    var monthNames = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec" ];
    var dateString = "";
    dateString += dateObj.getDate() < 10 && ("0" + dateObj.getDate()) || dateObj.getDate();
    dateString += "-";
    dateString += monthNames[dateObj.getMonth()];
    dateString += "-"
    dateString += dateObj.getFullYear()
    dateString += " "
    dateString += dateObj.getHours() < 10 && ("0" + dateObj.getHours()) || dateObj.getHours();
    dateString += ":"
    dateString += dateObj.getMinutes() < 10 && ("0" + dateObj.getMinutes()) || dateObj.getMinutes();
    dateString += ":"
    dateString += dateObj.getSeconds() < 10 && ("0" + dateObj.getSeconds()) || dateObj.getSeconds();
    return dateString;
}
function hostDetailsTable() {
    var $table = $("<table/>").addClass("tt-table").attr({"cellspacing": "0", "cellpadding": "0", "width": "100%"});
    var $tr = $("<tr/>");
    $("<td/>").addClass("cell-label").html("Host Alias").appendTo($tr);
    $("<td/>").addClass("cell-info").html(hostObj["host_alias"]).appendTo($tr);
    $("<td/>").addClass("cell-label").html("IP Address").appendTo($tr);
    $("<td/>").addClass("cell-info").html(hostObj["ip_address"]).appendTo($tr);
    $tr.appendTo($table);
    var $tr = $("<tr/>");
    $("<td/>").addClass("cell-label").html("MAC Address").appendTo($tr);
    $("<td/>").addClass("cell-info").html(hostObj["mac_address"]).appendTo($tr);
    $("<td/>").addClass("cell-label").html("Device Type").appendTo($tr);
    $("<td/>").addClass("cell-info").html(hostObj["device_name"]).appendTo($tr);
    $tr.appendTo($table);
    $hostDetailsContainerObj.html("");
    $table.appendTo($hostDetailsContainerObj);
}
function monitoringTabs() {
    $.ajax({
        type: "get",
        url: "get_live_monitoring_graphs.py",
        cache: false,
        data: {
            "device_type": hostObj["device_type"],
            "ip_address": hostObj["ip_address"],
            "host_id": hostObj["host_id"]
        },
        success: function (result) {
            graphObj = result;
            createtabs();
        },
        complete: function () {
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}
function createtabs() {
    var $div = $("<div/>").addClass("yo-tabs");
    var $ul = $("<ul/>");
    var graphI = 0;
    for (graph in graphObj) {
        var $divContent = $("<div/>").attr({"id": "content_" + String(graphI)}).addClass("tab-content");
        var $subDiv = $("<div/>").addClass("form-div").css({"margin-top": "93px", "margin-bottom": "0", "overflow-y": "scroll"});
        var $controlDiv = $("<div/>").addClass("live-controller");
        var $graphDiv = $("<div/>").show().attr({"id": String(graph) + "_graph_div"}).css({"margin": "15px", "height": "300px"});
        var $tableDiv = $("<div/>").show().css({"margin": "0px"});

        // create datatable
        var $table = $("<table/>");
        $table.attr({"cellpadding": "0", "cellspacing": "0", "border": "0", "id": String(graph) + "_table_div"});
        $table.addClass("display");
        $table.css({"width": "100%"});
        $table.appendTo($tableDiv);


        var $li = $("<li/>");//<a %shref=\"#content_%s\" id=\"%s_tab\">%s</a>
        var $a = $("<a/>").attr({"href": "#content_" + String(graphI), "id": graph + "_tab"}).html(graphObj[graph]["name"]);
        $a.data({"graph_name": String(graph)});
        $a.click(function () {
            var $this = $(this);
            createGraph($this.data("graph_name"), $this.text());
        });
        $a.appendTo($li);
        $li.appendTo($ul);

        var $btnDiv = $("<div/>").addClass("bar-btn-div").css({"margin": 0});
        var $startBtn = $("<a/>").addClass("ltft").attr({"title": "Start", "id": String(graph) + "_start"}).hide().tipsy({gravity: 'n'});
        $("<span/>").addClass("start").appendTo($startBtn);
        $startBtn.click(function (e) {
            e.stopPropagation();
            $.ajax({
                type: startStopGraph.type,
                url: startStopGraph.url,
                data: $.extend({
                    "graph_name": String(selectedGraphName),
                    "device_type": hostObj["device_type"],
                    "ip_address": hostObj["ip_address"],
                    "host_id": hostObj["host_id"],
                    "action": "start",
                    "community": hostObj["read_community"],
                    "port": hostObj["get_set_port"],
                    "version": hostObj["snmp_version"]
                }, startStopGraph.data),
                cache: false,
                success: function (result) {
                    if (result != "0") {
                        $().toastmessage('showErrorToast', messages["StartStopError"]);
                    }
                    else {
                        createGraph(String(selectedGraphName), $("a#" + String(selectedGraphName) + "_tab").text());
                        selectedStartBtn.hide();
                        selectedStopBtn.show();
                    }
                }
            });
        });
        $startBtn.appendTo($btnDiv);

        var $stopBtn = $("<a/>").addClass("ltft").attr({"title": "Stop", "id": String(graph) + "_stop"}).hide().tipsy({gravity: 'n'});
        ;
        $("<span/>").addClass("stop").appendTo($stopBtn);
        $stopBtn.click(function (e) {
            e.stopPropagation();
            $.ajax({
                type: startStopGraph.type,
                url: startStopGraph.url,
                data: $.extend({
                    "graph_name": String(selectedGraphName),
                    "device_type": hostObj["device_type"],
                    "ip_address": hostObj["ip_address"],
                    "host_id": hostObj["host_id"],
                    "action": "stop",
                    "community": hostObj["read_community"],
                    "port": hostObj["get_set_port"],
                    "version": hostObj["snmp_version"]
                }, startStopGraph.data),
                cache: false,
                success: function (result) {
                    if (result != "0") {
                        $().toastmessage('showErrorToast', messages["StartStopError"]);
                    }
                    else {
                        liveChartSetInterval && clearInterval(liveChartSetInterval);
                        selectedStartBtn.show();
                        selectedStopBtn.hide();
                    }
                }
            });
        });
        $stopBtn.appendTo($btnDiv);

        if (graphObj[graph]["live_status"]) {
            $stopBtn.show();
        }
        else {
            $startBtn.show();
        }
        $btnDiv.appendTo($controlDiv);

        // download excel report
        var $btnDiv = $("<div/>").addClass("bar-btn-div").css({"margin": 0});
        var $excelBtn = $("<a/>").addClass("ltft").attr({"title": "Download excel report", "id": String(graph) + "_excel"}).tipsy({gravity: 'n'});
        $("<span/>").addClass("excel").appendTo($excelBtn);
        $excelBtn.click(function (e) {
            e.stopPropagation();
            var recCfValue = $("#" + String(selectedGraphName) + "_select").val().split(",");
            $.ajax({
                type: "get",
                url: "download_live_monitoring_excel_file.py",
                data: {
                    "graph_name": String(selectedGraphName),
                    "device_type": hostObj["device_type"],
                    "ip_address": hostObj["ip_address"],
                    "host_id": hostObj["host_id"],
                    "resolution": recCfValue[0],
                    "cf": recCfValue[1]
                },
                cache: false,
                success: function (result) {
                    $().toastmessage('showSuccessToast', messages["excelFileDownload"]);
                }
            });
        });
        //$excelBtn.appendTo($btnDiv);
        $btnDiv.appendTo($controlDiv);

        // download csv report
        var $btnDiv = $("<div/>").addClass("bar-btn-div").css({"margin": 0});
        var $csvBtn = $("<a/>").addClass("ltft").attr({"title": "Download CSV report", "id": String(graph) + "_csv"}).tipsy({gravity: 'n'});
        $("<span/>").addClass("csv").appendTo($csvBtn);
        $csvBtn.click(function (e) {
            e.stopPropagation();
            var recCfValue = $("#" + String(selectedGraphName) + "_select").val().split(",");
            $.ajax({
                type: "get",
                url: "download_live_monitoring_csv_file.py",
                data: {
                    "graph_name": String(selectedGraphName),
                    "device_type": hostObj["device_type"],
                    "ip_address": hostObj["ip_address"],
                    "host_id": hostObj["host_id"],
                    "resolution": recCfValue[0],
                    "cf": recCfValue[1]
                },
                cache: false,
                success: function (result) {
                    $().toastmessage('showSuccessToast', messages["csvFileDownload"]);
                }
            });
        });
        //$csvBtn.appendTo($btnDiv);
        $btnDiv.appendTo($controlDiv);

        // Refresh Time
        var $refreshTimeLabel = $("<label/>").html("Refresh Rate: ").css({"float": "left", "line-height": "30px", "padding-right": "5px"});
        $refreshTimeLabel.appendTo($controlDiv);

        var $refreshTimeList = $("<select/>").attr({"id": String(graph) + "_select"}).css({"float": "left", "vertical-align": "middle", "width": "auto", "margin-top": "2px"});
        for (var i = 0; i < graphObj[graph]["rra_dataset"].length; i++) {
            var $option = $("<option/>").val(String(parseInt(graphObj[graph]["rra_dataset"][i]) * parseInt(graphObj[graph]["rrd_step"])) + "," + graphObj[graph]["rra_cf"][i]).text(refreshRateText(parseInt(graphObj[graph]["rra_dataset"][i]) * parseInt(graphObj[graph]["rrd_step"])) + " (" + graphObj[graph]["rra_cf"][i] + ")")
            $option.appendTo($refreshTimeList);
        }
        $refreshTimeList.change(function () {
            createGraph(String(selectedGraphName), $("a#" + String(selectedGraphName) + "_tab").text());
        });
        $refreshTimeList.appendTo($controlDiv);

        $controlDiv.appendTo($subDiv);
        $graphDiv.appendTo($subDiv);
        $tableDiv.appendTo($subDiv)
        $subDiv.appendTo($divContent);
        $divContent.appendTo($div);
        graphI++;
    }
    if (i != 0) {
        $div.appendTo($liveMonitoringContainer);
        $ul.appendTo($div);
        $div.yoTabs();
    }
    else {
        $("<div class=\"error\">Live monitoring configuration doesn't exist for this device.</div>").appendTo($liveMonitoringContainer);
    }
}
/*
 * function: refreshRateText
 * parameter:
 *		time : seconds (integer)
 * description: to convert second to min or hours and return converted time in string (append sec or min or hour automatically).
 * author: Yogesh Kumar
 * Date: 7-July-2012
 */
function refreshRateText(time) {
    try {
        time = parseInt(time)
        if (time < 101) {
            return(String(time) + " sec");
        }
        else if (time < 3600) {
            if (time % 60 == 0) {
                return(String(time / 60) + " min");
            }
            else {
                return(parseFloat(time / 60).toFixed(2) + " min");
            }
        }
        else {
            if (time % 3600 == 0) {
                return(String(time / 3600) + " hour");
            }
            else {
                return(parseFloat(time / 3600).toFixed(2) + " hour");
            }
        }
    }
    catch (err) {
        return(time);
    }
}
function liveSettings() {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax(
        {
            type: "get",
            url: "settings_live_monitoring.py",
            data: {"device_type": hostObj["device_type"]},
            cache: false,
            success: function (result) {
                $settingDiv.show();
                $liveMonitoringDiv.hide();
                $hostDetailsDiv.hide();
                $settingDiv.html(result);
                $("select[name='device_type']").attr("disabled", true);
                bindEventsOnSettingForm();
            },
            error: function () {
                var $errorMsgP = $("<p/>").addClass("error");
                errorMsgP.html("Live Monitoring configuration has to be currupt");
                var $loadDefaultA = $("<a/>").attr({"href": "#"}).click(function (e) {
                    e.preventDefault();
                    loadDefaultSetting();
                    dontSaveSetting();
                });
                $loadDefaultA.appendTo($errorMsgP);
                $settingDiv.html("");
                $errorMsgP.appendTo($settingDiv);
            },
            complete: function () {
                spinStop($spinLoading, $spinMainLoading);
            }
        });
}
function bindEventsOnSettingForm() {
    $form["name"] = graphNameSelectList();
    $form["graph_name_div"] = $("div#graph_name_div");
    $form["graph_name_div"].append($form["name"]);
    $form["desc"] = $("textarea[name='desc']");
    $form["is_localhost"] = $("input[name='is_localhost']");
    $form["is_snmp"] = $("select[name='is_snmp']");
    $form["oid_table"] = $("input[name='oid_table']");
    $form["row_index"] = $("input[name='row_index']");
    $form["row"] = $("input[name='row']");
    $form["column_index"] = $("input[name='column_index']");
    $form["column"] = $("input[name='column']");
    $form["ds_type"] = $("select[name='ds_type']");
    $form["ds_heartbeat"] = $("input[name='ds_heartbeat']");
    $form["ds_lower_limit"] = $("input[name='ds_lower_limit']");
    $form["ds_upper_limit"] = $("input[name='ds_upper_limit']");
    $form["unit"] = $("input[name='unit']");
    $form["ds_name"] = null;
    $form["rra_cf"] = null;
    $form["rra_dataset"] = null;
    $form["rrd_file_name"] = $("input[name='rrd_file_name']");
    $form["timestamp"] = $("input[name='timestamp']");
    $form["show_ds"] = $("select[name='show_ds']");
    $form["dyn_ds_name"] = $("input[name='dyn_ds_name']");
    $form["get_dyn_name"] = $("input[name='get_dyn_name']");
    $form["unreachable_value"] = $("input[name='unreachable_value']");
    $form["rrd_table_div"] = $("div#rrd_table_div");
    $form["rra_table_div"] = $("div#rra_table_div");
    $form["rrd_size"] = $("input[name='rrd_size']");
    $form["rrd_step"] = $("select[name='rrd_step']");
    $form["total_rra"] = $("input[name='total_rra']");

    $form["row"].blur(function () {
        drawDatasetTable();
    });
    $form["column"].blur(function () {
        drawDatasetTable();
    });
    $form["total_rra"].keyup(function () {
        drawRRATable();
    });
    $("#cancel,#close").click(function () {
        dontSaveSetting();
    });
    $("#save").click(function () {
        saveSetting();
        //return false;
    });
    $form["rrd_step"].css("width", "auto");
    $form["rrd_step"].change(function () {
        $form["ds_heartbeat"].val(String(2 * parseInt($(this).val())));
    });
    setDataInSettingForm($form["name"].val());
}
function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        if (charCode == 37 || charCode == 38 || charCode == 39 || charCode == 40 || charCode == 46) {

        }
        else {
            return false;
        }
    return true;
}
function drawRRATable() {
    $form["rra_table_div"].html("");
    var $label = $("<label/>").addClass("lbl").addClass("lbl-big").html("Archive Details");
    $label.appendTo($form["rra_table_div"]);
    var $table = $("<table/>").addClass("yo-table").css({"width": "400px", "border": "1px solid #AAA", "float": "left"});
    var $tr = $("<tr/>").addClass("yo-table-head");
    $("<th/>").html("Function").appendTo($tr);
    $("<th/>").html("Total Dataset").appendTo($tr);
    $tr.appendTo($table);
    var rraCount = parseInt($form["total_rra"].val());
    if (rraCount == NaN || rraCount <= 0) {
        var $tr = $("<tr/>");
        $("<td/>").attr({"colspan": "2"}).html(" No RRA exist ").appendTo($tr)
        $tr.appendTo($table);
        $table.appendTo($form["rra_table_div"]);
    }
    for (var i = 0; i < rraCount; i++) {
        var $tr = $("<tr/>");
        var $rraCf = rraCfSelectList();
        $rraCf.appendTo($("<td/>").appendTo($tr));
        if (graphObj[$form["name"].val()]["rra_cf"][i] != undefined)
            $rraCf.val(graphObj[$form["name"].val()]["rra_cf"][i]);

        $("<input/>").keypress(function (event) {
            return isNumberKey(event);
        }).attr({"name": "rra_dataset", "type": "text"}).css({"width": "30px", "height": "13px", "padding": "3px 3px 4px"}).val(graphObj[$form["name"].val()]["rra_dataset"][i] != undefined ? graphObj[$form["name"].val()]["rra_dataset"][i] : "").appendTo($("<td/>").appendTo($tr));
        $tr.appendTo($table);
    }
    $table.appendTo($form["rra_table_div"]);
    $form["rra_cf"] = $("select[name='rra_cf']");
    $form["rra_dataset"] = $("input[name='rra_dataset']");
}
function rraCfSelectList() {
    var $rraCfList = $("<select>").attr({"name": "rra_cf"}).css({"width": "120px"});
    $("<option>").val("AVERAGE").text("Average").appendTo($rraCfList);
    $("<option>").val("MIN").text("Min").appendTo($rraCfList);
    $("<option>").val("MAX").text("Max").appendTo($rraCfList);
    $("<option>").val("LAST").text("Last").appendTo($rraCfList);
    return $rraCfList;
}
function drawDatasetTable() {
    $form["rrd_table_div"].html("");
    var $label = $("<label/>").addClass("lbl").addClass("lbl-big").html("Dataset");
    $label.appendTo($form["rrd_table_div"]);
    var $table = $("<table/>").addClass("yo-table").css({"width": "400px", "border": "1px solid #AAA", "float": "left"});
    var $tr = $("<tr/>").addClass("yo-table-head");
    $("<th/>").html("Row Index").appendTo($tr);
    $("<th/>").html("Column Index").appendTo($tr);
    $("<th/>").html("Dataset Name").appendTo($tr);
    $tr.appendTo($table);
    var rowCount = parseInt($form["row"].val());
    var columnCount = parseInt($form["column"].val());
    if (rowCount * columnCount == NaN || rowCount * columnCount <= 0) {
        var $tr = $("<tr/>");
        $("<td/>").attr({"colspan": "3"}).html(" No row exist ").appendTo($tr)
        $tr.appendTo($table);
        $table.appendTo($form["rrd_table_div"]);
    }
    var tempRow = new Array();
    var tempColumn = new Array();
    for (var i = 0; i < rowCount; i++) {
        for (var j = 0; j < columnCount; j++) {
            if (graphObj[$form["name"].val()]["row_index"][i] != undefined)
                tempRow[tempRow.length] = graphObj[$form["name"].val()]["row_index"][i];
            else
                tempRow[tempRow.length] = "";
        }
    }
    for (var i = 0; i < rowCount; i++) {
        for (var j = 0; j < columnCount; j++) {
            if (graphObj[$form["name"].val()]["column_index"][j] != undefined)
                tempColumn[tempColumn.length] = graphObj[$form["name"].val()]["column_index"][j];
            else
                tempColumn[tempColumn.length] = "";
        }
    }
    for (var i = 0; i < (rowCount * columnCount); i++) {
        var $tr = $("<tr/>");
        $("<input/>").keypress(function (event) {
            return isNumberKey(event);
        }).attr({"name": "row_index", "type": "text"}).css({"width": "30px", "height": "13px", "padding": "3px 3px 4px"}).val(tempRow[i]).appendTo($("<td/>").appendTo($tr));
        $("<input/>").keypress(function (event) {
            return isNumberKey(event);
        }).attr({"name": "column_index", "type": "text"}).css({"width": "30px", "height": "13px", "padding": "3px 3px 4px"}).val(tempColumn[i]).appendTo($("<td/>").appendTo($tr));

        $("<input/>").attr({"name": "ds_name", "type": "text"}).css({"width": "80px", "height": "13px", "padding": "3px 3px 4px"}).val(graphObj[$form["name"].val()]["ds_name"][i] != undefined ? graphObj[$form["name"].val()]["ds_name"][i] : "").appendTo($("<td/>").appendTo($tr));
        $tr.appendTo($table);
    }
    $table.appendTo($form["rrd_table_div"]);
    $form["row_index"] = $("input[name='row_index']");
    $form["column_index"] = $("input[name='column_index']");
    $form["ds_name"] = $("input[name='ds_name']");
}
function graphNameSelectList() {
    var $graphList = $("<select>").attr({"name": "name"});
    for (var graph in graphObj) {
        $("<option>").val(graph).text(graphObj[graph]["name"]).appendTo($graphList);
    }
    $graphList.change(function () {
        setDataInSettingForm($(this).val());
    });
    return $graphList;
}
function setDataInSettingForm(graph) {
    //graphObj
    $form["desc"].val(graphObj[graph]["desc"]);
    graphObj[graph]["is_localhost"] == 0 ? $form["is_localhost"].attr("checked", false) : $form["is_localhost"].attr("checked", true);

    if (graphObj[graph]["is_snmp"] == true) {
        $form["is_snmp"].val("1");
    }
    else {
        $form["is_snmp"].val("0");
    }
    $form["oid_table"].val(graphObj[graph]["oid_table"]);

    $form["row"].val(graphObj[graph]["row_index"].length);
    $form["column"].val(graphObj[graph]["column_index"].length);
    drawDatasetTable();

    $form["ds_type"].val(graphObj[graph]["ds_type"]);
    $form["ds_heartbeat"].val(graphObj[graph]["ds_heartbeat"]);
    $form["ds_lower_limit"].val(graphObj[graph]["ds_lower_limit"]);
    $form["ds_upper_limit"].val(graphObj[graph]["ds_upper_limit"]);
    $form["unit"].val(graphObj[graph]["unit"]);


    $form["rrd_file_name"].val(graphObj[graph]["rrd_file_name"]);
    $form["timestamp"].val(graphObj[graph]["timestamp"]);
    $form["show_ds"].val(graphObj[graph]["show_ds"]);
    $form["dyn_ds_name"].attr("checked", graphObj[graph]["dyn_ds_name"]);

    $form["get_dyn_name"].val(graphObj[graph]["get_dyn_name"]);
    $form["unreachable_value"].val(graphObj[graph]["unreachable_value"]);
    $form["rrd_step"].val(graphObj[graph]["rrd_step"]);
    $form["rrd_size"].val(parseInt(graphObj[graph]["rrd_size"], 10) / 3600);
    $form["total_rra"].val(graphObj[graph]["rra_cf"].length);
    drawRRATable();

    $form["row"].blur(function () {
        drawDatasetTable();
    });
    $form["column"].blur(function () {
        drawDatasetTable();
    });
    $form["total_rra"].keyup(function () {
        drawRRATable();
    })
}
function saveSetting() {
    var formData = {};
    formData["device_type"] = hostObj["device_type"];
    formData["graph_key"] = $form["name"].val();
    formData["name"] = $form["name"].find("option:selected").text()
    formData["desc"] = $form["desc"].val();
    formData["is_localhost"] = $form["is_localhost"].attr("checked") == true ? 1 : 0;
    formData["is_snmp"] = $form["is_snmp"].val();
    formData["oid_table"] = $form["oid_table"].val();
    var rowIndexArr = $form["row_index"].map(function () {
        return $(this).val();
    }).get();
    formData["row_index"] = String(rowIndexArr.getUnique());
    var columnIndexArr = $form["column_index"].map(function () {
        return $(this).val();
    }).get();
    formData["column_index"] = String(columnIndexArr.getUnique());
    formData["ds_name"] = String($form["ds_name"].map(function () {
        return $(this).val();
    }).get());
    formData["ds_type"] = $form["ds_type"].val();
    formData["ds_heartbeat"] = $form["ds_heartbeat"].val();

    formData["ds_lower_limit"] = $form["ds_lower_limit"].val();
    formData["ds_upper_limit"] = $form["ds_upper_limit"].val();
    formData["unit"] = $form["unit"].val();


    formData["rrd_file_name"] = $form["rrd_file_name"].val();
    formData["timestamp"] = $form["timestamp"].val();

    formData["show_ds"] = $form["show_ds"].val();
    formData["dyn_ds_name"] = $form["dyn_ds_name"].attr("checked") == true ? "True" : "False";

    formData["get_dyn_name"] = $form["get_dyn_name"].val();
    formData["unreachable_value"] = $form["unreachable_value"].val();
    formData["rrd_step"] = $form["rrd_step"].val();
    formData["rra_cf"] = String($form["rra_cf"].map(function () {
        return $(this).val();
    }).get());
    formData["rra_dataset"] = String($form["rra_dataset"].map(function () {
        return $(this).val();
    }).get());
    formData["rrd_size"] = $form["rrd_size"].val();


    // jugaad
    if ($.trim($form["desc"].val()) == "") {
        $.prompt("Graph Description can't leave empty.", {prefix: 'jqismooth'});
        return false;
    }
    else if ($.trim($form["unit"].val()) == "") {
        $.prompt("Unit can't leave empty.", {prefix: 'jqismooth'});
        return false;
    }
    else if ($.trim($form["total_rra"].val()) == "") {
        $.prompt("Total Archive can't leave empty.", {prefix: 'jqismooth'});
        return false;
    }
    else if (parseInt($form["total_rra"].val()) <= 0) {
        $.prompt("Total Archive can't be zero or less then zero.", {prefix: 'jqismooth'});
        return false;
    }
    var isDatasetValid = true;
    $form["rra_dataset"].each(function () {
        if ($(this).val() == "" || parseInt($(this).val()) <= 0) {
            isDatasetValid = false
            return false;
        }
    });
    if (isDatasetValid == false) {
        $.prompt("Total Dataset can't be zero or empty.", {prefix: 'jqismooth'});
        return false;
    }
    // jugaad end
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "save_live_monitoring_config.py",
        data: formData,
        cache: false,
        success: function (result) {
            if (result.success == 0) {
                $().toastmessage('showSuccessToast', messages["saveSettingSuccess"]);
            }
            else {
                if (result.result == undefined) {
                    $().toastmessage('showErrorToast', messages["unknownError"]);
                }
                else {
                    $().toastmessage('showErrorToast', messages[result.msg]);
                }
            }
            //updateCurrentObject(formData);
            isSaveSetting = true;
        },
        error: function () {
            $().toastmessage('showErrorToast', messages["unknownError"]);
        },
        complete: function () {
            spinStop($spinLoading, $spinMainLoading);
        }
    });
    //dontSaveSetting();
}
function updateCurrentObject(formData) {
    var formData = {};
    formData["device_type"] = hostObj["device_type"];
    formData["graph_key"] = $form["name"].val();
    formData["name"] = $form["name"].find("option:selected").text()
    formData["desc"] = $form["desc"].val();
    formData["is_localhost"] = $form["is_localhost"].attr("checked") == true ? 1 : 0;
    formData["is_snmp"] = $form["is_snmp"].val();
    formData["oid_table"] = $form["oid_table"].val();
    var rowIndexArr = $form["row_index"].map(function () {
        return $(this).val();
    }).get();
    formData["row_index"] = String(rowIndexArr.getUnique());
    var columnIndexArr = $form["column_index"].map(function () {
        return $(this).val();
    }).get();
    formData["column_index"] = String(columnIndexArr.getUnique());
    formData["ds_name"] = String($form["ds_name"].map(function () {
        return $(this).val();
    }).get());
    formData["ds_type"] = $form["ds_type"].val();
    formData["ds_heartbeat"] = $form["ds_heartbeat"].val();

    formData["ds_lower_limit"] = $form["ds_lower_limit"].val();
    formData["ds_upper_limit"] = $form["ds_upper_limit"].val();
    formData["unit"] = $form["unit"].val();


    formData["rrd_file_name"] = $form["rrd_file_name"].val();
    formData["timestamp"] = $form["timestamp"].val();

    formData["show_ds"] = $form["show_ds"].val();
    formData["dyn_ds_name"] = $form["dyn_ds_name"].attr("checked") == true ? "True" : "False";

    formData["get_dyn_name"] = $form["get_dyn_name"].val();
    formData["unreachable_value"] = $form["unreachable_value"].val();
    formData["rrd_step"] = $form["rrd_step"].val();
    formData["rra_cf"] = String($form["rra_cf"].map(function () {
        return $(this).val();
    }).get());
    formData["rra_dataset"] = String($form["rra_dataset"].map(function () {
        return $(this).val();
    }).get());
    formData["rrd_size"] = $form["rrd_size"].val();


    // jugaad
    if ($.trim($form["desc"].val()) == "") {
        $.prompt("Graph Description can't leave empty.", {prefix: 'jqismooth'});
        return false;
    }
    else if ($.trim($form["unit"].val()) == "") {
        $.prompt("Unit can't leave empty.", {prefix: 'jqismooth'});
        return false;
    }
    else if ($.trim($form["total_rra"].val()) == "") {
        $.prompt("Total Archive can't leave empty.", {prefix: 'jqismooth'});
        return false;
    }
    else if (parseInt($form["total_rra"].val()) <= 0) {
        $.prompt("Total Archive can't be zero or less then zero.", {prefix: 'jqismooth'});
        return false;
    }
    var isDatasetValid = true;
    $form["rra_dataset"].each(function () {
        if ($(this).val() == "" || parseInt($(this).val()) <= 0) {
            isDatasetValid = false
            return false;
        }
    });
    if (isDatasetValid == false) {
        $.prompt("Total Dataset can't be zero or empty.", {prefix: 'jqismooth'});
        return false;
    }


}
function loadDefaultSetting() {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "load_live_monitoring_default_config.py",
        data: {},
        cache: false,
        success: function (result) {
            if (result.success == 0) {
                $().toastmessage('showSuccessToast', messages["loadDefaultConfig"]);
            }
            else {
                if (result.result == undefined) {
                    $().toastmessage('showErrorToast', messages["unknownError"]);
                }
                else {
                    $().toastmessage('showErrorToast', messages[result.msg]);
                }
            }
        },
        error: function () {
            $().toastmessage('showErrorToast', messages["unknownError"]);
        },
        complete: function () {
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}
function dontSaveSetting() {
    $settingDiv.hide();
    $liveMonitoringDiv.show();
    $hostDetailsDiv.show();
    if (isSaveSetting)
        window.location.reload();
}
$(function () {
    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    $hostDetailsContainerObj = $("#host_details");
    $liveMonitoringContainer = $("#live_monitoring");
    hostId = $("#host_id").val();
    $settingDiv = $("#live_monitoring_setting_div");
    $liveMonitoringDiv = $("#live_monitoring");
    $hostDetailsDiv = $("#host_details");

    setTimeout(function () {
        if (tactical_call != null) {
            clearTimeout(tactical_call);
        }
    }, 25000);
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "get_host_by_id.py?host_id=" + hostId,
        cache: false,
        success: function (result) {
            if (result.success == 0) {
                hostObj = result.result;
                hostDetailsTable();
                monitoringTabs();
            }
            else {
                if (result.result == undefined) {
                    $().toastmessage('showErrorToast', messages["unknownError"]);
                }
                else {
                    $().toastmessage('showErrorToast', messages[result.msg]);
                }
            }
        }
    });
    // page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
//	$("#page_tip").colorbox(
//	{
//		href:"help_live_monitoring.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	});
});
