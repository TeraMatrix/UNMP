var $spinLoading = null;
var $spinMainLoading  = null;
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
var graphAjax = {
	type:"get",
	url:"get_graph_data.py",
	data:{}
};
var startStopGraph={
	type:"get",
	url:"live_graph_action.py",
	data:{}
};
var messages = {
	"unknownError":"UNMP Server is busy at the moment, please try again later ",
	"dbError":"UNMP Database Server is busy at the moment, please try again later ",
	"noRecordError":"No such record found",
	"sysError":"UNMP Server is busy at the moment, please try again later",
	"nagiosConfigError":"UNMP Server is busy at the moment, please try again later time.",
	"StartStopError":"UNMP Server is busy at the moment, please try again later"
};
/**
 * Grid theme for Highcharts JS
 * @author Torstein Hønsi
 */

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

function createGraph(graphName,graphFullName)
{
	selectedGraphName = String(graphName);
	selectedStartBtn = $("#" + selectedGraphName + "_start"); 
	selectedStopBtn = $("#" + selectedGraphName + "_stop"); 
	liveChartSetInterval && clearInterval(liveChartSetInterval);
	liveChartObj && liveChartObj.destroy();
	liveChartObj = null;
	$.ajax({
		type:graphAjax.type,
		url:graphAjax.url,
		data:$.extend({
				"graph_name":String(selectedGraphName),
				"device_type":hostObj["device_type"],
				"ip_address":hostObj["ip_address"],
				"host_id":hostObj["host_id"],
				"total":15
				},graphAjax.data),
		cache:false,
		success:function(result){
			isLive = result["is_live"];
			unit = result["unit"];
			if(isLive == true)
			{
				selectedStartBtn.hide();
				selectedStopBtn.show();
			}
			else
			{
				selectedStartBtn.show();
				selectedStopBtn.hide();
			}
			result = result["data_series"];
			liveChartObj = new Highcharts.Chart({
				global:{
						useUTC:false
					},
				chart: {
					renderTo: String(selectedGraphName) + "_graph_div",
					defaultSeriesType: 'spline',
					marginRight: 120,
					animation: {
						duration: 1000
					},
					events: {
						load: function() {
			
							// set up the updating of the chart each second
							if(isLive==true)
							{
								var series = this.series;
								liveChartSetInterval = setInterval(function() {
									$.ajax({
										type:graphAjax.type,
										url:graphAjax.url,
										cache:false,
										data:$.extend({
											"graph_name":String(selectedGraphName),
											"device_type":hostObj["device_type"],
											"ip_address":hostObj["ip_address"],
											"host_id":hostObj["host_id"],
											"total":1
											},graphAjax.data),
										cache:false,
										success:function(result){
											isLive = result["is_live"];
											if(isLive == true)
											{
												selectedStartBtn.hide();
												selectedStopBtn.show();
											}
											else
											{
												selectedStartBtn.show();
												selectedStopBtn.hide();
												liveChartSetInterval && clearInterval(liveChartSetInterval);
											}
											result = result["data_series"];
											if(result.length == series.length)
											{
												for(var i=0;i<series.length;i++)
												{
													if(result[i].data.length>0)
														series[i].addPoint([result[i]["data"][0]["x"],result[i]["data"][0]["y"]], true, true);
												}
											}
										}
									});
								}, 60000);
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
						formatter: function() {
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
					plotLines: [{
						value: 0,
						width: 1,
						color: '#808080'
					}]
				},
				tooltip: {
					formatter: function() {
			                return '<b>'+ this.series.name +'</b><br/>'+
							Highcharts.dateFormat('%H:%M:%S', this.x) +'<br/>'+ 
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
		}
	});
}
function hostDetailsTable()
{
	var $table = $("<table/>").addClass("tt-table").attr({"cellspacing":"0", "cellpadding":"0", "width":"100%"});
	var $tr=$("<tr/>");
	$("<td/>").addClass("cell-label").html("Host Alias").appendTo($tr);
	$("<td/>").addClass("cell-info").html(hostObj["host_alias"]).appendTo($tr);
	$("<td/>").addClass("cell-label").html("IP Address").appendTo($tr);
	$("<td/>").addClass("cell-info").html(hostObj["ip_address"]).appendTo($tr);
	$tr.appendTo($table);
	var $tr=$("<tr/>");
	$("<td/>").addClass("cell-label").html("MAC Address").appendTo($tr);
	$("<td/>").addClass("cell-info").html(hostObj["mac_address"]).appendTo($tr);
	$("<td/>").addClass("cell-label").html("Device Type").appendTo($tr);
	$("<td/>").addClass("cell-info").html(hostObj["device_name"]).appendTo($tr);
	$tr.appendTo($table);
	$hostDetailsContainerObj.html("");
	$table.appendTo($hostDetailsContainerObj);
}
function monitoringTabs()
{
	$.ajax({
		type:"get",
		url:"get_live_monitoring_graphs.py",
		cache:false,
		data:{
			"device_type":hostObj["device_type"],
			"ip_address":hostObj["ip_address"],
			"host_id":hostObj["host_id"]
		},
		success:function(result){
			graphObj = result;
			createtabs();
		},
		complete:function(){
			spinStop($spinLoading,$spinMainLoading);
		}
	});
}
function createtabs()
{
	var $div = $("<div/>").addClass("yo-tabs");
	var $ul = $("<ul/>");
	var i=0;
	for(graph in graphObj)
	{
		var $divContent = $("<div/>").attr({"id":"content_"+String(i)}).addClass("tab-content");
		var $subDiv = $("<div/>").addClass("form-div").css({"margin-top":"93px","margin-bottom":"0","overflow-y":"scroll"});
		var $controlDiv = $("<div/>").addClass("live-controller");
		var $graphDiv = $("<div/>").show().attr({"id":String(graph) + "_graph_div"}).css({"margin":"15px","height":"300px"});
		var $li = $("<li/>");//<a %shref=\"#content_%s\" id=\"%s_tab\">%s</a>
		var $a = $("<a/>").attr({"href":"#content_"+ String(i),"id":graph+"_tab"}).html(graphObj[graph]["name"]);
		$a.data({"graph_name":String(graph)});
		$a.click(function(){
			var $this = $(this);
			createGraph($this.data("graph_name"),$this.text());
		});
		$a.appendTo($li);
		$li.appendTo($ul);
		
                var $btnDiv = $("<div/>").addClass("bar-btn-div").css({"margin":0});
                var $startBtn = $("<a/>").addClass("ltft").attr({"title":"Start","id":String(graph)+"_start"}).hide().tipsy({gravity: 'n'});
                $("<span/>").addClass("start").appendTo($startBtn);
                $startBtn.click(function(e){
                	e.stopPropagation();
			$.ajax({
				type:startStopGraph.type,
				url:startStopGraph.url,
				data:$.extend({
						"graph_name":String(selectedGraphName),
						"device_type":hostObj["device_type"],
						"ip_address":hostObj["ip_address"],
						"host_id":hostObj["host_id"],
						"action":"start",
						"community":hostObj["read_community"],
						"port":hostObj["get_set_port"],
						"version":hostObj["snmp_version"]
						},startStopGraph.data),
				cache:false,
				success:function(result){
					if(result != "0")
					{
						$().toastmessage('showErrorToast', messages["StartStopError"]);
					}
					else
					{
						createGraph(String(selectedGraphName),$("a#"+ String(selectedGraphName) +"_tab").text());
						selectedStartBtn.hide();
						selectedStopBtn.show();
					}
				}
			});
		});
                $startBtn.appendTo($btnDiv);
                
                var $stopBtn = $("<a/>").addClass("ltft").attr({"title":"Stop","id":String(graph)+"_stop"}).hide().tipsy({gravity: 'n'});;
                $("<span/>").addClass("stop").appendTo($stopBtn);
                $stopBtn.click(function(e){
	                e.stopPropagation();
			$.ajax({
				type:startStopGraph.type,
				url:startStopGraph.url,
				data:$.extend({
						"graph_name":String(selectedGraphName),
						"device_type":hostObj["device_type"],
						"ip_address":hostObj["ip_address"],
						"host_id":hostObj["host_id"],
						"action":"stop",
						"community":hostObj["read_community"],
						"port":hostObj["get_set_port"],
						"version":hostObj["snmp_version"]
						},startStopGraph.data),
				cache:false,
				success:function(result){
					if(result != "0")
					{
						$().toastmessage('showErrorToast', messages["StartStopError"]);
					}
					else
					{
						liveChartSetInterval && clearInterval(liveChartSetInterval);
						selectedStartBtn.show();
						selectedStopBtn.hide();
					}
				}
			});
		});
                $stopBtn.appendTo($btnDiv);
                
                /*
		var $startBtn = $("<button/>").attr({"id":String(graph)+"_start","type":"button"}).addClass("yo-small").addClass("yo-button").hide();
		$("<span/>").addClass("play").html("Start").appendTo($startBtn);
		$startBtn.click(function(){
			$.ajax({
				type:startStopGraph.type,
				url:startStopGraph.url,
				data:$.extend({
						"graph_name":String(selectedGraphName),
						"device_type":hostObj["device_type"],
						"ip_address":hostObj["ip_address"],
						"host_id":hostObj["host_id"],
						"action":"start",
						"community":hostObj["read_community"],
						"port":hostObj["get_set_port"],
						"version":hostObj["snmp_version"]
						},startStopGraph.data),
				cache:false,
				success:function(result){
					if(result != "0")
					{
						$().toastmessage('showErrorToast', messages["StartStopError"]);
					}
					else
					{
						createGraph(String(selectedGraphName),$("a#"+ String(selectedGraphName) +"_tab").text());
						selectedStartBtn.hide();
						selectedStopBtn.show();
					}
				}
			});
		});
		
		var $stopBtn = $("<button/>").attr({"id":String(graph)+"_stop","type":"button"}).addClass("yo-small").addClass("yo-button").hide();
		$("<span/>").addClass("stop").html("Stop").appendTo($stopBtn);
		$stopBtn.click(function(){
			$.ajax({
				type:startStopGraph.type,
				url:startStopGraph.url,
				data:$.extend({
						"graph_name":String(selectedGraphName),
						"device_type":hostObj["device_type"],
						"ip_address":hostObj["ip_address"],
						"host_id":hostObj["host_id"],
						"action":"stop",
						"community":hostObj["read_community"],
						"port":hostObj["get_set_port"],
						"version":hostObj["snmp_version"]
						},startStopGraph.data),
				cache:false,
				success:function(result){
					if(result != "0")
					{
						$().toastmessage('showErrorToast', messages["StartStopError"]);
					}
					else
					{
						liveChartSetInterval && clearInterval(liveChartSetInterval);
						selectedStartBtn.show();
						selectedStopBtn.hide();
					}
				}
			});
		});
		*/
		if(graphObj[graph]["live_status"])
		{
			$stopBtn.show();
		}
		else
		{
			$startBtn.show();
		}
		//$stopBtn.appendTo($controlDiv);
		//$startBtn.appendTo($controlDiv);
		$btnDiv.appendTo($controlDiv);
		$controlDiv.appendTo($subDiv);
		$graphDiv.appendTo($subDiv);
		$subDiv.appendTo($divContent);
		$divContent.appendTo($div);
		i++;
	}
	if(i!=0)
	{
		$div.appendTo($liveMonitoringContainer);
		$ul.appendTo($div);
		$div.yoTabs();
	}
	else
	{
		$("<div class=\"error\">Live monitoring configuration doesn't exist for this device.</div>").appendTo($liveMonitoringContainer);
	}
}
$(function(){
	// spin loading object
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	
	$hostDetailsContainerObj = $("#host_details");
	$liveMonitoringContainer = $("#live_monitoring");
	hostId = $("#host_id").val();
	setTimeout(function()
	{
		if(tactical_call != null)
		{
			clearTimeout(tactical_call);
		}
	},25000);
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"get_host_by_id.py?host_id=" + hostId,
		cache:false,
		success:function(result){
			try
			{
				result = eval("(" + result + ")");
			}
			catch(err)
			{
				result = {success:1,msg:"unknownError"};
			}
			if(result.success == 0)
			{
				hostObj = result.result; 
				hostDetailsTable();
				monitoringTabs();
			}
			else
			{
				$().toastmessage('showErrorToast', messages[result.msg]);
			}
		}
	});
});
