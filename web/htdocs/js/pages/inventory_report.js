/* Active Host */
var $gridViewActiveHostTableObj = null;
var $gridViewActiveHostDataTable = null;
var $gridViewActiveHostFetched = 0;

/* Disable Host */
var $gridViewDisableHostTableObj = null;
var $gridViewDisableHostDataTable = null;
var $gridViewDisableHostFetched = 0;

/* Discovered Host */
var $gridViewDiscoveredHostTableObj = null;
var $gridViewDiscoveredHostDataTable = null;
var $gridViewDiscoveredHostFetched = 0;

/* Deleted Host */
var $gridViewDeletedHostTableObj = null;
var $gridViewDeletedHostDataTable = null;
var $gridViewDeletedHostFetched = 0;

var $spinLoading = null;
var $spinMainLoading  = null;

$(function(){
	// spin loading object
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	
	// page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
	$("#page_tip").colorbox(
	{
		href:"page_tip_inventory_report.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"600px",
		height:"400px"
	});
		
	/* Call Active Host Data Table */
	$gridViewActiveHostTableObj = $("#grid_view_active_host");
	//gridViewActiveHost();
	
	/* Call Active Host Data Table */
	$gridViewDisableHostTableObj = $("#grid_view_disable_host");
	//gridViewDisableHost();
	
	/* Call Active Host Data Table */
	$gridViewDiscoveredHostTableObj = $("#grid_view_discovered_host");
	//gridViewDeletedHost();
	
	/* Call Active Host Data Table */
	$gridViewDeletedHostTableObj = $("#grid_view_deleted_host");
	//gridViewDiscoveredHost();
	
	/* Bind Function With Tabs */
	

	/* Active Host Tab*/
	$("a#active_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "active";
		if($gridViewActiveHostDataTable == null)
		{
			gridViewActiveHost();
		}
	});
	
	/* Disable Host Tab*/
	$("a#disable_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "disable";
		if($gridViewDisableHostDataTable == null)
		{
			gridViewDisableHost();
		}
	});
	
	/* Discovered Host Tab*/
	$("a#discovered_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "discovered";
		if($gridViewDiscoveredHostDataTable == null)
		{
			gridViewDiscoveredHost();
		}
	});
	
	/* Deleted Host Tab*/
	$("a#deleted_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "deleted";
		if($gridViewDeletedHostDataTable == null)
		{
			gridViewDeletedHost();
		}
	});
	
	/* It Shows Active Host as Default Host Grid View */
	$("a#active_host_tab").click();

