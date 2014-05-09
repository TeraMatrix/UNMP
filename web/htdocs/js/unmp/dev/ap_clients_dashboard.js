var reload_time = 60000;
var chart1;
var chart2;
$(function () {
    reload_time = parseInt($("#refresh_time").val()) * 60000;
    getOverAllBandwidth()
    setTimeout(function () {
        apConnectedClients();
    }, reload_time);
})
function getOverAllBandwidth() {
    date = new Date();
    date.setMinutes(date.getMinutes() - 60);
    $.ajax({
        type: "get",
        url: "get_overall_bandwidth.py",
        success: function (result) {
            result = eval("(" + result + ")");
            chart1 = new Highcharts.Chart({
                chart: {
                    renderTo: 'bandwidth_graph_div',
                    zoomType: 'x',
                    spacingRight: 20,
                    animation: false
                },
                title: {
                    text: 'Bandwidth Usage'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        '' :
                        ''
                },
                xAxis: {
                    type: 'datetime',
                    maxZoom: 1 * 24 * 3600000, // one days
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    title: {
                        text: 'Bandwidth (KB/sec)'
                    },
                    min: 0.0,
                    startOnTick: false,
                    showFirstLabel: false
                },
                tooltip: {
                    shared: true
                },
                legend: {
                    enabled: false
                },
                plotOptions: {
                    area: {
                        fillColor: {
                            linearGradient: [0, 0, 0, 300],
                            stops: [
                                [0, Highcharts.theme.colors[0]],
                                [1, 'rgba(230,250,50,0)']
                            ]
                        },
                        lineWidth: 1,
                        marker: {
                            enabled: false,
                            states: {
                                hover: {
                                    enabled: true,
                                    radius: 5
                                }
                            }
                        },
                        shadow: false,
                        states: {
                            hover: {
                                lineWidth: 1
                            }
                        }
                    }
                },

                series: [
                    {
                        type: 'area',
                        name: 'Tx',
                        pointInterval: 60 * 1000,
                        pointStart: Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()),
                        data: result.tx
                    },
                    {
                        type: 'area',
                        name: 'Rx',
                        pointInterval: 60 * 1000,
                        pointStart: Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()),
                        data: result.rx
                    }
                ]
            });
        }
    });
    setTimeout(function () {
        getOverAllBandwidth();
    }, reload_time);
}
function apConnectedClients() {
    $.ajax({
        type: "post",
        url: "ap_connected_user.py",
        success: function (result) {
            $("#client_div").html(result);
        }
    });
    setTimeout(function () {
        apConnectedClients();
    }, reload_time);
}
