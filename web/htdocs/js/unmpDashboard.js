var $spinLoading = null;
var $spinMainLoading = null;
var deviceTypeId='';
var graph_type=1;
var limitFlag=1;
var spRecursionVar=null;
var refresh_time=10;// default time for refreshing the hidden datatime value.
var spE1MainObj=null;
var linkObj=null;
var spEndDate='';
var spEndTime='';
var totalSelectedGraph="";
var mozilBrowser=false;

var chart1 = null;
var chart2 = null;
var chart3 = null;
var chart4 = null;

var yo1 = null;
var yo2 = null;
var yo3 = null;
var yo4 = null;

var homeDashboard = null;

$(function(){
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	//$("input[id='current_rept_div']").attr("checked","checked");
	//refresh_time=$("#sp_refresh_time").val();
	//deviceTypeId=$("select[id='device_type']").val();
	deviceTypeId = 'mou';// test purpose
	$('#sp_start_date, #sp_start_time, #sp_end_date,  #sp_end_time').calendricalDateTimeRange({
		isoTime:true
	    });
	/*$("#page_tip").colorbox(
	{
	href:"page_tip_sp_monitor_dashboard.py",
	title: "Dashboard",
	opacity: 0.4,
	maxWidth: "80%",
	width:"650px",
	height:"500px",
	onComplte:function(){}
	});*/
	
	/*$("#sp_ad_graph").click(function(){
		parent.main.location="get_ap_advanced_graph_value.py?ip_address='"+String(spIpAddress)+"'&device_type_id="+deviceTypeId;
	});*/
	Highcharts.getOptions().colors = $.map(Highcharts.getOptions().colors, function(color) {
			    return {
				radialGradient: { cx: 0.5, cy: 0.3, r: 0.7 },
				stops: [
				    [0, color],
				    [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
				]
			    };
			});
	
	homeDashboardCreation();
	//specificGenericGraphJson();

});



function homeDashboardCreation(){
	if (homeDashboard) // Clear the dashboard object
		clearInterval(homeDashboard);
		
	yo1 = $("#dashboard1").yoDashboard({
		title:"Host Statistics<span style=\"float:right;margin-right: .5em;\"><a href=\"manage_service.py\">More>></a></span>",
		showRefreshButton:false,
		showNextPreButton:false,
		ajaxRequest:function(div_obj, start,limit,tab_value){
			reachabilityDetails(div_obj.attr("id"));
			return true;
		},
		showTabOption:false,
		height:"220px"
	});
	yo2 = $("#dashboard2").yoDashboard({
		title:"Events Statistics of recent 3 hour<span style=\"float:right;margin-right: .5em;\"><a href=\"status_snmptt.py\">More>></a></span>",
		showRefreshButton:false,
		showNextPreButton:false,
		ajaxRequest:function(div_obj, start,limit,tab_value){
			eventGraphDetails(div_obj.attr("id"));
			return true;
		},
		showTabOption:false,
		height:"220px"
	});
	yo3 = $("#dashboard3").yoDashboard({
		title:"Last 7 Critical Devices<span style=\"float:right;margin-right: .5em;\"><a href=\"status_snmptt.py\">More>></a></span>",
		ajaxRequest:function(div_obj){
			reachabilityHtmlTable(div_obj);
			return true;
		},
		height:"256px"
	});
	
	yo4 = $("#dashboard4").yoDashboard({
		title:"Last 7 Current Events<span style=\"float:right;margin-right: .5em;\"><a href=\"status_snmptt.py\">More>></a></span>",
		ajaxRequest:function(div_obj){
			eventHtmlTable(div_obj);
			return true;
		},
		height:"256px"
	});



    var $right = $("div#home-snapin-container");
    var $left = $("div#home_dashboard_id");
    $("#home_button_div").toggle(
        function(){
            //$left.animate({ width:0},{complete:function(){$(this).hide();}});
            $left.hide();
            //$right.show("slide",{ direction: "right" }, 1000);
            $right.show().animate({ width: "100%" });
            $(this).html("Dasboard");
        },function() {
            //$right.animate({ width: 0},{complete:function(){$(this).hide();}});
            $right.hide();
            //$left.show("slide",{ direction: "left" },1000);
            $left.show().animate({ width: "100%" });
            $(this).html("Snapins");
        });

	hostStatusTable();
	homeDashboard = setInterval(function(){homeDashboardCreation()},300000);

}


function eventHtmlTable(div_obj){
	$.ajax({
		type: "get",
		url: "unmp_common_graph_creation.py?graph_id=mouEventTable&device_type="+deviceTypeId,
		cache:false,
		success:function(result){
			if (result.success == 0)
				div_obj.html(result.table_html);
			else
				div_obj.html("Some Error occured");
		},
		complete : function(){
			$.yoDashboard.hideLoading(yo3);
			}
	});
}

function reachabilityHtmlTable(div_obj){
	$.ajax({
		type: "get",
		url: "unmp_common_graph_creation.py?graph_id=mouReachabilityTable&device_type="+deviceTypeId,
		cache:false,
		success:function(result){
			if (result.success == 0)
				div_obj.html(result.table_html);
			else
				div_obj.html("Some Error occured");
		},
		complete : function(){
			$.yoDashboard.hideLoading(yo4);
			}
	});
	
}

function hostStatusTable(){
	$.ajax({
		type: "get",
		url: "dashlet_hoststats.py",
		cache:false,
		success:function(result){
			$("#dashboard12").html(result);
		}
	});
	
}



function eventGraphDetails(div_id)
{
	$.ajax({
		type: "get",
		url: "unmp_common_graph_creation.py?graph_id=mouEventGraph&device_type="+deviceTypeId,
		cache:false,
		success:function(result){
				// total,free,available,used
				if (result.success == 0){
					chart1 && chart1.destroy();
					chart1 = null;
					Highcharts.setOptions({
						global: {
							useUTC: false
						}
					});

					
					chart1 = new Highcharts.Chart({
						chart: {
							renderTo: div_id,
							plotBackgroundColor: null,
							plotBorderWidth: null,
							plotShadow: false,
							defaultSeriesType: 'column'
						},
						title: {
							text: ''
						},
						xAxis: {
//								type: 'datetime',
								labels: {
									formatter: function() {
									    var hh = Highcharts.dateFormat('%H:%M:%S', this.value);
									    return Highcharts.dateFormat('%H:%M', this.value);
									},
								 style: {
								    	color:(result.timestamp.length<29)?'rgb(102,102,102)':'#FFF',
								    	font: '10px Trebuchet MS, Verdana, sans-serif'
								 }
            							},
            //								labels: {
//									rotation: 0
//									},
								  tickLength: 20,
								  reversed : true,
								categories: result.timestamp
						},
						yAxis: {
							min: 0,
							title: {
								text: ''
							}
						},
							tooltip: {
								crosshairs: true,
								shared: true,
								formatter: function() {
								var s = '<b>'+ 
								(Highcharts.dateFormat('%H:%M',this.x)=="00:00" ? Highcharts.dateFormat('%e. %b %Y', this.x):Highcharts.dateFormat('%e. %b %Y, %H:%M', this.x));
								//Highcharts.dateFormat('%e. %b %Y, %H:%M', this.x)+
								'</b>';
								$.each(this.points, function(i, point) {
								    s += '<br/><span style="color: ' + String(point.series.color) + '">'+ point.series.name +'</span>: '+
									point.y;
								});
								return s;
							    }
								},
						plotOptions: {
							column: {
								stacking: 'normal'
							}
						},
						series: [{
							color:"#90D968",
							name: 'Normal',
							data: result.data[0].normal
						}, {
							color:"#3C9C08",
							name: 'Informational',
							data: result.data[0].inforamtional
						},  {
							color:"#5185C1",
							name: 'Minor',
							data: result.data[0].minor
						},  {
							color:"#ECDA3B",
							name: 'Major',
							data: result.data[0].major
						}, {
							color:"#EB2D23",
							name: 'Critical',
							data: result.data[0].critical
						}]
					});
					$.yoDashboard.hideLoading(yo2);
				}
			}
	});
}


function reachabilityDetails(div_id)
{
	$("#"+div_id).html("<div id=\"dashboard11\"  style=\"height:220px;float:left;\"></div><div id=\"dashboard12\"  style=\"height:220px;float:left;\"></div>");
	$.ajax({
	type: "get",
	url: "unmp_common_graph_creation.py?graph_id=mouReachablity&device_type="+deviceTypeId,
	cache:false,
	success:function(result){
			if (result.success == 0){
				chart2 = null;
				chart2 = new Highcharts.Chart({
					chart: {
						renderTo: "dashboard11",
						plotBackgroundColor: null,
						plotBorderWidth: null,
						plotShadow: false
					},
					title: {
						text: ''
					},
					tooltip: {
						formatter: function() {
							return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.y, 0);
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
					/*plotOptions: {
						pie: {
						    allowPointSelect: true,
						    cursor: 'pointer',
						    dataLabels: {
							enabled: true,
							color: '#000000',
							connectorColor: '#000000',
							formatter: function() {
							    return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
							}
						    }
						}
					    },
					*/
					series: [{
						type: 'pie',
						name: 'Browser share',
						data: [
							{name : 'Up', y :result.data[0].Ok,color:'#1BB62E'},
							{name : 'Down', y : result.data[0].Warning,color:'#ECDA3B'},
							{name : 'Unreachable',y : result.data[0].Critical,color:'#EB2D23'},
							{name : 'Unknown', y : result.data[0].Unknown,color:'#00AAFF'}
						]
					}]
				});
			$.yoDashboard.hideLoading(yo1);
			}
		}
	});
}


function alarmDetail(trap_id,option)
{
	$.colorbox(
	{
		href:"trap_detail_information.py?trap_id="+trap_id + "&option="+option,
		title: "",
		opacity: 0.4,
		maxWidth: "80%",
		width:"536px",
		height:"auto"
	});
}



