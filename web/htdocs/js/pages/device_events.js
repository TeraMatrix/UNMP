var hideShow = null;
var searchFormTable = null;
var $spinLoading = null;
var $spinMainLoading = null;
var $gridViewHostServiceEventsDataTable = null;
var $gridViewHostServiceEventsTableObj = null;

$(function(){
	hideShow = $("#hide_show");
	searchFormTable = $("#search_form_table");
	// spin loading object
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	$gridViewHostServiceEventsTableObj = $("table#grid_view_events_table");
	
	hideShow.toggle(function(){
		var $this = $(this);
		$this.attr("src","images/new/up.png");
		searchFormTable.find("tbody").slideDown();
		$this.attr("original-title","Hide");
	},function(){
		var $this = $(this);
		$this.attr("src","images/new/down.png");
		searchFormTable.find("tbody").slideUp();
		$this.attr("original-title","Show");
	});
	hideShow.tipsy({gravity: 'n'});
	searchEvents();
	$("input#submit").click(function(){
		searchEvents();
	});
});
function searchEvents()
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"search_events.py",
		data:{
			"host":$("#host").val(),
			"service":$("#service").val(),
			"logtime":$("input[name='logtime']:checked").val(),
			"logtime_sec":$("#logtime_sec").val(),
			"logtime_min":$("#logtime_min").val(),
			"logtime_hours":$("#logtime_hours").val(),
			"logtime_days":$("#logtime_days").val(),
			"log_plugin_output":$("#log_plugin_output").val()
		},
		success:function(result){
			$gridViewHostServiceEventsDataTable = $gridViewHostServiceEventsTableObj.dataTable({
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"aaData": result,
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "sTitle": "State" , "sClass": "center", "sWidth": "2%"},
					{ "sTitle": "Time", "sClass": "center", "sWidth": "15%" },
					{ "sTitle": "Host Alias" , "sClass": "center", "sWidth": "10%"},
					{ "sTitle": "Service", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "Event Type", "sClass": "center", "sWidth": "10%" },
					{ "sTitle": "Log Plugin Output", "sWidth": "45%" }
				]
			});
			spinStop($spinLoading,$spinMainLoading);
		}
	});
}