/*	gridViewActiveHost();
	gridViewDisableHost();
	gridViewDiscoveredHost();
	gridViewDeletedHost();
*/
	$("div#main_grid_view_div","div#container_body").yoTabs();
});
function gridViewActiveHost()
{
	$gridViewActiveHostDataTable = $gridViewActiveHostTableObj.dataTable({
				"bServerSide": true,
				"sAjaxSource": "grid_view_active_host.py",
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true
			});
			$gridViewActiveHostDataTable.fnSetColumnVis( 0, false,false );
			$gridViewActiveHostDataTable.fnSetColumnVis( 1, false,false );
			$gridViewActiveHostDataTable.fnSetColumnVis( 6, false,false );
/*	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"post",
		url:"grid_view_active_host.py",
		cache:false,
		success:function(result){
			try
			{
				result = eval(result);
				$gridViewActiveHostFetched = 1;
			}
			catch(err)
			{
				result = [];
			}
			//	create data table object
			$gridViewActiveHostDataTable = $gridViewActiveHostTableObj.dataTable({
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"aaData": result,
				"aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
				"bLengthChange":true,
				"sScrollY":String($("div#container_body").height()-150),
				"iDisplayLength":20,
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 1 ] },
					{ "sTitle": "Host Name" , "sClass": "center", "sWidth": "18%"},
					{ "sTitle": "Host Alias" , "sClass": "center", "sWidth": "20%"},
					{ "sTitle": "IP Address", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "Device Type", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "MAC Address", "sClass": "center", "sWidth": "17%" },
					{ "sTitle": " ", "sWidth": "9%", "bVisible": false }
				]
			});
			$gridViewActiveHostDataTable.fnDraw();
			spinStop($spinLoading,$spinMainLoading);
		}
	});*/
}
function gridViewDisableHost()
{

		$gridViewDisableHostDataTable = $gridViewDisableHostTableObj.dataTable({
				"bServerSide": true,
				"sAjaxSource": "grid_view_disable_host.py",
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false
			});
			$gridViewDisableHostDataTable.fnSetColumnVis( 0, false,false );
			$gridViewDisableHostDataTable.fnSetColumnVis( 1, false,false );
			$gridViewDisableHostDataTable.fnSetColumnVis( 6, false,false );
/*	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"post",
		url:"grid_view_disable_host.py",
		cache:false,
		success:function(result){
			try
			{
				result = eval(result);
				$gridViewDisableHostFetched = 1;
			}
			catch(err)
			{
				result = [];
			}
			//	create data table object
			$gridViewDisableHostDataTable = $gridViewDisableHostTableObj.dataTable({
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"aaData": result,
				"aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
				"bLengthChange":true,
				"sScrollY":String($("div#container_body").height()-150),
				"iDisplayLength":20,
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 1 ] },
					{ "sTitle": "Host Name" , "sClass": "center", "sWidth": "18%"},
					{ "sTitle": "Host Alias" , "sClass": "center", "sWidth": "20%"},
					{ "sTitle": "IP Address", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "Device Type", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "MAC Address", "sClass": "center", "sWidth": "17%" },
					{ "sTitle": " ", "sWidth": "9%", "bVisible": false }
				]
			});
			$gridViewDisableHostDataTable.fnDraw();
			spinStop($spinLoading,$spinMainLoading);
		}
	});*/
}
function gridViewDiscoveredHost()
{

			$gridViewDiscoveredHostDataTable = $gridViewDiscoveredHostTableObj.dataTable({
				//"sScrollY": "250px",
				"bServerSide": true,
				"sAjaxSource": "grid_view_discovered_host.py",
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				//"aaData": result,
				//"aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
				"bLengthChange":true
			});
			$gridViewDiscoveredHostDataTable.fnSetColumnVis( 0, false,false );
/*	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"grid_view_discovered_host.py",
		cache:false,
		success:function(result){
			try
			{
				result = eval(result);
				$gridViewDiscoveredHostFetched = 1;
			}
			catch(err)
			{
				result = [];
			}
			//	create data table object
			$gridViewDiscoveredHostDataTable = $gridViewDiscoveredHostTableObj.dataTable({
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"aaData": result,
				"aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
				"bLengthChange":true,
				"sScrollY":String($("div#container_body").height()-150),
				"iDisplayLength":20,
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "sTitle": "Discovery Type", "sClass": "center","sWidth": "20%" },
					{ "sTitle": "IP Address" , "sClass": "center","sWidth": "25%"},
					{ "sTitle": "Mac Address" , "sClass": "center","sWidth": "25%"},
					{ "sTitle": "Discovery Time" , "sClass": "center","sWidth": "30%"}
				]
			});
			$gridViewDiscoveredHostDataTable.fnDraw();
			spinStop($spinLoading,$spinMainLoading);
		}
	});*/
}
function gridViewDeletedHost()
{
			$gridViewDeletedHostDataTable = $gridViewDeletedHostTableObj.dataTable({
				//"sScrollY": "250px",
				"bServerSide": true,
				"sAjaxSource": "grid_view_deleted_host.py",
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				//"aaData": result,
				//"aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
				"bLengthChange":true
			});
			$gridViewDeletedHostDataTable.fnSetColumnVis( 0, false,false );
			$gridViewDeletedHostDataTable.fnSetColumnVis( 1, false,false );
	/*spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"post",
		url:"grid_view_deleted_host.py",
		cache:false,
		success:function(result){
			try
			{
				result = eval(result);
				$gridViewDeletedHostFetched = 1;
			}
			catch(err)
			{
				result = [];
			}
			//	create data table object
			$gridViewDeletedHostDataTable = $gridViewDeletedHostTableObj.dataTable({
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"aaData": result,
				"aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
				"bLengthChange":true,
				"sScrollY":String($("div#container_body").height()-150),
				"iDisplayLength":20,
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 1 ] },
					{ "sTitle": "Host Name" , "sClass": "center", "sWidth": "12%"},
					{ "sTitle": "Host Alias" , "sClass": "center", "sWidth": "15%"},
					{ "sTitle": "IP Address", "sClass": "center", "sWidth": "15%" },
					{ "sTitle": "Device Type", "sClass": "center", "sWidth": "15%" },
					{ "sTitle": "MAC Address", "sClass": "center", "sWidth": "12%" },
					{ "sTitle": "Deleted By", "sClass": "center", "sWidth": "15%" },
					{ "sTitle": "Delete Time", "sClass": "center", "sWidth": "16%" }
				]
			});
			$gridViewDeletedHostDataTable.fnDraw();
			spinStop($spinLoading,$spinMainLoading);
		}
	});*/
}


// Function for inventory report
function inventory_report(){
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"post",
		url:"inventory_reprot_creating.py",
		cache:false,
		success:function(result){
			if (result==1 || result=="1")
			{
				$().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
				spinStop($spinLoading,$spinMainLoading);
				return	;
			}
			else if (result==0 || result=='0')
			{
				$().toastmessage('showSuccessToast', 'Report generated Successfully.');
				window.location = "download/inventory_report.xls";
			}
			else
			{
				$().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');

			}
		spinStop($spinLoading,$spinMainLoading);
		}
		});  
}
